#### 字符串hash

```py
import hashlib

#方法:
'''
hashlib.md5
hashlib.sha256 
hashlib.sha512 
hashlib.sha384 
hashlib.sha1 
hashlib.sha224
'''
def str_hash(content: str, hash_method, encoding: str = 'UTF-8') -> str:
	return hash_method(content.encode(encoding)).hexdigest()

#示例
content = "hello"
method = hashlib.md5		#指定hash方法
str_hash(content,method)
```

#### 文件hash

```python
# -*- coding:utf-8 -*-

import os
import hashlib

#方法:
'''
hashlib.md5
hashlib.sha256 
hashlib.sha512 
hashlib.sha384 
hashlib.sha1 
hashlib.sha224
'''
#python3.8及以上版本
def file_hash2(file_path: str, hash_method) -> str:
	if not os.path.isfile(file_path):
		print('文件不存在。')
		return ''
	h = hash_method()
	with open(file_path, 'rb') as f:
		while b := f.read(8192):		#py3.8以上使用海象运算符,更简洁
			h.update(b)
	return h.hexdigest()

#示例
file_path = "C:/xxx/xxx/xxx.xx"
hash_method = hashlib.sha512			#指定hash方法
s = file_hash(file_path,hash_method)
print(s)
```

