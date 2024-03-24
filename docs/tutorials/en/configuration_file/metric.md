## Evaluation Methods

We construct a variety of common metrics to meet the requirements of different evaluation methods.

After the post-processing process, UltraEval needs to compare the model's output with the correct answer to calculate the corresponding metric. In `metrics/`, we have defined a variety of evaluation metrics.

**Taking prefix_match as an example:**

```python
from typing import Any

class PrefixMatch:
    def __init__(self):
        pass

    def __call__(self, doc, ground_truth, results) -> Any:
        """
        Calculate and return the metric result for a single piece of data.
        doc: The entire data in UltraEval format, offering a flexible way of handling data.
        ground_truth: The correct answer, corresponding to the processed_output in transform.py, i.e., the post-processed answer.
        results: The model's output, also post-processed.
        Return value: If the model's output (results[0]), after trimming leading and trailing spaces, starts with the correct answer, it returns 1 (indicating the question is answered correctly); otherwise, it returns 0 (answered incorrectly).
        """
        # Compare if the beginning part of the processed model output matches the correct answer
        return 1.0 if results[0].strip().startswith(ground_truth.strip()) else 0.0
```