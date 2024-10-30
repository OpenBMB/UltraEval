from flask import Flask, request, jsonify
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import os
from gevent.pywsgi import WSGIServer
from URLs.dispatcher import GPUDispatcher as gdp
import torch.nn.functional as F
gdp.bind_worker_gpus()

app = Flask(__name__)

print("Initializing model and tokenizer...")

# Set the device to GPU if available
device = 'cuda' if torch.cuda.is_available() else 'cpu'

model_name = os.environ.get('HF_MODEL_NAME')
port = os.environ.get('PORT')

# Load the model and tokenizer
model = AutoModelForCausalLM.from_pretrained(model_name, trust_remote_code=True, torch_dtype="bfloat16").to(device)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Check and add pad token if necessary
if tokenizer.pad_token is None:
    tokenizer.pad_token_id = 0
    # tokenizer.add_special_tokens({'pad_token': '[PAD]'})
    # model.resize_token_embeddings(len(tokenizer))

print("Model and tokenizer initialized.")

params_dict = {
    "do_sample": True,
    "temperature": 0.1,
    "max_new_tokens": 400,
    "top_p": 0.95,
}

@app.route('/infer', methods=['POST'])
def main():
    try:
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

        print('max new token is ', params_dict["max_new_tokens"])

        inputs = tokenizer(prompt, padding=True, return_tensors="pt").to(device)  # Prepare the input tensor

        if "prompt_logprobs" in params and params["prompt_logprobs"] is not None:
            logits = model(inputs.input_ids, attention_mask=inputs.attention_mask)[0]
            input_ids = inputs.input_ids
            assert input_ids.shape == logits.shape[:2]

            log_prob_batch = []
            for input_id, logit in zip(input_ids, logits):
                log_prob_seq = []
                sid = torch.eq(input_id, tokenizer.bos_token_id).nonzero(as_tuple=True)[0].item()
                for i in range(sid + 1, len(input_id) - 1):
                    past, cur = i, i + 1
                    token_logit = logit[past, :]
                    token_log_probs = F.log_softmax(token_logit, dim=-1)
                    log_token_prob = token_log_probs[input_id[cur]].item()
                    log_prob_seq.append(log_token_prob)
                log_prob_batch.append(log_prob_seq)

            return jsonify(log_prob_batch)
        else:

            while True:
                try:
                    import gc
                    torch.cuda.empty_cache()
                    print('mem allocated: ', torch.cuda.memory_allocated())
                    gc.collect()

                    input_ids: torch.Tensor = inputs.input_ids
                    if input_ids.size(-1) > 3000:
                        input_ids_part1, input_ids_part2 = input_ids[:, :-3000], input_ids[:, -3000:]
                        generate_ids = model.generate(input_ids_part2, attention_mask=inputs.attention_mask[:, -3000:], **params_dict)
                        generate_ids = torch.cat((input_ids_part1, generate_ids), dim=-1)
                    else:
                        generate_ids = model.generate(inputs.input_ids, attention_mask=inputs.attention_mask, **params_dict)
                    print('no problem', inputs.input_ids.shape, generate_ids.shape)
                    break
                except Exception as e:
                    print(e)
                    print('jile', inputs.input_ids.shape)
                    params_dict['max_new_tokens'] = max(params_dict['max_new_tokens'] - 50, 1)
                    print('decrease max new tokens to', params_dict['max_new_tokens'])
            # Decoding the generated ids to text
            generated_text = tokenizer.batch_decode(generate_ids, skip_special_tokens=True,
                                                    clean_up_tokenization_spaces=False)
            assert len(prompt) == len(generated_text)
            for j in range(len(prompt)):
                generated_text[j] = generated_text[j][len(prompt[j]):]
            return jsonify(generated_text)
    except Exception as err:
        torch.save(err, "debug.pkl")
        raise err


if __name__ == '__main__':
    # Run the Flask app
    print("Begin Start Server")
    http_server = WSGIServer(('127.0.0.1', port), app)
    http_server.serve_forever()
    print("Server Initialized")
