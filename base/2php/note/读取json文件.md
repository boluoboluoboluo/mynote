#### 读取json文件

```php
public function test_get_json(){
	$path = __DIR__."/d.json";
	$json_str = file_get_contents($path); 
	$data = json_decode($json_str,true);
	var_dump($data);
}
```

