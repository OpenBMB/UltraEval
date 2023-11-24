import csv
import json
import os


def transform_entry(row):
    passage = [
        row["InputSentence1"],
        row["InputSentence2"],
        row["InputSentence3"],
        row["InputSentence4"],
    ]

    answer_right_ending = int(row["AnswerRightEnding"])
    target_scores = {
        row["RandomFifthSentenceQuiz1"]: int(answer_right_ending == 1),
        row["RandomFifthSentenceQuiz2"]: int(answer_right_ending == 2),
    }
    return {
        "passage": passage,
        "question": "",
        "target_scores": target_scores,
        "answer": "",
    }


def convert(input_file_path, output_file_path):
    with open(input_file_path, "r", encoding="utf-8") as file:
        csv_reader = csv.DictReader(file)
        with open(output_file_path, "w", encoding="utf-8") as outfile:
            for row in csv_reader:
                new_entry = transform_entry(row)
                outfile.write(json.dumps(new_entry, ensure_ascii=False) + "\n")


def main():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    input_path = "../../RawData/storycloze/cloze_test_val__winter2018-cloze_test_ALL_val - 1 - 1.csv"
    output_path = "./data/storycloze.jsonl"
    input_file_path = os.path.join(script_dir, input_path)
    output_file_path = os.path.join(script_dir, output_path)
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
    convert(input_file_path, output_file_path)


if __name__ == "__main__":
    main()
