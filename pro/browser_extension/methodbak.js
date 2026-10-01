//备份的一些方法 api 等

//==============================================
//监听页面刷新事件
//==============================================
// chrome.tabs.onUpdated.addListener(async (tabId, changeInfo, tab) => {
// 	// status 有两个状态：'loading'（开始刷新）和 'complete'（刷新完成）
// 	if (changeInfo.status === 'loading') {
// 		console.log("页面开始刷新,清理缓存中...")
// 	}
// 	if (changeInfo.status === 'complete') {
// 		console.log(`标签页 ${tabId} 刷新完成，当前地址: ${tab.url}`);
// 	}
// });

//==============================================
//===往后台脚本发送消息
//==============================================
// await chrome.runtime.sendMessage({
// 	type: "OPEN_LISTEN",	
// 	listen_status:1,	//开启监听开关
// 	btn_id:btn.id		//当前下载按钮 id
// });

//==============================================
//===监听后台脚本消息
//==============================================
// chrome.runtime.onMessage.addListener((message) => {
// 	if(message.type === "NORMAL_DOWN_URL"){
// 		//todo..
// 	}
// })

//==============================================
// 给内容脚本发送通知
//==============================================
// chrome.tabs.sendMessage(details.tabId, {		//tabId:当前标签页id
// 	type: 'VIDEO_FOUND',
// 	url: details.url,
// 	filename: filename
//  });

//==============================================
// 监听内容脚本消息
//==============================================
// chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
// 	if (request.type === 'CLEAR_CACHE') {		//传递的事件名称
// 		const tab_id = sender.tab.id;		//当前页id
// 		sendResponse({ done: true });
// 		return;
// 	}
// 	//如果是异步,需要这么写
// 	if(request.tpye === "xxx"){
// 		async()=>{
// 			await chrome.storage.local.get(["xxx"]);	//异步取数据
// 			sendResponse({ done: true });	//此时,才关闭通道
// 		}
// 		return true;	//告诉内容脚本,保持通道
// 	}
// })

//==============================================
//===下载api
//==============================================
// chrome.downloads.download({
// 	url: videoInfo.url,
// 	filename: videoInfo.filename,
// 	saveAs: true		//是否显示另存为对话框
// });

//==============================================
//页面注入js,将pagescript.js注入当前页面
//==============================================
// ;(function(){
// 	let id = "bl_js_" + createRandomStr()
// 	if(!document.getElementById(id)){
// 		js_ele = document.createElement("script")
// 		js_ele.id = id
// 		js_ele.src = chrome.runtime.getURL("pagescript.js")
// 		js_ele.async = true
// 		document.head.appendChild(js_ele)
// 	}
// })();

//==============================================
//内容脚本派发事件到注入的js
//==============================================
// const event = new CustomEvent("downEvent",{
// 	detail:{		//必须通过 detail 传递参数
// 		video_url:video_url
// 	}
// })
// document.dispatchEvent(event)	//派发事件到注入的js脚本

//==============================================
//监听内容脚本转发的下载事件
//==============================================
// document.addEventListener("downEvent",(event)=>{
// 	const data = event.detail;
// 	//todo..
// })

//==============================================
//创建一个尺寸观察器 (用于页面刷新时更新一次位置)
//==============================================
// const ro = new ResizeObserver((entries) => {
// 	for (let entry of entries) {
// 	// 拿到视频当前在网页上的真实物理宽高
// 	const rect = entry.target.getBoundingClientRect();
// 	// 核心拦截：只要还是 0，就绝对不执行
// 	if (rect.width === 0 || rect.height === 0) continue;
// 	updatePosition();	//渲染
// 	ro.disconnect();	//这行代码取消监听
// 	}
// });
// ro.observe(video);	// 开始对你的视频元素进行像素级肉眼追踪
//==============================================