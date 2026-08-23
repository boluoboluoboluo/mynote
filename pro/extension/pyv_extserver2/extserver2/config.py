import httpx    #type:ignore

DOWN_DIR = "./down"		#文件下载目录
RETRY_TIMES = 3			#网络下载重试次数

# PROXY = "socks5h://127.0.0.1:21881"		# westworld代理
# PROXY = "socks5h://127.0.0.1:7897"		# clash 代理
PROXY = "socks5h://127.0.0.1:7993"		# uniclash代理

MAX_CONNECT_TASKS = 5		#异步最大并发

TASKS_LIMIT_SIZE = 20*1024*1024   #20M, 超过20M启用并发
TASKS = 5                   #并发数

global_client: httpx.AsyncClient = None       #全局网络下载连接池,实例启动时初始化
global_semaphore = None     #控制全局并发的信号量
global_find_ids = {}       #全局,每个下载的进度统计


