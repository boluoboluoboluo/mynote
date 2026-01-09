console.log("background.js init ..")



// 监听网络请求
chrome.webRequest.onResponseStarted.addListener(
	async (details)=>{

		const result = await get_storagedata('listen_status')
		// console.log(result)
		if(result['listen_status'] !== 1){
			return
		}
		

		//响应头content-type
		const contentType = details.responseHeaders?.find(
			h => h.name.toLowerCase() === 'content-type'
		)?.value || '';
		//常见视频mime类型
		const videoTypes = [
			'video/mp4',
			'video/webm',
			'video/ogg',
			'video/quicktime',
			'video/matroska',
			'application/x-mpegURL'
		];
		const isVideo = videoTypes.some(t => contentType.includes(t));
		if(isVideo){

			// const result2 = await get_storagedata(details.url)
			// if(result2[details.url] !== undefined){					去除重复
			// 	return
			// }

		
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
					const ext = contentType.split('/')[1] || 'mp4';
					filename += `.${ext.split(';')[0]}`;
				}
				// 保存下载选项
				add_storagedata_tokey('listen_urls',{
					url: details.url,
					filename: filename,
					tabId: details.tabId
				})

				console.log("video url: ",details.url)

				// // 发送通知
				// chrome.tabs.sendMessage(details.tabId, {
				// 	type: 'VIDEO_FOUND',
				// 	url: details.url,
				// 	filename: filename
				//   });


			}catch(e){
				console.error("error processing video: ",e)
			}
		}
	},
	{ urls: ["<all_urls>"] },
	["responseHeaders"]
)

function get_storagedata(key){
	return new Promise((resolve)=>{
		chrome.storage.local.get([key],resolve)
	})
}
async function add_storagedata_tokey(key,data){
	const result = await get_storagedata(key)
	const exist_data = result[key] || []
	exist_data.push(data)
	chrome.storage.local.set({
		[key]:exist_data
	})
}


// 给内容脚本发送通知
// chrome.tabs.sendMessage(details.tabId, {
// 	type: 'VIDEO_FOUND',
// 	url: details.url,
// 	filename: filename
//  });

// 处理内容脚本消息
// chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
// 	if (request.type === 'DOWNLOAD_VIDEO') {
// 	  chrome.storage.local.get(request.url, (data) => {
// 		const videoInfo = data[request.url];
// 		if (videoInfo) {
// 			try{
// 				console.log("background handle message...")
// 				// down_video(videoInfo)
// 				down_video(request.url)
// 			}catch(e){
// 				console.error("error:", e)
// 			}
		  		
// 		}
// 	  });
// 	}
// });

// function  down_video(url){
// 	console.log("video_url:",url)
// 	//===下载api
// 	chrome.downloads.download({
// 		url: url,
// 		filename: 'out.mp4',
// 		saveAs: true		//是否显示另存为对话框
// 	});
// }

// function fetch_video(video_url){
// 	fetch("http://localhost:8000/down_video",{
// 		method:'post',
// 		headers:{
// 			'content-type':'application/json'
// 		},
// 		body:JSON.stringify({url:video_url}),
// 	}).then(response => {
// 		if(!response.ok){
// 			throw new Error("network response is not ok")
// 		}
// 		return response.blob()
// 	}).then(blob => {
// 		//创建下载链接触发下载
// 		const tmp_url = window.URL.createObjectURL(blob)		//该行在后台脚本无法执行
// 		const a = document.createElement("a")
// 		a.style.display = 'none'
// 		a.href = tmp_url
// 		a.download = "video.mp4"
//		document.body.appendChild(a)
// 		a.click()
// 		window.URL.revokeObjectURL(tmp_url)
// 		document.body.removeChild(a)
// 	}).catch(error => {
// 		console.error("error:",error)
// 	})
//  }




//===下载api
// chrome.downloads.download({
// 	url: videoInfo.url,
// 	filename: videoInfo.filename,
// 	saveAs: true		//是否显示另存为对话框
// });

