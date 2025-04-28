

#### 视频

```php
<?php
// 视频文件的路径
$videoPath = '/path/to/your/video/file.mp4';
 
// 确保视频文件存在
if (file_exists($videoPath)) {
    // 设置正确的内容类型头信息
    header('Content-Type: video/mp4');		//mp4格式
 
    // 发送视频文件的内容
    readfile($videoPath);
    exit;
} else {
    // 视频文件不存在的错误处理
    http_response_code(404);
    echo 'Video not found.';
}
?>
```

#### 音频

```php
$url = '/path/to/your/music/file.mp3';
// trace("url:".$url);
if(file_exists($url)){
    header('Content-Type: audio/mpeg');		//mp3,m4a格式
    header('Content-Disposition: inline; filename="' . basename($url) . '"');
    header('Content-Transfer-Encoding: binary');
    header('Content-Length: ' . filesize($url));
    header('Accept-Ranges: bytes');
    readfile($url);
    exit;
}else{
    echo "not found.";
}
```

#### 图片

````php
<?php
// 图片文件的路径
$path = '/path/to/your/file.jpg';
 
// 确保视频文件存在
if (file_exists($path)) {
    // 设置正确的内容类型头信息
    header('Content-Type: image/jpeg');	
 
    // 发送视频文件的内容
    readfile($path);
    exit;
} else {
    // 视频文件不存在的错误处理
    http_response_code(404);
    echo 'Video not found.';
}
?>
````

