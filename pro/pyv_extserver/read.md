#### 说明
```sh
# 简单版本,适用自用

# 功能:
配合浏览器插件,作为后端服务,提供下载功能

# 技术点:
1.httpserver	# python 原生服务,单线程
2.requests		# 网络请求库
3.ffmpeg		# 用于处理音视频(合并,等..)

# 思路:
httpserver捕获客户端插件请求,使用requests进行下载,然后ffmpeg合并音视频

```

```sh
# 项目结构:
pyv_extserver	#虚拟环境 (在此目录下创建虚拟环境)
|--extserver	#项目
	 |--tmp		#文件下载临时目录
	 |--app.py	#服务入口文件
	 |--service.py	#业务方法
	 |--config.py	#配置
	 |--util.py		#工具方法
|--run_activate.py	#快捷脚本,激活虚拟环境
|--run_app.py		#快捷脚本,运行项目
|--read.md			#说明文档
```

#### 准备

```sh
# 系统环境
1.安装 python
2.安装 ffmpeg

# python环境
1.创建并激活虚拟环境		#略
2.安装依赖
	pip install requests
	pip install requests[socks]	#代理走 socks 协议,需要安装这个(安装即可,不需要额外的代码)

```

#### 启动

```sh
# 运行:
run_app.py		#快捷脚本,运行项目
```

#### 备注

```sh
# 需要配置代理
config.py 里配置
```

