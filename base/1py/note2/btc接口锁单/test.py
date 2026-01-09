#-*- coding:utf-8 -*-
#
import urllib3
import os
import time

def deal_orderfile():
	filename = "orderids.txt"
	filelog = "error.log"
	fin = None
	fout =None

	if not os.path.exists(filename):
		print('文件不存在，请检查')

	fin = open(filename,"rt")
	fout = open(filelog,"wt")

	for row in fin:
		tmpid = row.strip()

		res = send_request(tmpid)

		if "error" in res:
			fout.write(tmpid + ":" + res + "\n")
		time.sleep(0.1)
		print(tmpid + ":" + res)
		

	print("done..")
	fin.close()
	fout.close()

'''
发送请求
'''
def send_request(orderid):
	res = None
	http = urllib3.PoolManager()
	url = "xxx" + orderid
	headers = {
		'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
	}

	try:
		res = http.request('get',
				url,
				headers=headers,
				retries=False	#不使用重定向
			)
		
		json_str = res.data.decode()		# bytes 转 string
		return json_str
	except Exception as err:
		print("except..")
		print(err)
		return 'server error..'
	finally:
		if res:
			res.release_conn()

def main():
	deal_orderfile()
	
if __name__ == "__main__":
	main()