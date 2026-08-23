console.log("background.js init ..")

importScripts('constants.js');

let checktimer = null;		//监听响应定时器 (防抖)
let request_data_map = {};	//临时存储请求数据
let netlistener_open_status = 0;		//onBeforeSendHeaders 和 onResponseStarted 监听器创建状态 (保证全局只有一份被创建)

//==============================================
//监听页面刷新事件
//==============================================
chrome.tabs.onUpdated.addListener(async (tabId, changeInfo, tab) => {
	// status 有两个状态：'loading'（开始刷新）和 'complete'（刷新完成）
	if (changeInfo.status === 'loading') {
		console.log("页面开始刷新,清理缓存中...")
		delete request_data_map[tabId]		//清理数据
	}
	if (changeInfo.status === 'complete') {
		console.log(`标签页 ${tabId} 刷新完成，当前地址: ${tab.url}`);
		console.log("本次刷新后,request_data_map:",request_data_map);
	}
});
//==============================================
// 开启网络监听
//==============================================
function open_net_listen(){
	if(netlistener_open_status ==1){
		console.log("当前网络监听器正在监听中...")
		return
	}
	netlistener_open_status = 1;
	//监听请求, (获取请求头,用于后端请求时使用)
	chrome.webRequest.onBeforeSendHeaders.addListener(
		handle_before_sendheaders,
		{ 
			urls: ["<all_urls>"],
			types: ["media","xmlhttprequest"]		//只允许媒体类型(视频,音频) 和 ajax请求 通过
		},
		["requestHeaders", "extraHeaders"] // 必须有 extraHeaders 才能拿 Cookie
	);
	// 监听网络请求响应 (捕获 url)
	chrome.webRequest.onResponseStarted.addListener(
		handle_response_start,
		{ 
			urls: ["<all_urls>"],
			types: ["media","xmlhttprequest"]		//只允许媒体类型(视频,音频) 和 ajax请求 通过
		},
		["responseHeaders", "extraHeaders"]
	);
	console.log("网络监听器已开启...")
}
//==============================================
// 关闭网络监听
//==============================================
function close_net_listen(){
	if(netlistener_open_status == 0)return;
	netlistener_open_status = 0;
	chrome.webRequest.onBeforeSendHeaders.removeListener(handle_before_sendheaders);
	chrome.webRequest.onResponseStarted.removeListener(handle_response_start);
	console.log("网络监听器已关闭...")
}
//==============================================
// onBeforeSendHeaders 被监听到时的处理函数
//==============================================
async function handle_before_sendheaders(details){
	if(request_data_map["listen_tab_id"] !== details.tabId)return;
	const VIDEO_KEYWORDS = ['m3u8', 'mp4', '.mpd', '.flv', '.f4v', 'video', 'stream', '.ts', '.m4s'];
	if(details.type === 'xmlhttprequest' && !VIDEO_KEYWORDS.some(kw => details.url.includes(kw))){
		return;
	}
	//后端请求时需要headers
	request_data_map[details.tabId] = request_data_map[details.tabId] ||{};
	request_data_map[details.tabId]["headers"] = request_data_map[details.tabId]["headers"] ||{};
	// 存入 Map，用 requestId 做唯一标识
	request_data_map[details.tabId]["headers"][details.requestId] = {
		requestHeaders: details.requestHeaders
	};
}
//==============================================
// onResponseStarted 被监听到时的处理函数
//==============================================
async function handle_response_start(details){
	if(request_data_map["listen_tab_id"] !== details.tabId)return;
	const tab_id = details.tabId;
	// let btn_id = request_data_map[tab_id]["btn_id"];
	// console.log("listen data: ",result);
	//响应头content-type
	const content_type = details.responseHeaders?.find(
		h => h.name.toLowerCase() === 'content-type'
	)?.value || '';
	//常见视频mime类型
	const video_types = [
		'video/mp4',
		'video/webm',
		'video/ogg',
		'video/quicktime',
		'video/matroska',
		'application/x-mpegURL'
	];
	const is_video = video_types.some(t => content_type.includes(t));
	const is_m3u8 = details.url.includes(".m3u8") || content_type.includes('mpegurl')
	// const isvnd = details.url.includes("videoplayback") && content_type.includes('vnd.yt-ump')		//youtube  todo...
	if(!(is_video || is_m3u8)){
		return;
	}
	// console.log("listen url: ",details.url);
	// console.log("content_type: ",content_type);
	let url_type = is_m3u8 ? MY_CONFIG.M3U8_TYPE : MY_CONFIG.NORMAL_TYPE;
	// if(isvnd)url_type = "DASH_DOWN_URL";		//youtube
	let listen_urls = request_data_map[tab_id]["listen_urls"];
	if(listen_urls && listen_urls.some(item => item.url === details.url)){			//去除重复
		return;
	}
	// console.log("responseHeaders: ",details.responseHeaders)
	try{
		const url = new URL(details.url)
		let filename = url.pathname.split('/').pop() || 'video';
		const contentDisposition = details.responseHeaders?.find(
			h => h.name.toLowerCase() === 'content-disposition'
		)?.value || '';
		const match = contentDisposition.match(/filename="?([^"]+)"?/i);
		if (match && match[1]) filename = match[1];
		// 检查扩展名
		if (!filename.includes('.')) {
			const ext = content_type.split('/')[1] || 'mp4';
			filename += `.${ext.split(';')[0]}`;
		}
		const url_data = {filename:filename,tab_id:tab_id,request_id:details.requestId,url_type:url_type,url:details.url}
		// console.log("已捕获 Headers:", headers);
		//--------更新 listen_urls
		listen_urls = listen_urls || [];
		listen_urls.push(url_data);
		request_data_map[tab_id]["listen_urls"] = listen_urls
		//--------end
		clearTimeout(checktimer);
		checktimer = setTimeout(async ()=>{
			close_net_listen();		//关闭监听
			console.log("监听关闭..")
			await deal_urls(tab_id)		//处理url
		},2000);	//2秒后再无请求就检查,处理urls,主要判断视频流是否m3u8(分片)
	}catch(e){
		console.error("error processing video: ",e)
	}
}
//==============================================
//处理监听到的urls
//==============================================
async function deal_urls(tab_id){
	const listen_urls = request_data_map[tab_id]["listen_urls"];
	let is_m3u8 = false;	//标志变量 优先判断m3u8
	if(!listen_urls || listen_urls.length == 0)return;
	console.log("处理urls:",listen_urls)
	//---------------------------
	// 判断处理 m3u8 url
	for(const item of listen_urls){
		if(item.url_type !== MY_CONFIG.M3U8_TYPE)continue;	//不是 m3u8 url 不处理
		is_m3u8 = true;
		const headers = get_request_headers(tab_id,item.request_id);
		// console.log("当前处理url:",item.url);
		// console.log("requestid:",item.request_id);
		// console.log("headers:",headers);
		const res = await fetch(item.url,{
			method: 'GET',
			headers: headers
		})
		const text = await res.text();

		// 取前 10 行进行快速判断
		const firstLines = text.split('\n').slice(0, 10).join('\n');
		// console.log("text前10行内容:",firstLines);
		if (firstLines.includes("#EXT-X-STREAM-INF")) {		//主索引 m3u8 文件
			//获取域名 (包含端口) 示例: https://localhost:8080/abc/def -> https://localhost:8080
			let base_url = new URL(item.url).origin;
			console.log("这是一个【主索引文件】，包含多个分辨率");
			const video_infos = parse_main_m3u8(text);	//解析 主索引 m3u8 文件内容
			const send_data = [];		// 多个分辨率的地址放在一起,一次性发给内容脚本
			video_infos.forEach(async (v)=>{
				if(!v.video_uri.startsWith("/")){
					base_url = item.url.slice(0,item.url.lastIndexOf("/")+1);	//用于m3u8分片地址为相对路径时,此时根据索引m3u8的url的最后一个斜杠前的部分
				}
				const tmp_data = {
					type: MY_CONFIG.M3U8_TYPE,
					video_url: base_url + v.video_uri,
					audio_url: v.audio_uri?(base_url + v.audio_uri):"",
					filename: v.video_rs,
					// btn_id:item.btn_id,
					request_id:item.request_id
				}
				send_data.push(tmp_data)

			})
			// 将 视频url 数据发送给内容脚本
			chrome.tabs.sendMessage(Number(item.tab_id), {
				type:"CREATE_DOWN_BUTTON",		//创建下载按钮消息
				data:send_data
			});
			break;		// 处理了 主m3u8索引文件 就ok,其他的url不用理会
		} else if (firstLines.includes("#EXTINF")) {
			console.log("这是一个【媒体列表】，包含分片地址");
		} else {
			console.log("不是标准的 M3U8 文件");
		}
	}
	if(is_m3u8)return;		//如果是m3u8的url,上面的步骤处理就可以了,故直接返回
	//---------------------------
	// 处理 normal urls
	const send_data = [];	//要发送的 url 数据
	for(const item of listen_urls){
		const tmp_data = {
			type: MY_CONFIG.NORMAL_TYPE,
			video_url: item.url,
			audio_url:"",
			filename: item.filename,
			// btn_id:item.btn_id,
			request_id:item.request_id
		}
		send_data.push(tmp_data)
	}
	//发送到内容脚本
	chrome.tabs.sendMessage(Number(listen_urls[0].tab_id), {
		type:"CREATE_DOWN_BUTTON",		//创建下载按钮消息
		data:send_data
	});
}
//==============================================
//解析主索引m3u8文件
//==============================================
function parse_main_m3u8(text){
	const lines = text.split('\n')
	// console.log("length:",lines.length)
	const audio_infos = []
	const video_infos = []
	let cur_video_line = ""
	let add_line_flag = 0
	lines.forEach((item)=>{
		if(item.trim() && add_line_flag){
			cur_video_line = cur_video_line + ",VIDEOURI=" + item.trim()
			video_infos.push(cur_video_line)
			add_line_flag = 0
		}
		if(item.includes("TYPE=AUDIO")){		//音频信息行
			audio_infos.push(item)
		}else if(item.includes("RESOLUTION")){	//视频信息行
			cur_video_line = item;
			// console.log("url:",cur_video_line)
			add_line_flag = 1;		//表示下一行为视频uri,需和视频元信息行添加到一起
		}
	});
	const re_video_infos = []
	video_infos.forEach((v)=>{
		// console.log("vinfo:",v)
		let audio_type = v.match(/AUDIO="([^"]+)"/)?.[1];		//获取audio类型 示例: audio-128000
		// console.log("audiotype:",audio_type)
		let audio_uri = ""
		for(const a of audio_infos){
			if(a.includes(audio_type)){
				audio_uri = a.match(/URI="([^"]+)"/)?.[1];
				break;
			}
		}
		let vinfo = {
			video_rs:v.match(/RESOLUTION=([^,]+)/)?.[1],		// 获取分辨率
			video_uri:v.match(/VIDEOURI=(.+)$/)?.[1],
			audio_uri:audio_uri
		}
		re_video_infos.push(vinfo);
	})
	// console.log("re_video_infos:",re_video_infos);
	return re_video_infos;
}
//==============================================
// 监听内容脚本消息
//==============================================
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
	// 开启监听事件
	if (request.type === 'OPEN_LISTEN') {
		if(netlistener_open_status == 1){	//如果当前正在监听,则返回 (不能同时监听多个需求)
			sendResponse({ done: false,msg:"当前有任务正在监听,请稍后.." });	//结束和内容脚本通话
			return;
		}
		console.log("监听前清理缓存数据...");
		request_data_map[sender.tab.id] = {};		//清空旧数据
		console.log("处理 OPEN LISTEN 事件...");
		request_data_map[sender.tab.id]["btn_id"] = request.btn_id;	//保存下载按钮id
		request_data_map["listen_tab_id"] = sender.tab.id;			//指定要监听的页面tab_id
		open_net_listen();				//开启网络监听
		sendResponse({ done: true });	//结束和内容脚本通话
		return;
	}
	// 获取 请求头 消息
	if(request.type === "GET_REQUEST_HEADERS"){
		const headers = get_request_headers(sender.tab.id,request.request_id);
		sendResponse({headers:headers});
		return;
	}
	// m3u8下载消息
	if (request.type === "DOWN_M3U8") {
		(async()=>{
			try{
				console.log("===============ready to send server down ...")
				let servel_url = MY_CONFIG.SERVEL_ADDR+"/down_m3u8"	//python后端处理下载
				const headers = get_request_headers(sender.tab.id,request.request_id);
				const r = await fetch(servel_url,{
					method: 'POST',
					body: JSON.stringify({
						video_url: request.video_url,
						audio_url: request.audio_url,
						headers: headers
					})
				})
				if(r.ok){
					const data = await r.json();
					sendResponse({ error:0,task_id:data.task_id });
				}else{
					sendResponse({ error:1});
				}
			}catch(error){	//异常
				sendResponse({ error:1});
			}
		})();
		return true;	//在异步回复之前需先保持通道开启
	}
	// 正常下载消息
	if (request.type === "DOWN_NORMAL") {
		(async()=>{
			try{
				console.log("===============ready to send server down ...")
				let servel_url = MY_CONFIG.SERVEL_ADDR + "/down_normal"	//python后端处理下载
				const headers = get_request_headers(sender.tab.id,request.request_id);
				const r = await fetch(servel_url,{
					method: 'POST',
					body: JSON.stringify({
						video_url: request.video_url,
						audio_url: request.audio_url,
						headers: headers
					})
				})
				if(r.ok){
					const data = await r.json();
					sendResponse({ error:0,task_id:data.task_id });
				}else{
					sendResponse({ error:1 });
				}
			}catch(error){	//异常
				sendResponse({ error:1 });
			}
		})();
		return true;	//在异步回复之前需先保持通道开启
	}
});
//==============================================
// 长连接和内容脚本 保持通信
//==============================================
chrome.runtime.onConnect.addListener((port) => {
	// 校验通道名称
	if (port.name === "UPDATE_PROGRESS") {
		console.log("长连接已建立");
		// 监听这个通道发来的消息
		port.onMessage.addListener(async (msg) => {
			try{
				console.log("来自内容脚本的长连接消息:", msg);
				const data = await query_progress(msg.task_id);	//向后端发起进度查询
				console.log("查询到下载进度数据:",data);
				// 通过这个通道向内容脚本发送消息
				port.postMessage({ error:0,status: data.status,pg_value:data.pg_value });
			}catch(error){	//异常,通知长连接关闭
				port.postMessage({ error:1 });
			}
		});
		// 监听连接断开事件（例如网页关闭、或手动关闭）
		port.onDisconnect.addListener(() => {
			console.log("长连接已断开");
		});
	}
});

//==============================================
//查询下载进度
//task_id: 对应下载的id值,服务端生成
//==============================================
async function query_progress(task_id){
	servel_url = MY_CONFIG.SERVEL_ADDR+"/find_progress"
	const r = await fetch(servel_url,{
		method: 'POST',
		body: JSON.stringify({
			task_id: task_id
		})
	})
	if(r.ok){
		const data = await r.json();
		return data;
	}
}

//==============================================
//根据请求id获取请求头
//解析监听到的请求头,转换为对象格式 {key:value}
//==============================================
function get_request_headers(tab_id,request_id){
	const headers = {};
	if (request_data_map[tab_id]["headers"][request_id]) {				// 从 Map 中取出之前存好的请求头
		request_data_map[tab_id]["headers"][request_id].requestHeaders.forEach(h => {
			headers[h.name] = h.value;
		});
	}
	return headers;
}	


//==============================================
//帮助发送请求
//==============================================
// async function help_send_request(url,headers){
// 	servel_url = MY_CONFIG.SERVEL_ADDR+"/help_query_data"
// 	const r = await fetch(servel_url,{
// 		method: 'POST',
// 		body: JSON.stringify({
// 			url: url,
// 			headers:headers
// 		})
// 	})
// 	if(r.ok){
// 		const data = await r.text();
// 		return data;
// 	}
// 	return "";
// }



