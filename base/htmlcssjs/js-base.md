

#### 数组

```js

//数组添加元素：
arr.push("a")

//数组删除元素：
arr.pop()	//删除最后一个，或者arr.slice(0,-1)
arr.shift()	//删除第一个，或者arr.slice(0,1)
arr.splice(arr.indexOf("aaa"),1)		//删除指定元素，删除aaa

//判断数组是否存在某个值：
arr.indexOf("a") == -1	//不存在
arr.includes("a)	//ES6新增方法，存在返回true，不存在返回false


//json转数组(对象)：
JSON.parse(jsonstr)

//数组(对象)转json：
JSON.stringify(arr)
```

#### 基本类型转换

```js
i = 2

s = i.toString();
alert(typeof i)		//string类型

i = parseInt(s);
f = parseFloat(s);
alert(typeof i)		//number类型
alert(typeof f)		//number类型

i = Number(s);
alert(typeof i)		//number类型

b = null
nb = Boolean(b)
alert(typeof nb)	//object类型
```

#### string

```js

//==============字符串是否包含字串
var s = "abcd";
var s2 = "ab";
//方式一：支持旧版浏览器
if(s.indexOf(s2) !== -1){
    alert("包含")
}
//方式二：新版浏览器
s.includes(s2); //true

//正则方式
var str = "123"
var reg = RegExp(/3/);
if(str.match(reg)){
 //包含；
}
//==============字符串是否包含字串
```





#### 时间日期

```js
//时间戳转日期对象
let timestamp = new Date().valueOf();//当前时间戳:毫秒
date = new Date(timestamp);		//日期对象
let formattedDate = date.toLocaleString();	//格式化日期
formattedDate = date.toLocaleDateString() + ' ' + date.toLocaleTimeString();	//同上

//字符串转时间戳
var dateString = "2022-01-01";
var timestamp = Date.parse(dateString);	//毫秒级时间戳

//字符串转日期对象，再转时间戳
var dateString = "2022-01-01";
var dateObject = new Date(dateString);
var timestamp = dateObject.getTime();	//毫秒级时间戳

//===年月日时分秒
let timestamp = 1619183582000;			//毫秒级时间戳
let date = new Date(timestamp);
let year = date.getFullYear();
let month = ('0' + (date.getMonth() + 1)).slice(-2);
let day = ('0' + date.getDate()).slice(-2);
let hours = ('0' + date.getHours()).slice(-2);
let minutes = ('0' + date.getMinutes()).slice(-2);
let seconds = ('0' + date.getSeconds()).slice(-2);
let formattedDate = year + '-' + month + '-' + day + ' ' + hours + ':' + minutes + ':' + seconds;
console.log(formattedDate);
```

```js
//秒级别时间戳转日期
function timestampToDate(stamp:any){
    const date = new Date(stamp*1000);
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0'); // 月份从0开始，所以加1，并用0填充
    const day = String(date.getDate()).padStart(2, '0'); // 用0填充
    const hours = String(date.getHours()).padStart(2, '0'); // 用0填充
    const minutes = String(date.getMinutes()).padStart(2, '0'); // 用0填充
    return `${year}-${month}-${day} ${hours}:${minutes}`;
}
```



#### js换行

 ```js
 //太长使用反斜杠\换行
 let m = `mmmmmmmmmmmm\
 	iiiiiiiiiiii\
     iiiiiiiiiiiiiiii\
     dddddddddddddd\
 	rrrrr`;
 ```

#### ts可选参数

```js
//param? 参数后面加问好表示可选参数
function test(x:string,y?:string){
	console.log("test")    
}
```

