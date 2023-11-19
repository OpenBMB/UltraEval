import json
import os


def transform_entry(data_entry):
    question_info = data_entry[1][0]
    choices = question_info["choice"]
    answer = question_info["answer"]

    target_scores = {choice: int(choice == answer) for choice in choices}

    return {
        "passage": data_entry[0],
        "question": question_info["question"],
        "target_scores": target_scores,
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
    input_path = "../../RawData/c3/m-dev.json"
    output_path = "./data/mixed.jsonl"
    input_file_path = os.path.join(script_dir, input_path)
    output_file_path = os.path.join(script_dir, output_path)
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
    convert(input_file_path, output_file_path)

    input_path = "../../RawData/c3/d-dev.json"
    output_path = "./data/dialog.jsonl"
    input_file_path = os.path.join(script_dir, input_path)
    output_file_path = os.path.join(script_dir, output_path)
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
    convert(input_file_path, output_file_path)


if __name__ == "__main__":
    main()
