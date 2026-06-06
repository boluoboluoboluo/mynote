**代码示例** 

```py
#subprocess.Popen

	try:
		# 彻底去掉 check=True，改用 Popen 进行非阻塞捕获
		# stdout/stderr 设置为 PIPE，并使用 communicate 优雅读取
		process = subprocess.Popen(
			ffmpeg_cmd,
			stdout=subprocess.PIPE,
			stderr=subprocess.PIPE,
			text=True
		)
		
		# 强制设置 60 秒超时，防止无限卡死，同时获取输出
		stdout_data, stderr_data = process.communicate(timeout=60)
		
		if process.returncode != 0:
			logger.error(f"【FFmpeg 失败】进程返回码(Exit Code): {process.returncode}")
			logger.error(f"【FFmpeg 错误输出现形】:\n{stderr_data}")
		else:
			logger.error("【FFmpeg 成功】切片已顺利完成！")

	except subprocess.TimeoutExpired as e:
		logger.error("【FFmpeg 严重超时】进程在后台被锁死或卡住。")
		process.kill()
		stdout_data, stderr_data = process.communicate()
		logger.error(f"超时前的错误输出:\n{stderr_data}")
	except Exception as e:
		# 捕获诸如 OSError, PermissionError 等一切系统级异常
		logger.exception("【Subprocess 触发系统级致命异常】")
```

```py
#subprocess.run

	try:
		subprocess.run(ffmpeg_cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
	except subprocess.CalledProcessError as e:
		logger.error(f"FFmpeg 错误输出: {e}")  #
```





**项目里使用ffmepg切片时遇到的问题** 

```sh
# linx系统上:
在后台运行时(非终端):调用 subprocess.run 且没有妥善处理输出，Linux 内核会把 FFmpeg 的日志塞进一个大小只有 64KB 的内核内存管道（Pipe Buffer）。FFmpeg 切片时每切一个片就打印好几行进度，大视频很快就会喷出超过 64KB 的文本。

#死锁发生：
管道满了，Linux 内核为了保护内存，会强行把 FFmpeg 进程挂起（暂停运行），等待 Python 来读走数据。然而，subprocess.run 是一个死板的同步阻塞函数，它的内部逻辑是：“我必须等子进程彻底结束（Exit），我才去读数据。
```

**subprocess.run 和 subprocess.Popen 的本质区别** 

```sh
# 区别
subprocess.run 在 Python 底层就是对 subprocess.Popen 的封装

# subprocess.run 的底层逻辑伪代码：
def run(cmd, ...):
    # 1. 悄悄在底层拉起 Popen
    process = Popen(cmd, ...) 
    
    # 2. 强行卡死当前的 Python 线程，直到子进程自己结束
    process.wait() 
    
    # 3. 结束后，一次性把结果返回给你
    return CompletedProcess(...)

```

|              | `subprocess.run` (上层封装)                           | `subprocess.Popen` (底层核心)                                |
| ------------ | ----------------------------------------------------- | ------------------------------------------------------------ |
| **执行方式** | **同步（阻塞）**。不运行完，代码绝不往下走。          | **异步（非阻塞）**。拉起子进程后，Python 立刻继续往下走。    |
| **控制力**   | 很弱。你无法在它运行期间和它互动。                    | 极强。可以实时读取进度、随时强行杀死（Kill）它。             |
| **管道通信** | 一次性读取。如果数据量过大，极易触发 Linux 管道死锁。 | 可以通过 `.communicate()` 在内存中分批动态清空管道，**天然免疫死锁**。 |

**subprocess.run 比较常用的原因** 

```sh
1.绝大多数场景不需要异步：
绝大多数人调用外部命令只是为了执行一个简单的操作，比如 ls -l 或 mkdir test。这种命令输出极少、瞬间结束，用简单的 run 写起来只有一行代码，最省事。

2.Popen 编写门槛高，容易写出 bug：
Popen 就像一把锋利的手术刀，如果开发者拉起了子进程，却忘记写 .wait() 或 .communicate() 去回收它，这个子进程在执行完后就会变成系统里的僵尸进程（Zombie Process），常年常月耗尽服务器的进程号。网上的教程为了安全，一般不推荐新手使用
```

