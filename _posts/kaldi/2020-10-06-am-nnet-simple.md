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
