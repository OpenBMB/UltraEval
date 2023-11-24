import random


def transform(data, num_sample: int, r: random.Random, dataset_name: str):
    ans = data["answer"] + "\n"
    prompt = f"请将下面这段内容从中文翻译为英文：\n{data['question']}\n译文：\n"
    return {"input": prompt, "output": ans, "processed_output": ans}
