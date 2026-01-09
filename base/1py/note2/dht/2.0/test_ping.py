import socket
import threading
import os
from bencode import bencode,bdecode	# type:ignore
import time


server = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
server.bind(('0.0.0.0',6882))

def listen():
	while True:
		response,addr = server.recvfrom(65536)
		print(f"receive response ...")
		print(bdecode(response))

threading.Thread(target=listen,daemon=True).start()

id = os.urandom(20)
request = {
	b't':b'aa',		# tid如果是字符串，返回字节，如果是字节直接返回（始终返回字节）
	b'y':b'q',
	b'q':b'ping',
	b'a':{b'id':id}
}

# target_host = "87.98.162.88"
 
target_host = '60.186.55.57'
target_port = 6881
addressinfo = (target_host,target_port)
addressinfo = ('114.80.9.182',6883)

data = bencode(request)
print(f"send request ...")
server.sendto(data,addressinfo)

while True:
	time.sleep(1)