import socket

# 创建 UDP 套接字
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 设置接收缓冲区大小（单位：字节）
buffer_size = 1024 * 1024  # 1 MB
sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, buffer_size)

# 获取当前接收缓冲区大小
current_size = sock.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF)
print(f"当前接收缓冲区大小: {current_size} 字节")
