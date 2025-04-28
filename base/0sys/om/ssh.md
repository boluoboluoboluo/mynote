###  ssh服务

```shell
#步骤一：主机认证
#步骤二：用户认证
	#方式一：基于口令认证
	#方式二基于密钥认证

#linux：openssh软件
#C/S架构
	服务端：sshd，配置文件/etc/ssh/sshd_config
	
    客户端：ssh,配置文件/etc/ssh/ssh_config
    	#一些命令：
    	ssh USERNAME@HOST [-p port]		#登录
    	ssh -l USERNAME HOST			#同上
    	ssh USERNAME@HOST 'COMMAND'		#远程主机执行命令（不登录）
    	
    	ssh-keygen		#密钥生成器（基于密钥认证）
    		-t			#指定加密方式，一般为rsa
    		-f			#指定存放路径，可省，默认~/.ssh/id_rsa
    		#用法：
    		ssh-keygen -t rsa -f ~/.ssh/id_rsa		#生成密钥，（一路回车即可）
    										#私钥保存在~/.ssh/id_rsa，（若没有.ssh则创建，权限700）
    										#公钥保存在~/.ssh/id_rsa.pub
    										#公钥需要追加保存到远程主机对应用户家目录下.ssh/authorized_keys文件中（或authorized_keys2文件）
    	
    	ssh-copy-id		#将公钥传输至远程服务器对应家目录的.ssh对应文件（自动快捷实现）
    		#用法
    		ssh-copy-id -i ~/.ssh/id_rsa.pub kk@192.168.1.100	#-i参数为指定本地公钥文件
    	
    	scp				#跨主机安全复制工具（复制数据）
    		#语法：
    		scp SRC DEST	
    			-r #参数，递归复制目录数据
    			-a	#复制文件及其存档属性数据(权限等)
    		#示例：
    		scp /temp/testfile kk@192.168.1.100:/temp	#本地数据复制到远程temp目录
    		scp kk@192.168.1.100:/temp/testfile /temp 	#远程数据复制到本地temp目录
    	
    	exit			#退出登录会话

```

#### dropbear

```sh
#嵌入式系统专用的ssh服务端和客户端工具，体积小
#略
```



### sftp

```sh
#既是客户端又是服务端
#语法：
sftp USERNAME@HOST		#登录
sftp> help				#显示帮助
sftp> get remote_file [local_dir]	#下载文件
sftp> mget remote_files [local_dir]	#批量下载文件
sftp> put local_file [remote_dir]	#上传文件
sftp> mput local_files [remote_dir]	#批量上传文件		
sftp> mput -r /test/ /home/test2/	#本地test下所有文件，传输到远程test2目录下
sftp> exit 							#退出
```

 



