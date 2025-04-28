#### 一些命令

```sh
type file	#查看文件内容
more file	#查看文件内容
```



#### 局域网共享

电脑a访问电脑b用户目录

```
1.获取b电脑ip（a和b在同一个网段）
2.电脑a，开始->运行，输入:\\b电脑ip
3.输入b电脑用户名密码
```

#### 批处理打开指定目录

新建批处理文件 test.bat，写入如下内容：

```sh
@echo off
@set LESSCHARSET=UTF8
@d:
cmd /k "cd /job/test"
```

保存。双击即可打开cmd窗口，目录`d:/job/test`

#### 批处理代替命令执行脚本

示例：使用bat文件，调用c盘某安装路径的php.exe，执行当前路径php文件

假设当前目录为`c:\home`，`php.exe`路径：`c:\install\php.exe`

新建run.bat，内容：

```sh
@ C:\install\php.exe %1
```

新建test.php，内容：

```php
<php?
    echo "hello";
```

cmd下执行：

```sh
c:\home> run test.php
```

输出：hello

#### win11禁用自动更新

 ```sh
 #禁用更新
 1.打开注册表win+r ，输入regedit
 2.定位到 \HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\WindowsUpdate\UX\Settings
 3.新建DWORD，名字：FlightSettingsMaxPauseDays，十进制值36524
 4.打开电脑->设置->windows更新，暂停更新-延长一周 那个条目，选择延长5000周
 
 #禁用windows update服务
 win+r，输入services.msc，查找windows update服务，停止服务，并设置启动方式为手动
 
 ```

#### win11进入安全模式

```sh
win+r，输入msconfig
选择引导，
勾选安全引导（最小）	

#注意，不要选Active Directory修复，否则重启黑屏
```

