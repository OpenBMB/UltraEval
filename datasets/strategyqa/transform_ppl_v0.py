import random


def transform(data, num_sample: int, r: random.Random, dataset_name: str):
    facts_str = ", ".join(data["passage"][2])

    text = f"Background: {data['passage'][0]} - {data['passage'][1]}\nFact: {facts_str}\nQuestion: {data['question']}\nAnswer: "
    correct_answer = [
        key for key, value in data["target_scores"].items() if value == 1
    ][0].strip()

    return {"input": text, "output": correct_answer, "processed_output": correct_answer}
