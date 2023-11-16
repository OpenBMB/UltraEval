import random
import re
def transform(data, num_sample: int, r: random.Random, dataset_name: str):
    options = list(data['target_scores'].keys())
    sol1, sol2 = options
    text = f"{data['question']}\nA. {sol1}\nB. {sol2}\nAnswer: "
    index_of_correct_answer = list(data['target_scores'].values()).index(1)
    answers = ['A', 'B']
    correct_answer = answers[index_of_correct_answer]

    return {"input": text, "output": correct_answer, "processed_output": correct_answer}