console.log("pagescript init ...")


document.addEventListener("downEvent",(event)=>{
	const params = event.detail
	console.log("receive message: ",params)
	p_down(params)
})



async function p_down(url){
	// const res = await fetch(url)
	// const blob = await res.blob()
	// console.log("type:" + blob.type)
	// console.log("size:" + blob.size)


	console.log("video_url:",url)
	const res = await fetch(url)
	const blob = await res.blob()
	const tmp_url = window.URL.createObjectURL(blob)
	console.log("tmp_url",tmp_url)

	const a = document.createElement("a")
	a.href = tmp_url
	a.style.display = "none"
	a.download = "output.mp4"
	document.body.appendChild(a)
	a.click()
	setTimeout(()=>{
		document.body.removeChild(a)
		window.URL.revokeObjectURL(tmp_url)
	},1000)

}