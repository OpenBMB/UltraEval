## Data Preprocessing

Preprocess task data to standardize its format, with the final result corresponding to the path specified in the config file.

UltraEval performs unified format processing on raw datasets from authoritative public channels such as HuggingFace and dataset GitHub official websites, to ensure traceability and transparency of evaluation data. These processing steps are carried out in `datasets/{dataset_name}/make_dataset.py`, with the original datasets retained in the `RawData/` directory after download.

Below are the commonly retained fields explained for UltraEval:

- **passage**: Supplementary information, other text besides the question.
- **question**: The question.
- **target_scores**: (For multiple-choice type tasks) Options and the correct answer. This is a dictionary where keys are different options' scores, with the correct option having a value of 1, and incorrect options 0. In PPL evaluation mode, these options are directly appended to the sentence input to the model, to calculate the negative loglikelihood of each option. Note that when the task requires inserting options into the middle of a sentence rather than at the end, it should be specially handled. Refer to the implementation for the `chid` dataset (i.e., all keys in target_scores are the concatenation of an option and subsequent sentences).
- **answer**: (For fill-in-the-blank type tasks) The correct answer.

Note: For single-choice questions, the answer is usually an empty string; for fill-in-the-blank tasks, target_scores is usually an empty dictionary. For processing multiple-choice questions, refer to the implementation of the `gaokao-physics` task in the `agieval` dataset, where both target_score (to store options) and answer (to store the correct answer) fields are retained. Additionally, users can customize other fields as per their requirements, but must ensure these fields are logically consistent with the fields in `transform.py` in the same dataset directory.

- Taking ax-b as an example:

```
import json
import os

def transform_entry(data_entry):
    # The ax-b dataset focuses on judging the entailment relationship between two sentences. It provides limited answers, hence we choose to format it as a multiple-choice question.
    # Here, we use the target_scores field to indicate whether each option ("Yes" or "No") is correct, while setting the answer field to an empty string.
    return {
        "passage": [data_entry["sentence1"], data_entry["sentence2"]],
        "question": "",
        "target_scores": {
            "Yes": int(data_entry["label"] == "entailment"),
            "No": int(data_entry["label"] == "not_entailment")
        },
        "answer": ""
    }

def convert(input_file_path, output_file_path):
    # Open the input and output files for reading and writing operations.
    # The input file is the official raw format data, and the output file is the converted UltraEval version in JSONL format.
    with open(input_file_path, 'r', encoding='utf-8') as infile, \
         open(output_file_path, 'w', encoding='utf-8') as outfile:
        for line in infile:
            # For each line in the input file, convert it to JSON format, then apply the transform_entry function for UltraEval formatting.
            data_entry = json.loads(line.strip())
            transformed_entry = transform_entry(data_entry)
            outfile.write(json.dumps(transformed_entry, ensure_ascii=False) + '\n')

def main():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    # Define the paths for the official dataset and the converted dataset.
    # Note, the converted data should remain in JSONL format.
    # When a dataset includes multiple subtasks, refer to the handling method for the mmlu dataset, ensuring each subtask corresponds to a JSONL file.
    input_path = '../../RawData/ax-b/AX-b.jsonl'
    output_path = './data/ax-b.jsonl'
    input_file_path = os.path.join(script_dir, input_path)
    output_file_path = os.path.join(script_dir, output_path)
    convert(input_file_path, output_file_path)

if __name__ == "__main__":
    main()
```

Users can either run `make_dataset.py` for a specific dataset individually to create an UltraEval format task set for a single dataset, or run `data_process.py` in the main directory to create UltraEval format datasets for all datasets.