import random


def transform(data, num_sample: int, r: random.Random, dataset_name: str):
    keys = list(data["target_scores"].keys())
    A, B, C, D, E, F, G = [key[:4] for key in keys]
    text = f"{data['passage']}\n请选择______处所填的词\nA. {A}\nB. {B}\nC. {C}\nD. {D}\nE. {E}\nF. {F}\nG. {G}\n请从”A“，”B“，”C“，”D“，”E“，”F“，”G“中进行选择。答："
    index_of_correct_answer = list(data["target_scores"].values()).index(1)
    answers = ["A", "B", "C", "D", "E", "F", "G"]
    correct_answer = answers[index_of_correct_answer]

    return {"input": text, "output": correct_answer, "processed_output": correct_answer}
