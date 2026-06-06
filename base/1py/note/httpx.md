```sh
# 说明
httpx 是一个现代的、支持同步和异步的 Python HTTP 客户端库

# 安装
pip install httpx

```

#### 同步

同步请求的用法与 `requests` 库几乎完全一致，可以无缝切换

```py
# 同步示例代码:

# 1. GET 请求（带查询参数）
params = {"name": "tt", "age": 18}
response = httpx.get("https://httpbin.org", params=params)
print(response.status_code) # 获取状态码

# 2. POST 请求（提交表单或 JSON）
data = {"key": "value"}
response_form = httpx.post("https://httpbin.org", data=data) # 表单提交
response_json = httpx.post("https://httpbin.org", json=data) # JSON提交

# 3. 解析响应内容
print(response.text)        # 文本格式
print(response.json())      # JSON 字典格式
print(response.content)     # 二进制字节流（如下载图片）
```

#### 连接池

```py
import httpx

# 相当于 requests 里的session
with httpx.Client() as client:
    # 可以设置通用的 headers 或 base_url
    client.headers.update({"User-Agent": "my-app/1.0.0"})
    
    res1 = client.get("https://httpbin.org")
    res2 = client.get("https://httpbin.org")
   
# 示例:
async with httpx.AsyncClient(headers=headers,http2=True,proxy=config.PROXY,timeout=15) as client:
    # 注意: client 里又写了请求头的话,会发生合并和覆盖
	await client.get(url,headers=headers)

如果 client.get(url,headers=headers) 又写了请求头的话,会发生合并和覆盖
```

#### 异步

##### 基础并发

```py
import asyncio
import httpx

async def fetch_data():
    # 注意：异步使用的是 AsyncClient
    async with httpx.AsyncClient() as client:
        response = await client.get("https://httpbin.org")
        print(response.status_code)

asyncio.run(fetch_data())


# 单次异步:
r = await httpx.AsyncClient(timeout=10,headers=headers,proxy=config.PROXY).get(m3u8_url)
```

##### 高并发

```py
import asyncio
import httpx

async def download_site(client, url):
    response = await client.get(url)
    return response.status_code

async def main():
    urls = [f"https://httpbin.org" for _ in range(5)]
    
    async with httpx.AsyncClient() as client:
        # 并发执行所有请求
        tasks = [download_site(client, url) for url in urls]
        results = await asyncio.gather(*tasks)
        print(results)

asyncio.run(main())

```

#### 其他

##### http2

`httpx `原生支持 `HTTP/2`，但需要通过 `pip install httpx[http2] `额外安装依赖

```sh
# 说明:
HTTP/2 是第二代超文本传输协议，相比旧的 HTTP/1.1，它最大的核心改进是 “多路复用”

# http1:
HTTP/1.1 的痛点：同一个 TCP 连接上，请求必须排队（先进先出）。如果前一个请求卡住了，后面的请求就得等（称为“头部阻塞”）。因此，浏览器通常限制对同一个域名只能同时开 6 左右的连接。
#http2:
HTTP/2 的解决方式：它允许在同一个 TCP 连接上同时发送无数个请求和响应。数据被拆分成碎片（帧）混杂在一起传输，到了对端再组装

对异步爬虫的好处：使用 httpx(http2=True) 时，你对同一个网站并发发起的几十个请求，可能只需要建立 一个 TCP 连接。这极大节省了服务器和客户端的握手时间，也更不容易被服务器误认为是恶意攻击
```

```py
# 会话 client 初始化时开启 http2=True
with httpx.Client(http2=True) as client:
    response = client.get("https://httpbin.org")
    print(response.http_version) # 输出: "HTTP/2"

```

##### 异常处理

```py
import httpx

try:
    response = httpx.get("https://httpbin.org", timeout=1.0)
    response.raise_for_status() # 如果状态码是 4xx 或 5xx 则抛出异常
except httpx.TimeoutException:
    print("请求超时")
except httpx.HTTPStatusError as exc:
    print(f"状态码错误: {exc.response.status_code}")
except httpx.RequestError as exc:
    print(f"网络连接或请求错误: {exc}")
except httpx.HTTPError as e:
    print(f"all error.")
```

##### 代理

```sh
# 若要使用 SOCKS5 代理，你需要先确保安装了额外的依赖
pip install httpx[socks]

```

```py
import httpx

# 无论是 Client 还是快捷方法（httpx.get）都可以直接传入 proxies
proxy = "http://127.0.0.1:7890"
# 本地 SOCKS5 代理示例
proxy = "socks5://127.0.0.1:1080"
# 带有账号密码的 SOCKS5 代理
proxy = "socks5://myuser:mypassword@192.168.1.100:1080"

with httpx.Client(proxy=proxy) as client:
    response = client.get("https://httpbin.org")
    print(response.json())

```

##### 流式

```py
import asyncio
import httpx
import aiofiles  # 需要先 pip install aiofiles

async def download_perfectly(url: str, save_path: str):
    async with httpx.AsyncClient(http2=True) as client:
        async with client.stream("GET", url) as response:		#核心代码
            response.raise_for_status()
            
            # 使用 aiofiles 异步打开文件
            async with aiofiles.open(save_path, "wb") as f:
                # 正确的迭代语法，无 SideNote 错字
                async for chunk in response.aiter_bytes(chunk_size=8192):	# 核心代码
                    # 异步写入，绝不阻塞主线程事件循环
                    await f.write(chunk)

async def main():
    await download_perfectly("https://example.com", "video.mp4")

# asyncio.run(main())


```

##### 控制并发

```py
# 注意: 在外部（全局或主函数）只初始化一次信号量 !
sem = asyncio.Semaphore(config.MAX_CONNECT_TASKS)

async def down_file(client, url,down_path, semaphore=sem):
    #在这里竞争同一个信号量资源
    async with semaphore:	# 核心代码
        async with client.stream("GET", url, headers=headers) as res:
        	res.raise_for_status()
```

##### 重试

```py
async def down_file(client, url,down_path, semaphore=sem):
    async with semaphore:	#在这里竞争同一个信号量资源
        for attempt in range(config.MAX_RETRY+1):
            try:
        		async with client.stream("GET", url, headers=headers) as res:
            		res.raise_for_status()
                    return
        	except httpx.HTTPError as e:
                if attemp == config.MAX_RETRY:
                    print("超过重试次数")
                    raise e
```

##### 任务组

```py
# 说明:
-- asyncio.TaskGroup 管理任务 	# pyton3.11+
-- 有1个任务异常,则其他任务都会终止

# 开启任务组
async def main():
	async with asyncio.TaskGroup() as tg:
	# 循环将任务注册进 tg。注意：此时任务已经开始在后台并发执行了！
		for url in urls:
		tg.create_task(down_file(url))
        
# asyncio.run(main())
```

