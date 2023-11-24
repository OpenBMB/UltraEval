import random


def transform(data, num_sample: int, r: random.Random, dataset_name: str):
    facts_str = ", ".join(data["passage"][2])

    text = f"Background: {data['passage'][0]} - {data['passage'][1]}\nFact: {facts_str}\nQuestion: {data['question']}\nA. Yes\nB. No\nAnswer: "
    correct_answer = "A" if data["target_scores"].get("Yes") == 1 else "B"

    return {"input": text, "output": correct_answer, "processed_output": correct_answer}
