import service
import util
import uuid
import config
import os
import json
import asyncio
import shutil
import httpx	#type:ignore
from contextlib import asynccontextmanager
from fastapi import FastAPI, BackgroundTasks,Request	#type:ignore
from fastapi.middleware.cors import CORSMiddleware	#type:ignore
# import tracemalloc

#===========================================
# 上下文管理
@asynccontextmanager
async def lifespan(app: FastAPI):
	# -----------------------------
	# 【项目启动时】
	os.makedirs(config.DOWN_DIR,exist_ok=True)	# 下载目录初始化
	config.global_semaphore = asyncio.Semaphore(5)     #全局控制并发信号量,控制多用户并发,此处用于ffmpeg合并时,保护cpu和内存资源
	# 连接池,全局单例
	config.global_client = httpx.AsyncClient(
		# headers={"User-Agent": "Mozilla/5.0 ..."}, # 提取公共 headers
		http2=True, 				# 开启全局 HTTP/2
		proxy=config.PROXY,			# 全局走代理
		limits=httpx.Limits(
			max_connections=1000,	# 限制最大总连接数，防止内存爆掉
			max_keepalive_connections=200	# 允许复用的空闲连接数
		)
	)
	yield
	# -----------------------------
	# 【项目关闭时】
	try:
		# 强制 3 秒内如果不关闭就直接中断，绝不卡死 Ctrl+C
		await asyncio.wait_for(config.global_client.aclose(), timeout=3.0)
		print("服务停止..")
	except asyncio.TimeoutError:
		print("警告：关闭服务超时，已强行忽略并退出服务！")

#===========================================
app = FastAPI(lifespan=lifespan)		#fastapi 实例
# 允许浏览器插件跨域访问（CORS）
app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],  # 生产环境建议改为你插件的 ID 或具体域名
	allow_methods=["*"],
	allow_headers=["*"],
)

#===========================================
# normal url 下载
#===========================================
@app.post("/down_normal")
async def down_normal(request:Request, background_tasks: BackgroundTasks):
	# 获取请求参数
	data = await request.json()		# 直接从请求中获取 JSON 字典
	video_url = data.get("video_url")
	audio_url = data.get("audio_url")
	headers = data.get("headers") # 这里拿到的就是你前端传的 headers 字典或字符串
	print(f"video_url:{video_url}")
	print(f"audio_url:{audio_url}")
	print(f"headers:{headers}")
	print()
	del headers["Range"]			# 去掉请求头的Range字段,否则只会下载部分内容
	# -----------------------------
	try:
		# 1.head 请求查看被下载文件大小
		r = await config.global_client.head(video_url,headers=headers)
		r.raise_for_status()
		# print("head请求:",r.headers)	# httpx 已经把请求头字段转为小写了
		total_size = int(r.headers.get("content-length")) if "content-length" in r.headers else 0
		# -----------------------------
		# 2.下载进度数据
		task_id = uuid.uuid4().hex	# 本次下载任务id
		config.global_find_ids[task_id] = {"total_size":total_size,"has_download":0,"status":0}	# 保存下载文件大小和已下载,用于更新进度,status:0下载中1完成
		# -----------------------------
		# 3.如果存在"Content-Length" "Accept-Ranges",以及"Content-Length">20M,就启用异步下载
		if "content-length" in r.headers and "accept-ranges" in r.headers and total_size > config.TASKS_LIMIT_SIZE:
			print(f"正常并发下载:")
			# 后台任务,下载
			background_tasks.add_task(service.down_async_normal_file,task_id,video_url,headers)
		else: # 3.1常规下载
			print(f"正常下载:")
			background_tasks.add_task(service.down_normal_file,task_id,video_url,headers)
		# -----------------------------
		# 4.立即返回
		return {"error":0,"task_id":task_id}
	except Exception as e:
		print(f"error: [错误类型:{type(e).__name__},错误信息:{str(e)}")
		return {"error":1,"msg":"down error.."}

#===========================================
# m3u8 url 下载
#===========================================
@app.post("/down_m3u8")
async def down_m3u8(request:Request, background_tasks: BackgroundTasks):
	# 获取请求参数
	data = await request.json()		#直接从请求中获取 JSON 字典
	video_url = data.get("video_url")
	audio_url = data.get("audio_url")
	headers = data.get("headers") # 这里拿到的就是你前端传的 headers 字典或字符串
	print(f"video_url:{video_url}")
	print(f"audio_url:{audio_url}")
	print(f"headers:{headers}")
	print()
	
	try:
		total_size = 0		# 总大小,用于统计进度
		video_media_urls = []	# 视频分片地址列表
		audio_media_urls = []	# 音频分片地址列表
		# -----------------------------
		# 1.下载视频 m3u8 索引文件
		r = await config.global_client.get(video_url,headers=headers)
		r.raise_for_status()
		# 解析 m3u8 text
		video_media_urls = util.parse_m3u8_text(r.text,video_url)
		total_size = total_size + len(video_media_urls)
		# print(video_media_urls)
		# -----------------------------
		# 2.音频:
		if audio_url:
			# 下载音频 m3u8 索引文件
			r = await config.global_client.get(audio_url,headers=headers)
			r.raise_for_status()
			# 解析 m3u8 text
			audio_media_urls = util.parse_m3u8_text(r.text,audio_url)
			total_size = total_size + len(audio_media_urls)
			# print(audio_media_urls)
		# -----------------------------
		# 3.下载进度数据
		task_id = uuid.uuid4().hex	# 本次下载任务id
		config.global_find_ids[task_id] = {"total_size":total_size,"has_download":0,"status":0}	# 保存下载文件大小和已下载,用于更新进度,status:0下载中1完成
		# -----------------------------
		# 4.开启后台任务,(并发)
		background_tasks.add_task(_down_m3u8,task_id,video_media_urls,audio_media_urls,headers)
		# -----------------------------
		# 5.立即返回
		return {"error":0,"task_id":task_id}
	except Exception as e:
		print(f"error: [错误类型:{type(e).__name__},错误信息:{str(e)}")
		return {"error":1,"msg":"down error.."}

async def _down_m3u8(task_id,video_media_urls,audio_media_urls,headers):
	outfile = f"{config.DOWN_DIR}/{uuid.uuid4().hex}.mp4"	# 最后生成的文件
	v_tmp_dir = f"{config.DOWN_DIR}/{uuid.uuid4().hex}"		#视频分片临时目录
	a_tmp_dir = f"{config.DOWN_DIR}/{uuid.uuid4().hex}"		#音频分片临时目录
	os.makedirs(v_tmp_dir,exist_ok=True)
	os.makedirs(a_tmp_dir,exist_ok=True)
	v_tsfile,a_tsfile = "",""
	try:
		# 1.下载
		v_tsfile = await service.down_m3u8_file(task_id,video_media_urls,headers,v_tmp_dir)		# 下载视频数据
		if audio_media_urls:
			# 如果有音频分片地址url
			a_tsfile = await service.down_m3u8_file(task_id,audio_media_urls,headers,a_tmp_dir)	# 下载音频数据
		# -----------------------------
		# 2.视频处理 (合并等)
		await util.ffmpeg_merge(v_tsfile,a_tsfile,outfile)
		print(f"视频下载完成.{outfile}")
		config.global_find_ids[task_id]["status"] = 1		# 进度状态:完成
	except Exception as e:
		del config.global_find_ids[task_id]	# 删除进度
		print(f"error: [错误类型:{type(e).__name__},错误信息:{str(e)}")
	finally:
		# 5.清理临时文件
		shutil.rmtree(v_tmp_dir)
		shutil.rmtree(a_tmp_dir)
		print("临时文件清理完毕.")

#===========================================
# 查询下载进度
#===========================================
@app.post("/find_progress")
async def find_progress(request:Request, background_tasks: BackgroundTasks):
	# 获取请求参数
	data = await request.json()		# 直接从请求中获取 JSON 字典
	task_id = data.get("task_id")	# 安全过滤?
	if task_id in config.global_find_ids:
		process_data = config.global_find_ids[task_id]
		print(f"进度:{json.dumps(process_data)}")
		return process_data
	else:
		return None

#===========================================
# 帮助前端发送请求,
#===========================================
# @app.post("/help_query_data")
# async def help_query_data(request:Request, background_tasks: BackgroundTasks):
# 	# 获取请求参数
# 	data = await request.json()		# 直接从请求中获取 JSON 字典
# 	url = data.get("url")
# 	headers = data.get("headers")
	
# 	print("url:",url)
# 	print("headers",headers)
# 	try:
# 		client = request.app.state.global_client	# 获取全局网络连接池
# 		r = await client.get(url,headers=headers)
# 		print(r.text)
# 	finally:
# 		# 清理临时文件
# 		pass

# 	data = {"status":1,"pg_value":10}
# 	print(json.dumps(data))

#===========================================
# 测试: 百度请求
#===========================================
@app.get("/test_baidu")
async def test_baidu(request:Request, background_tasks: BackgroundTasks):
	headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
	try:
		# client = request.app.state.global_client	# 获取全局网络连接池
		url = "https://www.baidu.com"
		r = await config.global_client.get(url,headers=headers,follow_redirects=True)
		print(r.status_code)
	finally:
		# 清理临时文件
		pass

#===========================================
# 查看内存占用
#===========================================
@app.get("/memory")
def show_memory():
	# 访问此接口可实时查看当前 Python 进程占用的物理内存
	return {"current_memory_mb": util.get_memory_usage()}

#===========================================
# 追踪内存,用于查看哪些代码行消耗了最多内存
# 使用方法:
#	1.先访问 /capture-start	#开始追踪
#	2.请求接口...
#	3.访问 /capture-compare	#会比对出结果
#===========================================
# tracemalloc.start()  # 启动内存追踪
# snapshot1 = None
# @app.get("/capture-start")
# def capture_start():
# 	global snapshot1
# 	snapshot1 = tracemalloc.take_snapshot()
# 	return {"status": "基准快照已记录"}
# @app.get("/capture-compare")
# def capture_compare():
# 	global snapshot1
# 	if not snapshot1:
# 		return {"error": "请先请求 /capture-start"}

# 	snapshot2 = tracemalloc.take_snapshot()
# 	# 对比两个快照，按内存增加大小排序
# 	top_stats = snapshot2.compare_to(snapshot1, 'lineno')

# 	# 格式化输出前 5 个最耗内存的代码位置
# 	result = []
# 	for stat in top_stats[:5]:
# 		result.append(str(stat))
# 	return {"top_leaks": result}