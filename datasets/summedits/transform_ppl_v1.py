import random


def transform(data, num_sample: int, r: random.Random, dataset_name: str):
    context = f"Context:\n{data['passage'][0]}\nSummary:\n{data['passage'][1]}\n"
    question = f"Question:\nIs the summary factually consistent with the context?\n"
    instruction = f"Requirement:\nPlease respond with either 'Yes' or 'No'.\n"
    answer_prompt = f"Answer:\n"
    text = context + question + instruction + answer_prompt
    processed_correct_answer = correct_answer = [
        key for key, value in data["target_scores"].items() if value == 1
    ][0].strip()
    return {"input": text, "output": correct_answer, "processed_output": correct_answer}
