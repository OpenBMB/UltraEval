import json
import os


def load_theorems(theorems_file_path):
    with open(theorems_file_path, "r", encoding="utf-8") as file:
        theorems_data = json.load(file)
        return {key.lower(): value for key, value in theorems_data.items()}


def transform_entry(data_entry, theorems):
    theorem_key = data_entry["theorem"].lower()
    if theorem_key not in theorems:
        raise ValueError(
            f"Theorem '{data_entry['theorem']}' not found in theorems dictionary."
        )
    return {
        "passage": theorems[theorem_key],
        "question": data_entry["Question"],
        "target_scores": {},
        "answer": [data_entry["Answer_type"], data_entry["Answer"]],
    }


def convert(input_file_path, output_file_path, theorems):
    with open(input_file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
        with open(output_file_path, "w", encoding="utf-8") as outfile:
            for entry in data:
                new_entry = transform_entry(entry, theorems)
                outfile.write(json.dumps(new_entry, ensure_ascii=False) + "\n")


def main():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    input_path = "../../RawData/theoremqa/theoremqa_test.json"
    theorems_path = "../../RawData/theoremqa/all_theorems.json"
    output_path = "./data/theoremqa.jsonl"
    input_file_path = os.path.join(script_dir, input_path)
    theorems_file_path = os.path.join(script_dir, theorems_path)
    output_file_path = os.path.join(script_dir, output_path)

    theorems = load_theorems(theorems_file_path)
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
    convert(input_file_path, output_file_path, theorems)


if __name__ == "__main__":
    main()
