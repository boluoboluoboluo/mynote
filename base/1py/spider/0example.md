

##### 爬取京东网页

```py
import requests

url = 'https://item.jd.com/10059498042364.html'
kv = { 'User-Agent': "Mozilla/5.0" }
r = requests.get(url,headers=kv)

print(r.status_code)
#print(r.request.headers)
# print(r.text[:1000])
print(r.text)
```



##### 爬百度网页

根据关键字搜索

```py
#date:2024-02-23
#要绕过百度安全验证，需要cookie字段，以及http协议

import requests

url = "http://www.baidu.com/s"		#此处只能用http协议
cookie = ""		#此处需要cookie
headers = {
			'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
'Accept':"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
			'cookie':cookie
		}
params = {"wd":"孙悟空"}
r = requests.get(url,params=params,headers=headers)

print(r.status_code)
r.encoding="utf-8"
print(r.text)
```



