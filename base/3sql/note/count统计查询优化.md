### count统计查询优化

`count(*)`查询优化：

分析：单独`count(*)`查询很快，但是如果后面有`where`条件，会根据最终结果集的大小影响查询时间

```sql
#思路：先查一条id最大的记录last_id
select id from 表1 left jon 表2 ...
where 条件... order by id desc limit 1
#然后：
select count(*) where id <= last_id
```

这样查询就会很快




