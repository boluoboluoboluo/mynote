### windows11搭建服务器

1. 官网下载nginx：[http://nginx.org/en/download.html](http://nginx.org/en/download.html)

2. 将下载的nginx解压到指定目录，如c:/nginx

3. 删除nginx目录下html文件夹里面的内容

4. 将项目拷贝到html文件夹下（如vue3打包的项目）

5. 找到nginx.conf文件，用编辑器打开，修改：

   ```ng
   location / {
       root   html;
       index  index.html index.htm;
       try_files $uri $uri/ /index.html;
   }
   ```

6. 启动项目

   方式一：

   ```
   双击nginx.exe		#可能出现闪退，不建议使用
   ```

   方式二：	

   ```sh
   c:\nginx1.24>nginx.exe
   ```

   说明：此时不能ctrl+c结束，需要再打开一个终端，输入：

   ```sh
   c:\nginx1.24>nginx -s stop 		#或者 nginx -s quit
   ```

   补充：

   ```sh
   nginx -s reload  	#重启
   ```

7. 在浏览器中输入：http://localhost 查看
   
