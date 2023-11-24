import random


def transform(data, num_sample: int, r: random.Random, dataset_name: str):
    text = (
        data["passage"]
        + "\n此处，代词“"
        + data["question"][1]
        + "”被用于指代“"
        + data["question"][0]
        + "”吗?请回答是或者否。"
    )
    correct_answer = [
        key for key, value in data["target_scores"].items() if value == 1
    ][0].strip()

    return {"input": text, "output": correct_answer, "processed_output": correct_answer}
