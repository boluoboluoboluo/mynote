<?php /*a:1:{s:62:"C:\z_data\wkspace\php\tp8test\view\admin\index\uploadtest.html";i:1695054092;}*/ ?>
<html>
	<head>
		<title>hello</title>
	</head>
	<body>
		<form action="/admin/index/upload" enctype="multipart/form-data" method="post">
		<input type="file" name="image" /> <br> 
		<input type="submit" value="上传" /> 
		</form> 

	
		<br><br>

		<form action="/admin/index/uploads" enctype="multipart/form-data" method="post">
		<input type="file" name="images[]" /> <br> 
		<input type="file" name="images[]" /> <br> 
		<input type="file" name="images[]" /> <br> 
		<input type="submit" value="多文件上传" /> 
		</form> 
	</body>
</html>