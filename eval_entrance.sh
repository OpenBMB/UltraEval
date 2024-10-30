set -ex

# bash eval_entrance.sh /path/to/the/huggingface/model/ 8 piqa,siqa,hellaswag,winogrande,copa,boolq,agieval ppl
# bash eval_entrance.sh /path/to/the/huggingface/model/ 8 humaneval,mbpp,lambada,tydiqa,gsm8k,mmlu,bbh gen

CKPT=$1
NUM_GPUS=$2
VISIBLE_GPUS="0,1,2,3,4,5,6,7"
TASK=$3
METHOD=$4
PORT=9876

export HF_ENDPOINT=https://hf-mirror.com

bash scripts/run_job_base.sh $CKPT $NUM_GPUS 1 $CKPT/eval_results $TASK $METHOD -1 $VISIBLE_GPUS $PORT transformers
