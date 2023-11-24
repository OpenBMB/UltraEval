import random


def transform(data, num_sample: int, r: random.Random, dataset_name: str):
    text = f"阅读文章：{data['passage'][0]}\n根据上文，回答如下问题：{data['passage'][1]}\n请从“无关”，“蕴含”，“矛盾”中进行选择。\n答："
    correct_answer = [
        key for key, value in data["target_scores"].items() if value == 1
    ][0].strip()
    return {"input": text, "output": correct_answer, "processed_output": correct_answer}
