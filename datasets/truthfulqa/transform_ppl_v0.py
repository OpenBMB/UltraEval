import random


def transform(data, num_sample: int, r: random.Random, dataset_name: str):
    correct_answer = [key for key, value in data["target_scores"].items() if value == 1]
    text = f"Question: {data['question']}\nAnswer: "

    return {"input": text, "output": correct_answer, "processed_output": correct_answer}
