## Data Transformation

After data standardization, prompts are added to adapt to the requirements of different models and evaluation methods.

UltraEval uses the `datasets/{dataset_name}/transform.py` script to organize and create UltraEval format task sets, generating model input prompts suitable for different scenarios. This script processes each piece of data in the dataset and returns a dictionary containing the following fields:

- **input**: The input text that the model needs to process. This should be in string form.
- **output**: The correct answer used for concatenation with the input when few-shot is greater than 0. Data forming few-shot examples are also organized through this script.
- **processed_output**: The correct answer used for evaluation. The model's output, after post-processing in the metric, will be compared with processed_output to calculate the score for this piece of data.

When using the GEN evaluation method, most datasets' `output` and `processed_output` fields are typically the same. However, there are exceptions, such as when processing the `gsm8k` task, where the `processed_output` field requires additional post-processing based on the `output` field. This is because, in these special cases, the answer used for few-shot concatenation differs from the answer used for actual evaluation. This inconsistency mainly stems from the influence of factors such as Chain of Thought (CoT) or special extraction formats.

When using the PPL evaluation method, UltraEval only uses the `input` field and concatenates it with each key value in the `target_scores` field from the UltraEval format task set to calculate the negative loglikelihood of the entire sentence. In this case, the `output` and `processed_output` fields are not used.

For more efficient management, we have adopted a version-based naming convention for the `transform` scripts in our repository. For example, `datasets/{dataset_name}/transform_{gen/ppl}_v0.py` indicates that this script is the v0 version of the transform for that dataset and also declares the corresponding evaluation method. This naming strategy not only facilitates our continuous iteration and optimization of prompts to meet different needs but also allows us to retain older versions of prompts, thereby corresponding to the leaderboard and ensuring the transparency and traceability of the entire process.

**Taking ax-b as an example:**

- **For GEN-form tasks**

```
import random

def transform(data, num_sample: int, r: random.Random, dataset_name: string):
    # Construct the question, context, instruction, and options parts.
    question = f"Question:\nIs the second sentence entailed by the first sentence?\n"
    context = f"First sentence: {data['passage'][0]}\nSecond sentence: {data['passage'][1]}\n"
    instruction = f"Requirement:\nChoose and respond with the letter of the correct answer, including the parentheses.\n"
    options = "Options:\n"
    for idx, item in enumerate(data['target_scores'].keys()):
        options += f"({chr(65 + idx)}) {item}\n"
    answer_prompt = f"Answer:\n"
    text = question + context + instruction + options + answer_prompt

    # Determine the correct answer based on the target_scores field.
    index_of_correct_answer = list(data['target_scores'].values()).index(1)
    processed_correct_answer = correct_answer = f"({chr(65 + index_of_correct_answer)})"

    return {"input": text, "output": correct_answer, "processed_output": processed_correct_answer}
```

- **For PPL-form tasks**

```
import random

def transform(data, num_sample: int, r: random.Random, dataset_name: string):
    # Construct the question description, context, and instruction parts.
    question = f"Question:\nIs the second sentence entailed by the first sentence?\n"
    context = f"First sentence: {data['passage'][0]}\nSecond sentence: {data['passage'][1]}\n"
    instruction = f"Requirement:\nPlease respond with either 'Yes' or 'No'.\n"
    answer_prompt = f"Answer:\n"
    text = question + context + instruction + answer_prompt

    # processed_correct_answer and correct_answer are not used during evaluation, shown here for corresponding logic
    processed_correct_answer = correct_answer = [key for key, value in data["target_scores"].items() if value == 1][0].strip()
    return {"input": text, "output": correct_answer, "processed_output": processed_correct_answer}
```
