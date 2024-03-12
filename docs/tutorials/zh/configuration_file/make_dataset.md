## 数据预处理

对任务数据进行预处理，规整格式，最终的结果对应于config文件中的path路径。

UltraEval对来自HuggingFace、数据集GitHub官网等权威公开渠道的原始数据集，进行统一格式化处理，以确保评测数据的可溯源和透明度。这些处理步骤在 `datasets/{dataset_name}/make_dataset.py` 中进行，原始数据集下载后保留在 `RawData/` 目录下。

以下是UltraEval通常保留的字段说明：

- **passage**: 补充信息，除问题之外的其他文本。
- **question**: 问题。
- **target_scores**: （选择题类型任务）选项及正确答案。字典形式，键为不同选项的得分，正确选项的值为1，错误选项为0。在PPL评测方式中，这些选项会直接拼接到模型输入的句子末尾，以计算各选项的负对数概率（negative loglikelihood）。特别注意，当任务要求将选项插入句子中间而非末尾时，应特别处理，可参考 `chid` 数据集的实现方式（即target_scores中的所有键为选项及后续句子的拼接）。
- **answer**: （填空题类型任务）正确答案。

注：当任务为单项选择题的时候，answer通常为空字符串；当任务为填空题时，target_scores通常为空字典。对于多项选择题的处理，可参考`agieval` 数据集中`gaokao-physics`任务的实现方式 ，此时同时保留了target_score字段（用以存放选项）和answer字段（用以存放答案）。另外，用户可以根据个人需求自定义其他字段，但需确保这些字段与同一数据集目录下的 `transform.py`中的字段保持逻辑上的一致性。

- 以ax-b为例：

```
import json
import os

def transform_entry(data_entry):
    # ax-b数据集关注于判断两个句子之间的蕴含关系。它提供的回答是有限的，因此选择将其处理成选择题的形式。
    # 在这里，我们使用target_scores字段来表示每个选项（"Yes"或"No"）是否正确，同时将answer字段置为空字符串。
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
    # 打开输入文件和输出文件，以进行读取和写入操作。
    # 输入文件是官方提供的原始格式数据，输出文件是转换后的UltraEval版的JSONL格式。
    with open(input_file_path, 'r', encoding='utf-8') as infile, \
         open(output_file_path, 'w', encoding='utf-8') as outfile:
        for line in infile:
            # 对于输入文件的每一行，将其转换成JSON格式，然后应用transform_entry函数进行UltraEval格式化处理。
            data_entry = json.loads(line.strip())
            transformed_entry = transform_entry(data_entry)
            outfile.write(json.dumps(transformed_entry, ensure_ascii=False) + '\n')

def main():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    # 定义官方数据集的路径和转换后的数据集路径。
    # 注意，转换后的数据应保持为JSONL格式。
    # 当一个数据集包含多个子任务时，可参考mmlu数据集的处理方式，并确保每个子任务对应一个JSONL文件。
    input_path = '../../RawData/ax-b/AX-b.jsonl'
    output_path = './data/ax-b.jsonl'
    input_file_path = os.path.join(script_dir, input_path)
    output_file_path = os.path.join(script_dir, output_path)
    convert(input_file_path, output_file_path)

if __name__ == "__main__":
    main()
```

用户使用时，既可以单独运行特定数据集的`make_dataset.py`来对单一数据集进行UltraEval格式的任务集创建，也可以运行主目录下的`data_process.py`实现全部数据集的UltraEval格式的数据集创建。