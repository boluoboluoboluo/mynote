##### vue3整体运行机制
1. 编译（挂载虚拟dom）

2. 监听

3. 渲染 （创建新虚拟dom，通过渲染函数替换旧虚拟dom，挂载到web界面）

##### 请求执行

命中路由，执行中间件，不命中，不执行

 ##### 准备

1. node配置：官网下载，安装（示例安装目录为c：/node）

   ```sh
   node -v 	#终端查看node版本
   npm -v		#终端查看npm版本
   ```

2. 配置全局路径及缓存路径（不配置则模块默认安装在` c:/users/用户名/AppData/Roaming/npm`）

   `c:/node`下创建目录`node_global`和`node_cache`

   ```sh
   npm config set prefix "c:/node/node_global"		#终端设置全局模块目录
   npm config set prefix "c:/node/node_cache"
   ```

##### 术语说明

vue-cli是vue2.x的脚手架，使用`webpack`创建项目

@vue/cli是vue3.x的脚手架（兼容vue2.x），使用 `vue create` 项目名 创建项目

create-vue是vue3专用脚手架,使用vite创建项目，使用rollup打包，特点快速冷启动，热部署，性能更好（官方文档目前只保留此方式）

##### 创建项目

```sh
#create-vue方式创建项目：
npm create vue@latest		#此步需要填写项目名，还有一些选项
cd 项目目录
npm install				#安装依赖
npm run dev 			#启动项目
```

##### 打包

```sh
npm run build		#打包命令

npm run preview		#打包文件，本地预览
```

##### 常见模块安装

```sh
#安装vue3-element-plus
npm install element-plus --save

#安装node-sass
npm install node-sass --save

#安装sass-loader
npm install sass-loader --save

#安装axios
npm install axios --save
```

##### 查看安装的模块

```shell
npm ls
```



