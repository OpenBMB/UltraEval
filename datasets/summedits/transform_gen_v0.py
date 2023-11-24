import random


def transform(data, num_sample: int, r: random.Random, dataset_name: str):
    text = f"Given the document below, you have to determine if 'Yes' or 'No', the summary is factually consistent with the document.\nDocument: {data['passage'][0]}\nSummary: {data['passage'][1]}\nQuestion: Is the summary factually consistent with the document?\nA. Yes\nB. No\nAnswer: "
    index_of_correct_answer = list(data["target_scores"].values()).index(1)
    answers = ["A", "B"]
    correct_answer = answers[index_of_correct_answer]

    return {"input": text, "output": correct_answer, "processed_output": correct_answer}
