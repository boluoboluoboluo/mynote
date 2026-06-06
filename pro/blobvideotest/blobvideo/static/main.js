// --- 功能 1: 上传视频 ---
async function uploadVideo() {
	const fileInput = document.getElementById('videoFile');
	const statusText = document.getElementById('uploadStatus');
	if (!fileInput.files[0]) return alert('请先选择一个 MP4 视频');

	const formData = new FormData();
	formData.append('video', fileInput.files[0]);

	statusText.innerText = "正在上传并切片（FFmpeg 转换中，请稍候...）";
	
	try {
		const res = await fetch('/api/upload', { method: 'POST', body: formData });
		const data = await res.json();
		if (data.code === 200) {
			statusText.innerText = `处理成功！视频 ID 为: ${data.videoId}。...`;

		} else {
			statusText.innerText = "失败: " + data.msg;
		}
	} catch (err) {
		statusText.innerText = "网络请求错误";
	}
}

const video_id = "123";	//测试
play(video_id);

//播放代码
async function play(video_id){
	let m3u8_url = "";
	let token = "";
	try{
		const res = await fetch("/api/get_auth?video_id="+video_id);
		const data = await res.json();
		token = data.token
		m3u8_url = data.url+"?token="+token;
		// console.log("m3u8_url:",m3u8_url);
		// console.log("token:",token);
	}catch(err){
		console.log("网络错误.")
	}

	var player = videojs('my-video');		//播放实例
	player.ready(function() {
		//请求分片的时候,没有自动携带参数
		//通过这里拦截,添加参数
		videojs.Vhs.xhr.beforeRequest = function(options) {
			var url = options.uri;
			// 检查 URL 中是否已经有了这个 token，如果没有，且是 ts 或 m3u8 请求，则手动拼接
			if (url.indexOf('token=') === -1) {
				// 判断原 URL 是否已经带了其他参数
				var separator = url.indexOf('?') === -1 ? '?' : '&';
				options.uri = url + separator + 'token=' + token;
			}
			
			return options;
		};
	});

	player.src({
		src: m3u8_url,
		type: 'application/x-mpegURL'	//hls流
	});

	// player.on('error', function() {
	// 	console.log("error........")
	// 	player.removeClass('vjs-waiting');
	// 	player.removeClass('vjs-seeking');
	// });

	// // 1. 定义一个全局变量，用来备份原生的 VHS XHR 方法
	// var originalVhsXhr = null;
	// //用于监听分片加载失败,断开网络请求 (避免一后台一直错误请求,转圈圈)
	// player.on('loadstart', function(event, data) {
	// 	// 此时 tech_ 必然存在，直接绑定底层重试事件
	// 	if (player.tech_) {
	// 		player.tech_.on('retryplaylist', function(event, data) {
	// 			console.log('分片加载失败...');
	// 			if (player.tech_.vhs && player.tech_.vhs.xhr) {
	// 				if (!originalVhsXhr) {
	// 					originalVhsXhr = player.tech_.vhs.xhr; 
	// 				}
	// 				player.tech_.vhs.xhr = function() { 	//把本次准备xhr发起请求的函数清空,目的是断开请求
	// 					return { 
	// 						addEventListener: function() {},
	// 						removeEventListener: function() {},
	// 						abort: function() {},
	// 						readyState: 0,
	// 						status: 0
	// 					}; // 返回一个空对象，防止内部调用 abort 报错
	// 				};
	// 			}
		
	// 		});
	// 	}
	// });

}