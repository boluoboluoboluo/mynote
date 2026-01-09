##### 创建项目

`@vue/cli`方式（已不是最新版）

1. 安装vue3

   ```sh
   #安装命令
   npm install -g @vue/cli
   #更新
   npm update -g @vue/cli
   #查看版本
   vue -version
   #图形化界面
   vue ui
   ```

2. 创建vue3应用

   ```sh
   #创建项目
   vue create 应用名称
   #说明：
   #选项如下：
   Please pick a preset: Manually select features
   ? Check the features needed for your project: Babel, TS, Router, Vuex
   ? Choose a version of Vue.js that you want to start the project with 3.x
   ? Use class-style component syntax? No
   ? Use Babel alongside TypeScript (required for modern mode, auto-detected polyfills, transpiling JSX)? No
   ? Use history mode for router? (Requires proper server setup for index fallback in production) Yes
   ? Where do you prefer placing config for Babel, ESLint, etc.? In dedicated config files
   ? Save this as a preset for future projects? (y/N) n
   ```

3. 运行vue3应用

   ```sh
   cd 应用目录
   npm run serve
   #说明：安装模块也在应用目录下，则安装在应用内
   
   #补充：拿到一个vue项目之后，通常运行 
   npm install		#先运行安装包的依赖
   ```

   注意：如项目出错，检查node版本和package.json里的模块版本是否匹配

4. 打包

   ```sh	
   #打包后的文件在项目下的dist目录
   npm run build		
   ```

   

-------------------------------------

##### 运行打包的项目

1，可以使用http-server搭建一个服务器
	--全局安装http-server
		-- npm install -g http-server
	--创建目录httptest,其下创建public，将打包项目拷贝到public目录下
	--cd到httptest目录，执行http-server，启动项目
	--打开浏览器访问
2，注意，如果打包后的文件扔到服务器（比如nginx）出现其他路径跳转404的问题
	--此时应该是history模式
	--检查项目下router/index.ts文件，采用的应该是createWebHistory
	--将createWebHistory改成createWebHashHistory，即改成hash模式
	--重新打包，即可
3，history模式如何配置打包，以及配置nginx
	-- 暂没找到可行方案 ？？？
