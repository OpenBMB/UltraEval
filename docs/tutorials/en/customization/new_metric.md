## Adding a New Evaluation Method

- **Writing a Metric File**
  - In the `metrics/` directory, create a new Python file for your evaluation metric, naming it `metrics/{metric_name}.py`.
  - Refer to the [Metric Introduction](../configuration_file/metric.md) tutorial to complete writing the corresponding MetricName class in `metrics/{metric_name}.py`.
  - Register it in `metrics/__init__.py` by adding `from .metric_name import MetricName` and registering your custom evaluation metric class in the `METRICS_REGISTRY` dictionary.