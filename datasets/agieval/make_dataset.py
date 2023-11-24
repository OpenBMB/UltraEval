import glob
import json
import os
import re


def extract_options(input_str):
    options = {}
    option_order = []

    pattern = re.compile(r"([A-D])[.．]?\s*((?:[^A-D\n]|(?!\n[A-D])[.．\n])+)")
    matches = pattern.findall(input_str)

    for match in matches:
        key, value = match
        options[key.strip().replace("\n", "")] = value.strip()
        option_order.append(key.strip())

    return options, option_order


def transform_entry(example, file_name):
    multi_choice_cases = ["gaokao-physics.jsonl", "jec-qa-ca.jsonl", "jec-qa-kd.jsonl"]
    cloze_cases = ["gaokao-mathcloze.jsonl", "math.jsonl"]
    deprecated_cases = ["sat-en-without-passage.jsonl"]

    if file_name in multi_choice_cases:
        if isinstance(example["label"], str):
            example["label"] = [example["label"]]
        answer = example["label"]
        target_scores = {}
        for option in example["options"]:
            key = option[3:]
            target_scores[key] = 1 if option[1] in example["label"] else 0
        if 1 not in target_scores.values():
            return None
        if list(target_scores.values()).count(1) != len(answer):
            return None

    elif file_name in cloze_cases:
        answer = example["answer"]
        target_scores = {}
    else:
        answer = ""
        target_scores = {}
        for option in example["options"]:
            key = option[3:]
            target_scores[key] = 1 if option[1] == example["label"] else 0

        if 1 not in target_scores.values():
            return None

    return {
        "passage": example["passage"] if example["passage"] else "",
        "question": example["question"],
        "target_scores": target_scores,
        "answer": answer,
    }


def convert(input_file_path, output_file_path, file_name):
    with open(input_file_path, "r", encoding="utf-8") as file:
        with open(output_file_path, "w", encoding="utf-8") as outfile:
            for line in file:
                example = json.loads(line)
                new_entry = transform_entry(example, file_name)
                if new_entry:
                    outfile.write(json.dumps(new_entry, ensure_ascii=False) + "\n")


def main():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    input_dir = os.path.join(script_dir, "../../RawData/agieval")
    output_dir = os.path.join(script_dir, "./data")

    os.makedirs(output_dir, exist_ok=True)

    for input_file in glob.glob(input_dir + "/*.jsonl"):
        file_name = os.path.basename(input_file)
        output_file = os.path.join(output_dir, file_name)
        convert(input_file, output_file, file_name)


if __name__ == "__main__":
    main()
