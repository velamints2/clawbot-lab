---
name: content-repurposer
description: 把经营日志转成多平台内容包。输入 xianyu-journal 的 journal.json，输出小红书/抖音/B站文案与脚本草稿。
---

# 多平台内容改写工厂

## 何时使用
- 你已经有 `journal_*.json`
- 你要自动得到平台差异化表达，而不是同一条文案硬拷贝

## 快速开始

```bash
python3 content_repurposer.py \
  --journal ~/.openclaw/workspace/content_assets/journal_20260228.json \
  --out-dir ~/.openclaw/workspace/content_assets
```

## 输出
- `content_pack_YYYYMMDD.json`
- `content_pack_YYYYMMDD.md`

## 平台策略
- 小红书：经验 + 细节 + 反思
- 抖音：钩子 + 冲突 + 反转 + CTA
- B站：过程复盘 + 方法论 + 数据图表位

## 参考项目
- ReaJason/xhs：话题与笔记结构
- Superheroff/douyin_uplod：标题、话题、@人、发布流程元素
- biliup/biliup：投稿字段结构（标题、简介、分区、标签）
