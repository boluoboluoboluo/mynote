import Node
import time
import exit_handler
import os
import tools
import socket
from tools import log
import asyncio

async def main():
	node1 = Node.Node(port=6881)

	await node1.run()

	# if only know ip address info : dht.transmissionbt.com -> 87.98.162.88
	# target_host = "dht.transmissionbt.com"
	# target_ip = socket.gethostbyname(target_host)
	# target_port = 6881
	# node1.join_guide_node((target_ip,target_port))

	# avaliable ip
	# node1.join_guide_node(('223.109.206.184',6889))
	await node1.join_guide_node(('114.80.9.182',6883))

	await asyncio.sleep(2)

	await node1.find_node(node1) # expend nodes

	# if os.path.exists(tools.ROUTE_FILE):
	# 	print(f'read route file...')
	# 	node1.read_route_file(tools.ROUTE_FILE)
	# else:
	# 	print(f'find node ...')
	# 	node1.find_node(node1) # expend nodes


	await asyncio.sleep(20)


	info_hash = b'\xab\xebK\xe4\xa4\x1d\x9a\xd4\x8f\xf1=`\xd46\x87&\x0f\xbd\x87\x99'
	# node1.get_peers(info_hash)


	exit_handler.handler(node1.save_route_table)

	log("loop...")

	while True:
		await asyncio.sleep(1)

asyncio.run(main())