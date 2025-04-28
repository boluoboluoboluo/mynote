##### 字符串以及文件的hash

```python
# -*- coding:utf-8 -*-

import os
import hashlib

# 其它python3版本使用此方法
def file_hash(file_path: str, hash_method) -> str:
	if not os.path.isfile(file_path):
		print('文件不存在。')
		return ''
	h = hash_method()
	with open(file_path, 'rb') as f:
		while True:
			b = f.read(8192)
			if not b:
				break	
			h.update(b)
	return h.hexdigest()


# 使用python3.8及以上可以用此方法，写法更简洁。
# def file_hash2(file_path: str, hash_method) -> str:
# 	if not os.path.isfile(file_path):
# 		print('文件不存在。')
# 		return ''
# 	h = hash_method()
# 	with open(file_path, 'rb') as f:
# 		while b := f.read(8192):
# 			h.update(b)
# 	return h.hexdigest()


def str_hash(content: str, hash_method, encoding: str = 'UTF-8') -> str:
	return hash_method(content.encode(encoding)).hexdigest()

def file_md5(file_path: str) -> str:
	return file_hash(file_path, hashlib.md5)

def file_sha256(file_path: str) -> str:
	return file_hash(file_path, hashlib.sha256)

def file_sha512(file_path: str) -> str:
	return file_hash(file_path, hashlib.sha512)

def file_sha384(file_path: str) -> str:
	return file_hash(file_path, hashlib.sha384)

def file_sha1(file_path: str) -> str:
	return file_hash(file_path, hashlib.sha1)

def file_sha224(file_path: str) -> str:
	return file_hash(file_path, hashlib.sha224)

def str_md5(content: str, encoding: str = 'UTF-8') -> str:
	return str_hash(content, hashlib.md5, encoding)

def str_sha256(content: str, encoding: str = 'UTF-8') -> str:
	return str_hash(content, hashlib.sha256, encoding)

def str_sha512(content: str, encoding: str = 'UTF-8') -> str:
	return str_hash(content, hashlib.sha512, encoding)

def str_sha384(content: str, encoding: str = 'UTF-8') -> str:
	return str_hash(content, hashlib.sha384, encoding)

def str_sha1(content: str, encoding: str = 'UTF-8') -> str:
	return str_hash(content, hashlib.sha1, encoding)

def str_sha224(content: str, encoding: str = 'UTF-8') -> str:
	return str_hash(content, hashlib.sha224, encoding)


def main():
	file_path = "C:/xxx/xxx/xxx.xx"
	hash_method = hashlib.sha512
	s = file_hash(file_path,hash_method)
	print(s)
	
if __name__ == "__main__":
	main()
```

