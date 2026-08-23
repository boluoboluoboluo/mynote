import util
import config
import uuid
import time
import random
import os
import sys

#===========================================
# 下载 m3u8 文件
# m3u8_url: m3u8 文件地址
# headers: 请求头
#===========================================
def down_m3u8_file(m3u8_url,headers):
	# 启用session下载
	session = util.create_session()
	session.headers.update(headers)
	# 下载后保存到本地的文件名
	f_path = f"{config.TMP_DIR}/{uuid.uuid4().hex}.ts"	
	fout = None		# 文件读写流
	try:
		r = session.get(m3u8_url,timeout=15)	# 下载 m3u8 文件
		m3u8_piece_urls = util.parse_m3u8_media(r.text,m3u8_url)		# 解析m3u8文件,将得到的分片地址按顺序保存到列表
		# print("分片信息:",m3u8_piece_urls)
		# sys.exit(1)
		#本地写入文件流
		fout = open(f_path,"wb+")
		for m in m3u8_piece_urls:
			# print(f"准备下载分片url:{m['url']}")
			util.down_file(m["url"],session,fout)	# 流式下载
			print(f"共有 {len(m3u8_piece_urls)}个分片,分片 {m['name']} 已下载")
			time.sleep(random.uniform(0.2, 0.6)) 	# 随机暂停
	except Exception as e:
		os.path.exists(f_path) and os.remove(f_path)
		raise e
	finally:
		if session:session.close()
		if fout:fout.close()
	print("下载完成.")
	# 返回文件路径
	return f_path

