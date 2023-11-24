import random

from UltraEval.tasks.postprocess import ExactMatchPost


def transform(data, num_sample: int, r: random.Random, dataset_name: str):
    context = f"文章：\n{data['passage']}\n"
    question = f"问题：\n{data['question']}\n"
    instruction = f"要求：\n根据文章回答问题。你的答案应该尽可能简练，请以 ‘答案是’ 开头的句式作答。\n"
    answer_prompt = f"答案：\n"
    text = question + context + instruction + answer_prompt
    correct_answer = data["answer"]
    emp = ExactMatchPost()
    _, processed_correct_answer = emp([], correct_answer)
    return {
        "input": text,
        "output": correct_answer,
        "processed_output": processed_correct_answer,
    }
