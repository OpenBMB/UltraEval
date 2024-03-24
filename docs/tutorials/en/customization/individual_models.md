## Deploying Your Own Model

This section involves modifying the following code files:

1. Create a new `URLs/YourModel_url.py`
2. Modify `URLs/gunicorn_conf.py` to include logic for `YourModel_url.py`

### 1. Template Code

Create a new `URLs/YourModel_url.py`. For this part, we provide a template compatible with the gunicorn framework, and you only need to implement/replace the initialization method and the inference function to adapt:

```
from flask import Flask, request, jsonify
import torch
import os
from gevent.pywsgi import WSGIServer
from URLs.dispatcher import GPUDispatcher as gdp
gdp.bind_worker_gpus()

app = Flask(__name__)

print("Initializing model and tokenizer...")

# model_name = os.environ.get('HF_MODEL_NAME')
port = os.environ.get('PORT')

# Load the model and tokenizer
model = #### Initialize Model ####
tokenizer = #### Initialize Tokenizer ####

print("Model and tokenizer initialized.")

# The parameters dictionary can be customized based on the characteristics of your model
params_dict = {
    "max_new_tokens": 100,
    "temperature": 0.1,
    "top_p": 0.95
}

@app.route('/infer', methods=['POST'])
def main():
    datas = request.get_json()
    params = datas["params"]
    prompt = datas["instances"]

    for key, value in params.items():
        if key == "max_tokens":
            params_dict["max_new_tokens"] = value
        elif key in params_dict:
            params_dict[key] = value
    if prompt == "":
        return jsonify({'error': 'No prompt provided'}), 400
    
    # Call the tokenizer; this interface needs to be defined
    inputs = tokenizer(prompt)  # Prepare the input tensor

    # Call the model's inference function; this interface needs to be defined
    generate_ids = model.generate(inputs.input_ids, attention_mask=inputs.attention_mask, **params_dict)

    # Decoding the generated ids to text
    generated_text = tokenizer.batch_decode(generate_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)
    assert len(prompt) == len(generated_text)
    for j in range(len(prompt)):
        generated_text[j] = generated_text[j][len(prompt[j]):]
    return jsonify(generated_text)

if __name__ == '__main__':
    # Run the Flask app
    http_server = WSGIServer(('127.0.0.1', port), app)
    http_server.serve_forever()
```

### 2. Example: Deploying a Model with transformers

The following example demonstrates the use of the template for deploying with transformers, assuming the file is named "transformers_url_m.py":

```
from flask import Flask, request, jsonify
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import os
from gevent.pywsgi import WSGIServer
from URLs.dispatcher import GPUDispatcher as gdp
gdp.bind_worker_gpus()

app = Flask(__name__)

print("Initializing model and tokenizer...")

# Set the device to GPU if available
device = 'cuda' if torch.cuda.is_available() else 'cpu'

model_name = os.environ.get('HF_MODEL_NAME')
port = os.environ.get('PORT')

# Load the model and tokenizer
#### Initialize Model ####
model = AutoModelForCausalLM.from_pretrained(model_name).to(device)
#### Initialize Tokenizer ####
tokenizer = AutoTokenizer.from_pretrained(model_name)

# This is a special adaptation for deploying models with the transformers library
if tokenizer.pad_token is None:
    tokenizer.add_special_tokens({'pad_token': '[PAD]'})
    model.resize_token_embeddings(len(tokenizer))

print("Model and tokenizer initialized.")

# The parameters dictionary can be customized based on the characteristics of your model
params_dict = {
    "max_new_tokens": 100,
    "temperature": 0.1,
    "top_p": 0.95
}

@app.route('/infer', methods=['POST'])
def main():
    datas = request.get_json()
    params = datas["params"]
    prompt = datas["instances"]

    for key, value in params.items():
        if key == "max_tokens":
            params_dict["max_new_tokens"] = value
        elif key in params_dict:
            params_dict[key] = value
    if prompt == "":
        return jsonify({'error': 'No prompt provided'}), 400
    
    # Call the tokenizer; this interface needs to be defined
    inputs = tokenizer(prompt, padding=True, return_tensors="pt").to(device)  # Prepare the input tensor

    # Call the model's inference function; this interface needs to be defined
    generate_ids = model.generate(inputs.input_ids, **params_dict)

    # Decoding the generated ids to text
    generated_text = tokenizer.batch_decode(generate_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)
    assert len(prompt) == len(generated_text)
    for j in range(len(prompt)):
        generated_text[j] = generated_text[j][len(prompt[j]):]
    return jsonify(generated_text)

if __name__ == '__main__':
    # Run the Flask app
    http_server = WSGIServer(('127.0.0.1', port), app)
    http_server.serve_forever()
```

### 3. Configuration and Startup

Modify `gunicorn_conf.py` and `start_gunicorn.sh` files to accommodate the newly deployed model.

- **start_gunicorn.sh**: No modification needed, but note the new possible values for the `INFER_TYPE` parameter, which need to correspond with modifications in `gunicorn_conf.py`.
- **gunicorn_conf.py**: Assign the appropriate values to the `wsgi_app` variable based on the `infer_type` variable's value.

```
import os
import sys
from URLs.dispatcher import GPUDispatcher

# gunicorn config & hook

gdp = GPUDispatcher()

port = os.environ.get('PORT')
infer_type = os.environ.get('INFER_TYPE')

bind = '127.0.0.1:' + port
workers = gdp.workers_num()

# Determine deploy type, currently support 'vLLM' and 'transformers'
if infer_type == "vLLM":
    wsgi_app = 'URLs.vllm_url_m:app'
#### ADD YOUR CODE BELOW ####
elif infer_type == "transformers":
    wsgi_app = 'URLs.transformers_url_m:app'

proc_name = 'infer' 
accesslog = '-'
timeout = 300

# ...(other parts of the code)...
```

### 4. Testing

After modifications, test the deployment of the model.

```bash
bash URLs/start_gunicorn.sh --hf-model-name meta-llama/Llama-2-7b-hf
```

Once the deployment is successful and `Model and tokenizer initialized.` is printed correctly, you can select a simple dataset for testing.

```python
TASK_NAME=humaneval  # The task to be evaluated, use commas to separate multiple tasks
URL="http://127.0.0.1:5002/infer"  # This URL is fixed
NUMBER_OF_THREAD=2  # The number of threads, typically set to the number of GPUs/per-proc-gpus
CONFIG_PATH=configs/eval_config.json  # Path to the evaluation file
OUTPUT_BASE_PATH=test  # Path where results are saved

# Step 1
# Select the task for evaluation and generate the evaluation config file. Here, method=gen indicates a generative method
python configs/make_config.py --datasets $TASK_NAME --method gen

# Step 4
# Execute the Python script
python main.py \
    --model general \
    --model_args url=$URL,concurrency=$NUMBER_OF_THREAD \
    --config_path $CONFIG_PATH \
    --output_base_path $OUTPUT_BASE_PATH \
    --batch_size 1 \
    --postprocess general_torch \
    --params models/model_params/vllm_sample.json \
    --write_out \
    #--limit 32
```