import random


def transform(data, num_sample: int, r: random.Random, dataset_name: str):
    prefixes = ["A. ", "B. ", "C. ", "D. "]
    opt = "\n".join(
        [prefixes[i] + list(data["target_scores"].keys())[i] for i in range(4)]
    )
    text = f"Question: {data['question']}\nOptions: {opt}\nAnswer: "
    index_of_correct_answer = list(data["target_scores"].values()).index(1)
    processed_correct_answer = correct_answer = f"{chr(65 + index_of_correct_answer)}"

    return {
        "input": text,
        "output": correct_answer,
        "processed_output": processed_correct_answer,
    }
