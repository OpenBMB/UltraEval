import random

from UltraEval.tasks.postprocess import ExactMatchPost


def transform(data, num_sample: int, r: random.Random, dataset_name: str):
    context = f"Passage: {data['passage']}\n{data['question'].replace('@placeholder', '____')}\n"
    question = f"Question: What entity does ____ refer to in the result? Give me the entity name: "
    text = context + question
    correct_answer = data["answer"]
    emp = ExactMatchPost()
    _, processed_correct_answer = emp([], correct_answer)
    return {
        "input": text,
        "output": correct_answer,
        "processed_output": processed_correct_answer,
    }
