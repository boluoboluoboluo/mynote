### 概要

#### 系统设定

```sh
系统设定
	默认输出设备：标准输出：stdout，1
	默认输入设备：标准输入：stdin，1
	标准错误输出：stderr，2
标准输入：键盘
标准输出和错误输出：显示器

I/O重定向
> 输出重定向，覆盖输出
>> 追加输出
< 输入重定向
2> 重定向错误输出
2>> 重定向错误追加输出
-------------
#2者等价,重定向标准和错误输出
&> 		#格式: command &> file.txt
2>&1 	#格式: command > file.txt 2>&1
-------------

set -C 禁止对已存在文件使用覆盖重定向
>| 强制覆盖

管道：前一个命令的输出，作为后一个命令的输入
语法:命令1 | 命令2	#管道后必须接命令
echo "hello" | tr 'a-z' 'A-Z'		#hello 转为 HELLO

#不显示
echo "hello" &> /dev/null	
```

#### shell介绍

```sh
登录式shell：
	正常终端登录
	su - username
	su -l username
非登录式shell：
	su username
	图形终端打开命令窗口
	自动执行的shell脚本
全局配置：
	/etc/profile, /etc/profile.d/*.sh, /etc/bashrc
个人配置：
	~/.bash_profile, ~/.bashrc

profile类文件：
	设定环境变量
	运行命令或脚本
bashrc类的文件：
	设定本地变量
	定义命令别名
	
登录式shell读取配置文件顺序：
/etc/profile -> /etc/profile.d/*.sh -> ~/.bash_profile -> ~/.bashrc -> /etc/bashrc
非登录式shell读取配置文件：
~/.bashrc -> /etc/bashrc -> /etc/profile.d/*.sh

#脚本执行会启动一个子shell进程：
	命令行启动的脚本会继承当前shell的环境变量
	系统自动执行的脚本（非命令行）需要自我定义环境变量
```

#### bash说明

```sh
#bash脚本,第一行添加：
#!/bin/bash

#bash脚本退出，退出码可自行指定，若无，则取退出前最后一条指定的状态码
exit i	#i可为0,1,2...

#执行方式1
bash xxx	#指定使用bash执行 xxx文件
#执行方式2
./xxx.bash	#执行当前路径的 xxx.bash 文件(文件需要有执行权限)

#测试脚本是否语法错误
bash -n xxx.bash

#显示单步执行步骤
bash -x xxx.bash
```

#### EOF

```sh
#自定义终止符
cat 1.txt
输入...
EOF		#输出EOF，终止

#示例
cat << EOF
...
EOF
```



### 变量

```sh
#bash变量类型：
	环境变量 export a=1
	本地变量 a=1（局部变量:local a=1）
	位置变量 
		脚本参数$1,$2,..,  #$0:当前脚本名字
		shift	#踢出1个参数
		shift 2	#踢出2个参数，此时$1表示第3个参数
	特殊变量 
		$? 	#上一个命令执行状态返回值0-255，0为成功
		$$	#当前进程id
		$!	#后台运行得最后一个进程id
		$#	#表示参数个数
		$* 	#参数列表
		
		$_	#上一个命令的最后一个参数	#如果只有命令,那就是命令本身,如果是引号,则为引号里的内容
	
```



### 一些命令

#### 示例

```sh
witch 命令	#命令路径
whereis 命令	#命令相关文件位置
whatis 命令	#命令属性
type 命令		#命令类型	，然后用 help 命令 或者 man 命令	查看命令文档
----------------
command &	#命令后面加 & 表示让命令后台运行

#命令替换
``
$()		#同上, 现取代上面	
$(command) 	#的作用是：先执行括号内的命令，然后将该命令的输出（结果）放回到原处，作为外层命令的参数
$(IFS=];b=ls]test;$b)		#等同于: ls test 	
	#实际上IFS以]为分割符,将 ls]test 分割成2部分ls 和 test 传给shell,执行时
	#Shell 尝试运行第一个片段（ls），并将后续片段（test）作为参数传给它

"" ：弱引用，可以实现变量替换
'' ：强引用，不完成变量替换

#命令历史
history
history -c		# 清楚命令历史 (输入命令时前面加空格可不留历史)
history -d num	# 清除某个命令

#相当于windows下cls
printf "\033c"

#文件名
basename 	#获取当前文件名
basename `pwd`	#当前目录名
basename $0	#命令本身或脚本文件本身

#计算器 scale=2 保留2位精度， quit退出
bc
bc <<< "scale=2;111/22;"	

#排序
sort
sort -u a.txt b.txt			#取并集
sort a.txt b.txt | uniq		#取交集
sort data.txt | uniq -u		#仅显示非重复行(即只出现过一次,没有重复过的行)

#显示头部行数
head -1 filename	#显示一行

#显示文件行数，字符，字节
wc filename
ls | wc -l	#统计文件数量

#cut命令 显示文件指定分隔符隔开的字段数据，默认分隔符为空格
cut -d : -f1 filename	# -d 指定分隔符为：，-f 1,3 第1,3个字段
echo "hello" | cut -c 1-3	#显示1-3的字符

#seq 语法 seq [起始数 [步进长度]] 结束数
seq 1 10	#列表1-10

#从标准输入中接收数据 xargs
echo "hello" | xargs echo	#输出hello
ls | xargs echo		#输出当前目录文件

#暂停
slee 3	#暂停3秒

#生成随机数生成器：熵池， random 0-32768，在如下文件取
#/dev/random 记录平时键盘等随机动作到熵池，熵池可能取空，引发阻塞
#/dev/urandom 模拟随机，不会阻塞
echo $RANDOM	#显示一个随机数
```

```sh
#通配符
*/ (单星号)：只匹配当前这一层的子目录。
**/ (双星号)：匹配当前层、下一层、下下层……直到最底层的所有目录。	#递归通配符
```

#### echo

```sh
#输出
echo hello	
echo -n hello	#不换行

echo *	#输出当前目录下的内容, 类似 ls
echo $(<xx.file)	#输出当前目录下文件 xx.file的内容,类似 cat
```

#### tr

```sh
#用于转换、压缩或删除字符。通常通过管道（pipe）接收标准输入，并将处理后的结果输出
tr [选项] SET1 [SET2]
-d (delete)：删除 SET1 中出现的所有字符。
-s (squeeze)：压缩连续重复的字符，使其只保留一个。
-c (complement)：取反，针对 SET1 以外的字符进行操作。
-t (truncate)：将 SET1 截断为 SET2 的长度进行匹配。 
echo "hello" | tr a-z A-Z			#转大写
echo "abc123" | tr -d '0-9'			#删除所有数字，输出 abc
echo "A   B" | tr -s ' '			#将多个空格变为一个，输出 A B
echo "a1b2" | tr -cd '0-9'			#仅保留数字，输出 12
echo "abcde" | tr -t 'abcde' '123'	#输出 123de
```

#### diff

```sh
#对比文件,查看不同
diff file1 file2
diff -u file1 file2		#友好格式查看
time diff file1 file2 	#查看耗时
```



#### grep

```sh
#文本查找 示例:
grep 'hello' filename		#查找文件中有hello的行
grep '\bhello\b' filename	#匹配完整hello单词
grep 'a\?' filename			#匹配a出现0-1次
grep '.\{1,3\}' filename	#匹配任意字符1-3次
grep '[abc]' filename 		#范围，匹配a或b或c出现的行
grep '[a-c]' filename 		#同上
grep '^a' filename			#匹配a开头的行
grep '^$' filename 			#匹配空白行
grep '[[:space:]]' filename	#匹配空格的行

grep '\(hello\)*' filename	#分组，hello出现任意次
grep '\(hello\).*\1' filename	#分组，hello出现2次,\1表示前面的第一个分组hello
grep '\(hello\)\|\(ab\)' filename	#匹配hello或ab出现的行	

#参数
-i	#忽略大小写
-v	#反向，显示不匹配的
-o	#仅显示匹配部分 
-P	#启用正则 (功能符号不需要使用 \ 转义)

#在目录下递归所有文件,查找某个字符串 不区分大小写
grep -rni "字符串" 目录路径
grep -rni "hello"	#当前目录及子目录递归查找所有文件,找出有"hello"的行

#-o	仅显示匹配部分 -P	启用正则
grep -oP '.{0-1}hello.{0-50}' filename	#只显示匹配部分内容

```

#### sed

##### 用法

```sh
#流编辑器，逐行处理文本，默认不编辑原文件，仅处理模式空间 
#处理结束，将模式空间打印至屏幕
sed [options] 'AddresssCommand' file ...	#语法

options:
	-n	#静默模式，不显示模式空间内容
	-i	#修改源文件（比较危险 ）
	-e	#执行多次，举例：sed -e '1d' -e '2d' file
	-f 	#从文件读取执行，
		举例：sed -f scrfile file	#scrfile内容为-e '1d' -e '2d'
	-r	#使用扩展正则

#参数
Addresss:
	1.StartLine,EndLine
		比如1，100
		$	#最后一行
	2./RegExp/		#正则
	3./pattern1/,/pattern2/
		第一次pattern1匹配的行开始,至第一次被pattern2匹配到的行结束
	4.LineNumber
		指定的行
	5.StartLine, +N
		从StartLine开始，向后的N行
Command：
	d	#删除符合条件的行
	p	#显示符合条件的行
	a \string	#在指定的行后面追加内容string
	i \string	#在指定行前面添加新行
	r filepath	#将指定文件内容添加，可用于合并文件
	w filepath	#将范围内容保存到filepath
	s/pattern/string/ 	#查找并替换，将pattern匹配内容替换成string,默认替换每行第1次匹配到的内容
		g	#修饰符，全局替换，示例: sed s/a/A/g filename	#将所有a替换成A
		i	#修饰符，忽略大小写
		分隔符/可换成别的字符，如 s#pattern#string# 或 s@pattern@string@ 等
		&	#引用pattern匹配到的串
	
	

```

##### 示例

```sh
sed -n '1p' filename	#显示第一行
sed '1,2d' filename	#删除文件的1-2行
sed '/root/d' filename #删除含有root的行
sed '2a \ppp'	filename	#在第2行追加ppp
sed 's/A/X/' filename	#将A替换成X
```

#### awk

```sh
顺序读取文件行，并进行切割，切割的每一段赋值给变量$1,$2...
#语法
awk 'pattern[action]' file		#pattern：匹配模式，action：处理动作
#示例 默认分隔符空格
df -Ph | awk '{print $1}'		#df数据每行根据空白字符分割（不管多少空格），取第一个字段
df -Ph | awk '{pring $0}'		#$0表示所有字段
df -Ph | awk '{pring $NF}'		#NF字段个数，$NF表示最后一个字段

awk -F: '{print $1,$3}' /etc/passwd		#指定分隔符为冒号:
```

#### find

```sh
#实时，精确，速度慢

#语法
find [查找路径] [查找标准] 查找后处理动作
查找路径：默认当前目录
查找标准：默认所有文件
处理动作：默认打印
#查找标准：
	-name 'filename'	#精确查找，按文件名
		*	#任意长度任意字符
		?	#
		[]	#
	-iname 'filename'	#不区分大小写
	-user	#根据属主查找
	-group	#根据属组查
	-uid	#根据uid查找
	-gid	#根据gid查找
	-nouser	#查找没有属主的文件
	-nogroup	#没有属组的文件
	-type	#根据类型查找
		f	#普通
		d	#目录
		c	#字符设备
		b	#块设备
		l	#链接文件
		p	#管道设备
		s	#套接字设备
	-size	#根据大小查找
		c	#字节
		k	# +8k 查找大于8K的文件，-8k 查找小于8k的文件
			# 注意!:向上取整规则 +1k 即 >1 即文件>= 2k
		M	# 
		G	# 
	-mindepth	#最小目录层级
	-maxdepth 	#最大目录层级，find -maxdepth 1 #值查找当前目录下（不在子目录查找）
	-empty	#查找空文件
	
	-atime	#访问时间 +5 表示5天前访问过 -5 表示5天内访问过
	-mtime	#修改时间
	-ctime	#状态改变时间
	-amin	#访问时间 +5 表示5分钟前访问过 -5 表示5分钟内访问过
	-cmin
	-mmin
	
	-perm mode	#根据权限匹配
		mode	#精确匹配	find ./ -perm 664
		/mode	#有一个权限匹配即可	find ./ -perm /664
		-mode	#包含才能匹配	find ./ -perm -664	#例：权限为755文件可以匹配
	
	
	#组合条件查找
	-not	#查找不匹配的结果
	-a		#与
	-o		#或

#查找后处理动作
	-print
	-ls		#类似ls
	-ok	COMMAND {} \;	#执行命令 例：find ./ -ok chmod o-w {} \;		#对查找文件去掉其他用户的写权限（根据提示输入y即可）
	-exec COMMAND {} \;	#同上，但无提示 例：find ./ -exec mv {} {}.new \;		#对查找文改名

#示例
find -name 'test'	#当前目录查找test文件
find -name 't*'
find ./ -not \( -user test1 -o -user test2 \)	#查找不属于test1,也不属于test2的文件
find . -readable -writable -type f	#可读,可写,文件类型
find . 	-size +1024c -size -2048c ! -executable	#文件大小:1024~2048字节,不可执行
```

#### xxd

```sh
#十六进制查看与反向转换工具

#将文件内容以“地址偏移量、十六进制原始码、ASCII 字符”三列显示
xxd filename	
xxd -l 64 filename	#只查看前64字节
xxd -s 0x400 filename	#从 1KB 的位置开始看
xxd -p filename		# 只看16进制内容,-p 代表 plain (纯净版)

echo "hello" | xxd -p	#将字符串转16进制

#将十六进制还原为二进制文件
xxd -r hex_file.txt > bin_file.bin	# -r 代表 reverse (反向)
```

#### dd

```sh
#使用dd命令复制，dd表示复制数据流
dd if=数据来源路径 of=数据复制路径	#示例：dd if=/test of=/home/test
    bs=1	#示例，block size大小
    count=2	#示例，block size数目
    seek=#	#创建数据，跳过的空间大小，示例 -seek=10
dd if=/dev/sda of=/mnt/usb/mbr.bakup bs=512 count=1	#备份mbr
dd if=/mnt/usb/mbr.bakup of=/dev/sda bs=512 count=1	#还原mbr
dd if=/dev/cdrom of=/root/rhe15.iso		#制作镜像

#/dev/zero 表示读0，数据要多少有多少（与/dev/null相反）
dd if=/dev/zero of=/home/swapfile bs=1M count=1024
sync	#数据立刻写入磁盘
```

#### read

```sh
read 	#和用户交互，输入  #read的内容在当前进程空间,退出进程即销毁

#示例
read -p "tips:"	x 	#输入时提示tips:输入内容保存到变量x
echo $x		#输出变量

read -t 3 x		#等待输入,3秒后超时
read -d ":" x	#读取到':'停止,默认遇到换行停止

#示例2
read x y	#输入的内容以空格分开，保存到x和y变量

```

#### watch

```sh
监控命令执行结果，并全屏显示

#示例
watch 'ls -l'		#查看当前目录情况，每隔2秒刷新
```

#### trap

```sh
#信号捕捉
# 语法：trap 'command' sig
trap 'echo hello' SIGINT	#捕捉SINGINT信号 ,注意：脚本里不能捕捉9和15信号
```

#### base64

```sh
base64 "字符串"	#编码
base64 -d "编码串"	#解码
```

#### hash

```sh
#查看最近使用的命令
hash
hash -r		#清空命令表
```

**计算hash值的命令:** 

| 算法       | 计算文件 hash 的命令 | 计算字符串 hash 的常用写法        |
| ---------- | -------------------- | --------------------------------- |
| **MD5**    | md5sum 文件名        | echo -n "你的字符串" \| md5sum    |
| **SHA1**   | sha1sum 文件名       | echo -n "你的字符串" \| sha1sum   |
| **SHA224** | sha224sum 文件名     | echo -n "你的字符串" \| sha224sum |
| **SHA256** | sha256sum 文件名     | echo -n "你的字符串" \| sha256sum |
| **SHA384** | sha384sum 文件名     | echo -n "你的字符串" \| sha384sum |
| **SHA512** | sha512sum 文件名     | echo -n "你的字符串" \| sha512sum |
| **BLAKE2** | b2sum 文件名         | echo -n "你的字符串" \| b2sum     |

**注意**： echo -n 中的 -n 非常重要！它表示**不输出换行符**，否则字符串后面会多一个 \n，导致 hash 值完全不同。

#### 其他命令

```sh
#打印程序或库文件的共享依赖库
ldd	

#创建虚根
chroot /PATH/TO/TMPROOT
chroot /text/virroot /bin/bash	#示例
```

