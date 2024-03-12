## config文件概述


UltraEval选择具体任务（task）作为最小粒度进行评测，用户可以同时选择不同的任务评测。我们通过配置文件（config）来规定每个任务是如何进行评测的，例如fewshot、metric、超参数等等。这些参数配置是通过指定路径下的配置文件来实现，配置文件以json格式组织，路径格式为 `datasets/dataset_name/config/{task_name}_{gen/ppl}.json` 。这里，每个配置文件都针对一个特定任务定义了完整的参数配置。这种方式确保了配置文件与模型之间的完全解耦。

以tydiqa任务的配置文件为例，我们详细介绍每个属性（以下涉及到路径的value均在UltraEval目录下）：

```json
{
    "task_name": "tydiqa",
    "path": "datasets/tydiqa/data/tydiqa.jsonl",
    "description": "",
    "transform": "datasets/tydiqa/transform_gen_v0.py",
    "fewshot": 0,
    "generate": {
        "method": "generate", 
        "params": ""
    },
    "postprocess": "exact_match_post",
    "metric": {
            "f1_score": {
                "evaluation": {
                    "type": "f1_score"
                }
            },
            "accuracy": {
                "evaluation": {
                    "type": "exact_match"
                }
            }
        }
}
```

- **task_name**: 任务名称。此名称需与对应路径`datasets/dataset_name/config/{task_name}_{gen/ppl}.json`中的`task_name`一致。这里的 `task_name` 指的是 `dataset_name` 下的特定任务的名称；如果 `dataset_name` 下仅有一个任务，则 `task_name` 应与 `dataset_name` 设置为相同。
- **path**: 数据路径，与任务严格对应。评测任务的数据是通过make_dataset.py生成的UltraEval格式数据，详情参见[【make_dataset介绍】](./make_dataset.md)。
- **description**: 任务所需的前置字符串类型提示（prompt），可为空。例如，对于`gaokaobench`数据集中的`Biology-MCQs`任务，其官方提供了以下描述：

```
请你做一道生物选择题\n请你一步一步思考并将思考过程写在【解析】和<eoe>之间。你将从A，B，C，D中选出正确的答案，并写在【答案】和<eoa>之间。\n例如：【答案】: A <eoa>\n完整的题目回答的格式如下：\n【解析】 ... <eoe>\n【答案】 ... <eoa>\n请你严格按照上述格式作答。\n题目如下：
```

- **transform**: 数据格式转换文件路径。从`path`读取任务数据后，通过此路径下的transform.py文件将每一条数据转换为输入到模型的prompt格式。详情参见[【transform介绍】](./transform.md)。
- **fewshot**: Few-shot数量，0表示zero-shot，5表示five-shot。表示将多个经过transform处理后的数据（问题+答案）拼接后，放在最终问题前。
- **generate**: 模型评测的方式。
  - `method`字段可选`generate`和`loglikelihood`，即gen和ppl两种方式。gen方式要求模型输出生成的内容，而ppl方式将prompt和每一个选项进行拼接，分别计算模型对选项的负对数概率。
  - `params`字段允许传入特定于任务的模型推理参数，如`models/model_params/vllm_beamsearch.json`。详情参见[【model_params介绍】](./model_params.md)。
- **postprocess**: 生成内容的后处理方式。需要在`tasks/postprocess.py`中注册并实现。详情参见[【postprocess介绍】](./postprocess.md)。
- **metric**: 计算指标。遵循以下字典格式，其中
  - `user_designed_name` 可根据需要自定义。该字典包含两个主要字段：
    - **评估（evaluation）**：对每个instance的模型输出进行评估。模型输出的数量是由 `generate` 字段中的 `params` 控制，具体为每个参数文件中的 `sampling_num` 字段，一般设置为 1，表示每个instance仅生成一条。但例如`HumanEval`任务计算`pass@k`，当k大于1时，`sampling_num`则随之改变。
      - `metric_name` 需要在 `metric/__init__.py` 中进行注册，并在相应的 `{metric_name}.py` 文件中实现具体的评估逻辑。具体细节可参考[【metric介绍】](./metric.md)。
    - **聚合（aggregation）**：对每个instance的所有评估结果进行聚合，默认操作是取平均值。在某些特殊情况下（例如 `humaneval`，`mbpp`），可能会选择 `pass_k` 作为聚合方式。

```
"user_designed_name": {
            "evaluation": {
                "type": "metric_name"
            },
            "aggregation": {
                "type": "aggregation_name"
            }
        }
```
