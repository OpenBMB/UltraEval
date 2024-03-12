## 新的后处理方法

- 添加postprocess类
  - 在`tasks/postprocess.py`中，参照[【 postprocess介绍 】](../configuration_file/postprocess.md)教程，添加自定义后处理类。
  - 在`tasks/postprocess.py`中的`POSTPROCESS_REGISTRY`字典中注册你的自定义后处理类。
