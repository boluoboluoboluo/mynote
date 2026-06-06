### js基础

#### common

```js

typeof myvar === 'undefined'			//判断变量是否存在
if(myvar){}								//判断变量,通常此写法即可
typeof window.myvar === 'undefined'		//判断全局变量是否存在

//typeof操作符可以判断出`number`、`boolean`、`string`、`function`、`undefined`

Array.isArray(arr)		//判断数组

if(mvar === null){}		//判断null

//if 格式
if (条件1) {
  // 当 条件1 为 true 时执行的代码
} else if (条件2) {
  // 当 条件1 为 false 且 条件2 为 true 时执行的代码
} else {
  // 当以上所有条件都不满足时执行的代码
}

//==================
//关于null 	// 表示“我现在知道有这个用户变量，但目前还没获取到具体的用户数据”
let a;           // a 是 undefined (系统自动给的)
let b = null;    // b 是 null (你手动给的)

console.log(a == b);  // true (值相等，都代表“空”)
console.log(a === b); // false (类型不同)

console.log(typeof null); // 输出 "object" //虽然返回 "object"，但 null 并不是真正的对象，它是一个原始类型（Primitive Type）。

//undefined：表示“未定义”。比如声明了变量但没赋值，或者访问对象不存在的属性。
//null：表示“空值”。通常用于释放内存或初始化一个预期的对象变量。

//设置初始null,防止undefined,或者释放引用(垃圾回收)
let bigData = { ... }; 
bigData = null; // 释放引用
//===================
```



#### 数组

```js
//数组是特殊的js对象
//定义
const arr = []
const arr2 = new Array();
//数组添加元素：
arr.push("a")

//数组删除元素：
arr.pop()	//删除最后一个，或者arr.slice(0,-1)
arr.shift()	//删除第一个，或者arr.slice(0,1)
arr.splice(arr.indexOf("aaa"),1)		//删除指定元素，删除aaa

//判断数组是否存在某个值：
arr.indexOf("a") == -1	//不存在
arr.includes("a")	//ES6新增方法，存在返回true，不存在返回false

//==============
//遍历,方式1
const arr = ['a', 'b', 'c'];
arr.forEach((item, index) => {			//注意:无法使用 break 跳出循环。
    console.log(index, item);
});
//方式2
for (const item of arr) {			//ES6, 支持 break、continue，语义清晰。
    console.log(item);
}
//方式3 遍历并返回一个新数组，不改变原数组
const doubled = [1, 2, 3].map(num => num * 2); // [2, 4, 6]
//==============
   
//清空数组：首选 
arr.length = 0。
```

#### 对象

```js
// 方式 1
const user = {}; // 定义一个空对象
const person = {
    name: 'Alice',
    age: 25,
    greet: function() { console.log('Hello'); } // 包含方法
};
// 方式 2
const obj = new Object();
obj.name = 'Bob'; // 动态添加属性,或覆盖

//删除
delete obj[name]

const jsonstr = '{"name": "Alice", "age": 25}';	//json字符串示例

//json转js对象：
const obj = JSON.parse(jsonstr)
//js对象转json字符串：
const str = JSON.stringify(obj)

//==============
//遍历,方式1
const user = { name: 'Alice', age: 25 };
Object.keys(user).forEach(key => {
    console.log(key, user[key]);
});
//方式2
for (const [key, value] of Object.entries(user)) {
    console.log(`${key}: ${value}`);
}
//方式3	慎用!  (会遍历对象自身及其原型链上的可枚举属性)
for (const key in user) {
    if (user.hasOwnProperty(key)) { // 必须加这个判断来过滤原型链属性
        console.log(key, user[key]);
    }
}
//==============

//清空对象：通常直接 
obj = {}
```

#### map

```js
// 说明:
// 比js对象稍多内存,但是性能高

const map = new Map();
map.set(key,value);			//key不存在,新增,存在则覆盖
const value = map.get(key);	//获取值,不存在返回undefined
let has = map.has(key);		//判断是否存在,true or false ,时间复杂度o(1)
let isdelete = map.delete(key);		//删除,成功返回true,key不存在返回false
map.clear();				//清空
let size = map.size;		//数量,性能高

const obj = Object.fromEntries(map);	//转json对象 (前提是 Key 都是纯字符串)

for (const [key, value] of map) {}	//遍历
for (const key of btn_maps.keys()) {}	//遍历key
```



#### 基本类型转换

```js
//不要使用`new Number()`、`new Boolean()`、`new String()`创建包装对象

i = 2

s = i.toString();
alert(typeof i)		//string类型
//null和undefined没有toString()方法

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

```js
//保留精度并四舍五入
const num = 3.1415926;
const str = num.toFixed(2); //注意 返回的是字符串 "3.14"
const val = Number(num.toFixed(2)); //返回数字 3.14	

//只保留整数部分
Math.trunc(3.9);  // 3
Math.trunc(-3.9); // -3

//四舍五入到整数
Math.round(3.5); // 4
Math.round(3.4); // 3

//向下取整
Math.floor(3.9);  // 3
Math.floor(-3.1); // -4
//向上取整
Math.ceil(3.1);	//4
Math.ceil(3.0);	//3	注意

Math.abs(-1.2);	//绝对值 1.2


```



#### string

```sh
#JavaScript 的字符串具有不可变性（所有方法都返回新字符串，不改变原字符串）。以下是按功能分类的常用方法:

#1. 查找与校验 (Search & Check)
includes(str): 判断是否包含子串，返回 true/false。
startsWith(str) / endsWith(str): 判断是否以特定子串开头或结尾。
indexOf(str): 返回子串首次出现的索引，未找到返回 -1。
lastIndexOf(str): 返回子串最后一次出现的索引
#2. 截取子串 (Extracting)
slice(start, end): 提取从 start 到 end（不含）的部分。推荐使用，支持负数索引。
substring(start, end): 类似 slice，但不支持负数，且会自动交换较小的参数作为起点。
at(index): 获取指定位置字符，支持 -1 获取末尾字符（ES2022 新增）
#3. 修改与转换 (Modify & Convert)
replace(old, new): 替换第一个匹配项；若要替换全部，可使用正则或 replaceAll()。
split(separator): 按分隔符将字符串拆分为数组。
trim(): 去除字符串两端的空格。
toLowerCase() / toUpperCase(): 转为全小写或全大写。 
#4. 填充与重复 (Padding & Repeat)
padStart(length, pad) / padEnd(): 在开头或结尾填充字符直到达到指定长度（常用于日期或补零）。
repeat(count): 返回重复 count 次后的新字符串。
#5. 常用属性
length: 返回字符串的字符长度
```



```js
//判断字符串开头子串
const str = "Hello World";
if(str.startsWith("Hello")){
    alert("yes")
}

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

#### 正则

```js
//=================
//捕获组示例: 匹配双引号中的内容
let s = 'AUDIO="audio-128000"';
//(): 表示捕获组
//[^"]：表示匹配“除了双引号以外”的任意字符
let match = s.match(/"([^"]+)"/);	
if (match) {
    console.log(match[1]); // 输出: audio-128000
}
//=================

//------------------
[^,]	//非逗号
.+		//多个任意字符
    
//------------------
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



### dom操作

```js
//创建元素
const dom = document.createElement("button");
//设置id
dom.id = "111"
newDiv.setAttribute('id', 'my-unique-id');
//访问id
id = dom.id

//className	同上

//innerText 同上

//dom节点
pa_ele == ele.parentElement		//常用,返回父级元素
pa_ele == ele.parentNode 		//返回父节点，包括 Document 节点
//子节点
element.children	//返回一个 HTMLCollection，最推荐，因为它会自动过滤掉文本和换行符
element.childNodes 	//包含文字、注释、空格换行

//第一个/最后一个
element.firstElementChild / element.lastElementChild 	//(推荐，只找标签)
element.firstChild / element.lastChild 		//(可能拿到的是个空格或换行)

// 获取兄弟节点
element.nextElementSibling / element.previousElementSibling 	//(推荐，找邻居标签)
element.nextSibling / element.previousSibling 		//(可能拿到的是文本节点)

//节点删除
ele.remove();

//向上查找特定祖先
element.closest('.className')

//--------向下查找子孙
element.querySelectorAll('*')
const videos = node.querySelectorAll('video');	//示例,查找所有video元素
videos.forEach(addBtnToVideo);	//遍历,对每一个video执行addBtnToVideo方法
//--------end




```

### 其他

```js
//阻止冒泡
e.stopPropagation()
```

#### 关于import

```sh
#js 之间用 import

#html 使用 <script src=""></script> 引入js ,不要用import:
	--压缩的js可能出问题
	--页面每次都要加载,影响缓存性能
	--旧浏览器无法识别
```



#### 定时器

```js
const timeId = setInterval(()=>{
    if(condition){
        //todo..
        clearInterval(timeId)	//退出
    }
},intervalTime)		//间隔 intervalTime 毫秒执行
```

#### 调试

```js
//引入文件
<script src="https://cdn.bootcss.com/vConsole/3.3.4/vconsole.min.js"></script>
//初始化
var vConsole = new VConsole();
```

#### 屏蔽网页右键

```js
function cl(){
	window.event.returnValue=false;
}
document.oncontextmenu=cl;
```

#### 一些问题

```js
//F5刷新不提交表单
window.history.replaceState(null,null,window.location.href);

//textarea 不能通过name属性获取值
//jq通过class属性获取
$(".textarea").val()

//搜索框下拉透明度变化
$(window).scroll(function(){
    $(".index-search-al").css({
         opacity:($(".index-search-al").offset().top)/500
    });
})
```



