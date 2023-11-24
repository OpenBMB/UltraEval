import json
import os


def transform_entry(entry1, entry2):
    return {
        "passage": [entry1, entry2],
        "question": "",
        "target_scores": {},
        "answer": "",
    }


def convert(input_file_path1, input_file_path2, output_file_path):
    with open(input_file_path1, "r", encoding="utf-8") as infile1, open(
        input_file_path2, "r", encoding="utf-8"
    ) as infile2, open(output_file_path, "w", encoding="utf-8") as outfile:
        for line1, line2 in zip(infile1, infile2):
            transformed_entry = transform_entry(line1.strip(), line2.strip())
            outfile.write(json.dumps(transformed_entry, ensure_ascii=False) + "\n")


def main():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    input_path1 = "../../RawData/flores/devtest/eng_Latn.devtest"
    input_path2 = "../../RawData/flores/devtest/zho_Hans.devtest"
    output_path = "./data/flores.jsonl"
    input_file_path1 = os.path.join(script_dir, input_path1)
    input_file_path2 = os.path.join(script_dir, input_path2)
    output_file_path = os.path.join(script_dir, output_path)
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
    convert(input_file_path1, input_file_path2, output_file_path)


if __name__ == "__main__":
    main()
