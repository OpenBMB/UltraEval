import random


def transform(data, num_sample: int, r: random.Random, dataset_name: str):
    text = f"阅读文章：{data['passage'][0]}\n根据上文，回答如下问题：{data['passage'][1]}\nA. 错\nB. 可能\nC. 对\n请从“A”，“B”，“C”中进行选择。\n答："
    index_of_correct_answer = list(data["target_scores"].values()).index(1)
    answers = ["A", "B", "C"]
    correct_answer = answers[index_of_correct_answer]

    return {"input": text, "output": correct_answer, "processed_output": correct_answer}
