# 高情商回复微调数据集 v3（Alpaca 格式）

## 数据规模

- 全量数据：1166 条
- 训练集：1026 条
- 验证集：140 条

## 类别分布

{
  "工作": 221,
  "感情": 205,
  "被怼反击": 173,
  "情绪安慰": 173,
  "家庭": 173,
  "社交": 173,
  "校园学习": 48
}

## 任务定义

输入一个尴尬、冲突、情绪化或需要体面沟通的场景，模型输出更合适的高情商回复。

覆盖类别：

- 感情：安全感、吃醋、冷战、撒娇、争吵、承诺、暧昧拉扯、异地恋
- 工作：被否定、被催进度、被甩锅、临时加活、客户投诉、跨部门协作、面试表达
- 家庭：催婚、比较、催工作、打听隐私、家庭边界、父母干涉感情
- 社交：借钱、劝酒、被问隐私、玩笑过界、爽约、尴尬破冰、被起哄
- 被怼反击：辱骂、阴阳怪气、嘲讽、贬低、网络争论
- 情绪安慰：焦虑、失败、失恋、自责、迷茫、崩溃、孤独
- 校园学习：成绩比较、老师批评、小组协作

## 文件说明

- `eq_reply_train_1500plus.jsonl`：训练集
- `eq_reply_eval.jsonl`：验证集
- `eq_reply_full_1500plus.jsonl`：全量数据
- `eq_reply_dataset_preview.csv`：Excel 预览
- `dataset_info_snippet.json`：LLaMA Factory 注册片段

## LLaMA Factory 注册方式

把 `eq_reply_train_1500plus.jsonl` 放到 LLaMA Factory 的 `data/` 目录，然后在 `data/dataset_info.json` 加入：

```json
{
  "eq_reply_train_v3": {
    "file_name": "eq_reply_train_1500plus.jsonl",
    "formatting": "alpaca",
    "columns": {
      "prompt": "instruction",
      "query": "input",
      "response": "output"
    }
  }
}
```

## 推荐训练配置

快速验证：

- model：Qwen2.5-1.5B-Instruct / Qwen2.5-3B-Instruct
- template：qwen
- stage：sft
- finetuning_type：lora
- cutoff_len：512
- learning_rate：2e-4
- num_train_epochs：2~3
- lora_rank：8 或 16
- lora_alpha：16 或 32

显存充足：

- model：Qwen2.5-7B-Instruct
- method：LoRA 或 QLoRA
- epoch：2~3

## 数据清洗建议

这版数据已经可以直接训练，但正式写简历项目时，建议：

1. 用 `eq_reply_dataset_preview.csv` 人工抽查；
2. 删除过于模板化、不符合你想要风格的回复；
3. 保留“感情、工作、家庭、社交、反击、安慰”之间的均衡比例；
4. 单独留出 `eq_reply_eval.jsonl` 做效果对比。
