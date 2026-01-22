AES加密，用的是第三方模块 pycryptodome。

> 模块安装命令：pip install pycryptodome

AES有好几种模式，本模块列了ECB，CFB，CBC三种模式。据说，CBC模式是其中公认的安全性最好的模式。

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import hashlib
import base64
from Crypto.Cipher import AES

##############################################
the_salt = "my_salt"

the_key = "my_key"
######################################################

class HashManager():
    #######AES加密，ECB模式#######
    def get_aes_ecb(self, the_string):
        aes = AES.new(self.pkcs7padding_tobytes(the_key), AES.MODE_ECB)           # 初始化加密器
        encrypt_aes = aes.encrypt(self.pkcs7padding_tobytes(the_string))          # 进行aes加密
        encrypted_text = str(base64.encodebytes(encrypt_aes), encoding='utf-8')   # 用base64转成字符串形式
        return encrypted_text


    #######AES解密，ECB模式#######
    def back_aes_ecb(self, the_string):
        aes = AES.new(self.pkcs7padding_tobytes(the_key), AES.MODE_ECB)             # 初始化加密器
        decrypted_base64 = base64.decodebytes(the_string.encode(encoding='utf-8'))  # 逆向解密base64成bytes
        decrypted_text = str(aes.decrypt(decrypted_base64), encoding='utf-8')       # 执行解密密并转码返回str
        decrypted_text_last = self.pkcs7unpadding(decrypted_text)                   # 去除填充处理
        return decrypted_text_last



    #######AES加密，CFB模式#######
    def get_aes_cfb(self, the_string):
        key_bytes = self.pkcs7padding_tobytes(the_key)
        iv = key_bytes
        aes = AES.new(key_bytes, AES.MODE_CFB, iv)                              # 初始化加密器，key,iv使用同一个
        encrypt_aes = iv + aes.encrypt(the_string.encode())                     # 进行aes加密
        encrypted_text = str(base64.encodebytes(encrypt_aes), encoding='utf-8') # 用base64转成字符串形式
        return encrypted_text


    #######AES解密，CFB模式#######
    def back_aes_cfb(self, the_string):
        key_bytes = self.pkcs7padding_tobytes(the_key)
        iv = key_bytes
        aes = AES.new(key_bytes, AES.MODE_CFB, iv)                                 # 初始化加密器，key,iv使用同一个
        decrypted_base64 = base64.decodebytes(the_string.encode(encoding='utf-8')) # 逆向解密base64成bytes
        decrypted_text = str(aes.decrypt(decrypted_base64[16:]), encoding='utf-8') # 执行解密密并转码返回str
        return decrypted_text




    #######AES加密，CBC模式#######
    def get_aes_cbc(self, the_string):
        key_bytes = self.pkcs7padding_tobytes(the_key)
        iv = key_bytes
        aes = AES.new(key_bytes, AES.MODE_CBC, iv)                              # 初始化加密器，key,iv使用同一个
        encrypt_bytes = aes.encrypt(self.pkcs7padding_tobytes(the_string))      # 进行aes加密
        encrypted_text = str(base64.b64encode(encrypt_bytes), encoding='utf-8') # 用base64转成字符串形式
        return encrypted_text


    #######AES解密，CBC模式#######
    def back_aes_cbc(self, the_string):
        key_bytes = self.pkcs7padding_tobytes(the_key)
        iv = key_bytes
        aes = AES.new(key_bytes, AES.MODE_CBC, iv)                              # 初始化加密器，key,iv使用同一个
        decrypted_base64 = base64.b64decode(the_string)                         # 逆向解密base64成bytes
        decrypted_text = str(aes.decrypt(decrypted_base64), encoding='utf-8')   # 执行解密密并转码返回str
        decrypted_text_last = self.pkcs7unpadding(decrypted_text)               # 去除填充处理
        return decrypted_text_last


    #######填充相关函数#######
    def pkcs7padding_tobytes(self, text):
        return bytes(self.pkcs7padding(text), encoding='utf-8')

    def pkcs7padding(self,text):
        bs = AES.block_size
        ####tips：utf-8编码时，英文占1个byte，而中文占3个byte####
        length = len(text)
        bytes_length = len(bytes(text, encoding='utf-8'))
        padding_size = length if (bytes_length == length) else bytes_length
        ####################################################
        padding = bs - padding_size % bs
        padding_text = chr(padding) * padding    # tips：chr(padding)看与其它语言的约定，有的会使用'\0'
        return text + padding_text


    def pkcs7unpadding(self,text):
        length = len(text)
        unpadding = ord(text[length - 1])
        return text[0:length - unpadding]
```

