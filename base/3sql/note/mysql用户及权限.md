## 一：用户管理



### 1：登录MySQL服务器

　　我们在安装完MySQL以后，就会通过root用户进行登录；那么root该怎么登录呢？所以我们启动MySQL服务后，可以通过mysql命令来登录MySQL服务器

```mysql
基本语法：mysql <-u username> <-p> [password] [-h hostname|hostIP] [-P port] [databaseName] [-e "SQL语句"]
详细介绍命令中的参数：
    -u：后面些当前登录的用户名。
    -p：输入密码，若直接-p 后面不携带密码，则回车后让其输入密码。
    -h：后面跟主机名或者IP，默认为localhost（127.0.0.1）
    -P：后面跟MySQL服务的端口，通过该参数连接到指定的端口。MySQL服务的默认端口是3306，不使用该参数时自动连接到3306端口。
    databaseName：指明登录到哪一个数据库中。如果没有该参数，登录后需要使用USE命令来选择数据库。
    -e：后面可以直接加SQL语句。登录MySQL服务器以后即可执行这个SQL语句，然后退出MySQL服务器。
示例：
    mysql -uroot -p1234 -h49.235.99.193 -P3306 mysql -e "select host,user from user;"
```



### 2：用户增删改

```sql
### 创建用户
基本语法：CREATE USER 用户名 [IDENTIFIED BY '密码'] [,用户名 [IDENTIFIED BY '密码']];
参数说明：
    用户名：
        其实MySQL用户名由 '用户名'@'主机名' 构成；即用户连接MySQL时所用主机的名字。如果在创建的过程中，只给出了用户名，
        而没指定主机名，那么主机名默认为“%”，表示一组主机，即对所有主机开放权限。
示例：
    CREATE USER 'zhangsan' IDENTIFIED BY '1234';
        -- 创建'zhangsan'，并且默认开放任意主机连接的权限
    CREATE USER 'wangwu'@'%' IDENTIFIED BY '1234';
        -- 创建'wangwu'，并且设置任意主机连接的权限
    CREATE USER 'xiaofeng'@'192.168.%.%' IDENTIFIED BY '1234';
        -- 创建'xiaofeng'，并且设置只能IP段为'192.168.*.*'的主机开放连接权限
    -- 查询创建用户（这个表的具体查询后面会说明）
        SELECT user, host FROM mysql.user;
        +---------------+-------------+
        | user          | host        |
        +---------------+-------------+
        | wangwu        | %           |
        | zhangsan      | %           |
        | xiaofeng      | 192.168.%.% |
        | mysql.session | localhost   |     -- 默认就存在
        | mysql.sys     | localhost   |     -- 默认就存在
        | root          | localhost   |     -- 默认就存在 root 用户
        +---------------+-------------+
注意：在MySQL8.0时需要指定用户名和用户名密码；而在MySQL5.7则不需要强制指定密码，不指定则无密码登录，如：mysql -uxxx 即可
注意：创建用户时最好'用户名'@'主机名' 写全，因为user和host是个联合主键；

### 修改用户
基本语法：RENAME USER <旧用户> TO <新用户>
参数说明：
    <旧用户>：系统中已经存在的 MySQL 用户账号
    <新用户>：新的 MySQL 用户账号
示例：
    RENAME USER 'zhangsan'@'%' TO 'zhangsan1'@'192.168.1.1';
        -- 修改'zhangsan'用户名为'zhangsan1'，并且只指定'192.168.1.1'的主机才可以连接

### 删除用户
基本语法：DROP USER <用户1> [, <用户2> ]...;
说明：用户的删除不会影响他们之前所创建的表、索引或其他数据库对象，因为 MySQL 并不会记录是谁创建了这些对象
示例：
    DROP USER 'wangwu'@'%', 'xiaofeng'@'192.168.%.%', 'zhangsan1'@'192.168.1.1';
        -- 删除了刚才创建的全部用户

### 修改当前用户密码
①：MySQL5.7版本修改当前用户密码：
    SET PASSWORD = PASSWORD('新密码');
②：MySQL通用推荐语法：
    ALTER USER USER() IDENTIFIED BY '新密码'; -- 注：USER()为当前用户函数
③：使用mysqladmin可执行程序修改密码
    mysqladmin -u用户名 -p当前登录账户的密码(旧密码) password 新密码
### 修改其它用户密码（一般只有root权限可以直接修改其它用户密码）
①：基本语法：ALTER 'user'@'host' [IDENTIFIED BY '新密码'] [, 'user'@'host' [IDENTIFIED BY '新密码']]…;
②：基本语法：SET PASSWORD FOR 'user'@'host' = '新密码';

注：其实上面的用户增删改查都可以使用基本的DML语句（INSERT，DELETE，UPDATE，SELECT）操作；但是强烈不推荐这种操作；
    推荐上面介绍的几种方式；因为使用基本的DML操作表后，它不能关联的操作其它残留当前用户的表信息；
    就如使用DELETE删除用户，就是一个单一的删除user表里面的记录，而使用DROP USER 删除命令会删除用户以及对应的权限，
    执行命令后你会发现mysql.user表和mysql.db表的相应记录都消失了。
```



### 3：用户密码管理

　　其实除了设置密码复杂度策略外，我们还可以设置密码自动过期，比如说隔30天密码会过期必须修改密码后才能继续使用，还可以设置密码重用策略，比如设置新密码不可以和之前几次的老密码重复；这样我们的数据库账号就更加安全了。下面我们来看下如何设置密码自动过期。

```sql
### 设置密码过期策略（单独）：
说明：
    ①：在MySQL中，数据库管理员可以 手动设置 账号密码过期，也可以建立一个 自动 密码过期策略。
    ②：过期策略可以是 全局的，也可以为 每个账号 设置单独的过期策略。
创建一个测试账号：CREATE USER 'tom'@'%' IDENTIFIED BY '1234';
其实我们使用 ALTER USER 语句来设置单个账号密码过期，也可以更改账号过期时间
查询当前创建的用户：
    SELECT user,host,password_expired,password_lifetime,password_last_changed,account_locked FROM mysql.user;
    +-------------+---------+----------------+-----------------+---------------------+--------------+
    |user         |host     |password_expired|password_lifetime|password_last_changed|account_locked|
    +-------------+---------+----------------+-----------------+---------------------+--------------+
    |root         |localhost|N               |             NULL|2023-01-09 14:03:45  |N             |
    |mysql.session|localhost|N               |             NULL|2021-12-26 17:20:11  |Y             |
    |mysql.sys    |localhost|N               |             NULL|2021-12-26 17:20:11  |Y             |
    |tom          |%        |N               |             NULL|2023-01-09 15:37:59  |N             |
    +-------------+---------+----------------+-----------------+---------------------+--------------+
使用 EXPIRE（到期） 来设置密码立即过期：
    ALTER USER 'tom'@'%' PASSWORD EXPIRE;
    SELECT user,host,password_expired,password_lifetime,password_last_changed,account_locked FROM mysql.user
        WHERE user='tom' AND host='%';
    +------+------+------------------+-------------------+-----------------------+----------------+
    | user | host | password_expired | password_lifetime | password_last_changed | account_locked |
    +------+------+------------------+-------------------+-----------------------+----------------+
    | tom  | %    | Y                |              NULL | 2023-01-09 15:37:59   | N              |
    +------+------+------------------+-------------------+-----------------------+----------------+
    -- 这时候去登录tom账号，修改其当前用户密码即可恢复操作
使用 EXPIRE NEVER（永不过期）来设置密码永不过期：
ALTER USER 'tom'@'%' PASSWORD EXPIRE NEVER;
    SELECT user,host,password_expired,password_lifetime,password_last_changed,account_locked FROM mysql.user
        WHERE user='tom' AND host='%';
    +------+------+------------------+-------------------+-----------------------+----------------+
    | user | host | password_expired | password_lifetime | password_last_changed | account_locked |
    +------+------+------------------+-------------------+-----------------------+----------------+
    | tom  | %    | N                |                 0 | 2023-01-09 15:37:59   | N              |
    +------+------+------------------+-------------------+-----------------------+----------------+
使用 EXPIRE INTERVAL（过期时间间隔）来设置密码的过期期限：
ALTER USER 'tom'@'%' PASSWORD EXPIRE INTERVAL 30 DAY;
    SELECT user,host,password_expired,password_lifetime,password_last_changed,account_locked FROM mysql.user
        WHERE user='tom' AND host='%';
    +------+------+------------------+-------------------+-----------------------+----------------+
    | user | host | password_expired | password_lifetime | password_last_changed | account_locked |
    +------+------+------------------+-------------------+-----------------------+----------------+
    | tom  | %    | N                |                30 | 2023-01-09 15:56:11   | N              |
    +------+------+------------------+-------------------+-----------------------+----------------+
让此账号使用默认的密码过期全局策略
    ALTER USER 'tom'@'%' PASSWORD EXPIRE DEFAULT;
    SELECT user,host,password_expired,password_lifetime,password_last_changed,account_locked FROM mysql.user
        WHERE user='tom' AND host='%';
    +------+------+------------------+-------------------+-----------------------+----------------+
    | user | host | password_expired | password_lifetime | password_last_changed | account_locked |
    +------+------+------------------+-------------------+-----------------------+----------------+
    | tom  | %    | N                |              NULL | 2023-01-09 15:56:11   | N              |
    +------+------+------------------+-------------------+-----------------------+----------------+

说明：mysql.user系统表记录着每个账号的相关信息，当password_expired字段值为 Y 时，代表此密码已过期，使用过期密码仍可以登录，
     但不能进行任何操作，进行操作会抛出错误；必须更改密码后才能进行正常操作。
     对于给定过期时间的账号，比如说设置30天过期，数据库系统会比较当前时间与上次修改密码的时间差值，如果距离上次修改密码时间
     超过30天，则将此账号密码标记为过期，必须更改密码后才能进行操作。
     password_expired：是否过期
     password_lifetime：过期时间
     password_last_changed：上次修改密码时间

### 设置密码过期策略（全局）：
    每个账号可以单独设置策略；也可以不单独设置而延用全局密码过期策略。
    要构建全局密码自动过期策略，请使用 default_password_lifetime 系统变量。在 5.7.11 版本之前，
    默认的 default_password_lifetime 值为 360 (密码大约每年必须更改一次)，之后的版本默认值为 0，表示密码不会过期。
    此参数的单位是天，比如我们可以将此参数设置为 30 ，则表示全局密码自动过期策略是 30 天。
    查询默认全局密码过期策略：
        SHOW VARIABLES LIKE 'default_password_lifetime';
        +---------------------------+-------+
        | Variable_name             | Value |
        +---------------------------+-------+
        | default_password_lifetime | 0     |
        +---------------------------+-------+
    方式①：使用SQL设置全局过期策略：
        SET GLOBAL default_password_lifetime = 30;
        或 SET PERSIST default_password_lifetime = 30;
            SHOW VARIABLES LIKE 'default_password_lifetime';
            +---------------------------+-------+
            | Variable_name             | Value |
            +---------------------------+-------+
            | default_password_lifetime | 30    |
            +---------------------------+-------+
    方式②：在my.cnf文件写入配置文件使得重启生效：
        [mysqld]
        default_password_lifetime = 30

### 设置密码重用策略（MySQL8.0特性）
    Ⅰ：手动设置密码重用方式（全局）
        -- 使用SQL方式
            SET GLOBAL password_history = 3; -- 设置不能选择最近使用过的3个密码
            SET GLOBAL password_reuse_interval = 365; -- 设置不能选择最近一年内的密码
        -- 使用my.cnf配置文件方式
            [mysqld]
            password_history=3
            password_reuse_interval=365
    Ⅱ：手动设置密码重用方式（单独）
        ALTER USER 'tom'@'%' PASSWORD HISTORY 5;
            -- 不能使用最近5个密码
        ALTER USER 'tom'@'%' PASSWORD REUSE INTERVAL 365 DAY;
            -- 不能使用最近365天内的密码
        ALTER USER 'tom'@'%' PASSWORD HISTORY 5 PASSWORD REUSE INTERVAL 365 DAY;
            -- 既不能使用最近5个密码，也不能使用365天内的密码
        -- 查询
        SELECT user,host,password_expired,password_reuse_history,password_reuse_time FROM mysql.user
            WHERE user='tom' AND host='%';
        +------+------+------------------+------------------------+---------------------+
        | user | host | password_expired | password_reuse_history | password_reuse_time |
        +------+------+------------------+------------------------+---------------------+
        | tom  | %    | N                |                      5 |                 365 |
        +------+------+------------------+------------------------+---------------------+

补充说明：MySQL的设置可以在运行时通过SET GLOBAL命令来更改，但是这种更改只会临时生效，到下次启动时数据库又会从配置文件中读取
         MySQL8新增了SET PERSIST命令，例如：default_password_lifetime = 30;MySQL 会将该命令的配置保存到数据目录下的
         mysqld-auto.cnf 文件中，下次启动时会读取该文件，用其中的配置来覆盖缺省的配置文件。
         如文件：{"Version": 2, "mysql_dynamic_variables":
                {"default_password_lifetime":
                {"Value": "180", "Metadata": {"Host": "", "User": "root", "Timestamp": 1672908539603706}}}}
```



### 4：用户账户锁定及解锁

　　从MySQL 5.7.8开始，用户管理方面添加了锁定/解锁用户帐户的新特性。

```sql
关键词：
    ACCOUNT LOCK    锁定账户
    ACCOUNT UNLOCK  解除锁定
创建一个带帐户锁的用户：
    CREATE USER 'jack'@'%' IDENTIFIED BY '1234' ACCOUNT LOCK;
    SELECT user,host,account_locked FROM mysql.user;
    +---------------+-----------+----------------+
    | user          | host      | account_locked |
    +---------------+-----------+----------------+
    | root          | localhost | N              |
    | mysql.session | localhost | Y              |
    | mysql.sys     | localhost | Y              |
    | jack          | %         | Y              |
    +---------------+-----------+----------------+
    若锁定的账户登录就会出现错误提示：
        ERROR 3118 (HY000): Access denied for user 'jack'@'localhost'. Account is locked.
解除账户的锁定：
    ALTER USER 'jack'@'%' ACCOUNT UNLOCK;
修改一个用户为锁定状态：
    ALTER USER 'jack'@'%' ACCOUNT LOCK;
```



## 二：权限管理



### 1：部分权限列表及授权原则

　　其实MySQL权限是有很多，具体权限划分很细，有库权限、表权限、字段权限等等，我们可以通过 **SHOW PRIVILEGES;** 语句查询全部权限。

```sql
基本权限说明：
    CREATE、DROP：可以创建新的数据库和表，或删除（移掉）已有的数据库和表。如果将MySQL数据库中的DROP权限授予某用户，
        用户就可以删除MySQL访问权限保存的数据库
    SELECT、INSERT、UPDATE、DELETE：允许在一个数据库现有的表上实施操作
    SELECT：只有在它们真正从一个表中检索行时才被用到
    INDEX：允许创建或删除索引，INDEX适用于已有的表。如果具有某个表的CREATE权限，就可以在CREATE TABLE语句中包括索引定义
    ALTER：可以使用ALTER TABLE来更改表的结构和重新命名表
    CREATE、ROUTINE：用来创建保存的程序（函数和程序），ALTER ROUTINE权限用来更改和删除保存的程序
    EXECUTE：用来执行保存的程序
    GRANT：允许授权给其他用户，可用于数据库、表和保存的程序
    FILE：使用户可以使用LOAD DATA INFILE和SELECT ... INTO OUTFILE语句读或写服务器上的文件，任何被授予FILE权
        限的用户都能读或写MySQL服务器上的任何文件（说明用户可以读任何数据库目录下的文件，因为服务器可以访问这些文件）
授予权限的原则：
    权限控制主要是出于安全因素，因此需要遵循以下几个经验原则：
        ①：只授予能满足需要的最小权限，防止用户干坏事。比如用户只是需要查询，那就只给select权限就可以了
        ②：创建用户的时候限制用户的登录主机，一般是限制成指定IP或者内网IP段
        ③：为每个用户设置满足密码复杂度的密码
        ④：定期清理不需要的用户，回收权限或者删除用户
```



### 2：用户授权及收回

　　给用户授权的方式有 2 种，分别是通过把角色（MySQL8特性）赋予用户给用户授权和直接给用户授权。用户是数据库的使用者，我们可以通过给用户授予访问数据库中资源的权限，来控制使用者对数据库的访问，消除安全隐患。

```sql
授权命令语法：
    ①：GRANT 权限1 [, 权限n] ON 数据库名称.表名称 TO '用户名'@'主机名';
    ②：GRANT 权限1 [, 权限n] ON 数据库名称.表名称 TO '用户名'@'主机名' [IDENTIFIED BY '密码'];
    注：第一种方式为MySQL8版本；
        第二种方式为MySQL5.7方式，它可以在修改权限时修改密码，若用户不存在也可以在指定权限时创建用户和密码
    为用户赋予权限：
        -- 导入数据库信息（方便后期授权）
            【腾讯文档】DQL_003_SQL语句(UTF8)
        -- 创建基本用户信息
            CREATE USER 'tom'@'%' IDENTIFIED BY '1234';
            CREATE USER 'jack'@'%' IDENTIFIED BY '1234';
            CREATE USER 'mark'@'%' IDENTIFIED BY '1234';
        -- 赋予权限
            GRANT SELECT,UPDATE ON demo_school.student TO 'tom'@'%';
                -- 为tom设置demo_school库里的student表中的SELECT,UPDATE权限
            GRANT SELECT ON demo_school.* TO 'jack'@'%';
                -- 为jack设置demo_school库里的所以表中的SELECT权限
            GRANT ALL PRIVILEGES ON *.* TO 'mark'@'%';
                -- 为mark设置所有库所有表的全部权限及其它权限（注：但当前用户不能赋予其它人权限）
            GRANT ALL PRIVILEGES ON *.* TO 'zhangsan'@'%' IDENTIFIED BY '12345';
                -- 创建一个'zhangsan'用户并设置所有权限（MySQL5.7版本可行）
查看赋予的权限：
    ①：查询当前用户的权限（3种方式）
        SHOW GRANTS;
        SHOW GRANTS FOR CURRENT_USER;
        SHOW GRANTS FOR CURRENT_USER();
    ②：查询指定用户权限（一般由root操作）
        SHOW GRANTS FOR 'tom'@'%';
            +--------------------------------------------------------------+
            | Grants for tom@%                                             |
            +--------------------------------------------------------------+
            | GRANT USAGE ON *.* TO 'tom'@'%'                              |
            | GRANT SELECT, UPDATE ON `demo_school`.`student` TO 'tom'@'%' |
            +--------------------------------------------------------------+
        SHOW GRANTS FOR 'jack'@'%';
            +-----------------------------------------------+
            | Grants for jack@%                             |
            +-----------------------------------------------+
            | GRANT USAGE ON *.* TO 'jack'@'%'              |
            | GRANT SELECT ON `demo_school`.* TO 'jack'@'%' |
            +-----------------------------------------------+
        SHOW GRANTS FOR 'mark'@'%';
            +-------------------------------------------+
            | Grants for mark@%                         |
            +-------------------------------------------+
            | GRANT ALL PRIVILEGES ON *.* TO 'mark'@'%' |
            +-------------------------------------------+
收回赋予的权限：
    基本语法：
        REVOKE 权限1 [, 权限n] ON 数据库名称.表名称 FROM '用户名'@'主机名';
    收回权限就是取消已经赋予用户的某些权限。收回用户不必要的权限可以在一定程度上保证系统的安全性。
    MySQL中使用 REVOKE语句 取消用户的某些权限。使用REVOKE收回权限之后，用户账户的记录将从db、host、tables_priv
    和columns_priv表中删除，但是用户账户记录仍然在user表中保存（删除user表中的账户记录使用DROP USER语句）
    举例（收回mark权限）：
        REVOKE ALL PRIVILEGES ON *.* FROM 'mark'@'%';
        -- 注：须用户重新登录后才能生效

其它说明：
①：为指定用户赋予能够赋予权限的权限
    例：为xiaowu赋予最高权限，并且还可以指定别人权限的权限
        CREATE USER 'xiaowu'@'%' IDENTIFIED BY '1234';
        GRANT ALL PRIVILEGES ON *.* TO 'xiaowu'@'%' WITH GRANT OPTION;
```



## 三：权限表说明

　　MySQL是一个多用户管理的数据库，可以为不同用户分配不同的权限，分为root用户和普通用户，root用户为超级管理员，拥有所有权限，而普通用户拥有指定的权限；这些用户信息和用户信息被保存在指定的表里面；MySQL关于用户的权限主要有五张表，分别为 **user、db、tables_priv、columns_priv、procs_priv**

### 1：user表

　　user表是MySQL中最重要的一张权限表，记录着用户的基本信息和数据库级别大粒度的权限信息，可以判断是否允许连接到服务器的账号信息，**该表里启用的所有权限都是全局级的，适用于所有数据库；**

```sql
我们可以通过SQL语句查看表结构: DESC mysql.user;
查询后表字段主要分为四大类：范围列（或用户列）、权限列、安全列、资源控制列
#### 范围列（或用户列）：
    该类型字段用来确定登录的用户名和登录主机
    Host：用户主机
    User：用户名称
    说明：
        host：表示连接主机类型
            ①：% 表示所有远程通过 TCP方式的连接
            ②：IP 地址 如 (192.168.1.2、127.0.0.1) 通过制定ip地址进行的TCP方式的连接
            ③：机器名 通过制定网络中的机器名进行的TCP方式的连接
            ④：::1 IPv6的本地ip地址，等同于IPv4的 127.0.0.1
            ⑥：localhost 本地方式通过命令行方式的连接 ，比如mysql -u xxx -p xxx 方式的连接。
        user：表示用户名，同一用户通过不同方式链接的权限是不一样的
#### 权限列：
    Select_priv：             是否可以通过SELECT命令查询数据
    Insert_priv：             是否可以通过INSERT命令查询数据
    Update_priv：             是否可以通过UPDATE命令查询数据
    Delete_priv：             是否可以通过DELETE命令查询数据
    Index_priv：              是否可以对索引进行增删查
    Alter_priv：              是否可以重命名和修改表结构
    Create_priv：             是否可以创建新的数据库和表
    Drop_priv：               是否可以删除现有数据库和表
    Grant_priv：              是否可以将自己的权限再授予其他用户
    Create_view_pri：         是否可以创建视图
    Show_view_priv：          是否可以查看视图
    Create_routine_priv：     是否可以更改或放弃存储过程和函数
    Alter_routine_priv：      是否可以修改或删除存储函数及函数
    Trigger_priv：            是否可以创建和删除触发器
    Event_priv：              是否可以创建、修改和删除事件
    Execute_priv：            表示是否拥有EXECUTE权限。拥有EXECUTE权限，可以执行存储过程和函数
    Create_tmp_table_priv：   是否可以创建临时表
    Lock_tables_priv：        是否可以使用LOCK TABLES命令阻止对表的访问/修改
    References_priv：         是否可以创建外键约束
    Reload_priv：             是否可以执行刷新和重新加载MySQL所用的各种内部缓存的特定命令，包括日志、权限、主机、查询和表
    Shutdown_priv：           是否可以关闭MySQL服务器。将此权限提供给root账户之外的任何用户时，都应当非常谨慎
    Process_priv：            是否可以通过SHOW PROCESSLIST命令查看其他用户的进程
    File_priv：               是否可以执行SELECT INTO OUTFILE和LOAD DATA INFILE命令
    Show_db_priv：            是否可以查看服务器上所有数据库的名字，包括用户拥有足够访问权限的数据库
    Super_priv：              是否可以执行某些强大的管理功能，例如通过KILL命令删除用户进程；使用SET GLOBAL命令修改
                                全局MySQL变量，执行关于复制和日志的各种命令。（超级权限）
    Repl_slave_priv：         是否可以读取用于维护复制数据库环境的二进制日志文件
    Repl_client_priv：        是否可以确定复制从服务器和主服务器的位置
    Create_user_priv：        是否可以执行CREATE USER命令，这个命令用于创建新的MySQL账户
    Create_tablespace_priv：  是否可以创建表空间
    Create_role_priv：        是否可以创建角色
    Drop_role_priv：          是否可以删除角色
    说明：权限列的字段决定了用户的权限，用来描述在全局范围内允许对数据和数据库进行的操作
        权限大致分为两大类，分别是高级管理权限和普通权限：
            ①：高级管理权限主要对数据库进行管理，例如关闭服务的权限、超级权限和加载用户等；
            ②：普通权限主要操作数据库，例如查询权限、修改权限等。
    user表的权限列包括Select_priv、Insert_ priv等以priv结尾的字段，这些字段值的数据类型为ENUM，
    可取的值只有Y和N：Y 表示该用户有对应的权限，N 表示该用户没有对应的权限。从安全角度考虑，这些字段的默认值都为N
#### 安全列：
    ssl_type：                支持ssl标准加密安全字段
    ssl_cipher：              支持ssl标准加密安全字段
    x509_issuer：             支持x509标准字段
    x509_subject：            支持x509标准字段
    plugin：                  引入plugins以进行用户连接时的密码验证，plugin创建外部/代理用户
    authentication_string：   密码
    password_expired：        密码是否过期 (N 未过期，y 已过期)
    password_last_changed：   记录密码最近修改的时间
    password_lifetime：       设置密码的有效时间，单位为天数
    account_locked：          用户是否被锁定（Y 锁定，N 未锁定）
    Password_reuse_history：  历史重用密码次数
    Password_reuse_time：     历史重用密码天数
    说明：
        ①：通常标准的发行版不支持ssl，读者可以使用 SHOW VARIABLES LIKE "have_openssl" 语句来查看是否具有ssl功能
            如果have_openssl的值为 DISABLED，那么则不支持 ssl 加密功能
        ②：即使password_expired为“Y”，用户也可以使用密码登录 MySQL，但是不允许做任何操作
            password_expired为“Y”代表密码已经过期
        ③：authentication_string为MySQL5.7+版本的密码存储列
            其实在早些版本时，所有密码串通过password(明文字符串) 生成的密文字符串。MySQL8.0在用户管理方面增加了
            角色管理，默认的密码加密方式也做了调整，由之前的SHA1改为了SHA2，密码不可逆。同时加上MySQL 5.7的禁用
            用户和用户过期的功能，MySQL在用户管理方面的功能和安全性都较之前版本大大的增强了。
            MySQL5.7及之后版本的密码保存到 authentication_string 字段中不再使用password 字段
        ③：引入plugins以进行用户连接时的密码验证
            其实密码加密在5.7时使用的是“mysql_native_password”加密方式，总的来说不怎么安全，可以通过撞库的方式破解；
            在MySQL8.0时使用“caching_sha2_password”加密方式，即使相同的密码生成的密文也是不一样的；
            注：我们要使用低版本的navicat来连接MySQL8.0会导致连接失败，要么升级navicat或者更改加密方式
#### 资源控制列：
    max_questions：           规定每小时允许执行查询的操作次数
    max_updates：             规定每小时允许执行更新的操作次数
    max_connections：         规定每小时允许执行的连接操作次数
    max_user_connections：    规定允许同时建立的连接次数
    说明：资源控制列的字段用来限制用户使用的资源，字段的默认值为 0，表示没有限制。
        一个小时内用户查询或者连接数量超过资源控制限制，用户将被锁定，直到下一个小时才可以在此执行对应的操作。
        可以使用 GRANT 语句更新这些字段的值

补充查询常用信息：
    ①：查询用户基本信息(MySQL5.7)
        SELECT Host '主机', User '用户名',password_expired '密码是否过期',password_lifetime '密码预计过期天数',
            password_last_changed '上次修改密码时间', account_locked '用户是否被锁定' FROM mysql.user;
    ②：查询用户基本信息(MySQL8.0)
        SELECT Host '主机', User '用户名',password_expired '密码是否过期',password_lifetime '密码预计过期天数',
            password_last_changed '上次修改密码时间', account_locked '用户是否被锁定',Password_reuse_history
            '历史重用密码次数', Password_reuse_time '历史重用密码天数' FROM mysql.user;
补充说明：
    ①：user表中的一些权限是全局级的，适用于所有数据库；所以要想设置到user表上权限需要全局数据库，(主要 *.* )
        如：GRANT SELECT,DELETE ON *.* TO 'tom'@'%';　　　　　　-- 这时候我们就可以查看user表中的指定用户记录下拥有了全局数据库的SELECT,DELETE权限
```

### 2：db表

　　db表主要存储了用户对某个数据库的操作权限；其中db表用户列有3个字段，分别是Host、User、Db，标识从某个主机连接某个用户对某个数据库的操作权限，这3个字段的组合构成了db表的主键。

```sql
我们可以通过SQL语句查看表结构: DESC mysql.db;
查询后表字段主要分为两大类：范围列（或用户列）、权限列
#### 范围列（或用户列）：
    Host：       主机名
    Db：         数据库名
    User：       用户名
#### 权限列：
    db表中的权限列和user表中的权限列大致相同，只是user表中的权限是针对所有数据库的，而db表中的权限只针对指定的数据库。
    如果希望用户只对某个数据库有操作权限，可以先将user表中对应的权限设置为N，然后在db表中设置对应数据库的操作权限。

补充说明：
    ①：db表中的权限是针对指定数据库；所以要想设置到db表上权限需要指定数据库，(主要 数据库名称.* )
        如：GRANT SELECT,DELETE ON demo_school.* TO 'tom'@'%';
            -- 这时候我们就可以查看db表中多出来一条user为tom的记录，并且只有SELECT,DELETE权限
```

### 3：tables_priv表

　　tables_priv表用来对表设置操作权限

```sql
我们可以通过SQL语句查看表结构: DESC mysql.tables_priv;
#### 范围列
    Host：        主机名
    Db：          数据库名
    User：        用户名
    Table_name：  表名
    说明：tables_priv权限表记录了host、db、user、table_name四个字段正好构建一个联合主键
#### 权限列
    Table_priv： 表示当前表的操作权限；权限如下（参考user权限说明）
        Select,Insert,Update,Delete,Create,Drop,Grant,References,Index,Alter,Create View,Show view,Trigger
    Column_priv：字段表示对表中的列的操作权限；权限如下（参考user权限说明）
        Select,Insert,Update,References
#### 其它列
    Timestamp：  表示修改该记录的用户。
    Grantor：    表示修改该记录的时间

补充说明：
    ①：tables_priv表中的权限是表级的，所以要想设置到tables_priv表上权限需要表权限，(主要 数据库名称.数据库表名称)
            如：GRANT SELECT,DELETE ON demo_school.student TO 'tom'@'%';
　　　　　　-- 这时候我们就可以查看tables_priv表中多出来一条user为tom的记录，并且只有SELECT,DELETE权限
```

### 4：columns_priv表

　　columns_priv表用来对表的某一列设置权限；通过这样可以对权限更细粒度处理 

```sql
我们可以通过SQL语句查看表结构: DESC mysql.columns_priv;
#### 范围列
    Host：          主机名
    Db：            数据库名
    User：          用户名
    Table_name：    表名
    Column_name：   字段名
    说明：columns_priv权限表记录了host、db、user、table_name、column_name五个字段正好构建一个联合主键
#### 权限列
    Column_priv：字段表示对表中的列的操作权限；权限如下（参考user权限说明）
        Select,Insert,Update,References
#### 其它列
    Timestamp：  表示修改该记录的用户
补充说明：
    ①：columns_priv表中的权限是列级别的，所以要想设置到columns_priv表上权限需要列权限
        -- 设置列权限和其它几种不一样，具体如下：
        -- 列权限适用于给定表中的单个列。要在列级别授予的每个权限后必须跟着列或列括在括号内
        如：GRANT SELECT(sname,saddress),UPDATE(saddress) ON demo_school.student TO 'tom'@'%';
            -- 这时我们就设置了列权限，但是一般开发中最多涉及到表权限即可
        登录tom账号后可以查看到demo_school.student表，但是使用DESC student后却发现只有两个字段了
        DESC demo_school.student;
        +----------+-------------+------+-----+---------+-------+
        | Field    | Type        | Null | Key | Default | Extra |
        +----------+-------------+------+-----+---------+-------+
        | sname    | varchar(5)  | NO   |     | NULL    |       |
        | saddress | varchar(10) | YES  |     | NULL    |       |
        +----------+-------------+------+-----+---------+-------+
        -- 这就说明：既然开启列权限，那么没在授权中指定的字段全部代表未授权不可见；针对授权的字段得看具体授权了什么权限
        -- 所以tom用户只能执行查看语句：
            SELECT sname,saddress FROM demo_school.student;
        -- 所以tom用户只能执行更新类似语句：
            UPDATE demo_school.student set saddress = '安徽滁州' WHERE sname = '王生安';
        -- 查询tom权限
            SHOW GRANTS FOR 'tom'@'%';
            +----------------------------------------------------------------------------------------------+
            |Grants for tom@%                                                                              |
            +----------------------------------------------------------------------------------------------+
            |GRANT USAGE ON *.* TO `tom`@`%`                                                               |
            |GRANT SELECT (`saddress`, `sname`),UPDATE (`saddress`) ON `demo_school`.`student` TO `tom`@`%`|
            +----------------------------------------------------------------------------------------------+
        -- 清空tom权限
            REVOKE SELECT (`saddress`, `sname`),UPDATE (`saddress`) ON `demo_school`.`student` FROM 'tom'@'%';
```



## 四：角色管理（MySQL8.0）

　　MySQL数据库中通常都会出现多个拥有相同权限集合的用户，在之前版本中只有分别向多个用户授予和撤销权限才能实现单独更改每个用户的权限。在用户数量比较多的时候，这样的操作是非常耗时的。而MySQL8.0为了用户权限管理更容易，提供了一个角色管理的新功能。角色是指定的权限集合，和用户帐户一样可以对角色进行权限的授予和撤消。如果用户被授予角色权限，则该用户拥有该角色的权限。
　　**注：MySQL5.7版本如果想使用角色，可以通过mysql.proxies_priv来模拟角色(Role)的功能，这里不在介绍。**



### 1：角色基本管理

```sql
开发中实际四个场景：
    ①app权限：应用程序需要读、写权限
    ②ops权限：运维人员需要完全访问数据库权限
    ③dev_read权限：部分开发人员需要读取权限
    ④dev_write：部分开发人员需要读写权限

### 创建角色基本语法：
   CREATE ROLE '角色名称'[@'角色主机'] [,'角色名称'[@'角色主机']]
    注：角色名称的命名规则和用户名类似。如果'角色主机'省略，默认为%，'角色名称'不可省略或不可为空
    创建实际开发场景的四个角色，建议将角色名称命名得比较直观：
        CREATE ROLE 'app'@'%', 'ops'@'%', 'dev_read'@'%', 'dev_write'@'%';
        注：角色名称格式类似于由用户和主机部分组成的用户帐户，如：role_name@host_name。
            如果省略主机部分，则默认为 “%”，表示任何主机。
    我们创建好的角色全部存放在user表中，虽然存放在user，但是角色没有密码，也无法像用户一样登录，
    查询角色刚刚创建的角色：
        SELECT host,user FROM mysql.user;
            +-----------+------------------+
            | host      | user             |
            +-----------+------------------+
            | %         | app              |
            | %         | dev_read         |
            | %         | dev_write        |
            | %         | ops              |
            | %         | root             |
            | localhost | mysql.infoschema |
            | localhost | mysql.session    |
            | localhost | mysql.sys        |
            +-----------+------------------+
### 给角色赋予权限
    授权使用的是 GRANTE 关键词，其实和我们上面用户授权一样：
        GRANT 权限1 [, 权限n] ON 数据库名称.表名称 TO '角色名'@'主机名';
    为上面四个角色赋予对应权限：
        GRANT SELECT,INSERT,UPDATE,DELETE ON demo_school.* TO 'app'@'%';
        GRANT ALL PRIVILEGES ON demo_school.* TO 'ops'@'%';
        GRANT SELECT ON demo_school.* TO 'dev_read'@'%';
        GRANT INSERT,UPDATE,DELETE ON demo_school.* TO 'dev_write'@'%';
        注：这里我就以demo_school数据库来说明

### 查询角色权限
    赋予角色权限之后，我们可以通过 SHOW GRANTS 语句，来查看权限是否创建成功了（具体参考上面的查询用户权限信息）：
        SHOW GRANTS FOR '角色名'@'主机名';
    查看上面角色授权权限信息：
        SHOW GRANTS FOR 'app'@'%';
            +----------------------------------------------------------------------+
            | Grants for app@%                                                     |
            +----------------------------------------------------------------------+
            | GRANT USAGE ON *.* TO `app`@`%`                                      |
            | GRANT SELECT, INSERT, UPDATE, DELETE ON `demo_school`.* TO `app`@`%` |
            +----------------------------------------------------------------------+
        SHOW GRANTS FOR 'ops'@'%';
        SHOW GRANTS FOR 'dev_write'@'%';
            +------------------------------------------------------+
            | Grants for ops@%                                     |
            +------------------------------------------------------+
            | GRANT USAGE ON *.* TO `ops`@`%`                      |
            | GRANT ALL PRIVILEGES ON `demo_school`.* TO `ops`@`%` |
            +------------------------------------------------------+

### 回收角色权限
    角色授权后，可以对角色的权限进行维护，对角色内的权限进行添加或撤销。添加权限使用GRANT语句，与用户授权相同。
    撤销角色或角色权限使用REVOKE语句。修改了角色的权限，会影响拥有该角色的账户的权限。
    撤销角色权限的SQL语法如下：
        REVOKE 权限1 [, 权限n] ON 数据库名称.表名称 FROM '角色名'@'主机名';
    撤销上面四个角色的权限：
        REVOKE SELECT, INSERT, UPDATE, DELETE ON `demo_school`.* FROM 'app'@'%';
        REVOKE ALL PRIVILEGES ON `demo_school`.* FROM 'ops'@'%';
        REVOKE SELECT ON `demo_school`.* FROM 'dev_read'@'%';
        REVOKE INSERT, UPDATE, DELETE ON `demo_school`.* FROM 'dev_write'@'%';

### 删除角色
    当我们需要对业务重新整合的时候，可能就需要对之前创建的角色进行清理，删除一些不会再使用的角色
    基本语法：
        DROP ROLE role1 [,role2]...
        注：如果删除了角色，那么用户也就失去了通过这个角色所获得的所有权限
    删除上面四个角色：
        DROP ROLE 'app'@'%', 'ops'@'%', 'dev_read'@'%', 'dev_write'@'%';
```



### 2：用户赋予角色

　　我们创建完角色后会根据实际情况，将指定用户加入到对应的角色。

```sql
### 创建用户(后面授权角色)
    假设现在需要一个应用程序使用的帐户、一个运维人员帐户、一个是开发人员只读帐户和一个开发人员读写帐户
        -- 应用程序帐户（待分配app权限）
            CREATE USER 'app01'@'%' IDENTIFIED BY '1234';
        -- 运维人员帐户（待分配ops权限）
            CREATE USER 'ops01'@'%' IDENTIFIED BY '1234';
        -- 开发人员只读帐户（待分配dev_read权限）
            CREATE USER 'dev01'@'%' IDENTIFIED BY '1234';
        -- 开发读写帐户（待分配dev_write权限）
            CREATE USER 'dev02'@'%' IDENTIFIED BY '1234';

### 给用户赋予角色
    角色创建并授权后，要赋给用户并处于 激活状态 才能发挥作用。给用户添加角色可使用GRANT语句，语法形式如下：
        GRANT '角色名1'@'主机' [,'角色名2'@'主机',...] TO '用户名1'@'主机' [,'用户名2'@'主机',...];
    为用户赋予角色：
        GRANT 'app'@'%' TO 'app01'@'%';
        GRANT 'ops'@'%' TO 'ops01'@'%';
        GRANT 'dev_read'@'%' TO 'dev01'@'%';
        GRANT 'dev_write'@'%' TO 'dev02'@'%';
        -- 这时候这些用户都会存在这些角色信息了，但是得注意的是默认用户是未激活这个角色权限的

### 激活角色
    我们登录其中一个账号后查看自己的权限信息
    -- 查看当前登录的账号
        SELECT USER();
        +----------------------+
        | USER()               |
        +----------------------+
        | ops01@125.119.190.81 |
        +----------------------+
    -- 查询当前账户的角色信息
        SELECT CURRENT_ROLE();
        +----------------+
        | CURRENT_ROLE() |
        +----------------+
        | NONE           |
        +----------------+
        -- 此时发现我们之前设置的角色并未生效
    -- 查看权限是否存在（之前角色设置的demo_school数据库）
        SHOW DATABASES;
        +--------------------+
        | Database           |
        +--------------------+
        | information_schema |
        | performance_schema |
        +--------------------+
    此时我们发现虽然设置了角色，但是未生效，其实我们设置完角色后需要激活权限，
    ①：使用SET DEFAULT ROLE语句来指定激活当前账户的角色：
        SET DEFAULT ROLE ALL TO 'ops01'@'%';
        -- 激活完后退出账户在登录即可
        SELECT CURRENT_ROLE();
        +----------------+
        | CURRENT_ROLE() |
        +----------------+
        | `ops`@`%`      |
        +----------------+
    ②：使用将activate_all_roles_on_login配置（ON开启自动激活，OFF关闭自动激活）
        服务器会在登录时激活帐户的所有角色。这优先于使用 SET default ROLE 指定的默认角色。
        对于在定义器上下文中执行的存储程序和视图，也只在开始执行时应用。
        默认情况：
            SHOW VARIABLES LIKE 'activate_all_roles_on_login';
            +-----------------------------+-------+
            | Variable_name               | Value |
            +-----------------------------+-------+
            | activate_all_roles_on_login | OFF   |
            +-----------------------------+-------+
        使用SQL语句修改配置：
            SET GLOBAL activate_all_roles_on_login=ON;  -- MySQL服务重启后就失效
            SET PERSIST activate_all_roles_on_login=ON;  -- MySQL服务重启后不失效
        修改配置文件方式(vim /etc/my.cnf)：
            [mysqld]
            activate_all_roles_on_login=ON

### 撤销角色用户
    语法：REVOKE '角色名'@'主机' FROM '用户名'@'主机';
    撤销之前设置的四个账户的角色：
        REVOKE 'app'@'%' FROM 'app01'@'%';
        REVOKE 'ops'@'%' FROM 'ops01'@'%';
        REVOKE 'dev_read'@'%' FROM 'dev01'@'%';
        REVOKE 'dev_write'@'%' FROM 'dev02'@'%';

### 设置强制角色
    强制角色是允许定义用户登录时强制权的角色
    ①：使用SQL方式指定强制角色：
        SET PERSIST mandatory_roles = '角色名1@主机,角色名2@主机...'; -- MySQL服务重启后不失效
        SET GLOBAL mandatory_roles = '角色名1@主机,角色名2@主机...';  -- MySQL服务重启后就失效
    ②：使用配置文件方式(vim /etc/my.cnf)：
        [mysqld]
        mandatory_roles='角色名1@主机,角色名2@主机...'
```

