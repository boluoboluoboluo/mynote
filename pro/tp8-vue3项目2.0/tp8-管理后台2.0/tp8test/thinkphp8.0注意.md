### 备注

##### env文件

根目录下`.example.env`文件，改成`.env`，默认调试模式。

##### 开启mysql扩展

在`php.ini`文件里开启`pdo_mysql`扩展

##### 开启多应用

默认只有一个app应用，可通过开启多应用，创建admin应用等，用于区分业务

```sh
composer require topthink/think-multi-app	#安装多应用模式扩展
```

##### 日志问题

调试模式下，每次数据库访问都会在`runtime/log`下记录日志，部署模式不会记录的。

```php
//在/config/log.php中配置日志path
// 日志通道列表
'channels'     => [
    'file' => [
        // 日志记录方式
        'type'           => 'File',
        // 日志保存目录
        'path'           => app()->getRootPath().'/runtime/log',
        // 单文件日志写入
        'single'         => false,
        //该文件后面代码略...
```



##### 模板渲染问题

使用模板渲染，需安装`think-view` 扩展

```sh
composer require topthink/think-view 	#应用根目录下执行，安装think-view扩展
```

##### session问题

需在`app/middleware.php`开启session：

```php
<?php
// 全局中间件定义文件
return [
    // 全局请求缓存
    // \think\middleware\CheckRequestCache::class,
    // 多语言加载
    // \think\middleware\LoadLangPack::class,
    // Session初始化
    \think\middleware\SessionInit::class
];
```

注意：<font color='red'>会话数据统一在当前请求结束的时候统一写入 所以不要在`session`写入操作之后执行`exit`等中断操作,否则会导致`Session`数据写入失败。</font>

##### 404页面问题

在`config/app.php`配置：

```php
'http_exception_template'    =>  [
    // 定义404错误的模板文件地址
    404 =>  \think\facade\App::getRootPath() . 'view/404.html',
    // 还可以定义其它的HTTP status
    // 401 =>  \think\facade\App::getRootPath() . '401.html',
]
```

还可以在`app/ExceptionHandle.php`里自己配置：

```php
public function render($request, Throwable $e): Response{
    // 添加自定义异常处理机制
   if($e->getStatusCode() == '404'){
        return view("/404")->code(404);		//访问view目录下404.html，返回404状态码
    }

    // 其他错误交给系统处理
    return parent::render($request, $e);
}
```

##### 文件上传

上传到远程需要安装`think-filesystem`扩展，首先使用下面的命令安装。

```sh
composer require topthink/think-filesystem
```

##### 清除缓存

如果需要清除应用的缓存文件，可以使用下面的命令

```sh
php think clear

php think clear --dir		#不保留空目录

php think clear --log		#清除日志目录
```

说明：多应用下，建议手动清除缓存

##### 	验证码配置

1.开启php-gd库

说明：在`php.ini`搜索gd：

```
#将前面的分号;去掉
extension=gd
```

2.配置

在`config/captcha.php`中配置验证码的宽度和高度

```php
// 验证码图片高度
'imageH'   => 80,
// 验证码图片宽度
'imageW'   => 260,
```

3.编写后台方法

```php
<?php
namespace app\index\controller;
use think\captcha\facade\Captcha;

class Index{
	public function verify(){
        return Captcha::create();    
    }
}
```

4.访问

然后访问下面的地址就可以显示验证码：

```
http://serverName/index/index/verify
```

##### 缓存导致访问慢问题

描述：

本地通过localhost访问很慢，127.0.0.1访问会快很多

打开F12可以看到，两者每次都重新加载静态资源了，由于localhost方式会走域名解析，导致非常慢。

解决方案：

//TODO...

