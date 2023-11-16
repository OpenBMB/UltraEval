import random
import re
def transform(data, num_sample: int, r: random.Random, dataset_name: str):
    text = f"Sentence 1: {data['passage'][0]}\nSentence 2: {data['passage'][1]}\nAre '{data['question']}' in the above two sentenses the same?\nA. Yes\nB. No\nAnswer: "
    index_of_correct_answer = list(data['target_scores'].values()).index(1)
    answers = ['A', 'B']
    correct_answer = answers[index_of_correct_answer]

    return {"input": text, "output": correct_answer, "processed_output": correct_answer}