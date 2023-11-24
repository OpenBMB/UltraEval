import random


def transform(data, num_sample: int, r: random.Random, dataset_name: str):
    opt1 = data["question"] + list(data["target_scores"].keys())[0]
    opt2 = data["question"] + list(data["target_scores"].keys())[1]
    question = f"Question:\nWhich of the following is a good sentence?\n"
    instruction = f"Requirement:\nChoose and respond with the letter of the correct answer, including the parentheses.\n"
    options = f"Options:\n(A) {opt1}\n(B) {opt2}\n"
    answer_prompt = f"Answer:\n"
    text = question + instruction + options + answer_prompt
    index_of_correct_answer = list(data["target_scores"].values()).index(1)
    processed_correct_answer = correct_answer = f"({chr(65 + index_of_correct_answer)})"

    return {
        "input": text,
        "output": correct_answer,
        "processed_output": processed_correct_answer,
    }
