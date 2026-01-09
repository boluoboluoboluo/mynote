import os
import socket
import threading
import base64
#install command: pip install bencode.py
from bencode import bencode,bdecode	# type:ignore
import struct
import tools
import time
import random
import json
from tools import log
import asyncio

# dht node
class Node:
	def	__init__(self,id=None,address='127.0.0.1',port=6881):
		self.id = id if id else tools.get_local_nodeid(port)
		# print(f'node{port} id: {self.id}')
		self.address = address
		self.port = port
		self.lastping_stamp = 0
		self.send_req = 0
		self.recv_res = 0
		
	async def run(self):
		# self.id_b64 = base64.b64encode(self.id).decode('ascii')
		self.route_table = RouteTable(self)
		self.network = NetWork(self)
		self.transaction_id_counter = 0
		self.pending_transactions = {}
		# self.transaction_lock = threading.Lock()		#不可重入锁，递归或同一线程多次调用会导致无法获取锁
		# self.transaction_lock = threading.RLock()		#可重入锁

		self.transaction_lock = asyncio.Lock()

		# threading.Thread(target=self.network.listen,daemon=True).start()
		# threading.Thread(target=self._refresh_route_table,daemon=True).start()
		# threading.Thread(target=self._timeout_loop,daemon=True).start()

		asyncio.create_task(self.network.listen())
		# asyncio.create_task(self._refresh_route_table())
		# asyncio.create_task(self._timeout_loop())
		await asyncio.sleep(0)

	# run if program first time run ,or have no cache nodes file
	async def join_guide_node(self,address_info):
		tid = self.get_next_transaction_id()
		request = {
			b't':os.fsencode(tid),		# tid如果是字符串，返回字节，如果是字节直接返回（始终返回字节）
			b'y':b'q',
			b'q':b'ping',
			b'a':{b'id':self.id}
		}
		data = bencode(request)
		self.network.send_message(data,address_info)
		async def callback(response):
			print("join guide node callback..")
			nodeid = response['r']['id']
			ip = address_info[0]
			port = address_info[1]
			node = Node(nodeid,ip,port)
			self.route_table.add_node(node)		# lock
		self.add_pending_transactions(tid,callback)

	def get_next_transaction_id(self):
		tid = self.transaction_id_counter
		self.transaction_id_counter = (self.transaction_id_counter + 1) % 65536
		return str(tid)
	
	def add_pending_transactions(self,tid,callback):
		self.pending_transactions[tid] = {
			'callback':callback,
			'timeout':time.time() + 5
		}
	
	# message response
	async def handle_response(self,tid,response):
		if tid in self.pending_transactions:
			callback = self.pending_transactions[tid]['callback']
			del self.pending_transactions[tid]
			await callback(response)
	
	async def _timeout_loop(self):
		while True:
			await asyncio.sleep(1)
			current_time = time.time()
			to_remove = [tid for tid, data in self.pending_transactions.items() if data['timeout'] < current_time]
			for tid in to_remove:
				del self.pending_transactions[tid]


	async def ping(self,node):
		tid = self.get_next_transaction_id()
		request = {
			b't':os.fsencode(tid),
			b'y':b'q',
			b'q':b'ping',
			b'a':{b'id':self.id}
		}
		data = bencode(request)
		self.network.send_message(data,(node.address,node.port))
		async def callback(response):
			node.lastping_stamp = time.time()
			self.route_table.add_node(node)		# lock
		self.add_pending_transactions(tid,callback)

	async def find_node(self,target_node):
		closest = self.route_table.find_closest_nodes(target_node.id)
		contact = set()
		for n in closest[:3]:	#?
			print("find node init ...")
			await self._find_node_request(n,target_node.id,contact)

	async def _find_node_request(self,node,target_id,contact,depth=0):
		print("find node ...")
		depth = depth + 1
		if depth > 15:
			log("============= find node to max depth ================= ")
			return
		tid = self.get_next_transaction_id()
		request = {
			b't':os.fsencode(tid),
			b'y':b'q',
			b'q':b'find_node',
			b'a':{
				b'id':self.id,
				b'target': target_id
			}
		}
		data = bencode(request)
		self.network.send_message(data,(node.address,node.port))
		
		self.send_req += 1
		contact.add(node.id)
		# print(f"已访问节点{len(contact)}")
		async def callback(response):
			self.recv_res += 1
			log(f"socket counts:send:{self.send_req},recv:{self.recv_res}")
			if 'nodes' not in response['r']:
				return
			nodes_bin = response['r']['nodes']
			new_nodes = []
			for i in range(0, len(nodes_bin), 26):
				nid = nodes_bin[i:i+20]
				ip = socket.inet_ntoa(nodes_bin[i+20:i+24])
				port = struct.unpack('!H', nodes_bin[i+24:i+26])[0]		#!表示网络字节序(也就是大端模式)，H表示16位无符号整数
				new_node = Node(nid, ip, port)
				# log(f'new node:{nid} {ip} {port}')
				new_nodes.append(new_node)
				self.route_table.add_node(new_node)
			for n in new_nodes:
				if n.id not in contact:
					await self._find_node_request(n,target_id,contact,depth)
		self.add_pending_transactions(tid,callback)
		await asyncio.sleep(0.05)

	async def get_peers(self,info_hash):
		log(f'============= get peers start ==================')	
		re_peers = []
		contact = set()
		closet_nodes = self.route_table.find_closest_nodes(info_hash,k=16)
		# log(f'local closet nodes(info_hash):{closet_nodes}')
		for n in closet_nodes[:3]:
			await self._get_peers(n,info_hash,re_peers,contact)

	async def _get_peers(self,node,info_hash,re_peers,contact,depth=0):
		# print("find peers ing...")
		if re_peers:
			log(f'============= get peers success ==================')
			log(f"peers:{re_peers}")
			return
		depth = depth + 1
		if depth > 20:
			log(f'============= get peers to max depth ==================')
			return
		tid = self.get_next_transaction_id()
		request = {
			b't':os.fsencode(tid),
			b'y':b'q',
			b'q':b'get_peers',
			'a':{
				b'id':self.id,
				b'info_hash':os.fsencode(info_hash)
			}
		} 
		data = bencode(request)
		self.network.send_message(data,(node.address,node.port))
		contact.add(node.id)
		self.send_req += 1
		async def callback(response):
			self.recv_res += 1
			# log(f"socket counts:send:{self.send_req},recv:{self.recv_res}")
			# log(f'get peers response :{response}')
			if 'values' in response['r']:
				if response['r']['values']:
					if response['r']['values'] not in re_peers:
						re_peers.append(response['r']['values'])
					return
			if 'nodes' in response['r']:
				nodes_bin = response['r']['nodes']
				if not nodes_bin:
					log("2 have no return nodes...")
					return
				new_nodes = []
				for i in range(0, len(nodes_bin), 26):
					nid = nodes_bin[i:i+20]
					ip = socket.inet_ntoa(nodes_bin[i+20:i+24])
					port = struct.unpack('!H', nodes_bin[i+24:i+26])[0]		#!表示网络字节序(也就是大端模式)，H表示16位无符号整数
					new_node = Node(nid, ip, port)
					new_nodes.append(new_node)
				print(f"new nodes ...{len(new_nodes)}")
				for n in new_nodes:
					if n.id not in contact:
						print("send get peers...")
						await self._get_peers(n,info_hash,re_peers,contact,depth)
			else:
				log("have no return nodes...")
		self.add_pending_transactions(tid,callback)

	async def _refresh_route_table(self):
		# print(f'node({self.port}) refresh route_table..')
		refresh_time = 5 * 60 	# sec
		kbucket_check_time = 30 * 60		# sec
		
		await asyncio.sleep(refresh_time)
		log("refresh route table...")
		while True:
			for k in self.route_table.kbuckets:
				if not k.nodes:
					continue
				for n in k.nodes:
					self.ping(n)
				if k.update_time + kbucket_check_time < time.time():	# current timestamp
					k.update_time = time.time()
					await self.find_node(k.nodes[random.randint(0,len(k.nodes)-1)])		# random node
			await asyncio.sleep(refresh_time)
			for k in self.route_table.kbuckets:
				for n in k.nodes:
					if time.time() - n.lastping_stamp > 4 * refresh_time:	# if ping 3 times have no response,then remove
						with self.transaction_lock:
							k.nodes.remove(n)
			# break

	def save_route_table(self):
		save_data = {}
		save_data['kbuckets'] = [] 
		# print(self.route_table.kbuckets)
		save_flag = 0
		for kb in self.route_table.kbuckets:
			tmp_bucket = {}
			tmp_bucket['max_size'] = kb.max_size
			tmp_bucket['update_time'] = kb.update_time
			tmp_bucket['nodes'] = []
			for n in kb.nodes:
				save_flag = 1
				tmp_node = {}
				tmp_node['id'] = n.id.hex()
				tmp_node['address'] = n.address
				tmp_node['port'] = n.port
				tmp_bucket['nodes'].append(tmp_node)
			save_data['kbuckets'].append(tmp_bucket)

		if not save_flag:
			return
		with open(tools.ROUTE_FILE,'w') as f:
			json.dump(save_data,f)
		log("route_table saved..")
		
	def read_route_file(self,file_path):
		save_data = {}
		with open(file_path,'r') as f:
			save_data = json.load(f)

		self.route_table.kbuckets = []
		for kb in save_data['kbuckets']:
			tmp_bucket = KBucket()
			tmp_bucket.max_size = kb['max_size']
			tmp_bucket.update_time = kb['update_time']
			tmp_bucket.nodes = []
			for n in kb['nodes']:
				tmp_node = Node(bytes.fromhex(n['id']),n['address'],n['port'])
				tmp_bucket.nodes.append(tmp_node)
			self.route_table.kbuckets.append(tmp_bucket)

# a dht node have a route_table
class RouteTable:
	def __init__(self,node):
		self.node = node
		self.kbuckets = [KBucket() for _ in range(160)] # 160 kbucket	?

	def add_node(self,node):
		# print(f"node {self.node.port} add node({node.port})..")
		if node.id == self.node.id:
			return
		xor = bytes([a ^ b for a, b in zip(self.node.id, node.id)])		#zip方法：将多个可迭代对象的元素打包成元组，返回一个迭代器
		distance = int.from_bytes(xor, byteorder='big')
		if distance == 0:
			return
		msb = distance.bit_length() - 1		#bit_length()返回该整数所需的二进制位数，不包括符号位和前导零
		bucket_index = min(msb, 159)
		self.kbuckets[bucket_index].add_node(node)

	def find_closest_nodes(self,target_id,k=20):
		nodes = []
		for bucket in self.kbuckets:
			nodes.extend(bucket.nodes)
		nodes.sort(key=lambda n: tools.xor_distance(n.id, target_id))	#?
		return nodes[:k]


# a route_table have 160 kbucket 
class KBucket:
	def __init__(self,max_size=20):
		self.nodes = []		# store network node
		self.max_size = max_size
		self.update_time = 0 # sec

	def add_node(self,node):
		# print(f'add node ...')
		for n in self.nodes:
			if n.id == node.id:
				self.nodes.remove(n)
				self.nodes.append(node)
				return
		if len(self.nodes) < self.max_size:
			self.nodes.append(node)
		else:
			pass # something todo..
			

class NetWork:
	def __init__(self,node):
		self.node = node
		self.socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)	#
		self.socket.setblocking(False)	#设置为非阻塞模式
		self.socket.bind(('0.0.0.0',self.node.port))		#监听全部网段

		# 设置接收缓冲区大小（单位：字节）
		buffer_size = 1024 * 1024  # 1 MB
		self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, buffer_size)

# 获取当前接收缓冲区大小
		current_size = self.socket.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF)
		print(f"当前接收缓冲区大小: {current_size} 字节")

	def send_message(self,data,address_info):
		# print(f"node({self.node.port}) send message ..")
		try:
			self.socket.sendto(data,address_info)
		except Exception as e:
			log(f'send message error:{e} \n [query:{bdecode(data)}]')

	async def listen(self):

		loop = asyncio.get_event_loop()		#获取当前事件循环
		print(f"node({self.node.port}) open listen ..")
		def callback(sock):	#回调
			while True:
				try:
					data, addr = sock.recvfrom(65536)  # 调整缓冲区大小
					
					asyncio.create_task(self.handle_message(data,addr))
				except BlockingIOError:
					# log("data read done...")
					break
				except OSError as e:
					log(f"Error reading from socket: {e}")
					break
				except Exception as e:
					log(f'socket recv error: {e}')
					break
		loop.add_reader(self.socket.fileno(), callback, self.socket) #监听数据变化

	async def handle_message(self,data,addr):
		# print(f'node({self.node.port}) handle message...')
		# await asyncio.sleep(0.12)
		try:
			msg = bdecode(data)
			# print(f'msg:{msg}')
			if msg['y'] == 'q':
				# log(f'node({self.node.port}) handle query...')
				await self.handle_query(msg,addr)		# query message
			elif msg['y'] == 'r':
				await self.handle_response(msg,addr)	# response message
		except Exception as e:
			log(f'node({self.node.port}) handle_message error: {e}')
			log(f're message:{data}')

	async def handle_query(self,msg,addr):
		log(f'hand query : {msg} [addr:{addr}]')
		if msg['q'] == 'ping':
			request = {
				b't':os.fsencode(msg['t']),
				b'y':b'r',
				b'r':{b'id':self.node.id}
			}
			data = bencode(request)
			self.send_message(data,addr)
		elif msg['q'] == 'find_node':
			target_id = msg['a']['target']
			closest = self.node.route_table.find_closest_nodes(target_id)
			#?
			nodes_bin = b''.join([
				n.id + socket.inet_aton(n.address) + struct.pack('!H', n.port)
				for n in closest[:20]
			])
			request = {
				b't':os.fsencode(msg['t']),
				b'y':b'r',
				b'r':{
					b'id': self.node.id,
					b'nodes': nodes_bin
				}
			}
			data = bencode(request)
			self.send_message(data,addr)

	async def handle_response(self,msg,addr):
		if 'values' in msg['r']:
			if msg['r']['values']:
				log(f'get peers avaliable addr:{addr}')
				log(f'msg:{msg}')
		await self.node.handle_response(msg['t'],msg)