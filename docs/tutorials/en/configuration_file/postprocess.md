## Post-Processing

Post-process the model's output to meet the requirements of different evaluation methods.

Before computing the evaluation metric (metric), UltraEval performs necessary post-processing on the model's output. This post-processing process is divided into two levels: model-level post-processing and task-level post-processing. This process is implemented through the postprocess.py file.

- **Model-level post-processing**: Outputs from different models may vary, so it's essential to uniformly extract the actual model output.
- **Task-level post-processing** (optional depending on the task): This step focuses on extracting or normalizing the model output more precisely to enable more accurate comparison with the correct answer, thereby calculating more accurate evaluation metrics.

The "post-processing" mentioned in this section generally refers to task-level post-processing. Task-level post-processing is specified through the postprocess setting in the config. Model-level post-processing can be set through the `postprocess` parameter in the `main` file.

In the `tasks/postprocess.py` file, we define various post-processing methods for selection and application.

**Taking UntilReturnPost as an example:**

```
class UntilReturnPost:
    def __init__(self):
        pass

    def __call__(self, raw_outputs, processed_outputs):
        # Redefine the __call__ method for processing outputs
        processed_outputs_ = []
        
        # If processed_outputs is of string type, convert it to a list for uniform processing
        if isinstance(processed_outputs, str):  
            processed_outputs = [processed_outputs]
        
        # Iterate through the processed outputs
        for output in processed_outputs:
            # Remove leading and trailing whitespace for each output, then take the content before the first newline and remove whitespace again
            output = output.strip().split('\n')[0].strip()
            processed_outputs_.append(output)

        # Return both the raw outputs and the processed outputs
        return raw_outputs, processed_outputs_

# Note: Custom post-processing classes need to be registered in POSTPROCESS_REGISTRY
```
