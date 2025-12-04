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

# response refer:
# OrderedDict([('ip', b"'\xb9\xd0\xd1\xcb\xe9"),
# 	      ('r', OrderedDict([('id', b"\x9f\x1a\xc2\xd4wI\xea\xb3\xeeF\xaf\xfaod](\x8f'\xbe\xf3"), 
# 			  ('nodes', b'\x9f\x1a\xda_6g\xe8A\xf4B\x96Y\xac[\xaal\xae\xc5\xca\x98T\xe1\xb3C\xcd\xee\x9f\x
#       1a\xdbi\xdc\xeb\xfe\xb2\xfb\xfdS\xbaliK\xd4`2\xbf\xa0\xaa\xf7\xee\xa5n\x05\x9f\x1a\xde\x97\xf2.@\x10&I\x80\
# 		x05\xfd\xf4\x92\xfb\xaf\xc6\x8fX\xb3\x05DG|\x8c\x9f\x1a\xdf\x10?\xd5\x86u\x16\x0e;\xf8q\xaeif\xcftu/\xd4X\x1b
# 		v`\xb3\x9f\x1a\xdc\xda\xe6O\xe8\xa3\n\xcf\x981\xd3\xeb~\x84\xb8\xc8Mwb>\x9d\xa1\xb4M\x9f\x1a\xd7)\xf8\xdcL\x9f\
# 			xf43\xe4\x13\xe5\xac\x97\x89\x8e\xd4~5>\xaf\x1a\xe4\xc5\xe4\x9f\x1a\xd6\x1d\xe9\x19\xef\xd3\xbd\x03@]GL\x
# 			d1\xb6}\x96\x80\x1a%\x84\xedY83\x9f\x1a\xc9\xd3=N\xbe\x93\xcaK\t\xca\x8e\x7f\x07<t\x0c\x12Y\xbc\x1b\x92\xb9\xbfK'), 
# 			('p', 52201), ('token', b'\xfcq1\xc5')])), ('t', b'u\xcc'), ('v', 'LT\x01/'), ('y', 'r')])

id = os.urandom(20)
tid = os.urandom(2)

info_hash = b'\xda\xc3C\xd2\xbdX45d\xea\x10\t\xb3\x17\x99]\x82L\xac\x8e'

request = {
	b't':os.fsencode(tid),
	b'y':b'q',
	b'q':b'get_peers',
	'a':{
		b'id':id,
		b'info_hash':os.fsencode(info_hash)
	}
} 

# hand query : OrderedDict([('a', OrderedDict([('id', b"\x9f\x1a\xc2\xd4wI\xea\xb3\xeeF\xaf\xfaod](\x8f'\xbe\xf3"),
# 					      ('info_hash', b'\x9f\x1a\xd9/\x150\xcb\xe1\xf7AR\xb0\x00\xf6\xea\x89\x18M\t\x83')])),
# 						    ('q', 'get_peers'), ('t', '\x0b\x1f'), ('v', 'LT\x01/'), ('y', 'q')])
# [addr:('88.234.85.252', 31880)]





# target_host = '60.186.55.57'
# target_port = 6881
addressinfo = ('82.208.124.59', 1537)

data = bencode(request)
print(f"send request ...")
server.sendto(data,addressinfo)

while True:
	time.sleep(1)