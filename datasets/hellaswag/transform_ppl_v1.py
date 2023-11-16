
import random

def transform(data, num_sample: int, r: random.Random, dataset_name: str):
    text = f"{data['question']} "
    processed_correct_answer = correct_answer = [key for key, value in data["target_scores"].items() if value == 1][0].strip()
    return {"input": text, "output": correct_answer, "processed_output": processed_correct_answer}