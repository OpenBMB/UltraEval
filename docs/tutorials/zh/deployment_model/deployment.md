## 单实例部署模型


对于需要部署单个模型实例的用户，可以利用 Flask 框架将模型部署为 URL 接口。使用以下命令来进行部署：

```
python URLs/vllm_url.py --model_name $MODEL_NAME --gpuid $GPU_ID --port $PORT
```

- 参数说明：
  - `$MODEL_NAME`，模型名称
    - 请确保名称与 HuggingFace 平台上的模型名称一致，格式为“机构名/模型名”（例如：`meta-llama/Llama-2-7b-hf`, `baichuan-inc/Baichuan2-13B-Chat`）。
    - 可参考 vLLM [官方文档](https://docs.vllm.ai/en/latest/models/supported_models.html)查看支持的模型列表。
    - 也可以提供下载好的模型路径。
  - `$GPU_ID`：指定用于部署模型的 GPU 编号，用英文逗号分隔，默认使用 GPU 0
    - 如“0,1”表示使用两张显卡来部署一个模型。
    - GPU 编号可以通过终端命令 `nvidia-smi` 查看。
    - 注意显存限制。若单卡部署失败，可尝试多卡部署。例如，使用 A800*80G 显卡可以成功部署 34B 以下模型，而 70b 模型则需要两张显卡。
    - 若遇到显存未满但 Ray 报错杀死进程，可调整 Ray 环境变量：
        ```
        export RAY_memory_usage_threshold=0.99
        export RAY_memory_monitor_refresh_ms=0
        ```
        - `RAY_memory_usage_threshold`：设置节点内存使用阈值。值为 0.99 表示内存使用达到总内存的 99% 时，Ray 开始释放内存
        - `RAY_memory_monitor_refresh_ms`：设置内存监控刷新间隔。值为 0 禁用内存超用的工作进程杀死行为。
  - `$PORT`：部署生成的 URL 端口号，默认为 5002。
    - 避免使用已被占用的端口号。
    - 部署多个模型实例时，确保每个实例使用不同的端口。

部署成功后，终端将显示“model load finished”和“Running on http://127.0.0.1:$PORT”等提示信息。
