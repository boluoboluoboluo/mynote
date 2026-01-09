代码：

```js
//点击按钮
$('#button').click(async function(){
    const p = new Promise(function(resolve, reject){
        layer.confirm('确认吗',function(index){
        	layer.close(index);
       		console.log("ssss");
        	resolve("");
    	})
    });
    await p;
    console.log("1111");
});
```

