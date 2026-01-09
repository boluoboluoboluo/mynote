##### nginx配置tp8

默认已安装如下环境：

> php-8.2.10-nts-Win32-vs16-x64
>
> tp8.0
>
> nginx-1.24.0



1. 开启php服务

   ```sh
   #通过php-cgi命令或者系统配置php-fpm服务启动
   php-cgi.exe -b 127.0.0.1:9000
   ```

   **注意：此时不要通过thinkphp的启动命令启动（会报错）**：~~php think run -p 8000~~

2. 编辑`nginx.conf`文件，添加一个server：

   ```nginx
   server {
   	listen 8005;
   	server_name localhost;
   	root C:/z_data/wkspace/php/tp8test/public;
       index index.php index.html index.htm;
       charset utf-8;
   
       location / {
           if (!-e $request_filename) {
   			# rewrite ^/index.php(.*)$ /index.php?=s=$1 last;
   			rewrite ^(.*)$ /index.php/$1 last;
   			break;
   		}
   	}
       location ~ \.php(/|$) {
           # fastcgi_pass unix:/tmp/php-cgi-74.sock;
           fastcgi_pass 127.0.0.1:9000;
           fastcgi_index index.php;
           fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
           include fastcgi_params;
           if ($fastcgi_script_name ~ "^(.+\.php)(/.+)$") {
               set $fastcgi_script_name2 $1;
               set $path_info $2;
           }
           fastcgi_param   PATH_INFO $path_info;
       }
   }
   ```

3. 启动nginx，浏览器访问`http://localhost:8005`