---
layout: post
title:  kaldi在话者分离中的应用
date:   2019-05-15 23:05:00 +0800
categories: 他山之玉 
tag: kaldi
---

kaldi 在话者分离任务中的应用
------------

随着语音生物信息识别和语音识别系统的发展，同时处理包含多说话人语音的能力变得十分关键。本文作为一篇基础教程，介绍了kaldi 中的state-of-the-art的x-vectors技术。

在大多数真实场景中，语音输入并没有严格按照说话人分段。在大多数我们的算法需要处理的对话中，人们往往会互相打断。因此分割这些语音输入并不是一个简单的任务。

在别的一些应用中，我们需要从对话中识别出多个说话人，比如会议记录的识别。在这些场景中，辨认出不同的说话人，并且将同一个人不同的语音片段联系起来变得至关重要。

[话者分离(Speaker Diarization)](https://en.wikipedia.org/wiki/Speaker_diarisation)技术为以上问题提供了解决方案。在话者分离的过程中，我们将一个输入音频按照说话人分段。针对一个输入音频，话者分离可以视为完成了“何人在何时说(who spoke when)”的任务。

第一个基于机器学习的话者分离方案诞生于2006年。但是直到2012年左右才获得了巨大进展，在当时，话者分离被视为一个特别困难的任务。当时的大多数方法基于[GMM](https://scikit-learn.org/stable/modules/mixture.html)和[HMM](https://en.wikipedia.org/wiki/Hidden_Markov_model)（[比如联合因子分析(Joint Factor Analysis, JFA)](https://www.crim.ca/perso/patrick.kenny/FAtheory.pdf)）。这些方法均没有采用神经网络。

[开源工具包LIUM](http://www-lium.univ-lemans.fr/diarization/doku.php/welcome)的发布是一个重大突破。 该工具包用java 语言开发，并且专门为话者分离而设计。该工具包是第一个能够[取得较好结果](http://ceur-ws.org/Vol-1012/papers/paper-08.pdf)同时并且免费发布的话者分离算法。LIUM工具包的核心算法是一个融合了GMM与[I-Vectors](https://link.springer.com/article/10.1007/s10772-015-9295-3)的复杂机制。I-Vectors方法在说话人识别领域取得了state-of-the-art的效果。

![LIUM框架图](/images/LIUM_framework.png)

LIUM话者分离软件框架

现在在很多领域，比如[图像分割](https://medium.com/@jonathan_hui/image-segmentation-with-mask-r-cnn-ebe6d793272)和[语音识别](http://proceedings.mlr.press/v48/amodei16.pdf)这样复杂的多算法融合的系统正在被神经网络的算法所取代。

X-Vectors
------------

最近的突破是2017年D.Snyder 等人发表的文章[“Deep Neural Network Embeddings for Text-Independent Speaker Verification”](http://danielpovey.com/files/2017_interspeech_embeddings.pdf). 该文章提出了一个后来被称为"X-Vectors"的模型。

![x_vector_model](/images/X_vectors_model.png)

该模型的输入是[MFCC特征](http://www.practicalcryptography.com/miscellaneous/machine-learning/guide-mel-frequency-cepstral-coefficients-mfccs/). 该模型的结构可以分为四部分。

1. 帧级别的层(Frame-level layers). 这些层本质上来说是[TDNN(Time Delay Neural Network)](https://en.wikipedia.org/wiki/Time_delay_neural_network). TDNN发明于上世纪90年代，即早于最近一次的神经网络大流行的浪潮。该网络结构在[2015年作为语音识别系统的一部分得到了复兴](https://www.danielpovey.com/files/2015_interspeech_multisplice.pdf)。TDNN 本质上仍然是全联接的网络结构，其特点在于使用了一个在样本时间轴上的滑动窗(sliding window)。通常该网络结构的速度要远远快于[LSTM](https://en.wikipedia.org/wiki/Long_short-term_memory) 或者[GRU](https://towardsdatascience.com/understanding-gru-networks-2ef37df6c9be).

2. 统计层(Statistics Pooling). 在帧级别的层，每一帧的输入，都会产生一个输出向量。因此我们需要综合利用这些输出向量。在该论文的中，我们通过计算这些向量的均值和标准差，然后将二者拼接为一个向量作为整个输入语音片段的表征。

3. 全联接层(Full connected layers). 统计层的输出向量被送入两层全联接层，分别有512和300个神经元。后面的一层包含非线性的ReLU模块。

4. Softmax 分类器(Softmax Classifier)。ReLU模块的输出经过一个简单的Softmax分类器，会分类至某个特定的说话人。

![tdnn_net_xvector_frame_layer_part](/images/tdnn_xvector_frame_layer.png)
TDNN网络的可视化，x-vector 模型的第一部分。

X-vectors模型的真正实力不仅仅在于识别训练集中不同的人，更在于最后两层的全联接作为整个输入的映射表征。在该论文中，作者用该映射表征对与训练集完全不匹配的测试集进行分类。分类的过程包含两步：1. 计算输入音频对应的embedding. 2. 利用[PLDA](http://www.odyssey2016.org/papers/pdfs_stamped/12.pdf)计算embedding之间的相似度。

利用X-Vectors进行话者分离
------------

综上，我们明白了全联接层的embedding 可以作为一段输入音频片段的说话人表征。接下来我们将研究如何用该说话人表征对完整音频按说话人进行分段。具体的方法参照论文["Diarization is Hard: Some Experiences and Lessons Learned for the JHUTeam in the Inaugural DIHARD Challenge]"(http://www.danielpovey.com/files/2018_interspeech_dihard.pdf). 该话者分离挑战赛难点在与包含了TV-shows, 电话以及儿童对话等10个不同的语音场景。另外，在验证集(validation set)包含了两个在训练集中没有的语音场景。

在上述论文中，作者介绍了很多方法从而使最终的话者分离系统达到了当前最好的性能。尽管这一系列方法[比如变分贝叶斯(Variational Bayes)](https://speech.fit.vutbr.cz/software/vb-diarization-eigenvoice-and-hmm-priors)的极大的提升了系统的准确率，但是系统本质上仍然是基于X-Vectors和PLDA相似度度量算法。

![tdnn_net_xvector_frame_layer_part](/images/DER_comparison_diasystems.png)
引自论文DIHARD Challenge article. 该图展示了X-Vectors带来的效果提升。蓝色框线内是初始系统。红色框线内是优化后的当前最优系统。

如何利用Kaldi实现上述系统
------------

首先，如果你以前从未用过Kaldi，可以参考[我的第一篇关于Kaldi的介绍](https://towardsdatascience.com/how-to-start-with-kaldi-and-speech-recognition-a9b7670ffff6)。没有语音处理知识的话，还是很难掌握Kaldi系统的。

其次，不必重新训练X-Vectors网络以及PLDA所需的参数。用户可以从[官网](http://kaldi-asr.org/models/m3)上下载已经训练好的模型。如果你特别想从头开始训练，可以按照kaldi示例中的[call_home_v2_recipe](https://github.com/kaldi-asr/kaldi/blob/master/egs/callhome_diarization/v2/run.sh)进行训练。

假设现在你已经获得了模型，无论是直接下载的还是自己从头训练的，接下来我会介绍如何利用这些模型实现话者分离。该步骤主要是从[David](https://github.com/kaldi-asr/kaldi/issues/2523#issuecomment-408935477)在github上的注释以及其他的一些相关文档整理而成。

数据准备
------------

首先你要按照该[自动语音识别的标准](http://kaldi-asr.org/doc/data_prep.html)准备wav.scp 和 segments 两个文档。如果你想快速创建这些文档，可以使用[compute_vad_decision.sh](https://github.com/kaldi-asr/kaldi/blob/master/egs/wsj/s5/steps/compute_vad_decision.sh)和[vad_to_segments.sh](https://github.com/kaldi-asr/kaldi/blob/master/egs/wsj/s5/steps/compute_vad_decision.sh)这两个脚本。如果你不想切分你的音频文件，只需要建立segments到各音频的映射就可以了。

然后，你需要创建utt2spk这个文件，该文件建立了segments 到所在音频文件的映射。你可以用下面的shell指令生成这个文件。
```
awk '{print $1, $2}' segments > utt2spk
```
接下来，为了生成别的相关文件，只需将wav.scp/segments/utt2spk 放入同一个文件夹，然后执行脚本fix_data_dir.sh; 其语法是
```
fix_data_dir.sh /path/to/target/folder/
```

特征提取
------------
接下来需要提取计算X-Vectors 所需的音频特征。

我们按照自动语音识别的方法计算所需的MFCC和CMVN。提取特征需要mfcc.conf配置文件，该配置文件应该和你训练模型时所用的一致。如果你用的是从官网上直接下载的模型，可以从[官网上下载相应的配置文件](https://github.com/kaldi-asr/kaldi/tree/master/egs/callhome_diarization/v2/conf).

执行下面命令提取MFCC特征：
```
steps/make_mfcc.sh --mfcc-config conf/mfcc.conf --nj 60 \
--cmd "$train_cmd_intel" --write-utt2num-frames true \
$data_dir exp/make_mfcc $mfccdir
```
然后执行下面命令计算CMVN：
```
local/nnet3/xvector/prepare_feats.sh — nj 60 — cmd \ "$train_cmd_intel" $data_dir $cmn_dir $cmn_dir
```
数据生成结束后，执行``` utils/fix_data_dir.sh $data_dir ```修复各文件潜在的错误。然后将segments文件复制到CMVN文件夹```cp $data_dir/segments $cmn_dir/```，并且修复该文件夹下潜在的错误```utils/fix_data_dir.sh $cmn_dir```。


提取X-Vectors
------------
接下来针对你的数据提取X-vectors. 下文将你从官网上下载的模型路径定义为变量$nnet_dir， 即其指向exp/xvectors_sre_combined所在的文件夹。执行下面的命令
```
diarization/nnet3/xvector/extract_xvectors.sh --cmd \ "$train_cmd_intel --mem 5G" \
--nj 60 --window 1.5 --period 0.75 --apply-cmn false \
--min-segment 0.5 $nnet_dir \
$cmn_dir $nnet_dir/exp/xvectors
```
在该例中，我们使用了1.5秒的窗长和0.75秒的窗移。降低窗移或许能获得更细节的信息。

对X-Vectors采用PLDA打分
------------
现在你要利用PLDA对提取的X-Vectors逐对打分。执行下面的命令：
```
diarization/nnet3/xvector/score_plda.sh \
--cmd "$train_cmd_intel --mem 4G" \
--target-energy 0.9 --nj 20 $nnet_dir/xvectors_sre_combined/ \
$nnet_dir/xvectors $nnet_dir/xvectors/plda_scores
```

话者分离
------------
最后一步是对PLDA的分值进行聚类。幸运的是有专门的脚本完成该步骤。但是，针对该聚类你有两个方案可以选择1. 有监督的聚类；2.无监督的聚类。

在有监督的聚类方案中，你需要指定在每个输入音频文件中各有几个说话人。如果处理对象已知，该信息很容易获得，比如在电话场景中，往往只有两个人；在会议场景中，参会对象往往是事前指定的。如果各输入文件中的说话人数目已知，我们可以将该信息存储在reco2num_spk文件中，该文件存储了wav.scp中各音频文件中包含的说话人个数，格式为：
```
rec1 2
rec2 2
rec3 3
rec4 1
```
需要注意的，该文件是说话人整个音频文件包含说话人数目的映射，而不是某个片段包含的说话人数目。在创建reco2num_spk文件后，执行下面的命令：
```
diarization/cluster.sh --cmd "$train_cmd_intel --mem 4G" --nj 20 \
--reco2num-spk $data_dir/reco2num_spk \
$nnet_dir/xvectors/plda_scores \
$nnet_dir/xvectors/plda_scores_speakers
```

如果各音频包含说话人数目未知，你可以采用无监督的方案进行聚类。在无监督的聚类方案中，为了获得较好的结果，你需要不断调整脚本中所用的阈值。一个较好的初值是0.5。执行下面的命令进行无监督的聚类。

```
diarization/cluster.sh --cmd "$train_cmd_intel --mem 4G" --nj 40 \
--threshold $threshold \
$nnet_dir/xvectors/plda_scores \
$nnet_dir/xvectors/plda_scores_speakers
```

输出结果
------------
在聚类完成之后，输出的rttm格式文件存储在$nnet_dir/xvectors/plda_scores_speakers 文件夹中， 该文件的具体格式为：
```
SPEAKER rec1 0 86.200 16.400 <NA> <NA> 1 <NA> <NA>`
SPEAKER rec1 0 103.050 5.830 <NA> <NA> 1 <NA> <NA>`
SPEAKER rec1 0 109.230 4.270 <NA> <NA> 1 <NA> <NA>`
SPEAKER rec1 0 113.760 8.625 <NA> <NA> 1 <NA> <NA>`
SPEAKER rec2 0 122.385 4.525 <NA> <NA> 2 <NA> <NA>`
SPEAKER rec2 0 127.230 6.230 <NA> <NA> 2 <NA> <NA>`
SPEAKER rec2 0 133.820 0.850 <NA> <NA> 2 <NA> <NA>`
```
该文件的第2列是wav.scp文件中存储的recording-id;第4列是每个片段的开始时间；第5列是相应片段的持续时间，第8列是各片段对应的speaker-id。

到此为止，我们完成了整个说话人聚类的过程。接下来我们可以调用语音识别的系统来分析各个说话人的预料内容。或者调用说话人识别的系统来识别各个说话人的身份。

原作者整理了一些kaldi相关的资料链接：[kaldi awesome tools](https://github.com/YoavRamon/awesome-kaldi)


[原文链接](https://towardsdatascience.com/speaker-diarization-with-kaldi-e30301b05cc8)



* content
{:toc}

