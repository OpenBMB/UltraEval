## 模型实例化


模型部署成功后，会产生一个URL。首先需要进行实例化。我们在`models`目录下提供了两类脚本，`general_model.py`对应URL实例化, `openai_model.py`对应API服务。其中，定义了`Model`类和请求转接方法`_post_request`。

- `Model`类包含了初始化、`loglikelihood`和`generate`三个方法。
  - 初始化使用main文件中传入的model_args，实例化model。
  - `loglikelihood`和`generate`分别和模型推理的方式是对应的。如果用户评测自己训练的模型，则需要在推理代码中，实现这两部分对应的功能。
- 在评测过程中，所有的数据会传送到`Model`类中，根据推理方式不同，交给`loglikelihood`或`generate`函数，然后提取传入的`params`和`instance`，通过`_post_request`方法将包装后的数据给到模型进行推理。最后将模型生成的结果，返回到评测过程中，进行后处理。

