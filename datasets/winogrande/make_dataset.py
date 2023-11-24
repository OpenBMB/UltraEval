import json
import os


def transform_entry(data_entry):
    question = data_entry["sentence"].split("_")[0]
    option1 = data_entry["option1"] + data_entry["sentence"].split("_")[1]
    option2 = data_entry["option2"] + data_entry["sentence"].split("_")[1]
    answer = data_entry["answer"]

    target_scores = {option1: int(answer == "1"), option2: int(answer == "2")}

    return {
        "passage": "",
        "question": question,
        "target_scores": target_scores,
        "answer": "",
    }


def convert(input_file_path, output_file_path):
    with open(input_file_path, "r", encoding="utf-8") as file:
        with open(output_file_path, "w", encoding="utf-8") as outfile:
            for line in file:
                entry = json.loads(line)
                new_entry = transform_entry(entry)
                outfile.write(json.dumps(new_entry, ensure_ascii=False) + "\n")


def main():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    input_path = "../../RawData/winogrande/dev.jsonl"
    output_path = "./data/winogrande.jsonl"
    input_file_path = os.path.join(script_dir, input_path)
    output_file_path = os.path.join(script_dir, output_path)
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
    convert(input_file_path, output_file_path)


if __name__ == "__main__":
    main()
