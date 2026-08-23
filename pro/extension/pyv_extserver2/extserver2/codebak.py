
# chrome 底层指纹

# 如果没安装，请先执行: pip install curl_cffi
from curl_cffi import requests

# 1. 必须使用 Session，确保底层复用同一个安全连接（TLS Session Resumption）
with requests.Session() as session:
    
    # 2. 只需要最基础的头部，把所有 : 开头的和干扰项全删掉
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "accept": "application/json, text/plain, */*",
        "accept-language": "zh-CN,zh;q=0.9",
    }
    
    # 3. impersonate="chrome" 是核心：让底层 TLS/HTTP2 指纹变成 100% 真实的 Chrome
    url = "你的那个专门URL"
    
    print("正在尝试第一次请求...")
    response = session.get(url, headers=headers, impersonate="chrome")
    
    print("状态码:", response.status_code)
    print("返回内容片段:", response.text[:500]) # 打印前500个字看是否成功
