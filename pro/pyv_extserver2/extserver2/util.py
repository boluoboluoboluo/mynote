
from urllib.parse import urlsplit
import re
import aiofiles		#type:ignore
import config
import asyncio
import httpx 	#type:ignore

#===========================================
# ffmpeg 合并音视频,如果只有视频,则封装
# v_path: 视频路径	示例: ./down/xxx/all.ts
# a_path: 音频路径	示例: ./down/yyy/all.ts
# outfile: 输出文件路径	示例: ./down/xxxxxxxx.mp4
#===========================================
async def ffmpeg_merge(v_path,a_path,outfile):
	# 1.编写 ffmpeg 音视频处理命令
	ffmpeg_cmd = ["ffmpeg", "-y", "-i", v_path, "-c", "copy", outfile]	# 视频封装命令
	if a_path:	# 如果音频文件不为空,则为合并命令
		ffmpeg_cmd = ["ffmpeg", "-y", "-i", v_path, "-i", a_path, "-c", "copy", outfile]	# 合并命令
	# -----------------------------
	# 2.异步调用 ffmpeg 
	process = await asyncio.create_subprocess_exec(		# 异步方式
		*ffmpeg_cmd,
		stdout=asyncio.subprocess.DEVNULL,	# 标准输出直接丢弃，不打印，不占内存
		stderr=asyncio.subprocess.PIPE	 	# 错误输出接入水管，准备拦截
	)
	# -----------------------------
	# 3.异步等待命令完成
	_, stderr = await process.communicate()
	# 运行出错,抛异常
	if process.returncode != 0:
		error_msg = stderr.decode('utf-8', errors='ignore')
		raise RuntimeError(f"FFmpeg 处理报错！退出码: {process.returncode}，错误原因: {error_msg}")
	
#===========================================
# 解析 m3u8 媒体文件内容,得到分片地址列表
# text: m3u8 索引文件内容文本
# m3u8_url: 索引url,此处用于生成前缀,拼接分片url
# @return: media_urls [返回分片url信息(分片url,和分片下载后保存的文件名)] 示例: [{"filename":"file0.ts","url":"http://xxx"},{}..]
#===========================================
def parse_m3u8_text(text,m3u8_url):
	parsed = urlsplit(m3u8_url)
	# base_urls 为分片前缀部分,用于拼接分片url:
	#	如果分片 uri 以 / 开头,则为绝对地址,和域名拼接, 使用 base_urls[0]
	#	否则为相对地址,和 m3u8_url 最后一个 / 前面的部分做拼接,使用 base_urls[1]
	base_urls = [f"{parsed.scheme}://{parsed.netloc}",f"{m3u8_url.rsplit('/', 1)[0]}/"]	# 分片前缀,根据分片地址使用
	media_urls = []
	i = 1	# 记录分片顺序
	arr = text.split("\n")
	for line in arr:
		line = line.strip()
		if "EXT-X-MAP:URI" in line:	# 分片首部判断
			tmpinfo = re.search(r'EXT-X-MAP:URI="([^"]+)"',line)	# 正则匹配到分片首部 uri 数据
			# 根据规则拼接 分片url
			url = f"{base_urls[0]}{tmpinfo[1]}" if tmpinfo[1].startswith("/") else f"{base_urls[1]}{tmpinfo[1]}"
			media_urls.insert(0,{"filename":"file0.ts","url":url})	# 分片首部 放到最前面
		elif line and not line.startswith("#"):	# 分片 uri 判断
			# 根据规则拼接 分片url
			url = f"{base_urls[0]}{line}" if line.startswith("/") else f"{base_urls[1]}{line}"
			media_urls.append({"filename":f"file{str(i)}.ts","url":url})		# 其他分片 url
			i = i+1
		else:
			pass
	return media_urls
#===========================================
# 下载
# client: httpx的异步的连接池
# url: 下载的目的地址
# semaphore: 全局的信号量
# down_path: 下载后写入到文件
#===========================================
async def down_file(client,url,semaphore,down_path):
	#---------------------------
	# semaphore: 竞争同一个信号量资源, 控制并发数量
	# client.stream: 流式下载
	# aiofiles.open: 异步写文件
	#---------------------------
	async with semaphore:		
		for i in range(config.RETRY_TIMES+1):	# 请求出错 重试机制
			try:
				async with client.stream("GET",url) as res:		# 开启 流式 下载
					res.raise_for_status()
					async with aiofiles.open(down_path, "wb") as f:	#使用 aiofiles 代替普通 open，不阻塞事件循环
						async for chunk in res.aiter_bytes(chunk_size=256*1024):	# 流式下载数据,写入到文件
							await f.write(chunk )
						print(f"分片 {down_path} 下载完成.")
					return	# 下载成功后记得返回,不要再执行for循环
			except httpx.HTTPError as e:
				if i == config.RETRY_TIMES:
					print(f"分片 {down_path} 超过重试次数.")
					raise
				else:
					print(f"分片 {down_path} 正在重试...")
					await asyncio.sleep(1)


