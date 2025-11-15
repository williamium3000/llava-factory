# install lmms_eval without building dependencies
# cd lmms_eval;
# pip install --no-deps -U -e .

# # install TinyLLaVA without building dependencies
# cd ..
# git clone https://github.com/TinyLLaVA/TinyLLaVA_Factory
# cd TinyLLaVA_Factory
# pip install --no-deps -U -e .

# install all the requirements that require for reproduce llava results
# pip install torch==2.0.1 torchvision==0.15.2 --index-url https://download.pytorch.org/whl/cu118
# pip install -r tinyllava_repr_requirements.txt

# Run and reproduce tinyllava best results!
export NCCL_IGNORE_DISABLED_P2P=1
accelerate launch \
    --num_processes=8 \
    -m lmms_eval \
    --model tinyllava \
    --model_args pretrained=../work_dirs/llava-Qwen3-8B-clip-vit-large-patch14-336-base-cc15m-pt-finetune-llava_v1_5_mix665k,conv_mode=qwen2_instruct \
    --tasks vqav2,gqa,scienceqa_img,textvqa,mmvet,pope,mme,mmmu_val \
    --batch_size 1 \
    --log_samples \
    --log_samples_suffix llava-Qwen3-8B-clip-vit-large-patch14-336-base-cc15m-pt-finetune-llava_v1_5_mix665k \
    --output_path ./logs/