## Model Instantiation

After the model is successfully deployed, a URL is generated. The first step is to instantiate the model. In the `models` directory, we provide two types of scripts, `general_model.py` for URL instantiation, and `openai_model.py` for API services. Within these, the `Model` class and the request forwarding method `_post_request` are defined.

- The `Model` class includes three methods: initialization, `loglikelihood`, and `generate`.
  - The initialization uses model_args passed from the main file to instantiate the model.
  - `loglikelihood` and `generate` correspond to the model's inference methods, respectively. If users evaluate their trained models, they need to implement these two functionalities in their inference code.
- During the evaluation process, all data is sent to the `Model` class. Depending on the inference method, it's handled by either the `loglikelihood` or `generate` function. Then, the passed `params` and `instance` are extracted and sent to the model for inference through the `_post_request` method. Finally, the results generated by the model are returned to the evaluation process for post-processing.