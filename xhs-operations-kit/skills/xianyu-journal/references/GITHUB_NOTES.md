# GitHub 参考（数据化记录）

## 参考仓库
- harry0703/MoneyPrinterTurbo
  - 参考点：任务分阶段（脚本→terms→音频→字幕→视频）
  - 借鉴：将经营流程拆解成可重跑阶段，产出中间文件供下游消费

## 设计落地
- `journal_builder.py` 输出 JSON/MD 双产物
- 下游技能只依赖 JSON 契约，不耦合内部实现
