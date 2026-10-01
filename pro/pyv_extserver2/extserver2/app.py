import service
import util
import uuid
import config
import os
import shutil
import httpx	#type:ignore
from fastapi import FastAPI, BackgroundTasks,Request	#type:ignore
from fastapi.middleware.cors import CORSMiddleware	#type:ignore

app = FastAPI()		#fastapi 实例
os.makedirs(config.DOWN_DIR,exist_ok=True)	# 下载目录初始化
#===========================================
# 允许浏览器插件跨域访问（CORS）
app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],  # 生产环境建议改为你插件的 ID 或具体域名
	allow_methods=["*"],
	allow_headers=["*"],
)
#===========================================
# m3u8 url 下载
#===========================================
@app.post("/down_m3u8")
async def down_m3u8(request:Request, background_tasks: BackgroundTasks):
	# 直接从请求中获取 JSON 字典
	data = await request.json()
	# 直接通过字典的 key 拿数据
	video_url = data.get("video_url")
	audio_url = data.get("audio_url")
	headers = data.get("headers") # 这里拿到的就是你前端传的 headers 字典或字符串
	print(f"video_url:{video_url}")
	print(f"audio_url:{audio_url}")
	print(f"headers:{headers}")
	print()
	# -----------------------------
	outfile = f"{config.DOWN_DIR}/{uuid.uuid4().hex}.mp4"	# 最后生成的文件
	v_tmp_dir,v_tsfile,a_tmp_dir,a_tsfile = "","","",""
	try:
		# 使用异步连接池方式(httpx.AsyncClient),执行并发任务: 开启hppt2,设置代理,设置公共请求头,设置全局超时时间
		async with httpx.AsyncClient(headers=headers,http2=True,proxy=config.PROXY,timeout=15) as client:
			v_tmp_dir = f"{config.DOWN_DIR}/{uuid.uuid4().hex}"		#临时目录,用于保存请求的分片数据
			v_tsfile = await service.down_m3u8_file(client,video_url,v_tmp_dir)		# 下载视频数据
			if audio_url:	# 如果有音频url
				a_tmp_dir = f"{config.DOWN_DIR}/{uuid.uuid4().hex}"	#临时目录,用于保存请求的分片数据
				a_tsfile = await service.down_m3u8_file(client,audio_url,a_tmp_dir)	# 下载音频数据
			# 视频处理
			await util.ffmpeg_merge(v_tsfile,a_tsfile,outfile)	# 封装
			print(f"视频下载完成.{outfile}")
	finally:
		# 清理临时文件
		if os.path.exists(v_tmp_dir):shutil.rmtree(v_tmp_dir)
		if os.path.exists(a_tmp_dir):shutil.rmtree(a_tmp_dir)
		print("临时文件清理完毕.")

	
