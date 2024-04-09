CUDA_VISIBLE_DEVICES=0 API_PORT=8000 python src/api_demo.py \
    --model_name_or_path Qwen/Qwen1.5-7B-Chat \
    --template mistral \
    --infer_backend vllm \
    --vllm_enforce_eager