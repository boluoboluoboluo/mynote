# -*- coding:utf-8 -*-

import requests
import time, threading



	
def send_request(d):
	
	url = "http://localhost:8000/mobile/test4/test?d=" + d
	res = requests.get(url)
	print(res.text)


if __name__ == '__main__':

	for i in range(1000):
		threading.Thread(target=send_request,args=(str(i),)).start()


















