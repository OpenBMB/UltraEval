import random

from UltraEval.tasks.postprocess import ExactMatchPost


def transform(data, num_sample: int, r: random.Random, dataset_name: str):
    text = f"根据文章回答问题。你的答案应该尽可能简练，请以 ‘答案是’ 开头的句式作答。\n文章：{data['passage']}\n问：{data['question']}\n答："
    correct_answer = data["answer"]
    emp = ExactMatchPost()
    _, processed_correct_answer = emp([], correct_answer)
    return {
        "input": text,
        "output": correct_answer,
        "processed_output": processed_correct_answer,
    }
