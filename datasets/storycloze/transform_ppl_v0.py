import random


def transform(data, num_sample: int, r: random.Random, dataset_name: str):
    passage = "\n".join(data["passage"]) + "\n"
    correct_answer = [
        key for key, value in data["target_scores"].items() if value == 1
    ][0]
    return {
        "input": passage,
        "output": correct_answer,
        "processed_output": correct_answer,
    }
