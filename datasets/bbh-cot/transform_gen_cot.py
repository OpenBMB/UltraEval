import random

from ultraeval.tasks.postprocess import ExactMatchPost

import os, json
# def get_info(task_name):

#     with (f"datasets/bbh/bbh/{task_name.replace('-', '_')}.json", "r", encoding="utf-8") as f:
#         temp = json.load(f)
    


def transform(data, num_sample: int, r: random.Random, dataset_name: str):

# """
#     first_task = [
#         "word_sorting", # (具体内容) answer 匹配
#         "web_of_lies", # (Yes/No) target_scores 匹配
#         "sports_understanding", #（yes/no）,target_scores 匹配
#         "object_counting", #(具体内容) answer 匹配
#         "multistep_arithmetic_two", #(具体内容) answer 匹配
#         "dyck_languages", #(具体内容), answer 匹配
#         "boolean_expressions", #(True/False) target_scores 匹配
#     ]
#     second_task = [
#         "tracking_shuffled_objects_three_objects", #target_scores 匹配
#         "tracking_shuffled_objects_seven_objects", #target_scores 匹配
#         "tracking_shuffled_objects_five_objects", #target_scores 匹配
#         "temporal_sequences", #target_scores 匹配
#         "snarks", #target_scores 匹配
#         "salient_translation_error_detection", #target_scores 匹配
#         "ruin_names", #target_scores 匹配
#         "reasoning_about_colored_objects", #target_scores 匹配
#         "penguins_in_a_table", #target_scores 匹配
#         "movie_recommendation", #target_scores 匹配
#         "logical_deduction_three_objects", #target_scores 匹配
#         "logical_deduction_seven_objects", #target_scores 匹配
#         "logical_deduction_five_objects", #target_scores 匹配
#         "hyperbaton", #target_scores 匹配
#         "geometric_shapes", #target_scores 匹配
#         "disambiguation_qa", #target_scores 匹配
#         "date_understanding" #target_scores 匹配
#     ]
#     third_task = [
#         "navigate", #(Yes/No), #target_scores 匹配
#         "formal_fallacies", #(valid/invalid), #target_scores 匹配
#         "causal_judgement", #(Yes/No) #target_scores 匹配
#     ]
# """
    prompt = "{cot}\n\nQ: {input}\nA: Let's think step by step."

    return {
        "input": prompt.format(cot=data["cot"].strip(), input = data["input"].strip()),
        "output": [item.lower() for item in data["answer"]],
        "processed_output": [item.lower() for item in data["answer"]],
    }
