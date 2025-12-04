### 静态模式

```sh
#此方式只支持开发环境测试,勿用于生产环境!

#测试目录 打开终端执行:
python -m http.server
#浏览器输入 http://localhost:8000 访问
```

### 动态模式

```sh
#动态脚本方式:
python -m http.server --cgi
#需在测试目录下创建 cgi-bin 目录
#里面存放脚本,例如hello.py:		# 需包含 HTTP 头部和内容：
	#!/usr/bin/env python3
	print("Content-Type: text/html\n")  # \n 表示空行分隔头部与内容	
	print("<h1>Hello from Python!</h1>")
#浏览器输入 http://localhost:8000/cgi-bin/hello.py 访问
```

#### 请求参数获取

后台代码示例:

```py
#!/usr/bin/env python3
import os
import sys
from urllib.parse import parse_qs
import cgi
import json

print("content-type:","application/json")
print()

method = os.environ.get("REQUEST_METHOD","GET")

if method == 'GET':
	query_string = os.environ.get("QUERY_STRING","")
	params = parse_qs(query_string)
	print(params)
elif method == "POST":
	content_length = int(os.environ.get("CONTENT_LENGTH",0))
	post_data = sys.stdin.read(content_length)		#如果数据多(比如文件上传),不建议这一步
	content_type = os.environ.get("CONTENT_TYPE","")
	if content_type.startswith("application/x-www-form-urlencoded"):		#表单默认
		params = parse_qs(post_data)
		print(params)
	elif content_type == "application/json":
		params = json.loads(post_data)
		print(params)
	elif content_type.startswith("multipart/form-data"):
		# 前面的sys.stdin.read(content_length) 代码读取输入流后指针位置
		# 会影响cgi模式读取
		form = cgi.FieldStorage()	#文件上传需要导入cgi
		pp = form.getvalue("pp")	

		#获取文件
		# file_item = form['file1']
		# if file_item.filename:
		# 	# todo
		# 	pass
		print(pp)
	elif content_type == "text/plain":
		print(post_data)
	elif content_type == "application/xml":
		print(post_data)
```

前端js代码:

```js
async function param_test(){
    const base_url = "http://localhost:8000/cgi-bin/test.py"
	//====================== get
    const get_params = new URLSearchParams({
        p1:'get_param1',
        p2:'get_param2'
    })
    const r = await fetch(base_url + '?' + get_params)
    const r_text = await r.text()
    console.log(r_text)
    //====================== post json
    const post_json_params = {
        p1:'post_json_param1',
        p2:'post_json_param2'
    }
    const r2 = await fetch(base_url,{
        'method':'post',
        'headers':{
            'content-type':'application/json'
        },
        'body':JSON.stringify(post_json_params)
    })
    const r_text2 = await r2.text()
    console.log(r_text2)
    //===================== post url form
    const post_form_params = new URLSearchParams()
    post_form_params.append('p1','post_form_param1')
    post_form_params.append('p2','post_form_param2')
    const r3 = await fetch(base_url,{
        'method':'post',
        'headers':{
            'content-type':'application/x-www-form-urlencoded'
        },
        'body':post_form_params
    })
    const r_text3 = await r3.text()
    console.log(r_text3)
    //===================== post form data
    const post_formdata_params = new FormData()
    // post_formdata_params.append("file1",document.getElementById("file1").files[0])
    post_formdata_params.append("pp","post_formdata_param")
    const r4 = await fetch(base_url,{
        'method':'POST',
        //multipart/form-data 不需要设置headers
        'body':post_formdata_params
    })
    const r_text4 = await r4.text()
    console.log(r_text4)
}
```



#### 简易下载

说明: 页面提供 a 链接,点击, 服务器返回二进制流下载

目录结构

```
--应用目录
	--test.html
	--1.mp4
	--cgi-bin
		--down.py
```

down.py 代码:

```py
import requests
import os
import sys

file_name = "1.mp4"

# 设置下载头
print("Content-Type: application/octet-stream")
print(f"Content-Disposition: attachment; filename=\"{filename}\"")
# print("Cache-Control: no-store")
# print("Pragma: no-cache")
print()  # 结束头部

f_path = os.path.abspath(file_name)

with open(f_path,'rb') as f:
	while True:
		c = f.read(1024)
		if not c:
			break
		sys.stdout.buffer.write(c)
```

页面 test.html 代码:

```html
<!DOCTYPE html>
<html>
	<head>
		<title>test</title>
		<meta charset="utf-8">
	</head>
	<body>
		<a href="http://localhost:8000/cgi-bin/down.py" download="v.mp4">下载测试</a>
	</body>
</html>
```

#### 简易下载2

说明: 从网络资源返回流下载

down.py 代码修正:

```py
import requests
import os
import sys

filename = "1.mp4"

# 设置下载头
print("Content-Type: application/octet-stream")
print(f"Content-Disposition: attachment; filename=\"{filename}\"")
print()  # 结束头部

v_path = "http://localhost:8000/1.mp4"

res = requests.get(v_path,stream=True)
res.raise_for_status()

for chunk in res.iter_content(chunk_size=8192):
	sys.stdout.buffer.write(chunk)
    sys.stdout.buffer.flush()
```

