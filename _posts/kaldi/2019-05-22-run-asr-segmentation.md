---
layout: post
title:  kaldi-lstm-vad
date:   2019-05-21 23:05:00 +0800
categories: kaldi
tag: kaldi
---

本文学习[kaldi 中的run_asr_segmentation.sh](https://github.com/kaldi-asr/kaldi/blob/8ce3a95761e0eb97d95d3db2fcb6b2bfb7ffec5b/egs/aspire/s5/local/run_asr_segmentation.sh), 其实现了基于lstm的语音活动监测(voice activity detection)

1. [合并segments及其对应的text文件](https://github.com/kaldi-asr/kaldi/blob/8ce3a95761e0eb97d95d3db2fcb6b2bfb7ffec5b/egs/aspire/s5/local/run_asr_segmentation.sh#L93)
   ```
   utils/data/convert_data_dir_to_whole.sh $data_dir $whole_data_dir
   ```
   该命令中用到的python文件[combine_segments_to_recording.py](https://github.com/kaldi-asr/kaldi/blob/master/egs/wsj/s5/utils/data/internal/combine_segments_to_recording.py)默认采用python3，总是报编码错误，改成python2执行不报错。

3. 由whole_data_dir中的feats.scp以及data_dir中的segmetns，[生成各片段对应的feats.scp/utt2spk/spk2utt](https://github.com/kaldi-asr/kaldi/blob/8b54ef83e20b682a0b1f91cdbaf6abd53ce3c32d/egs/wsj/s5/steps/segmentation/prepare_targets_gmm.sh#L139)
   ```
   utils/data/subsegment_data_dir.sh $whole_data_dir ${data_dir}/segments ${data_dir}/tmp
   ```

2. [生成targets.scp prepare_targets_gmm.sh](https://github.com/kaldi-asr/kaldi/blob/8ce3a95761e0eb97d95d3db2fcb6b2bfb7ffec5b/egs/aspire/s5/local/run_asr_segmentation.sh#L111)
   ```
   该命令有5个参数：
   1. lang 解码需要的lang信息，包括 L.fst/phones.txt/oov.int/words.txt等
   2. data 提供segments信息
   3. whole 提供feats.scp。 该feats.scp对应的是完整recording的特征，结合data/segments文件可以得到具体某一段的特征
   4. ali_model_dir: a speaker-adapted system to align data_dir
   5. model_dir:  a speaker-independent system like LDA+MLLT system to decode the whole-recording version  

   ```

   所以[需要的文件有](https://github.com/kaldi-asr/kaldi/blob/8b54ef83e20b682a0b1f91cdbaf6abd53ce3c32d/egs/wsj/s5/steps/segmentation/prepare_targets_gmm.sh#L102)：
   ```
   for f in $in_whole_data_dir/feats.scp $in_data_dir/segments \
     $lang/phones.txt $garbage_phones_list $silence_phones_list \
     $ali_model_dir/final.mdl $model_dir/final.mdl $extra_files; do
     if [ ! -f $f ]; then
       echo "$0: Could not find file $f"
       exit 1
     fi
   done
   ```
 


* content
{:toc}

