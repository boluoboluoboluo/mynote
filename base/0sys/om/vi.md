###  vi语法

```shell
:	#底部命令模式
:w	#保存
:q	#退出
:q!	#退出不保存
:wq	#保存退出
:wq!	#强制保存退出
:set nu 	#显示行号
:set nonu	#取消行号

`esc`	#退出命令模式
i	#输入模式
o 	#换行输入

命令模式
`0`	#回到行首
n`space`	#n为数字，跳转到行第n个字符
n`enter`	#向下移动n行
`gg`	#回到第一行
1`gg`	#回到第一行
n`gg`	#到第n行
`ctrl+d`	#向下移动半页
`ctrl+u`	#向上移动半页
n`k`	#向下n行
n`j`	#向上n行

`yy`	#复制行
n`y`	#复制光标往下n行
`dd`	#剪切行
`p`		#粘贴行
`x`		#向后删除字符
n`x`	#向后删除n个字符

`u`		#复原前一个动作
`ctrl+r`	#重做上一个动作
`.`		#重复前一个动作

/word	#word为字符串，n往下查找
?word	#往上查找




```

### vim常用

```sh
#配置文件
/etc/vimrc
~/.vimrc	#家目录下，当前用户有效（没有可新建）

vim + filename	#打开处于最后一行

ctrl+f	#向下翻屏
ctrl+b	#向上翻屏
ctrl+d	#向下半屏
ctrl+u	#向上半屏

0	#行首

#上下左右，前面按数字n，代表移动n个字符
h	#左
l	#右
k	#上
j	#下

x	#向后删除

dd	#剪切一行
yy	#复制行
p	#粘贴

u	#撤销
.	#重复上次操作
ctrl + r	#还原最近一次的撤销

#可视化
v	#光标操作
	d	#选中删除
	y	#选中复制
	p	#选中粘贴

#查找，末行模式
/pattern	#pattern为字符串，n往下查找，N往上查找
?pattern	#往上查找

#查找替换 末行模式下s命令
ADDR1,ADDR2s@PATTERN@string@[gi]	#ADDR1,ADDR2 为起始和结束地址 (.代表当前行，$代表最后行,%代表全文)

#显示行号 末行模式
set nu
set nonu	#取消显示行号

#忽略大小写
set ic

#设置自动缩进
set ai

#查找到的文本高亮显示
set hlsearch

#语法高亮
syntax on
```

```sh
w	#移动下一个单词词首
e	#跳至当前或下个单词词尾
b	#前一个单词词首

#编辑多个文件
vim file1 file2 ...
	next	#末行模式，切换下一个文件
	prev	#末行模式，切换上一个文件
	last	#最后一个文件
	first	#第一个文件
	qa		#全部退出
	
#分屏
ctrl+w,再按s	#水平拆分
ctrl+w,再按v	#垂直拆分
ctrl+w,加箭头	#在窗口间切换光标
#分屏显示多个文件
vim -o file1 file2	#水平分屏
vim -O file1 file2	#垂直分屏

#另存为 末行模式
w /path
ADDR1,ADDR2w /path		#部分内容另存

#读取另一个文件内容
r /path		#读取另一个文件内容到当前光标下(粘贴)

#和shell交互 末行模式
! command
```





### 备注

* 文件异常，非法退出等，打开文件出现下述提示：found a swap file by the name`
  解决：列出隐藏文件，删除对应swap文件

  

