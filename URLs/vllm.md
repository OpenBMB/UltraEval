## 运行代码

```bash
python URLs/vllm_url.py --model_name meta-llama/Llama-2-13b-hf --gpuid "1" --port 5002
```

* --model_name：和huggingface官网一致的模型名
* --gpuid：使用的gpu id，如果特别大的模型，需要多卡，用,隔开
* --port：端口号


## vLLM的返回值
vLLM的返回值是一个列表，大小等于prompt的大小。下面是实例
```python
[RequestOutput(request_id=0, prompt='The president of the United States is', prompt_token_ids=[2, 133, 394, 9, 5, 315, 532, 16], outputs=[CompletionOutput(index=0, text=' trying to blame the Latin American people for the political turmoil of his presidency.\n', token_ids=[667, 7, 4887, 5, 5862, 470, 82, 13, 5, 559, 12225, 9, 39, 5662, 4, 50118], cumulative_logprob=-35.04854726418853, logprobs={}, finish_reason=length), CompletionOutput(index=1, text=' making it easy for his predecessor to take control over his position.\n\nThe', token_ids=[442, 24, 1365, 13, 39, 9933, 7, 185, 797, 81, 39, 737, 4, 50118, 50118, 133], cumulative_logprob=-43.799275651574135, logprobs={}, finish_reason=length)], finished=True), RequestOutput(request_id=1, prompt='The capital of France is', prompt_token_ids=[2, 133, 812, 9, 1470, 16], outputs=[CompletionOutput(index=0, text=' France, not the US.  The capital of Germany is Germany.\nHa', token_ids=[1470, 6, 45, 5, 382, 4, 1437, 20, 812, 9, 1600, 16, 1600, 4, 50118, 24017], cumulative_logprob=-29.934647351503372, logprobs={}, finish_reason=length), CompletionOutput(index=1, text=" more than just a world capital. It's an entire city and city in the", token_ids=[55, 87, 95, 10, 232, 812, 4, 85, 18, 41, 1445, 343, 8, 343, 11, 5], cumulative_logprob=-39.127986401319504, logprobs={}, finish_reason=length)], finished=True)]
```

RequestOutput: <class 'vllm.outputs.RequestOutput'>
prompt: 输入的prompt
output: 模型返回的结果，类型是list，每个元素是一个<class 'vllm.outputs.CompletionOutput'>。数量和参数中的n保持一致
index：表示某个prompt的第几个输出
text：表示模型的输出


## 输入参数

* --max_tokens：生成文本的最大token数，至少为1
* --logprobs：生成的每个token的logprob的数量，必须是非负数
* --n：对于一个prompt，模型返回几个输出
### sampling[除了下面两种情况之外]：
* --use_beam_search: 等于False
* --early_stopping：必须为False，当不使用beam search
* --length_penalty： 必须为1，当不适用beam search
### beam_search[use_beam_search=True]:
* --use_beam_search：等于True
* --best_of：大于1
* --temperature：等于0
* --top_p：等于1
* --top_k：等于-1
* --early_stopping：in [True, False, "never"]
### greedy_sampling[use_beam_search=False, temperature无限小，或者=0]:
* --best_of: 等于1
* --top_p: 等于1
* --top_k: 等于-1
* --temperature：等于0

```python
@cached_property
def sampling_type(self) -> SamplingType:
    if self.use_beam_search:
        return SamplingType.BEAM
    if self.temperature < _SAMPLING_EPS:
        return SamplingType.GREEDY
    return SamplingType.RANDOM
```