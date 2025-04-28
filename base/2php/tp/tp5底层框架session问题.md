### tp5底层框架关于session的bug



设置session时：

```php
//当设置成''，空字符时，如果session中的var_name有指，会默认取之前存放的数据，无法设置成功
session('var_name','');
```

这个问题可能会导致bug，需注意！