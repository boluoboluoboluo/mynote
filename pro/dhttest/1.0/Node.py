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

# dht node
class Node:
	def	__init__(self,id=None,address='127.0.0.1',port=6881):
		self.id = id if id else tools.get_local_nodeid(port)
		# print(f'node{port} id: {self.id}')
		self.address = address
		self.port = port
		self.lastping_stamp = 0
		
	def run(self):
		self.id_b64 = base64.b64encode(self.id).decode('ascii')
		self.route_table = RouteTable(self)
		self.network = NetWork(self)
		self.transaction_id_counter = 0
		self.pending_transactions = {}
		# self.transaction_lock = threading.Lock()		#不可重入锁，递归或同一线程多次调用会导致无法获取锁
		self.transaction_lock = threading.RLock()		#可重入锁
		threading.Thread(target=self.network.listen,daemon=True).start()
		threading.Thread(target=self._refresh_route_table,daemon=True).start()
		threading.Thread(target=self._timeout_loop,daemon=True).start()

	# run if program first time run ,or have no cache nodes file
	def join_guide_node(self,address_info):
		tid = self.get_next_transaction_id()
		request = {
			't':tid,
			'y':'q',
			'q':'ping',
			'a':{'id':self.id_b64}
		}
		data = bencode(request)
		self.network.send_message(data,address_info)
		def callback(response):
			# print("join guide node callback..")
			nodeid = base64.b64decode(response['r']['id'])
			ip = address_info[0]
			port = address_info[1]
			node = Node(nodeid,ip,port)
			self.route_table.add_node(node)		# lock
		self.add_pending_transactions(tid,callback)

	def get_next_transaction_id(self):
		with self.transaction_lock:
			tid = self.transaction_id_counter
			self.transaction_id_counter = (self.transaction_id_counter + 1) % 65536
			return str(tid)
	
	def add_pending_transactions(self,tid,callback):
		with self.transaction_lock:
			self.pending_transactions[tid] = {
				'callback':callback,
				'timeout':time.time() + 5
			}
	
	# message response
	def handle_response(self,tid,response):
		# print(f'id:{msg["r"]["id"]}')
		with self.transaction_lock:
			if tid in self.pending_transactions:
				callback = self.pending_transactions[tid]['callback']
				del self.pending_transactions[tid]
				callback(response)
	
	def _timeout_loop(self):
		while True:
			time.sleep(1)
			current_time = time.time()
			with self.transaction_lock:
				to_remove = [tid for tid, data in self.pending_transactions.items() if data['timeout'] < current_time]
				for tid in to_remove:
					del self.pending_transactions[tid]


	def ping(self,node):
		tid = self.get_next_transaction_id()
		request = {
			't':tid,
			'y':'q',
			'q':'ping',
			'a':{'id':self.id_b64}
		}
		data = bencode(request)
		self.network.send_message(data,(node.address,node.port))
		def callback(response):
			node.lastping_stamp = time.time()
			self.route_table.add_node(node)		# lock
		self.add_pending_transactions(tid,callback)

	def find_node(self,target_node):
		# print("find node ...")
		closest = self.route_table.find_closest_nodes(target_node.id)
		contact = set()
		for n in closest:	#?
			self._find_node_request(n,target_node.id,contact)

	def _find_node_request(self,node,target_id,contact):
		# print(f'=======================find node from node({node.port})')
		if node.id in contact:
			return
		if len(contact) > 1000:
			print("find node contact over 1000 times...")
			return
		contact.add(node.id)
		tid = self.get_next_transaction_id()
		request = {
			't':tid,
			'y':'q',
			'q':'find_node',
			'a':{
				'id':self.id_b64,
				'target': base64.b64encode(target_id).decode('ascii')	
			}
		}
		data = bencode(request)
		self.network.send_message(data,(node.address,node.port))
		def callback(response):
			# print("find node callback...")
			nodes_bin = base64.b64decode(response['r']['nodes'])
			new_nodes = []
			for i in range(0, len(nodes_bin), 26):
				nid = nodes_bin[i:i+20]
				ip = socket.inet_ntoa(nodes_bin[i+20:i+24])
				port = struct.unpack('!H', nodes_bin[i+24:i+26])[0]
				new_node = Node(nid, ip, port)
				print(f'new node:{nid} {ip} {port}')
				new_nodes.append(new_node)
				self.route_table.add_node(new_node)
			for n in new_nodes:
				if n.id not in contact:
					self._find_node_request(n,target_id,contact)
		self.add_pending_transactions(tid,callback)

	def _refresh_route_table(self):
		# print(f'node({self.port}) refresh route_table..')
		refresh_time = 5 * 60 	# sec
		kbucket_check_time = 30 * 60		# sec
		while True:
			for k in self.route_table.kbuckets:
				if not k.nodes:
					break
				for n in k.nodes:
					self.ping(n)
				if k.update_time + kbucket_check_time < time.time():	# current timestamp
					k.update_time = time.time()
					self.find_node(k.nodes[random.randint(0,len(k.nodes)-1)])		# random node
			time.sleep(refresh_time)
			for k in self.route_table.kbuckets:
				for n in k.nodes:
					if time.time() - n.lastping_stamp > 4 * refresh_time:
						with self.transaction_lock:
							k.nodes.remove(n)

	def save_route_table(self):
		save_data = {}
		save_data['kbuckets'] = [] 
		# print(self.route_table.kbuckets)
		for kb in self.route_table.kbuckets:
			tmp_bucket = {}
			tmp_bucket['max_size'] = kb.max_size
			tmp_bucket['update_time'] = kb.update_time
			tmp_bucket['nodes'] = []
			for n in kb.nodes:
				tmp_node = {}
				tmp_node['id'] = n.id.hex()
				tmp_node['address'] = n.address
				tmp_node['port'] = n.port
				tmp_bucket['nodes'].append(tmp_node)
			save_data['kbuckets'].append(tmp_bucket)

		with open(tools.ROUTE_FILE,'w') as f:
			json.dump(save_data,f)
		print("route_table saved..")
		
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
		xor = bytes([a ^ b for a, b in zip(self.node.id, node.id)])		#?
		distance = int.from_bytes(xor, byteorder='big')
		if distance == 0:
			return
		msb = distance.bit_length() - 1
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
		self.socket.bind(('0.0.0.0',self.node.port))

	def send_message(self,data,address_info):
		print(f"node({self.node.port}) send message ..")
		self.socket.sendto(data,address_info)

	def listen(self):
		print(f"node({self.node.port}) open listen ..")
		while True:
			data,addr = self.socket.recvfrom(65536)
			# self.socket.recvfrom(65536)
			threading.Thread(target=self.handle_message,args=(data,addr)).start()

	def handle_message(self,data,addr):
		print(f'node({self.node.port}) handle message...')
		try:
			msg = bdecode(data)
			if msg['y'] == 'q':
				self.handle_query(msg,addr)		# query message
			elif msg['y'] == 'r':
				self.handle_response(msg,addr)	# response message
		except Exception as e:
			print(f'node({self.node.port}) handle_message error: {e}')

	def handle_query(self,msg,addr):
		if msg['q'] == 'ping':
			request = {
				't':msg['t'],
				'y':'r',
				'r':{'id':self.node.id_b64}
			}
			data = bencode(request)
			self.send_message(data,addr)
		elif msg['q'] == 'find_node':
			target_id = base64.b64decode(msg['a']['target'])
			closest = self.node.route_table.find_closest_nodes(target_id)
			#?
			nodes_bin = b''.join([
				n.id + socket.inet_aton(n.address) + struct.pack('!H', n.port)
				for n in closest[:20]
			])
			request = {
				't':msg['t'],
				'y':'r',
				'r':{
					'id': self.node.id_b64,
					'nodes': base64.b64encode(nodes_bin).decode('ascii')
				}
			}
			data = bencode(request)
			self.send_message(data,addr)

	def handle_response(self,msg,addr):
		self.node.handle_response(msg['t'],msg)