##### vuepress搭建

> 依赖node环境（v16.19.0+）



1. 创建目录

   ```shell
   mkdir vuepress-test
   cd vuepress-test
   ```

2. 初始化项目

   ```shell
   git init 	#git初始化，可选
   npm init
   ```

3. 安装

   ```shell
   #参数-D 即 --save-dev 用于开发环境，-S 即 --save 用于生产环境
   npm install -D vuepress@next
   ```

4. 修改package.json

   ```json
   {
     "scripts": {
       "docs:dev": "vuepress dev docs",
       "docs:build": "vuepress build docs"
     }
   }
   ```

5. 将临时目录和缓存目录添加到 `.gitignore` （可选）

   ```shell
   echo 'node_modules' >> .gitignore
   echo '.temp' >> .gitignore
   echo '.cache' >> .gitignore
   ```

6. 创建第一篇文档

   ```shell
   mkdir docs
   echo '# Hello VuePress' > docs/README.md
   ```

7. 启动服务器 （默认打开docs/README.md）

   ```shell
   npm run docs:dev
   ```

   