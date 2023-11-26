import random

from ...tasks.postprocess import CommonMathPost

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
    "jec-qa-kd",
    "jec-qa-ca",
    "gaokao-chinese",
    "gaokao-geography",
    "gaokao-history",
    "gaokao-biology",
    "gaokao-chemistry",
    "gaokao-physics",
    "gaokao-mathqa",
]
english_cloze_datasets = ["math"]
chinese_cloze_datasets = ["gaokao-mathcloze"]

english_qa_datasets = [f"agieval_{dataset}_gen" for dataset in english_qa_datasets]
chinese_qa_datasets = [f"agieval_{dataset}_gen" for dataset in chinese_qa_datasets]
english_cloze_datasets = [
    f"agieval_{dataset}_gen" for dataset in english_cloze_datasets
]
chinese_cloze_datasets = [
    f"agieval_{dataset}_gen" for dataset in chinese_cloze_datasets
]


def transform(data, num_fewshot: int, r: random.Random, dataset_name: str):
    passage: str = data.get("passage", "")
    question: str = data.get("question", "")
    if data["target_scores"]:
        options = ""
        for idx, item in enumerate(data["target_scores"].keys()):
            options += f"({chr(65 + idx)}) {item} "
        final_option_char = "ABCDEF"[len(list()) - 1]

    if dataset_name in english_qa_datasets:
        if num_fewshot == 0:
            text = (
                f"{passage}Q: {question} "
                f"Answer Choices: {options}\n"
                f"A: Among A through {final_option_char}, the answer is "
            )
        else:
            text = (
                f"Problem.    {passage} {question}\n"
                f"Choose from the following options:    {options}\n"
                f"The answer is therefore "
            )
        if data["answer"]:
            correct_answer = processed_correct_answer = data["answer"]
        else:
            index_of_correct_answer = list(data["target_scores"].values()).index(1)
            processed_correct_answer = (
                correct_answer
            ) = f"{chr(65 + index_of_correct_answer)}"
    elif dataset_name in chinese_qa_datasets:
        if num_fewshot == 0:
            text = (
                f"{passage}问题：{question} "
                f"选项：{options}\n"
                f"答案：从A到{final_option_char}, 我们应选择"
            )
        else:
            text = f"问题.    {passage} {question}\n" f"从以下选项中选择:    {options}\n" f"答案是 "
        if data["answer"]:
            correct_answer = processed_correct_answer = data["answer"]
        else:
            index_of_correct_answer = list(data["target_scores"].values()).index(1)
            processed_correct_answer = (
                correct_answer
            ) = f"{chr(65 + index_of_correct_answer)}"
    elif dataset_name in english_cloze_datasets:
        if num_fewshot == 0:
            text = f"{passage}Q: {question}\n" f"A: the answer is "
        else:
            text = f"Problem.   {passage}{question}.\n" f"The answer is therefore "
        cmp = CommonMathPost()
        correct_answer = data["answer"]
        _, processed_correct_answer = cmp([], correct_answer)
    elif dataset_name in chinese_cloze_datasets:
        if num_fewshot == 0:
            text = f"{passage}问题：{question}\n" f"答案："
        else:
            text = f"问题.   {passage}{question}\n" f"答案是 "
        cmp = CommonMathPost()
        correct_answer = data["answer"]
        _, processed_correct_answer = cmp([], correct_answer)
    return {
        "input": text,
        "output": correct_answer,
        "processed_output": processed_correct_answer,
    }
