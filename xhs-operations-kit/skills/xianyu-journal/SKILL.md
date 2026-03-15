---
name: xianyu-journal
description: 闲鱼经营过程记录器。把 raw_resources.csv/ready_for_goofish.csv 生成每日经营日志与可发布素材，供小红书、抖音、B站二次创作使用。
---

# 闲鱼经营日志生成

## 何时使用
- 你想把“今天做了什么、卖了什么、赚了多少”整理成可讲故事的数据
- 你要给后续文案/视频脚本提供结构化输入

## 快速开始

```bash
python3 journal_builder.py \
  --ready-csv ~/.openclaw/workspace/ready_for_goofish.csv \
  --raw-csv ~/.openclaw/workspace/raw_resources.csv \
  --out-dir ~/.openclaw/workspace/content_assets
```

## 输出
- `journal_YYYYMMDD.json`：结构化经营数据
- `journal_YYYYMMDD.md`：可读日报

## 决策树

```text
需求
├─ 只要日报 → 运行 journal_builder.py
├─ 想做平台改写 → 先产出 journal_*.json，再交给 content-repurposer
└─ 想做排期 → 用 content-calendar 读取 content_pack.json
```

## 参考实现
- Data-first pipeline 参考 MoneyPrinterTurbo 的任务分阶段设计
- 多平台发布衔接参考现有 skills: xiaohongshu-publish / douyin-publish / bilibili-upload
