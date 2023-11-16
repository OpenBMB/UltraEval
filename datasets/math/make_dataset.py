import json
import os
import re

def transform_entry(data_entry):
    return {
        "passage": "",
        "question": data_entry['problem'],
        "target_scores": {},
        "answer": data_entry['solution'],
    }

def convert(input_folder_path, output_folder_path):
    for folder_name in os.listdir(input_folder_path):
        folder_path = os.path.join(input_folder_path, folder_name)
        if os.path.isdir(folder_path):
            output_file_path = os.path.join(output_folder_path, f"{folder_name.replace('_', '-')}.jsonl")
            with open(output_file_path, 'w', encoding='utf-8') as outfile:
                for file_name in os.listdir(folder_path):
                    file_path = os.path.join(folder_path, file_name)
                    with open(file_path, 'r', encoding='utf-8') as file:
                        data_entry = json.load(file)
                        new_entry = transform_entry(data_entry)
                        outfile.write(json.dumps(new_entry, ensure_ascii=False) + '\n')

def main():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    input_path = '../../RawData/math/test'
    output_path = './data/'
    input_folder_path = os.path.join(script_dir, input_path)
    output_folder_path = os.path.join(script_dir, output_path)
    os.makedirs(output_folder_path, exist_ok=True)
    convert(input_folder_path, output_folder_path)

if __name__ == "__main__":
    main()
