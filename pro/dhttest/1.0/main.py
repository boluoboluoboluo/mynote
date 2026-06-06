import Node
import time
import exit_handler
import os
import tools

node1 = Node.Node(port=6881)
node2 = Node.Node(port=6882)
node3 = Node.Node(port=6883)
node4 = Node.Node(port=6884)
node5 = Node.Node(port=6885)

node1.run()		# init route table .. open socket and listen message..
node2.run()
node3.run()
node4.run()
node5.run()

# if only know ip address info
node1.join_guide_node((node2.address,node2.port))
node2.join_guide_node((node3.address,node3.port))
node3.join_guide_node((node4.address,node4.port))
node4.join_guide_node((node5.address,node5.port))
time.sleep(5)

if os.path.exists(tools.ROUTE_FILE):
	node1.read_route_file(tools.ROUTE_FILE)
else:
	node1.find_node(node1) # expend nodes

exit_handler.handler(node1.save_route_table)


while True:
	time.sleep(1)

