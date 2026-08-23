import subprocess
import re
# pip install requests
# pip install requests[socks]	#代理走 socks 协议,需要安装这个(安装即可,不需要额外的代码)
import requests #type:ignore
import config
import time
import random
from urllib.parse import urlsplit

#===========================================
# 使用 ffmpeg 封装视频
#===========================================
def ffmpeg_pack(file_path,outfile):
	ffmpeg_cmd = ["ffmpeg","-loglevel", "quiet","-i",file_path,"-c","copy",outfile]
	subprocess.run(ffmpeg_cmd,check=True)
#===========================================
# ffmpeg 合并音视频
#===========================================
def ffmpeg_merge(v_path,a_path,outfile):
	ffmpeg_cmd = ffmpeg_cmd = ["ffmpeg","-loglevel", "quiet","-i",v_path,"-i",a_path,"-c","copy",outfile]
	subprocess.run(ffmpeg_cmd,check=True)
#===========================================
# 解析 m3u8 媒体文件内容,得到分片地址列表
#===========================================
def parse_m3u8_media(text,m3u8_url):
	parsed = urlsplit(m3u8_url)
	# 分片前缀,根据分片地址使用,如果分片地址斜杠开头为绝对地址,和域名拼接 使用 base_urls[0]
	# 否则为相对地址,和 m3u8_url 最后一个 / 前面的部分做拼接,使用 base_urls[1]
	base_urls = [f"{parsed.scheme}://{parsed.netloc}",f"{m3u8_url.rsplit('/', 1)[0]}/"]	# 分片前缀,根据分片地址使用
	media_urls = []
	i = 1	# 记录分片顺序
	arr = text.split("\n")
	for line in arr:
		line = line.strip()
		if "EXT-X-MAP:URI" in line:	# 分片首部
			tmpinfo = re.search(r'EXT-X-MAP:URI="([^"]+)"',line)	# 分片首部 url
			url = f"{base_urls[0]}{tmpinfo[1]}" if tmpinfo[1].startswith("/") else f"{base_urls[1]}{tmpinfo[1]}"
			media_urls.insert(0,{"name":"file0.ts","url":url})	# 放到最前面
		elif line and not line.startswith("#"):
			url = f"{base_urls[0]}{line}" if line.startswith("/") else f"{base_urls[1]}{line}"
			media_urls.append({"name":f"file{str(i)}.ts","url":url})		# 其他分片 url
			i = i+1
		else:
			pass
	return media_urls
#===========================================
# 流式下载,写入本地,重试机制
# url: 下载的 url
# session: requests打开的 session 连接
# fout: 保存到本地的文件流
#===========================================
def down_file(url,session,fout):
	for i in range(config.RETRY_TIMES+1):
		try:
			rs = session.get(url,stream=True,timeout=20)
			rs.raise_for_status()  # 检查 HTTP 状态码是否正常
			for chunk in rs.iter_content(chunk_size=512*1024):	#512KB
				fout.write(chunk)
			break
		except requests.RequestException as rqe:
			if i == config.RETRY_TIMES:
				raise Exception(f"网络下载出错,重试次数达到上限,报错原因:{rqe}")
			print("网络下载出错,正在重试...")
			time.sleep(random.uniform(1, 3)) 	#随机停 1~3 秒
		except Exception as e:
			raise e
#===========================================
# 创建下载会话 session
#===========================================
def create_session():
	# 启用session下载
	session = requests.Session()
	session.trust_env = False # 强制它只听代码的，别乱看系统的(代理)
	session.proxies = config.PROXIES	# 设置代理
	# session.headers.update({
	# 	# 告诉服务器：请直接给我原始数据，别压缩.
	# 	# 正常情况,不要这么做,不压缩会导致数据量变大很多
	# 	# 特殊情况:
	# 	#   对于服务器某些压缩算法,可能导致拿到的数据无法解压缩,可以设置这个
	# 	#   某些时候使用了代理导致网络异常的时候,可以尝试这个参数
		
	# 	# 'Accept-Encoding': 'identity', 
	# })
	return session