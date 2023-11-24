import random

from UltraEval.tasks.postprocess import CommonMathPost

english_qa_datasets = [
    "lsat-ar",
    "lsat-lr",
    "lsat-rc",
    "logiqa-en",
    "sat-math",
    "sat-en",
    "aqua-rat",
    "sat-en-without-passage",
    "gaokao-english",
]
chinese_qa_datasets = [
    "logiqa-zh",
    "gaokao-chinese",
    "gaokao-geography",
    "gaokao-history",
    "gaokao-biology",
    "gaokao-chemistry",
    "gaokao-mathqa",
]

english_qa_datasets = [f"agieval_{dataset}_ppl" for dataset in english_qa_datasets]
chinese_qa_datasets = [f"agieval_{dataset}_ppl" for dataset in chinese_qa_datasets]


def transform(data, num_fewshot: int, r: random.Random, dataset_name: str):
    passage: str = data.get("passage", "")
    question: str = data.get("question", "")
    if dataset_name in english_qa_datasets:
        if num_fewshot == 0:
            text = f"{passage}Q: {question} " f"the answer is "
        else:
            text = f"Problem.    {passage} {question}\n" f"The answer is therefore "
        processed_correct_answer = correct_answer = [
            key for key, value in data["target_scores"].items() if value == 1
        ][0].strip()
    elif dataset_name in chinese_qa_datasets:
        if num_fewshot == 0:
            text = f"{passage}问题：{question} " f"答案："
        else:
            text = f"问题.    {passage} {question}\n" f"答案是 "
        processed_correct_answer = correct_answer = [
            key for key, value in data["target_scores"].items() if value == 1
        ][0].strip()

    return {
        "input": text,
        "output": correct_answer,
        "processed_output": processed_correct_answer,
    }
