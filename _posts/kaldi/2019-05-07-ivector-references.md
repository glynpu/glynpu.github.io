---
layout: post
title:  ivector 参考文献
date:   2019-05-07 14:05:00 +0800
categories: kaldi
tag: kaldi
---

* content
{:toc}



微软声纹识别工具包，mtalab 版本  
[MSR identity toolbox](https://www.microsoft.com/en-us/research/wp-content/uploads/2013/09/MSR-Identity-Toolbox-v1_1.pdf)  


[GMM-UBM](http://statweb.stanford.edu/~tibs/stat315a/LECTURES/em.pdf)   
[Another tutorial](http://www.ee.bgu.ac.il/~haimp/ml/lectures/lec2/lec2.pdf)

GMM看成软分类的knn：
a soft version of k-means: EM algorithm for Gaussian mixture model

UBM到GMM的adaption 和UBM训练过程用到的EM本质思想是一样的，只不过UBM用的是全部数据，adaptation用的是target speaker 数据

EM for UBM 
![](https://github.com/glynpu/voiceprint_review/blob/master/jpeg/EM_for_GMM.png)


[Speaker verification using adapted Gaussian mixture models](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.117.338&rep=rep1&type=pdf)

The specifics of the adaptation are as follows. Given a UBM and training vectors from the hypothesized speakers, <a href="https://www.codecogs.com/eqnedit.php?latex=X&space;=&space;\left&space;\{&space;{x_{1},&space;...,&space;x_{T}}&space;\right&space;\}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?X&space;=&space;\left&space;\{&space;{x_{1},&space;...,&space;x_{T}}&space;\right&space;\}" title="X = \left \{ {x_{1}, ..., x_{T}} \right \}" /></a>
we first determine the probabilistic alignment of the training vectors into the UBM mixture components. That is, for mixture i in the UBM, we compute  

<a href="https://www.codecogs.com/eqnedit.php?latex=Pr(i|x_{t})&space;=&space;\frac{w_{i}p_{i}(x_{t})}{\Sigma^{M}_{j=1}w_{j}p_{j}(x_{t})}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?Pr(i|x_{t})&space;=&space;\frac{w_{i}p_{i}(x_{t})}{\Sigma^{M}_{j=1}w_{j}p_{j}(x_{t})}" title="Pr(i|x_{t}) = \frac{w_{i}p_{i}(x_{t})}{\Sigma^{M}_{j=1}w_{j}p_{j}(x_{t})}" /></a>

We then use <a href="https://www.codecogs.com/eqnedit.php?latex=Pr(i|x_{t})" target="_blank"><img src="https://latex.codecogs.com/gif.latex?Pr(i|x_{t})" title="Pr(i|x_{t})" /></a> and <a href="https://www.codecogs.com/eqnedit.php?latex=x_{t}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?x_{t}" title="x_{t}" /></a>
to compute the sufficient statistics for the weight, mean and variance parameters.  

<a href="https://www.codecogs.com/eqnedit.php?latex=n_{i}&space;=&space;\Sigma^{T}_{t=1}Pr(i|x_{t}))" target="_blank"><img src="https://latex.codecogs.com/gif.latex?n_{i}&space;=&space;\Sigma^{T}_{t=1}Pr(i|x_{t}))" title="n_{i} = \Sigma^{T}_{t=1}Pr(i|x_{t}))" /></a>


<a href="https://www.codecogs.com/eqnedit.php?latex=E_{i}(x)&space;=&space;\frac{1}{n_{i}}\Sigma^{T}_{t=1}Pr(i|x_{t})x_{t}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?E_{i}(x)&space;=&space;\frac{1}{n_{i}}\Sigma^{T}_{t=1}Pr(i|x_{t})x_{t}" title="E_{i}(x) = \frac{1}{n_{i}}\Sigma^{T}_{t=1}Pr(i|x_{t})x_{t}" /></a>


<a href="https://www.codecogs.com/eqnedit.php?latex=E_{i}(x^2)&space;=&space;\frac{1}{n_i}\Sigma^{T}_{t=1}Pr(i|x_t)x^{2}_t" target="_blank"><img src="https://latex.codecogs.com/gif.latex?E_{i}(x^2)&space;=&space;\frac{1}{n_i}\Sigma^{T}_{t=1}Pr(i|x_t)x^{2}_t" title="E_{i}(x^2) = \frac{1}{n_i}\Sigma^{T}_{t=1}Pr(i|x_t)x^{2}_t" /></a>


Finally, these new sufficient statistics form the training data are used to update the old UBM sufficient statistics for mixture i to create the adapted 
parameters for mixture i with the equations:


<a href="https://www.codecogs.com/eqnedit.php?latex=\hat{w_i}&space;=&space;[\alpha^w_in_i/T&space;&plus;&space;(1-\alpha^w_i)w_i&space;]&space;\gamma&space;\\&space;\hat{u_i}&space;=&space;\alpha^m_i&space;E_i(x)&space;&plus;&space;(1&space;-&space;\alpha^m_i)\mu_i&space;\\&space;\hat{\sigma}^2_i&space;=&space;\alpha^v_iE_i(x^2)&space;&plus;&space;(1-\alpha^v_i)&space;(&space;\sigma^2_i&space;&plus;&space;\mu_i^2)&space;-&space;\hat{mu}^2_i" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\hat{w_i}&space;=&space;[\alpha^w_in_i/T&space;&plus;&space;(1-\alpha^w_i)w_i&space;]&space;\gamma&space;\\&space;\hat{u_i}&space;=&space;\alpha^m_i&space;E_i(x)&space;&plus;&space;(1&space;-&space;\alpha^m_i)\mu_i&space;\\&space;\hat{\sigma}^2_i&space;=&space;\alpha^v_iE_i(x^2)&space;&plus;&space;(1-\alpha^v_i)&space;(&space;\sigma^2_i&space;&plus;&space;\mu_i^2)&space;-&space;\hat{mu}^2_i" title="\hat{w_i} = [\alpha^w_in_i/T + (1-\alpha^w_i)w_i ] \gamma \\ \hat{u_i} = \alpha^m_i E_i(x) + (1 - \alpha^m_i)\mu_i \\ \hat{\sigma}^2_i = \alpha^v_iE_i(x^2) + (1-\alpha^v_i) ( \sigma^2_i + \mu_i^2) - \hat{mu}^2_i" /></a>


i-vector 公式总结：
1. 认为均值超矢量包含两部分factors: speaker + channel  
<a href="https://www.codecogs.com/eqnedit.php?latex=M&space;=&space;s&space;&plus;&space;c" target="_blank"><img src="https://latex.codecogs.com/gif.latex?M&space;=&space;s&space;&plus;&space;c" title="M = s + c" /></a>  
    进一步分解为：  
<a href="https://www.codecogs.com/eqnedit.php?latex=\begin{align*}&space;M&space;&=&space;s&space;&plus;&space;c&space;\\&space;&=&space;m&space;&plus;&space;vy&space;&plus;&space;dz&space;&plus;&space;ux\\&space;&=&space;c&space;&plus;&space;s&space;\\&space;&=&space;ux&space;&plus;&space;m&space;&plus;&space;vy&space;&plus;&space;dz&space;\end{align*}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\begin{align*}&space;M&space;&=&space;s&space;&plus;&space;c&space;\\&space;&=&space;m&space;&plus;&space;vy&space;&plus;&space;dz&space;&plus;&space;ux\\&space;&=&space;c&space;&plus;&space;s&space;\\&space;&=&space;ux&space;&plus;&space;m&space;&plus;&space;vy&space;&plus;&space;dz&space;\end{align*}" title="\begin{align*} M &= s + c \\ &= m + vy + dz + ux\\ &= c + s \\ &= ux + m + vy + dz \end{align*}" /></a>

    In the new model, we make no distinction between speaker effects and the channel effects in GMM supervector space  
<a href="https://www.codecogs.com/eqnedit.php?latex=M&space;=&space;m&space;&plus;&space;Tw" target="_blank"><img src="https://latex.codecogs.com/gif.latex?M&space;=&space;m&space;&plus;&space;Tw" title="M = m + Tw" /></a>

如何训练i-vector extractor 的文章  
[A straightforward and Efficient Implementation of the Factor Analysis Model for Speaker Verification](https://alize.univ-avignon.fr/doc/publis/07_Interspeech_Matrouf.pdf)

[Front-End Factor Analysis for Speaker Verification](http://habla.dc.uba.ar/gravano/ith-2014/presentaciones/Dehak_et_al_2010.pdf)

[Eigenvoice Modeling With Sparse Training Data](https://www.crim.ca/perso/patrick.kenny/eigenvoices.PDF)

[A Small Footprint i-Vector Extractor](https://www.crim.ca/perso/patrick.kenny/kenny_odyssey2012.pdf)




[A Study of Inter-Speaker Variability in Speaker Verification](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.494.6825&rep=rep1&type=pdf)
总结： 如何估计 v矩阵 和 d 对角阵  
Our concern in this article is with the way the hyperparameters v and d are estimated 
Abstract of Abstract:

hyperparameters are T U Z   
    <a href="https://www.codecogs.com/eqnedit.php?latex=M&space;=&space;s&space;&plus;&space;c" target="_blank"><img src="https://latex.codecogs.com/gif.latex?M&space;=&space;s&space;&plus;&space;c" title="M = s + c" /></a>
    
    S is short for Speaker
    c is short for channel
  <a href="https://www.codecogs.com/eqnedit.php?latex=s&space;=&space;m&space;&plus;&space;Vy&space;&plus;&space;Dz" target="_blank"><img src="https://latex.codecogs.com/gif.latex?s&space;=&space;m&space;&plus;&space;Vy&space;&plus;&space;Dz" title="s = m + Vy + Dz" /></a>

    D is short for Diagnoal   
    V is a rectangular matrix

<a href="https://www.codecogs.com/eqnedit.php?latex=c&space;=&space;ux" target="_blank"><img src="https://latex.codecogs.com/gif.latex?c&space;=&space;ux" title="c = ux" /></a>

so   
<a href="https://www.codecogs.com/eqnedit.php?latex=\begin{align*}&space;M&space;&=&space;s&space;&plus;&space;c&space;\\&space;&=&space;m&space;&plus;&space;vy&space;&plus;&space;dz&space;&plus;&space;ux\\&space;&=&space;c&space;&plus;&space;s&space;\\&space;&=&space;ux&space;&plus;&space;m&space;&plus;&space;vy&space;&plus;&space;dz&space;\end{align*}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\begin{align*}&space;M&space;&=&space;s&space;&plus;&space;c&space;\\&space;&=&space;m&space;&plus;&space;vy&space;&plus;&space;dz&space;&plus;&space;ux\\&space;&=&space;c&space;&plus;&space;s&space;\\&space;&=&space;ux&space;&plus;&space;m&space;&plus;&space;vy&space;&plus;&space;dz&space;\end{align*}" title="\begin{align*} M &= s + c \\ &= m + vy + dz + ux\\ &= c + s \\ &= ux + m + vy + dz \end{align*}" /></a>

    F is short for feature vectors
    C is short Components in a Universal Backgroud Model(UBM)
    supervector: CF-dimensional vector obtained by concatenating the F-dimensional mean vectors in the GMM corresponding to a given utterance
 

PHD thesis [Discriminative and generative approches for long- and short-term speaker characteristics modeling: Application to speaker verification](http://espace.etsmtl.ca/33/1/DEHAK_Najim.pdf)
这个工作使JFA 转向 i-vector 

[Joint Factor Analysis versus Eigenchannels in Speaker Recognition](https://www.crim.ca/perso/patrick.kenny/FASysJ.pdf)


JFA ["Comparison of Scoring methods used in speaker recognition with joint factor analysis"](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.535.8896&rep=rep1&type=pdf)
Published in 2009

1. Each speaker is represented by means, convariance, and weights of a mixture of C multivariate Gaussian densities defined in some continuous feature space of dimension F
2. GMM is adapted from the Universal Backgournd Model(UBM) mean parameters.
3. In Jonint Factor Analysis, the basic assumption is that a speaker- and channel- dependent supervector of means M can be decomposed into a sum of two supervectors: a speaker supervector s and a channel supervector c
 
     <a href="https://www.codecogs.com/eqnedit.php?latex=M&space;=&space;s&space;&plus;&space;c" target="_blank"><img src="https://latex.codecogs.com/gif.latex?M&space;=&space;s&space;&plus;&space;c" title="M = s + c" /></a>

4. the speaker supervector s can further decomposed of 

    <a href="https://www.codecogs.com/eqnedit.php?latex=s&space;=&space;m&space;&plus;&space;Vy&space;&plus;&space;Dz" target="_blank"><img src="https://latex.codecogs.com/gif.latex?s&space;=&space;m&space;&plus;&space;Vy&space;&plus;&space;Dz" title="s = m + Vy + Dz" /></a>

    m is the speaker and channel independent supervector(UBM)
    D is a diagonal matrix(Why? because it models residual)
    V is a rectangular matrix of low rank;
    y and z are independent random vectors having standard normal distributions

    In other words, s is assumed to be normally distributed with mean m and covariance matrix  <a href="https://www.codecogs.com/eqnedit.php?latex=VV^*&space;&plus;&space;DD^*" target="_blank"><img src="https://latex.codecogs.com/gif.latex?VV^*&space;&plus;&space;DD^*" title="VV^* + DD^*" /></a>
 
    y is speaker factor
    z is common factor

    The channel-dependent supervector c, which represents the channel effect in an utterance, is assumed to be distributed according to 

   <a href="https://www.codecogs.com/eqnedit.php?latex=c&space;=&space;Ux" target="_blank"><img src="https://latex.codecogs.com/gif.latex?c&space;=&space;Ux" title="c = Ux" /></a>

    U is eigenchannel matrix, x is a vector distributed with standard normal distribution
    This is equivalent ot saying that c is normally distributed with zero mean and covariance <a href="https://www.codecogs.com/eqnedit.php?latex=UU^*" target="_blank"><img src="https://latex.codecogs.com/gif.latex?UU^*" title="UU^*" /></a>  
    x is channel factor

5. Task Define  
    train the hyperparamenters U, V, D
6. Scoring is unerstood as computing the log-likelihood ratio(LLR) between the target speaker model s and the UBM for the test utterance
   就是看是s 生成的概率大，还是UBM生成的概率大
7. The likehood of test utterance is then computed by integrating over he posterior distribution of y and z and the prior distribution of x
8. Not only the training algorithm differ, but also the results were reported using different scoring strategies
9. frame by frame scoring, MAP point estimates are used for channel factors x (as well as for speaker and common factor y and z)
<a href="https://www.codecogs.com/eqnedit.php?latex=logP(\chi&space;|s))&space;=&space;\sum_{t=1}^{T}log\sum_{c=1}^{C}w_{c}&space;\mathcal&space;N(\bold&space;o_{t};&space;\bold&space;\mu,&space;\Sigma)" target="_blank"><img src="https://latex.codecogs.com/gif.latex?logP(\chi&space;|s))&space;=&space;\sum_{t=1}^{T}log\sum_{c=1}^{C}w_{c}&space;\mathcal&space;N(\bold&space;o_{t};&space;\bold&space;\mu,&space;\Sigma)" title="logP(\chi |s)) = \sum_{t=1}^{T}log\sum_{c=1}^{C}w_{c} \mathcal N(\bold o_{t}; \bold \mu, \Sigma)" /></a>  
C is number of Gaussians in the GMM
10. Integrating over Channel Distribution  
<a href="https://www.codecogs.com/eqnedit.php?latex=P(\chi|s)&space;=&space;\int&space;P(\chi|s,x)&space;\mathcal&space;N(x;&space;0,I)dx" target="_blank"><img src="https://latex.codecogs.com/gif.latex?P(\chi|s)&space;=&space;\int&space;P(\chi|s,x)&space;\mathcal&space;N(x;&space;0,I)dx" title="P(\chi|s) = \int P(\chi|s,x) \mathcal N(x; 0,I)dx" /></a>

The closed form(logarithmic) solution is then given as

<a href="https://www.codecogs.com/eqnedit.php?latex=\begin{align*}&space;log\tilde{P}(\chi|x)&space;=&space;\sum_{c=1}^{C}N_{c}log\frac{1}{(2\pi)^\frac{F}{2}&space;\left&space;|&space;\Sigma_{c}&space;\right&space;|^\frac{1}{2}}&space;\\&space;-&space;\frac{1}{2}tr(\Sigma^{-1}&space;\bold&space;S_{s})&space;-&space;\frac{1}{2}log\left|&space;\bold&space;L\right|&space;\\&space;&plus;&space;\frac{1}{2}\left&space;\|&space;\bold&space;L^{\frac{-1}{2}}&space;\bold&space;U^*&space;\Sigma^{-1}&space;\bold&space;F_{s}&space;\right&space;\|^{2}&space;\end{align*}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\begin{align*}&space;log\tilde{P}(\chi|x)&space;=&space;\sum_{c=1}^{C}N_{c}log\frac{1}{(2\pi)^\frac{F}{2}&space;\left&space;|&space;\Sigma_{c}&space;\right&space;|^\frac{1}{2}}&space;\\&space;-&space;\frac{1}{2}tr(\Sigma^{-1}&space;\bold&space;S_{s})&space;-&space;\frac{1}{2}log\left|&space;\bold&space;L\right|&space;\\&space;&plus;&space;\frac{1}{2}\left&space;\|&space;\bold&space;L^{\frac{-1}{2}}&space;\bold&space;U^*&space;\Sigma^{-1}&space;\bold&space;F_{s}&space;\right&space;\|^{2}&space;\end{align*}" title="\begin{align*} log\tilde{P}(\chi|x) = \sum_{c=1}^{C}N_{c}log\frac{1}{(2\pi)^\frac{F}{2} \left | \Sigma_{c} \right |^\frac{1}{2}} \\ - \frac{1}{2}tr(\Sigma^{-1} \bold S_{s}) - \frac{1}{2}log\left| \bold L\right| \\ + \frac{1}{2}\left \| \bold L^{\frac{-1}{2}} \bold U^* \Sigma^{-1} \bold F_{s} \right \|^{2} \end{align*}" /></a>

Dehak [Front-end factor analysis for speaker verification](http://habla.dc.uba.ar/gravano/ith-2014/presentaciones/Dehak_et_al_2010.pdf)
Published in 2010

Abstract of Abstract:
1. Totabl varibility space models both speaker and channel variabilities
2. Two scoring method: SVM with cosine kernel VS. cosine similarity, i-vector_SVM(cosine_kernel)
3. Three channel compensation techniques WCCN / LDA / NAP; the best is LDA followed by WCCN 

Abstract of Introduction
1. JFA model inter-speaker variability and propose compenstate for channel/session variability in the context of GMM
2. speaker GMM is obtained by adapting UBM 
3. UBM_GMM_NAP_SVM(KL kernal)
4. UBM_GMM_WCCN_JFA_SVM(cosine kernel), as opposed to the high-dimensional GMM supervector space for classical JFA
5. Channel factors which are supposed to model only channel effects, also contain information about speakers
6. In i-vector system, factor analysis is used as a feature-extractor.
7. The channel compensation in thie new approach is carried out in low-dimensional space, the total variability space, as opposed to the high-dimensional GMM supervector space for classical JFA.
8. One important characteristic of this approach is that there is no speaker enrollment? 啥意思？

Abstract of JOINT FACTOR ANALYSIS
1. M consists of additive components from a speaker and a channel/session subspace. (Channel is session)
2. 



A review of  ["I-vector Extraction for Speaker Recognition Based on Dimensionality Reduction"](https://pdf.sciencedirectassets.com/280203/1-s2.0-S1877050918X00118/1-s2.0-S1877050918314042/main.pdf?x-amz-security-token=AgoJb3JpZ2luX2VjEHoaCXVzLWVhc3QtMSJGMEQCIDIEP4zGiqfC0hbEv7pZCx9edyUc0oe0jlzJVlnMGiOfAiBRKrfBAznANc45m85IW5CQ%2BeJ3NdKIyG8v%2FmUJwtkXXyraAwhSEAIaDDA1OTAwMzU0Njg2NSIMpUe1wwSVD9oIBk5fKrcD9gZTuQLraKsF%2Fc8EE87OEMn1dSpVFItkJDQTXlNYbkqXYNfflF%2F1dLGn1r1R8s7J0Ixkz88DVT2lj0S3FpypSbOpSbT0xGv8mVCYPjapvTmIHubJqE6JEym06qNJpFaopyePwR0tycIYy09Szfxq6fLbWTy229Rcifaqj%2FAPKXWxUozf010FWsZKuAORZHkrdCqJe3HpLpd2ULzIC2%2FxuXVBr%2BTF%2BqIzHoiea9E6ycZozeaikOfO%2B3OAOPjGirJVt%2FKzWbhwEDJhdcGXbOalL0Y8aeI6XjEcEgz4VzRery6cuKWLqoF047E0cSdP6MnLbYQNiGdIm%2FWUqWwQZOvCvnjcduYaW5NnRehNmF9ELMw14hyC6AS74HpCH3YwkKfj%2Ft2fW5ZKPLFTy077gNB4qCmQD4Al8K0KisVk4hjNJSw0WdaxOc9nmdpU5BCxuWG%2BTHHK4fC5m7HNxwCyFxTzQyH05DVixIbraExN5oz69W1qnxOA%2BBpDXWB44b6opwyrAg7weg1E6loAPq8AUcqpfw1DC2va7mBxCZYC9LuLv%2BRB%2F0iBfl8q%2BO%2FlidugIjZweU0416gPNTDixOTlBTq1AbGMZSqNnClInctK%2B6cNm%2BHCJS1rk7qvyjph384ZbFXD6dEyM6E2KyDEIoUDtuVq9WLquQ2uTVpqHkFV5H0CdbOxuzdaOoD7dLaWTlX5e5yD2bFSOKO%2FKoVUd5rZw5HUH9exGeQ201MTIS2coMMyxJGnIBKPh8YponVJoyLeuhF%2FMaf7zQ7C4gwXg8xLtG3bHnaefzfH4njiB5oKDWvpEuS74mSO6Fct6NngyE6UKlHv4pGGAso%3D&AWSAccessKeyId=ASIAQ3PHCVTYRYBOUGVA&Expires=1555640659&Signature=saSNSF%2BiTuuyV%2BtWKM1dkletLfU%3D&hash=7263ac8e3a142c2f3e178c3a11a71cc2e902561f244b6548c4946c506875f3ef&host=68042c943591013ac2b2430a89b270f6af2c76d8dfd086a07176afe7c76c2c61&pii=S1877050918314042&tid=spdf-118b68a7-1f5a-4a4a-a34f-44b11b358c1b&sid=50d782432bc9b345795a46a950b23b7f8603gxrqb&type=client)
published in 2018

Terms:   
Syllables means a segment of frog's voice, refered to [Automatic Syllables Segmentation for Frog Identification System](https://www.researchgate.net/profile/Dzati_Ramli/publication/251232572_Automatic_Syllables_Segmentation_for_Frog_Identification_System/links/02e7e51ef4a074b0d2000000.pdf)

Abstract of the abstract:
what is 2656 syllables bio-acoustic signals from 55 species of frog
1. i-vector is a factor analysis and a subspace modeling method
2. Total Variability(TV): a low dimensional speaker- and channel-dependent space is defined
3. Total means both speaker and channel variabilities
4. Benefit(?) of modelling both the intra-domain and inter-domain variabilities into the same low dimensional space
5. Smaller UBM and higher i-vector is better


Abstract of Introduction
1. Terms: channel variability == session variability 
2. Channel compensation and noise reduction gives improvements over TV
3. i-vector(total variability model) has many data-driven components 
4. hyper-parameters can be trained on a completely different out-of-set-data
5. traditional appraoch is GMM 
6. Unlike the separate speaker and channel dependent subspace of JFA, i-vectors represent the GMM super-vector by a single total variability space
7. channel space contains information that can be used ot distinguish between speakers

How:
1. i-vector is a space transformation method, i.e. a transformation matrix: The approach provides an elegant way of reducing high-dimensional sequential input data to a low-dimensional fixed-lenght feature vector

    <a href="https://www.codecogs.com/eqnedit.php?latex=s&space;=&space;m&space;&plus;&space;Tw" target="_blank"><img src="https://latex.codecogs.com/gif.latex?s&space;=&space;m&space;&plus;&space;Tw" title="s = m + Tw" /></a>  

    m is mean supervector  
    T is a matrix bases spanning the subspace covering the important variability  
    w is i-vector which is a standard normally distributed latent variable, and the Maximum A posterior(MAP) point estimate(极大后验点估计) of the latent variable w
    i-vector dimensionality is equal to the "rank" of eigenmatrix, a larger i-vector dimension would not give much improvement to the classification performance but it greatly increased the computation effort
    
  
Process
1. front-end: cepstral feature extraction and UBM training
2. back-end: sufficient statistics computation, T-matrix training, i-vector extraction, dimensionality reduction and scoring  
![](https://github.com/glynpu/voiceprint_review/blob/master/jpeg/block_diagram_for_frog_identification_system_experiment.png)
