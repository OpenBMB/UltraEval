## Deploying a Single Model Instance

For users who need to deploy a single model instance, the Flask framework can be used to deploy the model as a URL interface. Use the following command for deployment:

```
python URLs/vllm_url.py --model_name $MODEL_NAME --gpuid $GPU_ID --port $PORT
```

- Parameter Explanation:
  - `$MODEL_NAME`, the model name
    - Ensure the name matches the model name on the HuggingFace platform, formatted as "organization/model" (e.g., `meta-llama/Llama-2-7b-hf`, `baichuan-inc/Baichuan2-13B-Chat`).
    - Refer to the vLLM [official documentation](https://docs.vllm.ai/en/latest/models/supported_models.html) to view the list of supported models.
    - A downloaded model path can also be provided.
  - `$GPU_ID`: Specifies the GPU ID for deploying the model, separated by commas, defaulting to GPU 0
    - For example, "0,1" means using two graphics cards to deploy a model.
    - GPU IDs can be viewed using the terminal command `nvidia-smi`.
    - Be aware of memory limitations. If single-card deployment fails, try multi-card deployment. For instance, a model below 34B can be successfully deployed on an A800*80G graphics card, while a 70b model requires two graphics cards.
    - If encountering a situation where the process is killed by Ray even though the memory is not full, adjust the Ray environment variables:
        ```
        export RAY_memory_usage_threshold=0.99
        export RAY_memory_monitor_refresh_ms=0
        ```
        - `RAY_memory_usage_threshold`: Sets the memory usage threshold within a node. A value of 0.99 means Ray starts releasing memory when memory usage reaches 99% of the total memory.
        - `RAY_memory_monitor_refresh_ms`: Sets the refresh interval for memory monitoring. A value of 0 disables the behavior of killing overused work processes due to memory.
  - `$PORT`: The port number for the deployed URL, defaulting to 5002.
    - Avoid using ports that are already occupied.
    - When deploying multiple model instances, ensure each instance uses a different port.

Upon successful deployment, the terminal will display messages like “model load finished” and “Running on http://127.0.0.1:$PORT”.

(For users with multiple graphics cards, refer to [Multi-Card Deployment](./acceleration.md))