---
layout: post
title:  详解CNN系列
date:   2019-05-16 23:05:00 +0800
categories: 他山之玉
tag: cnn
---

实现卷积神经网络
------------

通过该系列博客，你将链接卷积神经网络的概念及其背后的数学基础，同时使用Python和Numpy 实现一个你自己的CNN. 完整的代码见[此github项目](https://github.com/parasdahal/deepnet)。

[卷积神经网络的介绍](https://deepnotes.io/intro)
----------

![cnn_jpg](/images/cnn_introduction/cnn.jpg)

卷积神经网络在计算机视觉领域带来了革命性的巨变；在围棋领域击败了世界冠军以及使得深度学习成为现实。接下来我们一起分析这些神奇的DNN背后的核心概念:局部感受野(Local Receptive Fields)，共享权重(shared Weights)，池化(Pooling)以及线性整流函数(Rectified Linear Unit, ReLU; 又称修正线性单元)。

[卷积层:卷积神经网络背后的核心概念](https://deepnotes.io/convlayer)
------------

![](/images/cnn_introduction/conv.png)

卷积神经网络的特殊之处当然在于卷机层。其灵感来自于动物的视觉皮层的工作机制，这写卷积层的特征提取过程独立于其在图像中所处的位置。让我们一起来推导其背后的数学原理并一起实现我们自己的卷积层。

[最大池化层：综合分析卷积层的输出](https://deepnotes.io/maxpool)
------------

![](/images/cnn_introduction/maxpool.jpg)

池化层是卷积神经网络的重要构件模块。它们负责综合分析激活图(activation maps)同时保证网络参数维持在较低的数量级。来, 实现最大池化层!

[批标准化层(BatchNorm Layer): 理解并消除内部协变量转移(Internal Covariance Shift)](https://deepnotes.io/batchnorm)
------------

![](/images/cnn_introduction/bn.png)

Batch Normalizatioin 是一项新的技术，该技术让我们能够轻松的初始化网络，使用更高的学习率以及训练深度网络结构。非常令人振奋！让我们一步步手动推导前向后向过程(forward and backward pass)并且实现BatchNorm layer层。

[Dropout层： 新奇的正则化(regularization)技巧](https://deepnotes.io/dropout)
----------

![](/images/cnn_introduction/dropout.jpeg)

过拟合(Overfitting)一直是[泛化过程](generalization)的敌人。Dropout是一种简单而有效的正则化技巧。它见小了神经元之间的互相适应(co-adaptation)。 更多讨论和实现方式见下文。

[分类和损失估计：Softmax和交叉熵损失函数](https://deepnotes.io/softmax-crossentropy)
------------

![](/images/cnn_introduction/softmax.png)

让我们深入一点研究如何用Softmax将CNN的输入转化为概率.同时采用交叉熵(Cross Entropy)这一损失度量来引导优化过程。

[求解模型：随机梯度优化(SGD)，动量(Momentum)和适应性学习率(Adaptive Learning Rate)](https://deepnotes.io/sgd-momentum-adaptive)
------------

![](/images/cnn_introduction/sgd.gif)

由于积极的研究，除了默认的梯度下降算法(vanilla Gradient Descent),我们已经有了格式各样的最优化方法。我们将会另外两种不同的梯度下降方法：动量法(Momentum)和适应性学习率(Adaptive Learning Rate)。

[组装各模块并且对MNIST数据集分类](https://deepnotes.io/classify-mnist)
------------
![](/images/cnn_introduction/mnist-cnn.jpg)

接下来是见证奇迹的时刻！组装各网络层，拿出模型训练器使用广为流行的MNISt数据集训练我们从头实现的CNN。感觉自己棒棒哒！

[原文链接](https://deepnotes.io/implementing-cnn)

* content
{:toc}

