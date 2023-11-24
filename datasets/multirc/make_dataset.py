import json
import os


def transform_entry(passage, question_data):
    entries = []
    for question in question_data:
        q_text = question["question"]
        for ans in question["answers"]:
            entry = {
                "passage": passage,
                "question": [q_text, ans["text"]],
                "target_scores": {
                    "Yes": int(ans["label"] == 1),
                    "No": int(ans["label"] == 0),
                },
                "answer": "",
            }
            entries.append(entry)
    return entries


def convert(input_file_path, output_file_path):
    with open(input_file_path, "r", encoding="utf-8") as infile, open(
        output_file_path, "w", encoding="utf-8"
    ) as outfile:
        for line in infile:
            data_entry = json.loads(line)
            passage_text = data_entry["passage"]["text"]
            questions = data_entry["passage"]["questions"]
            transformed_entries = transform_entry(passage_text, questions)
            for entry in transformed_entries:
                outfile.write(json.dumps(entry, ensure_ascii=False) + "\n")


def main():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    input_path = "../../RawData/multirc/val.jsonl"
    output_path = "./data/multirc.jsonl"
    input_file_path = os.path.join(script_dir, input_path)
    output_file_path = os.path.join(script_dir, output_path)
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
    convert(input_file_path, output_file_path)


if __name__ == "__main__":
    main()
