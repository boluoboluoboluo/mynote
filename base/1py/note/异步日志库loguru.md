#### 说明

```sh
# loguru 库

# 它原生支持异步非阻塞配置
enqueue=True	# 配置这个即可

# 异步原理:
# threading（多线程）,queue（内存队列），以及操作系统的 I/O 缓冲区机制
1.Loguru 会在后台开启一个独立的“日志写盘线程”
2.主线程把日志字符串当成一个轻量级的对象，塞进内存里的 queue.Queue（队列）里
3.后台写盘线程从队列里拿出来，慢慢调用操作系统的磁盘 write() 接口去写盘。

# 解释:
-- 日志线程 调用操作系统的 file.write() 后,就会主动释放 GIL 锁
-- 主线程瞬间 获取 GIL 锁
-- 无界队列（不限制大小的 queue.Queue）
```



#### 安装

```sh
# 安装
pip install loguru
```

#### 基本使用

```py
from loguru import logger

# Loguru 默认开箱就带有一个向控制台（标准错误）打印的 Handler。
# 如果想自定义，建议先“清除默认”，再“按需添加”：
logger.remove()

# 示例：添加一个异步写文件的日志器
logger.add(
    "app.log", 
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}", 
    level="INFO",
    enqueue=True # 开启异步无锁模式
)

# 基础打印（5 个常用级别）
logger.debug("低级别的调试信息")
logger.info("普通的日常流水日志")
logger.warning("警告信息")
logger.error("程序遇到了错误")

```



#### 示例

结合 Flask :

```py
from flask import Flask, g, request
import uuid
import sys
from loguru import logger

app = Flask(__name__)

# ─── 核心配置：彻底告别阻塞 ───

# 1. 移除 loguru 默认的控制台输出，防止重复打印
logger.remove()

# 2. 配置文件输出。关键参数：enqueue=True（开启异步内存队列，彻底告别磁盘I/O阻塞）
logger.add(
    "/var/log/nginx/blobvideo_app.log", 
    format="[{time:YYYY-MM-DD HH:mm:ss}] [{level}] [PID:{process}] [{extra[trace_id]}] [{file}:{line}] -> {message}",
    level="INFO",
    rotation="20 MB",   # 满20MB自动切割
    retention="10 days",# 日志只保留10天，防止撑爆磁盘
    enqueue=True        # 核心：开启多线程异步无锁队列！业务线程只管丢数据，不卡顿
)

# 3. 顺便把控制台打印也加上（非阻塞），方便测试
logger.add(sys.stdout, level="INFO", enqueue=True)

# ─── 注册 Flask 钩子：动态注入 TraceID ───

@app.before_request
def before_request():
    # 每次请求生成唯一 TraceID
    g.trace_id = uuid.uuid4().hex[:12]
    # 利用 logger.bind 将 trace_id 绑定到当前请求线程的上下文中
    g.req_logger = logger.bind(trace_id=g.trace_id)
    g.req_logger.info(f"--- 收到请求: {request.method} {request.path} ---")

@app.after_request
def after_request(response):
    g.req_logger.info(f"--- 请求结束 | 状态码: {response.status_code} ---")
    return response

# ─── 业务路由中使用 ───

@app.route('/test')
def test():
    # 生产环境中直接使用 g.req_logger 打印业务日志
    # 它不会引发任何磁盘阻塞，且高并发下自带完美的隔离 TraceID
    g.req_logger.info("正在执行核心业务逻辑...")
    return "Success"

```

#### 补充

```sh
# 切割机制:

# 当每次有新日志准备写入文件时，Loguru 内部会执行一段轻量级的检测代码
# 检测到满足条件，当前正在运行的 Python 进程就会在瞬间执行物理文件操作：
	关闭当前的 app.log，将其重命名（如 app_2026-05-23_12-00-00_001.log），
	接着在原地创建一个全新的 app.log 继续写入。
	整个过程通过内部互斥锁或异步队列保证绝对的数据安全。
```

