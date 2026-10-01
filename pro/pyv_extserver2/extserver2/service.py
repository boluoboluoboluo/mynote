import util
import config
import uuid
import os
import asyncio
import aiofiles	#type:ignore

#===========================================
# 全局信号量,并发时竞争同一个信号量, 用于控制并发数量
semaphore = asyncio.Semaphore(config.MAX_CONNECT_TASKS)

#===========================================
# 下载 m3u8 文件
# client: httpx异步请求连接池,用于下载
# m3u8_url: m3u8 文件地址
# tmp_dir: 下载的分片保存的目录
#===========================================
async def down_m3u8_file(client,m3u8_url,tmp_dir):
	# 1.下载 m3u8 索引文件
	r = await client.get(m3u8_url)
	r.raise_for_status()
	# -----------------------------
	# 2.解析 m3u8 text
	media_urls = util.parse_m3u8_text(r.text,m3u8_url)
	print(f"分片数量:{len(media_urls)}")
	print(media_urls)
	# -----------------------------
	# 3.下载所有分片
	os.makedirs(tmp_dir,exist_ok=True)
	try:
		async with asyncio.TaskGroup() as tg:
			# 使用任务组管理(asyncio.TaskGroup): 1个任务异常,其他任务全部中止
			for mu in media_urls:
				tg.create_task(util.down_file(client,mu["url"],semaphore,f"{tmp_dir}/{mu['filename']}"))	# 创建并运行任务
	except Exception as e:
		print(f"下载中止了: [错误类型:{type(e).__name__},错误信息:{str(e)}")
		raise
	print("本次文件的分片下载完成.")
	# -----------------------------
	# 4.将 m3u8分片 拼接成 总分片 文件
	all_tsfile = f"{tmp_dir}/all.ts"	# 总分片名
	async with aiofiles.open(all_tsfile,"ab") as outf:
		for mu in media_urls:
			async with aiofiles.open(os.path.join(tmp_dir,mu["filename"]), "rb") as inf:
				while True:
					chunk = await inf.read(1024 * 1024)  # 每次读写 1MB
					if not chunk:
						break
					await outf.write(chunk)
	print(f"分片 {all_tsfile} 拼接完成")
	# -----------------------------
	# 5.返回
	# 返回总分片文件,用于后续处理,ffmpeg合并等
	return all_tsfile