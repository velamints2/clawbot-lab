# GitHub 参考（编排与自动化）

## 参考仓库
- harry0703/MoneyPrinterTurbo
  - 参考点：任务流水线编排、阶段状态、中间产物
- ReaJason/xhs / Superheroff/douyin_uplod / biliup/biliup
  - 参考点：平台发布字段契约

## 设计落地
- `autopilot.py` 只负责编排，不侵入各平台发布技能
- 每个阶段独立可重跑，失败可断点恢复
