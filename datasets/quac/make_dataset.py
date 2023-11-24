import json
import os


def transform_entry(data_entry):
    title = data_entry["title"]
    section_title = data_entry["section_title"]
    paragraph = data_entry["paragraphs"][0]["context"]

    questions_answers = data_entry["paragraphs"][0]["qas"]

    transformed_entries = []
    for qa in questions_answers:
        entry = {
            "passage": [title, section_title, paragraph],
            "question": qa["question"],
            "target_scores": {},
            "answer": [ans["text"] for ans in qa["answers"]],
        }
        transformed_entries.append(entry)
    return transformed_entries


def convert(input_file_path, output_file_path):
    with open(input_file_path, "r", encoding="utf-8") as file:
        data = json.load(file)["data"]
        with open(output_file_path, "w", encoding="utf-8") as outfile:
            for entry in data:
                transformed_entries = transform_entry(entry)
                for te in transformed_entries:
                    outfile.write(json.dumps(te, ensure_ascii=False) + "\n")


def main():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    input_path = "../../RawData/quac/val_v0.2.json"
    output_path = "./data/quac.jsonl"
    input_file_path = os.path.join(script_dir, input_path)
    output_file_path = os.path.join(script_dir, output_path)
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
    convert(input_file_path, output_file_path)


if __name__ == "__main__":
    main()
