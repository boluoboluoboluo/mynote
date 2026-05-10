

#### prop和attr

```js
//2者都表示属性
$(".cls").attr("id","");
$(".cls").porp("id","");

//当表示是否选中时，用prop
$(".cls").porp("checked",true);
```

#### each

```js
//示例
$(".cls").each(function(index){
    console.log(this);
})
```

#### 动态绑定事件

```js
$("body").on("click",".play_video",function(){
	console.log("hello");
});
```

#### jq对象转字符串

```js
let s = $(this).get(0).outerHTML;
```

#### 子节点

```js
let c = $(this).children(":eq(1)");		//第二个子节点
```

#### ajax

```js
//ajax请求：
$.ajax({
	type : 'post',
	dataType : 'json',
	url : "/xxx",  
	data : $('form').serialize(),
	success : function(res){
		if(res.code == 1){
			
		}else{
			
		}
	},
	error : function(){
	
	}
});
```

#### 组件触发事件

```js
//2种方式
$('.btn-success').click()
$('.btn-success').trigger("click");

//*注意*：jquery的trigger无法触发a标签的click事件,方法:
$("a标签")[0].click();
```

