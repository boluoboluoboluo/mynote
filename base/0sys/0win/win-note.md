

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

#### cmd突然管理员运行

```sh
#打开cmd突然默认以管理员运行?
	可能用户账户控制手滑调到最低档了	#改回默认的第二档
```

#### 多个无效网络连接问题

```sh
#ipconfig /all  命令查看到多个无效的本地连接(媒体断开)
	设备管理器->显示隐藏设备->网络设备->选择对应的卸载
```

#### 文件默认打开方式还原

将文件的默认打开方式还原成无默认打开方式：
  --1.开始菜单右键运行/regedit
  --2.删除HKEY_CLASSES_ROOT下需要恢复文件格式的后缀名键值文件夹、HKEY_CURRENT_USER\Software\Microsoft\windows\CurrentVersion\Explorer  \FileExts下需要恢复文件格式的后缀名键值文件夹
  --3.重启电脑

#### 设置视频文件夹默认显示方式

**手动调整模板类型**

1. **进入目标文件夹**
   例如，打开存放视频的文件夹。
2. **设置文件夹模板**
   - 右键文件夹空白处 → **“属性”** → **“自定义”** 标签。
   - 在 **“优化此文件夹以”** 下拉菜单中选择 **“常规项”**（此模板默认支持详细信息视图）。
   - 勾选 **“同时应用于子文件夹”** → 点击 **“确定”**。
