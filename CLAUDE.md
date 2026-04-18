# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

TinyLLaVA Factory is a modular PyTorch/HuggingFace framework for training small-scale Large Multimodal Models (LMMs). It combines small LLMs, vision towers, and connectors into a unified architecture.

## Common Commands

### Installation
```bash
pip install -e .
pip install -e ".[train]"  # includes deepspeed, ninja, wandb
```

### Training (two-stage process)
```bash
# Stage 1: Pretrain (align vision-language features, connector unfrozen, LLM/vision frozen)
bash scripts/train/pretrain.sh

# Stage 2: Finetune (connector + LLM tuned, vision tower frozen)
bash scripts/train/finetune.sh

# Custom dataset finetuning (LoRA)
bash scripts/train/custom_finetune.sh

# Model-specific training (runs both stages)
bash scripts/train/train_phi.sh
```

All training uses DeepSpeed. The core entry point is:
```bash
deepspeed --master_port 29501 tinyllava/train/train.py \
    --deepspeed ./scripts/train/zero3.json \
    [model/data/training args...]
```

### Evaluation
```bash
# Individual benchmarks
bash scripts/eval/vqav2.sh
bash scripts/eval/gqa.sh
bash scripts/eval/textvqa.sh
bash scripts/eval/pope.sh
bash scripts/eval/mme.sh
bash scripts/eval/sqa.sh
bash scripts/eval/mmvet.sh
bash scripts/eval/mmmu.sh
```

### Inference
```bash
# Web UI demo
python tinyllava/serve/app.py
# CLI interactive inference
python tinyllava/serve/cli.py
# Quick test
python test.py
```

## Architecture

### Three-Component Model (`tinyllava/model/modeling_tinyllava.py`)

`TinyLlavaForConditionalGeneration` composes three pluggable components:

1. **LLM** (`tinyllava/model/llm/`) — Phi-2, Qwen 2/2.5/3, Gemma, TinyLlama, StableLM, OpenELM
2. **Vision Tower** (`tinyllava/model/vision_tower/`) — CLIP, SigLIP, DINOv2, MOF (dual-vision)
3. **Connector** (`tinyllava/model/connector/`) — MLP, QFormer, Resampler, Linear, Identity

Each component type has a factory with `@register` decorator pattern (see `__init__.py` in each subdir). Adding a new component means creating a file and registering it with the factory.

### Training Pipeline

- **Entry point**: `tinyllava/train/train.py` — parses args, builds config, loads recipe, trains
- **Trainer**: `tinyllava/train/tinyllava_trainer.py` — extends HF Trainer
- **Training Recipes** (`tinyllava/training_recipe/`): `common`, `lora`, `qlora` — control which parts are frozen/tuned via `tune_type_llm`, `tune_type_vision_tower`, `tune_type_connector` args
- **Arguments**: All training args defined as dataclasses in `tinyllava/utils/arguments.py`

### Data Pipeline

- **Dataset**: `tinyllava/data/dataset.py` — `LazySupervisedDataset` loads JSON annotations (local, HTTP, or S3)
- **JSON format**: `[{"id": str, "image": path, "conversations": [{"from": "human"|"gpt", "value": str}]}]`
- **Text templates**: `tinyllava/data/template/` — model-specific chat formatting (phi, llama, gemma, qwen2, pretrain)
- **Image preprocessing**: `tinyllava/data/image_preprocess.py`
- **S3 support**: Data can be loaded from S3 via `s3_config` argument (requires boto3)

### Key Config Files

- `scripts/train/zero3.json` / `zero2.json` — DeepSpeed ZeRO configs
- `scripts/train/config.yaml` — multi-node training config
- `.deepspeed_env` — DeepSpeed environment variables

## Key Constants (`tinyllava/utils/constants.py`)

- `IMAGE_TOKEN_INDEX = -200`
- `IGNORE_INDEX = -100`
- `DEFAULT_IMAGE_TOKEN = "<image>"`

## Dependencies

Pinned versions: torch 2.4.1, transformers 4.51.3, deepspeed 0.14.4, accelerate 0.27.2, peft 0.10.0. See `pyproject.toml` for full list.
