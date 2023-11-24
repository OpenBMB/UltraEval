import random


def transform(data, num_sample: int, r: random.Random, dataset_name: str):
    text = f"语句一：“{data['passage'][0]}”\n语句二：“{data['passage'][1]}”\n请判断语句一和语句二说的是否是一个意思？\nA. 相关\nB. 无关\n请从“A”，“B”中进行选择。\n答："
    index_of_correct_answer = list(data["target_scores"].values()).index(1)
    answers = ["A", "B"]
    correct_answer = answers[index_of_correct_answer]

    return {"input": text, "output": correct_answer, "processed_output": correct_answer}
