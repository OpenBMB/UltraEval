import json
import os


def transform_entry(data_entry):
    return {
        "passage": "",
        "question": data_entry["question"],
        "target_scores": {
            value: int(data_entry["answer_idx"] == key)
            for key, value in data_entry["options"].items()
        },
        "answer": "",
    }


def convert(input_file_path, output_file_path):
    with open(input_file_path, "r", encoding="utf-8") as infile, open(
        output_file_path, "w", encoding="utf-8"
    ) as outfile:
        for line in infile:
            data_entry = json.loads(line.strip())
            transformed_entry = transform_entry(data_entry)
            outfile.write(json.dumps(transformed_entry, ensure_ascii=False) + "\n")


def main():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    input_path = (
        "../../RawData/medqa/questions/US/4_options/phrases_no_exclude_test.jsonl"
    )
    output_path = "./data/medqa-usmle.jsonl"
    input_file_path = os.path.join(script_dir, input_path)
    output_file_path = os.path.join(script_dir, output_path)
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
    convert(input_file_path, output_file_path)


if __name__ == "__main__":
    main()
