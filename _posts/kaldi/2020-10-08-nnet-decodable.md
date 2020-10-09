---
layout: post
title:  nnet decodable的前向计算
date:   2020-10-08 10:05:00 +0800
<!-- categories: kaldi -->
tag: kaldi
---

在解码过程中,[ProcessingEmiting函数会调用decodable->LogLikelihood函数](https://github.com/kaldi-asr/kaldi/blob/3ce241b4ff1838d530e54b1aea9585c1493ee9f8/src/decoder/lattice-faster-decoder.cc#L754)  
```
      if (arc.ilabel != 0) {  // propagate..
        BaseFloat new_weight = arc.weight.Value() + cost_offset -
			// frame 是时间戳，即当前解码到的帧数
			// arc.ilabel是transition-id, 该值会转换为pdf-id，进而能达到对应的acoustic weight
            decodable->LogLikelihood(frame, arc.ilabel) + tok->tot_cost;
        if (new_weight + adaptive_beam < next_cutoff)
          next_cutoff = new_weight + adaptive_beam;
      }
```
[DecodableAmNnetSimple::LogLikelihood函数实现为](https://github.com/kaldi-asr/kaldi/blob/885dc04bf59a2ea1f4b6777b5ab7915c7dfc4d11/src/nnet3/nnet-am-decodable-simple.cc#L78)  
```
BaseFloat DecodableAmNnetSimple::LogLikelihood(int32 frame,
                                               int32 transition_id) {
  // 把transition-id转换为对应的pdf-id
  int32 pdf_id = trans_model_.TransitionIdToPdfFast(transition_id);
  // 由时间戳和pdf-id获得对应的神经网络的输出
  // 如果用tensorflow N H W C 的符号来解释，由于语音信号往往只有时间轴，采用一维卷机，即(Time Delay neural network, TDNN)或者[Temporal Convolutional Network, TCN](https://dida.do/blog/temporal-convolutional-networks-for-sequence-modeling), 所以N H W C退化为 N T C  
  // 又解码是往往逐条解码，所以N == 1
  // 下面函数参数(frame, pdf_id) 给定了 (T, C)
  return decodable_nnet_.GetOutput(frame, pdf_id);
}

```
[GetOutput是一个inline函数，直接在头文件里定义了](https://github.com/kaldi-asr/kaldi/blob/3ce241b4ff1838d530e54b1aea9585c1493ee9f8/src/nnet3/nnet-am-decodable-simple.h#L205)  
```
  // Gets the output for a particular frame and pdf_id, with
  // 0 <= subsampled_frame < NumFrames(),
  // and 0 <= pdf_id < OutputDim().
  inline BaseFloat GetOutput(int32 subsampled_frame, int32 pdf_id) {
    if (subsampled_frame < current_log_post_subsampled_offset_ ||
        subsampled_frame >= current_log_post_subsampled_offset_ +
                            current_log_post_.NumRows())
      // 计算subsampled_frame对应时刻的神经网络输出，
     // 即一个维度为OutputDim的向量
      EnsureFrameIsComputed(subsampled_frame);

	// current_log_post_ 的定义为：
	// Matrix<BaseFloat> current_log_post_;
	// current_log_post_（index_row, index_col) 是kaldi中matrix取元素的操作，不是函数调用
	// 即从上面计算得到的向量里取出pdf_id对应的概率
    return current_log_post_(subsampled_frame -
                             current_log_post_subsampled_offset_,
                             pdf_id);
  }

```

函数[EnsureFrameIsComputed](https://github.com/kaldi-asr/kaldi/blob/885dc04bf59a2ea1f4b6777b5ab7915c7dfc4d11/src/nnet3/nnet-am-decodable-simple.cc#L93)大致可以分为两部分，准备收入特征 + 神经网络计算。
```
  if (first_input_frame >= 0 &&
      last_input_frame < feats_.NumRows()) {
	// 正常的解码过程
    SubMatrix<BaseFloat> input_feats(feats_.RowRange(first_input_frame,
                                                     num_input_frames));
	// 把输入准备好后，进行神经网络的计算
    DoNnetComputation(first_input_frame, input_feats, ivector,
                      first_output_frame, num_subsampled_frames);
  } else {
	// 需要padding 的过程
	// 比如 subsampled_frame为第一帧时，假如left-context为21，  
	// 那么需要 -21, -20, -19,等时刻的输入，显然这些输入是不存在的
	// padding上 0时刻的数据
    Matrix<BaseFloat> feats_block(num_input_frames, feats_.NumCols());
    int32 tot_input_feats = feats_.NumRows();
    for (int32 i = 0; i < num_input_frames; i++) {
      SubVector<BaseFloat> dest(feats_block, i);
      int32 t = i + first_input_frame;
	  // 如果需要负时刻的输入，就padding 0时刻的数据
      if (t < 0) t = 0;
	  // 如果需要tot_input_feats之后的输入，就padding最后一个时刻的数据
      if (t >= tot_input_feats) t = tot_input_feats - 1;
      const SubVector<BaseFloat> src(feats_, t);
	  // 注意kaldi中是如何复制一个vector
      dest.CopyFromVec(src);
    }
    DoNnetComputation(first_input_frame, feats_block, ivector,
                      first_output_frame, num_subsampled_frames);
  }

```

[函数DecodableNnetSimple::DonnetComputation](https://github.com/kaldi-asr/kaldi/blob/885dc04bf59a2ea1f4b6777b5ab7915c7dfc4d11/src/nnet3/nnet-am-decodable-simple.cc#L215)真正执行神经网络前向运算  
主要过程分为五步：  
1. 把提供的输入和指定的输出打包成ComputationRequest  
2. compiler 把 ComputationRequest 和神经网络一块编译成NnetComputation  
3. NnetComputer接受输入  
4. NnetComputer执行Computation中的commands  
5. NnetComputer获取输出  

```
void DecodableNnetSimple::DoNnetComputation(
    int32 input_t_start,
    const MatrixBase<BaseFloat> &input_feats,
    const VectorBase<BaseFloat> &ivector,
    int32 output_t_start,
    int32 num_subsampled_frames) {
  ComputationRequest request;
  request.need_model_derivative = false;
  request.store_component_stats = false;

  bool shift_time = true; // shift the 'input' and 'output' to a consistent
  // time, to take advantage of caching in the compiler.
  // An optimization.
  int32 time_offset = (shift_time ? -output_t_start : 0);

  // First add the regular features-- named "input".
  request.inputs.reserve(2);
  request.inputs.push_back(
      IoSpecification("input", time_offset + input_t_start,
                      time_offset + input_t_start + input_feats.NumRows()));
  if (ivector.Dim() != 0) {
    std::vector<Index> indexes;
    indexes.push_back(Index(0, 0, 0));
    request.inputs.push_back(IoSpecification("ivector", indexes));
  }
  IoSpecification output_spec;
  // 这个是hard-code的，从这一行可以看出kaldi只会取一个叫"output"的node的输出
  // 为了获得特定node的输出，只需要把该node的名字改为output就行了
  output_spec.name = "output";
  // 解码过程中，只有前向计算不需要梯度
  output_spec.has_deriv = false;
  int32 subsample = opts_.frame_subsampling_factor;
  output_spec.indexes.resize(num_subsampled_frames);
  // leave n and x values at 0 (the constructor sets these).
  for (int32 i = 0; i < num_subsampled_frames; i++)
    output_spec.indexes[i].t = time_offset + output_t_start + i * subsample;
  request.outputs.resize(1);
  request.outputs[0].Swap(&output_spec);

  // 为什么此处需要是智能指针?
  // 为什么Compile只需要传入request 而不需要nnet? 因为nnet在定义compiler时已经传入了
  std::shared_ptr<const NnetComputation> computation = compiler_.Compile(request);
  Nnet *nnet_to_update = NULL;  // we're not doing any update.
  NnetComputer computer(opts_.compute_config, *computation,
                        nnet_, nnet_to_update);

  CuMatrix<BaseFloat> input_feats_cu(input_feats);
  computer.AcceptInput("input", &input_feats_cu);
  CuMatrix<BaseFloat> ivector_feats_cu;
  if (ivector.Dim() > 0) {
    ivector_feats_cu.Resize(1, ivector.Dim());
    ivector_feats_cu.Row(0).CopyFromVec(ivector);
    computer.AcceptInput("ivector", &ivector_feats_cu);
  }
  // 真正的分配空间 + 前向运算过程
  computer.Run();
  CuMatrix<BaseFloat> cu_output;
  computer.GetOutputDestructive("output", &cu_output);
  // subtract log-prior (divide by prior)
  if (log_priors_.Dim() != 0)
    cu_output.AddVecToRows(-1.0, log_priors_);
  // apply the acoustic scale
  cu_output.Scale(opts_.acoustic_scale);
  current_log_post_.Resize(0, 0);
  // the following statement just swaps the pointers if we're not using a GPU.
  cu_output.Swap(&current_log_post_);
  current_log_post_subsampled_offset_ = output_t_start / subsample;
}
```

上述compiler_是[CacheingOptimizingCompiler](https,//github.com/kaldi-asr/kaldi/blob/3ce241b4ff1838d530e54b1aea9585c1493ee9f8/src/nnet3/nnet-optimize.h#L219),它同时兼具编译和优化Computatation的功能,[compiler的调用示例](https://github.com/kaldi-asr/kaldi/blob/3ce241b4ff1838d530e54b1aea9585c1493ee9f8/src/nnet3bin/nnet3-latgen-faster.cc#L130)  
```
    // this compiler object allows caching of computations across
    // different utterances.
    CachingOptimizingCompiler compiler(am_nnet.GetNnet(),
                                       decodable_opts.optimize_config);
```

[CachingOptimizingCompiler::Compiler函数](https://github.com/kaldi-asr/kaldi/blob/885dc04bf59a2ea1f4b6777b5ab7915c7dfc4d11/src/nnet3/nnet-optimize.cc#L716)定义为:  
```
std::shared_ptr<const NnetComputation> CachingOptimizingCompiler::Compile(
    const ComputationRequest  &in_request) {
  Timer timer;
  std::shared_ptr<const NnetComputation>  ans = CompileInternal(in_request);
  seconds_taken_total_ += timer.Elapsed();
  return ans;
}

```
其主要功能有[CompileInternal函数](https://github.com/kaldi-asr/kaldi/blob/885dc04bf59a2ea1f4b6777b5ab7915c7dfc4d11/src/nnet3/nnet-optimize.cc#L724)实现：  
```
std::shared_ptr<const NnetComputation> CachingOptimizingCompiler::CompileInternal(
    const ComputationRequest  &request) {
  std::shared_ptr<const NnetComputation> ans = cache_.Find(request);
  if (ans != NULL) {
    return ans;
  } else {
    const NnetComputation *computation = NULL;
    if (config_.use_shortcut)
      computation = CompileViaShortcut(request);
    if (computation == NULL)
      computation = CompileNoShortcut(request);
    KALDI_ASSERT(computation != NULL);
    return cache_.Insert(request, computation);
  }
}
```

分析CompileNoShortcut,其中定义了[Compiler](https://github.com/kaldi-asr/kaldi/blob/3ce241b4ff1838d530e54b1aea9585c1493ee9f8/src/nnet3/nnet-compile.h#L44)和[NnetComputation](https://github.com/kaldi-asr/kaldi/blob/3ce241b4ff1838d530e54b1aea9585c1493ee9f8/src/nnet3/nnet-computation.h#L303)  
[CompileNoShortCut函数实现](https://github.com/kaldi-asr/kaldi/blob/885dc04bf59a2ea1f4b6777b5ab7915c7dfc4d11/src/nnet3/nnet-optimize.cc#L741)
```
const NnetComputation *CachingOptimizingCompiler::CompileNoShortcut(
    const ComputationRequest &request) {

  Compiler compiler(request, nnet_);
  // note: 'opts' only contains 'output_debug_info', which is true by default.
  // There may be situations where we'd prefer not to keep it, for speed.
  CompilerOptions opts;
  NnetComputation *computation = new NnetComputation;

  {
    Timer timer;
    compiler.CreateComputation(opts, computation);
    seconds_taken_compile_ += timer.Elapsed();
  }

```

Struct NnetComputation中有一个重要的成员[commands](https://github.com/kaldi-asr/kaldi/blob/3ce241b4ff1838d530e54b1aea9585c1493ee9f8/src/nnet3/nnet-computation.h#L439), 该成员记录了整个前向过程的所有操作，computer.run()函数的执行过程，就是不断从该vector中取指令，执行指令的过程  
```
  // The sequence of commands.
  std::vector<Command> commands;

```
[Compiler有一个重要的成员graph_](https://github.com/kaldi-asr/kaldi/blob/master/src/nnet3/nnet-compile.h#L64), 该[ComputationGraph](https://github.com/kaldi-asr/kaldi/blob/master/src/nnet3/nnet-computation-graph.h#L43) graph_把nnet_中nodes_等信息表达成更为直观的c_index + dependencies信息

[函数Compiler::CreateComputation](https://github.com/kaldi-asr/kaldi/blob/885dc04bf59a2ea1f4b6777b5ab7915c7dfc4d11/src/nnet3/nnet-compile.cc#L50)中的[ComputationGraphBuilder](https://github.com/kaldi-asr/kaldi/blob/3ce241b4ff1838d530e54b1aea9585c1493ee9f8/src/nnet3/nnet-computation-graph.h#L117)把nnet_转化为graph_  

同时builder还负责指定输出能否计算合法性检查  
精简计算图  
(学习到Compiler::CreateComputation, 未完待续)  

```
	void Compiler::CreateComputation(const CompilerOptions &opts,
                                 NnetComputation *computation) {
  computation->Clear();
  ComputationGraphBuilder builder(nnet_, &graph_);
  // note: there are only >1 segments in a 'looped' computation.
  for (size_t segment = 0; segment < requests_.size(); segment++) {
    builder.Compute(*(requests_[segment]));
    if (!builder.AllOutputsAreComputable()) {
      builder.ExplainWhyAllOutputsNotComputable();  // prints logging info
      KALDI_ERR << "Not all outputs were computable, cannot create computation.";
    }
    builder.Prune();
  }
  // see function declaration's comment for more on the meaning of "phases" (a
  // phase will later be decomposed into one or more steps).  for each segment
  // s, phases_per_segment[s] is a list of phases; each phase is a list of
  // cindex_ids.
  std::vector<std::vector<std::vector<int32> > > phases_per_segment;
  ComputeComputationPhases(nnet_, graph_, &phases_per_segment);
  std::vector<std::vector<int32> > steps;
  steps.reserve(1000);

  // maps each step to the segment in which it appears.  in the normal case
  // (non-looped computation), a vector of all zeros.
  std::vector<int32> step_to_segment;


  {
    // note: this class will output to 'steps' and to 'cindex_id_to_location_'.
    // it may incidentally change 'graph_' by adding a few cindexes.
    ComputationStepsComputer steps_computer(nnet_, &graph_, &steps,
                                            &cindex_id_to_location_);

    for (size_t segment = 0; segment < requests_.size(); segment++) {
      steps_computer.ComputeForSegment(*(requests_[segment]),
                                       phases_per_segment[segment]);
      while (step_to_segment.size() < steps.size())
        step_to_segment.push_back(segment);

      // save memory, by deleting the phases we just consumed.  the
      // following two lines just exist to save memory.
      std::vector<std::vector<int32> > temp;
      phases_per_segment[segment].swap(temp);
    }
    steps_computer.Check();
  }
  std::vector<bool> deriv_needed;
  ComputeDerivNeeded(steps, step_to_segment, &deriv_needed);
  CreateStepInfo(deriv_needed, step_to_segment, &steps, computation);
  AddCommands(deriv_needed, step_to_segment, computation);
  // the following command reorders commands so kAcceptInput and kProvideOutput
  // appear in the desired places.
  ConsolidateIoOperations(nnet_, computation);
  if (opts.output_debug_info)
    OutputDebugInfo(computation);
}
```



* content
{:toc}

