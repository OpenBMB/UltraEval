import random


def transform(data, num_sample: int, r: random.Random, dataset_name: str):
    options = list(data["target_scores"].keys())
    # A, B, C, D = options
    text = f"Read the article, and answer the question by replying A, B, C or D.\n\nArticle:\n{data['passage']}\n\nQuestion: {data['question']}\n\n"
    for i, opt in enumerate(options):
        text += f"{chr(65+i)}. {opt}\n"
    text += "\nAnswer: "
    index_of_correct_answer = list(data["target_scores"].values()).index(1)
    # answers = ['A', 'B', 'C', 'D']
    correct_answer = chr(65 + index_of_correct_answer)

    return {"input": text, "output": correct_answer, "processed_output": correct_answer}
