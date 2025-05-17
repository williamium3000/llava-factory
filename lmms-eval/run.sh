accelerate launch \
    --num_processes=4 \
    -m lmms_eval \
    --model tinyllava \
    --model_args pretrained=/myfiles/project/llava-factory/work_dirs/llava-Qwen3-8B-clip-vit-large-patch14-336-base-finetune,conv_mode=qwen2_instruct \
    --tasks mme,vqav2,gqa,scienceqa_img,textvqa,mmvet,pope,mme,mmmu_val \
    --batch_size 1 \
    --log_samples \
    --log_samples_suffix llava-Qwen3-8B-clip-vit-large-patch14-336-base-finetune \
    --output_path ./logs/


accelerate launch \
    --num_processes=4 \
    -m lmms_eval \
    --model tinyllava \
    --model_args pretrained=work_dirs/llava-vicuna-7b-v1.5-clip-vit-large-patch14-336-base-finetune,conv_mode=llama \
    --tasks mme,vqav2,gqa,scienceqa_img,textvqa,mmvet,pope,mme,mmmu_val \
    --batch_size 1 \
    --log_samples \
    --log_samples_suffix llava-vicuna-7b-v1.5-clip-vit-large-patch14-336-base-finetune \
    --output_path ./logs/
