import service
import util
import config
import uuid
from http.server import HTTPServer, BaseHTTPRequestHandler
import sys
from urllib.parse import urlparse
import json
import os

class ModernHandler(BaseHTTPRequestHandler):
	# 捕获 http post 请求
	def do_POST(self):
		url_path = urlparse(self.path).path
		if url_path == '/down_m3u8':
			content_length = int(self.headers.get('Content-Length', 0))
			post_body = self.rfile.read(content_length)
			params = json.loads(post_body.decode('utf-8'))
			self._handle_m3u8_request(params)
			self._send_json("已下载.")
		else:
			self._send_json("非法请求")

	#===========================================
	# 处理m3u8下载请求
	#===========================================
	def _handle_m3u8_request(self,params):
		video_url = params.get("video_url")
		audio_url = params.get("audio_url")
		headers = params.get("headers")
		print("video_url:",video_url)
		print("audio_url:",audio_url)
		print("headers:",headers)
		outfile = f"{config.TMP_DIR}/{uuid.uuid4().hex}.mp4"
		v_path = ""
		a_path = ""
		try:
			print("开始下载视频:")
			# 下载视频
			v_path = service.down_m3u8_file(video_url,headers)
			# 有音频就下载音频
			if audio_url:
				print("开始下载音频:")
				a_path = service.down_m3u8_file(audio_url,headers)
				print("开始合并:")
				util.ffmpeg_merge(v_path,a_path,outfile)	#合并
			else:	# 没有音频
				print("开始封装:")
				util.ffmpeg_pack(v_path,outfile)		# 封装成 mp4
			print("全部处理完成.")
		except Exception as e:
			os.path.exists(outfile) and os.remove(outfile)
		finally:
			os.path.exists(v_path) and os.remove(v_path)
			os.path.exists(a_path) and os.remove(a_path)
	
	# json 返回
	def _send_json(self, data):
		self.send_response(200)
		self.send_header('Content-Type', 'application/json')
		self._set_cors_headers() # 关键：发送 CORS 头             #允许跨域
		self.end_headers()
		self.wfile.write(json.dumps(data).encode())
	# 允许跨域的方法
	def _set_cors_headers(self):
		# 允许所有来源访问
		self.send_header('Access-Control-Allow-Origin', '*')
		# 允许的请求方法
		self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
		# 允许的请求头（特别是 Content-Type）
		self.send_header('Access-Control-Allow-Headers', 'Content-Type')

#===========================================		
# main 入口
#===========================================
if __name__ == '__main__':
	httpd = None
	try:
		print("Server: http://localhost:8000")
		httpd = HTTPServer(('localhost', 8000), ModernHandler)
		httpd.serve_forever()		# 这是一个阻塞调用
	except KeyboardInterrupt:		# 捕获 Ctrl+C
		print("\n正在停止服务器...")
		sys.exit(1)
	finally:
		# 必须执行 close 否则下次启动可能会报端口占用
		if httpd:httpd.server_close()
		print("服务器已关闭")