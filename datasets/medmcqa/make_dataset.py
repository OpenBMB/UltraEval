import json
import os


def transform_entry(data_entry):
    if data_entry["choice_type"] != "single":
        return None

    options = {chr(65 + i): data_entry[f"op{chr(97 + i)}"] for i in range(4)}
    correct_option_index = data_entry["cop"] - 1
    correct_option_key = chr(65 + correct_option_index)

    target_scores = {
        value: int(key == correct_option_key) for key, value in options.items()
    }
    if len(list(target_scores.keys())) != 4:
        return None
    return {
        "passage": data_entry.get("exp", ""),
        "question": data_entry["question"],
        "target_scores": target_scores,
        "answer": correct_option_key,
    }


def convert(input_file_path, output_file_path):
    with open(input_file_path, "r", encoding="utf-8") as file:
        with open(output_file_path, "w", encoding="utf-8") as outfile:
            for line in file:
                entry = json.loads(line)
                new_entry = transform_entry(entry)
                if new_entry:
                    outfile.write(json.dumps(new_entry, ensure_ascii=False) + "\n")


def main():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    input_path = "../../RawData/medmcqa/dev.json"
    output_path = "./data/medmcqa.jsonl"
    input_file_path = os.path.join(script_dir, input_path)
    output_file_path = os.path.join(script_dir, output_path)
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
    convert(input_file_path, output_file_path)


if __name__ == "__main__":
    main()
