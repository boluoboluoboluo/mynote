
TMP_DIR = "./tmp"		#文件下载临时目录
RETRY_TIMES = 3			#网络下载重试次数
#vpn代理
PROXIES = {
		# "http": "http://127.0.0.1:7897",  # 假设你的代理端口是 7890
		# "https": "http://127.0.0.1:7897"  # 
		"http": "socks5h://127.0.0.1:21881",  # 
		"https": "socks5h://127.0.0.1:21881"  # 
	}