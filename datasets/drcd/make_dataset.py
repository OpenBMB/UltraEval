import json
import os


def transform_entry(data_entry):
    transformed_entries = []

    for qa in data_entry["qas"]:
        question = qa["question"]
        answers = [answer["text"] for answer in qa["answers"]]

        entry = {
            "passage": data_entry["context"],
            "question": question,
            "target_scores": {},
            "answer": answers,
        }
        transformed_entries.append(entry)

    return transformed_entries


def convert(input_file_path, output_file_path):
    with open(input_file_path, "r", encoding="utf-8") as infile, open(
        output_file_path, "w", encoding="utf-8"
    ) as outfile:
        data_entries = json.load(infile)
        for data_entry in data_entries["data"]:
            for single_data_entry in data_entry["paragraphs"]:
                transformed_entries = transform_entry(single_data_entry)
                for transformed_entry in transformed_entries:
                    outfile.write(
                        json.dumps(transformed_entry, ensure_ascii=False) + "\n"
                    )


def main():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    input_path = "../../RawData/drcd/dev.json"
    output_path = "./data/drcd.jsonl"
    input_file_path = os.path.join(script_dir, input_path)
    output_file_path = os.path.join(script_dir, output_path)
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
    convert(input_file_path, output_file_path)


if __name__ == "__main__":
    main()
