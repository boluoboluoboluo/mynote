### 安装

1. 安装composer，命令如下：

   ```sh
   #下载安装脚本 composer-setup.php 到当前目录
   php -r "copy('https://install.phpcomposer.com/installer', 'composer-setup.php');"
   #执行安装过程
   php composer-setup.php
   #删除安装脚本
   php -r "unlink('composer-setup.php');"
   ```

   上述下载 Composer 的过程正确执行完毕后，可以将 `composer.phar` 文件复制到任意目录（比如项目根目录下），然后通过

    `php composer.phar` 指令即可使用 Composer 了！

2. composer全局配置（可选）

   **Mac 或 Linux 系统**，将下载的 `composer.phar` 文件移动到 `/usr/local/bin/` 目录下面：

   ```sh
   sudo mv composer.phar /usr/local/bin/composer
   ```

   **Windows 系统：**将 `composer.phar` 复制到 PHP 的安装目录下面，新建一个 `composer.bat` 文件，写入下列代码：

   ```sh
   @php "%~dp0composer.phar" %*
   ```

   然后可使用composer命令了

   ```sh
   #查看版本
   composer --version
   #更新
   composer selfupdate
   
   #查看配置
   composer config --list
   ```



### 配置源

如下：

```sh
#全局配置源，国内镜像（不稳定）
composer config -g repo.packagist composer https://packagist.phpcomposer.com
#阿里云源（可用）
composer config -g repo.packagist composer https://mirrors.aliyun.com/composer/

#若已有web应用，可以cd到应用目录下，进行局部配置
#composer config repo.packagist composer https://packagist.phpcomposer.com

#解除镜像命令，恢复到官方源
#composer config -g --unset repos.packagist
```