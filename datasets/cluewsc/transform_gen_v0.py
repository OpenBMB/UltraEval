import random


def transform(data, num_sample: int, r: random.Random, dataset_name: str):
    text = f"{data['passage']}\n此处，“{data['question'][1]}”是否指代“{data['question'][0]}“？\nA. 是\nB. 否\n请从”A“，”B“中进行选择。\n答："
    index_of_correct_answer = list(data["target_scores"].values()).index(1)
    answers = ["A", "B"]
    correct_answer = answers[index_of_correct_answer]

    return {"input": text, "output": correct_answer, "processed_output": correct_answer}
