---
layout: post
title:  kaldi fix_data_dir.sh脚本分析
date:   2019-05-21 14:05:00 +0800
categories: kaldi
tag: kaldi
---

* content
{:toc}

本文学习脚本[fix_data_dir.sh](https://github.com/kaldi-asr/kaldi/blob/master/egs/wsj/s5/utils/fix_data_dir.sh)。

依次执行下列五个步骤的原因：
```
filter_recordings 1. 仅保留recordings info 都齐全的segments
filter_speakers   2. 仅保留spk info都齐全的utt2spk
filter_utts       3. 将step 1的结果作用到step 2上，得到 recordings info / spk info都齐全的utt2spk, 并过滤recording info 相关文件
filter_speakers   4. 由step3 的结果重新生成spk2utt等spk info文件
filter_recordings 5. 由step3 的结果重新生成recordings info文件
```



```
set -e -o pipefail -u 

set 常用参数
-e errexit 如果一个命令返回一个非0退出状态值(失败),就退出.
-o pipefail -e 	不适合管道命令，加上-o pipefail可支持管道监测
-u 当执行时使用到未定义过的变量，则显示错误信息
-x 执行指令前，先输出指令

```

参考 [Linux set 命令参数及用法详解](https://www.cnblogs.com/liduanjun/p/3536996.html)
[linux set命令使用总结]



```
tmpdir=$(mktemp -d /tmp/kaldi.XXXX);
trap 'rm -rf "$tmpdir"' EXIT HUP INT PIPE TERM

利用trap监测脚本执行状态，当命令结束/终端后，删除生成的临时文件夹
```
参考博客:
[Linux信号机制与信号处理](https://www.jianshu.com/p/9c9b74f6a222?utm_campaign=maleskine&utm_content=note&utm_medium=seo_notes&utm_source=recommendation)
[linux的trap 命令](https://www.jianshu.com/p/b26d4e520385)

```
LC_ALL=C 是为了去除所有本地化的设置，让命令能正确执行。

```

./utils/filter_scp.pl 第一个参数是filters,第二个参数是待处理的文件。逐行处理第二个文件，若其第n-th列在filters中，则输出。 
-f n-th指定第二个输入文件中要匹配的列
--exclude 输出不再filters中的行

如filters文件input1.scp：
```
spk1
spk2
```
需要过滤的文件为input2.scp：
```
spk1_utt1 spk1
spk2_utt1 spk2
spk3_utt1 spk3
spk1_utt2 spk1
spk2_utt2 spk2
```
则执行命令 ./utils/filter_scp.pl -f 2 input1.scp input2.scp 得到
```
spk1_utt1 spk1
spk2_utt1 spk2
spk1_utt2 spk1
spk2_utt2 spk2
```
加上--exclude后得到不在filters中的行：
执行命令 ./utils/filter_scp.pl --exclude -f 2 input1.scp input2.scp 得到：
```
spk3_utt1 spk3
```

./utils/filter_scps.pl可同时处理多个文件，便于并发处理

这个命令处理两个文件之间的对应关系，功能类似命令：
```
awk 'NR==FNR{a[$1]=$1;next}{if($1 in a)print $0}' input1.scp input2.scp
```

```
n1=$(cat $tmpdir/recordings | wc -l)

计算recordings 的个数
```

```
function filter_recordings 
1. 用wav.scp 过滤segments/reco2file_and_channel/reco2dur

function filter_speakers
1. utt2spk生成spk2utt; 
2. cmvn.scp spk2gender等说话人信息文件(若有)过滤spk2utt中说话人信息不存在的行
3. 重新生成说话人信息完整的utt2spk

function filter_utts
1. 用feats.scp text segments utt2lang(若有)等utt的信息过滤utt2spk
```

