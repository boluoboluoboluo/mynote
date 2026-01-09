

##### html隐藏title

```html
<title>&lrm;</title>		//html里设置

document.title='\u200E';	//js设置
```

##### 固定屏幕底部

```css
position:fixed;
bottom:0px;
```

##### css-div顶部对齐代码

```css
vertical-align:top;
```

##### css换行总结

```css
p{ white-space:nowrap; }	#设置p标签不换行：
p{ word-wrap:break-word; }	#自动换行
p{ word-break:bread-all; }	#强制英文单词换行，需要将行内元素设置为块级元素
p{ text-overflow:ellipsis;overflow:hidden; }	#超出显示省略号
```

##### css清除浮动

```css
style="clear:both;"
```

##### css设置背景图

```css
background-image:url("bg.jpg");		#设置背景图的url
background-size:80%;		#设置背景图大小，可设置为绝对像素值、百分比、cover(填充整个容器)、contain(完整显示整个图片)
background-repeat:no-repeat;	#可设置为repeat(重复)、no-repeat(不重复)、repeat-x(横向重复)、repeat-y(纵向重复)
background-position:center;		#背景图位置，可设置为绝对像素值、百分比、center、top、bottom、lfet、right
```

##### js-div闪现问题

js控制div出现闪现问题时，在后面添加return false;

##### js-F5刷新不出现重复提交表单弹窗

添加如下js代码：

```js
window.history.replaceState(null,null,window.location.href);
```

##### js屏蔽网页右键

```javascript
<script language="javascript">
    function cl(){
        window.event.returnValue=false;
    }
    document.oncontextmenu=cl;
</script>
```

##### js-jquery-组件触发js事件

2种方式：

```javascript
$('.btn-success').click()
$('.btn-success').trigger("click");
```

*注意*：jquery的trigger无法触发a标签的click事件
解决方法：

```javascript
$("a标签")[0].click();
```
##### js-导航栏下拉透明

```js
<!--置顶-->
<div class="index-search-al  ub ub-ac ub-pj " style="width:6.4rem;height:1rem;display:block;opacity:0;
position:fixed;z-index:9999;background:#00C9B7;hover:{background:white;}">
</div >

/* 搜索狂下拉时透明度变化  lj */
$(window).scroll(function(){
    $(".index-search-al").css({
         opacity:($(".index-search-al").offset().top)/500
    });
})
```

