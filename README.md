<div align="center">

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=700&size=34&duration=2800&pause=900&color=FF6B81&center=true&vCenter=true&width=760&lines=EQ+Reply+LoRA;Fine-tune+More+Thoughtful+Replies" alt="EQ Reply LoRA animated title" />

### 一个专属于直男直女的高情商回复模型

不会接话、安慰只会说“多喝热水”、一紧张就把聊天聊死？这个模型专门负责把“我不知道怎么回”变成自然、得体又不油腻的回复。

<p>
  <img src="https://img.shields.io/badge/Base_Model-Qwen2.5--3B-7B68EE" alt="Qwen2.5" />
  <img src="https://img.shields.io/badge/Method-LoRA-FF6B81" alt="LoRA" />
  <img src="https://img.shields.io/badge/Framework-LLaMA--Factory-2E8B57" alt="LLaMA-Factory" />
  <img src="https://img.shields.io/badge/Serving-vLLM-00A6D6" alt="vLLM" />
  <img src="https://img.shields.io/badge/Dataset-1K%2B_Chinese_Samples-F5A623" alt="Dataset" />
  <img src="https://img.shields.io/badge/Status-Experimenting-orange" alt="Status" />
</p>

<p>
  <a href="#-项目目标">项目目标</a> ·
  <a href="#-数据类别">数据类别</a> ·
  <a href="#-快速开始">快速开始</a> ·
  <a href="#deploy">部署</a>
</p>

</div>

---

## 🎯 项目目标

我们想做一个“聊天救场器”，送给每一个面对消息框反复输入、删除，最后只发出一个“哦”的直男直女。

它不教人说虚假的漂亮话，也不生成千篇一律的网络话术，而是希望模型能先理解情绪和关系，再给出自然、得体、有分寸的中文回复。无论是对象生气、同事甩锅、父母催婚，还是朋友陷入低谷，它都尽量做到：**接得住情绪，说得清态度，也守得住边界。**

## ✨ 项目内容

为了让模型不再把天聊死，我们准备了覆盖真实沟通难题的数据：

- 1,000+ 条高情商回复 Alpaca 格式数据。
- 训练集、验证集、全量数据和 CSV 预览。
- 数据清洗脚本及清洗报告。
- Qwen2.5-3B-Instruct LoRA SFT 配置。
- 训练日志、验证集评估与最佳模型加载策略。
- Hugging Face 推理配置。
- 支持 LoRA Adapter 的 vLLM 服务脚本。
- 完整 LLaMA-Factory 源码环境，便于复现实验。

## 📊 数据类别

从“对象问你哪里错了”到“领导临时加活怎么回”，常见的聊天高危场景基本都在这里：

| 类别 | 场景示例 |
| --- | --- |
| 工作 | 被催进度、临时加活、甩锅、客户投诉 |
| 感情 | 吃醋、冷战、争吵、安全感、异地恋 |
| 家庭 | 催婚、比较、隐私、父母干涉 |
| 社交 | 借钱、劝酒、玩笑过界、爽约 |
| 情绪安慰 | 焦虑、失败、失恋、自责、迷茫 |
| 被怼反击 | 嘲讽、阴阳怪气、贬低、网络争论 |
| 校园学习 | 成绩比较、老师批评、小组协作 |

## 📁 目录结构

```text
lora/
├── eq_reply_finetune_dataset_v3/   # 原始数据、拆分与说明
├── eq_reply_train_clean.jsonl       # 清洗后的训练集
├── eq_reply_eval_clean.jsonl        # 清洗后的验证集
├── clean.py                         # 数据清洗脚本
├── clean_report.json                # 清洗统计
├── start_eq_reply_vllm.sh           # vLLM + LoRA 服务
├── llamafactory_configs/            # 本项目自己的训练与推理配置
│   ├── train_eq_reply_qwen_lora.yaml
│   ├── infer_eq_reply.yaml
│   ├── dataset_info_patch.json
│   └── train_eq_reply_gpu0.sh
└── LLaMA-Factory/                   # 空占位目录，按说明下载官方框架
```

## 🚀 快速开始

### 1️⃣ 下载 LLaMA-Factory

`LLaMA-Factory/` 只是占位目录，官方框架没有重复放入本仓库。首次使用时在项目根目录运行：

```bash
rm -f LLaMA-Factory/.gitkeep
git clone --depth 1 https://github.com/hiyouga/LLaMA-Factory.git
cd LLaMA-Factory
uv sync
```

如需严格复现本项目开发时使用的框架版本，可在克隆后执行：

```bash
git checkout b7615dbdc9f95c169361dacad1185852c4d28521
```

基础模型默认为 `Qwen/Qwen2.5-3B-Instruct`，模型权重会由 Hugging Face/ModelScope 在首次运行时下载。

### 2️⃣ 放置数据并注册

把项目根目录的清洗数据复制到 LLaMA-Factory：

```bash
cp eq_reply_train_clean.jsonl LLaMA-Factory/data/
cp eq_reply_eval_clean.jsonl LLaMA-Factory/data/
```

打开 `LLaMA-Factory/data/dataset_info.json`，将 `llamafactory_configs/dataset_info_patch.json` 中的两个数据集配置合并到最外层 JSON 对象中。注册名称必须保持为：

- `eq_reply_train_clean`
- `eq_reply_eval_clean`

### 3️⃣ 修改训练配置

项目自己的配置保存在 `llamafactory_configs/`，以后更新官方框架时不会被覆盖。常用修改项：

| 需求 | 配置项 |
| --- | --- |
| 更换基础模型 | `model_name_or_path` |
| 调整显存占用 | `per_device_train_batch_size`、`gradient_accumulation_steps` |
| 改变 LoRA 容量 | `lora_rank`、`lora_alpha` |
| 调整训练轮数 | `num_train_epochs` |
| 修改输出位置 | `output_dir` |
| 改用 BF16 | 将 `fp16: true` 改为 `bf16: true` |

### 4️⃣ 启动 LoRA 训练

后台训练：

```bash
chmod +x llamafactory_configs/train_eq_reply_gpu0.sh
./llamafactory_configs/train_eq_reply_gpu0.sh
```

前台训练：

```bash
cd LLaMA-Factory
uv run llamafactory-cli train ../llamafactory_configs/train_eq_reply_qwen_lora.yaml
```

默认使用 LoRA rank 16、alpha 32、3 个 epoch 和余弦学习率调度，并按验证集损失加载最佳模型。

### 5️⃣ 推理验证

```bash
cd LLaMA-Factory
uv run llamafactory-cli chat ../llamafactory_configs/infer_eq_reply.yaml
```

<a id="deploy"></a>

### 6️⃣ 使用 vLLM 部署

```bash
cd ..
./start_eq_reply_vllm.sh
```

脚本默认监听 `127.0.0.1:8001`，支持通过 `CUDA_VISIBLE_DEVICES`、`MODEL_NAME`、`ADAPTER_PATH`、`VLLM_PORT` 等环境变量覆盖配置。

## 📦 GitHub 包说明

为控制仓库体积，本仓库不重复保存可从官方获取的 LLaMA-Factory 源码，也不包含虚拟环境、模型缓存、训练检查点、优化器状态和日志。项目只保留自己的数据、训练配置与部署脚本；LoRA Adapter 可通过 GitHub Release、Hugging Face Hub 或其他模型仓库单独发布。

## 📄 许可说明

本项目包含 LLaMA-Factory 源码，其许可与引用要求见 `LLaMA-Factory/LICENSE` 和 `LLaMA-Factory/CITATION.cff`。基础模型与数据发布前也应分别核对对应许可。
