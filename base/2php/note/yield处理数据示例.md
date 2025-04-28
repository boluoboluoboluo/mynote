##### yield处理数据

说明：数据库 查询导出数据，数据量大时会出现内存溢出问题，使用yield解决

```php
//原sql查询代码
function fetchAll($sql){
    //$this->link 保存的是数据库的连接句柄
    $result=mysqli_query($this->link,$sql);
    $rows = array();
    while($row = mysqli_fetch_array($result,MYSQLI_ASSOC)){
        $rows[]=$row;
    }
    return $rows;
}

//yield代码
function fetchAll($sql){
    //$this->link 保存的是数据库的连接句柄
    $result=mysqli_query($this->link,$sql);
    $num = 0;//用作key
    while($row = mysqli_fetch_array($result,MYSQLI_ASSOC)){
        // =>是关联符，返回键值对
        yield $num => $row;//这里是关键
        $num ++;
    }
}
```

结果集处理：

```php
$result = fetchAll();	//

var_dump($result->valid());//检验是否有效，（true）

if($result->current()){
    //遍历...
}else{
    echo "no data..";
}

```

##### tp5+pdo+yield示例

```php
use PDO;

public function test(){
    $re = $this->test2();	//返回生成器
    foreach($re as $k=>$v){
        //遍历
    }
}

public function test2(){
    $where = array();
    $pdo = Db::name('firm_order')
				->where($where)
				->getPdo();

	$num=0;
    while($row = $pdo->fetch(PDO::FETCH_ASSOC)){
        // =>是关联符，返回键值对
        yield $num => $row;//这里是关键
        $num ++;
    }
}
```

