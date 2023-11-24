import random


def transform(data, num_sample: int, r: random.Random, dataset_name: str):
    question = f"问题：\n以下两句话是什么关系？\n"
    context = f"第一句话：{data['passage'][0]}\n第二句话：{data['passage'][1]}\n"
    instruction = f"要求：\n请回答“矛盾”,“无关”或者“蕴含”。\n"
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
