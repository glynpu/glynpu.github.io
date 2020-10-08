---
layout: post
title: am-nnet-simple笔记
date:   2020-10-06 14:05:00 +0800
categories: kaldi
tag: kaldi
---

* content
{:toc}

1. kaldi是如何判断读入的文件是binary还是txt格式的?  
   通过peek第一个字符是'\0'还是'B', [代码实现](https://github.com/kaldi-asr/kaldi/blob/bcd163c5ae45a9dcc488c86e98281649b8156529/src/base/io-funcs-inl.h#L306:1)  
   [调用示例](https://github.com/kaldi-asr/kaldi/blob/master/src/util/kaldi-io.cc#L817)其中contents_binary是一个bool指针，InitKaldiInputStream判断文件类型后，通过contents_binary指针把结果传递出来.

2. parse config line 每个input descriptor的处理  
   [逐行解析configline](https://github.com/kaldi-asr/kaldi/blob/bcd163c5ae45a9dcc488c86e98281649b8156529/src/nnet3/nnet-nnet.cc#L331)  
   [Descriptor::Parse函数](https://github.com/kaldi-asr/kaldi/blob/bcd163c5ae45a9dcc488c86e98281649b8156529/src/nnet3/nnet-descriptor.cc#L491)
   [调用示例](https://github.com/kaldi-asr/kaldi/blob/bcd163c5ae45a9dcc488c86e98281649b8156529/src/nnet3/nnet-nnet.cc#L331)
   解析后的descriptor在函数内部new 一个[GeneralDescriptor](https://github.com/kaldi-asr/kaldi/blob/bcd163c5ae45a9dcc488c86e98281649b8156529/src/nnet3/nnet-descriptor.cc#L626)
   返回该object的指针。（函数内部 new的object不会随着函数的结束而释放，需要自己手动delete）  
   [移动赋值构造函数](https://github.com/kaldi-asr/kaldi/blob/bcd163c5ae45a9dcc488c86e98281649b8156529/src/nnet3/nnet-descriptor.cc#L504)
   mutual recursive [GeneralDescriptor::Parse](https://github.com/kaldi-asr/kaldi/blob/bcd163c5ae45a9dcc488c86e98281649b8156529/src/nnet3/nnet-descriptor.cc#L585)和其余众多的[GeneralDescriptor::Parse*](https://github.com/kaldi-asr/kaldi/blob/bcd163c5ae45a9dcc488c86e98281649b8156529/src/nnet3/nnet-descriptor.cc#L713)
   
3. [kaldi::nnet3::Nnet](https://github.com/kaldi-asr/kaldi/blob/bcd163c5ae45a9dcc488c86e98281649b8156529/src/nnet3/nnet-nnet.h#L115)中四个私有属性：  
   std::vector<std::string> component_names_; // 各component的名字  
   std::vector<Component*> components_; // 各component, 对应权重参数,因为所有component都来自于同一基类，所以它们的指针转换为父类指针后可以放在同一个vector里  

   std::vector<std::string> node_names_;  //各node的名字
   std::vector<NetworkNode> nodes_; // 各node, 对应网络拓扑结构

4. 解析完成后[Descriptor的构造函数](https://github.com/kaldi-asr/kaldi/blob/master/src/nnet3/nnet-descriptor.h#L593)判断究竟有多少个dependencies
   [Descriptor的赋值构造函数][https://github.com/kaldi-asr/kaldi/blob/master/src/nnet3/nnet-descriptor.cc#L544]


5. [Nnet::Check检测网络validation](https://github.com/kaldi-asr/kaldi/blob/master/src/nnet3/nnet-nnet.cc#L694)
	[SortAndUniq](https://github.com/kaldi-asr/kaldi/blob/bcd163c5ae45a9dcc488c86e98281649b8156529/src/nnet3/nnet-nnet.cc#L713)  
   
6. [模型的collapse](https://github.com/kaldi-asr/kaldi/blob/master/src/nnet3/nnet-utils.cc#L1468)  
   [调用处](https://github.com/kaldi-asr/kaldi/blob/bcd163c5ae45a9dcc488c86e98281649b8156529/src/nnet3bin/nnet3-latgen-faster.cc#L102) --> [collapse 函数](https://github.com/kaldi-asr/kaldi/blob/bcd163c5ae45a9dcc488c86e98281649b8156529/src/nnet3/nnet-utils.cc#L2116:1)

7. 前向运算 Nnet --> [CachingOptimizingCompiler](https://github.com/kaldi-asr/kaldi/blob/bcd163c5ae45a9dcc488c86e98281649b8156529/src/nnet3bin/nnet3-latgen-faster.cc#L132) --> [DecodableAmNnetSimple](https://github.com/kaldi-asr/kaldi/blob/bcd163c5ae45a9dcc488c86e98281649b8156529/src/nnet3bin/nnet3-latgen-faster.cc#L174)

8. DecodableAmNnetSimple	--> CachingOptimizingCompiler 
							--> DecodableNnetSimple
