# -*- coding:utf-8 -*-

import os
from openpyxl import load_workbook
from openpyxl import Workbook
from Crypto.Util.Padding import pad
from Crypto.Cipher import AES
import base64
import hashlib
import codecs
import random

source_file = "./usersdata.xlsx"
dst_file = "./names.sql"

def create_sql(s_file,d_file):
	t_wb = load_workbook(s_file)
	t_sheet = t_wb.get_sheet_by_name('Sheet1')
	f = open(d_file,'w',encoding='utf-8')
	i = 1
	#i = 523
	
	while(True):
		if not t_sheet['A%d' % i].value:
			break
		# id = t_sheet['A%d' % i].value		#id
		username = str(t_sheet['A%d' % i].value)		#姓名
		if username:
			username = username.strip()	#去掉两端空格
			print(username)


		aes_username = create_pass(username)
		
		sql = "update hwc_firm_users set is_del=1  where aes_name = '%s' and firm_type='221008';" % (aes_username)

		f.write(sql)
		f.write("\n")
		i = i+1
		#print(str(i)+'       ',end='')
		# print("%s" % (id,aes_username))
	
	print("脚本生成成功!")
	
	f.close()

'''  '''
def aes_cipher(key, aes_str):
	# 使用key,选择加密方式
	aes = AES.new(key.encode('utf-8'), AES.MODE_ECB)
	pad_pkcs7 = pad(aes_str.encode('utf-8'), AES.block_size, style='pkcs7')  # 选择pkcs7补全
	encrypt_aes = aes.encrypt(pad_pkcs7)
	# 加密结果
	encrypted_text = str(base64.encodebytes(encrypt_aes), encoding='utf-8')  # 解码
	encrypted_text_str = encrypted_text.replace("\n", "")
	# 此处我的输出结果老有换行符，所以用了临时方法将它剔除
	return encrypted_text_str

''' 生成aes '''
def create_pass(aes_str):
	key =  "d279fb107a04cd885573183d3afc626b"
	encryption_result = aes_cipher(key, aes_str)
	return encryption_result

def main():
	s_file = source_file
	d_file = dst_file
	
	if not os.path.exists(s_file):
		print("源文件不存在，请检查")
		exit(0)
	create_sql(s_file,d_file)
	#dstr = create_pass('17701944005')
	#print(dstr)
	
if __name__ == "__main__":
	main()



