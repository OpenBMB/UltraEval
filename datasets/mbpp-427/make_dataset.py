import json
import os


def transform_entry(data_entry):
    return {
        "passage": "",
        "question": "",
        "target_scores": {},
        "answer": "",
        "text": data_entry["prompt"],
        "code": data_entry["code"],
        "task_id": data_entry["task_id"],
        "test_setup_code": "",
        "test_list": data_entry["test_list"],
        "challenge_test_list": "",
    }


def convert(input_file_path, output_file_path):
    with open(input_file_path, "r", encoding="utf-8") as infile, open(
        output_file_path, "w", encoding="utf-8"
    ) as outfile:
        for line in json.load(infile):
            data_entry = line
            transformed_entry = transform_entry(data_entry)
            outfile.write(json.dumps(transformed_entry, ensure_ascii=False) + "\n")


def main():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    input_path = "../../RawData/mbpp/sanitized-mbpp.json"
    output_path = "./data/mbpp.jsonl"
    input_file_path = os.path.join(script_dir, input_path)
    output_file_path = os.path.join(script_dir, output_path)
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
    convert(input_file_path, output_file_path)


if __name__ == "__main__":
    main()
