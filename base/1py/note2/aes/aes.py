# -*- coding:utf-8 -*-

import os
import re
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad
from Crypto.Cipher import AES
import base64
import hashlib
import codecs



''' 加密 '''
#aes-ecb-256
def aes_cipher(key, s_str):
	# 使用key,选择加密方式
	aes = AES.new(key.encode('utf-8'), AES.MODE_ECB)
	pad_pkcs7 = pad(s_str.encode('utf-8'), AES.block_size, style='pkcs7')  # 选择pkcs7补全
	encrypt_aes = aes.encrypt(pad_pkcs7)
	# 加密结果
	encrypted_text = str(base64.encodebytes(encrypt_aes), encoding='utf-8')  # 解码
	encrypted_text_str = encrypted_text.replace("\n", "")
	# 此处我的输出结果老有换行符，所以用了临时方法将它剔除
	return encrypted_text_str

''' 生成aes '''
def get_key():
	key =  "d279fb107a04cduuuu73183d3afcxxxx"
	return key

''' 解密 '''
def aes_dipher(key, aes_str):
	encrypted_text = base64.b64decode(aes_str)  # 解码

	#
	aes = AES.new(key.encode('utf-8'), AES.MODE_ECB)
	
	decrypt_aes = aes.decrypt(encrypted_text)

	re_str = unpad(decrypt_aes, AES.block_size, style='pkcs7')  # 选择pkcs7补全
	
	# 此处我的输出结果老有换行符，所以用了临时方法将它剔除
	return re_str.decode().strip()
	
if __name__ == '__main__':
	key = get_key()

	#加密
	# s_str = "17701944005"
	# to_str = aes_cipher(key,s_str)
	
	#解密
	aes_str = "rDsm57lth+fQ8pEfS4AKTw=="
	from_str = aes_dipher(key,aes_str)

	print ("%s" % from_str)
		
	




