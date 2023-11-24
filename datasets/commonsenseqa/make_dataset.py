import json
import os


def transform_entry(data_entry):
    target_scores = {
        choice["text"]: int(choice["label"] == data_entry["answerKey"])
        for choice in data_entry["question"]["choices"]
    }
    if 1 not in target_scores.values():
        return None
    return {
        "passage": "",
        "question": data_entry["question"]["stem"],
        "target_scores": target_scores,
        "answer": "",
    }


def convert(input_file_path, output_file_path):
    with open(input_file_path, "r", encoding="utf-8") as infile, open(
        output_file_path, "w", encoding="utf-8"
    ) as outfile:
        for line in infile:
            data_entry = json.loads(line.strip())
            transformed_entry = transform_entry(data_entry)
            if transformed_entry:
                outfile.write(json.dumps(transformed_entry, ensure_ascii=False) + "\n")


def main():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    input_path = "../../RawData/commonsenseqa/dev_rand_split.jsonl"
    output_path = "./data/commonsenseqa.jsonl"
    input_file_path = os.path.join(script_dir, input_path)
    output_file_path = os.path.join(script_dir, output_path)
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
    convert(input_file_path, output_file_path)


if __name__ == "__main__":
    main()
