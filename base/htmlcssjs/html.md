#### 示例

```html
<!DOCTYPE html>
<html>
	<head><title></title></head>
	<body>hello</body>
	<script>
		alert("hello");
	</script>
</html>
```

#### hr样式

```html
<!--通过border属性控制分隔线粗细颜色-->
<hr style="border:1px solid red">
```

#### textarea取值

```js
//textarea 不能通过name属性获取值
//jq通过class属性获取
$(".textarea").val()
```

#### div置顶

```html
<div style="position:fixed;top:0">
    
</div>
```

#### div浮动

```sh
#要浮动的div设置：
	positon:absolute;	#绝对定位
	top:xxx;		#顶部距离
	left:xxx;		#左侧距离
	z-index:999;	#顶层
	
#参照div设置：
	position:relative;
```





#### 多媒体播放

视频：

```html
<!-- controls控制按钮，进度条等组件 -->
<video width="50" height="50" style="cursor:pointer;" controls>
	<source src="/xxx" type="video/mp4">
</video>
```

音频：

```html
<audio controls>
    <!-- mp3 -->
    <source src="/xxx" type="audio/mpeg">
    <!-- m4a -->
    <source src="/xxx" type="audio/mp4">
</audio>
```

图片:

```html
<img height="100" src="/xxx" alt="">
```

#### 全屏设置

```html
<body style="height:100%;margin:0;background-color:#151515;color:#d5d5d5;">
</body>
```

#### 设置根元素字体

通常用于rem转换

```html
<!DOCTYPE html>
<html lang="en">
    <head>
        <title></title>
        <style>
            html{
                font-size:20px;
            }
        </style>
    </head>
</html>
```

#### rem , em , px关系

```sh
#px、em、rem都是计量单位，都能表示尺寸，但是有所不同，其各有各的优缺点

px像素（Pixel），像素px是相对于显示器屏幕分辨率而言的
px作为单位是固定不变的，不能适应浏览器缩放时产生的变化，因此一般不用于响应式网站。

em的值不固定，会继承父元素的字体大小，是一个相对单位

rem是css3中新增的相对单位，相对于html根元素，为根元素的字体大小
可以通过修改根元素字体大小就可以调整所有字体大小
可以避免字体大小逐层复合的连锁反应

#注意：任意浏览器的默认字体都是16px
```

#### html页面只能打印一页问题

```sh
#解决html页面只能打印一页问题
F12检查页面body元素样式
	#将 height:100%;	改成：	height:auto;
	#删除：overflow:hidden;
```

#### div中内容垂直水平居中

```html
<!-- div中内容居中 -->
<div style="display:flex;justify-content: center;align-items: center;">
    hello
</div>
```

```html
<!-- classB在classA中居中 -->
<div class="classA">
    <div class="classB" style="margin:auto;"
</div>
```



#### 透明度

```html
<style>
.div{
    /* 0：完全透明，1：完全不透明*/
    opacity:0;	/*完全透明*/
}
</style>
```

#### 沿基线对齐

```html
<span style="vertical-align:baseline;"></span>
```





