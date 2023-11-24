import random


def transform(data, num_sample: int, r: random.Random, dataset_name: str):
    options = list(data["target_scores"].keys())
    options_labels = ["A", "B", "C", "D", "E"]

    text = f"{data['question']}\n"
    for idx, option in enumerate(options):
        text += f"{options_labels[idx]}. {option}\n"
    text += "Answer: "

    index_of_correct_answer = list(data["target_scores"].values()).index(1)
    correct_answer = options_labels[index_of_correct_answer]

    return {"input": text, "output": correct_answer, "processed_output": correct_answer}
