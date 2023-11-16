import random
import re
def transform(data, num_sample: int, r: random.Random, dataset_name: str):
    documents_text = "\n".join(data["passage"])
    options = list(data['target_scores'].keys())
    
    choice_text = "\n".join([f"{chr(65 + i)}. {option}" for i, option in enumerate(options)])
    
    text = f"{documents_text}\n问：{data['question']}\n{choice_text}\n请从{','.join(['“'+chr(65 + i)+'”' for i in range(len(options))])}中进行选择。\n答："

    index_of_correct_answer = list(data['target_scores'].values()).index(1)
    answers = [chr(65 + i) for i in range(len(options))]
    correct_answer = answers[index_of_correct_answer]

    return {"input": text, "output": correct_answer, "processed_output": correct_answer}