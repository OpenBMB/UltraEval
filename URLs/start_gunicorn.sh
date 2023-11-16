#!/bin/bash

# 初始化变量
HF_MODEL_NAME=""
PER_PROC_GPUS=1 # 每个子进程占用GPU数，默认全部占用，单进程；该值必须能被POD内可用GPUs总数整除，worker数量=gpu总数/该数值

# 解析长选项
options=$(getopt -o "" --long hf-model-name:,per-proc-gpus: -- "$@")

# 设置解析后的参数
eval set -- "$options"

# 遍历解析后的选项和参数
while true; do
    case $1 in
        --hf-model-name)
            HF_MODEL_NAME=$2
            shift 2
            ;;
        --per-proc-gpus)
            PER_PROC_GPUS=$2 
            shift 2
            ;;
        --)
            shift
            break
            ;;
    esac
done

# 检查是否提供了必需的 HF_MODEL_NAME
if [ -z "$HF_MODEL_NAME" ]; then
  echo "Error: You must provide HF_MODEL_NAME using --hf-model-name."
  exit 1
fi

# 导出环境变量
export PER_PROC_GPUS
export HF_MODEL_NAME


# 运行 gunicorn
gunicorn -c URLs/gunicorn_conf.py
