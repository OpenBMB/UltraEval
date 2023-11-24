import random


def transform(data, num_sample: int, r: random.Random, dataset_name: str):
    if data["question"].endswith("?"):
        context = f"Context:\n{data['passage'].lower().strip()}\n"
        question = f"Question:\n{data['question'].lower()}\n"
        answer_prompt = f"Answer:\n"
        text = context + question + answer_prompt
    else:
        context = f"Context:\n{data['passage'].lower().strip()}\n"
        question = f"Question:\nAccording to the context above, we can infer that {data['question'].lower()}\n"
        answer_prompt = f"Answer:\n"
        text = context + question + answer_prompt
    processed_correct_answer = correct_answer = [
        key for key, value in data["target_scores"].items() if value == 1
    ][0].strip()

    return {
        "input": text,
        "output": correct_answer,
        "processed_output": processed_correct_answer,
    }
