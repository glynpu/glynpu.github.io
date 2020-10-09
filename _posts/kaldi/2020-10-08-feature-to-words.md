---
layout: post
title:  kaldi 特征到文字的转换过程
date:   2020-10-07 23:05:00 +0800
categories: kaldi
tag: kaldi
---

fbank/mfcc feature 到最终生成文字主要有三大模块在起作用
1. acoustic model(am) 声学模型
2. language modle(lm) 语言模型
3. decoder 解码器


下面以kaldi/src/nnet3bin/nnet3-latgen-faster.cc为例分析asr的流程：  
其总体框架为tdnn am  +  fst lm + lattice-faster-decoder

在am-nnet am 和解码图加载完毕后，调用[DecodeUtteranceLatticeFaster](https://github.com/kaldi-asr/kaldi/blob/3ce241b4ff1838d530e54b1aea9585c1493ee9f8/src/nnet3bin/nnet3-latgen-faster.cc#L180)进行解码：  
```
          DecodableAmNnetSimple nnet_decodable(
              decodable_opts, trans_model, am_nnet,
              features, ivector, online_ivectors,
              online_ivector_period, &compiler);

          double like;
		  // 该函数是一个模版函数，数据类型参数为构建decoder时的FST类型
          if (DecodeUtteranceLatticeFaster(
                  decoder, nnet_decodable, trans_model, word_syms, utt,
                  decodable_opts.acoustic_scale, determinize, allow_partial,
                  &alignment_writer, &words_writer, &compact_lattice_writer,
                  &lattice_writer,
                  &like)) {
            tot_like += like;
            frame_count += nnet_decodable.NumFramesReady();
            num_success++;
          } else num_fail++;
        }
```

[DecodeUtteranceLatticeFaster函数会调用decoder的成员函数Decode](https://github.com/kaldi-asr/kaldi/blob/885dc04bf59a2ea1f4b6777b5ab7915c7dfc4d11/src/decoder/decoder-wrappers.cc#L287:6)  

```
  if (!decoder.Decode(&decodable)) {
    KALDI_WARN << "Failed to decode utterance with id " << utt;
    return false;
  }

```

其中传入的decoder 类型[LatticeFasterDecoderTps是一个typedef](https://github.com/kaldi-asr/kaldi/blob/3ce241b4ff1838d530e54b1aea9585c1493ee9f8/src/decoder/lattice-faster-decoder.h#L522:1)
```
typedef LatticeFasterDecoderTpl<fst::StdFst, decoder::StdToken> LatticeFasterDecoder;
```

所以decoder.Decode函数其实是[模版类LatticeFasterDecoderTpl的成员函数Decode](https://github.com/kaldi-asr/kaldi/blob/master/src/decoder/lattice-faster-decoder.cc#L79)  
```
template <typename FST, typename Token>
bool LatticeFasterDecoderTpl<FST, Token>::Decode(DecodableInterface *decodable) {
  InitDecoding();
  // We use 1-based indexing for frames in this decoder (if you view it in
  // terms of features), but note that the decodable object uses zero-based
  // numbering, which we have to correct for when we call it.
  AdvanceDecoding(decodable);
  FinalizeDecoding();

  // Returns true if we have any kind of traceback available (not necessarily
  // to the end state; query ReachedFinal() for that).
  return !active_toks_.empty() && active_toks_.back().toks != NULL;
}
```
其中主要的解码过程集中在[AdvanceDecoding](https://github.com/kaldi-asr/kaldi/blob/3ce241b4ff1838d530e54b1aea9585c1493ee9f8/src/decoder/lattice-faster-decoder.cc#L580),其内部的while循环一直持续到解码出预期的frames位置:  
```
  if (max_num_frames >= 0)
    target_frames_decoded = std::min(target_frames_decoded,
                                     NumFramesDecoded() + max_num_frames);
  while (NumFramesDecoded() < target_frames_decoded) {
    if (NumFramesDecoded() % config_.prune_interval == 0) {
      PruneActiveTokens(config_.lattice_beam * config_.prune_scale);
    }
    BaseFloat cost_cutoff = ProcessEmitting(decodable);
    ProcessNonemitting(cost_cutoff);
  }

```

上述while循环中每次循环消耗一个frame的acoustic 输入.   
其中[ProcessEmitting](https://github.com/kaldi-asr/kaldi/blob/3ce241b4ff1838d530e54b1aea9585c1493ee9f8/src/decoder/lattice-faster-decoder.cc#L714)函数对应解码图上输入不为空的跳转,[消耗一个acoustic frame](https://github.com/kaldi-asr/kaldi/blob/3ce241b4ff1838d530e54b1aea9585c1493ee9f8/src/decoder/lattice-faster-decoder.cc#L752);  
```
    for (fst::ArcIterator<FST> aiter(*fst_, state);
         !aiter.Done();
         aiter.Next()) {
      const Arc &arc = aiter.Value();
	  // arc.ilabel != 0 即当前输入label不为空
      if (arc.ilabel != 0) {  // propagate..
		  // 注意decodable->LogLikelihood即消耗了一个acoustic frame
        BaseFloat new_weight = arc.weight.Value() + cost_offset -
            decodable->LogLikelihood(frame, arc.ilabel) + tok->tot_cost;
        if (new_weight + adaptive_beam < next_cutoff)
          next_cutoff = new_weight + adaptive_beam;
      }

```
[ProcessNonemitting](https://github.com/kaldi-asr/kaldi/blob/3ce241b4ff1838d530e54b1aea9585c1493ee9f8/src/decoder/lattice-faster-decoder.cc#L820)对应输入为空的跳转(扩大当前token的数目),不消耗acoustic frame
```
  // 注意queue_的用处
  // queue_可以用来处理连续多个跳转的输入都是空的情况
  // 每次空跳转产生的tok都塞到queue_里，即队列的尾部，
  // 随着依次出队，新的tok会被判断是否含有空跳转
  // 有一点广度优先遍历的感觉
	
  // 双重循环，第一重循环是不断的出队,
  // 因为队列在循环的过程中不断的增加/删除元素，不确定由多少个元素
  // 所以用while 循环
  while (!queue_.empty()) {
    const Elem *e = queue_.back();
    queue_.pop_back();

    StateId state = e->key;
    Token *tok = e->val;  // would segfault if e is a NULL pointer but this can't happen.
    BaseFloat cur_cost = tok->tot_cost;
    if (cur_cost >= cutoff) // Don't bother processing successors.
      continue;
    // If "tok" has any existing forward links, delete them,
    // because we're about to regenerate them.  This is a kind
    // of non-optimality (remember, this is the simple decoder),
    // but since most states are emitting it's not a huge issue.
    DeleteForwardLinks(tok); // necessary when re-visiting
    tok->links = NULL;
	// 对于特定的解码图,每个state有多少个跳转是确定的
	// 所以用for 循环
    for (fst::ArcIterator<FST> aiter(*fst_, state);
         !aiter.Done();
         aiter.Next()) {
      const Arc &arc = aiter.Value();
	  // 注意此处和ProcessEmiting函数的区别
      if (arc.ilabel == 0) {  // propagate nonemitting only...
        BaseFloat graph_cost = arc.weight.Value(),
			// 注意此处没有am cost
			// 即decodable->LogLikelihood
            tot_cost = cur_cost + graph_cost;
        if (tot_cost < cutoff) {
          bool changed;

          Elem *e_new = FindOrAddToken(arc.nextstate, frame + 1, tot_cost,
                                          tok, &changed);

          tok->links = new ForwardLinkT(e_new->val, 0, arc.olabel,
                                        graph_cost, 0, tok->links);

          // "changed" tells us whether the new token has a different
          // cost from before, or is new [if so, add into queue].
		  // 把新的token塞到队列里
          if (changed && fst_->NumInputEpsilons(arc.nextstate) != 0)
            queue_.push_back(e_new);
        }
      }
    } // for all arcs
  } // while queue not empty
```

总的来说, 解码的过程就是不断的ProcessEmiting 和ProcessNonEmiting沿着解码图把对应的acoustic weight 和 language weight 加一起	


相关知识:
-
[加载am nnet]({% link _posts/kaldi/2020-10-08-kaldi-am-nn-read.md %})  
[decodable->LogLikelihood函数是如何计算的]({% link _posts/kaldi/2020-10-08-nnet-decodable.md %})
