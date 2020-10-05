---
layout: post
title:  nnet3 xconfig 文件生成configs文件
date:   2019-07-08 23:05:00 +0800
categories: kaldi
tag: kaldi
---

1. steps/nnet3/xconfig_to_configs.py --xconfig-file --existing-model --config-dir --nnet-edits
   --existing-model可以用来做tranfer_learning
   
2. steps/libs/nnet3/xconfig/parser.py
   其中的config_to_layer dict 实现了xconfig-line 对应的转化函数，采用的技巧是：
   [Using a dict let you translate the key into a callable.](https://softwareengineering.stackexchange.com/questions/182093/why-store-a-function-inside-a-python-dictionary/182095)
   该技巧常被用于”同类函数的重载“ 。 比如kaldi model转化为tf pb的converter 过程中，也用到了该技巧。
   ptyhon dict with callables 更高级的技巧，可以参考[该处讨论](https://stackoverflow.com/questions/14610346/how-can-i-process-a-python-dictionary-with-callables)
   
3. steps/libs/nnet3/xoncifg/utils.py
   其中的parse_config_line函数解析出first_token，以及相应层的配置信息

4. steps/libs/nnet3/xconfig/layers.py 
   把所有的layers 都合并到一个出口文件，方便外部调用

5. steps/libs/nnet3/xconfig/{basic_layers, convolution, attention, lstm, gru, stats_layer, trivial_layers, composite_layers}
   kaldi nnet3 所能支持的所有网络结构

6. steps/libs/nnet3/xconfig/basic_layers
   各网络结构的基类


* content
{:toc}

