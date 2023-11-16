import random
import re
def transform(data, num_sample: int, r: random.Random, dataset_name: str):
    text = f"内容： {data['passage']}。请对上述内容进行情绪分类。\nA. 消极\nB. 积极\n请从”A“，”B“中进行选择。\n答："
    index_of_correct_answer = list(data['target_scores'].values()).index(1)
    answers = ['A', 'B']
    correct_answer = answers[index_of_correct_answer]

    return {"input": text, "output": correct_answer, "processed_output": correct_answer}