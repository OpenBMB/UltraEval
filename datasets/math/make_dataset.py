import json
import os


def transform_entry(data_entry):
    return {
        "passage": "",
        "question": data_entry["problem"],
        "target_scores": {},
        "answer": data_entry["solution"],
    }


def convert(input_folder_path, output_folder_path):
    for folder_name in os.listdir(input_folder_path):
        folder_path = os.path.join(input_folder_path, folder_name)
        output_file_path = os.path.join(
            output_folder_path, folder_name.replace("_", "-").replace(".json", ".jsonl")
        )
        with open(output_file_path, "w", encoding="utf-8") as outfile:
            with open(folder_path, "r") as infile:
                data_entry = json.load(infile)
            for ins in data_entry:
                new_entry = transform_entry(ins)
                outfile.write(json.dumps(new_entry, ensure_ascii=False) + "\n")


def main():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    input_path = "../../RawData/math/test"
    output_path = "./data/"
    input_folder_path = os.path.join(script_dir, input_path)
    output_folder_path = os.path.join(script_dir, output_path)
    os.makedirs(output_folder_path, exist_ok=True)
    convert(input_folder_path, output_folder_path)


if __name__ == "__main__":
    main()
