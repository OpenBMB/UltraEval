import glob
import json
import os
import re


def extract_options(input_str):
    options = {}

    pattern = re.compile(r"([A-D])[.．]?\s*((?:[^A-D\n]|(?!\n[A-D])[.．\n])+)")
    matches = pattern.findall(input_str)

    for match in matches:
        key, value = match
        options[key.strip().replace("\n", "")] = value.strip()

    return options


def transform_entry(example, file_name):
    multi_question_choice_cases = [
        "Chinese_Modern_Lit.json",
        "English_Fill_in_Blanks.json",
        "English_Reading_Comp.json",
    ]
    multi_choice_cases = ["Physics_MCQs.json"]
    five_out_of_seven_cases = ["English_Cloze_Test.json"]
    if (
        file_name in multi_question_choice_cases
        or file_name in multi_choice_cases
        or file_name in five_out_of_seven_cases
    ):
        answer = example["answer"]
        target_scores = {}
    else:
        options = extract_options(example["question"])
        if len(options) != 4:
            raise ValueError("Extract Options Error!")
        target_scores = {opt: 0 for opt in list(options.values())}
        correct_option = options[example["answer"][0]]
        if correct_option is not None and correct_option in target_scores:
            target_scores[correct_option] = 1
            answer = ""
        else:
            raise ValueError("No Keys In Targe_scores!")

    return {
        "passage": "",
        "question": example["question"],
        "target_scores": target_scores,
        "answer": answer,
        "score": example["score"],
    }


def convert(input_file_path, output_file_path, file_name):
    with open(input_file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
        with open(output_file_path, "w", encoding="utf-8") as outfile:
            for example in data["example"]:
                new_entry = transform_entry(
                    example, re.sub(r"\d{4}-\d{4}_", "", file_name)
                )
                if new_entry:
                    outfile.write(json.dumps(new_entry, ensure_ascii=False) + "\n")


def main():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    input_dir = os.path.join(
        script_dir, "../../RawData/gaokaobench/Multiple-choice_Questions"
    )
    output_dir = os.path.join(script_dir, "./data")

    os.makedirs(output_dir, exist_ok=True)

    for input_file in glob.glob(input_dir + "/*.json"):
        file_name = os.path.basename(input_file)
        output_file = os.path.join(
            output_dir,
            re.sub(r"\d{4}-\d{4}_", "", file_name.replace(".json", ".jsonl")).replace("_", "-"),
        )
        convert(input_file, output_file, file_name)


if __name__ == "__main__":
    main()
