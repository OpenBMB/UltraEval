import json
import os


def transform_entry(data_entry):
    passage = [data_entry["title"], data_entry["context"]]
    question = data_entry["question"]
    answers = [answer["text"] for answer in data_entry["answers"]]

    return {
        "passage": passage,
        "question": question,
        "target_scores": {},
        "answer": answers,
    }


def convert(input_file_path, output_file_path):
    with open(input_file_path, "r", encoding="utf-8") as file:
        with open(output_file_path, "w", encoding="utf-8") as outfile:
            data = json.load(file)
            for article in data["data"]:
                for paragraph in article["paragraphs"]:
                    for qa in paragraph["qas"]:
                        if qa["id"].startswith("english"):
                            entry = transform_entry(
                                {
                                    "title": article["title"],
                                    "context": paragraph["context"],
                                    "question": qa["question"],
                                    "answers": qa["answers"],
                                }
                            )
                            outfile.write(json.dumps(entry, ensure_ascii=False) + "\n")


def main():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    input_path = "../../RawData/tydiqa/tydiqa-goldp-v1.1-dev.json"
    output_path = "./data/tydiqa.jsonl"
    input_file_path = os.path.join(script_dir, input_path)
    output_file_path = os.path.join(script_dir, output_path)
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
    convert(input_file_path, output_file_path)


if __name__ == "__main__":
    main()
