---
layout: post
title:  kaldi nnet3 x-vector get_egs准备脚本
date:   2019-05-22 23:05:00 +0800
categories: kaldi
tag: kaldi
---

本文学习[X-vector egs生成脚本](https://github.com/kaldi-asr/kaldi/blob/master/egs/sre08/v1/sid/nnet3/xvector/get_egs.sh)

1. epoch/iteration/num_train_archives之间的联系  
   [epoch 是所有的egs过一遍即所有的egs.*.ark过一遍；
   iteration 是一个job处理特定的帧数](https://sourceforge.net/p/kaldi/discussion/1355347/thread/cc50c9fc/?limit=25#1aae)
   epoch 是从输入端分析的指标，```num_epochs*num_archives``` 即给模型训练过程提供的数据。  
   iteration是从输出端分析的指标，```iteration * avg_num_jobs```是模型训练过程中消耗的数据。  
   根据“物质守恒定律”，```num_epochs*num_archives == num_iters * avg_num_jobs```
   ```    
    # set num_iters so that as close as possible, we process the data
    # $num_epochs times, i.e. $num_iters*$avg_num_jobs) ==
    # $num_epochs*$num_archives, where
    # avg_num_jobs=(num_jobs_initial+num_jobs_final)/2.

   ```

   [来源](https://github.com/kaldi-asr/kaldi/blob/8b54ef83e20b682a0b1f91cdbaf6abd53ce3c32d/egs/wsj/s5/steps/nnet3/train_raw_dnn.py#L319)

   ```
    # 所有可能参与训练的样本frames总数
    num_train_frames=$(awk '{n += $2} END{print n}' <$temp/utt2num_frames.train)
    ***
    num_train_archives=$[($num_train_frames*$num_repeats)/$frames_per_iter + 1]
   ```
   [来源](https://github.com/kaldi-asr/kaldi/blob/8b54ef83e20b682a0b1f91cdbaf6abd53ce3c32d/egs/sre08/v1/sid/nnet3/xvector/get_egs.sh)

2. [ranges文件的生成](https://github.com/kaldi-asr/kaldi/blob/8b54ef83e20b682a0b1f91cdbaf6abd53ce3c32d/egs/sre08/v1/sid/nnet3/xvector/allocate_egs.py#L239)
    ```
    [#确定当前archive的chunk_length](https://github.com/kaldi-asr/kaldi/blob/8b54ef83e20b682a0b1f91cdbaf6abd53ce3c32d/egs/sre08/v1/sid/nnet3/xvector/allocate_egs.py#L248)
    length = deterministic_chunk_length(archive_index, args.num_archives, args.min_frames_per_chunk, args.max_frames_per_chunk);
    
    [#确定当前archive包含的egs确切个数](https://github.com/kaldi-asr/kaldi/blob/master/egs/sre08/v1/sid/nnet3/xvector/allocate_egs.py#L251)
    this_num_egs = int(float(args.frames_per_iter) / length + 1)
    
    [#for循环随机抽样](https://github.com/kaldi-asr/kaldi/blob/8b54ef83e20b682a0b1f91cdbaf6abd53ce3c32d/egs/sre08/v1/sid/nnet3/xvector/allocate_egs.py#L260)
    utt = get_random_utt(spkr, spk2utt, length)
    
    ```
   
   总结：
     1. 每个archive的chunk_length存储在/path/to/egs/temp/archive_chunk_lengths文件里 
     2. 同一个archive内部样本chunk_length是一致的
3. [outputs 文件的生成](https://github.com/kaldi-asr/kaldi/blob/8b54ef83e20b682a0b1f91cdbaf6abd53ce3c32d/egs/sre08/v1/sid/nnet3/xvector/allocate_egs.py#L304)

   outputs 内容为[this_archives_for_job](https://github.com/kaldi-asr/kaldi/blob/8b54ef83e20b682a0b1f91cdbaf6abd53ce3c32d/egs/sre08/v1/sid/nnet3/xvector/allocate_egs.py#L280),作用是指定ranges个样本最终所在的archive的名字


4. [训练样本archive文件的生成 nnet3-xvector-get-egs.cc](https://github.com/kaldi-asr/kaldi/blob/master/src/nnet3bin/nnet3-xvector-get-egs.cc)

   该代码中给出了ranges文件的格式说明：
   ```
        "<source-utterance> <relative-output-archive-index> "
        "<absolute-archive-index> <start-frame-index> <num-frames> "
        "<speaker-label>\n"
        "For example:\n"
          "  utt1  3  13  65  300  3\n"
          "  utt1  0  10  50  400  3\n"
          "  utt2  ...\n"
          "\n"

   ```
   ranges文件应满足以下关系：
      1. relative-output-archive-index 的个数与num-frames个数相同，
      2. 每个archive内的num-frames都应该一致。[根据get_egs脚本，为了避免训练时不重复compile 网络，不会把不同长度的样本混到同一个archive里。](https://github.com/kaldi-asr/kaldi/blob/8b54ef83e20b682a0b1f91cdbaf6abd53ce3c32d/egs/sre08/v1/sid/nnet3/xvector/get_egs.sh#L11)


* content
{:toc}

