//供页面注入的js脚本文件
//已改为后端下载,未使用
console.log("pagescript init ...")

//==============================================
//监听内容脚本转发的下载事件
//==============================================
document.addEventListener("downEvent",(event)=>{
	const data = event.detail;
	normal_down(data.video_url,data.headers);
})
//==============================================
//正常下载 (url为完整视频地址)
//==============================================
async function normal_down(url,headers){
	console.log("准备下载,video_url:",url)
	// console.log("headers:",headers);
	const res = await fetch(url,{
		headers:headers
	})
	console.log("res:",res)
	if (!res.ok) {
		console.log("请求出错. ")
		return
	}
	const reader = res.body.getReader(); // 获取读取器
	const contentLength = + parseInt(res.headers.get('content-length'), 10); // 获取总大小
	const totalMB = (contentLength / 1024 / 1024).toFixed(2);
	console.log("文件大小: ",totalMB)
	let receivedLength = 0; // 已接收字节
	let chunks = []; // 存储数据块
	while(true) {
		const {done, value} = await reader.read(); // 循环读取每一块
		if (done) break;
		chunks.push(value);
		receivedLength += value.length;
		// 下载进度
		console.log(`文件大小:${totalMB} MB, 进度: ${(receivedLength / contentLength * 100).toFixed(2)}%`);
	}
	// 全部接收完后再生成 Blob 下载
	const blob = new Blob(chunks);
	const tmp_url = window.URL.createObjectURL(blob);
	const a = document.createElement("a");
	a.href = tmp_url;
	a.style.display = "none";
	a.download = "output.mp4";
	document.body.appendChild(a);
	a.click();
	// 设置极短延时,确保点击事件在主线程处理完毕后(即交给浏览器下载进程后),再回收
	// 只有回收了这个url引用,gc才会回收blob,否则blob一直占据内存,会导致内存飙升,越来越卡(直到关闭或刷新当前页面)
	setTimeout(()=>{
		document.body.removeChild(a)
		window.URL.revokeObjectURL(tmp_url)
	},1000)
}
