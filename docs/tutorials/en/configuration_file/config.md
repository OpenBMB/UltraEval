## Overview of the Configuration File

UltraEval selects specific tasks as the minimum unit for evaluation, allowing users to choose different tasks for evaluation simultaneously. We use configuration files (config) to dictate how each task is evaluated, for example, fewshot, metric, hyperparameters, etc. These parameter configurations are implemented through configuration files located at specified paths, organized in JSON format with the path format as `datasets/dataset_name/config/{task_name}_{gen/ppl}.json`. Here, each configuration file defines a complete set of parameters for a specific task. This approach ensures complete decoupling between the configuration files and the models.

Taking the configuration file for the tydiqa task as an example, we detail each property (where values related to paths are within the UltraEval directory):

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

- **task_name**: The name of the task. This name must be consistent with the `task_name` in the path `datasets/dataset_name/config/{task_name}_{gen/ppl}.json`. Here, `task_name` refers to the name of a specific task under `dataset_name`; if there is only one task under `dataset_name`, then `task_name` should be set the same as `dataset_name`.
- **path**: The data path, strictly corresponding to the task. The data for evaluation tasks is generated in UltraEval format by make_dataset.py, see [Introduction to make_dataset](./make_dataset.md) for details.
- **description**: A prompt of string type required for the task, can be empty. For example, for the `Biology-MCQs` task in the `gaokaobench` dataset, the official description provided is as follows:

```
请你做一道生物选择题\n请你一步一步思考并将思考过程写在【解析】和<eoe>之间。你将从A，B，C，D中选出正确的答案，并写在【答案】和<eoa>之间。\n例如：【答案】: A <eoa>\n完整的题目回答的格式如下：\n【解析】 ... <eoe>\n【答案】 ... <eoa>\n请你严格按照上述格式作答。\n题目如下：
```

- **transform**: The path to the data format transformation file. After reading task data from `path`, the transform.py file at this path converts each data item into a prompt format input to the model. See [Introduction to transform](./transform.md) for details.
- **fewshot**: The number of few-shot examples, 0 for zero-shot, 5 for five-shot. It means concatenating multiple data items (questions + answers) processed by transform, placing them before the final question.
- **generate**: The method of model evaluation.
  - The `method` field can be `generate` or `loglikelihood`, corresponding to gen and ppl methods respectively. The gen method requires the model to output generated content, while the ppl method concatenates the prompt with each option, calculating the negative log probability of the model for each option separately.
  - The `params` field allows for task-specific model inference parameters, such as `models/model_params/vllm_beamsearch.json`. See [Introduction to model_params](./model_params.md) for details.
- **postprocess**: The method for post-processing the generated content. It needs to be registered and implemented in `tasks/postprocess.py`. See [Introduction to postprocess](./postprocess.md) for details.
- **metric**: The computation metrics. Follows the dictionary format below, where
  - `user_designed_name` can be customized as needed. This dictionary contains two main fields:
    - **Evaluation**: Evaluates the model's output for each instance. The number of model outputs is controlled by the `params` in the `generate` field, specifically by the `sampling_num` field in each parameter file, typically set to 1, indicating only one output is generated per instance. However, for tasks like `HumanEval` calculating `pass@k`, `sampling_num` changes accordingly when k is greater than 1.
      - `metric_name` needs to be registered in `metric/__init__.py` and implemented in the corresponding `{metric_name}.py` file. For specific details,refer to [Introduction to metric](./metric.md).
    - **Aggregation**: Aggregates all evaluation results for each instance, with the default operation being to take the average. In certain special cases (for example, `humaneval`, `mbpp`), `pass_k` may be chosen as the aggregation method.

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
