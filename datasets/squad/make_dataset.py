import json
import os


def transform_entry(data_entry):
    return {
        "passage": [data_entry["title"], data_entry["ctx"]],
        "question": data_entry["question"],
        "target_scores": {},
        "answer": data_entry["answer"],
    }


def convert(input_file_path, output_file_path):
    with open(input_file_path, "r", encoding="utf-8") as file:
        dataset = json.load(file)
        data = dataset["data"]

        with open(output_file_path, "w", encoding="utf-8") as outfile:
            for dat in data:
                title = dat["title"]
                para = dat["paragraphs"]
                for single in para:
                    ctx = single["context"]
                    qas = single["qas"]
                    for ques in qas:
                        answers = set()
                        if "answers" in ques and len(ques["answers"]) != 0:
                            for ans in ques["answers"]:
                                answers.add(ans["text"])
                        # elif 'plausible_answers' in ques:
                        #     for ans in ques['plausible_answers']:
                        #         answers.add(ans['text'])

                        entry = {
                            "title": title,
                            "ctx": ctx,
                            "question": ques["question"],
                            "answer": list(answers),
                        }
                        if len(entry["answer"]) == 0:
                            continue

                        new_entry = transform_entry(entry)
                        outfile.write(json.dumps(new_entry, ensure_ascii=False) + "\n")


def main():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    input_path = "../../RawData/squad/dev-v2.0.json"
    output_path = "./data/squad.jsonl"
    input_file_path = os.path.join(script_dir, input_path)
    output_file_path = os.path.join(script_dir, output_path)
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
    convert(input_file_path, output_file_path)


if __name__ == "__main__":
    main()
