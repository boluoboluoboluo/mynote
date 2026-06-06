import os
import time
from flask import Flask, request, jsonify, render_template, send_from_directory, abort	# type: ignore
import jwt	# type: ignore
from dotenv import load_dotenv # type: ignore
from log import logger,setup_global_logger
import util



app = Flask(__name__,template_folder="templates")

# 手动加载 .env 文件（该方法会默认寻找当前目录或上级目录的 .env 文件）
load_dotenv() 
IS_DEBUG = os.environ.get('DEBUG', 'False').lower() in ['true', '1']	#判断生产和开发模式
setup_global_logger(IS_DEBUG)	#全局设置一次 logger
# 密钥
SECRET_KEY = os.environ.get('SECRET_KEY', '123456')
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'videos')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


logger.info("i'm app.py, init...")

@app.route('/')
def index():
	"""渲染前端主页"""
	return render_template('index.html')

@app.route('/favicon.ico')
def icon():
	return send_from_directory(
		# os.path.join(app.root_path, 'static'), # 静态文件夹路径
		# 'favicon.ico',							# 文件名
		# mimetype='image/vnd.microsoft.icon'   # 声明文件类型
		os.path.join(app.root_path, ''), # 静态文件夹路径
		'favicon.ico',							# 文件名
		mimetype='image/vnd.microsoft.icon'   # 声明文件类型
	)

# =======================================================
# 1. 视频上传与自动【预切片】接口
# =======================================================
@app.route('/api/upload', methods=['POST'])
def upload_video():
	if 'video' not in request.files:
		return jsonify({"code": 400, "msg": "未找到视频文件"}), 400
	file = request.files['video']
	if file.filename == '':
		return jsonify({"code": 400, "msg": "文件名为空"}), 400
	# 1. 保存原始 MP4 文件
	video_id = str(int(time.time())) # 用时间戳作为视频唯一ID
	output_dir = os.path.join(UPLOAD_FOLDER, video_id)
	os.makedirs(output_dir, exist_ok=True)
	mp4_path = os.path.join(output_dir, "input.mp4")
	file.save(mp4_path)

	# 2. 调用 FFmpeg 命令行进行 HLS 切片
	# -hls_time 5: 每 5 秒切一刀
	# -hls_playlist_type vod: 点播模式
	m3u8_path = os.path.join(output_dir, "playlist.m3u8")
	ffmpeg_cmd = [
		"ffmpeg", "-i", mp4_path,
		"-c:v", "libx264", "-c:a", "aac", "-strict", "-2",
		"-f", "hls", "-hls_time", "5", "-hls_list_size", "0",
		"-hls_playlist_type", "vod",
		"-hls_segment_filename", os.path.join(output_dir, "seg_%03d.ts"),
		m3u8_path
	]
	# 对视频切片
	try:
		util.ffmpeg_splice(ffmpeg_cmd)		# 说明:如果视频数据大,可使用多线程,否则容易出现超时
		os.remove(mp4_path)
		return jsonify({"code": 200, "msg": "上传成功"}), 200
	except Exception as e:
		return jsonify({"code": 500, "msg": "视频切片出错"}), 500
	
	
# =======================================================
# 2. 获取视频播放鉴权（生成动态 Token）
# =======================================================
@app.route('/api/get_auth')
def get_video_auth():
	video_id = request.args.get('video_id')
	if not video_id:
		return jsonify({"code": 400, "msg": "缺少参数 videoId"}), 400
	
	# 生成一个有效期仅 10 分钟的 Token
	payload = {
		"video_id": video_id,
		"exp": int(time.time()) + 600  # 10分钟后过期
	}
	token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

	return jsonify({
		"code": 200,
		"url": f"/media/{video_id}/playlist.m3u8",
		"token":token
	})

# =======================================================
# 3. 视频切片分发（严格校验 Token）
# =======================================================
@app.route('/media/<video_id>/<filename>')
def serve_video(video_id, filename):
	token = request.args.get('token')
	if not token:
		abort(403, description="Access Denied: Missing Token")

	try:
		# 解密并验证 Token
		payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
		if payload.get("video_id") != video_id:
			abort(403, description="Access Denied: Invalid Video ID")
	except jwt.ExpiredSignatureError:
		abort(403, description="Access Denied: Token Expired")
	except jwt.InvalidTokenError:
		abort(403, description="Access Denied: Invalid Token")

	# 校验通过，安全发送切片文件
	video_dir = os.path.join(UPLOAD_FOLDER, video_id)
	return send_from_directory(video_dir, filename)


# 本地测试运行: python app.py
# 生产服务器用gunicorn加载app实例,不运行该方法
if __name__ == '__main__':
	current_port = os.environ.get('PORT')
	# app.run(host='0.0.0.0', port=5000)	# 允许任何 IP 访问，并指定端口
	app.run(port=current_port, debug=IS_DEBUG)