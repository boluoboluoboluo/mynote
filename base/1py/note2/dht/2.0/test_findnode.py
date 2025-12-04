import socket
import threading
import os
from bencode import bencode,bdecode	# type:ignore
import time
import struct


server = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
server.bind(('0.0.0.0',6882))


def listen():
	while True:
		response,addr = server.recvfrom(65536)
		print(f"receive response ...")
		
		data = bdecode(response)
		# print(data)
		if data.get('y') != 'r':
			return
		
		nodes_str = data['r']['nodes']
		nodes = []
		# 每26字节解析一个节点信息
		for i in range(0, len(nodes_str), 26):
			node_data = nodes_str[i:i+26]
			if len(node_data) != 26:
				continue

			# 前20字节为node_id
			node_id = node_data[:20]

			# 中间4字节为IPv4地址（网络字节序）
			ip_bytes = node_data[20:24]
			ip = socket.inet_ntoa(ip_bytes)

			# 最后2字节为端口（大端）
			port = struct.unpack('!H', node_data[24:26])[0]

			nodes.append((node_id, ip, port))

		print(f"nodes:")
		print(nodes)

threading.Thread(target=listen,daemon=True).start()

id = os.urandom(20)
id = b'\x18"u\xcf\xe2\xf7,\xb7\x1cc?t\x92\x97\xe7^\x85\xc7\xb6W'
request = {
	b't':b'1',
	b'y':b'q',
	b'q':b'find_node',
	b'a':{
		b'id':id,
		b'target': id
	}
}

target_host = "87.98.162.88"
target_port = 6881

target_host = '180.211.11.60'
target_port = 6881

addressinfo = (target_host,target_port)

data = bencode(request)
print(f"send request ...")

for i in range(10):
	server.sendto(data,addressinfo)

while True:
	time.sleep(1)