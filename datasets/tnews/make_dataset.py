import json
import os


def load_label_mappings(label_mappings_path):
    en_to_zh_labels = {}
    with open(label_mappings_path, "r", encoding="utf-8") as file:
        for line in file:
            entry = json.loads(line.strip())
            en_to_zh_labels[entry["label_desc"]] = entry["label_zh"]
    return en_to_zh_labels


def transform_entry(data_entry, label_mappings):
    target_scores = {label + "新闻": 0 for label in label_mappings.values()}
    zh_label = label_mappings.get(data_entry["label_desc"], "") + "新闻"
    target_scores[zh_label] = 1

    return {
        "passage": "",
        "question": data_entry["sentence"],
        "target_scores": target_scores,
        "answer": "",
    }


def convert(input_file_path, output_file_path, label_mappings):
    with open(input_file_path, "r", encoding="utf-8") as infile, open(
        output_file_path, "w", encoding="utf-8"
    ) as outfile:
        for line in infile:
            data_entry = json.loads(line.strip())
            transformed_entry = transform_entry(data_entry, label_mappings)
            outfile.write(json.dumps(transformed_entry, ensure_ascii=False) + "\n")


def main():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    input_path = "../../RawData/tnews/test_public.json"
    label_mappings_path = "../../RawData/tnews/label_index2en2zh.json"
    output_path = "./data/tnews.jsonl"
    input_file_path = os.path.join(script_dir, input_path)
    label_mappings_file_path = os.path.join(script_dir, label_mappings_path)
    output_file_path = os.path.join(script_dir, output_path)

    label_mappings = load_label_mappings(label_mappings_file_path)
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
    convert(input_file_path, output_file_path, label_mappings)


if __name__ == "__main__":
    main()
