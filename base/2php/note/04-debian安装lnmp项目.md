

> debian10.4
>
> nginx1.4
>
> php8.0
>
> mariadb10.3



#### 安装nginx

```sh
sudo apt update
sudo apt install nginx	#安装

sudo apt show nginx 	#查看
sudo systemctl status nginx 	#查看运行状态

#配置文件：
/etc/nginx/nginx.conf
```

#### 配置ngixn.conf

在http区域添加如下代码：

```nginx
server{
	  listen 8000;
	
	  location ~ \.php$ {
	    include snippets/fastcgi-php.conf;
	    fastcgi_pass unix:/run/php/php7.3-fpm.sock;
	  }
	}
```

#### 安装php

##### ~~安装php7.3~~

```sh
sudo apt update
sudo apt install php

php -v		#查看版本

#安装扩展
sudo apt install php-fpm	#默认会安装7.3
sudo apt install php-mysql php-cli php-gd	#安装通用库

#查看运行状态
sudo systemctl status php7.3-fpm
```

浏览器访问：http://127.0.0.1:8000

##### 安装php8.0

```sh
# 说明：由于本项目tp代码需>php8.0，所以重新安装

sudo apt update		#更新
#安装必要的软件包来添加非官方的软件源：
sudo apt install apt-transport-https ca-certificates gnupg2 software-properties-common
#添加PHP的官方GPG密钥：
sudo wget -O /etc/apt/trusted.gpg.d/php.gpg https://packages.sury.org/php/apt.gpg
#添加PHP的非官方源：
sudo add-apt-repository "deb https://packages.sury.org/php/ $(lsb_release -sc) main"

#再次更新索引
sudo apt update
#安装php及其常用扩展
sudo apt install php8.0 php8.0-cli php8.0-common php8.0-fpm php8.0-opcache php8.0-mysql php8.0-xml php8.0-gd php8.0-curl

#查看版本
php -v

#查看运行状态
sudo systemctl status php8.0-fpm
```

**<font color=red>注意：</font>** 

添加php非官方源后，再次执行更新索引，可能报错：

`无法下载 https://packages.sury.org/php/dists/buster/InRelease`

<u><font color=red>**说明**：php官方已不在支持buster</font></u> 

`When you go to https://packages.sury.org/php/dists/buster/ (with your browser) you get the 403 error. https://packages.sury.org/php/dists/bullseye/ works. `

<font color=red>**解决方法**</font>：此时需修改源配置文件`/etc/apt/sources.list`：

```sh
#将 deb https://packages.sury.org/php/ buster main 改成如下：
deb https://packages.sury.org/php/ bullseye main
```



####  安装mariadb

```sh
# 说明：debian不能直接安装mysql
# 这里安装mariadb

#如果报错（依赖关系）：先配置源

#安装命令
sudo apt update
sudo apt install mariadb-server		#安装服务，（自动启动）
sudo systemctl status mariadb		#查看服务状态

#安全加强 （测试环境可不用）
#脚本执行过程中，系统将提示为 root 帐户设置密码，删除匿名用户，限制 root 用户对本地计算机的访问权限并删除测试数据库。
sudo mysql_secure_installation

#改为经典身份验证，终端执行：
mysql

#运行以下SQL语句以更改经典身份验证：
ALTER USER 'root'@'localhost' IDENTIFIED VIA mysql_native_password;
ALTER USER 'root'@'localhost' IDENTIFIED BY 'your_root_passwd';

#在终端，使用新密码连接到 MariaDB 服务器：
mysql -u root -p
```

#### <u>示例：php和vue代码部署</u> 

> tp8项目代码
>
> vue3项目包

```sh
# tp8代码拷贝到用户目录/home/dbn/code/tp8test目录下
# vue3代码拷贝到/var/www/html/dist目录
# 修改nginx.conf配置文件（参考nginx相关文档，略）
	#php的server目录配置:
	root /home/dbn/code/tp8test/public
	#vue3的server目录配置：
	root /var/www/html/dist
	#修改：fastcgi_pass指向正确的php-fpm版本
# 执行相关sql脚本

#其他：
	#目录权限
	#nginx静态资源配置
	#日志配置
```

##### <font color=red>访问报错502</font> 

访问后端地址报错502，查看nginx错误日志/var/log/nginx/error.log：

报错内容：`connect() to unix:/run/php/php7.3-fpm.sock failed (13: Permission denied) while connecting to upstream,`...

```sh
# 此报错说明php8.0-fpm 不允许 nginx用户访问
# 查看php8.0-fpm.sock权限，发现创建者是www-data 	#(apt使用缺省用户www-data安装的)

#解决方式：
修改nginx配置文件第一条,改为：
user www-data;

#重启nginx
sudo systemctl restart nginx
```
