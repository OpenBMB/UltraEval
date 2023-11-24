import random


def transform(data, num_sample: int, r: random.Random, dataset_name: str):
    question = f"问题：\n如何将下面这句话从中文翻译为英文？\n"
    context = f"{data['question']}\n"
    answer_prompt = f"答案：\n"
    text = question + context + answer_prompt
    processed_correct_answer = correct_answer = data["answer"]

    return {
        "input": text,
        "output": correct_answer,
        "processed_output": processed_correct_answer,
    }
