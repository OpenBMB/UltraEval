import random


def transform(data, num_sample: int, r: random.Random, dataset_name: str):
    context = f"文章：\n{data['question']}\n"
    question = f"问题：\n请判断上述内容属于什么新闻？\n"
    answer_prompt = f"答案：\n"
    text = context + question + answer_prompt
    processed_correct_answer = correct_answer = [
        key for key, value in data["target_scores"].items() if value == 1
    ][0].strip()

    return {
        "input": text,
        "output": correct_answer,
        "processed_output": processed_correct_answer,
    }
