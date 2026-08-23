console.log("init content.js...")

//随机串
const createRandomStr = ()=>{
	return Math.random().toString(36).slice(2); 
}
let downbox_id = "";

//页面注入js,将pagescript.js注入当前页面 
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

const addBtnToVideo = (video) => {
	console.log("==============开始创建下载按钮...");
	if (video.parentElement.dataset.hasBtn) return; // 避免重复
	video.parentElement.dataset.hasBtn = "true";
	
	const dwnBox = document.createElement("div");
	
	dwnBox.style.cssText = `
		position: fixed;
		z-index: 999999;
		padding: 5px 10px;
	` 
	const btn = document.createElement('button');
	btn.id = createRandomStr();
	btn.innerText = '下载';
	btn.style.cssText = `
		background: #ff4757;
		color: white;
		border: none;
		border-radius: 4px;
		cursor: pointer;
	`;
	// Object.assign(btn.style, {
	// 	position: 'absolute',
	// 	zIndex: '2147483647',
	// 	padding: '4px 8px',
	// 	backgroundColor: 'rgba(0,0,0,0.8)',
	// 	color: '#fff',
	// 	border: '1px solid #fff',
	// 	borderRadius: '4px',
	// 	cursor: 'pointer',
	// 	fontSize: '12px',
	// });


	dwnBox.appendChild(btn);

	//核心逻辑：刷新按钮位置
	const updatePosition = () => {
		const rect = video.getBoundingClientRect();
		//只有视频可见时才显示
		if (rect.top === 0 && rect.left === 0 && rect.width === 0) {
			dwnBox.style.display = 'none';
			return;
		}
		
		dwnBox.style.top = `${rect.top + 10}px`;   // 距离视频顶部 10px
		dwnBox.style.left = `${rect.left + 10}px`; // 距离视频左侧 10px
		dwnBox.style.display = 'block';
	};
  
	// 初始化位置并挂载
	updatePosition();
	document.body.appendChild(dwnBox);
	console.log("==============下载按钮已经创建.");
  
	// 监听：滚动、缩放、视频加载完成时都要重新对齐
	window.addEventListener('scroll', updatePosition);
	window.addEventListener('resize', updatePosition);
	video.addEventListener('loadedmetadata',updatePosition);
	
	// 也可以简单用定时器补丁（针对某些动态调整大小的播放器）
	// setInterval(updatePosition, 1000);

	//下载按钮点击
	btn.onclick = async (e) =>  {
		e.stopPropagation()	
		if(btn.dataset.offflag){
			return;
		}
		btn.dataset.offflag = "1";
		//video.currentSrc 为当前正在播放的视频地址
		const video_url = video.currentSrc || video.src || video.querySelector('source')?.src;
		console.log("==========下载按钮点击了,find videoUrl:" + video_url)

		if(!video_url.startsWith("blob:")){
			console.log("==============该视频准备触发直接下载.");
			//派发事件到注入的js
			const event = new CustomEvent("downEvent",{
				detail:{
					video_url:video_url
				}
			})
			document.dispatchEvent(event)	//派发事件到注入的js脚本
		}else{
			console.log("==============创建下载面板...");
			add_realdown_box();

			//===往后台脚本发送消息 清理之前缓存的urls 		//后续优化,清理本标签页缓存的urls
			await chrome.runtime.sendMessage({
				type: 'CLEAR_CACHE',
			});
			console.log("=============开启网络监听..")
			//开启后台监听
			await chrome.storage.local.set(
				{
					listen_status:1,		//开启监听开关,(后台网络请求监听)
					btn_id:btn.id			//当前下载按钮
				}
			)
			console.log("=============当前视频开始重新加载..")
			video.load()					//视频重新加载 (后台就可以捕获视频地址)
		}
	};
};

//真实下载按钮显示左下角
const add_realdown_box = () => {
    // 检查 body 是否存在
    if (!document.body) {
        setTimeout(add_realdown_box, 100);
        return;
    }
    // 防止重复添加
    if (downbox_id){
		document.getElementById(downbox_id).innerHTML = "";

		return;
	}
	
	console.log("===============add down panel.")
    const panel = document.createElement("div");
	downbox_id = createRandomStr();
	panel.id = downbox_id
    
    // 增加明显的背景色和内边距，确保能看到
    panel.style.cssText = `
        position: fixed !important;
        z-index: 2147483647 !important;
        bottom: 15px !important;
        left: 10px !important;
        background: #ff0000 !important;
        color: #ffffff !important;
        padding: 10px !important;
        font-size: 12px !important;
        border: 2px solid white !important;
        box-shadow: 0 0 10px rgba(0,0,0,0.5) !important;
        pointer-events: auto !important;
    `;
    
    // panel.innerText = "下载:";
	// const btn = document.createElement("button");
	// btn.innerText = "hello"
	// panel.appendChild(btn)

    document.body.appendChild(panel);
};

//监听后台脚本消息
chrome.runtime.onMessage.addListener((message) => {

	// console.log("收到消息，当前窗口 URL:", window.location.href);
	if (window.self !== window.top) {	//只处理顶层,排除掉页面的iframe里接收消息的可能性
		return; 
	}

	const down_url_types = ["NOMAL_DOWN_URL","M3U8_DOWN_URL"];		//消息类型 捕获到的视频请求地址
	if (down_url_types.includes(message.type)) {
		const box = document.getElementById(downbox_id);
		let btn = document.createElement("button");			//创建下载按钮
		btn.innerText = message.filename;
		box.appendChild(btn);
		console.log("创建真实下载按钮..")
		btn.onclick = async (e) => {
			e.stopPropagation();

			if(message.type === "M3U8_DOWN_URL"){
				//往后台脚本发送消息 因为跨域的原因,只能让后台脚本下载
				chrome.runtime.sendMessage({
					type: message.type,
					base_url:message.base_url,
					video_url:message.video_url,
					audio_url:message.audio_url,
				});
				return;
			}

			if(message.type === "NOMAL_DOWN_URL"){
				//派发事件到注入的js
				const event = new CustomEvent("downEvent",{
					detail:{
						base_url:message.base_url,
						video_url:message.video_url,
						audio_url:message.audio_url,
					}
				})
				document.dispatchEvent(event)	//派发事件到注入的js脚本
				return;
			}
		}
	}
});

//创建 MutationObserver 实例
const observer = new MutationObserver((mutations) => {
	for (const mutation of mutations) {
		// 检查新增的节点
		mutation.addedNodes.forEach((node) => {
			// 如果新增的是 video 标签
			if (node.tagName === 'VIDEO') {
				// console.log("发现video...")
				addBtnToVideo(node);
			} 
			// 如果新增的是包含 video 的容器，需要进一步查找
			else if (node.querySelectorAll) {
				const videos = node.querySelectorAll('video');
				videos.forEach(addBtnToVideo);
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
document.querySelectorAll('video').forEach(addBtnToVideo);


