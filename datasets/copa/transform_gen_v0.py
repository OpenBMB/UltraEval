import random


def transform(data, num_sample: int, r: random.Random, dataset_name: str):
    options = list(data["target_scores"].keys())
    choice1, choice2 = options
    text = f"{data['passage']}\nQuestion: Which may be the {data['question']}?\nA. {choice1}\nB. {choice2}\nAnswer: "
    index_of_correct_answer = list(data["target_scores"].values()).index(1)
    answers = ["A", "B"]
    correct_answer = answers[index_of_correct_answer]

    return {"input": text, "output": correct_answer, "processed_output": correct_answer}
