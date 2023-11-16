import random
from seereval.tasks.postprocess import MathPost
def remove_boxed(s):
    left = '\\boxed{'
    try:
        assert s[:len(left)] == left
        assert s[-1] == '}'
        return s[len(left):-1]
    except Exception:
        return None

def last_boxed_only_string(string):
    idx = string.rfind('\\boxed')
    if idx < 0:
        idx = string.rfind('\\fbox')
        if idx < 0:
            return None

    i = idx
    right_brace_idx = None
    num_left_braces_open = 0
    while i < len(string):
        if string[i] == '{':
            num_left_braces_open += 1
        if string[i] == '}':
            num_left_braces_open -= 1
            if num_left_braces_open == 0:
                right_brace_idx = i
                break
        i += 1

    if right_brace_idx is None:
        retval = None
    else:
        retval = string[idx:right_brace_idx + 1]

    return retval

def transform(data, num_sample: int, r: random.Random, dataset_name: str):
    text = f"Problem: {data['question']}\nSolution: "
    correct_answer = data['answer']
    mp = MathPost()
    _, processed_correct_answer = mp([], remove_boxed(last_boxed_only_string(data['answer'])))

    return {"input": text, "output": correct_answer + f"\nFinal Answer: The final answer is ${processed_correct_answer[0]}$. I hope it is correct.", "processed_output": processed_correct_answer}