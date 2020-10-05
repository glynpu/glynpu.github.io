---
layout: post
title:  ivector/plda在kaldi中的实现
date:   2019-06-02 23:05:00 +0800
categories: kaldi
tag: kaldi
---

ivector in kaldi
---

 按照dan povey的说法，
1. kaldi 的ivector implementation is [more exact than the standard approach](https://groups.google.com/forum/#!topic/kaldi-help/h32x5hwtFUc)

2. kaldi 的ivector [采用的是non-zero mean](https://groups.google.com/forum/#!msg/kaldi-help/MhGbi5gEoM0/arJ5tXnjBwAJ)。 而标准的做法是要减去均值的

3. [lda 可以取得MLLT类似的decorrelate 的效果。虽然没有做实验验证](https://groups.google.com/forum/#!msg/kaldi-help/MhGbi5gEoM0/arJ5tXnjBwAJ)



ivector 的提取公式，还是要看最经典这一篇[Front-End Factor Analysis for Speaker Verification](http://habla.dc.uba.ar/gravano/ith-2014/presentaciones/Dehak_et_al_2010.pdf)

plda in kaldi
---
[用cholesky分解把within_var转化为I: within_var = LL^T, 所以转化矩阵采用L^-1即可]

[用特征分解bet_win的对角化：实对称矩阵的特征向量两两正交，方差矩阵肯定是实对称的，所以between_var 经过特征分解后的特征矩阵Q是正交矩阵，即Q^T 即为Q^-1, 所以可以Q^T可以把bet_wav 对角化为diag(s)]

[所以A=Q^T * L^-1]

[数据“白化”操作 Whitening transformation,把数据分布转换为MVN(0，I),即白噪声的分布](https://www.cnblogs.com/kevinGaoblog/archive/2012/06/20/2556335.html)

[kaldi plda python复现](https://github.com/vzxxbacq/PLDA/blob/master/plda.py)

[kaldi plda中文讲解，很详细 【学点Kaldi】Kaldi PLDA实现C++代码阅读](https://blog.csdn.net/Liusongxiang666/article/details/83024845)


[plda打分的计算，首先看Analysis of I-vector Length Normalization in Speaker Recognition Systems](https://pdfs.semanticscholar.org/1323/72db185b502e58765104c1465985fcab053a.pdf)

[再深一层次可以看A Straightforward and Efficient Implementation of the Factor Analysis Model for Speaker Verification](https://alize.univ-avignon.fr/doc/publis/07_Interspeech_Matrouf.pdf)

[A Note on Kaldi's PLDA Implementation](https://arxiv.org/pdf/1804.00403.pdf)

[ICCV Prince plda](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.97.6491&rep=rep1&type=pdf)

[Sizov_Unifying_Probabilistic_linear_Discriminant_Anslysis_variants_in_Biometric_Authentication](http://cs.uef.fi/~sizov/pdf/unifying_PLDA_ssspr2014.pdf)

Idiap 实验室实现了standard approach 和kaldi的ivector imp进行对比[Implementation of the Standard I-vector System for the Kaldi Speech Recognition Toolkit](https://infoscience.epfl.ch/record/223041/files/Madikeri_Idiap-RR-26-2016.pdf)

* content
{:toc}

