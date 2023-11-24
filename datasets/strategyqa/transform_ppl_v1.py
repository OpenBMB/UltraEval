import random


def transform(data, num_sample: int, r: random.Random, dataset_name: str):
    facts_str = ", ".join(data["passage"][2])
    context = f"Background:\n{data['passage'][0]} - {data['passage'][1]}\nFact:\n{facts_str}\n"
    question = f"Question:\n{data['question']}\n"
    instruction = f"Requirement:\nPlease respond with either 'Yes' or 'No'.\n"
    answer_prompt = f"Answer:\n"
    text = context + question + instruction + answer_prompt
    processed_correct_answer = correct_answer = [
        key for key, value in data["target_scores"].items() if value == 1
    ][0].strip()

    return {
        "input": text,
        "output": correct_answer,
        "processed_output": processed_correct_answer,
    }
