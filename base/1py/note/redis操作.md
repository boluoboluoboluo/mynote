#### redis

##### 安装

```sh
# linux:

# 安装 Redis 服务器
sudo apt install redis-server -y
# 启动并设置开机自启
sudo systemctl start redis-server
sudo systemctl enable redis-server

# 端口
默认端口: 6379	# 可通过配置文件修改

# 配置文件:
/etc/redis/redis.conf 或 /etc/redis.conf

# 设置密码: (可选)
配置文件redis.conf,找到 :
	-- '# requirepass foobared'
	-- '去掉开头的 #，将 foobared 改为你的密码'
	-- '如 requirepass my_secret_password'
```

```sh
# 验证连通性
redis-cli ping	#返回 pong 则成功

# 查看内存 (进入redis-cli)
info memory	
	-- used_memory_human: Redis 此时实际数据占用的内存大小（如 1.5M）
	-- used_memory_rss_human: 操作系统分配给 Redis 的总物理内存
	-- maxmemory_human: 允许使用的最大内存。若显示 0B，代表不限制内存

```

##### 操作示例

```sh
# 操作示例:

# 终端进入 redis-cli 命令:
redis-cli

# 查看key总数
info keyspace

# 查看key的数据类型
type 键名

# 查看所有key:
keys *			# 谨慎使用!
# 查看(范围)
scan 0 count 10	# 示例:从游标0,查看10个key
	#返回:
	-- 第1个数字为下1个key的游标
	-- 第2个为key列表
# 查看(范围匹配)
scan 0 match user:* count 10	#示例: 查看匹配'user'的key

# 删除:
redis-cli --scan --pattern "user:*" | xargs redis-cli unlink	# linux 终端操作,不用进入redis-cli 

# 清空当前数据库 {Redis 默认有 16 个数据库（db0 ~ db15）}
flushdb
# 清空所有数据库
flushall
---------------------
# string: 适合存单值
set user:1 "Tom"
get user:1
del user:1
---------------------
# hash: 适合存对象
hset userInfo:101 name "Alice" age 25 city "Beijing"
# 查看单个属性
hget userInfo:101 name
# 查看该对象的所有属性和值
hgetall userInfo:101
# 只删除对象里的某个属性（比如删掉年龄）
hdel userInfo:101 age
# 彻底删除整个对象
del userInfo:101
---------------------
# list: 队列和栈 (有序、可重复的元素列表。适合做消息队列、最新文章列表)
rpush mylist "task1"		# r 表示右侧, 左侧用 lpush
rpush mylist "task2" "task3"
# 改
lset mylist 0 "new_task1"	# 修改指定下标的元素（索引从 0 开始）
# 查
lrange mylist 0 -1 	# 查看指定范围的元素（0 -1 代表查看全部）
# 删
lpop mylist		# 从左侧弹出一个元素（弹出意味着从列表移除并返回该值）。
---------------------
# set: 自动去重 (序、不可重复的元素集合)
# 增
sadd tags "Java" "Python" "Java"
# 改
Set 是无序的，通常不直接“修改”某个元素，而是先删掉旧的，再加入新的。
# 查
smembers tags	# 查看集合内所有元素
sismember tags "Java"	# 判断某个元素在不在集合里（在返回 1，不在返回 0）
# 删
srem tags "Python"

```

#### valkey

```sh
# 说明: redis 平替,且开源免费

# 安装:
sudo apt update
sudo apt install -y valkey

# 启动及自启动
sudo systemctl start valkey-server
sudo systemctl enable valkey-server

# 配置文件: 
valkey.conf

# 命令: 完全redis-cli
valkey-cli
> ping
> set key value
> get key

```



#### python使用

```sh
# redis 和 valkey ,python代码无需更改,完全兼容
```

```sh
# 安装依赖:
pip install redis
```

##### 示例

```py
# python代码
import redis

# 建立连接 (decode_responses=True 表示自动将二进制转字符串)
client = redis.Redis(host='localhost', port=6379, decode_responses=True)
# 测试连线 ,成功返回True
print(f"連線測試: {client.ping()}")

#==========================
# 字符串操作 (String)
# 增/改
client.set("user:name", "张三", ex=3600)
# 查
name = client.get("user:name")  # 返回 "张三"
# 删
client.delete("user:name")
#==========================
# hash操作
# 增/改
client.hset("user:101", mapping={"name": "李四", "age": "25"})
# 查
age = client.hget("user:101", "age")  # 返回 "25"
user_dict = client.hgetall("user:101")  # 返回 {"name": "李四", "age": "25"}
# 删单个字段
client.hdel("user:101", "age")
#==========================
# 列表操作
# 增
client.rpush("tasks", "task1", "task2", "task3")	# key 为 'tasks'
# 改 (将索引 0 的位置改为新任务)
client.lset("tasks", 0, "task_updated")
# 查 (获取前两个元素)
active_tasks = client.lrange("tasks", 0, 1)  # 返回 ['task_updated', 'task2']
# 删 (弹出最右侧元素)
client.rpop("tasks")
#==========================
# 集合操作
client.zadd('leaderboard', {'PlayerA': 100, 'PlayerB': 250, 'PlayerC': 180})
# 由低到高排序輸出
rank = client.zrange('leaderboard', 0, -1, withscores=True)

# 关闭连接
client.close()
```

##### 连接池

```py
import redis

# 1. 创建连接池（只需创建一次，用于复用连接，提高性能）
pool = redis.ConnectionPool(
    host='127.0.0.1', # Redis 服务器 IP（本地为 127.0.0.1）
    port=6379,        # Redis 端口
    password=None,    # 如果设置了密码，写在这里，例如 'your_password'
    db=0,             # 默认选择 db0
    decode_responses=True # 【重要】自动将返回的字节（bytes）解码为 Python 字符串
)

# 2. 使用 context 模块（with 语句）自动管理连接与关闭
with redis.Redis(connection_pool=pool) as r:
    
    print("=== 1. String（字符串）操作 ===")
    r.set('user:1', 'aaa', ex=60) # 存数据，设置 60 秒过期
    r.set('user:2', 'bbb')
    
    val1 = r.get('user:1')
    print(f"获取 user:1 的值: {val1}")
    
    # 3. 应对你刚才提的需求：批量获取 MGET
    all_vals = r.mget(['user:1', 'user:2'])
    print(f"批量获取多个值: {all_vals}") # 输出: ['aaa', 'bbb']


    print("\n=== 2. Hash（哈希）操作 ===")
    r.hset('all_users', mapping={'1': 'aaa', '2': 'bbb', '3': 'ccc'})
    
    # 获取特定字段
    print(f"获取哈希中 1 的值: {r.hget('all_users', '1')}")
    # 获取整张哈希表
    print(f"获取哈希表全部数据: {r.hgetall('all_users')}")

    print("\n=== 3. 批量删除操作 ===")
    # 对应前文提到的：在 Python 中优雅地批量查找并删除
    # 使用 scan_iter 迭代器，安全、不阻塞
    keys_to_delete = []
    for key in r.scan_iter(match="user:*"):
        keys_to_delete.append(key)
        
    if keys_to_delete:
        print(f"找到需要删除的 Key: {keys_to_delete}")
        r.delete(*keys_to_delete) # 使用解包语法批量删除
    else:
        print("未找到匹配的 Key")

# 当程序离开 with 代码块时，Python 会自动将该连接归还给连接池，无需手动执行 close()
print("\nRedis 连接已安全关闭/回收。")

```

