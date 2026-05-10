

#### 图片xss

```sh
#如果图片被嵌入了恶意js代码
1.<img>加载的图片,安全 
2.浏览器打开图片的风险:
	--某些旧版浏览器会运行js代码
	--如果服务器返回的 Content-Type 是 text/html 而不是 image/jpeg，浏览器会把图片当成网页解析，从而执行其中的 JS 代码
3.svg格式图片,只要浏览器打开,js代码会立即执行
===============================
#防御:
1.服务器(nginx或apache)配置:
	X-Content-Type-Options: nosniff		#强调图片,告诉浏览器不要当成html运行
2.图片资源使用独立域名,使xss攻击失去立足点 	#同源策略保护
3.告诉浏览器下载而不是直接打开:
	Content-Disposition: attachment; filename="image.jpg"
4.图片渲染:清楚图片里的不明数据
5.设置权限:图片存放目录不能有执行脚本的权限
```

