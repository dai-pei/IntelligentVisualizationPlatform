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

