

```sh
#node环境:略

#cd 到项目文件夹
npm init -y 	#创建初始化项目 (如果没有的话)
npm install esbuild		#安装压缩工具包 esbuild

#压缩 test.js 文件
# --minify：核心参数。开启压缩，会自动去除空格、换行、注释，并混淆变量名（把长变量缩短）。
npx esbuild test.js --minify --outfile=test.min.js	#单文件压缩
npx esbuild static/js/*.js --minify --outdir=static/js/min/		#批量压缩

npx esbuild src/index.js --bundle --minify --outfile=dist/bundle.min.js	#合并压缩(a.js引入了b.js)

#使用
压缩后的js,在html里通过 <script src="xx.js"></script>
```

