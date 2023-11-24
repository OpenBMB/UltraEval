import random


def transform(data, num_sample: int, r: random.Random, dataset_name: str):
    question = f"问题：\n以下这句话中{data['question'][1]}是否指代{data['question'][0]}？\n"
    context = f"{data['passage']}\n"
    instruction = f"要求：\n请回答“是”或者“否”。\n"
    answer_prompt = f"答案：\n"
    text = question + context + instruction + answer_prompt
    processed_correct_answer = correct_answer = [
        key for key, value in data["target_scores"].items() if value == 1
    ][0].strip()
    return {
        "input": text,
        "output": correct_answer,
        "processed_output": processed_correct_answer,
    }
