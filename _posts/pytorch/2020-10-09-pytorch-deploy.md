---
layout: post
title: pytorch 模型的部署
date:   2020-10-07 23:05:00 +0800
<!-- categories: 他山之玉 -->
tag: c++
---

1. jit 是什么？  
	  [just in time, jit](https://en.wikipedia.org/wiki/Just-in-time_compilation) 是一种编程思想。  
  In Computing, Just-in-time(JIT) compilation (also dynamic translation or run-time compilations) is a way of executing computer code that involves compilation during execution of a program - at run time - rather than before execution.

2. 把模型定义看作是一种程序而不仅仅只是数据结构。  
	pytorch的Module包含模型参数和forward函数，该函数内部包含的当然是程序

3. torchscript 是一种语言，是python 语言的子集。可以从三个方面理解“子集”概念  
	a. 不是所有的python语言的模块在torchscript中都有定义，子集嘛，只有一部  
	b. torchscript可以用python 的解析器，也有自己独立的解析器  
	c. torchscript 可以用别的语言加载，只要该语言中能成功调用trochscript的解析器模块  
	(类似starlark也是python 的改造版语言)  
	(tensorflow 与其说是python 语言，不如说是一套新的语言)  
	(pytorch 语言和python 语言无缝兼容，以至于大家往往意识不到pytorch语言的存在)  

4. libtorch是一个库，毕竟名字里都带lib了，c++调用了这个库就可以调用torchscript的解释器，就能够解析torchscript程序（注意神经网络模型也可以看作是一种程序）,或者说加载了神经网络模型


5. [巨坑爹的view_as](https://github.com/espnet/espnet/blob/20b0c89369d9dd3e05780b65fdd00a9b4f4891e5/espnet/nets/pytorch_backend/transformer/attention.py#L156)
