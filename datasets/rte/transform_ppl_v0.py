import random


def transform(data, num_sample: int, r: random.Random, dataset_name: str):
    text = (
        data["passage"][0]
        + "\n"
        + data["passage"][1]
        + "\nIs the sentence below entailed by the sentence above? "
    )
    correct_answer = [
        key for key, value in data["target_scores"].items() if value == 1
    ][0].strip()

    return {"input": text, "output": correct_answer, "processed_output": correct_answer}
