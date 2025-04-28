修改vite.config.js文件

```js
// https://vitejs.dev/config/
export default defineConfig({
	plugins: [
		vue(),
		vueJsx(),
		Components({
		resolvers: [NaiveUiResolver()]
		})
	],
	resolve: {
		alias: {
			'@': fileURLToPath(new URL('./src', import.meta.url))
		}
	},
	define: {
		'process.env': {
			'baseURL': '/api'
		}
	}
})
```

添加如下内容：

```js
//配置跨域
server: {
	open: false, //启动项目后打开浏览器
	port: 3000, //端口
	proxy: {
		'/api': {
			target: 'http://localhost:80', //API服务地址
			changeOrigin: true, //开启跨域
			rewrite: (path) => path.replace(/^\/api/, '')
		}
	}
}
```

