### common

示例：

```php
<?php

$a = 1;		//全局变量
static $aa = "aa";

function test(){
	global $a;		//申明全局变量
	global $aa;
	echo "\n方法里访问全局变量a：".$a;
	echo "\n方法里访问全局静态变量aa：".$aa;
}

class O extends X{
	public $b = 2;
	static $bb = "33";

	function func(){
		global $a;	//申明全局变量
		echo "\n类的方法里访问全局变量a：".$a;

		echo "\n类的方法里访问类的属性b：".$this->b;
		echo "\n类的方法里访问类的静态属性bb:".self::$bb;
	}
}

test();
$o = new O();
echo "\n访问类的属性b：".$o->b;
echo "\n访问类的静态属性bb:".O::$bb;
echo $o->func();

```



```php
<?php

	funciton start_ex(){
		//段注释:/* */
	
		//查看版本：phpinfo();
	
		//命名空间:namespace
		//引入类：use xx\A	//引入命名空间xx下的class A
	}
	
	function common_ex(){
		$i = 3;
		$f = 3.0;
		$s = "abc";
		$arr = [1,2,3];
		$arr2 = array(1,2,3);
	
		// #打印(整型，浮点，字符串，json，数组，集合等)
		echo $str;
		var_dump($str);
		print_r($str);
	
		// #变量类型
	
		// #if语句
	
		// #switch语句
        switch($i){
            case 1:
                $s = "1";
                break;
			case 2:
               	$s = "2";
            default:
                $s = "3";
        }
	
		// #while语句
	
		// #循环 start
		// #循环 end
	
		// #随机数
	
		// #暂停3秒
	
		// #输入函数，回车结束
	
		// #退出，默认0正常
	
		// #调用全局表量
	
		// #调用其他方法
	
		// #new对象
		$classname = "testModel";		//命名空间下的类名
		$c = new classname;
	
		// #调用对象方法，属性
	
	}



	//include和reuqire说明
	function include_require(){
		//require和include几乎完全一样，除了处理失败的方式不同之外，require在出错时产生 E_COMPILE_ERROR 级别的错误。
		//换句话说将导致脚本中止而 include 只产生警告（E_WARNING），脚本会继续运行。
		//require_once 语句和 require 语句完全相同，唯一区别是 PHP 会检查该文件是否已经被包含过，如果是则不会再次包含。
		//include_once 语句在脚本执行期间包含并运行指定文件。此行为和 include 语句类似，唯一区别是如果该文件中已经被包含过，则不会再次包含。如同此语句名字暗示的那样，只会包含一次。
	}
	//中文乱码问题
	function zh_ex(){
		//解决中文乱码问题
		$str2 = iconv('gbk','utf-8',$str);
	}
	//判断是否微信浏览器
	function yf_isweixin(){
		if(strpos($_SERVER['HTTP_USER_AGENT'],'MicroMessenger') !== false){
			return 1;
		}else{
			return 0;
		}
	}
	//引号3层嵌套问题，
	function quote_ex(){
		$path = "./";
		echo "<label style='color:blue;background:#bbbbbb;' onclick='submit_info(\"".$path."\");'>";	//解决方案
	}
	//获取32位随机数
	public function get_32rand(){
		$chars = 'abcdefghijklmnopqrstuvwxyz0123456789'; 
		$length = 32;
		$token = "";
		for($i = 0; $i < $length; $i++) { 
			$token .= $chars[ mt_rand(0, strlen($chars) - 1) ]; 
		} 
		return $token;
	}
	//extract函数
	function meth_ex(){
		//extract函数
		$re = extract($_POST);	//将对象分解，键值对中的键变成变量，值变成变量值
	}
```

#### 常量

```php
define("AGE",12);
```

#### 魔术常量

```php
$s = __LINE__;	//文件的当前行号
$s = __FILE__;	//文件的完整路径和文件名。如果用在被包含文件中，则返回被包含的文件名。
$s = __DIR__;	//文件所在的目录。如果用在被包括文件中，则返回被包括的文件所在的目录。
   				// 它等价于 dirname(__FILE__)。除非是根目录，否则目录中名不包括末尾的斜杠。（PHP 5.3.0中新增）
$s = __FUNCTION__;	//返回该函数被定义时的名字（区分大小写）
$s = __CLASS__;	//返回该类被定义时的名字（区分大小写）。
$s = __METHOD__;	//返回该方法被定义时的名字（区分大小写）。
$s = __NAMESPACE__;	//当前命名空间的名称（区分大小写）
    
```



#### 变量

##### 超级全局变量

```
$GLOBALS
$_SERVER
$_REQUEST
$_POST
$_GET
$_FILES
$_ENV
$_COOKIE
$_SESSION
```

| 元素/代码                       | 描述                                                         |
| :------------------------------ | :----------------------------------------------------------- |
| $_SERVER['PHP_SELF']            | 当前执行脚本的文件名，与 document root 有关。例如，在地址为 http://example.com/test.php/foo.bar 的脚本中使用 $_SERVER['PHP_SELF'] 将得到 /test.php/foo.bar。__FILE__ 常量包含当前(例如包含)文件的完整路径和文件名。 从 PHP 4.3.0 版本开始，如果 PHP 以命令行模式运行，这个变量将包含脚本名。之前的版本该变量不可用。 |
| $_SERVER['GATEWAY_INTERFACE']   | 服务器使用的 CGI 规范的版本；例如，"CGI/1.1"。               |
| $_SERVER['SERVER_ADDR']         | 当前运行脚本所在的服务器的 IP 地址。                         |
| $_SERVER['SERVER_NAME']         | 当前运行脚本所在的服务器的主机名。如果脚本运行于虚拟主机中，该名称是由那个虚拟主机所设置的值决定。(如: www.w3cschool.cn) |
| $_SERVER['SERVER_SOFTWARE']     | 服务器标识字符串，在响应请求时的头信息中给出。 (如：Apache/2.2.24) |
| $_SERVER['SERVER_PROTOCOL']     | 请求页面时通信协议的名称和版本。例如，"HTTP/1.0"。           |
| $_SERVER['REQUEST_METHOD']      | 访问页面使用的请求方法；例如，"GET", "HEAD"，"POST"，"PUT"。 |
| $_SERVER['REQUEST_TIME']        | 请求开始时的时间戳。从 PHP 5.1.0 起可用。 (如：1377687496)   |
| $_SERVER['QUERY_STRING']        | query string（查询字符串），如果有的话，通过它进行页面访问。 |
| $_SERVER['HTTP_ACCEPT']         | 当前请求头中 Accept: 项的内容，如果存在的话。                |
| $_SERVER['HTTP_ACCEPT_CHARSET'] | 当前请求头中 Accept-Charset: 项的内容，如果存在的话。例如："iso-8859-1,*,utf-8"。 |
| $_SERVER['HTTP_HOST']           | 当前请求头中 Host: 项的内容，如果存在的话。                  |
| $_SERVER['HTTP_REFERER']        | 引导用户代理到当前页的前一页的地址（如果存在）。由 user agent 设置决定。并不是所有的用户代理都会设置该项，有的还提供了修改 HTTP_REFERER 的功能。简言之，该值并不可信。) |
| $_SERVER['HTTPS']               | 如果脚本是通过 HTTPS 协议被访问，则被设为一个非空的值。      |
| $_SERVER['REMOTE_ADDR']         | 浏览当前页面的用户的 IP 地址。                               |
| $_SERVER['REMOTE_HOST']         | 浏览当前页面的用户的主机名。DNS 反向解析不依赖于用户的 REMOTE_ADDR。 |
| $_SERVER['REMOTE_PORT']         | 用户机器上连接到 Web 服务器所使用的端口号。                  |
| $_SERVER['SCRIPT_FILENAME']     | 当前执行脚本的绝对路径。                                     |
| $_SERVER['SERVER_ADMIN']        | 该值指明了 Apache 服务器配置文件中的 SERVER_ADMIN 参数。如果脚本运行在一个虚拟主机上，则该值是那个虚拟主机的值。(如：someone@w3cschool.cn) |
| $_SERVER['SERVER_PORT']         | Web 服务器使用的端口。默认值为 "80"。如果使用 SSL 安全连接，则这个值为用户设置的 HTTP 端口。 |
| $_SERVER['SERVER_SIGNATURE']    | 包含了服务器版本和虚拟主机名的字符串。                       |
| $_SERVER['PATH_TRANSLATED']     | 当前脚本所在文件系统（非文档根目录）的基本路径。这是在服务器进行虚拟到真实路径的映像后的结果。 |
| $_SERVER['SCRIPT_NAME']         | 包含当前脚本的路径。这在页面需要指向自己时非常有用。__FILE__ 常量包含当前脚本(例如包含文件)的完整路径和文件名。 |
| $_SERVER['SCRIPT_URI']          | URI 用来指定要访问的页面。例如 "/index.html"。               |

#### class

```php
<?php

// 声明一个'iTemplate'接口
interface iTemplate
{
    public function setVariable($name, $var);
    public function getHtml($template);
}
class Template implements iTemplate
{
  //必须实现接口方法
}

//抽象类
abstract class AbstractClass
{
 // 强制要求子类定义这些方法
    abstract protected function getValue();
    abstract protected function prefixValue($prefix);

    // 普通方法（非抽象方法）
    public function printOut() {
        print $this->getValue() . PHP_EOL;
    }
}

//类
class O extends X{
    private $c;
    protected $d;
    
    const constant = '常量值';

    function showConstant() {
        echo  self::constant . PHP_EOL;
    }
    
    function __construct( $par1, $par2 ) {
       $this->url = $par1;
       $this->title = $par2;
	}
	function __destruct(){
       print "销毁 " . $this->name . "\n";
  	}
}   
	
```

##### stdClass

```php
//是 PHP 中的一个默认类，用于创建空的对象
//当你从数据库查询数据或者解析 JSON 字符串时，如果数据不能归于任何预定义的类，它会被解析为 stdClass 对象的实例。

$obj = new stdClass();
$obj->name = "John";
$obj->age = 25;
 
echo $obj->name; // 输出 John
echo $obj->age; // 输出 25
```

### numeric

```php
<?php
	
	function numerice_ex(){
		$i = 3;
	
		// #是否为数字，整数，浮点数
    	$flag = is_numeric($i);	//判断是否为数字
		$f = is_int($i);
    	$f = is_float($i);
    
		// #浮点数保留几位
    	$f = 0.223;
    	$f2 = number_format($f,2);	//0.22
	
		// #取整，四舍五入，向上取整，向下取整
    	$f = 0.3;
		$re = intval($f);	//取整
		$re = round($f,2);	//保留2位，四舍五入
		$re = ceil($f);		//向上取整
		$re = floor($f);	//向下取整
	
		// #数字类型转换（整数，浮点数，字符串）
		floatval($i);
    	strval($i);
    	intval($i)
	
		// #进制转换：2，8，10，16
        //方法原型：string base_convert(string $number, int $frombase, int $tobase)
        //$number：要转换的数。
		//$frombase：原数的进制。
        //$tobase：目标进制。
        // 将十进制数100转换为二进制
        $decimal = 100;
		$binary = base_convert($decimal, 10, 2);
    	// 将二进制数1100100转换为十六进制
		$hexadecimal = base_convert($binary, 2, 16);
        
		// #加减乘除，科学计算
		//$a+$b $a-$b $a*$b $a/$b $a%$b
    	bcadd($a,$b,1);
    	bcsub($a,$b,1);
    	bcmul($a,$b,1);
    	bcdiv($a,$b,1);
	
	}
```

### string

```php
<?php
	// #字符串方法
	function str_ex(){
		// s := "123"
	
		// #字符串太长续行
	
		// #字符串连接
	
		// #空和none
	
		// #字符串长度
	
		// #去除两端空格，去左lstrip，去右rstrip
	
		// #字符串转int，float（互转）
		intval(s);
        floatval(s)
		// #下标截取子串
	
		// #字串是否存在
    	if(strpos($str, $subStr) !== false){
            
        }
	
		// #字符串转数组
	
		// #根据字符分割成数组
    	$arr2 = explode("-",$str);	//-为分隔符,string转数组
	
		// #字符串转json
	
		// #大小写转换
    	$u = strtoupper($s);
    	$l = strtolower($s);
    	$x = ucwords($s);	//首字母大写
	
		// #获取编码类型
	
		// #编码
	
		// #解码
	
		// #编码转换（中文乱码）
	
		// #字符串编码解码
	}

	function common(){
		$str = "abcdef";
		//常见字符串操作
		//长度，字符索引，子串，去空格，preg_replace strtolower sizeof
		
		//长度
		$len = strlen($str);
		//索引
		$index = strpos($str,"b");		//子串第一次出现的位置
		//子字符串
		$sub_str = substr($str,2);		//索引位置后的子串
		$sub_str2 = substr($str,2,1);	//索引位置2，长度1
        $sub_str2 = substr($str,-1,1);	//倒数第一位
		//todo..
	
		$arr = ["a","b","c"];
		//数组转string
		$str = implode("-",$arr);	// -为分隔符
		//string转数组
		$arr2 = explode("-",$str);	//-为分隔符
	}
	
	//关于json
	function json_ex(){
		//json
		$arr = ["aabb","ccdd"];
		//数组转json
		$json_str = json_encode($arr);
		$json_str2 = json_encode($arr,JSON_UNESCAPED_UNICODE);	//设置不要编码unicode，可用于解决中文乱码问题
		//json转数组
		$re = json_decode($json_str,true);
	
		//json_encode 会自动转义字符串中的斜杠，需注意！
		$arr2 = ["aa/bb","ccdd"];
		$str2 = json_encode($arr2);		//输出 ["aa\/bb","ccdd"]
		$arr3 = ["aa\bb","ccdd"];
		$str3 = json_encode($arr3);		//输出 ["aa\\bb","ccdd"]
	
	}


```

##### 字符串和16进制互转

```php
function str_hex(){
    $str = "sdfsdfwe";
    $re = bintohex($str);
    return $re;
}
function hex_str(){
    $hex = "3d4e5a";
    $re = hex2bin($hex);
    return $re;
}
```

##### 判断身份证

```php
function check_idcard($input){
	$id = strtoupper($input);
    $regx = "/(^\d{15}$)|(^\d{17}([0-9]|X)$)/";
    $arr_split = array();
    if(!preg_match($regx, $id)){
        return false;
    }
    if(15==strlen($id)){ //检查15位
        $regx = "/^(\d{6})+(\d{2})+(\d{2})+(\d{2})+(\d{3})$/";

        @preg_match($regx, $id, $arr_split);
        //检查生日日期是否正确
        $dtm_birth = "19".$arr_split[2] . '/' . $arr_split[3]. '/' .$arr_split[4];
        if(!strtotime($dtm_birth)){
            return false;
        } 
    }else{//检查18位
        $regx = "/^(\d{6})+(\d{4})+(\d{2})+(\d{2})+(\d{3})([0-9]|X)$/";
        @preg_match($regx, $id, $arr_split);
        $dtm_birth = $arr_split[2] . '/' . $arr_split[3]. '/' .$arr_split[4];
        if(!strtotime($dtm_birth)){  //检查生日日期是否正确
            return false;
        }else{
            //检验18位身份证的校验码是否正确。
            //校验位按照ISO 7064:1983.MOD 11-2的规定生成，X可以认为是数字10。
            $arr_int = array(7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2);
            $arr_ch = array('1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2');
            $sign = 0;
            for ( $i = 0; $i < 17; $i++ ){
                $b = (int) $id{$i};
                $w = $arr_int[$i];
                $sign += $b * $w;
            }
            $n  = $sign % 11;
            $val_num = $arr_ch[$n];
            if ($val_num != substr($id,17, 1)){
                return false;
            }
        }
    }
	return true;
}
//根据身份证获取出生日期
function get_birth($idcard){
    $birth = strlen($idcard)==15 ? ('19'.substr($idcard,6,6)) : substr($idcard,6,8);
    $birth = substr($birth,0,4)."-".substr($birth,4,2)."-".substr($birth,6,2);	//yyyy-MM-dd
    return $birth;
}
//根据身份证获取性别
function get_sex($idcard){
    $sex = substr($idcard,(strlen($idcard)==15 ? -2 : -1),1) % 2 ? '1' : '0';	//0男，1女
    return $sex;
}
```

##### 手机号判断

```php
//手机号判断
function phone_ex(){
    $pre = "/^1[3|4|5|7|8]\d{9}$/";
    if(!preg_match($pre, $phone)) {
        return false;
    }
    return true;
}
```

##### 正则

```php
//正则
function re_ex(){
    $org_name = "[北京大学深圳医院]";
    //正则
    $tmp_reg = "/北京大学深圳医院/";
    if(preg_match($tmp_reg,$org_name)){		//如果是北大
        echo "yes";
    }
}
```

##### htmlspecialchars

```php
#一般可用于xss
#函数: htmlspecialchars(string,quotestyle,character-set)
#作用: 将特殊字元转换成html实体.
#备注: 转换的特殊字元包括(只有这5个):

　　& (和) 转成 &amp; 
　　" (双引号) 转成 &quot; 
　　< (小于) 转成 &lt;
　　> (大于) 转成 &gt; 
　　'' (单引号) 转成 &#039;
　　
```

##### addslashes

```php
#一般可用于防止sql注入
#函数：addslashes(string) 
#作用：返回在预定义字符之前添加反斜杠的字符串。

#预定义字符是：

    单引号（'）
    双引号（"）
    反斜杠（\）
    NULL
```

### array

```php
<?php

	function arr_ex(){
	
		$arr = ["a","b","c"];
	
		// #数组长度
		count($arr);
	
		// #数组是否为空
		empty();
	
		// #数组添加元素，删除元素，插入元素
		array_push($arr,$i);
	
		// #数组是否包含某元素
		in_array($i,$arr);
	
		// #数组合并
		array_merge();
	
		// #数组转json
    	$json_str = json_encode(arr,JSON_UNESCAPED_UNICODE);
    	$arr = json_decode($json_str,true);
	
		// #数组和字符串互转
		$str = implode("-",$arr);	// -为分隔符,数组转string
		$arr2 = explode("-",$str);	//-为分隔符,string转数组
	
		//#提取数组的key组成新数组
		array_keys($arr);
		//#提取数组的值组成新数组
		array_values($arr);
		//#二维数组某列值取出组成一个新得数组：
		$arr2 = array_column($arr1, 'age');	//将arr1的所有name列的值组成一个新的数组


	}
	
	function unset_ex(){
		//对数组中元素unset后，会导致结构发生变化（键值无法重新排列），此时json_encode(数组）会出现异常结果
		//解决办法：
		//当unset数组元素后，用array_values（数组）方法对键值重新排列
		//unset(arr[0])	
	}
```

#### 数组排序

```php
sort() - 对数组进行升序排列
rsort() - 对数组进行降序排列
asort() - 根据关联数组的值，对数组进行升序排列
ksort() - 根据关联数组的键，对数组进行升序排列
arsort() - 根据关联数组的值，对数组进行降序排列
krsort() - 根据关联数组的键，对数组进行降序排列
```

### date

```php
<?php

	function common(){
	
		t := "2023-01=01"
	
		// #当前日期
	
		// #当前时间戳
	
		// #日期和时间戳互相转换
	
		// #日期和字符串互相转换，日期字符串格式（年月日时分秒）
	
		// #时间戳和字符串互相转换
	
		// #获取毫秒
	
		// #日期计算，n天后日期，n月后日期，n年后日期
	
		// #某日期为星期几
	
		//--------------------------------------------------
	
		//日期
		$d = date("YmdHis");
		//时间戳
		$stmp = time();
	
		//日期转时间戳
		$stmp = strtotime("1999-01-01");
	
		//时间戳转日期
		$d = date("Ymd",$stmp);
	
		//明天的日期
		$next_day = @date("Y-m-d",strtotime("+1 day"));
	
		//某个时间戳+3天
		$stmp2 = strtotime("+3 day",$stmp);
	
	}
	
	//获取标准时间戳
	function get_time(){
		date_default_timezone_set('PRC');
		$t = time();
		return $t;
	}
	
	//获取毫秒
	function getMillisecond() {
	    list($s1, $s2) = explode(' ', microtime());
	    return (float)sprintf('%.0f', (floatval($s1) + floatval($s2)) * 1000);
	}
	//utc时间格式
	function about_utc(){
		//utc转标准时间
		$utc='2019-1-18T00:00:00Z';
		$unix= str_replace(array('T','Z'),' ',$utc);
	
		//标准时间转utc
		$time='2019-1-18 00:00:00';
		$unix=strtotime($time);
		$utc=date('Y-m-dTH:i:sZ', $unix);
	}
```

### file

```php
<?php
 	$file=fopen("welcome.txt","r") or exit("Unable to open file!");

	if(file_exists($file)){
        echo "file not exists.";
    }
	if(is_dir($file)){
        echo "is dir.";
    }
	if(is_file($file)){
        echo "is file.";
    }

	fgets();	//函数用于从文件中逐行读取文件。
	fgetc();	//函数用于从文件中逐字符地读取文件。

	while(feof($file)){
        $str = fgets();
    }
	fclose($file);

	unlink($file);		//delete file

//============================file_get_contents
// 读取文件内容
$content = file_get_contents('path/to/file.txt');
echo $content;

// 写入文件内容
$content = "Hello, World!";
file_put_contents('path/to/file.txt', $content);

//============================fread
// 读取文件内容
$file = fopen('path/to/file.txt', 'r');
$content = fread($file, filesize('path/to/file.txt'));
fclose($file);
echo $content;
 
// 写入文件内容
$file = fopen('path/to/file.txt', 'w');
$content = "Hello, World!";
fwrite($file, $content);
fclose($file);
//============================fgets
// 逐行读取文件内容
$file = fopen('path/to/file.txt', 'r');
while (!feof($file)) {
    $line = fgets($file);
    echo $line;
}
fclose($file);
 
// 逐行写入文件内容
$file = fopen('path/to/file.txt', 'w');
$content = "Hello, World!";
fputs($file, $content);
fclose($file);
//============================
?>
```

| 模式 | 描述                                                         |
| :--- | :----------------------------------------------------------- |
| r    | 只读。在文件的开头开始。                                     |
| r+   | 读/写。在文件的开头开始。                                    |
| w    | 只写。打开并清空文件的内容；如果文件不存在，则创建新文件。   |
| w+   | 读/写。打开并清空文件的内容；如果文件不存在，则创建新文件。  |
| a    | 追加。打开并向文件末尾进行写操作，如果文件不存在，则创建新文件。 |
| a+   | 读/追加。通过向文件末尾写内容，来保持文件内容。              |
| x    | 只写。创建新文件。如果文件已存在，则返回 FALSE 和一个错误。  |
| x+   | 读/写。创建新文件。如果文件已存在，则返回 FALSE 和一个错误。 |



```php
<?php


	// #文件方法
	function file_ex(){
		$sfile = "s.txt";		//源文件
		$dfile = "d.txt";		//目的文件
	
		// #判断目录是否存在，获取目录路径
	
		// #目录遍历
	
		// #目录创建，复制，移动，删除
	
		// #判断文件是否存在，获取文件路径，文件大小
	
		// #文件创建，复制，移动，删除
	
		// #打开文件 --只读，写入，追加，读写。编码方式
	
		// #读取文件 --字节，字符流，buf，读取，逐行读，全部读
	
		// #写入文件 --字节，字符流，buf，写入，写入行，写入全部
	
		// #换行符判断，文件末尾判断
	
		// #关闭文件，异常捕获，释放连接
	
		// #文件指针
	
		// #文件权限，设置文件权限
	
	}


	//example:record log
	function mlog($path,$msg){
		date_default_timezone_set('PRC');
		$msg="---[".@date('Y-m-d H:i:s',$_SERVER['REQUEST_TIME'])."] ".$msg." \r\n";
		$fp=@fopen($path,'a');
		//flock($fp, LOCK_EX);
		fwrite($fp, $msg);
		//flock($fp, LOCK_UN);
		@ob_flush();
		fclose($fp);
	}
```

### http

```php
<?php

	function http_ex(){
		// #获取http请求内容，url，域名，ip，请求头
	
		// #获取get参数
	
		// #获取post参数
	}
	
	// http请求示例
	function http_request_ex(){
		$url = "http://www.baidu.com";
	
		// #get请求头
	
		// #请求参数
	
		// #发送请求
	
		// #解析响应
	
		// #释放连接


		// #post请求
	}
	
	//=====================================================
	
	function common(){
		//常见http参数
		//$_GET,$_POST,$_SERVER，$_SERVER['REQUEST_TIME']
	}
	
	//获取HTTP请求原文 @return string 
	function get_http_raw(){ 
		$raw = ''; 
		// (1) 请求行 
		$raw .= $_SERVER['REQUEST_METHOD'].' '.$_SERVER['REQUEST_URI'].' '.$_SERVER['SERVER_PROTOCOL']."\r\n"; 
		// (2) 请求Headers 
		foreach($_SERVER as $key => $value){ 
			if(substr($key, 0, 5) === 'HTTP_'){ 
				$key = substr($key, 5); 
				$key = str_replace('_', '-', $key); 
				 
				$raw .= $key.': '.$value."\r\n"; 
			} 
		} 
		// (3) 空行 
		$raw .= "\r\n"; 
		// (4) 请求Body ,post过来的数据，content-type为application/json，可用此方法读取
		$raw .= file_get_contents('php://input'); 
		 
		return $raw; 
	}
	
	//获取ip
	function get_ip(){
		static $realip;
		if(isset($_SERVER)){
			if(isset($_SERVER["HTTP_X_FORWARDED_FOR"])){
				$realip = $_SERVER["HTTP_X_FORWARDED_FOR"];
			}elseif (isset($_SERVER["HTTP_CLIENT_IP"])) {
				$realip = $_SERVER["HTTP_CLIENT_IP"];
			}else{
				$realip = $_SERVER["REMOTE_ADDR"];
			}
		}else{
			if(getenv("HTTP_X_FORWARDED_FOR")){
				$realip = getenv("HTTP_X_FORWARDED_FOR");
			}elseif(getenv("HTTP_CLIENT_IP")) {
				$realip = getenv("HTTP_CLIENT_IP");
			}else{
				$realip = getenv("REMOTE_ADDR");
			}
		}
		$ip = explode(',',$realip);
		
		return trim($ip[0]);
	}
	
	//session相关
	function session_example(){ 
		//$PHP 获取 sessionid 的方法为
		$sid = session_id();
		//可以获取指定 sessionid 中的内容
		$s = session_id($sid);


		//session共享关键代码：
		session_destroy();
		//var_dump($_SESSION);
		session_id($_POST['sid']);
		session_start();
	}

	//下载文件
	function down_info($file){
		$date = date("Ymd-H:i:m");
		$ext = strrchr($file,'.');
		Header("Content-type:application/octet-stream");
		Header("Accept-Ranges:bytes");
		Header("Accept-Length:".filesize($file));
		Header("Content-Disposition:attachment;filename={$date}.{$ext}");
		echo file_get_contents($file);
		readfile($file);
	}
	
	//get方式获取数据
	private function get_it($url){
		$ch = curl_init();
		curl_setopt($ch, CURLOPT_URL,$url);
		curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, FALSE);
		curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, FALSE);
		curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
		//set_time_limit(0);	//设置不超时
		$result = curl_exec($ch);
		curl_close($ch);
		return $result ;
	}
	//post获取数据
	private function post_it($url,$data,$json_flag=0){
		$curl = curl_init();
		curl_setopt($curl, CURLOPT_URL, $url);
	
		curl_setopt($curl, CURLOPT_SSL_VERIFYPEER, FALSE);
		curl_setopt($curl, CURLOPT_SSL_VERIFYHOST, FALSE);
		curl_setopt($curl, CURLOPT_POST, 1);
		curl_setopt($curl, CURLOPT_POSTFIELDS, $data);
		curl_setopt($curl, CURLOPT_RETURNTRANSFER, 1);
		curl_setopt($curl, CURLOPT_TIMEOUT, 10);
	
		if($json_flag){
			$header = array(
				"Accept-Charset: utf-8",
				"Content-type: application/json"
			);
			curl_setopt($curl, CURLOPT_HTTPHEADER, $header);
		}
	
	 	$result = curl_exec($curl);
		if (curl_errno($curl)) {
			return 'Errno'.curl_error($curl);
	    }
		curl_close($curl);
		return $result;
	}
```



### 异常

```php
<?php 

    function checkNum($number){
 		if($number>1){
			throw new Exception("Value must be 1 or below");
 		}
 		return true;
	}

	try{
 		checkNum(2);
 		//If the exception is thrown, this text will not be shown
 		echo 'If you see this, the number is 1 or below';
 	}catch(Exception $e){	//catch exception
 		echo 'Message: ' .$e->getMessage();
 	}

```



### error_log

```php
public function log_test(){
    $path = "c:/t.log";
    $message = "a test log...";
    error_log($message,3,$path);	//3为记录到文件 -- 0默认，记录到服务器配置的日志系统，
}
```

