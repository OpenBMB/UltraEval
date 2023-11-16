import random

def transform(data, num_sample: int, r: random.Random, dataset_name: str):
    instruction = f"Requirement:\nPlease complete the following context with a single word.\n"
    context = f"Context:\n{data['question']} "
    text = instruction + context
    processed_correct_answer = correct_answer = data['answer']
    return {"input": text, "output": correct_answer, "processed_output": processed_correct_answer}  
