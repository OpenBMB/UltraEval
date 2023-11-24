import json
import os


def transform_entry(data_entry):
    return {
        "passage": [data_entry["doc"], data_entry["summary"]],
        "question": "",
        "target_scores": {
            "Yes": int(data_entry["label"] == 1),
            "No": int(data_entry["label"] == 0),
        },
        "answer": "",
    }


def convert(input_folder_path, output_folder_path):
    for file_name in os.listdir(input_folder_path):
        if file_name.endswith(".json"):
            output_file_name = (
                file_name.replace("summedits_", "")
                .replace(".json", ".jsonl")
                .replace("_", "-")
            )
            output_file_path = os.path.join(output_folder_path, output_file_name)

            with open(output_file_path, "w", encoding="utf-8") as outfile:
                input_file_path = os.path.join(input_folder_path, file_name)
                with open(input_file_path, "r", encoding="utf-8") as infile:
                    data_entries = json.load(infile)
                    for data_entry in data_entries:
                        new_entry = transform_entry(data_entry)
                        outfile.write(json.dumps(new_entry, ensure_ascii=False) + "\n")


def main():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    input_path = "../../RawData/summedits/summedits"
    output_path = "./data/"
    input_folder_path = os.path.join(script_dir, input_path)
    output_folder_path = os.path.join(script_dir, output_path)
    os.makedirs(output_folder_path, exist_ok=True)
    convert(input_folder_path, output_folder_path)


if __name__ == "__main__":
    main()
