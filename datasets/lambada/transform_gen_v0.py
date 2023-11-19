import random


def transform(data, num_sample: int, r: random.Random, dataset_name: str):
    prompt = "Please complete the following sentence:\n" + data["question"]
    return {
        "input": prompt,
        "output": data["answer"],
        "processed_output": data["answer"],
    }
