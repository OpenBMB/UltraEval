import random


def transform(data, num_sample: int, r: random.Random, dataset_name: str):
    text = (
        "Sentence 1: "
        + data["passage"][0]
        + "\nSentence 2: "
        + data["passage"][1]
        + "\nAre "
        + data["question"]
        + " in the above two sentenses the same?\n"
    )
    correct_answer = [
        key for key, value in data["target_scores"].items() if value == 1
    ][0].strip()

    return {"input": text, "output": correct_answer, "processed_output": correct_answer}
