import csv
import json
import os


def transform_entry(row):
    sentid, sentence = row
    gender = sentid.split(".")[3]

    occupation, participant, idx = sentid.split(".")[:3]
    pronouns = [" her", " his", " him", " their", " them", " they", " she", " he"]
    refer = next((pronoun.strip() for pronoun in pronouns if pronoun in sentence), None)

    target_scores = {occupation: int(idx == "0"), participant: int(idx == "1")}
    return gender, {
        "passage": sentence,
        "question": refer,
        "target_scores": target_scores,
        "answer": "",
    }


def convert(input_file_path, output_file_path):
    data = {"male": [], "female": [], "neutral": []}

    with open(input_file_path, "r", encoding="utf-8") as infile:
        reader = csv.reader(infile, delimiter="\t")
        next(reader)

        for row in reader:
            gender, transformed_data = transform_entry(row)
            data[gender].append(transformed_data)

    for gender, items in data.items():
        with open(
            os.path.join(output_file_path, f"{gender}.jsonl"), "w", encoding="utf-8"
        ) as outfile:
            for item in items:
                outfile.write(json.dumps(item, ensure_ascii=False) + "\n")


def main():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    input_path = "../../RawData/winogender/all_sentences.tsv"
    output_path = "./data/"
    input_file_path = os.path.join(script_dir, input_path)
    output_file_path = os.path.join(script_dir, output_path)
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
    convert(input_file_path, output_file_path)


if __name__ == "__main__":
    main()
