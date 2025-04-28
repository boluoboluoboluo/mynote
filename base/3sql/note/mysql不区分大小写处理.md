### mysql不区分大小写处理

```sql
select * from t_user where username = "Abc"
select * from t_user where username = "abc"
#上面两者一样

#使用binary区分
select * from t_user where binary usernsme = "Abc"
```



