---
name: creator-autopilot
description: 一键串联“经营日志→多平台改写→排期→发布命令清单”的总控技能。基于现有 xianyu-journal/content-repurposer/content-calendar 与发布 skills。
---

# 自媒体总控（原子编排）

## 功能
在不耦合各子技能代码的前提下，串联执行：
1) xianyu-journal
2) content-repurposer
3) content-calendar
4) 生成发布命令草案（调用 xiaohongshu-publish / douyin-publish / bilibili-upload）

## 快速开始

```bash
python3 autopilot.py \
  --workspace ~/.openclaw/workspace \
  --assets ~/.openclaw/workspace/content_assets \
  --days 7
```

## 输出
- `publish_plan_YYYYMMDD.md`
- 控制台输出每一步产物路径

## 原子化原则
- 不直接改写平台发布脚本
- 仅通过文件契约（journal/content_pack/calendar）进行协作
- 每个阶段可独立重跑
