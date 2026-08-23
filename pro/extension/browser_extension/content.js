console.log("init content.js...");

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
		// let video_url = video.currentSrc || video.src || video.querySelector('source')?.src;
		add_down_panel();		//创建下载面板
		console.log("=========开启网络监听=========");
		//往后台脚本发送消息 开启后台网络监听
		const msg = await chrome.runtime.sendMessage({
			type: "OPEN_LISTEN",	
			btn_id:btn.id		//当前下载按钮 id
		});
		if(!msg.done){
			console.log(msg.msg);
			return;
		}
		console.log("=========当前视频开始重新加载..");
		// 1. 记录当前的播放位置等信息
    	const savedTime = video.currentTime;
		const isPaused = video.paused;
		// 2. 监听元数据加载完成的事件（必须在此事件后才能设置时间）
		video.addEventListener('loadedmetadata', function onMetadata() {
			video.currentTime = savedTime;
			if(isPaused)video.pause();
			console.log("元数据加载事件...")
			// 移除监听器，避免下次播放时重复触发
			video.removeEventListener('loadedmetadata', onMetadata);
		}, { once: true }); // 使用 once: true 也可以确保只触发一次
		// 视频地址 判断重新加载方式
		let video_url = video.currentSrc || video.src || video.querySelector('source')?.src;
		if(video_url.startsWith("blob:")){		//blob 格式
			video.src = "";
			video.load();	// 清空当前缓冲区
			video.src = video_url;
		}else{
			video.load();	// 视频重新加载 (后台就可以监听视频地址)
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
	// 防止重复添加
	if (down_panel_id){
		document.getElementById(down_panel_id).querySelector('.content').innerHTML = "";
		document.getElementById(down_panel_id).style.display = "";
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
		min-width: 150px;
		min-height:50px;
		background-color: rgba(0,0,0,0.8) !important;
		color: #fff !important;
		border: 1px solid #fff;
		border-radius: 1px;
		padding: 5px 5px !important;
		font-size: 12px !important;
		pointer-events: auto !important;
	`;
	const tipspan = document.createElement("span");
	tipspan.innerHTML = "下载捕获";
	panel.appendChild(tipspan);
	const clbtn = document.createElement("span");
	clbtn.style.cssText = `
		position: absolute;       
		top: 1px;                /* 距离顶部的距离 */
		right: 1px;              /* 距离右侧的距离 */
		line-height: 0.7;
		cursor: pointer;          /* 鼠标悬停时显示小手图标 */
		font-size: 18px;
		color: #bbbbbb;
		user-select: none;        /* 防止用户双击误选中文本 */
		transition: color 0.2s;   /* 过渡动画 */
	`;
	clbtn.innerHTML = '&times;'; // 使用 HTML 实体叉号 ×
	// 为关闭按钮添加鼠标悬停效果（变红）
    clbtn.addEventListener('mouseenter', () => clbtn.style.color = '#fe1111');
    clbtn.addEventListener('mouseleave', () => clbtn.style.color = '#bbbbbb');
	clbtn.addEventListener('click', (event) => {
        event.stopPropagation(); // 阻止事件冒泡，防止触发父元素的点击事件
        panel.style.display = 'none'; // 隐藏整个弹窗
    });
	panel.appendChild(clbtn);
	const cont = document.createElement("div");
	cont.className = "content";
	panel.appendChild(cont);
	document.body.appendChild(panel);
};
//==============================================
//创建真实下载按钮
//==============================================
const add_down_btn=(name,down_type,video_url,audio_url,request_id)=>{
	//-------------------------------
	// 在下载面板里,创建真正的 下载按钮
	const down_panel = document.getElementById(down_panel_id);
	let btn = document.createElement("button");			//创建下载按钮
	let btnbox = document.createElement("div");
	btnbox.className = 'child-div';
	btn.style.cssText = `
		background-color: #fff !important;
		color: #111 !important;
		border: 1px solid #fff;
		border-radius: 2px;
		cursor: pointer;
		padding: 1px;
		margin:	1px !important;
	`
	btn.innerText = name;
	btnbox.appendChild(btn);
	const pg = document.createElement("span");	
	btnbox.appendChild(pg);
	down_panel.querySelector(".content").appendChild(btnbox);
	//-------------------------------
	// 点击事件
	btn.onclick = async (e) => {
		e.stopPropagation();
		btn.nextSibling.style.display = "";	//显示进度条
		console.log("down type: ",down_type)
		if(down_type === MY_CONFIG.NORMAL_TYPE){
			console.log("开始向后台发起下载...");
			//往后台脚本发送消息 因为跨域的原因,只能让后台脚本下载
			const data = await chrome.runtime.sendMessage({
				type: "DOWN_NORMAL",
				video_url:video_url,
				audio_url:audio_url,
				request_id:request_id
			});
			if(data.task_id){
				open_query_connect(btn,data.task_id);	//开启和后台脚本通信长连接,实时更新下载进度
			}
			return;
		}
		//下载m3u8格式
		if(down_type === MY_CONFIG.M3U8_TYPE){			
			console.log("开始向后台发起下载...");
			//往后台脚本发送消息 因为跨域的原因,只能让后台脚本下载
			const data = await chrome.runtime.sendMessage({
				type: "DOWN_M3U8",
				video_url:video_url,
				audio_url:audio_url,
				request_id:request_id
			});
			if(data.task_id){
				open_query_connect(btn,data.task_id);	//开启和后台脚本通信长连接,实时更新下载进度
			}
			return;
		}
	}
}
//==============================================
//开启和后台脚本通信长连接,实时查询下载进度
//btn: 当前真实下载按钮
//task_id: 后台生成的本次下载down_id,唯一
//==============================================
function open_query_connect(btn,task_id){
	// 1. 建立长连接，并给这个通道起个名字
	const port = chrome.runtime.connect({ name: "UPDATE_PROGRESS" });
	// 2. 500毫秒后发送一次询问
	setTimeout(()=>{
		port.postMessage({ task_id: task_id });
	},500);
	// 3. 监听后台发回来的消息
	port.onMessage.addListener((msg) => {
		console.log("长连接收到后台消息:", msg);
		if(msg.error == 1){
			btn.nextSibling.textContent = "进度:出错了..";
			port.disconnect();	//关闭连接
			return;
		}
		if(msg.status === 0){
			//更新进度
			btn.nextSibling.textContent = "进度:"+msg.pg_value;
			//500毫秒后再询问
			setTimeout(()=>{
				port.postMessage({ task_id: task_id });
			},500);
			return;
		}
		if(msg.status === 1){	//下载完成
			btn.nextSibling.textContent = "进度:"+msg.pg_value;
		}
		port.disconnect();	//关闭连接
	});
}
//==============================================
//监听后台脚本消息
//==============================================
chrome.runtime.onMessage.addListener((message) => {
	//只处理顶层,排除掉页面的iframe里接收消息的可能性
	if (window.self !== window.top) {
		return; 
	}
	// 创建下载按钮消息
	if (message.type == "CREATE_DOWN_BUTTON") {
		data = message.data;
		for(const d of message.data){
			add_down_btn(d.filename,d.type,d.video_url,d.audio_url,d.request_id);
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
