## 添加新的评测方法


- 编写metric文件
  - 在`metrics/`目录下，为你的评测指标创建一个新的Python文件，命名为`metrics/{metric_name}.py`。
  - 参照[【metric介绍】](../configuration_file/metric.md)教程，在 `metrics/{metric_name}.py` 中完成相应MetricName类的编写。
  - 在`metrics/__init__.py`中进行注册，包括添加`from .metric_name import MetricName`，并在`METRICS_REGISTRY`字典中注册你的自定义评测指标类。