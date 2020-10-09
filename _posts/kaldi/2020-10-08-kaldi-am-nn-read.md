---
layout: post
title:  kaldi 神经网络的加载 
date:   2020-10-07 23:05:00 +0800
categories: kaldi
tag: kaldi
---

目录
* content
{:toc}


kaldi神经网络的加载重点在于构建components_和nodes_两个私有成员

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

下面以kaldi/src/nnet3bin/nnet3-latgen-faster.cc为例分析神经网络加载的流程：  

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

components_的构建过程
-

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

  // 以上为components_的构建过程
  // 下面为nodes_的构建过程
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

nodes_的构建过程
-

nodes_的构建过程对应的是[这一句](https://github.com/kaldi-asr/kaldi/blob/master/src/nnet3/nnet-nnet.cc#L627)
```
  this->ReadConfig(config_file_in);
```

其中config_file_in是值模型的定义，示例如下：  
```
input-node name=input dim=43
component-node name=lda component=lda input=Append(Offset(input, -1), input, Offset(input, 1))
component-node name=tdnn1.affine component=tdnn1.affine input=lda
component-node name=tdnn1.relu component=tdnn1.relu input=tdnn1.affine
component-node name=tdnn1.batchnorm component=tdnn1.batchnorm input=tdnn1.relu
component-node name=tdnn2.affine component=tdnn2.affine input=Append(Offset(tdnn1.batchnorm, -1), tdnn1.batchnorm, Offset(tdnn1.batchnorm, 1))
component-node name=tdnn2.relu component=tdnn2.relu input=tdnn2.affine
component-node name=tdnn2.batchnorm component=tdnn2.batchnorm input=tdnn2.relu
component-node name=tdnn3.affine component=tdnn3.affine input=Append(Offset(tdnn2.batchnorm, -1), tdnn2.batchnorm, Offset(tdnn2.batchnorm, 1))
component-node name=tdnn3.relu component=tdnn3.relu input=tdnn3.affine
component-node name=tdnn3.batchnorm component=tdnn3.batchnorm input=tdnn3.relu
component-node name=tdnn4.affine component=tdnn4.affine input=Append(Offset(tdnn3.batchnorm, -3), tdnn3.batchnorm, Offset(tdnn3.batchnorm, 3))
component-node name=tdnn4.relu component=tdnn4.relu input=tdnn4.affine
component-node name=tdnn4.batchnorm component=tdnn4.batchnorm input=tdnn4.relu
component-node name=tdnn5.affine component=tdnn5.affine input=Append(Offset(tdnn4.batchnorm, -3), tdnn4.batchnorm, Offset(tdnn4.batchnorm, 3))
component-node name=tdnn5.relu component=tdnn5.relu input=tdnn5.affine
component-node name=tdnn5.batchnorm component=tdnn5.batchnorm input=tdnn5.relu
component-node name=tdnn6.affine component=tdnn6.affine input=Append(Offset(tdnn5.batchnorm, -3), tdnn5.batchnorm, Offset(tdnn5.batchnorm, 3))
component-node name=tdnn6.relu component=tdnn6.relu input=tdnn6.affine
component-node name=tdnn6.batchnorm component=tdnn6.batchnorm input=tdnn6.relu
component-node name=prefinal-chain.affine component=prefinal-chain.affine input=tdnn6.batchnorm
component-node name=prefinal-chain.relu component=prefinal-chain.relu input=prefinal-chain.affine
component-node name=prefinal-chain.batchnorm component=prefinal-chain.batchnorm input=prefinal-chain.relu
component-node name=output.affine component=output.affine input=prefinal-chain.batchnorm
output-node name=output input=output.affine objective=linear
component-node name=prefinal-xent.affine component=prefinal-xent.affine input=tdnn6.batchnorm
component-node name=prefinal-xent.relu component=prefinal-xent.relu input=prefinal-xent.affine
component-node name=prefinal-xent.batchnorm component=prefinal-xent.batchnorm input=prefinal-xent.relu
component-node name=output-xent.affine component=output-xent.affine input=prefinal-xent.batchnorm
component-node name=output-xent.log-softmax component=output-xent.log-softmax input=output-xent.affine
output-node name=output-xent input=output-xent.log-softmax objective=linear

```

回忆一下，在构建components_的时候，首先resize模型文件指定的num_components, 然后在一个一个赋值。  

然而模型文件并没有指定num_nodes, 该如何判断node的个数呢？  
kaldi的解决方式是把config文件解析[两遍](https://github.com/kaldi-asr/kaldi/blob/3ce241b4ff1838d530e54b1aea9585c1493ee9f8/src/nnet3/nnet-nnet.cc#L220)(即代码中的pass分别为0 或者1的情况）
当pass为0时，由各node的类型判断需要在nodes_中预留多少个位置，以及其类型  
当pass为1时， 构建依赖关系,需要注意的是一个component-node会用占据nodes_中的两个位置，一个位置用于处理输入,类型为[kaldi::nnet3::Descriptor](https://github.com/kaldi-asr/kaldi/blob/master/src/nnet3/nnet-descriptor.h#L525)，一个位置放置参数。其中Descriptor负责处理整合input依赖关系

为什么不一趟搞定，要分pass=0 和pass = 1？  
因为config file可能不是安被依赖顺序排好的。
在配置文件中一个node的dependencies可能在其后面定义
或者一些别的原因？

如何解析input中的Append, Offset？
kaldi 中的[GeneralDescriptor::Parse](https://github.com/kaldi-asr/kaldi/blob/master/src/nnet3/nnet-descriptor.cc#L585)是一个dispatch函数,负责根据token的类型，调用相应的函数处理，又是一堆if else


nodes_中的元素类型为NetworkNode,还不是指针，就直接是对象。 为什么NetworkNode对象可以建模所有的node? 而不是想components_那样，用一个基类指针指向所有的子类对象?  
其实[NetworkNode](https://github.com/kaldi-asr/kaldi/blob/master/src/nnet3/nnet-nnet.h#L81)是一个结构体，该结构体根据构造时传入的node type 决定生成一个何种类型的node对象,[示例如下](https://github.com/kaldi-asr/kaldi/blob/3ce241b4ff1838d530e54b1aea9585c1493ee9f8/src/nnet3/nnet-nnet.cc#L303)
```
    nodes_.push_back(NetworkNode(kDescriptor));
    nodes_.push_back(NetworkNode(kComponent));
```

注意[NetworkNode]中的成员descriptor总是会初始化，无论该node是否对应descriptor类型  
```
struct NetworkNode {
  NodeType node_type;
  // "descriptor" is relevant only for nodes of type kDescriptor.
  Descriptor descriptor;
  union {
    // For kComponent, the index into Nnet::components_
    int32 component_index;
    // for kDimRange, the node-index of the input node, which must be of
    // type kComponent or kInput.
    int32 node_index;

    // for nodes of type kDescriptor that are output nodes (i.e. not followed by
    // a node of type kComponents), the objective function associated with the
    // output.  The core parts of the nnet code just ignore; it is required only
    // for the information of the calling code, which is perfectly free to
    // ignore it.  View it as a kind of annotation.
    ObjectiveType objective_type;
  } u;
```
因为c++的成员都有默认的初始化方式，如果不在构造函数中显示初始化，它们就会自动初始化。
