
import random

def transform(data, num_sample: int, r: random.Random, dataset_name: str):
    context = f"Context:\n{data['passage']}\n"
    question = f"Question:\nWhat may be the {data['question']}?\n"
    answer_prompt = f"Answer:\n"
    text = context + question + answer_prompt
    processed_correct_answer = correct_answer = [key for key, value in data["target_scores"].items() if value == 1][0].strip()
    return {"input": text, "output": correct_answer, "processed_output": processed_correct_answer}



