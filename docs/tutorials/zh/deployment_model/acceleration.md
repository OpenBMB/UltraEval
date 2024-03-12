## 多实例部署模型-加速


Gunicorn+Flask+(vLLM/transformers) 多GPU加速框架

当GPU资源充足时，有效利用多GPU资源至关重要。我们提供的 Gunicorn 框架旨在解决这一需求，该框架由以下核心组件构成：`dispatcher.py`、`gunicorn_conf.py`、`start_gunicorn.sh` 及 (`vllm_url_m.py`/`transformers_url_m.py`)。以下为这几个组件的详细介绍及使用指南：

- `dispatcher.py` - GPU 分配与管理

  - 通过 `pynvml` 库来初始化并检索可用 GPU 数量。
  - `GPUDispatcher` 类负责各工作进程的 GPU 资源分配与释放。
  - 确保所有进程公平、高效地共享 GPU 资源。

- `gunicorn_conf.py` - Gunicorn 服务器配置，用于自定义服务器的运行参数，主要包含以下三个参数：

  - `bind`：设置服务器地址和端口
  - `workers`：根据 GPU 数量确定工作进程的数量，即部署的模型的实例个数
  - `wsgi_app`：指定 WSGI 应用程序的路径。

- `start_gunicorn.sh` - 启动脚本

  - 本脚本主要用于解析命令行参数并设置相应的环境变量，以便启动 Gunicorn 服务器。
  - 它特别适用于在不同的GPU资源和模型配置下部署huggingface上的大多数模型（LLM）。
  - 允许用户通过命令行参数指定模型名称、每个子进程所需的 GPU 数量以及使用的推理方式。
  - 脚本首先通过 getopt 命令解析长格式的命令行参数，然后根据解析结果设置环境变量，最后启动 Gunicorn 服务器。

- `vllm_url_m.py` - vllm_url.py适配于多卡框架的变种

  是针对多GPU框架优化的 `vllm_url.py` 的变体，在原有基础上适配了gunicorn的部署。主要功能如下：

  - **模型与参数初始化**：脚本首先通过环境变量读取模型名称（`HF_MODEL_NAME`）和每个进程所需的 GPU 数量（`PER_PROC_GPUS`），然后根据这些参数初始化 LLM 模型。
  - **参数配置**：设置了默认的参数字典 `params_dict`，包括控制生成文本行为的各种关键参数（如温度、Top-K、Top-P 等）。
  - **Web 服务器和路由**：通过 Flask 创建一个 Web 应用，并定义了一个 `/infer` 路由，用于处理 POST 请求，此类请求将包含文本生成的输入数据和参数。
  - **处理请求并生成响应**：服务器接收到 POST 请求后，提取请求体中的参数和实例数据，使用 LLM 进行生成，并将生成的文本或对应的概率日志作为 JSON 响应返回。
  - **Gunicorn 服务器支持**：通过 Gunicorn WSGI 服务器为 Flask 应用提供服务，并确保多GPU环境下的稳定运行。

- `transformers_url_m.py` - transformers_url.py适配于多卡框架的变种

  与上面的`vllm_url_m.py`功能基本一致，只是适配更多模型（transformers支持部署的模型远远多于vllm），但在部署推理上的速度和效率会相对低于vllm。

