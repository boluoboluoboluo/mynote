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
&> 重定向标准和错误输出
set -C 禁止对已存在文件使用覆盖重定向
>| 强制覆盖

管道：前一个命令的输出，作为后一个命令的输入
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
		脚本参数$1,$2,..,  
		shift	#踢出1个参数
		shift 2	#踢出2个参数，此时$1表示第3个参数
	特殊变量 
		$? 	#上一个命令执行状态返回值0-255，0为成功
		$#	#表示参数个数
		$* 	#参数列表
	
#声明
declare -i SUM	#声明SUM为整型
```

```sh
#变量长度
${#var}
#变量赋值
${var:-word}	#如果var为空或未定义，则变量展开为word，否则，展开为var
${var:+word}	#如果var为空或未定义，不做任何操作，否则展开为word
${var:=word}	#如果var为空或未定义，则变量展开为word，并将展开后的值赋值给var

#取子串
${var:offset}	#从偏移offset处取子串
${var:offset,length}	#

```





### 循环

```sh
#示例
declare -i SUM=0
for i in {1..100};do
	let SUM=$SUM+$i
done
```

### 列表

```sh
#定义方式
a=(1 2 3)
a=({1..100})	#自动展开1-100
a=(`seq 1 100`)	#采用序列生成
#读取
echo ${a[2]}
```

### 关系运算

#### 算术运算

```sh
#1.使用let
a=1
b=2
let c=$a+$b
echo $c

#2.使用$[]
c=$[$a+$b]

#3.使用$(())
c=$(($a+$b))

#4. expr
c=`expr $a + $b`	#注意空格
```



### 一些命令

#### 示例

```sh
witch 命令	#命令路径
whatis 命令	#命令属性
type 命令		#命令类型	，然后用 help 命令 或者 man 命令	查看命令文档
 
`` ：命令替换
#示例
ls -l `which useradd`

"" ：弱引用，可以实现变量替换
'' ：强引用，不完成变量替换

#命令历史
history

#输出
echo hello	
echo -n hello	#不换行

#相当于windows下cls
printf "\033c"

#文件名
basename 	#获取当前文件名
basename `pwd`	#当前目录名
basename $0	#命令本身或脚本文件本身

#查看文件状态
stat file

#计算器 scale=2 保留2位精度， quit退出
bc
bc <<< "scale=2;111/22;"	

#排序
sort

#显示头部行数
head -1 filename	#显示一行

#显示文件行数，字符，字节
wc filename
ls | wc -l	#统计文件数量

#转大写
echo "hello" | tr a-z A-Z

#文件内容类型
file filename

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

#### grep

```sh
#文本查找
grep -i	#忽略大小写
grep -v	#反向，显示不匹配的
grep  --color	#匹配内容显示颜色

grep ‘hello‘ filename	#查找文件中有hello的行
grep 'a\?b' filename	#匹配a出现0-1次后面跟b
grep 'a.\{1,3\}b' filename	#匹配a后面任意字符1-3次后面跟着b
grep '^a.*' filename	#匹配a开头的行
grep '^$' filename 		#匹配空白行
grep '\bhello\b' filename	#匹配完整hello单词
grep '[abc]' filename 	#范围，匹配a或b或c出现的行
grep '[a-c]' filename 	#同上
grep '\(hello\)*' filename	#分组，hello出现任意次
grep '\(hello\).*\1' filename	#分组，hello出现2次,\1表示前面的第一个分组hello
grep '\(hello\)\|\(ab\)' filename	#匹配hello或ab出现的行	
grep '[[:space:]]' filename	#匹配空格的行

#扩展正则命令
egrep

#快速查找，不支持正则
fgrep
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





#### locate

```sh
#文件查找：非实时，模糊查找，查找是根据全系统文件数据库进行
#（linux系统会根据任务计划，每天定时收集文件信息存储到数据库。新系统该数据库不存在，可使用`updatedb`生成，生成慢）
#速度快
#不建议使用
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
		k	# +8k 查找大于8K的文件，-8k 查找小于8k的文件
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
read 	#和用户交互，输入

#示例
read -p "tips:"	x 	#输入时提示tips:输入内容保存到变量x
echo $x		#输出变量

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

#### 其他命令

```sh
#打印程序或库文件的共享依赖库
ldd	

#创建虚根
chroot /PATH/TO/TMPROOT
chroot /text/virroot /bin/bash	#示例
```

