import random


def transform(data, num_sample: int, r: random.Random, dataset_name: str):
    text = f"语句一：“{data['passage'][0]}”\n语句二：“{data['passage'][1]}”\n语句一与语句二是关于蚂蚁金融产品的疑问，两者所询问的内容是否完全一致？\nA. 不完全一致\nB. 完全一致\n请从“A”，“B”中进行选择。\n答："
    index_of_correct_answer = list(data["target_scores"].values()).index(1)
    processed_correct_answer = correct_answer = f"{chr(65 + index_of_correct_answer)}"

    return {
        "input": text,
        "output": correct_answer,
        "processed_output": processed_correct_answer,
    }
