import re

class GeneralTorch:
    def __init__(self):
        pass

    def __call__(self, result, request):
        raw_outputs = []
        process_outputs = []

        if isinstance(result, list):
            raw_outputs = result
        elif isinstance(result, str):
            raw_outputs = [result]

        process_outputs = raw_outputs

        return raw_outputs, process_outputs

class GeneralTorchPPL:
    def __init__(self):
        pass

    def __call__(self, result, request):
        # result是三层的list
        process_outputs = [[-sum(inner) for inner in outer] for outer in result]
        return result, process_outputs

class GeneralTorchPPLNorm:
    def __init__(self):
        pass

    def __call__(self, result, request):
        process_outputs = [self.process_inner_lists(sublist) for sublist in result]
        return result, process_outputs 
        
    def process_inner_lists(self, inner_lists):
        transposed = list(zip(*inner_lists))
        prefix = []
        for items in transposed:
            if all(item == items[0] for item in items):
                prefix.append(items[0])
            else:
                break
        processed_lists = [-(sum(lst[len(prefix):]) / len(lst[len(prefix):])) for lst in inner_lists]
        return processed_lists


class ExactMatchPost: 
    def __init__(self):
        pass

    def __call__(self, raw_outputs, processed_outputs):
        if isinstance(processed_outputs, str):  
            processed_outputs = [processed_outputs]
        processed_outputs_ = [self.postprocess(text) for text in processed_outputs]
        return raw_outputs, processed_outputs_

    def postprocess(self, text: str) -> str:
        text = re.split(r'[\n]', text, 1)[0].lower()
        if 'answer is' in text:
            text = text.split('answer is')[-1].strip()
        if '答案是' in text:
            text = text.split('答案是')[-1].strip()
        text = general_postprocess(text)
        return text

class ArithmeticPost: 
    def __init__(self):
        pass

    def __call__(self, raw_outputs, processed_outputs):
        if isinstance(processed_outputs, str):  
            processed_outputs = [processed_outputs]
        processed_outputs_ = [self.postprocess(text) for text in processed_outputs]
        return raw_outputs, processed_outputs_

    def postprocess(self, text):
        text = text.strip().split('=')[-1].strip()
        return text

class UntilReturnPost: 
    def __init__(self):
        pass

    def __call__(self, raw_outputs, processed_outputs):
        processed_outputs_ = []  
        
        if isinstance(processed_outputs, str):  
            processed_outputs = [processed_outputs]
        
        for output in processed_outputs:
            output = output.strip().split('\n')[0].strip()
            processed_outputs_.append(output)

        return raw_outputs, processed_outputs_

class MbppPost:
    def __init__(self):
        pass
    
    def __call__(self, raw_outputs, processed_outputs):
        processed_outputs_ = []  
        
        if isinstance(processed_outputs, str):  
            processed_outputs = [processed_outputs]
        
        for output in processed_outputs:
            output = output.split("\n\n")[0]
            processed_outputs_.append(output)

        return raw_outputs, processed_outputs_

class HumanEvalPost:
    def __init__(self):
        pass

    def __call__(self, raw_outputs, processed_outputs):
        processed_outputs_ = []  
        
        if isinstance(processed_outputs, str):  
            processed_outputs = [processed_outputs]
        
        split_keywords = ["\nclass", "\ndef", "\n#", "\n@", "\nprint", "\nif", "<|endoftext|>"]
        
        for output in processed_outputs:
            for keyword in split_keywords:
                output = output.split(keyword)[0]
            processed_outputs_.append(output)

        return raw_outputs, processed_outputs_

class MathPost: 
    SUBSTITUTIONS = [('an ', ''), ('a ', ''), ('.$', '$'), ('\\$', ''),
                     (r'\ ', ''), (' ', ''), ('mbox', 'text'),
                     (',\\text{and}', ','), ('\\text{and}', ','),
                     ('\\text{m}', '\\text{}'), ('\\le', '<')]
    REMOVED_EXPRESSIONS = [
            'square', 'ways', 'integers', 'dollars', 'mph', 'inches', 'ft',
            'hours', 'km', 'units', '\\ldots', 'sue', 'points', 'feet', 'minutes',
            'digits', 'cents', 'degrees', 'cm', 'gm', 'pounds', 'meters', 'meals',
            'edges', 'students', 'childrentickets', 'multiples', '\\text{s}',
            '\\text{.}', '\\text{\ns}', '\\text{}^2', '\\text{}^3', '\\text{\n}',
            '\\text{}', r'\mathrm{th}', r'^\circ', r'^{\circ}', r'\;', r',\!',
            '{,}', '"', '\\dots', '\n', '\r', '\f'
    ]
    def __init__(self):
        pass

    def __call__(self, raw_outputs, processed_outputs):
        if isinstance(processed_outputs, str):  
            processed_outputs = [processed_outputs]
        try:
            processed_outputs_ = [self._strip_string(self.math_postprocess(text)) for text in processed_outputs]
        except:
            try:
                processed_outputs_ = [self.math_postprocess(text) for text in processed_outputs]
            except:
                processed_outputs_ = processed_outputs

        return raw_outputs, processed_outputs_

    def normalize_final_answer(self, final_answer: str) -> str:
        """Normalize a final answer to a quantitative reasoning question."""
        # final_answer = final_answer.split('=')[-1]
        for before, after in self.SUBSTITUTIONS:
            final_answer = final_answer.replace(before, after)
        for expr in self.REMOVED_EXPRESSIONS:
            final_answer = final_answer.replace(expr, '')

        # Extract answer that is in LaTeX math, is bold,
        # is surrounded by a box, etc.
        final_answer = re.sub(r'(\\text\{)(.*?)(\})', '\\2', final_answer)
        final_answer = re.sub(r'(\\textbf\{)(.*?)(\})', '\\2', final_answer)
        final_answer = re.sub(r'(\\overline\{)(.*?)(\})', '\\2', final_answer)
        final_answer = re.sub(r'(\\boxed\{)(.*)(\})', '\\2', final_answer)
        assert '\n' not in final_answer
        assert '\r' not in final_answer
        assert '\f' not in final_answer
        if len(re.findall(r'finalansweris(.*)', final_answer)) > 0:
            final_answer = re.findall(r'finalansweris(.*)', final_answer)[-1]

        if len(re.findall(r'oxed\{(.*?)\}', final_answer)) > 0:
            final_answer = re.findall(r'oxed\{(.*?)\}', final_answer)[-1]

        if len(re.findall(r'\$(.*?)\$', final_answer)) > 0:
            final_answer = re.findall(r'\$(.*?)\$', final_answer)[-1]
        final_answer = final_answer.strip()
        if 'rac' in final_answer and '\\frac' not in final_answer:
            final_answer = final_answer.replace('rac', '\\frac')

        # Normalize shorthand TeX:
        # \fracab -> \frac{a}{b}
        # \frac{abc}{bef} -> \frac{abc}{bef}
        # \fracabc -> \frac{a}{b}c
        # \sqrta -> \sqrt{a}
        # \sqrtab -> sqrt{a}b
        final_answer = re.sub(r'(frac)([^{])(.)', 'frac{\\2}{\\3}',
                              final_answer)
        final_answer = re.sub(r'(sqrt)([^{])', 'sqrt{\\2}', final_answer)
        final_answer = final_answer.replace('$', '')

        # Normalize 100,000 -> 100000
        if final_answer.replace(',', '').isdigit():
            final_answer = final_answer.replace(',', '')

        return final_answer

    def math_postprocess(self, text: str) -> str:
        for maybe_ans in text.split('.'):
            if 'final answer' in maybe_ans.lower():
                return self.normalize_final_answer(maybe_ans)
        return self.normalize_final_answer(text.split('.')[0])

    def _fix_fracs(self, string):
        substrs = string.split('\\frac')
        new_str = substrs[0]
        if len(substrs) > 1:
            substrs = substrs[1:]
            for substr in substrs:
                new_str += '\\frac'
                if substr[0] == '{':
                    new_str += substr
                else:
                    try:
                        assert len(substr) >= 2
                    except AssertionError:
                        return string
                    a = substr[0]
                    b = substr[1]
                    if b != '{':
                        if len(substr) > 2:
                            post_substr = substr[2:]
                            new_str += '{' + a + '}{' + b + '}' + post_substr
                        else:
                            new_str += '{' + a + '}{' + b + '}'
                    else:
                        if len(substr) > 2:
                            post_substr = substr[2:]
                            new_str += '{' + a + '}' + b + post_substr
                        else:
                            new_str += '{' + a + '}' + b
        string = new_str
        return string

    def _fix_a_slash_b(self, string):
        if len(string.split('/')) != 2:
            return string
        a = string.split('/')[0]
        b = string.split('/')[1]
        try:
            a = int(a)
            b = int(b)
            assert string == '{}/{}'.format(a, b)
            new_string = '\\frac{' + str(a) + '}{' + str(b) + '}'
            return new_string
        except:
            return string

    def _remove_right_units(self, string):
        # "\\text{ " only ever occurs (at least in the val set) when describing
        # units
        if '\\text{ ' in string:
            splits = string.split('\\text{ ')
            assert len(splits) == 2
            return splits[0]
        else:
            return string

    def _fix_sqrt(self, string):
        if '\\sqrt' not in string:
            return string
        splits = string.split('\\sqrt')
        new_string = splits[0]
        for split in splits[1:]:
            if split[0] != '{':
                a = split[0]
                new_substr = '\\sqrt{' + a + '}' + split[1:]
            else:
                new_substr = '\\sqrt' + split
            new_string += new_substr
        return new_string

    def _strip_string(self, string):
        # linebreaks
        string = string.replace('\n', '')

        # remove inverse spaces
        string = string.replace('\\!', '')

        # replace \\ with \
        string = string.replace('\\\\', '\\')

        # replace tfrac and dfrac with frac
        string = string.replace('tfrac', 'frac')
        string = string.replace('dfrac', 'frac')

        # remove \left and \right
        string = string.replace('\\left', '')
        string = string.replace('\\right', '')

        # Remove circ (degrees)
        string = string.replace('^{\\circ}', '')
        string = string.replace('^\\circ', '')

        # remove dollar signs
        string = string.replace('\\$', '')

        # remove units (on the right)
        string = self._remove_right_units(string)

        # remove percentage
        string = string.replace('\\%', '')
        string = string.replace('\%', '')  # noqa: W605

        # " 0." equivalent to " ." and "{0." equivalent to "{." Alternatively,
        # add "0" if "." is the start of the string
        string = string.replace(' .', ' 0.')
        string = string.replace('{.', '{0.')
        # if empty, return empty string
        if len(string) == 0:
            return string
        if string[0] == '.':
            string = '0' + string

        # to consider: get rid of e.g. "k = " or "q = " at beginning
        if len(string.split('=')) == 2:
            if len(string.split('=')[0]) <= 2:
                string = string.split('=')[1]

        # fix sqrt3 --> sqrt{3}
        string = self._fix_sqrt(string)

        # remove spaces
        string = string.replace(' ', '')

        # \frac1b or \frac12 --> \frac{1}{b} and \frac{1}{2}, etc. Even works
        # with \frac1{72} (but not \frac{72}1). Also does a/b --> \\frac{a}{b}
        string = self._fix_fracs(string)

        # manually change 0.5 --> \frac{1}{2}
        if string == '0.5':
            string = '\\frac{1}{2}'

        # NOTE: X/Y changed to \frac{X}{Y} in dataset, but in simple cases fix
        # in case the model output is X/Y
        string = self._fix_a_slash_b(string)

        return string

class TheoremQAPost: 
    def __init__(self):
        pass

    def __call__(self, raw_outputs, processed_outputs):
        if isinstance(processed_outputs, str):  
            processed_outputs = [processed_outputs]
        processed_outputs_ = [self.postprocess(text) for text in processed_outputs]
        return raw_outputs, processed_outputs_

    def postprocess(self, text):
        text = text.strip()
        matches = re.findall(r'answer is ([^\s]+)', text)
        if len(matches) == 0:
            return text
        else:
            text = matches[0].strip().strip('.,?!\"\';:')
            return text

class GSM8KPost:
    def __init__(self):
        pass

    def __call__(self, raw_outputs, processed_outputs):
        if isinstance(processed_outputs, str):  
            processed_outputs = [processed_outputs]
        processed_outputs_ = [self.postprocess(text) for text in processed_outputs]
        return raw_outputs, processed_outputs_

    def postprocess(self, text):
        ANS_RE = re.compile(r"#### (\-?[0-9\.\,]+)")
        text = ANS_RE.search(text)
        if text is not None:
            text = text.group(1).strip().replace(",", "")
        else:
            text = ""
        return text.strip()

class HumanEvalGPT:
    def __init__(self):
        pass

    def __call__(self, raw_outputs, processed_outputs):
        if isinstance(processed_outputs, str):  
            processed_outputs = [processed_outputs]
            
        processed_outputs_ = [extract_code_from_string(text) for text in processed_outputs]
        return raw_outputs, processed_outputs_

def extract_code_from_string(s):
    # 查找第一对代码块标记
    code_start = s.find("```python") + len("```python")
    code_end = s.find("```", code_start)
    # 提取并返回代码块
    return s[code_start:code_end]

def cut(input, output):  # 对输出做输入截断
    if output.strip().startswith(input.strip()):
        return output.strip()[len(input.strip()):]
    else:
        return output

def general_postprocess(text: str) -> str:
    # Cut off the first newline, period, or comma
    truncated_text = re.split(r'[\n.,]', text, 1)[0]
    # Remove punctuation
    no_punctuation = re.sub(r'[^\w\s]', '', truncated_text)
    # Remove article
    no_articles = re.sub(r'\b(a|an|the)\b',
                        '',
                        no_punctuation,
                        flags=re.IGNORECASE)
    # Remove duplicated blank spaces
    cleaned_text = re.sub(r'\s+', ' ', no_articles).strip()
    return cleaned_text

POSTPROCESS_REGISTRY = {"general_torch": GeneralTorch, "general_torch_ppl": GeneralTorchPPL, "general_torch_ppl_norm":GeneralTorchPPLNorm, "exact_match_post": ExactMatchPost, "math_post": MathPost, "until_return_post": UntilReturnPost, "humaneval_post": HumanEvalPost, "arithmetic_post": ArithmeticPost, "theoremqa_post": TheoremQAPost, "gsm8k_post": GSM8KPost, "mbpp_post": MbppPost, "humaneval_chatgpt": HumanEvalGPT}

def get_postprocess(postprocess_name):
    return POSTPROCESS_REGISTRY[postprocess_name]
