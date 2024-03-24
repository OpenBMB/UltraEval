## Inference Parameter Files

Specify the relevant parameters for model inference.

UltraEval sets the parameters for model inference through `models/model_params`. Different tasks may require different model inference parameters, and the same model might use different inference parameters depending on the choice of generation sampling method. Below are three common parameter configuration files:

- `vllm_beamsearch.json` for Beam Search

```json
{
    "use_beam_search": true,  // Whether to use beam search. True indicates it is used, typically to improve the quality of generated text.
    "best_of": 10,            // In beam search or other generation strategies, choose the best output from this number of candidates.
    "temperature": 0,         // Controls the randomness of the generated text. A temperature of 0 means always choosing the highest probability word.
    "top_p": 1,               // Keep the smallest set of words whose cumulative probability reaches top_p, used to control the diversity of generated text. 1 means no filtering is applied.
    "top_k": -1,              // Keep the top_k words with the highest probability, used to control the diversity of generated text. -1 means no filtering is applied.
    "early_stopping": "never", // The condition for early stopping. "never" means generation will continue until the maximum number of tokens is reached.
    "max_tokens": 100         // The maximum number of tokens in the generated text.
}
```

- `vllm_sample.json` for Random Sampling

```json
{
    "temperature": 0.3,   // Controls the randomness of the generated text. A lower temperature (e.g., 0.1) means the generated text is more likely to lean towards high probability words, making it more deterministic and consistent.
    "top_p": 0.8,        // Keep the smallest set of words whose cumulative probability reaches 0.8. This means the model will only consider words that cumulatively reach 80% probability for generation, helping to ensure the diversity and reliability of generated text.
    "max_tokens": 100     // The maximum number of tokens in the generated text. Here set to 100, meaning the generated text will contain up to 100 tokens.
}
```

Special notes for random sampling:
    
 For direct answer choice questions and mathematical code type problems, it is recommended to set: `temperature=0.1,top_p=0.95,max_tokens=10`
    
 For mathematical code type problems, it is recommended to set: `temperature=0.1,top_p=0.95,max_tokens=200`
    
 For other types of problems, the general recommended setting is: `temperature=0.3,top_p=0.8,max_tokens=100`

- `vllm_logprobs.json` for Log Likelihood, this file generally does not need changing of parameters, and changing them does not affect evaluation

```json
{
    "prompt_logprobs": 0,   // The number of log likelihoods returned for each prompt token, not recommended to change
    "max_tokens": 1         // The maximum number of tokens in the generated text. Here set to 1, meaning that during loglikelihood inference, only one token is generated at a time.
}
```

- Note: The difference between model_params appearing in the config and main files
  - `model_params` sets parameters related to model inference, affecting only the settings for the model's inference capabilities, unrelated to the input data and prompt, etc.
  - `config` sets the default parameters related to the dataset, mainly involving default recommended settings related to the dataset, such as the task name, data path, transform file, and the specified evaluation method and metrics, among others.
  - Parameters in the main file are more about controlling the entire evaluation process. When multiple tasks are being evaluated simultaneously, and some parameters conflict with those in the config, their priorities differ:
    - For task-specific parameters like `num_fewshot`, parameters in the main file have a higher priority, allowing users to uniformly specify the fewshot for tasks;
    - For model-specific parameters `model_params`, parameters in the config have a higher priority, with parameters in the main file being more general and special tasks treated specially.