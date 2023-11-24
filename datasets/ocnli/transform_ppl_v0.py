import random


def transform(data, num_sample: int, r: random.Random, dataset_name: str):
    text = (
        "语句一：“"
        + data["passage"][0]
        + "”\n语句二：“"
        + data["passage"][1]
        + "”\n请问这两句话是什么关系？"
    )
    correct_answer = [
        key for key, value in data["target_scores"].items() if value == 1
    ][0].strip()

    return {"input": text, "output": correct_answer, "processed_output": correct_answer}
