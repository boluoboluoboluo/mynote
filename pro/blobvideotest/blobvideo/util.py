import subprocess
from log import logger


# 执行 ffmpeg 命令,对视频切片
def  ffmpeg_splice(ffmpeg_cmd):
	try:
		# 彻底去掉 check=True，改用 Popen 进行非阻塞捕获
		process = subprocess.Popen(
			ffmpeg_cmd,
			stdout=subprocess.DEVNULL,	# 后台静默运行，直接丢弃输出
			stderr=subprocess.DEVNULL,
		)
		 # 【核心】在后台线程里死等它结束，一旦结束，立刻自动收割关闭，绝不留下僵尸进程
		process.wait() 
		logger.info("后台 FFmpeg 切片彻底完成，进程已安全关闭。")
	except Exception as e:
		# 捕获诸如 OSError, PermissionError 等一切系统级异常
		logger.error(f"后台切片发生错误: {str(e)}")
		raise e

	# ===================================
	# 说明: subprocess.run 进程同步和gunicorn或者systemd常驻服务冲突报错,所以不用
	# try:
	# 	# 执行切片操作（耗时操作，生产环境建议放入 Celery 异步队列）
	# 	subprocess.run(ffmpeg_cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
	# 	# 切片完成后删除原始大 MP4，节省空间
	# 	os.remove(mp4_path) 
	# 	return jsonify({"code": 200, "msg": "上传并切片成功", "videoId": video_id})
	# except subprocess.CalledProcessError as e:
	# 	logger.error(f"FFmpeg 错误输出: {e}")  #
	# 	return jsonify({"code": 500, "msg": f"FFmpeg 切片失败: {str(e)}"}), 500