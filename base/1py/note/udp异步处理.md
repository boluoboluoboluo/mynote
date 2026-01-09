#### 代码示例：

```py
import asyncio
import time
import socket

class server():
	def __init__(self):
		self.sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
		self.sock.setblocking(False)	#设置为非阻塞模式
		self.sock.bind(('127.0.0.1',10000))

	async def handle(self,data,addr):
		print(f'recvive data: {data}')
		await asyncio.sleep(1)

	async def listen(self):
		loop = asyncio.get_event_loop()		#获取当前事件循环

		def callback(sock):	#回调
			while True:
				try:
					data, addr = sock.recvfrom(4096)  # 调整缓冲区大小
					asyncio.create_task(self.handle(data,addr))
				except BlockingIOError:
					print("data read done...")
					break	#无数据可读时退出循环
				except OSError as e:
					print(f"Error reading from socket: {e}")
					break
				
		loop.add_reader(self.sock.fileno(), callback, self.sock) #监听数据变化

		# data, addr = await loop.sock_recvfrom(sock, 65536)	# 异步接收数据，unix-like架下的方法

class client:
	def __init__(self):
		self.sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
		self.sock.bind(('127.0.0.1',9999))

	async def run(self):	#运行测试
		data = b'hello1'
		data2 = b'hello2'
		addr = ('127.0.0.1',10000)

		loop = asyncio.get_event_loop()		#获取当前事件循环

		# await loop.sock_sendto(self.sock, data, addr)	# 异步发送数据，unix-like架下的方法

		self.sock.sendto(data,addr)
		self.sock.sendto(data2,addr)
		await asyncio.sleep(0.1)
		print('send end...')
		
async def main():
	s = server()
	asyncio.create_task(s.listen())		#并发任务

	c = client()
	asyncio.create_task(c.run())		#并发任务

	while True:
		await asyncio.sleep(1)

	# loop = asyncio.get_running_loop()
	# try:
	# 	await asyncio.Future()  # 永久运行，直到被取消
	# finally:
	# 	loop.remove_reader(s.sock.fileno())
	# 	s.sock.close()
	# 	c.sock.close()

asyncio.run(main())

```

