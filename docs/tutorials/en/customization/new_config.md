## Building New Configuration Files

- **Writing transform.py script**
  - Refer to the [Introduction to transform](../configuration_file/transform.md) tutorial, and write the corresponding data transformation logic in `datasets/{dataset_name}/transform_{gen/ppl}.py`.
- **Adding configuration files**
  - After adding datasets and prompts, you generally can add a configuration file to complete the new task (for custom post-processing and metrics, see below). Refer to the [Configuration file](../configuration_file/config.md) tutorial, and configure the dataset parameters in `datasets/{dataset_name}/config/{task_name}_{gen/ppl}.json`.
- **Viewing Task Format**
  - Users can use UltraEval’s `tasks/view_task.py` script to view the task organization format. First, set the environment variable `export PYTHONPATH="/tasks:$PYTHONPATH"`, then run `python tasks/view_task.py --config datasets/{dataset_name}/config/{task_name}_{gen/ppl}.json` to view the specific configuration’s task format. Note: When the evaluation method is PPL, the logic of `view_task.py` is to concatenate the `processed_output` field from `transform.py` as the correct answer, so ensure that the `processed_output` field in your code is `[key for key, value in data["target_scores"].items() if value == 1][0]` (consistent with the actual evaluation logic).