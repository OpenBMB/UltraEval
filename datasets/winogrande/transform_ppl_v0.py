import random


def transform(data, num_sample: int, r: random.Random, dataset_name: str):
    output_sentence = next(
        key for key, value in data["target_scores"].items() if value == 1
    )
    return {
        "input": data["question"],
        "output": output_sentence,
        "processed_output": output_sentence,
    }
