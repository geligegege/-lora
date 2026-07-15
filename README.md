# EQ Reply LoRA

一个基于 Qwen2.5 与 LLaMA-Factory 的“高情商回复”LoRA 微调项目，包含中文对话数据集、清洗脚本、训练/推理配置和 vLLM 部署脚本。

## 项目目标

针对尴尬沟通、工作冲突、情绪安慰、家庭边界、社交场景和被冒犯反击等问题，通过监督微调让模型生成更自然、得体且具有边界感的中文回复。

## 项目内容

- 1,000+ 条高情商回复 Alpaca 格式数据。
- 训练集、验证集、全量数据和 CSV 预览。
- 数据清洗脚本及清洗报告。
- Qwen2.5-3B-Instruct LoRA SFT 配置。
- 训练日志、验证集评估与最佳模型加载策略。
- Hugging Face 推理配置。
- 支持 LoRA Adapter 的 vLLM 服务脚本。
- 完整 LLaMA-Factory 源码环境，便于复现实验。

## 数据类别

| 类别 | 场景示例 |
| --- | --- |
| 工作 | 被催进度、临时加活、甩锅、客户投诉 |
| 感情 | 吃醋、冷战、争吵、安全感、异地恋 |
| 家庭 | 催婚、比较、隐私、父母干涉 |
| 社交 | 借钱、劝酒、玩笑过界、爽约 |
| 情绪安慰 | 焦虑、失败、失恋、自责、迷茫 |
| 被怼反击 | 嘲讽、阴阳怪气、贬低、网络争论 |
| 校园学习 | 成绩比较、老师批评、小组协作 |

## 目录结构

```text
lora/
├── eq_reply_finetune_dataset_v3/   # 原始数据、拆分与说明
├── eq_reply_train_clean.jsonl       # 清洗后的训练集
├── eq_reply_eval_clean.jsonl        # 清洗后的验证集
├── clean.py                         # 数据清洗脚本
├── clean_report.json                # 清洗统计
├── start_eq_reply_vllm.sh           # vLLM + LoRA 服务
└── LLaMA-Factory/
    ├── train_eq_reply_qwen_lora.yaml
    ├── infer_eq_reply.yaml
    ├── train_eq_reply_gpu0.sh
    └── data/                        # 注册后的训练数据
```

## 快速开始

### 1. 准备环境

建议使用支持 CUDA 的 Linux 环境。进入 LLaMA-Factory 后按其官方说明安装：

```bash
cd LLaMA-Factory
uv sync
```

基础模型默认为 `Qwen/Qwen2.5-3B-Instruct`。

### 2. 检查数据注册

`LLaMA-Factory/data/dataset_info.json` 中应包含：

- `eq_reply_train_clean`
- `eq_reply_eval_clean`

对应数据位于 `LLaMA-Factory/data/`。

### 3. 启动 LoRA 训练

```bash
cd LLaMA-Factory
./train_eq_reply_gpu0.sh
```

核心参数位于 `train_eq_reply_qwen_lora.yaml`：LoRA rank 16、alpha 32、3 个 epoch、余弦学习率调度，并按验证集损失加载最佳模型。

也可以前台运行：

```bash
uv run llamafactory-cli train train_eq_reply_qwen_lora.yaml
```

### 4. 推理验证

```bash
uv run llamafactory-cli chat infer_eq_reply.yaml
```

### 5. 使用 vLLM 部署

```bash
cd ..
./start_eq_reply_vllm.sh
```

脚本默认监听 `127.0.0.1:8001`，支持通过 `CUDA_VISIBLE_DEVICES`、`MODEL_NAME`、`ADAPTER_PATH`、`VLLM_PORT` 等环境变量覆盖配置。

## GitHub 包说明

为控制仓库体积，压缩包不包含虚拟环境、模型缓存、训练检查点、优化器状态、日志及嵌套 Git 历史。LoRA Adapter 可通过 GitHub Release、Hugging Face Hub 或其他模型仓库单独发布。

## 许可说明

本项目包含 LLaMA-Factory 源码，其许可与引用要求见 `LLaMA-Factory/LICENSE` 和 `LLaMA-Factory/CITATION.cff`。基础模型与数据发布前也应分别核对对应许可。
