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

#查看安装的模块
npm ls
```

#### 报错：证书过期

```sh
#解决方法：
更换npm源
```



