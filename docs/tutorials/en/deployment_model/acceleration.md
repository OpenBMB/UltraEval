## Multi-Instance Model Deployment - Acceleration

Gunicorn+Flask+(vLLM/transformers) Multi-GPU Acceleration Framework

When ample GPU resources are available, it's crucial to effectively utilize multiple GPUs. Our provided Gunicorn framework is designed to address this need, consisting of the following core components: `dispatcher.py`, `gunicorn_conf.py`, `start_gunicorn.sh`, and either `vllm_url_m.py` or `transformers_url_m.py`. Here is a detailed introduction and usage guide for these components:

- `dispatcher.py` - GPU Allocation and Management

  - Utilizes the `pynvml` library to initialize and retrieve the number of available GPUs.
  - The `GPUDispatcher` class is responsible for allocating and releasing GPU resources for each worker process.
  - Ensures all processes share GPU resources fairly and efficiently.

- `gunicorn_conf.py` - Gunicorn Server Configuration, customizes server's running parameters, primarily includes three parameters:

  - `bind`: Sets the server's address and port.
  - `workers`: Determines the number of worker processes based on the number of GPUs, i.e., the number of deployed model instances.
  - `wsgi_app`: Specifies the path to the WSGI application.

- `start_gunicorn.sh` - Startup Script

  - This script is mainly used to parse command-line arguments and set corresponding environment variables to start the Gunicorn server.
  - It's particularly suitable for deploying most models on huggingface (LLM) under various GPU resources and model configurations.
  - Allows users to specify the model name, the number of GPUs required per subprocess, and the inference method through command-line arguments.
  - The script first uses the `getopt` command to parse long-format command-line arguments, then sets environment variables based on parsing results, and finally starts the Gunicorn server.

- `vllm_url_m.py` - A variant of vllm_url.py adapted for the multi-card framework

  A variation of `vllm_url.py` optimized for a multi-GPU framework, adapted for deployment with Gunicorn. Key functionalities include:

  - **Model and Parameter Initialization**: The script first reads the model name (`HF_MODEL_NAME`) and the number of GPUs required per process (`PER_PROC_GPUS`) from environment variables, then initializes the LLM model based on these parameters.
  - **Parameter Configuration**: Sets up a default parameter dictionary `params_dict`, including various key parameters controlling text generation behavior (such as temperature, Top-K, Top-P, etc.).
  - **Web Server and Routing**: Creates a web application with Flask and defines an `/infer` route for handling POST requests containing input data and parameters for text generation.
  - **Processing Requests and Generating Responses**: Upon receiving a POST request, the server extracts parameters and instance data from the request body, generates text using the LLM, and returns the generated text or corresponding probability logs as a JSON response.
  - **Gunicorn Server Support**: Provides service for the Flask application via a Gunicorn WSGI server, ensuring stable operation in a multi-GPU environment.

- `transformers_url_m.py` - A variant of transformers_url.py adapted for the multi-card framework
  - Functionally similar to `vllm_url_m.py`, but adapted for a broader range of models (transformers support deploying many more models than vLLM), though deployment and inference speed and efficiency may be relatively lower with transformers.