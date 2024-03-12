## 添加新数据集


- **引入官方数据集**
  - 首先，将官方数据集文件放置到 `RawData/{dataset_name}` 目录下。这是准备数据的第一步，确保原始数据的完整性和可访问性。请注意，`dataset_name`及`task_name`中不建议出现"_"，需以"-"替代。
- **编写 make_dataset.py 脚本**
  - 在 `datasets/` 目录下为你的数据集创建一个新的文件夹 `datasets/{``dataset_name}/`。
  - 参照[【make_dataset介绍】](../configuration_file/make_dataset.md)教程，在 `datasets/{dataset_name}/make_dataset.py` 中编写相应的创建数据逻辑。
  - 运行 `make_dataset.py` 脚本可以将原始数据转换成UltraEval框架所需的格式。完成转换后，你的数据集中的所有任务将以UltraEval格式的 `.jsonl` 文件形式出现在 `datasets/{dataset_name}/data/` 目录下。这些文件将按照任务名称命名，格式为 `task_name.jsonl`。
