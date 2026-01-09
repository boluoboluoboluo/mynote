#### 变量判断

* 通常不需要把任意类型转换为boolean再判断，可以直接写 

  ```js
  if(myvar){}
  ```

* typeof操作符可以判断出`number`、`boolean`、`string`、`function`、`undefined`

* 判断Array

  ```js
  Array.isArray(arr)
  ```

* 判断null

  ```js
  mvar === null
  ```

* 判断某个全局表量是否存在

  ```js
  typeof window.myvar === 'undefined'
  ```

* 函数内判断某个变量是否存在

  ```js
  typeof myvar === 'undefined'
  ```

#### 类型转换

* 不要使用`new Number()`、`new Boolean()`、`new String()`创建包装对象

* 用`parseInt`或`parseFloat`来转换任意类型到`number`

* 用`String()`来转换任意类型到`string`，或直接调用某个对象的`toString()`方法

  **number对象调用toString()需特殊处理**：

  ```js
  123.toString();			//number对象转字符串，SyntaxError
  特殊处理：
  123..toString()			//number转字符串，方式一
  (123).toString()		//number转字符串，方式二
  ```

  **注意**： <font color=red>null和undefined没有toString()方法</font>
  
  