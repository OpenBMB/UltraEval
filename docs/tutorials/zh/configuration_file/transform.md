## 数据转换

在数据规整后，添加提示词（prompt），以适应不同的模型、评测方式的要求。

UltraEval通过 `datasets/{dataset_name}/transform.py` 脚本组织创建好的UltraEval格式任务集，生成适用于不同场景的模型输入提示（prompts）。该脚本对数据集中的每条数据进行处理，返回一个包含以下字段的字典：

- **input**: 模型需要处理的输入文本。要求为字符串形式。
- **output**: few-shot大于0时，用于与input拼接的正确答案。形成few-shot的数据也会通过此脚本组织。
- **processed_output**: 用于评测的正确答案。在metric中经过后处理的模型输出将与processed_output进行比较，以计算这条数据的得分。

在使用GEN评测方式时，大部分数据集的 `output` 和 `processed_output` 字段通常是相同的。然而，存在一些例外情况，如在处理 `gsm8k` 任务时，`processed_output` 字段需要基于 `output` 字段进行额外的后处理。因为在这些特殊情况下，用于few-shot拼接的答案与实际评测时的答案不同。这种不一致主要源于CoT（Chain of Thought）或特殊提取格式等因素的影响。

在采用PPL评测方式时，UltraEval仅使用 `input` 字段，并将其与UltraEval格式任务集中的 `target_scores` 字段的每个键值进行拼接，以计算整个句子的负对数概率（negative loglikelihood）。在这种情况下，`output` 和 `processed_output` 字段不会被使用。

为了实现更高效的管理，我们在仓库中的 `transform` 脚本上采用了基于版本号的命名方式。举例来说，`datasets/{dataset_name}/transform_{gen/ppl}_v0.py` 表示此脚本为该数据集的v0 版本transform，同时也声明了其对应的评测方式。这种命名策略不仅方便我们不断地迭代和优化提示词以适应不同的需求，同时也允许我们保留旧版本的提示词，从而和榜单相对应，以确保整个过程的透明度和可追溯性。

**以ax-b为例：**

- **GEN形式任务**

```
import random

def transform(data, num_sample: int, r: random.Random, dataset_name: str):
    # 构建问题、上下文、指令和选项部分。
    question = f"Question:\nIs the second sentence entailed by the first sentence?\n"
    context = f"First sentence: {data['passage'][0]}\nSecond sentence: {data['passage'][1]}\n"
    instruction = f"Requirement:\nChoose and respond with the letter of the correct answer, including the parentheses.\n"
    options = "Options:\n"
    for idx, item in enumerate(data['target_scores'].keys()):
        options += f"({chr(65 + idx)}) {item}\n"
    answer_prompt = f"Answer:\n"
    text = question + context + instruction + options + answer_prompt

    # 根据target_scores字段确定正确答案。
    index_of_correct_answer = list(data['target_scores'].values()).index(1)
    processed_correct_answer = correct_answer = f"({chr(65 + index_of_correct_answer)})"

    return {"input": text, "output": correct_answer, "processed_output": processed_correct_answer}
```

- **PPL形式任务**

```
import random

def transform(data, num_sample: int, r: random.Random, dataset_name: str):
    # 构建问题描述、上下文和指令部分。
    question = f"Question:\nIs the second sentence entailed by the first sentence?\n"
    context = f"First sentence: {data['passage'][0]}\nSecond sentence: {data['passage'][1]}\n"
    instruction = f"Requirement:\nPlease respond with either 'Yes' or 'No'.\n"
    answer_prompt = f"Answer:\n"
    text = question + context + instruction + answer_prompt

    # processed_correct_answer, correct_answer在评测时并不会使用，此处为展示对应逻辑
    processed_correct_answer = correct_answer = [key for key, value in data["target_scores"].items() if value == 1][0].strip()
    return {"input": text, "output": correct_answer, "processed_output": processed_correct_answer}
```