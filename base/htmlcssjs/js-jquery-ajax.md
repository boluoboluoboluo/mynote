

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

