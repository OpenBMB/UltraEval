import json
import os


def transform_entry(data_entry):
    passage = data_entry["article"]
    questions = data_entry["questions"]
    options = data_entry["options"]
    answers = data_entry["answers"]

    new_entries = []
    for idx, question in enumerate(questions):
        target_scores = {
            option: int(option == options[idx][ord(answers[idx]) - ord("A")])
            for option in options[idx]
        }

        entry = {
            "passage": passage,
            "question": question,
            "target_scores": target_scores,
            "answer": "",
        }
        new_entries.append(entry)

    return new_entries


def convert(input_file_path, output_file_path):
    with open(output_file_path, "w", encoding="utf-8") as outfile:
        with open(input_file_path, "r", encoding="utf-8") as file:
            for line in file:
                data_entry = json.loads(line)
                new_entries = transform_entry(data_entry)
                for entry in new_entries:
                    outfile.write(json.dumps(entry, ensure_ascii=False) + "\n")


def main():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    input_dirs = [
        "../../RawData/race/test/high.jsonl",
        "../../RawData/race/test/middle.jsonl",
    ]
    output_paths = ["./data/high.jsonl", "./data/middle.jsonl"]

    for input_dir, output_path in zip(input_dirs, output_paths):
        input_dir_path = os.path.join(script_dir, input_dir)
        output_file_path = os.path.join(script_dir, output_path)
        os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
        convert(input_dir_path, output_file_path)


if __name__ == "__main__":
    main()
