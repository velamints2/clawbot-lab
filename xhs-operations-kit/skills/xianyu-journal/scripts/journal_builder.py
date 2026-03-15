#!/usr/bin/env python3
"""将闲鱼经营数据转成结构化内容日志。"""

from __future__ import annotations

import argparse
import csv
import json
import os
from collections import Counter
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any


@dataclass
class JournalItem:
    title: str
    price: float
    tag: str
    source: str


def _safe_float(v: Any, default: float = 0.0) -> float:
    try:
        return float(str(v).replace("¥", "").strip())
    except Exception:
        return default


def read_csv(path: Path) -> List[Dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def build_journal(raw_rows: List[Dict[str, str]], ready_rows: List[Dict[str, str]], date_str: str) -> Dict[str, Any]:
    items: List[JournalItem] = []

    for row in ready_rows:
        title = row.get("标题") or row.get("title") or "未命名商品"
        price = _safe_float(row.get("价格") or row.get("price"), 0.0)
        tag = row.get("标签") or row.get("tag") or "未分类"
        source = row.get("网盘链接") or row.get("source") or ""
        items.append(JournalItem(title=title, price=price, tag=tag, source=source))

    tag_counter = Counter(i.tag for i in items if i.tag)
    top_tags = [{"tag": k, "count": v} for k, v in tag_counter.most_common(5)]

    avg_price = round(sum(i.price for i in items) / max(len(items), 1), 2)
    total_value = round(sum(i.price for i in items), 2)

    story_angles = [
        "从0到1：今天如何从选品到上架完成闭环",
        "数据复盘：哪些类目更容易转化",
        "自动化提效：脚本帮我省掉了哪些重复动作",
    ]

    top_items = sorted(items, key=lambda x: x.price, reverse=True)[:8]

    return {
        "date": date_str,
        "summary": {
            "raw_resources": len(raw_rows),
            "ready_products": len(ready_rows),
            "total_value": total_value,
            "avg_price": avg_price,
        },
        "top_tags": top_tags,
        "top_items": [asdict(x) for x in top_items],
        "story_angles": story_angles,
        "next_actions": [
            "明天新增一个细分类关键词并AB测试标题",
            "优先补充高点击类目的封面素材",
            "复用今日爆款结构生成3条短视频脚本",
        ],
    }


def render_markdown(data: Dict[str, Any]) -> str:
    s = data["summary"]
    lines = [
        f"# 闲鱼经营日报 {data['date']}",
        "",
        "## 今日概览",
        f"- 采集资源：{s['raw_resources']} 条",
        f"- 可上架商品：{s['ready_products']} 条",
        f"- 预估总货值：¥{s['total_value']}",
        f"- 平均定价：¥{s['avg_price']}",
        "",
        "## 热门标签",
    ]
    for t in data.get("top_tags", []):
        lines.append(f"- {t['tag']} × {t['count']}")

    lines += ["", "## 高价值商品"]
    for i, item in enumerate(data.get("top_items", []), 1):
        lines.append(f"{i}. {item['title']}（¥{item['price']}）[{item['tag']}]")

    lines += ["", "## 可讲故事角度"]
    for x in data.get("story_angles", []):
        lines.append(f"- {x}")

    lines += ["", "## 明日动作"]
    for x in data.get("next_actions", []):
        lines.append(f"- {x}")

    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="生成闲鱼经营日报（JSON+Markdown）")
    parser.add_argument("--ready-csv", default="ready_for_goofish.csv", help="已生成商品CSV")
    parser.add_argument("--raw-csv", default="raw_resources.csv", help="采集资源CSV")
    parser.add_argument("--date", default=datetime.now().strftime("%Y-%m-%d"), help="日报日期")
    parser.add_argument("--out-dir", default=".", help="输出目录")
    args = parser.parse_args()

    out_dir = Path(args.out_dir).expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    ready_rows = read_csv(Path(args.ready_csv).expanduser())
    raw_rows = read_csv(Path(args.raw_csv).expanduser())

    journal = build_journal(raw_rows, ready_rows, args.date)

    stamp = args.date.replace("-", "")
    json_path = out_dir / f"journal_{stamp}.json"
    md_path = out_dir / f"journal_{stamp}.md"

    json_path.write_text(json.dumps(journal, ensure_ascii=False, indent=2), encoding="utf-8")
    md_path.write_text(render_markdown(journal), encoding="utf-8")

    print(f"✅ journal json: {json_path}")
    print(f"✅ journal md:   {md_path}")


if __name__ == "__main__":
    main()
