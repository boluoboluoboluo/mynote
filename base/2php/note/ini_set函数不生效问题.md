#### ini_set函数不生效问题

说明：即使设定范围是`PHP_INI_ALL`，在类Class内部代码中也不会生效

```php
//记住，不要写在class内部
ini_set("session.gc_maxlifetime","5");
ini_set("session.cookie_lifetime","5");

print_r(ini_get_all());exit;
```





#### 配置可被设定范围说明

这些模式决定着一个 PHP 的指令在何时何地，是否能够被设定。手册中的每个指令都有其所属的模式。例如有些指令可以在 PHP 脚本中用 [ini_set()](https://www.php.net/manual/zh/function.ini-set.php) 来设定，而有些则只能在 php.ini 或 httpd.conf 中。

例如 [output_buffering](https://www.php.net/manual/zh/outcontrol.configuration.php#ini.output-buffering) 指令是属于 `PHP_INI_PERDIR`，因而就不能用 [ini_set()](https://www.php.net/manual/zh/function.ini-set.php) 来设定。但是 [display_errors](https://www.php.net/manual/zh/errorfunc.configuration.php#ini.display-errors) 指令是属于 `PHP_INI_ALL` 因而就可以在任何地方被设定，包括 [ini_set()](https://www.php.net/manual/zh/function.ini-set.php)。



| 模式             | 含义                                                         |
| :--------------- | :----------------------------------------------------------- |
| `PHP_INI_USER`   | 可在用户脚本（例如 [ini_set()](https://www.php.net/manual/zh/function.ini-set.php)）或 [Windows 注册表](https://www.php.net/manual/zh/configuration.changes.php#configuration.changes.windows)以及 .user.ini 中设定 |
| `PHP_INI_PERDIR` | 可在 php.ini，.htaccess 或 httpd.conf 中设定                 |
| `PHP_INI_SYSTEM` | 可在 php.ini 或 httpd.conf 中设定                            |
| `PHP_INI_ALL`    | 可在任何地方设定                                             |