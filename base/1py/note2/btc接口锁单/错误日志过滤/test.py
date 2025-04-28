#-*- coding:utf-8 -*-
#
import urllib3
import os
import time

def deal_logfile():
	filelog = "error.log"
	filename = "orderids.txt"
	fin = None
	fout =None

	if not os.path.exists(filelog):
		print('文件不存在，请检查')

	fin = open(filelog,"rt")
	fout = open(filename,"wt")

	for row in fin:
		s = row.strip()

		arr = s.split(":")
		fout.write(arr[0] + "\n")
		print(s)
		
	print("done..")
	fin.close()
	fout.close()

def main():
	deal_logfile()
	
if __name__ == "__main__":
	main()