

### 页面注入js脚本

manifest.json 添加权限代码:

```json
{
...
...,
  "web_accessible_resources": [{
    "resources": ["pagescript.js"],
    "matches": ["<all_urls>"]
  }]
}
```

content.js 添加的代码示例:

```js
function invoke_jss(url){
	const js_ele = document.createElement("script")
	js_ele.src = chrome.runtime.getURL("pagescript.js")
	js_ele.async = true
	js_ele.onload = function(){
		console.log("js_ele onload ...")
		//自定义事件
		const event = new CustomEvent("testEvent",{
			detail:url
		})
		document.dispatchEvent(event)	//派发事件

		// this.remove(); // 执行后移除script标签
	}
	document.head.appendChild(js_ele)
}
```

注入脚本pagescript.js 代码示例:

```js
//监听事件
document.addEventListener("testEvent",(event)=>{
	const params = event.detail
	console.log("receive message: ",params)
	p_down(params)
})

async function p_down(url){
	const res = await fetch(url)
	const blob = await res.blob()
	console.log("type:" + blob.type)
	console.log("size:" + blob.size)
}
```

