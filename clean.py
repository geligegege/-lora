import json
import re
import random
from collections import defaultdict, Counter
from pathlib import Path

random.seed(42)

LORA_DIR = Path(__file__).resolve().parent

INPUT_FILE = LORA_DIR / "eq_reply_finetune_dataset_v3" / "eq_reply_full_v10_natural_query.jsonl"
TRAIN_OUT = LORA_DIR / "eq_reply_train_clean.jsonl"
EVAL_OUT = LORA_DIR / "eq_reply_eval_clean.jsonl"
REPORT_OUT = LORA_DIR / "clean_report.json"

MIN_OUTPUT_LEN = 8
MAX_OUTPUT_LEN = 120
MAX_VARIANTS_PER_INPUT = 3
EVAL_RATIO = 0.12

# 注意：只检查 output，不检查 input
BAD_OUTPUT_WORDS = [
    "你妈", "全家", "去死", "废物", "垃圾",
    "滚远点", "脑残", "畜生", "贱", "死一边"
]

GENERIC_OUTPUTS = {
    "好的", "好", "没事", "加油", "别难过",
    "我理解你的感受", "我们好好沟通"
}


def normalize_text(text: str) -> str:
    text = text.strip()
    text = re.sub(r"\s+", "", text)
    text = text.replace("，", ",").replace("。", ".")
    return text


def chinese_len(text: str) -> int:
    return len(re.sub(r"\s+", "", text))


def parse_category(input_text: str) -> str:
    match = re.search(r"类别：(.+)", input_text)
    return match.group(1).strip() if match else "未知"


def is_bad_output(output: str) -> bool:
    output_norm = normalize_text(output)

    if chinese_len(output_norm) < MIN_OUTPUT_LEN:
        return True

    if chinese_len(output_norm) > MAX_OUTPUT_LEN:
        return True

    if output_norm in GENERIC_OUTPUTS:
        return True

    for word in BAD_OUTPUT_WORDS:
        if word in output:
            return True

    return False


def load_jsonl(path):
    data = []
    bad_json = 0

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            try:
                item = json.loads(line)
                data.append(item)
            except Exception:
                bad_json += 1

    return data, bad_json


def save_jsonl(path, data):
    with open(path, "w", encoding="utf-8") as f:
        for item in data:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")


def main():
    raw_data, bad_json = load_jsonl(INPUT_FILE)

    cleaned = []
    seen_exact = set()
    remove_reasons = Counter()

    for item in raw_data:
        instruction = item.get("instruction", "").strip()
        input_text = item.get("input", "").strip()
        output = item.get("output", "").strip()

        if not instruction or not input_text or not output:
            remove_reasons["empty_field"] += 1
            continue

        exact_key = (
            normalize_text(instruction),
            normalize_text(input_text),
            normalize_text(output)
        )

        if exact_key in seen_exact:
            remove_reasons["exact_duplicate"] += 1
            continue

        seen_exact.add(exact_key)

        if is_bad_output(output):
            remove_reasons["bad_output"] += 1
            continue

        cleaned.append({
            "instruction": instruction,
            "input": input_text,
            "output": output
        })

    # 限制同一个 input 下的 output 数量
    grouped = defaultdict(list)
    for item in cleaned:
        grouped[normalize_text(item["input"])].append(item)

    limited = []
    for _, items in grouped.items():
        random.shuffle(items)
        limited.extend(items[:MAX_VARIANTS_PER_INPUT])

    # 按 input 分组切分，避免同一个 input 同时出现在 train 和 eval
    grouped_limited = defaultdict(list)
    for item in limited:
        grouped_limited[normalize_text(item["input"])].append(item)

    group_values = list(grouped_limited.values())
    random.shuffle(group_values)

    eval_size = int(len(group_values) * EVAL_RATIO)

    eval_groups = group_values[:eval_size]
    train_groups = group_values[eval_size:]

    train_data = [x for group in train_groups for x in group]
    eval_data = [x for group in eval_groups for x in group]

    random.shuffle(train_data)
    random.shuffle(eval_data)

    save_jsonl(TRAIN_OUT, train_data)
    save_jsonl(EVAL_OUT, eval_data)

    report = {
        "raw_count": len(raw_data),
        "bad_json": bad_json,
        "after_basic_clean": len(cleaned),
        "after_limit_variants": len(limited),
        "train_count": len(train_data),
        "eval_count": len(eval_data),
        "remove_reasons": dict(remove_reasons),
        "train_category_count": dict(Counter(parse_category(x["input"]) for x in train_data)),
        "eval_category_count": dict(Counter(parse_category(x["input"]) for x in eval_data)),
    }

    with open(REPORT_OUT, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print("清洗完成")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()