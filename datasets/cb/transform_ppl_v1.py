import random


def transform(data, num_sample: int, r: random.Random, dataset_name: str):
    question = f"Question:\nWhat is the relation between the two sentences?\n"
    context = (
        f"First sentence: {data['passage'][0]}\nSecond sentence: {data['passage'][1]}\n"
    )
    instruction = f"Requirement:\nPlease respond with 'Contradiction', 'Entailment', or 'Neutral'.\n"
    answer_prompt = f"Answer:\n"
    text = question + context + instruction + answer_prompt
    processed_correct_answer = correct_answer = [
        key for key, value in data["target_scores"].items() if value == 1
    ][0].strip()
    return {
        "input": text,
        "output": correct_answer,
        "processed_output": processed_correct_answer,
    }
