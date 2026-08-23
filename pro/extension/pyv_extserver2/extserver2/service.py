import util
import config
import uuid
import os
import asyncio
import aiofiles	#type:ignore
import shutil

#===========================================
# 下载 文件
# task_id: 本次下载任务id
# url: 文件地址
# headers: 请求头
#===========================================
async def down_normal_file(task_id,url,headers):
	tmp_dir = f"{config.DOWN_DIR}/{uuid.uuid4().hex}"		# 下载临时目录
	os.makedirs(tmp_dir,exist_ok=True)
	try:
		down_path = f'{tmp_dir}/{uuid.uuid4().hex}.mp4'			# 下载文件路径
		# 局部信号量,并发时竞争同一个信号量, 用于控制并发数量,每个用户拥有的异步并发数		# 此处主要用于兼容 util.down_normal_file ,没有其他作用
		semaphore = asyncio.Semaphore(config.MAX_CONNECT_TASKS)
		await util.down_normal_file(task_id,url,headers,semaphore,down_path)
		# 移动到下载目录
		if os.path.exists(down_path):shutil.move(down_path,config.DOWN_DIR)
		config.global_find_ids[task_id]["status"] = 1		# 进度状态:完成
	except Exception as e:
		del config.global_find_ids[task_id]	# 删除进度
		print(f"error: [错误类型:{type(e).__name__},错误信息:{str(e)}")
	finally:
		shutil.rmtree(tmp_dir)		# 清理资源

#===========================================
# 异步并发 下载 文件
# url: 文件地址
# tmp_dir: 下载的文件保存的目录
# process_data: 用于统计下载进度的数据信息
#===========================================
async def down_async_normal_file(task_id,url,headers):
	tmp_dir = f"{config.DOWN_DIR}/{uuid.uuid4().hex}"		# 下载临时目录
	os.makedirs(tmp_dir,exist_ok=True)
	try:
		total_size = config.global_find_ids[task_id]["total_size"]
		task_data = []		# 保存任务数据信息:每个任务下载哪些内容,保存到哪个文件等
		# 1.根据任务数,准备每个任务的下载请求数据
		per_task_size = int(total_size / config.TASKS)		# 每个任务需下载的数据大小
		for i in range(config.TASKS):		# 任务数
			tmp_headers = headers.copy()	# 复制一份
			tmp_headers["Range"] = f'bytes={i*per_task_size}-{total_size}' if i == config.TASKS-1 else f'bytes={i*per_task_size}-{i*per_task_size + per_task_size-1}'
			task_data.append({"headers":tmp_headers,"down_path":f'{tmp_dir}/{str(i)}.ts'})
		# -----------------------------
		# 2.开启异步任务管理,运行并发
		async with asyncio.TaskGroup() as tg:
			for d in task_data:
				# 局部信号量,并发时竞争同一个信号量, 用于控制并发数量,每个用户拥有的异步并发数
				semaphore = asyncio.Semaphore(config.MAX_CONNECT_TASKS)
				tg.create_task(util.down_normal_file(task_id,url,d["headers"],semaphore,d["down_path"]))	# 创建并运行任务
		# -----------------------------
		# 3.合并任务下载文件
		out_file = f"{tmp_dir}/{uuid.uuid4().hex}.mp4"	# 总分片名
		async with aiofiles.open(out_file,"ab") as outf:
			for d in task_data:
				async with aiofiles.open(d["down_path"], "rb") as inf:
					while True:
						chunk = await inf.read(1024 * 1024)  # 每次读写 1MB
						if not chunk:
							break
						await outf.write(chunk)
		print(f"文件 {out_file} 合并完成")
		# -----------------------------
		# 4.移动到下载目录
		if os.path.exists(out_file):shutil.move(out_file,config.DOWN_DIR)
		config.global_find_ids[task_id]["status"] = 1		# 进度状态:完成
	except Exception as e:
		del config.global_find_ids[task_id]	# 删除进度
		print(f"error: [错误类型:{type(e).__name__},错误信息:{str(e)}")
	finally:
		shutil.rmtree(tmp_dir)		# 清理资源

#===========================================
# 下载 m3u8 文件
# client: httpx异步请求连接池,用于下载
# m3u8_url: m3u8 文件地址
# tmp_dir: 下载的分片保存的目录
#===========================================
async def down_m3u8_file(task_id,media_urls,headers,tmp_dir):
	# 1.异步并发下载所有分片
	# 局部信号量,并发时竞争同一个信号量, 用于控制并发数量,每个用户拥有的异步并发数
	semaphore = asyncio.Semaphore(config.MAX_CONNECT_TASKS)
	# 使用任务组管理(asyncio.TaskGroup): 1个任务异常,其他任务全部中止
	async with asyncio.TaskGroup() as tg:
		for mu in media_urls:
			tg.create_task(util.down_m3u8_file(task_id,mu["url"],headers,semaphore,f"{tmp_dir}/{mu['filename']}"))	# 创建并运行任务
	print("本次文件的分片下载完成.")
	# -----------------------------
	# 2.将 m3u8分片 拼接成 总分片 文件
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
	# 3.返回
	# 返回总分片文件,用于后续处理,ffmpeg合并等
	return all_tsfile