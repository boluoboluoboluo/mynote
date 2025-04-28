### tp5闭包查询

sql语句where条件：

```sql
where (good_name like "49岁以上" or good_name like "49岁以下") 
```

对应php写法：

```php
$where["goods_name"] = [['like','%49岁以上%'],['like','%49岁以下%'],'or'];
```



若sql里or查询条件不一样：
```sql
where (o.status =0 or o.need_amount >0)
```

对应php写法：

```php
->where(function($q){       //闭包查询
    $q->where('o.status',0)
    ->whereOr('o.need_amount','>',0);
})
//或者：
$where2['o.status'] = 0;
$where2['o.need_amount'] = ['>',0];
->where(function($q) use($where2){
    $q->whereOr($where2);
})
```











