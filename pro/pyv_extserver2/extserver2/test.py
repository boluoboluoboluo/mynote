#用于临时 写测试用例
import service

import httpx	#type:ignore
import asyncio
import uuid
import config
import os
import shutil
import util

# url = "http://www.baidu.com"
# r = httpx.get(url)

# print(len(r.text))


# url = "https://video.twimg.com/ext_tw_video/2060436620588027904/pu/pl/avc1/720x1280/hsHqr0cUYqLAyne2.m3u8"
# asyncio.run(service.down_m3u8_file(url,{}))

async def main():

	video_url = "https://video.twimg.com/ext_tw_video/2060436620588027904/pu/pl/avc1/720x1280/hsHqr0cUYqLAyne2.m3u8"
	audio_url = "https://video.twimg.com/ext_tw_video/2060436620588027904/pu/pl/avc1/720x1280/hsHqr0cUYqLAyne2.m3u8"
	headers = ""

	outfile = f"{config.DOWN_DIR}/{uuid.uuid4().hex}.mp4"	# 最后生成的文件
	v_tmp_dir,v_tsfile,a_tmp_dir,a_tsfile = "","","",""
	try:
		v_tmp_dir,v_tsfile = await service.down_m3u8_file(video_url,headers)		# 下载视频数据
		if audio_url:	# 如果有音频url
			a_tmp_dir,a_tsfile = await service.down_m3u8_file(audio_url,headers)	# 下载音频数据
		# 合并
		await util.ffmpeg_merge(v_tsfile,a_tsfile,outfile)	# 封装
		print("视频下载完成.")
	finally:
		# 清理临时文件
		if os.path.exists(v_tmp_dir):shutil.rmtree(v_tmp_dir)
		if os.path.exists(a_tmp_dir):shutil.rmtree(a_tmp_dir)
		print("临时文件清理完毕.")

asyncio.run(main())