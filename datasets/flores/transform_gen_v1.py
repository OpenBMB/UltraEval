import random


def transform(data, num_sample: int, r: random.Random, dataset_name: str):
    question = (
        f"Question:\nHow to translate the following English statements to Chinese?\n"
    )
    context = f"{data['passage'][0]}\n"
    answer_prompt = f"Answer:\n"
    text = question + context + answer_prompt
    processed_correct_answer = correct_answer = data["passage"][1]
    return {
        "input": text,
        "output": correct_answer,
        "processed_output": processed_correct_answer,
    }
