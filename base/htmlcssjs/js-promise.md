

### 说明

Promise是异步编程的一种解决方案，是一个对象，可以获取异步操作的消息，

Promise 对象代表一个异步操作，有三种状态：pending（进行中）、fulfilled（已成功）、rejected（已失败）

Promise构造函数接收一个函数作为参数，该函数的两个参数分别是 resolve 和 reject

```js
//示例
let promise = new Promise((resolve,reject)=>{
    ajax('first').success(function(res){
        resolve(res);
    })
})
```

### 5个常用方法

#### **then()**

then 方法可以接收两个回调函数作为参数，第一个回调函数是Promise对象的状态改变为 resoved 是调用，第二个回调函数是 Promise 对象的状态变为 rejected 时调用。其中第二个参数可以省略。

```js
let promise = new Promise((resolve,reject)=>{
    ajax('first').success(function(res){
        resolve(res);
    })
})
promise.then(res=>{
    console.log(res)
})
```

#### **catch()**

该方法相当于 then 方法的第二个参数，指向 reject 的回调函数。

另一个作用是，在执行resolve回调函数时，如果出错，抛出异常，不会停止陨星，而是进入catch 方法中。

```js
p.then((data) => {
    console.log('resolved',data);
}).catch((err) => {
    console.log('rejected',err);
});
```

#### **all()**

all 方法可以完成并进行任务，它接收的是一个数组，数组的每一项都是 Promise 对象。当数组中所有的 Promise 状态都达到 resolved 的时候，all 方法的状态就会变成 resolved，如果有一个状态变成了 rejected。那么all 方法的状态就会变成rejected。

```js
Promise.all([promise1,promise2,promise3]).then(res=>{
    console.log(res);
})
```

#### **rece()**

rece 方法和 all 一样，接收的参数是一个每项都是 Promise 的数组，但是与 all 不同的是，当最先执行完的事件执行完之后，就直接返回该 promise 对象的值

rece的实际作用：当要做一件事，超过长时间就不做了，可以用这个方法来解决。

```js
Promise.race([promise1,timeOutPromise(5000)]).then(res=>{})
```

#### **finally()**

finally 方法用于指定不管 Promise 对象最后状态如何，都会执行的操作。（该方法是ES2018中引入标准的）

finally 方法的回调函数不接受任何参数，这意味着没有办法知道前面的 Promise 状态到底是 fulfilled 还是 rejected

```js
promise
.then(result => {···})
.catch(error => {···})
.finally(() => {···});
```

