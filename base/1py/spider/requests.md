### requests

##### 安装

```sh
pip install requests
```

##### 示例

```py
import requests
import json

try:
    url = "https://www.baidu.com"
    headers = {'content-type': 'application/json',
           'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'}

    r = requests.get('url',params={'name':'ddd'},timeout=30) 
    #r = requests.post(url,headers=headers,data=json.dumps({'some': 'data'}))	#post
    r.raise_for_status()	#不是200,抛出httperror异常
    r.encoding='utf-8'
    #r.encoding=r.apparent_encoding	#根据内容分析编码
    print(r.text)
    #print(r.json())
except:
    print("异常")
```

##### 请求方式

```
requests.get(url,params=None,**kwargs)
requests.post(url,data=None,json=None,**kwargs)
requests.put(url)			# PUT请求
requests.delete(url)		# DELETE请求
requests.head(url) 			# HEAD请求
requests.patch(url) 		# PATCH请求
requests.options(url)   	# OPTIONS请求
```

##### 请求

```py
requests.request(method,url,**kwargs)
# **kwargs: 可选
params	#字典或字节序列，请求参数
data	#字典，字节序列或文件对象，请求体
json	#json格式请求体数据
headers	#字典，请求头
cookies	#字典
auth	#元组，支持http认证
files	#字典类型，传输文件
timeout	#超时时间，秒
proxies	#字典类型，代理服务器
allow_redirects	# True/False,默认Ture，重定向开关
stream	#True/False,默认false，获取内容立即下载开关
verify	#True/False,默认True，认证ssl证书开关
cert	#本地ssl证书路径
```

##### 响应

```py
r.url
r.encoding                       #获取当前的编码
r.encoding = 'utf-8'             #设置编码
#以encoding解析返回内容。字符串方式的响应体，会自动根据响应头部的字符编码进行解码。
r.text   
#以字节形式（二进制）返回。字节方式的响应体，会自动为你解码 gzip 和 deflate 压缩。
r.content                        
#以字典对象存储服务器响应头，但是这个字典比较特殊，字典键不区分大小写，若键不存在则返回None
r.headers                        

r.status_code                     #响应状态码
#返回原始响应体，也就是 urllib 的 response 对象，使用 r.raw.read()   
r.raw                             
r.ok                              # 查看r.ok的布尔值

#内容分析响应编码方式（备选编码方式）-网页编码
r.apparent_encoding

#Requests中内置的JSON解码器，以json形式返回,前提返回的内容确保是json格式的，不然解析出错会抛异常
r.json()                         
r.raise_for_status()             #失败请求(非200响应)抛出异常

r.request.headers                         #返回发送到服务器的头信息
r.request.body							#请求体
r.cookies                                  #返回cookie
#返回重定向信息,当然可以在请求是加上allow_redirects = false 阻止重定向
r.history   

r.iter_content#一块一块的遍历要下载的内容
	#示例：for chunk in r.iter_content(chunk_size=512):
r.iter_lines#一行一行的遍历要下载的内容
```

##### 异常

```py
r.raise_for_status()	#失败请求(非200响应)抛出异常

requests.ConnectionError	#网络连接错误异常，如dns查询失败，拒绝连接等
requests.HTTPError			#http异常
requests.URLRequired		#url缺失异常
requests.TooManyRedirects	#超过最大重定向次数，重定向异常
requests.ConnectTimeout		#连接超时异常
requests.Timeout			#请求超时异常
```



