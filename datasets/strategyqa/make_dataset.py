import json
import os


def transform_entry(data_entry):
    return {
        "passage": [
            data_entry["term"],
            data_entry["description"],
            data_entry["facts"],
            data_entry["decomposition"],
        ],
        "question": data_entry["question"],
        "target_scores": {
            "Yes": int(data_entry["answer"]),
            "No": int(not data_entry["answer"]),
        },
        "answer": "",
    }


def convert(input_file_path, output_file_path):
    with open(input_file_path, "r", encoding="utf-8") as infile, open(
        output_file_path, "w", encoding="utf-8"
    ) as outfile:
        data_entries = json.load(infile)
        for data_entry in data_entries:
            transformed_entry = transform_entry(data_entry)
            outfile.write(json.dumps(transformed_entry, ensure_ascii=False) + "\n")


def main():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    input_path = "../../RawData/strategyqa/strategyqa_train.json"
    output_path = "./data/strategyqa.jsonl"
    input_file_path = os.path.join(script_dir, input_path)
    output_file_path = os.path.join(script_dir, output_path)
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
    convert(input_file_path, output_file_path)


if __name__ == "__main__":
    main()
