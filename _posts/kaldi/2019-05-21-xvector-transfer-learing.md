---
layout: post
title:  xvector的迁移学习(transfer learning)
date:   2019-05-22 23:05:00 +0800
categories: 他山之玉
tag: kaldi
---

[原google group讨论区链接](https://groups.google.com/forum/#!topic/kaldi-help/X-m26M0j_Zs)

1. 直接修改pre-trained model的softmax层，采用in-domain data继续训练

   ```
    The first step is to create the example egs for your data. That means running the sre16/v2 recipe (using your data), until you reach stage 4 of local/nnet3/xvector/tuning/run_xvector_1a.sh. Even though you're using your data, you might still want to perform some kind of augmentation  (e.g., with MUSAN noises and music, and with reverberation).
    
    Once your examples are created, you'll need to do the following:
    
    1. Look for a file called "pdf2num" in your new egs directory. This is the number of speakers in your egs. Let's call this value num_speakers.
    
    2. Create an nnet3 config file (let's call it your_nnet_config), that looks similar to the following. Replace num_speakers with the actual number of speakers in your training egs.
    
    component name=output.affine type=NaturalGradientAffineComponent input-dim=512 output-dim=num_speakers param-stddev=0.0 bias-stddev=0.0 max-change=1.5
    component-node name=output.affine component=output.affine input=tdnn7.batchnorm
    component name=output.log-softmax type=LogSoftmaxComponent dim=num_speakers
    component-node name=output.log-softmax component=output.log-softmax input=output.affine
    output-node name=output input=output.log-softmax objective=linear
    
    3. Run the following command:
    nnet3-copy --nnet-config=your_nnet_config exp/xvector_nnet_1a/final.raw exp/your_experiment_dir/0.raw
    
    0.raw should be identical to the pretrained model, but the final layer has been reinitialized, and resized to equal the number of speakers in your training data.
    
    4. Now, run local/nnet3/xvector/tuning/run_xvector_1a.sh from --stage 6 with --train-stage 0. If everything went smoothly, this should start training the pretrained DNN further, using your egs. 
    
    
    
   ```

2. 仅对backend进行in-domain transfer learning
    ```
    Question:
 
    Thank you for your reply.
Actually I have tried adapt the PLDA but the improvement was not significant.
May I ask under your way, the parameter of the layers other than the final layer would be also trained?

    Answer:
    Yes, the other layers will get trained too by default. The binary nnet-copy will just resize and reinitialize the pre-softmax output layer, using the config file described. If you want to train only some of the layers, you'll have to set a learning rate of 0 on the layers you don't want to train. 
    
    By the way, transfer learning in the x-vector DNN isn't something we've really looked into. My first message is about the steps I think you need to get it working in theory. It may not actually work well, especially if you have a limited amount of data. 
    
    There are a few ways you could handle the domain shift in your backend:
    
    1. Keep the existing PLDA model, but replace the mean.vec (the one you use to center the embeddings) with one computed from your in-domain data. This is the easiest option, and it will probably help over using the mean.vec in the pretrained model. 
    
    2. In addition to 1, perform PLDA adaptation using the binary ivector-adapt-plda
    
    3. In addition to 1, retrain the LDA matrix and PLDA model. Obviously this one will require knowing speaker labels, and will require more data to be effective. 

    4. Perform some kind of PLDA score normalization. This isn't in Kaldi yet, but it's not too hard to implement. I have a naive implementation (which is very slow) in a personal branch https://github.com/david-ryan-snyder/kaldi/blob/scale17-xvector/src/ivectorbin/ivector-plda-scoring-snorm.cc
    
    ```




* content
{:toc}

