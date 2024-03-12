## 构建新配置文件


- **编写transform.py脚本**
  - 参照[【 transform介绍】](../configuration_file/transform.md)教程，在 `datasets/{dataset_name}/transform_{gen/ppl}.py` 中编写相应的数据转换逻辑。
- **添加配置文件**
  - 完成添加数据集和提示词后，一般即可添加配置文件以完成新任务（如需自定义后处理和评测指标，详见下文）。参照[【config文件】](../configuration_file/config.md)教程，在`datasets/{dataset_name}/config/{task_name}_{gen/ppl}.json`中配置好数据集的各项参数。
- **查看任务格式**
  - 用户可以使用UltraEval的`tasks/view_task.py`脚本查看任务组织格式。首先，设置环境变量`export PYTHONPATH="/tasks:$PYTHONPATH"`，然后执行`python tasks/view_task.py --config datasets/{dataset_name}/config/{task_name}_{gen/ppl}.json`，查看特定配置的任务格式。请注意：评测方式为PPL时，`view_task.py`的逻辑是将`transform.py`中的`processed_output`字段作为正确答案拼接，因此请确保代码中的`processed_output`字段为`[key for key, value in data["target_scores"].items() if value == 1][0]`（与实际评测时的逻辑保持一致）。
