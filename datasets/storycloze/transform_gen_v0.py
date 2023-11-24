import random


def transform(data, num_sample: int, r: random.Random, dataset_name: str):
    options = list(data["target_scores"].keys())
    sentence_quiz1, sentence_quiz2 = options
    passage = "\n".join(data["passage"])
    text = f"{passage}\nQuestion: Which ending makes the most sense?\nA. {sentence_quiz1}\nB. {sentence_quiz2}\nYou may choose between 'A' and 'B'.\nAnswer: "
    index_of_correct_answer = list(data["target_scores"].values()).index(1)
    answers = ["A", "B"]
    correct_answer = answers[index_of_correct_answer]

    return {"input": text, "output": correct_answer, "processed_output": correct_answer}
