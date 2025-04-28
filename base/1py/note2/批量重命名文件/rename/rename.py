# -*- coding:utf-8 -*-

import json
import time
import os
import re

source_dir = "s"
path = os.getcwd()
head = "2022-"
tail = "程序变更审批.pdf"
# tail = "程序变更测试报告.pdf"

def test():
	for root,dirs,files in os.walk(source_dir):
		# print(files)
		i = 1
		for f in files:
			# print(f)
			os.rename(path + "/s/" + f,path + "/s/" + head + str(i) + tail)
			i = i+1
		# rename(__file__ + "s/"+)


def main():
	test()
	
if __name__ == "__main__":
	main()