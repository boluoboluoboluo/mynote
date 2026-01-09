

### 跨域问题

```sh
#名词解释:
浏览器对JavaScript发起的跨域请求（如XMLHttpRequest或Fetch API）以及跨域的DOM访问（如iframe中的内容）进行了限制。

#同源策略(限制条件)
	同协议		# http ≠ https
	同域名		# a.com ≠ b.a.com
	同端口

#历史遗留可跨域
<img src=""/>
<link style=""/>
<script src=""/>

#标准解决方案:cros
除非服务器明确允许（通过CORS机制）。这是通过浏览器在请求头中添加`Origin`字段，并检查服务器返回的响应头中是否包含`Access-Control-Allow-Origin`等字段来实现的。

#
跨域请求默认不发送Cookie，除非服务器设置Access-Control-Allow-Credentials: true且前端开启credentials: 'include'。
```

### 网页注入js

```sh
#常见场景:
1.浏览器扩展（如Chrome扩展）在特定页面注入JS。
2.在开发者工具控制台中临时执行JS代码（用于调试）。
	打开浏览器的开发者工具（通常按F12），切换到“Console”标签，然后输入JavaScript代码并回车执行。
	这种方式仅在当前页面生命周期内有效，刷新页面就会消失
	
3.通过书签注入
	可以创建一个书签，其URL部分填写JavaScript代码（以`javascript:`开头）。点击该书签时，代码会在当前页面执行。
```

**网页console注入代码示例:**

```js
//使用a标签触发内容下载
function saveFile(content, filename, contentType = 'text/plain') {
  // 创建Blob对象
  const blob = new Blob([content], { type: contentType });
  // 生成临时URL
  const url = URL.createObjectURL(blob);
  
  // 创建隐藏的<a>标签触发下载
  const a = document.createElement('a');
  a.href = url;
  a.download = filename || 'file.txt';
  document.body.appendChild(a);
  a.click();
  
  // 清理
  setTimeout(() => {
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  }, 0);
}

// 使用示例
saveFile('Hello World!', 'example.txt');
```

**注意:控制台注入受同源策略限制, 此时需使用浏览器扩展** 

模拟点击下载代码:

```js
async function down(){
    const response = await fetch('1.mp4');
    const blob = await response.blob();
    const url = URL.createObjectURL(blob);
    console.log(url)

    const a = document.createElement('a');
    a.href = url;
    a.download = 'video.mp4';
    document.body.appendChild(a);
    a.click();

    // 清理
    setTimeout(() => {
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    }, 100);
}
```

