## 推理参数文件

指定模型推理的相关参数。

UltraEval通过`models/model_params`来设置模型推理的参数。不同任务需要的模型推理参数可能不同,同一个模型根据生成采样方式的不同选择，推理参数也会不一样。下面是常见的三个参数配置文件：

- `vllm_beamsearch.json` 束搜索

```
{
    "use_beam_search": true,  // 是否使用束搜索（Beam Search）。True表示使用，通常用于提高生成文本的质量。
    "best_of": 10,            // 在束搜索或其他生成策略中，从多少个候选中选择最佳输出。
    "temperature": 0,         // 用于控制生成文本的随机性。温度为0意味着总是选择概率最高的词。
    "top_p": 1,               // 保留累计概率达到top_p的最小词集合，用于控制生成文本的多样性。1意味着不应用过滤。
    "top_k": -1,              // 保留概率最高的top_k个词，用于控制生成文本的多样性。-1意味着不应用过滤。
    "early_stopping": "never", // 提前终止条件。"never"表示生成将继续进行，直到达到最大令牌数。
    "max_tokens": 100         // 生成文本的最大令牌数。
}
```

- `vllm_sample.json` 随机采样

```
{
    "temperature": 0.3,   // 控制生成文本的随机性。温度较低（如0.1）意味着生成的文本更可能倾向于高概率词，从而更加确定性和一致性。
    "top_p": 0.8,        // 保留累计概率达到0.8的最小词集合。这意味着模型只会考虑累计概率达到80%的词进行生成，帮助确保生成文本的多样性与可靠性。
    "max_tokens": 100     // 生成文本的最大token数。这里设置为100，意味着生成的文本最多包含100个token。
}
```

随机采样特殊说明：

​	对于直接回答选项的选择题和数学代码类题目，建议设置为：`temperature=0.1,top_p=0.95,max_tokens=10`

​	对于数学代码类题目，建议设置为：`temperature=0.1,top_p=0.95,max_tokens=200`

​	对于其它题目，通用设置推荐为：`temperature=0.3,top_p=0.8,max_tokens=100`

- `vllm_logprobs.json` 对数似然度，该文件一般不需要更改参数，且更改参数对评测无影响

```
{
    "prompt_logprobs": 0,   // 每个提示词token返回的对数似然的数量，不建议更改
    "max_tokens": 1         // 生成文本的最大token数。在这里设置为1，意味着在执行loglikelihood推理时，每次只生成一个token。
}
```

- 注：model_params出现在config以及main文件中的区别
  - model_params设置的是关于模型推理时的相关参数，仅影响模型的推理能力的设置，与输入的数据和prompt等无关。
  - config设置的是关于数据集的默认参数，主要是与数据集相关的默认推荐设置，涉及该任务的名称、数据路径、transform文件、以及推荐评测方式和metric的指定等等。
  - main文件中的参数更多是关于对于整个评测流程的调控。如果是多个任务同时进行评测时，当部分参数与config中的参数冲突时，优先级有所不同。
    - 对于针对任务的参数`num_fewshot`，main文件中的参数具有更高的优先级，便于用户统一指定任务的fewshot；
    - 对于针对模型的参数`model_params`，config中的参数具有更高的优先级，main文件中的参数更具普遍性，特殊任务则特殊处理。