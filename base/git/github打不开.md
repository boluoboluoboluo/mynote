

1. 进入网址https://websites.ipaddress.com/，搜索以下地址，查看 对应的ip

   > `www.github.com`

   > `github.global.ssl.fastly.net`

   > `assets-cdn.github.com`

2. 修改hosts文件，位置：`C:\Windows\System32\drivers\etc`

```sh
140.82.113.4 github.com

151.101.1.194 github.global.ssl.fastly.net
151.101.65.194 github.global.ssl.fastly.net
151.101.129.194 github.global.ssl.fastly.net
151.101.193.194 github.global.ssl.fastly.net

185.199.108.153 assets-cdn.github.com
185.199.109.153 assets-cdn.github.com
185.199.110.153 assets-cdn.github.com
185.199.111.153 assets-cdn.github.com
```

3. 刷新dns，检测

```sh
ipconfig /flushdns
ping github.com
```

