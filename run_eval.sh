#!/bin/bash

bash scripts/run_job_base.sh mistralai/Mistral-7B-v0.1 1 1 logs/mistralai/Mistral-7B-v0.1 bbh,mmlu,ceval,cmmlu,humaneval,mbpp-427,gsm8k,math,hellaswag,boolq,piqa,winogrande,arc-e,arc-c gen -1
sleep 600

bash scripts/run_job_base.sh mistralai/Mistral-7B-v0.1 1 1 logs/mistralai/Mistral-7B-v0.1B hellaswag,boolq,piqa,winogrande,arc-e,arc-c ppl -1