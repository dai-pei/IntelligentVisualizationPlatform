# 20220416
## package.json和package-lock.json
https://juejin.cn/post/7078233610683170824
后者固定版本号

# 20220417
## 选择es5而非es6的原因：es6在2015年刚出来，浏览器的支持不是很好，（但我做的是桌面应用：也可能改成浏览器版本……）
https://blog.csdn.net/weixin_42386551/article/details/111370285
https://www.jianshu.com/p/b2f544d7686e

## 主流js编译器——babel
https://juejin.cn/post/6844903781365186567

## v8引擎：为了更快地解析js脚本
[v8引擎与浏览器网页解析的原理](https://zhuanlan.zhihu.com/p/27628685)
[v8的性能优化技术——内联缓存](https://juejin.cn/post/6844904167333429256)

## v8引擎是js引擎（js编译器 plus）
如果需要用js/ts写桌面程序，主流写法两种
[electron或nw.js](https://www.jianshu.com/p/c6bdb087e60d)

## node.js是什么
node是一个软件，是一个js运行时环境（js不是c++这种系统语言，它是脚本语言，它的运行必须要依赖运行时环境，比如浏览器等），安装了node，就可以写js代码并run起来，node中核心的js引擎用的是google v8引擎
引擎： 负责整个JS程序的编译及执行过程
编译器： 负责语法分析及代码生成等工作
作用域： 收集并维护由所有声明的标识符（变量）组成的一系列查询，实施一套非常严格的规则， 确定当前执行的代码对这些标识符的访问权限
[js编译器，引擎，作用域](https://www.jianshu.com/p/36f5bfc6b7e6)

## 选择的前端框架，不是vue，而是svelte
[electron+svelte开发桌面程序](https://learnku.com/articles/45831)

[简介 / 添加数据 • Svelte 教程 | Svelte 中文网 (sveltejs.cn)](https://www.sveltejs.cn/tutorial/adding-data)

# 20220418

## [sing visualizer](https://github.com/weiijiie/singing-visualizer)
github已经有一个和我想做的差不多，但它是浏览器应用，我是桌面应用；而且他做的比较简单
但是现在后端网页他没有维护，所以我没法看它的运行情况

## js错误处理
```
try()
{
    do();
    //...
}
catch(e)
{
    console.log(e.name+" "+e.message);
    console.log(e.stack);
}
```

## js面向对象机制
js的面向对象使用function定义一个函数来实现

## js prototype原型对象，用于给对象增加属性或者方法
[prototype 原型链](https://www.runoob.com/js/js-object-prototype.html)

## js属性描述对象
```
{
  value: 123,
  writable: false,
  enumerable: true,
  configurable: false,
  get: undefined,
  set: undefined
}
```
seal和freeze冻结对象状态的修改
## js OOP
js 语言使用构造函数（constructor）作为对象的模板。所谓”构造函数”，就是专门用来生成实例对象的函数。它就是对象的模板，描述实例对象的基本结构。一个构造函数，可以生成多个实例对象，这些实例对象都有相同的结构。
var Vehicle = function () {
  this.price = 1000;
};

var ClassName=funciton(){
    this.prototype=xxx;
}
var test=new ClassName();

## js单线程
js引擎中，一个js脚本只能在一个单线程上运行

## 同步任务和异步任务
程序里面所有的任务，可以分成两类：同步任务（synchronous）和异步任务（asynchronous）。

同步任务是那些没有被引擎挂起、在主线程上排队执行的任务。只有前一个任务执行完毕，才能执行后一个任务。

异步任务是那些被引擎放在一边，不进入主线程、而进入任务队列的任务。只有引擎认为某个异步任务可以执行了（比如 Ajax 操作从服务器得到了结果），该任务（采用回调函数的形式）才会进入主线程执行。排在异步任务后面的代码，不用等待异步任务结束会马上运行，也就是说，异步任务不具有“堵塞”效应。

举例来说，Ajax 操作可以当作同步任务处理，也可以当作异步任务处理，由开发者决定。如果是同步任务，主线程就等着 Ajax 操作返回结果，再往下执行；如果是异步任务，主线程在发出 Ajax 请求以后，就直接往下执行，等到 Ajax 操作有了结果，主线程再执行对应的回调函数。

## 异步任务的调度，回调
首先，主线程会去执行所有的同步任务。等到同步任务全部执行完，就会去看任务队列里面的异步任务。如果满足条件，那么异步任务就重新进入主线程开始执行，这时它就变成同步任务了。等到执行完，下一个异步任务再进入主线程开始执行。一旦任务队列清空，程序就结束执行。

异步任务的写法通常是回调函数。一旦异步任务重新进入主线程，就会执行对应的回调函数。如果一个异步任务没有回调函数，就不会进入任务队列，也就是说，不会重新进入主线程，因为没有用回调函数指定下一步的操作。

JavaScript 引擎怎么知道异步任务有没有结果，能不能进入主线程呢？答案就是引擎在不停地检查，一遍又一遍，只要同步任务执行完了，引擎就会去检查那些挂起来的异步任务，是不是可以进入主线程了。这种循环检查的机制，就叫做事件循环（Event Loop）。维基百科的定义是：“事件循环是一个程序结构，用于等待和发送消息和事件（a programming construct that waits for and dispatches events or messages in a program）”。

## 异步的几种模式
### 回调函数

### 事件监听
https://wangdoc.com/javascript/async/general.html

https://www.sveltejs.cn/docs#Client-side_component_API

<<<<<<< HEAD

>>>>>>> e9c32ec645132bdd9b58416bb0dffdc1e0ec4ab0
