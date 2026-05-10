import os
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import re # 确保顶部有 import re


UPLOAD_DIR = 'uploads'
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

class ModernHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        url_path = urlparse(self.path).path
        if url_path == '/' :
            self.handle_test_page()
        elif url_path == '/home':
            self.handle_home()
        elif url_path == '/info':
            self.handle_info()
        elif url_path == '/download':
            self.handle_download()
        else:
            self.send_error(404)

    def do_POST(self):
        url_path = urlparse(self.path).path
        if url_path == '/upload':
            self.handle_upload()
        elif url_path == '/post-data':
            self.handle_post_params() # 新增：獲取 POST JSON 參數
        else:
            self.send_error(404)

    def handle_home(self):
        """返回首頁 HTML"""
        html = """
        <html>
            <head><meta charset="utf-8"><title>Python Server</title></head>
            <body>
                <h1>Python 原生服務器已啟動</h1>
                <p>當前運行路徑: / (首頁)</p>
                <ul>
                    <li>GET 測試: <a href="/info?name=py&age=20">查看請求信息</a></li>
                </ul>
            </body>
        </html>
        """
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html.encode())

    def handle_test_page(self):
        """读取并返回 test.html 文件"""
        file_path = 'test.html'
        if os.path.exists(file_path):
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            with open(file_path, 'rb') as f:
                self.wfile.write(f.read())
        else:
            self.send_error(404, "test.html not found on server")
    def handle_post_params(self):
        """核心：獲取 POST 請求參數 (JSON)"""
        content_length = int(self.headers.get('Content-Length', 0))
        post_body = self.rfile.read(content_length)
        
        try:
            params = json.loads(post_body.decode('utf-8'))
            print(f"收到 POST 參數: {params}")
            self._send_json({
                "status": "success",
                "received_params": params,
                "msg": "這是從 POST Body 中解析出的數據"
            })
        except json.JSONDecodeError:
            self.send_error(400, "Invalid JSON")

    def handle_info(self):
        """獲取 GET 參數、頭信息"""
        parsed = urlparse(self.path)
        info = {
            "method": self.command,
            "headers": dict(self.headers),
            "get_params": parse_qs(parsed.query)
        }
        self._send_json(info)

    #大文件不适合 (占内存)
    def handle_upload(self):
        try:
            # 1. 获取 Content-Type 并提取 boundary
            content_type = self.headers.get('Content-Type')
            if not content_type or 'boundary=' not in content_type:
                self.send_error(400, "Content-Type must be multipart/form-data with boundary")
                return
            
            boundary = content_type.split('boundary=')[-1].encode('ascii')
            content_length = int(self.headers.get('Content-Length'))
            
            # 2. 读取全部二进制数据
            body = self.rfile.read(content_length)

            # 3. 手动切割数据块 (multipart 格式: --boundary\r\nHeader\r\n\r\nData\r\n--boundary)
            parts = body.split(b'--' + boundary)
            
            for part in parts:
                if not part or part == b'--\r\n' or part == b'--': continue
                
                # 分离头部和内容 (由 \r\n\r\n 分隔)
                if b'\r\n\r\n' in part:
                    head, content = part.split(b'\r\n\r\n', 1)
                    
                    # 从头部提取文件名 (使用正则匹配 filename="...")
                    head_str = head.decode('ascii', errors='ignore')
                    match = re.search(r'filename="([^"]+)"', head_str)
                    
                    if match:
                        filename = match.group(1)
                        # 移除末尾可能的换行符 (multipart 规范中数据后带 \r\n)
                        if content.endswith(b'\r\n'):
                            content = content[:-2]
                        
                        filepath = os.path.join(UPLOAD_DIR, filename)
                        with open(filepath, 'wb') as f:
                            f.write(content)
                        
                        self._send_json({"status": "OK", "msg": f"文件 {filename} 上传成功"})
                        return

            self.send_error(400, "No file found")
        except Exception as e:
            print(f"上传失败: {e}")
            self.send_error(500, f"Server Error: {str(e)}")


    def handle_download(self):
        query = parse_qs(urlparse(self.path).query)
        filename = query.get('name', [''])[0]
        filepath = os.path.join(UPLOAD_DIR, filename)
        
        if filename and os.path.exists(filepath):
            self.send_response(200)
            self.send_header('Content-Type', 'application/octet-stream')
            self.send_header('Content-Disposition', f'attachment; filename="{filename}"')
            self.end_headers()
            with open(filepath, 'rb') as f:
                self.wfile.write(f.read())
        else:
            self.send_error(404, "文件不存在")

    def _send_json(self, data):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

#ctrl+c 中断不可用时: ctrl+break
if __name__ == '__main__':
    print("Server: http://localhost:8000")
    HTTPServer(('localhost', 8000), ModernHandler).serve_forever()
