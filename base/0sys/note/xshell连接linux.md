### openssh-server远程登录

> xshell4
>
> kalinux 5.18

```sh
思路：
1.远程linux 开启openssh-server服务:systemctl start ssh.service
	若没有，则安装：sudo apt install openssh-server
	查看ssh进程: ps - | grep ssh
2.本地xshell建立连接

3.若提示 'key exchange 算法错误'
	在linux，/etc/ssh/sshd_config里添加一行：
KexAlgorithms curve25519-sha256@libssh.org,ecdh-sha2-nistp256,ecdh-sha2-nistp384,ecdh-sha2-nistp521,diffie-hellman-group-exchange-sha256,diffie-hellman-group14-sha1,diffie-hellman-group-exchange-sha1,diffie-hellman-group1-sha1

4.若提示 'hostkey 算法错误'
	在linux，/etc/ssh/sshd_config里添加如下行：
# 在行尾增加",ecdh-sha2-nistp521"，以满足ecdsa公钥方式登录(密钥长度521)
KexAlgorithms curve25519-sha256,curve25519-sha256@libssh.org,diffie-hellman-group-exchange-sha256,ecdh-sha2-nistp521
# 在行尾增加",ssh-rsa"，以满足RSA 登录
HostKeyAlgorithms ssh-ed25519,ssh-ed25519-cert-v01@openssh.com,rsa-sha2-256,rsa-sha2-512,ssh-rsa
# 在行尾增加",ssh-rsa"，以满足RSA 登录
PubkeyAcceptedKeyTypes ssh-ed25519,ssh-ed25519-cert-v01@openssh.com,rsa-sha2-256,rsa-sha2-512,ssh-rsa

5.xshell乱码问题
	查看linux下编码：echo $LANG
	xshell：文件-属性-终端，设置编码一致

```

### ssh连接命令

```sh
#ssh默认端口22

ps -ef | grep ssh	#查看是否安装sshd服务
ssh -V	#查看版本

#连接命令
ssh username@host
ssh admin@192.168.0.1	#示例

#指定端口
ssh -p port user@host
```

