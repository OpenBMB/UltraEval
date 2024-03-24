## Adding New Datasets


- **Introducing Official Datasets**
  - First, place the official dataset files in the `RawData/{dataset_name}` directory. This is the first step in preparing data, ensuring the integrity and accessibility of the original data. Please note, it's recommended to use "-" instead of "_" in `dataset_name` and `task_name`.
- **Writing the make_dataset.py Script**
  - Create a new folder for your dataset in the `datasets/` directory, `datasets/{dataset_name}/`.
  - Refer to the [make_dataset introduction](../configuration_file/make_dataset.md) tutorial to write the corresponding data creation logic in `datasets/{dataset_name}/make_dataset.py`.
  - Running the `make_dataset.py` script will convert the raw data into the format required by the UltraEval framework. After conversion, all tasks in your dataset will appear in the `datasets/{dataset_name}/data/` directory as UltraEval format `.jsonl` files. These files will be named after the task names, in the format `task_name.jsonl`.