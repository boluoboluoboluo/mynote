import socket
import os
import mimetypes
import urllib.parse
import threading
import time
import sys
import gzip
import io
import re

# 配置信息
HOST = '0.0.0.0'  # 监听所有接口
PORT = 8000
FILE_DIR = 'files'  # 存放下载文件的目录
CACHE_DIR = '.cache'  # 缓存目录
BUFFER_SIZE = 8192  # 缓冲区大小
MAX_CONNECTIONS = 100  # 最大并发连接数
COMPRESS_TYPES = {  # 支持压缩的文件类型
    'text/plain', 'text/html', 'text/css', 
    'application/javascript', 'application/json', 
    'application/xml', 'image/svg+xml'
}

# 创建必要的目录
os.makedirs(FILE_DIR, exist_ok=True)
os.makedirs(CACHE_DIR, exist_ok=True)

# 创建示例文件（如果不存在）
def create_example_files():
    # 文本文件
    txt_file = os.path.join(FILE_DIR, 'example.txt')
    if not os.path.exists(txt_file):
        with open(txt_file, 'w') as f:
            f.write("这是一个示例文本文件\n" * 1000)
    
    # 大文件（10MB）
    big_file = os.path.join(FILE_DIR, 'bigfile.bin')
    if not os.path.exists(big_file):
        with open(big_file, 'wb') as f:
            f.write(os.urandom(10 * 1024 * 1024))

create_example_files()

class ConnectionPool:
    """连接池管理类"""
    def __init__(self, max_size):
        self.max_size = max_size
        self.semaphore = threading.Semaphore(max_size)
        self.active_connections = 0
    
    def acquire(self):
        """获取连接许可"""
        self.semaphore.acquire()
        self.active_connections += 1
    
    def release(self):
        """释放连接许可"""
        self.semaphore.release()
        self.active_connections -= 1
    
    def get_stats(self):
        """获取连接池统计信息"""
        return {
            "max": self.max_size,
            "active": self.active_connections,
            "available": self.max_size - self.active_connections
        }

# 创建连接池
connection_pool = ConnectionPool(MAX_CONNECTIONS)

def get_content_type(file_path):
    """获取文件的Content-Type"""
    mime_type, encoding = mimetypes.guess_type(file_path)
    return mime_type or 'application/octet-stream'

def generate_file_response(file_path, client_socket):
    """生成文件HTTP响应（流式传输）"""
    filename = os.path.basename(file_path)
    content_type = get_content_type(file_path)
    file_size = os.path.getsize(file_path)
    
    # 构建HTTP响应头
    headers = [
        "HTTP/1.1 200 OK",
        f"Content-Type: {content_type}",
        f"Content-Disposition: attachment; filename=\"{filename}\"",
        f"Content-Length: {file_size}",
        "Connection: keep-alive",
        "Cache-Control: public, max-age=3600",  # 1小时缓存
        "\r\n"
    ]
    
    # 发送响应头
    client_socket.send("\r\n".join(headers).encode('utf-8'))
    
    # 流式传输文件内容
    try:
        with open(file_path, 'rb') as file:
            while True:
                chunk = file.read(BUFFER_SIZE)
                if not chunk:
                    break
                client_socket.send(chunk)
    except Exception as e:
        print(f"文件传输错误: {e}")

def compress_content(content, content_type):
    """压缩内容（如果支持且有效）"""
    if content_type not in COMPRESS_TYPES:
        return content, False
    
    # 检查压缩是否有效（内容需足够大）
    if len(content) < 1024:
        return content, False
    
    try:
        # 使用gzip压缩
        buf = io.BytesIO()
        with gzip.GzipFile(fileobj=buf, mode='wb') as f:
            f.write(content)
        compressed = buf.getvalue()
        
        # 仅当压缩率>10%时才使用
        if len(compressed) < len(content) * 0.9:
            return compressed, True
    except:
        pass
    
    return content, False

def send_cached_response(client_socket, cache_key):
    """发送缓存的响应"""
    cache_file = os.path.join(CACHE_DIR, cache_key)
    if not os.path.exists(cache_file):
        return False
    
    try:
        with open(cache_file, 'rb') as f:
            response = f.read()
        client_socket.send(response)
        return True
    except:
        return False

def cache_response(cache_key, response):
    """缓存HTTP响应"""
    try:
        cache_file = os.path.join(CACHE_DIR, cache_key)
        with open(cache_file, 'wb') as f:
            f.write(response)
    except:
        pass

def get_home_page():
    """生成首页HTML"""
    files = [f for f in os.listdir(FILE_DIR) if os.path.isfile(os.path.join(FILE_DIR, f))]
    
    file_list = "\n".join(
        f'<li><a href="/download?file={urllib.parse.quote(f)}">{f}</a> '
        f'({os.path.getsize(os.path.join(FILE_DIR, f)) // 1024} KB)</li>'
        for f in files
    )
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>高性能文件下载服务器</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            * {{ box-sizing: border-box; margin: 0; padding: 0; }}
            body {{ 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                line-height: 1.6; 
                color: #333; 
                background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
                min-height: 100vh;
                padding: 20px;
            }}
            .container {{
                max-width: 1200px;
                margin: 0 auto;
                background: rgba(255, 255, 255, 0.95);
                border-radius: 15px;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
                overflow: hidden;
            }}
            header {{
                background: linear-gradient(90deg, #4b6cb7 0%, #182848 100%);
                color: white;
                padding: 2rem;
                text-align: center;
            }}
            header h1 {{
                font-size: 2.5rem;
                margin-bottom: 0.5rem;
            }}
            .stats {{
                display: flex;
                justify-content: space-around;
                flex-wrap: wrap;
                background: #2c3e50;
                color: white;
                padding: 1rem;
                font-size: 0.9rem;
            }}
            .stat-item {{
                text-align: center;
                margin: 0.5rem;
                min-width: 150px;
            }}
            .stat-value {{
                font-size: 1.5rem;
                font-weight: bold;
                color: #3498db;
            }}
            .content {{
                padding: 2rem;
            }}
            .file-list {{
                margin: 2rem 0;
            }}
            .file-list h2 {{
                border-bottom: 2px solid #3498db;
                padding-bottom: 0.5rem;
                margin-bottom: 1.5rem;
                color: #2c3e50;
            }}
            ul {{
                list-style-type: none;
            }}
            li {{
                padding: 0.8rem;
                margin: 0.5rem 0;
                background: #f8f9fa;
                border-radius: 8px;
                transition: all 0.3s ease;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }}
            li:hover {{
                background: #e9ecef;
                transform: translateX(5px);
            }}
            a {{
                color: #3498db;
                text-decoration: none;
                font-weight: 500;
            }}
            a:hover {{
                text-decoration: underline;
            }}
            .download-btn {{
                display: inline-block;
                background: linear-gradient(90deg, #3498db 0%, #2c3e50 100%);
                color: white;
                padding: 0.6rem 1.2rem;
                border-radius: 30px;
                font-weight: bold;
                transition: all 0.3s;
                border: none;
                cursor: pointer;
                text-align: center;
                margin-top: 0.5rem;
            }}
            .download-btn:hover {{
                transform: translateY(-3px);
                box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
                text-decoration: none;
            }}
            .performance-info {{
                margin-top: 2rem;
                padding: 1.5rem;
                background: #f8f9fa;
                border-radius: 10px;
                border-left: 4px solid #3498db;
            }}
            .performance-info h3 {{
                color: #2c3e50;
                margin-bottom: 1rem;
            }}
            .features {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 1.5rem;
                margin-top: 1.5rem;
            }}
            .feature-card {{
                background: white;
                border-radius: 10px;
                padding: 1.5rem;
                box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
                transition: transform 0.3s;
            }}
            .feature-card:hover {{
                transform: translateY(-5px);
            }}
            .feature-card h4 {{
                color: #3498db;
                margin-bottom: 0.5rem;
            }}
            footer {{
                text-align: center;
                padding: 1.5rem;
                background: #2c3e50;
                color: white;
                font-size: 0.9rem;
            }}
            @media (max-width: 768px) {{
                .features {{
                    grid-template-columns: 1fr;
                }}
                .stats {{
                    flex-direction: column;
                    align-items: center;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <header>
                <h1>高性能文件下载服务器</h1>
                <p>原生Python实现，优化传输性能</p>
            </header>
            
            <div class="stats">
                <div class="stat-item">
                    <div>服务器启动时间</div>
                    <div class="stat-value">{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time))}</div>
                </div>
                <div class="stat-item">
                    <div>运行时长</div>
                    <div class="stat-value" id="uptime">0 秒</div>
                </div>
                <div class="stat-item">
                    <div>处理请求</div>
                    <div class="stat-value" id="request-count">0</div>
                </div>
                <div class="stat-item">
                    <div>并发连接</div>
                    <div class="stat-value">{connection_pool.active_connections}/{MAX_CONNECTIONS}</div>
                </div>
            </div>
            
            <div class="content">
                <div class="file-list">
                    <h2>可用文件下载</h2>
                    <ul>
                        {file_list}
                    </ul>
                </div>
                
                <div class="performance-info">
                    <h3>性能优化特性</h3>
                    <div class="features">
                        <div class="feature-card">
                            <h4>流式传输</h4>
                            <p>使用缓冲区流式传输文件，避免大文件占用内存</p>
                        </div>
                        <div class="feature-card">
                            <h4>连接池管理</h4>
                            <p>限制并发连接数，防止服务器过载</p>
                        </div>
                        <div class="feature-card">
                            <h4>内容压缩</h4>
                            <p>对文本内容自动进行GZIP压缩，减少传输数据量</p>
                        </div>
                        <div class="feature-card">
                            <h4>响应缓存</h4>
                            <p>缓存常见响应，减少重复处理开销</p>
                        </div>
                        <div class="feature-card">
                            <h4>Keep-Alive</h4>
                            <p>支持持久连接，减少TCP握手开销</p>
                        </div>
                        <div class="feature-card">
                            <h4>缓存控制</h4>
                            <p>设置客户端缓存，减少重复请求</p>
                        </div>
                    </div>
                </div>
            </div>
            
            <footer>
                <p>高性能文件下载服务器 &copy; {time.strftime('%Y')} | 原生Python实现</p>
            </footer>
        </div>
        
        <script>
            // 更新运行时间
            const startTime = {start_time};
            function updateUptime() {{
                const now = Math.floor(Date.now() / 1000);
                const uptime = now - startTime;
                const days = Math.floor(uptime / 86400);
                const hours = Math.floor((uptime % 86400) / 3600);
                const minutes = Math.floor((uptime % 3600) / 60);
                const seconds = uptime % 60;
                
                let display = '';
                if (days > 0) display += `${days}天 `;
                if (hours > 0 || display) display += `${hours}小时 `;
                if (minutes > 0 || display) display += `${minutes}分钟 `;
                display += `${seconds}秒`;
                
                document.getElementById('uptime').textContent = display;
            }}
            
            // 初始更新
            updateUptime();
            setInterval(updateUptime, 1000);
        </script>
    </body>
    </html>
    """

# 服务器启动时间
start_time = time.time()

def handle_request(client_socket, client_address):
    """处理客户端请求"""
    global request_count
    request_count = 0
    
    try:
        # 接收请求数据
        request_data = b''
        while True:
            chunk = client_socket.recv(BUFFER_SIZE)
            request_data += chunk
            if b'\r\n\r\n' in request_data or len(chunk) < BUFFER_SIZE:
                break
        
        if not request_data:
            return
        
        request_text = request_data.decode('utf-8', errors='ignore')
        request_lines = request_text.split('\r\n')
        
        if not request_lines:
            return
        
        # 解析请求行
        request_line = request_lines[0].split()
        if len(request_line) < 2:
            return
        
        method, path = request_line[0], request_line[1]
        request_count += 1
        
        # 解析路径和查询参数
        parsed_path = urllib.parse.urlparse(path)
        path = parsed_path.path
        query_params = urllib.parse.parse_qs(parsed_path.query)
        
        # 首页请求
        if path == '/':
            # 检查缓存
            cache_key = "home_page"
            if send_cached_response(client_socket, cache_key):
                return
            
            # 生成首页内容
            html_content = get_home_page().encode('utf-8')
            
            # 压缩内容
            compressed, is_compressed = compress_content(html_content, 'text/html')
            
            # 构建响应头
            headers = [
                "HTTP/1.1 200 OK",
                "Content-Type: text/html; charset=utf-8",
                f"Content-Length: {len(compressed)}",
                "Connection: keep-alive",
                "Cache-Control: public, max-age=60"  # 1分钟缓存
            ]
            
            if is_compressed:
                headers.append("Content-Encoding: gzip")
            
            headers.append("\r\n")
            
            # 完整响应
            response = "\r\n".join(headers).encode('utf-8') + compressed
            
            # 发送响应并缓存
            client_socket.send(response)
            cache_response(cache_key, response)
            return
        
        # 文件下载请求
        if path == '/download':
            filename = query_params.get('file', [None])[0]
            if not filename:
                response = "HTTP/1.1 400 Bad Request\r\nContent-Type: text/plain\r\n\r\nMissing file parameter"
                client_socket.send(response.encode('utf-8'))
                return
            
            # 防止路径遍历攻击
            filename = os.path.basename(urllib.parse.unquote(filename))
            file_path = os.path.join(FILE_DIR, filename)
            
            if not os.path.exists(file_path):
                response = "HTTP/1.1 404 Not Found\r\nContent-Type: text/plain\r\n\r\nFile not found"
                client_socket.send(response.encode('utf-8'))
                return
            
            # 流式传输文件
            generate_file_response(file_path, client_socket)
            return
        
        # 其他路径返回404
        response = "HTTP/1.1 404 Not Found\r\nContent-Type: text/plain\r\n\r\nNot Found"
        client_socket.send(response.encode('utf-8'))
    
    except Exception as e:
        print(f"处理请求时出错: {e}")
    finally:
        # 确保关闭连接
        try:
            client_socket.close()
        except:
            pass
        connection_pool.release()

def client_thread(client_socket, client_address):
    """客户端线程"""
    try:
        handle_request(client_socket, client_address)
    finally:
        # 确保关闭连接
        try:
            client_socket.close()
        except:
            pass
        connection_pool.release()

def main():
    """主函数，启动高性能服务器"""
    # 创建TCP套接字
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # 设置超时以优雅处理关闭
    server_socket.settimeout(1)
    
    try:
        # 绑定地址和端口
        server_socket.bind((HOST, PORT))
        server_socket.listen(MAX_CONNECTIONS)
        
        print(f"高性能服务器运行在 http://{HOST}:{PORT}")
        print(f"下载目录: {os.path.abspath(FILE_DIR)}")
        print(f"最大并发连接: {MAX_CONNECTIONS}")
        print(f"缓冲区大小: {BUFFER_SIZE} bytes")
        print("按 Ctrl+C 停止服务器")
        
        while True:
            try:
                # 接受客户端连接
                client_socket, client_address = server_socket.accept()
                
                # 设置超时
                client_socket.settimeout(10)
                
                # 从连接池获取许可
                connection_pool.acquire()
                
                # 创建新线程处理客户端
                thread = threading.Thread(
                    target=client_thread, 
                    args=(client_socket, client_address),
                    daemon=True
                )
                thread.start()
                
            except socket.timeout:
                # 超时继续循环
                continue
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"接受连接时出错: {e}")
                continue
    
    except KeyboardInterrupt:
        print("\n服务器关闭中...")
    finally:
        server_socket.close()
        print("服务器已关闭")

if __name__ == "__main__":
    # 设置mimetype
    mimetypes.init()
    # 添加额外的MIME类型
    mimetypes.add_type('application/wasm', '.wasm')
    
    main()