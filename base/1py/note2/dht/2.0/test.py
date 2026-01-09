import asyncio
import time
import socket
import random

class client:
	def __init__(self):
		self.sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
		self.sock.setblocking(False)	#设置为非阻塞模式
		self.sock.bind(('127.0.0.1',9999))

	async def run(self):
		asyncio.create_task(self.listen())
		await asyncio.sleep(0)

	async def listen(self):
		loop = asyncio.get_event_loop()		#获取当前事件循环

		def callback(sock):	#回调
			while True:
				try:
					data, addr = sock.recvfrom(65536)  # 调整缓冲区大小
					print(f"rec:{data}")
					asyncio.create_task(self.handle(data,addr))
				except BlockingIOError:
					print("data read done...")
					break
				except OSError as e:
					print(f"Error reading from socket: {e}")
					break
		loop.add_reader(self.sock.fileno(), callback, self.sock) #监听数据变化

	async def handle(self,data,addr):
		# await asyncio.sleep(random.randint(1,3))
		await asyncio.sleep(0)
		print(f"======================")
		print(f"receive:{data}")
		

	def send(self,data):	#运行测试
		data = data.encode()
		addr = ('127.0.0.1',10000)

		# time.sleep(1)
		self.sock.sendto(data,addr)

		print('send end...')
		
async def main():

	c = client()

	await c.run()

	# asyncio.create_task(c.send())		#并发任务
	c.send("hello")

	print("xxxx...")

	print("yyyy...")

	c.send("world")
	c.send("123")
	c.send("456")

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
