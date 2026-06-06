# import multiprocessing


# 生产服务器 gunicorn 启动参数配置文件
# 仅用于linux服务器
# 需安装 gunicorn 库: pip install gunicorn
# 本地 windows 环境不用理会

# 此文件勿轻易改动,若改动,则服务器的nginx配置,项目常驻服务的配置,logrotate的配置,等都会影响





# 1. 绑定的端口和并发 Worker 数
bind = "127.0.0.1:8000"
# 进程数目,或者使用 multiprocessing.cpu_count() * 2 + 1 自动计算
workers = 4  

# 2. 运行时临时文件隔离（彻底解决你刚才遇到的权限神坑）
pidfile = "/run/gunicorn/gunicorn.pid"
worker_tmp_dir = "/run/gunicorn/"

# 3. 日志配置
# 日志目录blobvideo需先创建,并改所有者为 www-data:www-data
errorlog = "/var/log/blobvideo/gunicorn_error.log"
#只记录error日志
loglevel = "error"	
