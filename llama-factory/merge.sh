#!/bin/bash
# DO NOT use quantized model or quantization_bit when merging lora weights

CUDA_VISIBLE_DEVICES= python ../LLaMA-Factory/src/train_bash.py \
    --model_name_or_path Qwen/Qwen1.5-7B-Chat \
    --adapter_name_or_path ./saves/zztj_pretrain \
    --template qwen \
    --finetuning_type lora \
    --export_dir ./saves/zztj_pretrain_merged \
    --export_size 2 \
    --export_legacy_format False