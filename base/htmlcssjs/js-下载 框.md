### js-下载框代码

```js
<!DOCTYPE html>
	<head>
		<meta charset=utf-8>
		<title>下载</title>
		<style type="text/css">
			body{
				font-size:13px
			}
			p{
				padding:0px;
				margin:0px
			}
			.inputbtn{
				border:solid 1px #ccc;
				background-color:#eee;
				line-height:18px;
				font-size:12px
			}
		</style>
	</head>
	<body>
		<p id="pTip">开始下载</p>
		<progress value="0" max="100" id="proDownFile"></progress>
		<input type="button" value="下载" class="inputbtn" onClick="Btn_Click();">
		<script type="text/javascript">
			var intValue = 0;
			var intTimer;
			var objPro = document.getElementById('proDownFile');
			var objTip = document.getElementById('pTip');
			//定时事件
			function Interval_handler(){
				intValue++;
				objPro.value = intValue;
				if(intValue >= objPro.max){
					clearInterval(intTimer);
					objTip.innerHTML = "下载完成";
				}else{
					objTip.innerHTML = "正在下载" + intValue + "%";
				}
			}
			
			function Btn_Click(){
				intTimer = setInterval(Interval_handler,100);
			}
		</script>
	</body>
</html>
```















































