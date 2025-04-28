### 打包到nginx

将打包后的dist文件夹，拷贝到nginx的项目目录html下

修改nginx配置文件nginx.conf，添加server如下：

```nginx
server {
        listen 8006;
        server_name localhost;
        index index.php index.html index.htm;
        charset utf-8;

        location / {
            root   html\dist;
            index  index.html index.htm;
            try_files $uri $uri/ /index.html;	#此句关键，防止页面刷新404问题！
        }
    }
```



