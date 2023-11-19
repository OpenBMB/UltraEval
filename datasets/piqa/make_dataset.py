import json
import os


def transform_entry(data_entry, label):
    options = [data_entry["sol1"], data_entry["sol2"]]
    correct_option = options[label]
    target_scores = {option: int(option == correct_option) for option in options}

    return {
        "passage": "",
        "question": data_entry["goal"],
        "target_scores": target_scores,
        "answer": "",
    }


def convert(jsonl_file_path, lst_file_path, output_file_path):
    with open(jsonl_file_path, "r", encoding="utf-8") as jsonl_file, open(
        lst_file_path, "r"
    ) as lst_file, open(output_file_path, "w", encoding="utf-8") as outfile:
        for jsonl_line, lst_line in zip(jsonl_file, lst_file):
            data_entry = json.loads(jsonl_line.strip())
            label = int(lst_line.strip())
            transformed_entry = transform_entry(data_entry, label)
            outfile.write(json.dumps(transformed_entry, ensure_ascii=False) + "\n")


def main():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    jsonl_path = "../../RawData/piqa/valid.jsonl"
    lst_path = "../../RawData/piqa/valid-labels.lst"
    output_path = "./data/piqa.jsonl"
    jsonl_file_path = os.path.join(script_dir, jsonl_path)
    lst_file_path = os.path.join(script_dir, lst_path)
    output_file_path = os.path.join(script_dir, output_path)
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
    convert(jsonl_file_path, lst_file_path, output_file_path)


if __name__ == "__main__":
    main()
