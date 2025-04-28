##### 查看

```sql
#查看用户
select * from pg_user;

#创建数据库：
CREATE DATABASE dbname;

#查看所有数据库：
\l
#选择数据库：
\c 数据库名
#查看数据库的所有表：
\dt
#查看表：
\d 表名
```

##### 导入导出

```sh
#导出数据库示例：在终端打开pgsql安装目录的bin目录执行下面命令：
pg_dump -h 127.0.0.1 -U postgres -d tianxuan > c:/tianxuan.sql
说明：-h 数据库ip -U 用户名 -d 数据库名

#导入数据库示例：
psql -U postgres -d tianxuan < c:/bl_admin.sql
说明：-U 用户名 -d 数据库名

#导出表示例：在终端打开pgsql安装目录的bin目录执行下面命令：
pg_dump -h 127.0.0.1 -U postgres -d tianxuan -t bl_admin > c:/bl_admin.sql
说明：-h 数据库ip -U 用户名 -d 数据库名 -t 表名	

#导入表示例：在终端打开pgsql安装目录的bin目录执行下面命令：
psql -U postgres -d tianxuan < c:/bl_admin.sql
说明：-U 用户名 -d 数据库名
```

##### 表操作

```sql
#建表语句：
-----------start
create table xx_users(
	id bigserial primary key not null,			#说明bigserial 代表类型为bigint，且能实现自增
	name character varying(50) not null default '',
	password character varying(500) not null default '',
	nick_name character varying(100) not null default '',
	email character varying(100) not null default '',
	detail text not null default '',
	createtime bigint not null default 0,
	updatetime bigint not null default 0
);
comment on column xx_users.createtime is '创建时间';		#注释
-----------end

#删除表：
drop table 表名

#添加列：
alter table 表名 add column 列名 类型 not null default 默认值;

#查询字段注释：
select description from pg_description
join pg_class on pg_description.objoid = pg_class.oid
where relname = '表名'

select coalesce(字段名,‘xxx’) from 表名	//如果字段为空，则替换为xxx
```

##### 日期时间

```sql
#时间戳：
#精确到秒：
 select floor(extract(epoch from now()))
#精确到小数：
select extract(epoch from now());   #结果："1574826646.79929"
#精确到毫秒：
select floor(extract(epoch from((current_timestamp - timestamp '1970-01-01 00:00:00')*1000)));

#时间戳转字符串：
to_char(to_timestamp(createtime),'yyyy-mm-dd hh24:mi:ss') as createtime		#示例：createtime为整型时间戳字段名
```



