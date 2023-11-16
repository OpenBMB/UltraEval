
import random

def transform(data, num_sample: int, r: random.Random, dataset_name: str):
    documents_text = "\n".join(data["passage"])
    text = f"文章：{documents_text}\n问题：{data['question']}\n答案："
    correct_answer = [key for key, value in data["target_scores"].items() if value == 1][0].strip()

    return {"input": text, "output": correct_answer, "processed_output": correct_answer}


