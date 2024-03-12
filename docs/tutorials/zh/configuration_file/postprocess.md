## 后处理


对模型的输出进行清洗处理，以适应不同的评测方式的要求。

在计算评估指标（metric）之前，UltraEval会对模型输出进行必要的后处理。这个后处理过程分为两个层面：模型层面的后处理以及任务层面的后处理。这个过程通过postprocess.py文件实现。

- **模型层面后处理**：不同的模型的输出，可能会有不同，所以统一提取出真正的模型输出。
- **任务层面后处理**（根据任务可选）：这一步骤着重于通过更精确地提取或规范化模型输出，以便能够更准确地与正确答案进行比较，从而计算出更加准确的评估指标。

本节中所提及的“后处理”一般指任务层面的后处理。任务层面的后处理通过config中的postprocess进行指定。模型层面的后处理，则可通过 `main` 文件的 `postprocess` 参数进行设置。

在 `tasks/postprocess.py` 文件中，我们定义了多种后处理方法供选择和应用。

**以UntilReturnPost为例：**

```
class UntilReturnPost:
    def __init__(self):
        pass

    def __call__(self, raw_outputs, processed_outputs):
        # 重新定义__call__方法，用于处理输出
        processed_outputs_ = []
        
        # 如果processed_outputs是字符串类型，为了统一处理，将其转换为列表
        if isinstance(processed_outputs, str):  
            processed_outputs = [processed_outputs]
        
        # 遍历处理后的输出
        for output in processed_outputs:
            # 去除每个输出的首尾空白，然后截取第一个换行符之前的内容，并再次去除首尾空白
            output = output.strip().split('\n')[0].strip()
            processed_outputs_.append(output)

        # 返回原始输出和处理后的输出
        return raw_outputs, processed_outputs_

# 注：在POSTPROCESS_REGISTRY中需注册自定义后处理类
```