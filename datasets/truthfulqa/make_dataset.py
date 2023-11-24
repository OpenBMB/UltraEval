import json
import os


def transform_entry(data_entry, mc_type):
    return {
        "passage": "",
        "question": data_entry["question"],
        "target_scores": data_entry[f"{mc_type}_targets"],
        "answer": "",
    }


def convert(input_file_path, output_file_path, mc_type):
    with open(input_file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
        with open(output_file_path, "w", encoding="utf-8") as outfile:
            for entry in data:
                new_entry = transform_entry(entry, mc_type)
                outfile.write(json.dumps(new_entry, ensure_ascii=False) + "\n")


def main():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    input_path = "../../RawData/truthfulqa/mc_task.json"
    mc1_output_path = "./data/mc1.jsonl"
    mc2_output_path = "./data/mc2.jsonl"

    input_file_path = os.path.join(script_dir, input_path)
    mc1_output_file_path = os.path.join(script_dir, mc1_output_path)
    mc2_output_file_path = os.path.join(script_dir, mc2_output_path)
    os.makedirs(os.path.dirname(mc1_output_file_path), exist_ok=True)
    convert(input_file_path, mc1_output_file_path, "mc1")
    convert(input_file_path, mc2_output_file_path, "mc2")


if __name__ == "__main__":
    main()
