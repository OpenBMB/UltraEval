import random


def transform(data, num_sample: int, r: random.Random, dataset_name: str):
    if data["passage"]:
        text = "Article: " + data["passage"] + "\n\n"
    else:
        text = ""

    if data["question"][-6:] == "  _  .":
        formatted_question = data["question"][:-6]
    else:
        formatted_question = "Question: " + data["question"] + "\n" + "Answer: "
    text += formatted_question
    correct_answer = [
        key for key, value in data["target_scores"].items() if value == 1
    ][0].strip()

    return {"input": text, "output": correct_answer, "processed_output": correct_answer}
