#### 项目说明

```sh
# 该项目为测试项目,功能如下:
	1.上传视频
	2.前端以blob格式播放
	
# 技术点:
	1.pyhton Flask
	2.上传的视频用 ffmpeg 进行切片存储
	3.前端用video.js加载视频流
	
# 目的:熟悉项目上线流程
```

#### 前期工作

```sh
# 安装 ffmpeg:	(windows:略)
sudo apt install ffmpeg		# linux

# 创建项目文件夹 blobvideo
# 创建py虚拟环境:略

pip install Flask PyJWT		# 安装 flask框架,jwt鉴权库
pip install python-dotenv	# 用于加载配置文件(到当前进程环境变量)
pip install loguru			# 异步日志库

# fblobvideo文件结构如下:
blobvideo/
|--.env					# 本地使用的环境配置文件 (不提交到服务器)
|--.env.production		#生产环境配置文件 (文件名改成.env 上传到服务器即可)
|-- app.py        		# Python 后端主程序
|-- templates/
|	|-- index.html 		# 前端播放页面
|--videos/              # 存放视频的文件夹（代码会自动创建）
|--static/
| 	|--video.min.js
|	|--video-js.css
|--gunicorn.conf.py		#生产服务器参数配置(Linux) 本地不适用 (勿动即可)
|--log.py				#日志模块
|--util.py				#工具,ffmpeg切片方法等
|--favicon.ico			#图标
|--requirements.txt		#依赖清单
```

#### 代码

参考项目代码

#### 启动

```sh
python app.py	# 仅用于本地开发时执行

# 打开浏览器访问：
http://127.0.0.1:5000
```

#### 上线

##### 思路整理

```sh
# 步骤:
1.服务器安装python环境,ffmpeg,nginx
2.创建python虚拟环境目录,在目录下创建虚拟环境	  #注意目录权限
3.拷贝项目目录到虚拟环境						#注意目录权限
4.创建日志目录								#注意目录权限
5.激活虚拟环境,安装依赖清单
6.测试1:		#pyton3 app.py 测试
-------------
7.虚拟环境安装gunicorn
8.测试2:		# gunicorn 启动服务 ...
-------------
9.创建nginx配置		#nginx配置,反向代理到gunicorn
10.测试3:		# nginx 服务
-------------
11.创建常驻服务 (自启动)		#system 配置
12.测试4:		# 


# 路径整理:
项目目录:		/var/www/pyv_blobvideo/blobvideo
nginx配置:	 /etc/nginx/conf.d/blobvideo.conf
常驻服务配置:		/etc/systemd/system/blobvideo.service
-------------
ngxin日志		/var/log/nginx/access.log 和 error.log
gunicorn日志	/var/log/blobvideo/gunicorn_error.log
项目日志	  /var/log/blobvideo/app.log
-------------
gunicorn切割配置	/etc/logrotate.d/gunicorn

```

##### 打包

```sh

# js压缩: 略
# python核心文件编译成二进制: 略	(无)
================
# 本地导出依赖清单
	pip freeze > requirements.txt
# 项目打包zip,略
# 使用sftp上传到服务器: 
	sftp username@ip -p port 
	input:<pass>
	put blobvideo.zip /home/dbn/	#注意检查 .开头的文件
```

##### 服务器python环境

```sh
sudo apt update
# 安装 Python3 的完整版、pip 以及开发必备的依赖环境
sudo apt install python3 python3-pip python3-venv -y

# 检查 Python 版本
python3 --version
# 检查 Pip 版本
pip3 --version
```

##### 项目初始化工作

```sh

# 创建py虚拟环境目录 /var/www/pyv_blobvideo
	cd /var
	sudo mkdir www
	#修改目录属主,不要用root权限 (重要!) 
	#/var/www 默认为www-data用户的家目录,项目运行时第三方调用(比如gunicorn)会在该目录写入临时数据
	#所以需要设置权限属主为www-data
	sudo chown -R www-data:www-data www
	cd www
	sudo mkdir pyv_blobvideo
	
# 创建python虚拟环境
	cd /var/www/pyv_blobvideo
	python3 -m venv venv	#linux 不要使用名称: env	此命令不要用sudo 权限 (重要!)

# 拷贝项目
	cd /home/dbn
	unzip blobvideo.zip 	#解压
	mv blobvideo /var/www/py_blobvideo/
	#将项目根目录及其所有子目录的权限改为 755（主人可读写执行，其他人可读可进入） !不修改文件!
	cd /var/www/pyv_blobvideo
	sudo find ./blobvideo -type d -exec chmod 755 {} +	#高效命令

# 修改上传目录权限
	cd blobvideo
	sudo find ./videos -type d -exec chmod 755 {} \;	#修改目录权限
	sudo find ./videos -type f -exec chmod 644 {} \;	#修改文件权限,不能给执行权限!

	# 说明: 默认上传权限为当前 服务用户权限-umask, (一般为 666-022)

	
# 创建项目日志目录
    cd /var/log
    mdkir blobvideo
    sudo chown -R www-data:www-data /var/log/blobvideo	#权限配置

# 安装项目依赖
	cd /var/www/pyv_blobvideo
	source venv/bin/activate		#激活虚拟环境
	pip install --upgrade pip		#虚拟环境更新pip !
	cd blobvideo					#进入项目
	pip install -r requirements.txt	#安装项目依赖

# 运行测试:
	python3 app.py

# 访问:
http://127.0.0.1:5000
	#远程如不能访问,需要更改代码,flask app实例,监听所有ip地址:
	app.run(host='0.0.0.0', port=5000)		#由于后续使用nginx,此方式只用于测试
	
```

##### 后端服务引擎

```sh
# 说明:
# 不要用app.run()：
# Flask 自带的开发服务器是单线程的，性能极差且有安全漏洞。
# 线上必须改用 Gunicorn（Linux 首选）或 Waitress（Windows 服务器首选）

# 服务器上额外安装生产级服务器,轻量优秀,安装:
pip install gunicorn

# 启动:
#注意,不需要再执行 python3 app.py 了
# app.py 里的main方法不会执行,因为此时app.py被当作模块加载
gunicorn -w 4 -b 127.0.0.1:8000 app:app		
	-w 4：开启 4 个工作进程（并发能力暴增）
	app:app：代表寻找 app.py 文件里的 app 这个 Flask 实例。
	
	
# 访问:
http://127.0.0.1:8000
```

##### Nginx

```sh
# 安装: 
sudo apt install nginx	#安装后,即启动了,并自启动状态,监听80端口

#配置文件路径:
/etc/nginx/nginx.conf

# 通常在 /etc/nginx/conf.d/ 下创建独立配置文件 blobvideo.conf,
cd /etc/nginx/conf.d
sudo vi blobvideo.conf
#内容如下:
server {
    listen 80;
    server_name your_domain.com; # 你的域名或服务器IP

    # 1. 静态文件由 Nginx 直接读取，不经过 Python，速度极快
    location /static/ {
        alias /var/www/pyv_blobvideo/blobvideo/static/;
        expires 7d; # 缓存 7 天,告诉浏览器：这个文件 7 天内不要再向服务器要了
    }

    # 2. 动态请求转发给后端的 Gunicorn
    location / {
        proxy_pass http://127.0.0.1:8000;	#Gunicorn 监听的地址
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        
        # 调整超时时间，防止大请求报 504 timeout
        proxy_read_timeout 60s;
        # 允许上传的最大文件大小，防止报 413 Too Large
        client_max_body_size 20m; 
    }
}

# 语法检查:
sudo nginx -t

# 注意: nginx开启的时候默认在下面这个文件会开启80端口,请注意
etc/nginx/sites-enabled/default		#这是个软连接,删除即可

# 重启
sudo systemctl reload nginx

# 访问:
http://ip
```

##### 常驻服务

**创建服务文件** `/etc/systemd/system/blobvideo.service` , 示例如下 : (创建后不用改权限)

```sh
#注意,注释必须单独写一行

[Unit]
Description=Gunicorn instance to serve Flask Application
#网络启动后再启动本服务
After=network.target	

[Service]
# 1. 运行该服务的 Linux 用户和组（出于安全考虑，千万不要用 root，改用普通用户）
User=www-data
Group=www-data

# 2. 你的 Python 项目在服务器上的绝对根目录
WorkingDirectory=/var/www/pyv_blobvideo/blobvideo

# 运行目录,相对路径,绑定到/run目录下的
RuntimeDirectory=gunicorn

# 3. 核心：调用【虚拟环境】里的 Gunicorn 来启动服务
# 注意：一定要写绝对路径！
# app:app 代表“app.py里的app对象”,项目根目录下
# gunicorn.conf.py 为启动配置,项目根目录下
ExecStart=/var/www/pyv_blobvideo/venv/bin/gunicorn -c gunicorn.conf.py app:app

# 4. 崩溃重启策略：只要程序死了，10秒后自动拉起复活
Restart=always
RestartSec=10

# 5. 环境变量配置（可以直接在这里注入生产环境参数，解耦代码）,不用这个
#Environment=FLASK_ENV=production
#Environment=SECRET_KEY=your_final_production_key_here

[Install]
#多用户命令行状态（即常规的开机自启）
WantedBy=multi-user.target	

```

**启动并激活** 

```sh
# 刷新 Systemd 系统配置，让它识别新服务
sudo systemctl daemon-reload

# 启动你的 Flask 服务
sudo systemctl start blobvideo

# 将服务设置为【开机自启】（服务器重启后会自动运行）
sudo systemctl enable blobvideo

# 检查服务运行状态
sudo systemctl status blobvideo

# Gunicorn 已将代码加载进内存, 单例模式,
# 同一个进程接管的所有请求到来都是访问同一个代码内存, (警惕内存泄漏)
# 更新代码需要重启服务:
sudo systemctl restart blobvideo
```

#### 日志

##### 规范

```sh
# 规范:
# nginx 记录访问日志
# gunicorn 记录服务错误日志(如服务崩溃,内存溢出等)
# 项目日志 单独记录
```

##### nginx日志

```sh
# 使用默认即可
/var/log/nginx/access.log 和 error.log

# 关于切割:
# 切割nginx日志: nginx安装后logrotate.d/下会建立配置文件,执行切割,使用默认即可
```

##### gunicorn日志

```sh
# 路径:
/var/log/blobvideo/gunicorn_error.log

# 查看:
# Gunicorn 标准输出的日志默认会被系统的 journald 收集,查看如下:
sudo journalctl -u blobvideo.service -f
# 或者是只看最新的 50 行，并进行翻页
sudo journalctl -u blobvideo.service -n 50

# 优化:
# 让 Gunicorn 自己把日志写到特定的文件里
# 在项目根目录 gunicorn.conf.py 里配置

# 关于切割:
使用 Linux 自带的 logrotate 工具, 在 /etc/logrotate.d/ 下为项目新建一个配置

# 切割gunicorn日志:
在 /etc/logrotate.d/ 目录新建切割配置文件:
sudo nano /etc/logrotate.d/gunicorn

#内容如下: (里面不要有注释!)
/var/log/blobvideo/gunicorn_error.log {
    daily                
    missingok            
    rotate 14            
    compress             
    delaycompress        
    notifempty           
    create 0640 www-data www-data  
    sharedscripts        
    postrotate
        /bin/kill -USR1 `cat /run/gunicorn/gunicorn.pid 2>/dev/null` 2>/dev/null || true
    endscript
}

# 手动触发一次,检查配置文件
# -f 代表强制立刻轮转（Force），-v 代表打印详细过程（Verbose）
sudo logrotate -fv /etc/logrotate.d/gunicorn
	-- 提示 renaming ... to ...，就说明已经完美切割成功
	
	
	
----------------
# 配置参数说明:
daily  				 # 每天定时切割一次
missingok            # 如果日志文件不存在，直接跳过不报错
rotate 14            # 最多保留 14 个历史日志文件，旧的自动删除
compress             # 切割后的历史日志自动压缩成 .gz 格式，节省磁盘空间
delaycompress        # 延迟压缩：昨天的日志切出来先不压缩，留到明天再压缩，方便紧急排查
notifempty           # 如果日志文件是空的（大小为 0），则不进行切割
create 0640 www-data www-data  # 切割后自动创建新文件，并指定[权限]以及[所有者/用户组]（请修改为你的实际运行用户）
sharedscripts        # 所有的日志文件切完后，后面的 postrotate 脚本只执行一次
postrotate
        # 核心：切割完成后，向 Gunicorn 的 Master 进程发送 USR1 信号
        # 这会通知 Gunicorn 平滑地关闭旧文件句柄并重新打开新文件，绝对不丢请求、不卡顿
        /bin/kill -USR1 `cat /run/gunicorn/gunicorn.pid 2>/dev/null` 2>/dev/null || true
endscript
----------------
```

##### 项目日志

```sh
# 路径:
/var/log/blobvideo/app.log

# 使用 loguru 库,可以实现异步高效记录日志,安装:
pip install loguru

# 配置: log.py

# 关于切割:
# 切割项目日志: 使用loguru库自带的切割功能 (不使用logrotate,与异步冲突!)
loguru提供功能,log.py 里配置即可

```

#### 其他

##### 热部署

```sh
# 方案一
# gunicorn 天然支持不中断服务的热部署（通过 Linux 的 HUP 信号）

# 操作:
# 向主进程发送 HUP (平滑重启) 信号 即可
kill -HUP $(cat gunicorn.pid)		# gunicorn.pid 文件路径 改成项目里设置的该文件路径
```

```sh
# 方案二
# nginx双端口轮流切换: nginx -s reload Nginx 的自带热部署，瞬间生效

# 操作:
# 服务器跑2个同样的项目实例,运行在不同端口
实例A:5000
备用实例B:5001
# 滚动更新过程:
1.修改ngxin配置,导向B, 执行: nginx -s reload
2.更新代码后,重启A实例
3.修改nginx配置,导向A, 执行: nginx -s reload
4.重启实例B
```



##### 静态资源 缓存加载

```sh
# nginx 静态资源 缓存加载
# 修改了静态资源后,需通过 动态参数 方式获取新版本
# 示例:(引入版本号)
<script src="{{ url_for('static', filename='js/bundle.min.js') }}?v=1.0.1"></script>


```

##### ffmpeg报错记录

```sh
# 如果上传报错,日志看到ffmpeg进程报错:

# 用 www-data 用户执行 ffmpeg 命令排查:
 sudo su -s /bin/bash www-data -c "/usr/bin/ffmpeg -i /var/www/pyv_blobvideo/blobvideo/videos/1779899406/input.mp4 -c:v libx264 -c:a aac -strict -2 -f hls -hls_time 5 -hls_list_size 0 -hls_playlist_type vod -hls_segment_filename /var/www/pyv_blobvideo/blobvideo/videos/1779899406/seg_%03d.ts /var/www/pyv_blobvideo/blobvideo/videos/1779899406/playlist.m3u8"
-- 执行成功,说明命令,权限都没问题

# 问题说明1:
subprocess.run同步进程和gunicorn创建的进程冲突了,无法通过systemd的审查

# 问题说明2:
subprocess.run拉起进程时,Linux 内核会把 FFmpeg 的日志塞进一个大小只有 64KB 的内核内存管道（Pipe Buffer）。FFmpeg 切片时每切一个片就打印好几行进度，大视频很快就会喷出超过 64KB 的文本。

# 死锁发生：
管道满了，Linux 内核为了保护内存，会强行把 FFmpeg 进程挂起（暂停运行），等待 Python 来读走数据。然而，subprocess.run 是一个死板的同步阻塞函数，它的内部逻辑是：“我必须等子进程彻底结束（Exit），我才去读数据。

# 解决办法:
使用 subprocess.Popen ,它是 异步（非阻塞）的,天然免疫死锁
```

##### 关于超时问题

```sh
# 前端超时
-- js fetch请求和Axios库		# 默认无超时
-- nginx超时						# 默认60s	 504 Gateway
-- 数据库连接与执行超时			# 通常 30s - 60s）
-- Gunicorn 的默认超时是	  		# 默认30 秒
	-- 看门狗机制,如果处理某个请求连续 30 秒没有给出任何响应,就超时
-- Chrome 浏览器的硬性超时	  	#通常为 5 分钟（300秒）。主动拒绝并抛出 ERR_TIMED_OUT
-- 云服务器						# 60s, 超时直接断开
-- cdn 							# 硬性死规定是 100 秒, 弹回 524 错误
```

##### 图标

```sh
# favicon.ico 放在网站根目录

# 格式
1.ico 格式
2.png 格式

# 尺寸要求	图标必须是 正方形（1:1 比例）
16 x 16 像素		# 显示在浏览器的标签页（Tab）上
32 x 32 像素		# 显示在浏览器的收藏夹/书签栏中
48 x 48 / 128 x 128 像素	#显示在 Windows 桌面快捷方式或高分辨率屏幕上

# 示例:
-- 找一张png图片(32x3),取名favicon.ico
-- 放网站根目录,设置好路由
-- ctrl+F5,刷新
```

