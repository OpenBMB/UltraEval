import random


def transform(data, num_sample: int, r: random.Random, dataset_name: str):
    text = "以下句子是否通顺？\n" + data["passage"]
    correct_answer = [
        key + "这句话是通顺的。" for key, value in data["target_scores"].items() if value == 1
    ][0].strip()

    return {"input": text, "output": correct_answer, "processed_output": correct_answer}
