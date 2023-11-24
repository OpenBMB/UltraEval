import random


def transform(data, num_sample: int, r: random.Random, dataset_name: str):
    text = data["question"]
    processed_correct_answer = correct_answer = next(
        key for key, value in data["target_scores"].items() if value == 1
    )
    return {
        "input": text,
        "output": correct_answer,
        "processed_output": processed_correct_answer,
    }
