#### 摘要

win11简单搭建php8，nginx，mysql8，thinkphp8环境

> 官网下载：php8（zip版，非线程安全）[php-8.2.10-nts-Win32-vs16-x64](https://windows.php.net/download#php-8.2
>
> 官网下载：nginx（zip版）[nginx/Windows-1.24.0](https://nginx.org/en/download.html)
>
> 官网下载：mysql8（zip版）[mysql-8.1.0-winx64](https://dev.mysql.com/downloads/mysql/)

#### php安装

- 解压下载的zip，把根目录的php.ini-development改成php.ini

- 启动php-cgi，监听9000端口（可自行设置）。打开cmd终端，cd到安装目录，输入：

  ```
  c:\php8.0>php-cgi.exe -b 127.0.0.1:9000
  ```

#### nginx安装

- 解压下载的zip。修改nginx.conf文件：

  ```
  location ~ \.php$ {
      root           html;
      fastcgi_pass   127.0.0.1:9000;
      fastcgi_index  index.php;
      fastcgi_param  SCRIPT_FILENAME  $document_root$fastcgi_script_name;
      include        fastcgi_params;
  }
  ```

- 打开cmd终端，cd到安装目录，启动nginx：

  ```
  c:\nginx1.24>nginx.exe
  ```

  此时无法通过ctrl+c关闭nginx，需再打开一个cmd终端，输入`nginx -s stop` 或者 `nginx -s quit` 关闭

  nginx重启命令：`nginx -s reload`

- 在nginx目录下的html目录，编写index.php，用于测试

  ```
  <?php
  	echo "hello world";
  ?>
  ```

- 打开浏览器，输入：http://localhost/index.php，显示 hello world

#### mysql8安装

+ 解压下载的zip。在根目录下新建my.ini文件：（**部分参数根据情况自行修改**）

  ```
  [client]
  default-character-set=utf8
  [mysql]
  default-character-set=utf8
  [mysqld]
  character-set-server=utf8
  # 设置mysql的安装目录
  basedir=C:/z_install/mysql8/mysql-8.1.0-winx64/mysql-8.1.0-winx64
  # 设置mysql数据库的数据的存放目录
  datadir=C:/z_install/mysql8/mysql-8.1.0-winx64/mysql-8.1.0-winx64/data
  # 允许最大连接数
  max_connections=200
  # 允许连接失败的次数。这是为了防止有人从该主机试图攻击数据库系统
  max_connect_errors=10
  # 创建新表时将使用的默认存储引擎
  default-storage-engine=INNODB
  # 端口
  port=3307
  ```
  
+ 安装MySQL服务。**管理员权限**打开cmd，cd到安装目录下的bin目录，运行命令：

  ```
  c:\mysql8.1.0\bin>mysqld install mysql8
  ```

  说明：**这里我取服务名为`mysql8`**，可自行更改。

+ 初始化mysql数据库。此时会在安装目录下生成data目录，运行命令：

  ```
  c:\mysql8.1.0\bin>mysqld --initialize --console
  ```

  **此时会生成一串临时密码**，注意查看。

+ 启动mysql服务：

  ```
  c:\mysql8.1.0\bin>net start mysql8
  ```

  说明：停止服务为 `net stop mysql8` 卸载服务为：`sc delete mysql8`

+ 登录mysql，输入下面命令，回车，输入上面的临时密码：

  ```
  c:\mysql8.1.0\bin>mysql -P 3307 -u root -p
  ```

  *说明：由于我用的是3307端口，所以指定了端口*，（**如果电脑同时安装了其他版本的mysql，不指定端口，登录可能会出问题**）

+ 登录后，系统要求先修改密码，执行下面命令：

  ```
  mysql>ALTER USER 'root'@'localhost' IDENTIFIED BY '新密码';
  ```

#### 测试

 测试php访问mysql

* php打开mysqli扩展，编辑php.ini文件，下面两处前面的分号去掉：

  `extension=mysqli`

  `extension_dir = "ext"`

  *重启php-cgi*

* 登录mysql，执行建库建表等语句：

  ```
  create database test;		# 创建test数据库
  ```

  ```
  use test;					# 使用数据库
  ```

  ```
  # 建表
  DROP TABLE IF EXISTS `user`;
  CREATE TABLE `user` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `name` varchar(255) NOT NULL default "" COMMENT '名字',
    `age` int(11) NOT NULL default 0 COMMENT '年龄',
  
    PRIMARY KEY (`id`)
  ) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;
  ```

  ```
  # 添加数据
  insert into user values(null,'孙悟空','500');
  insert into user values(null,'猪八戒','300');
  ```

* nginx下的web应用目录html下，新建 sqltest.php：

  ```php
  <?php
  
  	$config["db_host"] = "localhost";
  	$config["db_port"] = "3307";
  	$config["db_user"] = "root";
  	$config["db_pass"] = "root";
  	$config["db_name"] = "test";
  
  	//数据库查询操作
  	function getquerydata($sql){
  		global $config;
  		//获取数据库连接
  		$link = getconnection($config);
  		$link->query("SET NAMES utf8");
  		$data = array();
  		$res = $link->query($sql);
  		if($res->num_rows > 0){
  			while($row = $res->fetch_assoc()){
  				array_push($data,$row);
  			}
  		}
  		if($link){
  			mysqli_close($link);
  		}
  		return $data;
  	}
  	//获取数据库连接
  	function getconnection($config){
  		$link = new mysqli($config['db_host'],$config['db_user'],$config['db_pass'],$config['db_name'],$config["db_port"]);
  		if($link->connect_error){
  			die("连接失败：".$link->connect_error);
  		}
  		return $link;
  	}
  
  	$sql = "select * from user";
  	$data = getquerydata($sql);
  
  	var_dump($data);
  
  ?>
  ```

* 测试，浏览器输入：http://localhost/sqltest.php
