### shell

##### test

新建`test.sh`，写入：

```shell
#!/bin/bash
echo "hello world"
```

说明：#!是一个约定的标记，告诉系统该脚本用什么解释器执行，即使用哪一种shell

```shell
#使用#号注释
#多行注释如下(EOF可用其他符号代替)：
:<<EOF
注释内容...
注释内容...
EOF
#或者
#格式为：: + 空格 + 单引号。
: '
这是注释的部分。
可以有多行内容。
'

chmod +x ./test.sh		#使脚本具有执行权限
./test.sh		#执行脚本

#另一种执行方式
/bin/sh test.sh	#此时不需要在第一行指定解释器信息
```

##### common

```shell
#脚本内获取参数的格式为：$n。n 代表一个数字，1 为执行脚本的第一个参数，2 为执行脚本的第二个参数，以此类推
#其中 $0 为执行的文件名（包含文件路径

$#		#传递到脚本得参数个数
$*	#输出所有参数
$$	#当前进程id
$!	#后台运行得最后一个进程id



a=1		#等号两边无空格，bash进程有效
local a=1 	#局部变量，代码段有效（函数内）
echo $a	#输出
echo "我是 ${a}"
echo '我是 ${a}'		#单引号的任何字符都会原样输出

#readonly a	#a为只读变量
unset a	#删除变量（不能删除只读变量）
```

##### 字符串

```shell
str="abcd"
echo ${#str}	#获取字符串长度
echo "xxx"$str	#字符串拼接
echo ${str:1:2}	#提取子串，索引1开始提取2个，为bc
```

##### 数组

```shell
arr=(1 2)	#定义数组
arr[2]='a'
${arr[1]}	#读取数组
${arr[@]}	#获取数组所有元素
${#arr[@]}	#获取数组长度，或者${#arr[*]}

#关联数组（键值对形式）
declare -A site
site["google"]="www.google.com"
site["baidu"]="www.baidu.com"

echo ${site[*]}		#获取所有值
echo ${!site[*]}	#获取数组所有键
echo ${#site[*]}	#获取数组长度

```

##### 运算符

```shell
val=`expr 2 + 2`		#加法，+号两边有空格
echo "两数之和为 : $val"

val=`expr $a + $b`
val=`expr $a - $b`
val=`expr $a \* $b`
val=`expr $b / $a`
val=`expr $b % $a`
if [ $a == $b ]
then
else
fi
if [ $a != $b ]
then
fi

#关系运算
if [ $a -eq $b ]	#等于
if [ $a -ne $b ]	#不等于
if [ $a -gt $b ]	#大于
if [ $a -lt $b ]	#小于
if [ $a -ge $b ]	#大于等于
if [ $a -le $b ]	#小于等于
#布尔运算
if [ $a != $b ]		#不等于 ，非
if [ $a -lt 100 -a $b -gt 15 ]	#a>100 且 b小于15 ，与
if [ $a -lt 100 -o $b -gt 100 ]	#a>100 或 b大于100 ，或
#逻辑运算
if [[ $a -lt 100 && $b -gt 100 ]]		#逻辑and
if [[ $a -lt 100 || $b -gt 100 ]]		#逻辑or
#字符串运算
if [ $a == $b ]		#检查是否相对
if [ $a != $b ]		#不相等
if [ -z $a ]		#字符串长度是否为0
if [ -n "$a" ]		#字符串长度是否不为0
if [ $a ]			#字符串是否不为空


```

##### 文件测试运算符

| 操作符  | 说明                                                         | 举例                      |
| :------ | :----------------------------------------------------------- | :------------------------ |
| -b file | 检测文件是否是块设备文件，如果是，则返回 true。              | [ -b $file ] 返回 false。 |
| -c file | 检测文件是否是字符设备文件，如果是，则返回 true。            | [ -c $file ] 返回 false。 |
| -d file | 检测文件是否是目录，如果是，则返回 true。                    | [ -d $file ] 返回 false。 |
| -f file | 检测文件是否是普通文件（既不是目录，也不是设备文件），如果是，则返回 true。 | [ -f $file ] 返回 true。  |
| -g file | 检测文件是否设置了 SGID 位，如果是，则返回 true。            | [ -g $file ] 返回 false。 |
| -k file | 检测文件是否设置了粘着位(Sticky Bit)，如果是，则返回 true。  | [ -k $file ] 返回 false。 |
| -p file | 检测文件是否是有名管道，如果是，则返回 true。                | [ -p $file ] 返回 false。 |
| -u file | 检测文件是否设置了 SUID 位，如果是，则返回 true。            | [ -u $file ] 返回 false。 |
| -r file | 检测文件是否可读，如果是，则返回 true。                      | [ -r $file ] 返回 true。  |
| -w file | 检测文件是否可写，如果是，则返回 true。                      | [ -w $file ] 返回 true。  |
| -x file | 检测文件是否可执行，如果是，则返回 true。                    | [ -x $file ] 返回 true。  |
| -s file | 检测文件是否为空（文件大小是否大于0），不为空返回 true。     | [ -s $file ] 返回 true。  |
| -e file | 检测文件（包括目录）是否存在，如果是，则返回 true。          | [ -e $file ] 返回 true。  |

其他检查符：

- **-S**: 判断某文件是否 socket。
- **-L**: 检测文件是否存在并且是一个符号链接。

示例：

```shell
file="/var/www/runoob/test.sh"
if [ -r $file ]
then
   echo "文件可读"
else
   echo "文件不可读"
fi
```

##### echo

```shell
#read 命令从标准输入中读取一行,并把输入行的每个字段的值指定给 shell 变量
read name 
echo "$name It is a test"

#显示换行
echo -e "OK! \n" # -e 开启转义
echo "It is a test"

#显示不换行
echo -e "OK! \c" # -e 开启转义 \c 不换行
echo "It is a test"

#显示结果定向至文件
echo "It is a test" > myfile

#显示命令执行结果
echo `date`
```

##### printf

```shell
$ printf "Hello, Shell\n"		#换行

printf "%-10s %-8s %-4s\n" 姓名 性别 体重kg  
printf "%-10s %-8s %-4.2f\n" 郭靖 男 66.1234
printf "%-10s %-8s %-4.2f\n" 杨过 男 48.6543
printf "%-10s %-8s %-4.2f\n" 郭芙 女 47.9876
```

**%s %c %d %f** 都是格式替代符，**％s** 输出一个字符串，**％d** 整型输出，**％c** 输出一个字符，**％f** 输出实数，以小数形式输出。

**%-10s** 指一个宽度为 10 个字符（**-** 表示左对齐，没有则表示右对齐），任何字符都会被显示在 10 个字符宽的字符内，如果不足则自动以空格填充，超过也会将内容全部显示出来。

**%-4.2f** 指格式化为小数，其中 **.2** 指保留2位小数。



##### test命令

Shell中的 test 命令用于检查某个条件是否成立，它可以进行数值、字符和文件三个方面的测试。

```shell
num1=100
num2=100
if test $[num1] -eq $[num2]

a=5
b=6
result=$[a+b] # 注意等号两边不能有空格	,[]执行算数运算
echo "result 为： $result"

#测试文件
if test -e ./bash
then
    echo '文件已存在!'
else
    echo '文件不存在!'
fi
```

##### 流程控制

```shell
if condition1
then
    command1
elif condition2 
then 
    command2
else
    commandN
fi

if [ $(ps -ef | grep -c "ssh") -gt 1 ]; then echo "true"; fi		#使用与终端

#for
for var in item1 item2 ... itemN
do
    command1
    ...
done

for loop in 1 2 3 4 5
do
    echo "The value is: $loop"
done

#while
while condition
do
    command
done

int=1
while(( $int<=5 ))
do
    echo $int
    let "int++"
done

echo '按下 <CTRL-D> 退出'
echo -n '输入你最喜欢的网站名: '
while read FILM
do
    echo "是的！$FILM 是一个好网站"
done

#无限循环
while :
do
    command
done
#或
while true
do
    command
done
#或
for (( ; ; ))

#until
until condition
do
    command
done

#case
case 值 in
模式1)
    command1
    ...
    ;;		#表示break
模式2)
    command1
    ...
    ;;
esac

read aNum
case $aNum in
    1)  echo '你选择了 1'
    ;;
    2)  echo '你选择了 2'
    ;;
    *)  echo '你没有输入 1 到 2 之间的数字'	#代表default
    ;;
esac

#匹配字符串
site="runoob"
case "$site" in
   "runoob") echo "菜鸟教程"
   ;;
   "google") echo "Google 搜索"
   ;;
   "taobao") echo "淘宝网"
   ;;
esac

#跳出循环
break
continue
```

##### 函数

```shell
demoFun(){
    echo "这是我的第一个 shell 函数!"
}
echo "-----函数开始执行-----"
demoFun
echo "-----函数执行完毕-----"

#函数返回值在调用该函数后通过 $? 来获得，$? 仅对其上一条指令负责
#示例
funWithReturn(){
    echo "这个函数会对输入的两个数字进行相加运算..."
    echo "输入第一个数字: "
    read aNum
    echo "输入第二个数字: "
    read anotherNum
    echo "两个数字分别为 $aNum 和 $anotherNum !"
    return $(($aNum+$anotherNum))
}
funWithReturn
echo "输入的两个数字之和为 $? !"

#调用函数时可以向其传递参数。在函数体内部，通过 $n 的形式来获取参数的值，例如，$1表示第一个参数，$2表示第二个参数...
#注意，$10 不能获取第十个参数，获取第十个参数需要${10}。当n>=10时，需要使用${n}来获取参数。
#示例
funWithParam(){
    echo "第一个参数为 $1 !"
    echo "第二个参数为 $2 !"
    echo "参数总数有 $# 个!"
    echo "作为一个字符串输出所有参数 $* !"
}
funWithParam 1 2 


```

##### 输入/输出重定向

| 命令            | 说明                                               |
| :-------------- | :------------------------------------------------- |
| command > file  | 将输出重定向到 file。                              |
| command < file  | 将输入重定向到 file。                              |
| command >> file | 将输出以追加的方式重定向到 file。                  |
| n > file        | 将文件描述符为 n 的文件重定向到 file。             |
| n >> file       | 将文件描述符为 n 的文件以追加的方式重定向到 file。 |
| n >& m          | 将输出文件 m 和 n 合并。                           |
| n <& m          | 将输入文件 m 和 n 合并。                           |
| << tag          | 将开始标记 tag 和结束标记 tag 之间的内容作为输入。 |

> 需要注意的是文件描述符 0 通常是标准输入（STDIN），1 是标准输出（STDOUT），2 是标准错误输出（STDERR）。

```shell
#执行command1然后将输出的内容存入file1。
#注意任何file1内的已经存在的内容将被新内容替代。如果要将新内容添加在文件末尾，请使用>>操作符。
command1 > file1

#和输出重定向一样，Unix 命令也可以从文件获取输入
command1 < file1

#示例
wc -l users		#统计 users 文件的行数
wc -l < users	#统计 users 文件的行数
#注意：上面两个例子的结果不同：第一个例子，会输出文件名；第二个不会，因为它仅仅知道从标准输入读取内容。

command < infile > outfile	#执行command1，从文件infile读取内容，然后将输出写入到outfile中。
command 2>>file			# stderr 追加到 file 文件末尾
command >> file 2>&1	# stdout 和 stderr 合并后重定向到 file

#如果希望执行某个命令，但又不希望在屏幕上显示输出结果，那么可以将输出重定向到 /dev/null
command > /dev/null
command > /dev/null 2>&1	#屏蔽 stdout 和 stderr，这里的 2 和 > 之间不可以有空格
```

##### 文件包含

```shell
#Shell 也可以包含外部脚本。格式如下：
. filename   # 注意点号(.)和文件名中间有一空格
或
source filename

```

示例，test1.sh内容如下：

```shell
#!/bin/bash
# author:菜鸟教程
# url:www.runoob.com

url="http://www.runoob.com"
```

test2.sh，代码如下：

```shell
#!/bin/bash
# author:菜鸟教程
# url:www.runoob.com

#使用 . 号来引用test1.sh 文件
. ./test1.sh

# 或者使用以下包含文件代码
# source ./test1.sh

echo "菜鸟教程官网地址：$url"
```

我们为 test2.sh 添加可执行权限并执行：

```shell
chmod +x test2.sh 
./test2.sh 
```

**注：**被包含的文件 test1.sh 不需要可执行权限。

