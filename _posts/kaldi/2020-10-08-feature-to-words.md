---
layout: post
title:  kaldi 特征到文字的转换过程
date:   2019-05-21 23:05:00 +0800
categories: kaldi
tag: kaldi
---

fbank/mfcc feature 到最终生成文字主要有三大模块在起作用
1. acoustic model(am) 声学模型
2. language modle(lm) 语言模型
3. decoder 解码器


下面以kaldi/src/nnet3bin/nnet3-latgen-faster.cc为例分析asr的流程：  
其总体框架为tdnn am  +  fst lm + lattice-faster-decoder


[加载am nnet](https://github.com/kaldi-asr/kaldi/blob/master/src/nnet3bin/nnet3-latgen-faster.cc#L99)  
```
    TransitionModel trans_model;
    AmNnetSimple am_nnet;
    {
      bool binary;
      Input ki(model_in_filename, &binary);
      trans_model.Read(ki.Stream(), binary);
	  // 这个函数读入模型，重点在于为components_和nodes_赋值
      am_nnet.Read(ki.Stream(), binary);
      SetBatchnormTestMode(true, &(am_nnet.GetNnet()));
      SetDropoutTestMode(true, &(am_nnet.GetNnet()));
      CollapseModel(CollapseModelConfig(), &(am_nnet.GetNnet()));
    }
```

[kaldi::nnet3::Nnet部分成员变量，这些成员变量都是在Read函数执行过程中赋值](https://github.com/kaldi-asr/kaldi/blob/master/src/nnet3/nnet-nnet.h#L333)

```
  // the names of the components of the network.  Note, these may be distinct
  // from the network node names below (and live in a different namespace); the
  // same component may be used in multiple network nodes, to define parameter
  // sharing.
  std::vector<std::string> component_names_;

  // the components of the nnet, in arbitrary order.  The network topology is
  // defined separately, below; a given Component may appear more than once in
  // the network if necessary for parameter tying.
  // 注意components_是Component*的vector, 即其中每一个成员都是一个指针
  // 该指针指向一个Component
  // 问： 为什么一个网络的所有component都用Component指针去指向, 难道它们都是一个类型？(解释见下文)
  std::vector<Component*> components_;

  // names of network nodes, i.e. inputs, components and outputs, used only in
  // reading and writing code.  Indexed by network-node index.  Note,
  // components' names are always listed twice, once as foo-input and once as
  // foo, because the input to a component always gets its own NetworkNode index.
  std::vector<std::string> node_names_;

  // the network nodes of the network.
  std::vector<NetworkNode> nodes_;


```


[am_nnet.Read函数实现](https://github.com/kaldi-asr/kaldi/blob/3ce241b4ff1838d530e54b1aea9585c1493ee9f8/src/nnet3/nnet-nnet.cc#L586)  
```
  // Now we read the Components; later we try to parse the config_lines.
  ExpectToken(is, binary, "<NumComponents>");
  int32 num_components;
  // 欲载入的模型的componnet的数目是在文件中直接指明的，
  // 所以components_可以直接resize到目标大小, 即留够num_components个位置
  ReadBasicType(is, binary, &num_components);
  KALDI_ASSERT(num_components >= 0 && num_components < 100000);
  components_.resize(num_components, NULL);
  component_names_.resize(num_components);
  for (int32 c = 0; c < num_components; c++) {
    ExpectToken(is, binary, "<ComponentName>");
    ReadToken(is, binary, &(component_names_[c]));
	// 问： 每一个componet的加载方式不同，比如affine component 的参数和batchnorm component完全不同，为什么Component::ReadNew函数总是能够找到合适的加载方式？
    components_[c] = Component::ReadNew(is, binary);
  }
  ExpectToken(is, binary, "</Nnet3>");
  std::istringstream config_file_in(config_file_out.str());
  this->ReadConfig(config_file_in);

```






// 问： 为什么一个网络的所有component都用Component指针去指向, 难道它们都是一个类型？(解释见下文)  
// 问： 每一个componet的加载方式不同，比如affine component 的参数和batchnorm component完全不同，为什么Component::ReadNew函数总是能够找到合适的加载方式？  

解： Component 类是RestrictedAttentionComponent StatisticsExtractionComponent 等其他人所有componet的基类，基类的指针可以指向所有子类的对象.  
[Component::ReadNew](https://github.com/kaldi-asr/kaldi/blob/master/src/nnet3/nnet-component-itf.cc#L84)函数首先确定componet的类别(代码中的token), 再调用[Component::NewComponentOfType](https://github.com/kaldi-asr/kaldi/blob/master/src/nnet3/nnet-component-itf.cc#L98)定义具体的子类对象. 其中NewComponentOfType是一个dispatch 函数， 写一串 if else 判断token的值，进而生成对应类型的对象  

[Component::ReadNew函数](https://github.com/kaldi-asr/kaldi/blob/master/src/nnet3/nnet-component-itf.cc#L84)  

```
// static
Component* Component::ReadNew(std::istream &is, bool binary) {
  // 解析当前component的类型，赋值给token
  std::string token;
  ReadToken(is, binary, &token); // e.g. "<SigmoidComponent>".
  token.erase(0, 1); // erase "<".
  token.erase(token.length()-1); // erase ">".
  // 根据token的值定义具体的子类component对像，并复制给基类Component的指针ans
  Component *ans = NewComponentOfType(token);
  if (!ans)
    KALDI_ERR << "Unknown component type " << token;
  // 由基类指针ans 调用子类的Read函数，不出意外的化，该Read函数一定是一个虚函数
  ans->Read(is, binary);
  return ans;
}
```

[正如预料Component::Read函数确实是一个虚函数](https://github.com/kaldi-asr/kaldi/blob/master/src/nnet3/nnet-component-itf.h#L628)  
```
  /// We implement Read at this level as it just needs the Type().
  virtual void Read(std::istream &is, bool binary);
```

* content
{:toc}

