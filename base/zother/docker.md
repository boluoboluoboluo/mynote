

```sh
# 说明:
环境隔离,不污染系统,项目所需文件全部在容器里,可一键删除
自带完整linux运行环境,脱离宿主机,启动快
项目一键打包镜像,一次构建到处运行,生产环境标准
```

```sh
#功能:

# 拉取镜像
运行容器,拉取项目镜像

# 项目打包成镜像
自己写的项目使用docker打包成镜像,到处运行
=================================
# 沙盒: (支持一般,多进程不友好)
拉取原生linux系统(原始,纯净),在里面编写项目(及安装所需依赖等),与系统隔离 	
	# 创建容器 (并进入) :
	docker run -it --name my_sandbox -v D:\my_workspace:/workspace ubuntu:latest /bin/bash
		-- D:\my_workspace:/workspace # 表示目录挂载
	# 进入:
	docker start my_sandbox  # 唤醒你的沙盒电脑
	docker exec -it my_sandbox /bin/bash # 再次钻进你的沙盒电脑
	# 删除:
	docker rm -f my_sandbox


```

