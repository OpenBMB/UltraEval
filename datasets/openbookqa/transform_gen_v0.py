import random


def transform(data, num_sample: int, r: random.Random, dataset_name: str):
    options = list(data["target_scores"].keys())
    A, B, C, D = options
    text = f"Given the fact: {data['passage']}\nQuestion: {data['question']}\nA. {A}\nB. {B}\nC. {C}\nD. {D}\nAnswer: "
    index_of_correct_answer = list(data["target_scores"].values()).index(1)
    answers = ["A", "B", "C", "D"]
    correct_answer = answers[index_of_correct_answer]

    return {"input": text, "output": correct_answer, "processed_output": correct_answer}
