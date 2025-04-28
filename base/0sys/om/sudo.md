#### sudo

```sh
#定义：允许某用户以另一用户的身份在哪个主机执行什么命令 	
	需输入密码				   #输入正确后，5分钟可不用再输入密码
	配置文件/etc/sudoers		#可通过专属命令 visudo 编辑
	
sudo
	-k	#每次sudo需要密码验证
	-l	#列出当前用户可使用的sudo类命令

	
```

#### 配置文件sudoers

```sh
#配置文件/etc/sudoers条目格式:
who	which_hosts(runas) command
    #解释：
    who				#用户
    which_hosts		#可连接的主机
    runas			#以某用户的身份
    command			#运行哪些命令
    
#sudo条目示例：
hadoop All(root) /usr/sbin/useradd,/usr/sbin/usermod
hadoop All(root) NOPASSWD:/usr/sbin/useradd,PASSWD:/usr/sbin/usermod	#sudo时useradd不需要输密码，usermod需要输入密码
hadoop All(root) /usr/sbin/passwd [a-zA-Z]*,!/usr/bin/passwd root		#sudo时不能修改root用户的密码
    
#sudo条目可使用别名，以下为定义别名的关键字：
who: User_Alias
which_hosts: Host_Alias
runas: Runas_Alias
command:Cmnd_Alias

#别名必须全部且只能大写字母的组合
    #用户别名：
    User_Alias USERADMIN = user1,user2,user3	#示例：定义USERADMIN别名，包括3个用户
    User_Alias USERADMIN2 = %group1				#示例：定义别名，包含用户组group中的用户		
    User_Alias USERADMIN3 = USERADMIN2				#示例：定义别名，包含其他别名

    #主机别名：
    Host_Alias
    	#可包含：
    	主机名
    	IP
    	网络地址
    	其他主机别名
    	
    #runas别名：
    Runas_Alias
    	用户名
    	%组名
    	其他Runas别名
    	
    #command别名：
    Cmnd_Alias
    	命令路径	#绝对路径
    	目录		#目录下所有命令
        其他命令别名
```

