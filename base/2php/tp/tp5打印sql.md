### tp5打印sql：
```php 
//查询最近的sql
db::table('table_name')->getLastSql();
```

```php
db::table('table_name')->where("id",1)->fetchSql(true)->select();
```

```sql
#常用于构建子查询
db::table('table_name')->where("id",1)->buildSql();
```

