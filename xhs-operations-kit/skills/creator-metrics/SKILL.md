---
name: creator-metrics
description: 自媒体数据复盘原子技能。记录每条内容的曝光/互动/转化，生成周报并反哺选题策略。
---

# 自媒体数据复盘

## 作用
将各平台发布后的数据沉淀到统一台账，输出每周复盘和下周优化建议。

## 快速开始

```bash
# 记录一条数据
python3 metrics_tracker.py log \
  --platform xiaohongshu \
  --content-id abc123 \
  --title "第60天副业复盘" \
  --views 1200 --likes 86 --comments 19 --follows 12 --leads 4

# 生成周报
python3 metrics_tracker.py weekly --out-dir ~/.openclaw/workspace/content_assets
```
