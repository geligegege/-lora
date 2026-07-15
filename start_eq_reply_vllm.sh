#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 可通过环境变量覆盖 CUDA、模型、LoRA 适配器及服务参数。
export CUDA_HOME="${CUDA_HOME:-${PROJECT_DIR}/.venv/lib/python3.12/site-packages/nvidia/cu13}"
export PATH="$CUDA_HOME/bin:$PATH"
export CUDA_DEVICE_ORDER=PCI_BUS_ID
export CUDA_VISIBLE_DEVICES="${CUDA_VISIBLE_DEVICES:-0}"
export VLLM_USE_FLASHINFER_SAMPLER=0

VLLM_BIN="${VLLM_BIN:-${PROJECT_DIR}/.venv/bin/vllm}"
MODEL_NAME="${MODEL_NAME:-Qwen/Qwen2.5-3B-Instruct}"
ADAPTER_PATH="${ADAPTER_PATH:-${PROJECT_DIR}/LLaMA-Factory/saves/qwen2.5-3b/lora/eq_reply}"

exec "$VLLM_BIN" serve "$MODEL_NAME" \
  --enable-lora \
  --lora-modules "eq-reply=${ADAPTER_PATH}" \
  --max-lora-rank 16 \
  --chat-template "${ADAPTER_PATH}/chat_template.jinja" \
  --host "${VLLM_HOST:-127.0.0.1}" \
  --port "${VLLM_PORT:-8001}" \
  --gpu-memory-utilization "${GPU_MEMORY_UTILIZATION:-0.7}" \
  --enforce-eager \
  --max-model-len "${MAX_MODEL_LEN:-8192}"
