import random

from UltraEval.tasks.postprocess import ExactMatchPost


def transform(data, num_sample: int, r: random.Random, dataset_name: str):
    context = f"Context:\n{data['passage'][1]}\n"
    question = f"Question:\n{data['question']}\n"
    answer_prompt = f"Answer:\n"
    text = context + question + answer_prompt
    correct_answer = data["answer"]
    emp = ExactMatchPost()
    _, processed_correct_answer = emp([], correct_answer)

    return {
        "input": text,
        "output": correct_answer,
        "processed_output": processed_correct_answer,
    }
