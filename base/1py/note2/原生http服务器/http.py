import socket
import os
import mimetypes
import urllib.parse

# 配置信息
HOST = 'localhost'
PORT = 8000
FILE_DIR = 'files'  # 存放下载文件的目录

def get_content_type(file_path):
    """获取文件的Content-Type"""
    mime_type, _ = mimetypes.guess_type(file_path)
    return mime_type or 'application/octet-stream'

def send_file_response(client_socket, file_path):
    """发送文件作为HTTP响应"""
    try:
        with open(file_path, 'rb') as file:
            file_content = file.read()
        
        filename = os.path.basename(file_path)
        content_type = get_content_type(file_path)
        
        # 构建HTTP响应头
        headers = [
            "HTTP/1.1 200 OK",
            f"Content-Type: {content_type}",
            f"Content-Disposition: attachment; filename=\"{filename}\"",
            f"Content-Length: {len(file_content)}",
            "Connection: close",
            "\r\n"
        ]
        
        # 发送响应头
        client_socket.send("\r\n".join(headers).encode('utf-8'))
        
        # 发送文件内容
        client_socket.send(file_content)
        
    except FileNotFoundError:
        # 文件不存在时返回404
        response = "HTTP/1.1 404 Not Found\r\nContent-Type: text/plain\r\n\r\nFile not found"
        client_socket.send(response.encode('utf-8'))
    except Exception as e:
        # 其他错误返回500
        response = f"HTTP/1.1 500 Internal Server Error\r\nContent-Type: text/plain\r\n\r\nError: {str(e)}"
        client_socket.send(response.encode('utf-8'))

def handle_request(client_socket):
    """处理客户端请求"""
    # 接收请求数据
    request_data = client_socket.recv(1024).decode('utf-8')
    
    if not request_data:
        return
    
    # 解析请求行
    request_lines = request_data.split('\r\n')
    request_line = request_lines[0].split()
    
    if len(request_line) < 2:
        return
    
    method, path = request_line[0], request_line[1]
    
    # 只处理GET请求
    if method != 'GET':
        response = "HTTP/1.1 405 Method Not Allowed\r\nAllow: GET\r\n\r\n"
        client_socket.send(response.encode('utf-8'))
        return
    
    # 解析路径和查询参数
    parsed_path = urllib.parse.urlparse(path)
    path = parsed_path.path
    
    # 首页请求
    if path == '/':
        # 返回包含下载链接的HTML页面
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>文件下载</title>
            <style>
                body { font-family: Arial, sans-serif; padding: 20px; }
                a.download-btn {
                    display: inline-block;
                    padding: 10px 20px;
                    background: #4CAF50;
                    color: white;
                    text-decoration: none;
                    border-radius: 4px;
                    margin: 10px 0;
                }
            </style>
        </head>
        <body>
            <h1>文件下载示例</h1>
            <p>点击下方链接下载文件：</p>
            <a href="/download?file=example.txt" class="download-btn">下载示例文件</a>
        </body>
        </html>
        """
        
        response = f"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: {len(html_content)}\r\n\r\n{html_content}"
        client_socket.send(response.encode('utf-8'))
        return
    
    # 文件下载请求
    if path == '/download':
        # 解析查询参数
        query_params = urllib.parse.parse_qs(parsed_path.query)
        filename = query_params.get('file', [None])[0]
        
        if not filename:
            response = "HTTP/1.1 400 Bad Request\r\nContent-Type: text/plain\r\n\r\nMissing file parameter"
            client_socket.send(response.encode('utf-8'))
            return
        
        # 防止路径遍历攻击
        filename = os.path.basename(filename)
        file_path = os.path.join(FILE_DIR, filename)
        
        # 发送文件
        send_file_response(client_socket, file_path)
        return
    
    # 其他路径返回404
    response = "HTTP/1.1 404 Not Found\r\nContent-Type: text/plain\r\n\r\nNot Found"
    client_socket.send(response.encode('utf-8'))

def main():
    """主函数，启动服务器"""
    # 确保文件目录存在
    os.makedirs(FILE_DIR, exist_ok=True)
    
    # 创建示例文件
    example_file = os.path.join(FILE_DIR, 'example.txt')
    if not os.path.exists(example_file):
        with open(example_file, 'w') as f:
            f.write("这是一个示例文件内容\n" * 10)
    
    # 创建TCP套接字
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        # 绑定地址和端口
        server_socket.bind((HOST, PORT))
        server_socket.listen(5)
        print(f"服务器运行在 http://{HOST}:{PORT}")
        print(f"下载目录: {os.path.abspath(FILE_DIR)}")
        print("访问 http://localhost:8000 测试下载功能")
        
        while True:
            # 接受客户端连接
            client_socket, addr = server_socket.accept()
            print(f"来自 {addr[0]}:{addr[1]} 的连接")
            
            # 处理请求
            handle_request(client_socket)
            
            # 关闭连接
            client_socket.close()
    
    except KeyboardInterrupt:
        print("\n服务器关闭")
    finally:
        server_socket.close()

if __name__ == "__main__":
    main()