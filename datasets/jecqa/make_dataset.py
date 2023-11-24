import json
import os


def transform_entry(data_entry):
    if len(data_entry["answer"]) != 1:
        return None
    target_scores = {
        value: int(data_entry["answer"][0] == key)
        for key, value in data_entry["option_list"].items()
    }
    if len(list(target_scores.keys())) != 4:
        return None
    return {
        "passage": "",
        "question": data_entry["statement"],
        "target_scores": {
            value: int(data_entry["answer"][0] == key)
            for key, value in data_entry["option_list"].items()
        },
        "answer": "",
    }


def convert(input_file_path, output_file_path):
    with open(input_file_path, "r", encoding="utf-8") as infile, open(
        output_file_path, "a", encoding="utf-8"
    ) as outfile:
        for line in infile:
            data_entry = json.loads(line.strip())
            transformed_entry = transform_entry(data_entry)
            if transformed_entry:
                outfile.write(json.dumps(transformed_entry, ensure_ascii=False) + "\n")


def main():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    input_paths = [
        "../../RawData/jecqa/0_train.json",
        "../../RawData/jecqa/1_train.json",
    ]
    output_path = "./data/jecqa.jsonl"
    output_file_path = os.path.join(script_dir, output_path)

    if os.path.exists(output_file_path):
        os.remove(output_file_path)

    for input_path in input_paths:
        input_file_path = os.path.join(script_dir, input_path)
        os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
        convert(input_file_path, output_file_path)


if __name__ == "__main__":
    main()
