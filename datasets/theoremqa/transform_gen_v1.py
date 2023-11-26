import random

from ...tasks.postprocess import TheoremQAPost


def transform(data, num_sample: int, r: random.Random, dataset_name: str):
    question = f"Question:\n{data['question']}\n"
    answer_prompt = f"Answer:\n"
    text = question + answer_prompt
    correct_answer = str(data["answer"][1])
    tqap = TheoremQAPost()
    _, processed_correct_answer = tqap([], correct_answer)
    return {
        "input": text,
        "output": correct_answer,
        "processed_output": processed_correct_answer,
    }
