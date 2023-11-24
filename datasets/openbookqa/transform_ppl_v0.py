import random


def transform(data, num_sample: int, r: random.Random, dataset_name: str):
    if data["question"].endswith("?"):
        text = (
            "Given the fact: "
            + data["passage"].lower().strip()
            + " "
            + "\nQuestion: "
            + data["question"].lower()
            + "\nAnswer: "
        )
    else:
        text = (
            "Given the fact: "
            + data["passage"].lower().strip()
            + ", we can infer that "
            + data["question"].lower()
            + " "
        )

    correct_answer = [
        key for key, value in data["target_scores"].items() if value == 1
    ][0].strip()

    return {"input": text, "output": correct_answer, "processed_output": correct_answer}
