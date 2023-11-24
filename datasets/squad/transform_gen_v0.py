import random

from UltraEval.tasks.postprocess import ExactMatchPost


def transform(data, num_sample: int, r: random.Random, dataset_name: str):
    text = f"{data['passage'][1]}\nAccording to the above passage, answer the following question. If it is impossible to answer according to the passage, answer `impossible to answer`:\nQuestion: {data['question']}\n Answer: "
    correct_answer = data["answer"]
    emp = ExactMatchPost()
    _, processed_correct_answer = emp([], correct_answer)
    return {
        "input": text,
        "output": correct_answer,
        "processed_output": processed_correct_answer,
    }
