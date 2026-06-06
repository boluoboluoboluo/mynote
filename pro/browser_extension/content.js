console.log("init content.js...")

let down_panel_id = "";	//下载面板id
let render_timer = null;	//渲染定时器
let renderlistener_open_status = 0;	//渲染监听器开启状态, (确保全局只有一份)
const btn_maps = new Map();	//保存添加的下载按钮,与视频元素绑定,方便做实时渲染等工作

//==============================================
//随机串
//==============================================
const createRandomStr = ()=>{
	return Math.random().toString(36).slice(2); 
}
//==============================================
//页面注入js,将pagescript.js注入当前页面
//==============================================
;(function(){
	let id = "bl_js_" + createRandomStr()
	if(!document.getElementById(id)){
		js_ele = document.createElement("script")
		js_ele.id = id
		js_ele.src = chrome.runtime.getURL("pagescript.js")
		js_ele.async = true
		document.head.appendChild(js_ele)
	}
})();
//==============================================
//处理视频元素 (添加下载按钮及其功能)
//==============================================
const handle_video = (video)=>{
	if(video.has_add_btn)return;
	video.has_add_btn = 1;
	//创建下载按钮 (与当前视频元素绑定,视频左上角)
	const btn = add_video_btn(video);
	//开启渲染监听器 (监听滚动,缩放事件等..)
	open_render_listener();
	//执行一次渲染
	btn_rendering();
	console.log("渲染监听器开启状态:",renderlistener_open_status,"下载按钮数量:",btn_maps.size);
};
//==============================================
//创建下载按钮(到视频左上角)
//==============================================
const add_video_btn = (video)=>{
	const btn = document.createElement('button');
	btn.id = createRandomStr();
	btn.innerText = '下载';
	Object.assign(btn.style, {
		position: 'fixed',
		zIndex: '2147483647',
		padding: '4px 8px',
		backgroundColor: 'rgba(0,0,0,0.8)',
		color: '#fff',
		border: '1px solid #fff',
		borderRadius: '4px',
		cursor: 'pointer',
		fontSize: '12px',
	});
	btn.style.setProperty('white-space', 'nowrap', 'important');
	//按钮点击事件
	btn.onclick = async (e) =>  {
		e.stopPropagation()	
		// if(btn.dataset.offflag)return;
		// btn.dataset.offflag = "1";		//执行一次
		let video_url = video.currentSrc || video.src || video.querySelector('source')?.src;
		console.log("=========find videoUrl:" + video_url)
		if(video_url && !video_url.startsWith("blob:")){
			console.log("=========非blob格式=========");
			//派发事件到注入的js
			const event = new CustomEvent("downEvent",{
				detail:{
					video_url:video_url
				}
			})
			document.dispatchEvent(event)	//派发事件到注入的js脚本
		}else{
			console.log("=========blob格式=========");
			add_down_panel();		//创建下载面板
			console.log("=========开启网络监听=========")
			//往后台脚本发送消息 开启后台网络监听
			const msg = await chrome.runtime.sendMessage({
				type: "OPEN_LISTEN",	
				btn_id:btn.id		//当前下载按钮 id
			});
			if(!msg.done){
				console.log(msg.msg);
				return;
			}
			console.log("=========当前视频开始重新加载..")
			video.load()	//视频重新加载 (后台就可以监听视频地址)
		}
	};
	document.body.appendChild(btn);
	//添加到全局的map表中
	btn_maps.set(btn.id,video);				
	return btn;
}
//==============================================
//开启渲染监听器
//==============================================
const open_render_listener = ()=>{
	if(renderlistener_open_status==1)return;			//已开启
	renderlistener_open_status = 1;
	window.addEventListener('scroll', btn_rendering,true);			//开启滚动监听器
	window.addEventListener('resize', btn_rendering);				//开启缩放监听器
	render_timer = setInterval(btn_rendering,500);					//渲染定时器,每隔500ms,刷新渲染
	// console.log("渲染监听器已经开启..");
}
//==============================================
//关闭渲染监听器
//==============================================
const close_render_listener = ()=>{
	if(renderlistener_open_status==0)return;			//已关闭
	renderlistener_open_status = 0;
	window.removeEventListener('scroll',btn_rendering);				//关闭滚动监听器
	window.removeEventListener('resize',btn_rendering);				//关闭缩放监听器
	clearInterval(render_timer);		//关闭定时器
	render_timer = null;
	// console.log("渲染监听器已经关闭..");
}
//==============================================
//渲染函数
//==============================================
const btn_rendering = ()=>{
	if(btn_maps.size == 0){			//如果没有按钮 关闭监听器
		close_render_listener();
		return;
	}
	//遍历渲染
	for (const [btnid, video] of btn_maps) {
		const btn = document.getElementById(btnid);
		if(!btn)continue;
		//视频元素不存在时,销毁资源
		if (!document.body.contains(video)) {
			btn.remove()
			btn_maps.delete(btnid);
			// console.log("渲染监听器开启状态:",renderlistener_open_status);
			// console.log("当前下载按钮数量:",btn_maps.size);
			continue;
		}
		const rect = video.getBoundingClientRect();
		// 位置隐藏：滚出屏幕（上下左右四个方向完全脱离视口）
		const isOutOfViewport = 
		rect.bottom < 0 ||							// 完全滚到屏幕上方
		rect.top > window.innerHeight ||			// 完全滚到屏幕下方
		rect.right < 0 ||							// 完全滚到屏幕左侧
		rect.left > window.innerWidth;				// 完全滚到屏幕右侧
		if (isOutOfViewport) {
			btn.style.display = 'none';
			// console.log("因为视频不在屏幕内,所以无法刷新按钮...")
			continue;
		}
		if (rect.width === 0 || rect.height === 0) {
			btn.style.display = 'none';
			// console.log("因为视频未能加载出来,所以无法刷新按钮...")
			continue;
		}
		btn.style.top = `${rect.top + 10}px`;   // 距离视频顶部 10px
		btn.style.left = `${rect.left + 10}px`; // 距离视频左侧 10px
		btn.style.display = 'block';
	}
}
//==============================================
//真实下载面板,显示左下角
//==============================================
const add_down_panel = () => {
	if (down_panel_id){	// 防止重复添加
		document.getElementById(down_panel_id).innerHTML = "";
		return;
	}
	const panel = document.createElement("div");
	down_panel_id = createRandomStr();
	panel.id = down_panel_id
	// 增加明显的背景色和内边距，确保能看到
	panel.style.cssText = `
		position: fixed !important;
		z-index: 2147483647 !important;
		bottom: 15px !important;
		left: 10px !important;
		background: #ffffff !important;
		color: #000000 !important;
		padding: 10px !important;
		font-size: 12px !important;
		border: 2px solid black !important;
		box-shadow: 0 0 10px rgba(0,0,0,0.5) !important;
		pointer-events: auto !important;
	`;
	document.body.appendChild(panel);
};
//==============================================
//创建真实下载按钮
//==============================================
const add_down_btn=(name,jump_type)=>{
	const down_panel = document.getElementById(down_panel_id);
	let btn = document.createElement("button");			//创建下载按钮
	let btnbox = document.createElement("div");
	btnbox.cssText = `
		padding: 5px !important;
	`
	btn.cssText = `
		background: #ffffff !important;
	`
	btn.innerText = message.filename;
	btnbox.appendChild(btn);
	down_panel.appendChild(btnbox);
}
//==============================================
//监听后台脚本消息
//==============================================
chrome.runtime.onMessage.addListener((message) => {
	if (window.self !== window.top) {	//只处理顶层,排除掉页面的iframe里接收消息的可能性
		return; 
	}
	//-------------------------------
	const down_url_types = ["NORMAL_DOWN_URL","M3U8_DOWN_URL"];		//消息类型 捕获到的视频请求地址
	if (down_url_types.includes(message.type)) {

		// add_down_btn();

		const down_panel = document.getElementById(down_panel_id);
		let btn = document.createElement("button");			//创建下载按钮
		let btnbox = document.createElement("div");
		btnbox.cssText = `
			padding: 5px !important;
		`
		btn.cssText = `
			background: #ffffff !important;
		`
		btn.innerText = message.filename;
		btnbox.appendChild(btn);
		down_panel.appendChild(btnbox);
		//-------------------------------
		btn.onclick = async (e) => {
			e.stopPropagation();
			if(message.type === "NORMAL_DOWN_URL"){
				console.log("开始向注入js发起下载...");
				//向后台脚本发消息,拿请求头
				const headers = await chrome.runtime.sendMessage({ type: "GET_REQUEST_HEADERS",request_id:message.request_id });
				//派发事件到注入的js
				const event = new CustomEvent("downEvent",{
					detail:{
						video_url:message.video_url,
						audio_url:message.audio_url,
						headers:headers.headers
					}
				})
				document.dispatchEvent(event)	//派发事件到注入的js脚本
				return;
			}
			if(message.type === "M3U8_DOWN_URL"){
				console.log("开始向后台发起下载...");
				//往后台脚本发送消息 因为跨域的原因,只能让后台脚本下载
				chrome.runtime.sendMessage({
					type: message.type,
					video_url:message.video_url,
					audio_url:message.audio_url,
					request_id:message.request_id
				});
				return;
			}
		}
	}
});
//==============================================
//创建 MutationObserver 实例
//==============================================
const observer = new MutationObserver((mutations) => {
	for (const mutation of mutations) {
		// 检查新增的节点
		mutation.addedNodes.forEach((node) => {
			// 如果新增的是 video 标签
			if (node.tagName === 'VIDEO') {
				// console.log("发现video...")
				handle_video(node);
			} 
			// 如果新增的是包含 video 的容器，需要进一步查找
			else if (node.querySelectorAll) {
				const videos = node.querySelectorAll('video');
				videos.forEach(handle_video);
			}
		});
	}
});
//监听整个文档
observer.observe(document.body, {
	childList: true,
	subtree: true
});
// 首次执行：处理页面上已经存在的视频
document.querySelectorAll('video').forEach(handle_video);
//==============================================
