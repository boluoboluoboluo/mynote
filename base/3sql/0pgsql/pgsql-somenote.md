```sql
#建表时，实现id自增，需额外创建序列指向该id键

character[3]为定长字符串数组  插入格式：'{   }'
character varying(100)为变长字符串

#空字符串和null不一样，字段非空则必须指定值，否则插入空数据报错

#单引号表示值，双引号表示系统标识符：
select "age" from t_users where name='test' 

#pgsql查询时默认使用asc排序
#注意：pgsql默认使用asc排序，所以分页查找时结果会和预期不一致，所以建议查询时使用自定义排序
```



