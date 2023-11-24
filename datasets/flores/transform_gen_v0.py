import random


def transform(data, num_sample: int, r: random.Random, dataset_name: str):
    text = f"Translate the following English statements to Chinese (Simpl).\nSource: {data['passage'][0]}\nTarget: "

    return {
        "input": text,
        "output": data["passage"][1],
        "processed_output": data["passage"][1],
    }
