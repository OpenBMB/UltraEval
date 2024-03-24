## Task Instantiation

Within the UltraEval framework, the evaluation of each dataset is conducted at the task level, which is the smallest granularity. Taking the MMLU dataset as an example, there are 57 tasks. In the tasks directory, we provide an `eval_task.py` script, which constructs an `EvalTask` class containing the following methods:

- `__init__`: In the initialization phase, this includes not only the assignment of various parameters but also the implementation of the transform method and post-processing methods.
- `construct_metrics`: Instantiates metrics defined in the config file.
- `construct_input`: Processes task data for prompts, including fewshot. This involves calling the transform method specified in the config.
- `yield_batch_requests`: Batches task data according to `batch_size`, packaging them into request objects, which include the following information:

```
class Request:
    def __init__(self, request_type, instances, params, raw_example):
        if request_type not in REQUEST_RETURN_LENGTHS.keys():
            raise NotImplementedError(
                "The request type {} is not implemented!".format(request_type)
            )

        self.request_type = request_type # The "method" attribute from config, indicating the inference method of the model
        self.instances = instances # Batched data after prompt processing
        self.params = params # Parameters for model inference
        self.raw_example = raw_example # The original data corresponding to the batched data above
```

- `run`: Combines the `yield_batch_requests` and `construct_input` methods to process data with prompts. It handles data in batches according to `batch_size`, sends them for model inference, and then post-processes the model's returned results.
- `evaluate`: Assesses the post-processed model output. This stage invokes the metric instantiated during the `construct_metrics` phase. The evaluation part calculates the results for each individual instance.
- `finish`: Calculates the final score for a task, generally by averaging the results of all instances. It also saves config and metric result information.