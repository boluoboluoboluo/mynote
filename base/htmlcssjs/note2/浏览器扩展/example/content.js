
console.log("content.js init ...")
invoke_js()


add_down_buttons()

function add_down_buttons(){
	const videos = document.querySelectorAll('video')
	videos.forEach(video => {
		if(!video.hasAttribute("data-downbtn")){
			add_down_button(video)
		}
	})
}

function add_down_button(video){

	const pa_ele = video.parentElement
	const down_box = document.createElement("div")
	const down_ele = document.createElement("button")
	const url_box = document.createElement("div")
	url_box.style.float = "left"
	url_box.style.position = "relative"
	url_box.style.zIndex = "99999"
	down_box.appendChild(down_ele)
	down_box.appendChild(url_box)
	down_ele.style.float = "left"
	down_ele.style.position = "relative"
	down_ele.style.top = "1px"
	// down_ele.style.left = "50px"
	down_ele.style.height = "23px"
	down_ele.style.width = "50px"
	down_ele.style.backgroundColor = "pink"
	down_ele.style.borderRadius = '3px'

	down_ele.style.zIndex = "99999"
	down_ele.textContent = "下载"
	down_ele.style.cursor = "pointer"
	pa_ele.insertBefore(down_box,video)


	video.setAttribute("data-downbtn","1")			//下载按钮已添加标识

	// 鼠标悬停效果
	down_ele.addEventListener('mouseenter', () => {
		down_ele.style.opacity = '1';
	});
	down_ele.addEventListener('mouseleave', () => {
	down_ele.style.opacity = '0.8';
	});


	let video_loaded_listener = null
	let is_down_click = 0
	down_ele.onclick = (e)=> {					//下载按钮点击事件
		e.stopPropagation()	
		// console.log("down_ele clicked ..")
		if(is_down_click){
			return 
		}
		console.log("listen urls on fetching...")

		if(video_loaded_listener){
			video.removeEventListener("loadeddata",video_loaded_listener)		//移除之前的监听器
		}
		video_loaded_listener = function video_loaded(){					//创建监听器
			
			url_box.innerHTML = ""
			let listen_urls = ""
			//--------- 定时器 获取视频地址
			const startTime = Date.now(); // 记录开始时间
			const timerId = setInterval(async function(){
				const currentTime = Date.now()
				const elapsedTime = currentTime - startTime;
				if(elapsedTime > 5000){
					clearInterval(timerId)
					console.log("listen_urls is empty.")
					return
				}

				const result = await get_storagedata('listen_urls')
				if(result['listen_urls']){
					listen_urls = result['listen_urls']
					clearInterval(timerId)

					chrome.storage.local.set(			//关闭网络请求监听
						{'listen_status':0}
					)

					listen_urls.forEach(url=>{
						const url_button = document.createElement("button")
						url_button.textContent = url.filename
						// url_button.style.positive = "relative"
						// url_button.style.zIndex = "99999"
		
						//派发事件到注入的js
						url_button.onclick = ()=>{
							const event = new CustomEvent("downEvent",{
								detail:url.url
							})
							document.dispatchEvent(event)	//派发事件到注入的js脚本
						}
		
						url_box.append(url_button)
					})
					chrome.storage.local.set({'listen_urls':null})
					return 
				}
			},500)
			//--------- 定时器 获取视频地址 end
		}
		
		video.load()							//视频重新加载
		chrome.storage.local.set(
			{'listen_status':1}					//开启网络请求监听
		)
		video.addEventListener("loadeddata",video_loaded_listener)		//添加监听器

		is_down_click = 1
	}
}

function add_sub_down(){

}



// 监听DOM变化，以便在动态加载的视频上添加按钮
const observer = new MutationObserver(mutations => {
	mutations.forEach(mutation => {
	  if (mutation.addedNodes.length) {
		  // console.log("change...")
		  add_down_buttons();
	  }
	});
  });
  
  observer.observe(document.body, {
	childList: true,
	subtree: true
  });







//页面注入
function invoke_js(){
	let js_ele = document.getElementById("bl_js")
	if(!js_ele){
		js_ele = document.createElement("script")
		js_ele.id = "bl_js"
		js_ele.src = chrome.runtime.getURL("pagescript.js")
		js_ele.async = true
		document.head.appendChild(js_ele)
	}
	
}


//监听后台脚本消息
chrome.runtime.onMessage.addListener((message) => {
	if (message.type === 'VIDEO_FOUND') {

		console.log("video url: ",message.url)

		
	}
 });

 function get_storagedata(key){
	return new Promise((resolve)=>{
		chrome.storage.local.get([key],resolve)
	})
}


//===往后台脚本发送消息
// downloadBtn.onclick = () => {
// 	chrome.runtime.sendMessage({
// 	  type: 'DOWNLOAD_VIDEO',
// 	  url: message.url
// 	});
// };


//===创建下载链接触发下载
// const tmp_url = window.URL.createObjectURL(blob)
// const a = document.createElement("a")
// a.style.display = 'none'
// a.href = tmp_url
// a.download = "video.mp4"
// document.body.appendChild(a)
// a.click()
// window.URL.revokeObjectURL(tmp_url)
// document.body.removeChild(a)



// //派发事件到注入的js
// down_ele.onclick = ()=>{
// 	const event = new CustomEvent("downEvent",{
// 		detail:video.src
// 	})
// 	document.dispatchEvent(event)	//派发事件到注入的js脚本
// }