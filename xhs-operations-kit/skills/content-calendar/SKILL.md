---
name: content-calendar
description: 自媒体排期引擎。读取 content_pack.json，自动生成 7/14 天跨平台发布日历（小红书/抖音/B站）与执行清单。
---

# 内容排期引擎

## 作用
把 `content-repurposer` 产出的内容包拆到未来 N 天，形成可执行的发布计划，避免“有内容但不连续”。

## 快速开始

```bash
python3 content_calendar.py \
  --content-pack ~/.openclaw/workspace/content_assets/content_pack_20260301.json \
  --days 7 \
  --out-dir ~/.openclaw/workspace/content_assets
```

## 输出
- `calendar_YYYYMMDD.json`
- `calendar_YYYYMMDD.md`

## 规则
- 默认：小红书每日、抖音隔日、B站每周2更
- 自动给每条内容附带“素材待办”“发布时间窗口”“复盘点”

## 参考项目
- Social media scheduler 思路（任务队列+时间窗口）
- MoneyPrinterTurbo 的任务状态思想（阶段化执行）
