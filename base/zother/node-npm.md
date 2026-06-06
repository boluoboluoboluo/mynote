

#### 准备

```sh
#安装node.js (官网下载)
node -v 	#检查
npm -v 		#检查
```

```sh
#运行js代码
node test.js		#示例
```

```sh
===========
#一些设置:

#如果指定了安装路径的话,则不会安装到项目目录,此时需要下面命令:
npm config delete prefix	#删除安装路径 (恢复默认) 
npm config delete cache		#删除缓存路径 (恢复默认) 

#npm 安装包的 默认缓存 在 C:\Users\52369\AppData\Local\npm-cache
npm config set cache ./.npm-cache	#修改到当前项目下
===========

#项目初始化
#cd 到工作目录 (没有则创建)
npm init -y				#初始化一个项目
npm install esbuild		#安装示例(esbuild为一个用来压缩js的包),会安装到当前目录
===========
#项目删除:
删除文件夹即可
```

```sh
===========
#如果是克隆的项目
#cd 到项目目录:
npm install  #即可
```



#### 常见命令和设置

```sh
#查看当前镜像源：
npm config get registry

#设置淘宝镜像源：
npm config set registry https://registry.com.npm.taobao.org --global

#新的镜像（2024）
npm config set registry https://registry.npmmirror.com --global

#切换原本npm源：
npm config set registry https://registry.npmjs.org

#查看.npmrc配置：
npm config list

#安装模块命令：
#参数：--save 		将模块依赖关系写入到package.json文件的dependencies参数中，代表运行时依赖（开发和运行都需要的包）
#参数：--save-dev 	将模块依赖关系写入到package.json文件的devDependencies参数中，代表开发时依赖（仅开发需要的包）
#说明：判断包是否开发和运行需要，参考https://npmjs.com/package/npm，以该网站安装命令为准
#参数：-g			表示全局
#参数：@+version	//位于模块名后面，安装指定版本
npm install [-g] 模块名 [--save][-dev]

#更新模块命令
npm update [-g] 模块名 [--save][-dev]

#卸载模块命令
npm uninstall [-g] 模块名 [--save][-dev]

#搜索模块命令
npm search [-g] 模块名 [--save][-dev]

#查看安装的模块 -g 全局模块
npm ls
npm list -g --depth=0	#全局包完整目录树

#查看安装路径
npm config get prefix

```

#### 报错：

```sh
#提示证书过期
#解决方法：
更换npm源

#全局安装时报错:
终端需要管理员权限
```



