import random


def transform(data, num_sample: int, r: random.Random, dataset_name: str):
    text = f"题目：{data['question']}\n答案："
    if data["answer"]:
        correct_answer = "".join(data["answer"])
        processed_correct_answer = data["answer"]
    else:
        index_of_correct_answer = list(data["target_scores"].values()).index(1)
        processed_correct_answer = (
            correct_answer
        ) = f"{chr(65 + index_of_correct_answer)}"

    return {
        "input": text,
        "output": correct_answer,
        "processed_output": processed_correct_answer,
    }
