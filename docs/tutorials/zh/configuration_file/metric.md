## 评估方法


构建了一些常用的metric，以适应不同的评测方式的要求。

经过后处理流程后，UltraEval需要对比模型的输出和正确答案以计算对应指标。在 `metrics/`中，我们定义了多种评价指标。

**以prefix_match为例：**

```
from typing import Any

class PrefixMatch:
    def __init__(self):
        pass

    def __call__(self, doc, ground_truth, results) -> Any:
        """
        计算并返回单条数据的评价指标结果。
        doc: UltraEval格式的整条数据，提供灵活的数据处理方式。
        ground_truth: 正确答案，与transform.py中的processed_output相对应，即经过后处理的答案。
        results: 模型输出，同样经过后处理。
        返回值：如果模型输出（results[0]）在去除首尾空格后以正确答案开始，则返回1（即此问题答对），否则返回0（答错）。
        """
        # 比较经过处理的模型输出的起始部分是否与正确答案一致
        return 1.0 if results[0].strip().startswith(ground_truth.strip()) else 0.0
```