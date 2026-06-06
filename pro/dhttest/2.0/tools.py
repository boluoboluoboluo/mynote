from urllib.parse import urlparse,parse_qs
import os
import logging
import bencode  #type:ignore
import re
from base64 import b32decode
from urllib.parse import unquote

ROUTE_FILE = "./route_table_cache.json"


logging.basicConfig(level = logging.INFO,format = '[%(asctime)s|%(levelname)s]%(message)s')
#生成日志句柄
logger = logging.getLogger("test")

handler1=logging.FileHandler("base-log.log")
handler1.setLevel(logging.INFO)
formatter=logging.Formatter('[%(asctime)s|%(levelname)s]%(message)s')
handler1.setFormatter(formatter)
logger.addHandler(handler1)

def log(msg):
	global logger
	logger.info(msg)


# 解析磁力链接
# 磁力链接的核心是 xt=urn:btih: 后的 Info Hash（40位16进制SHA-1哈希算法生成或32位Base32编码）
# 示例：
# magnet1 = "magnet:?xt=urn:btih:e8427a656de0af45e3db7d8513d8a4f2a38a6d4"
# magnet2 = "magnet:?xt=urn:btih:SUOLLD3ZJ6GWLWA35Z2E6E3ESKQC7J5"
def magnet_to_infohash(magnet_link):
    # 解码 URL 转义字符
    decoded_link = unquote(magnet_link)
    
    # 匹配十六进制或 Base32 的哈希值
    hex_match = re.search(r'urn:btih:([0-9a-fA-F]{40})', decoded_link)
    if hex_match:
        return bytes.fromhex(hex_match.group(1).lower())
    
    b32_match = re.search(r'urn:btih:([2-7A-Za-z]{32})', decoded_link, re.I)
    if b32_match:
        b32_str = b32_match.group(1).upper()
        # 补全 Base32 的填充
        b32_str += '=' * ((8 - len(b32_str) % 8) % 8)
        return b32decode(b32_str)
    
    raise ValueError("无法解析磁力链接中的 info_hash")

# 解析bt种子（bencode编码）
def parse_bttorrent(btfile):
	with open(btfile,'rb') as f:
		data = bencode.bdecode(f.read())

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