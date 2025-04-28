from urllib.parse import urlparse,parse_qs
import os

ROUTE_FILE = "./route_table_cache.json"

# 解析磁力链接
# 磁力链接的核心是 xt=urn:btih: 后的 Info Hash（40位16进制或32位Base32编码）
'''
magnet_uri = "magnet:?xt=urn:btih:DAC343D2BD58343564EA1009B317995D824CAC8E"	#示例
info_hash = tools.parse_magnet(magnet_uri)	#解析磁力链接
print("info hash:",info_hash)
'''
def parse_magnet(magnet_uri):
	parsed = urlparse(magnet_uri)
	params = parse_qs(parsed.query)
	info_hash = params.get('xt',[''])[0].split(':')[-1]
	return info_hash

# local nodeid
def get_local_nodeid(port):
	file_name = "./nodeid-"+str(port)
	nodeid = ""
	with open(file_name,'ab+') as f:
		f.seek(0)
		s = f.read()
		if s:
			nodeid = s
		else:
			nodeid = os.urandom(20)
			f.write(nodeid)
	return nodeid

def xor_distance(id1, id2):
	return int.from_bytes(bytes([a ^ b for a, b in zip(id1, id2)]), 'big')