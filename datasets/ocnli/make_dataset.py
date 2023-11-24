import json
import os


def transform_entry(data_entry):
    target_scores = {
        "矛盾": int(data_entry["label"] == "contradiction"),
        "无关": int(data_entry["label"] == "neutral"),
        "蕴含": int(data_entry["label"] == "entailment"),
    }
    if 1 not in list(target_scores.values()):
        return None
    return {
        "passage": [data_entry["sentence1"], data_entry["sentence2"]],
        "question": "",
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
    input_path = "../../RawData/ocnli/dev.json"
    output_path = "./data/ocnli.jsonl"
    input_file_path = os.path.join(script_dir, input_path)
    output_file_path = os.path.join(script_dir, output_path)
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
    convert(input_file_path, output_file_path)


if __name__ == "__main__":
    main()
