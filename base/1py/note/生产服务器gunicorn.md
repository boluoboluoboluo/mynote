#### 说明

```sh
# python原生或者flask框架 自带的开发服务器是单线程的，性能极差且有安全漏洞
# 线上优先改用 Gunicorn（Linux 首选）

# 安装
pip install gunicorn # 服务器上额外安装生产级服务器,轻量优秀

# 启动
gunicorn -w 4 -b 127.0.0.1:8000 app:app		# 本地访问,远程访问为: 0.0.0.0:8000
	-w 4：开启 4 个工作进程（并发能力暴增）
	app:app：代表寻找 app.py 文件里的 app 这个 Flask 实例。

# 访问:
http://127.0.0.1:8000

========================
# 注意,不需要再执行 python3 app.py 
# app.py 里的app.run()方法不会执行,因为此时app.py被当作模块加载

```

#### 系统常驻服务

项目根目录新建启动配置文件 `gunicorn.conf.py`, 内容如下:

```py
# gunicorn.conf.py
# import multiprocessing

# 说明 gunicorn 启动参数配置文件,用于linux服务器

# 1. 绑定的端口和并发 Worker 数
bind = "127.0.0.1:8000"
# 进程数目,或者使用 multiprocessing.cpu_count() * 2 + 1 自动计算
workers = 4  

# 2. 运行时临时文件隔离（彻底解决你刚才遇到的权限神坑）
pidfile = "/run/gunicorn/gunicorn.pid"
worker_tmp_dir = "/run/gunicorn/"

# 3. 日志配置
# 日志目录 my_pro 需先创建,并改所有者为 www-data:www-data
errorlog = "/var/log/my_pro/gunicorn_error.log"
#只记录error日志
loglevel = "error"	
```

在`/etc/systemd/system/`目录下新建服务文件 `sudo vi my_pro.service`, 内容如下:

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
WorkingDirectory=/var/www/vpro/my_pro

# 运行目录,相对路径,绑定到/run目录下的
RuntimeDirectory=gunicorn

# 3. 核心：调用【虚拟环境】里的 Gunicorn 来启动服务
# 注意：一定要写绝对路径！
# app:app 代表“app.py里的app对象”,项目根目录下
# gunicorn.conf.py 为启动配置,项目根目录下
ExecStart=/var/www/vpro/venv/bin/gunicorn -c gunicorn.conf.py app:app

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
```

#### 日志切割

使用`Linux` 自带的 `logrotate `工具, 在` /etc/logrotate.d/ `目录新建切割配置文件, 

`sudo nano /etc/logrotate.d/gunicorn`

内容如下: **(里面不要有注释!)** 

```sh
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
```

```sh
# 相关参数说明:

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
```

```sh
# 手动触发一次,检查配置文件
# -f 代表强制立刻轮转（Force），-v 代表打印详细过程（Verbose）
sudo logrotate -fv /etc/logrotate.d/gunicorn
	-- 提示 renaming ... to ...，就说明已经完美切割成功
```

#### 部署

```sh
# Gunicorn 已将代码加载进内存, 单例模式,
# 同一个进程接管的所有请求到来都是访问同一个代码内存, (警惕内存泄漏)
# 更新代码需要重启服务:
sudo systemctl restart my_flask
```

