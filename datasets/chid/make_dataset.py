import json
import os


def transform_entry(data_entry):
    input_data = data_entry["content"].split("#idiom#")[0]

    suffix = data_entry["content"].split("#idiom#")[1]
    target_scores = {
        candidate + suffix: int(idx == int(data_entry["answer"]))
        for idx, candidate in enumerate(data_entry["candidates"])
    }

    return {
        "passage": input_data,
        "question": "",
        "target_scores": target_scores,
        "answer": "",
    }


def convert(input_file_path, output_file_path):
    with open(input_file_path, "r", encoding="utf-8") as file:
        with open(output_file_path, "w", encoding="utf-8") as outfile:
            for line in file:
                data_entry = json.loads(line)
                new_entry = transform_entry(data_entry)
                outfile.write(json.dumps(new_entry, ensure_ascii=False) + "\n")


def main():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    input_path = "../../RawData/chid/test_public.json"
    output_path = "./data/chid.jsonl"
    input_file_path = os.path.join(script_dir, input_path)
    output_file_path = os.path.join(script_dir, output_path)
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
    convert(input_file_path, output_file_path)


if __name__ == "__main__":
    main()
