#### 说明
```sh
# 功能:
配合浏览器插件,作为后端服务,提供下载功能

# 技术点:
1.FastAPI 	# 基于ASGI协议,原生支持异步非阻塞io	轻量
2.Httpx		# 用于异步下载
3.aiofiles	# 用于异步io写磁盘
5.ffmpeg	# 用于音视频处理(合并等..)

```

#### 准备

```sh
# 系统环境
1.安装python
2.安装ffmpeg

# python 安装依赖
pip install fastapi uvicorn httpx aiofiles
pip install httpx[socks]
pip install httpx[http2]

	# 说明:
	-- uvicorn #启动 FastAPI 服务的必备容器

```

#### 启动

```sh
# 终端命令:
uvicorn app:app --host 127.0.0.1 --port 8000
	-- 主文件为app.py ,里面有个app实例
```



#### 生产环境

```sh
# 使用 gunicorn 进程管理 uvicorn, Gunicorn 当老大，带一帮 Uvicorn 当小弟
# 安装
pip install gunicorn
# 命令:
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
	# 参数说明:
	-k uvicorn.workers.UvicornWorker：告诉 Gunicorn，请使用 Uvicorn 作为你的执行员工。

```

#### 其他

```sh
# 注意:
不要用reload 方式启动,会导致ffmpeg调用失败
uvicorn app:app --reload --port 8000		# 不要用这个命令
```



