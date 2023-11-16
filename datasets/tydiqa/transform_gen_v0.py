
import random
from seereval.tasks.postprocess import ExactMatchPost
def transform(data, num_sample: int, r: random.Random, dataset_name: str):
    text = f"Answer the following question based on the information in the given passage.\n\nPassage: {data['passage'][1]}\nQuestion: {data['question']}\nAnswer: "
    correct_answer = data['answer']
    emp = ExactMatchPost()
    _, processed_correct_answer = emp([], correct_answer)

    return {"input": text, "output": correct_answer, "processed_output": processed_correct_answer}


