

#### 请屏脚本

新建立`cls`文件：

```sh
printf '\033c'
```

添加权限并拷贝到/usr/bin/目录：

```sh
chmod 755 cls
mv ./cls /usr/bin/
```

#### 切换目录

```sh
#切换到当前目录下的第一个目录（如果是目录的话）
cd `ls | sed -n '1p'`
```

#### 查看哪些用户可登录

```sh
#可使用bash登录的用户
cat /etc/passwd |grep "/bin/bash" | cut -d : -f 1
```



#### 添加用户脚本

添加

```sh
#!/bin/bash

#add test
#test账号存在则退出
id test &> /dev/null && (echo "user test exists..." && exit) && exit
#创建test账号失败则退出
! useradd test && exit
echo "user test has created ..."
#密码设置失败则退出
! (echo "123456" | passwd --stdin test)  && exit
echo "password has added ..."

#统计当前用户总数
USERS=`wc -l /etc/passwd | cut -d' ' -f1`
echo "$USERS users."
```

查看是否管理员

```sh
#!/bin/bash
#
NAME=test
USERID=`id -u $NAME` || exit	#用户不存在退出
[ $USERID -eq 0 ] && echo "admin" || echo "common user."

```

查看是否有账户用的bash

```sh
#!/bin/bash
#
grep 'bash$' /etc/passwd
NAME=$?
if [ $NAME -eq 0 ];then
  echo "yes,there has users use bash shell."
else
  echo "no,there has not users use bash shell."
fi
  
```

#### 算术脚本

参数之和

```sh
#!/bin/bash
#如果参数小于2个
if [ $# -lt 2 ];then
  echo "need 2 params"
  exit 8
fi
#2个参数相加
let s=$1+$2
echo $s
```

乘法（保留精度）

```sh
#!/bin/bash
a=2
b=4.1
SUM=$(echo "scale=2;$a*$b;" | bc -l) 
echo $SUM
```

#### case判断输入

```sh
#!/bin/bash

case $1 in
[0-9])
	echo "a digit";;
[a-z])
	echo "a lower";;
[A-Z])
	echo "a upper";;
*)
	echo "special character";;
esac
```

#### 读取并输出

```sh
#!/bin/bash
 
read -p "请输入一些文本: " input
echo "你输入的文本是: $input"
```

#### 控制台输出颜色

```sh
#示例
echo -e "\033[1;31;40m这是红色的字体\033[0m"

#说明
\033[ ：开始颜色设置。
1 ：字体加粗。
32 ：文字颜色，绿色。
41 ：背景颜色，红色。
m ：结束颜色设置。
\033[0m ：重置所有终端属性，包括颜色。

#文字颜色代码
30	#黑色
31	#红色
32	#绿色
33	#黄色
34	#蓝色
35	#紫色
36	#蓝绿色
37	#白色

#文字样式
0	#无效果
1	#加粗
2	#下划线
3	#斜体

#文字背景
40	#黑色
41	#红色
...同文字颜色，4开头
```

#### 默认赋值

```sh
A=3
echo ${A:-30}	#输出3
unset A
echo ${A:-30}	#输出30 (若为空或不存在，则使用默认赋值)
```

#### 引入配置文件

当前目录脚本` ./a.sh`，配置文件`./a.conf`

```sh
#./a.conf内容
A="hello"
```

```sh
#./a.sh内容
. ./a.conf	#引入配置文件
echo ${A}
```

#### 创建临时文件

```sh
#语法
mktemp file.XXX		# "XXX" 会生成随机数字，如file.PeE
mktemp -d file.XXX		# 创建临时目录
#创建临时文件并获取文件名
FILE='mktemp file.XXX'
echo $FILE
```

#### ping网段

```sh
#!/bin/bash
#
PINGFILE = `mktemp pingfile.XXXX`
NET=192.168.0
trap 'echo "quit.";exit 1' INT		#捕捉进程中断信号，退出
for I in {200..254};do
	if ping -c 1 -W 1 $NET.$I &> /dev/null;then
		echo "$NET.$I is up." | tee >> ./PINGFILE	#能ping通的写入文件
	else
		echo "$NET.$I is down."
	fi
done
```

#### txt2utf8

```sh
#!/bin/bash
dirs=$(find ./ -type f -name "*.txt")
for path in $dirs
do
	iconv -f gbk -t utf8 $path > $path.utf8
	rm $path
done

```

