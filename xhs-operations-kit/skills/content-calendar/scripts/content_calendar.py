#!/usr/bin/env python3
"""根据 content_pack 生成跨平台发布日历。"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, List


@dataclass
class CalendarItem:
    date: str
    platform: str
    slot: str
    title: str
    objective: str
    checklist: List[str]


def windows(platform: str) -> str:
    return {
        "xiaohongshu": "20:00-22:00",
        "douyin": "18:30-20:30",
        "bilibili": "19:00-21:00",
    }.get(platform, "20:00-21:00")


def build(pack: Dict[str, Any], days: int) -> Dict[str, Any]:
    start = datetime.now().date()
    cal: List[CalendarItem] = []

    x_title = pack["xiaohongshu"]["title"]
    d_title = pack["douyin"]["caption"][:28]
    b_title = pack["bilibili"]["title"]

    for i in range(days):
        d = start + timedelta(days=i)
        ds = d.strftime("%Y-%m-%d")

        # 小红书：每日
        cal.append(CalendarItem(
            date=ds,
            platform="xiaohongshu",
            slot=windows("xiaohongshu"),
            title=x_title,
            objective="沉淀经验、建立信任",
            checklist=["补3张过程图", "确认话题", "发布后1小时回复评论"],
        ))

        # 抖音：隔日
        if i % 2 == 0:
            cal.append(CalendarItem(
                date=ds,
                platform="douyin",
                slot=windows("douyin"),
                title=d_title,
                objective="拉新曝光",
                checklist=["确认封面前3秒钩子", "添加4个话题", "置顶评论引导"],
            ))

        # B站：每周2更（周二/周六）
        if d.weekday() in (1, 5):
            cal.append(CalendarItem(
                date=ds,
                platform="bilibili",
                slot=windows("bilibili"),
                title=b_title,
                objective="方法论沉淀",
                checklist=["补数据图表", "加时间戳", "简介放流程清单"],
            ))

    return {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "source": pack.get("source", ""),
        "days": days,
        "items": [asdict(x) for x in cal],
    }


def render_md(calendar: Dict[str, Any]) -> str:
    lines = [
        f"# 自媒体发布日历（{calendar['days']}天）",
        "",
        f"生成时间：{calendar['generated_at']}",
        "",
    ]
    grouped: Dict[str, List[Dict[str, Any]]] = {}
    for item in calendar["items"]:
        grouped.setdefault(item["date"], []).append(item)

    for day, items in grouped.items():
        lines += [f"## {day}"]
        for x in items:
            lines += [
                f"- [{x['platform']}] {x['slot']} · {x['title']}",
                f"  - 目标：{x['objective']}",
            ]
            for c in x["checklist"]:
                lines.append(f"  - [ ] {c}")
        lines.append("")

    return "\n".join(lines)


def main() -> None:
    p = argparse.ArgumentParser(description="生成跨平台内容发布日历")
    p.add_argument("--content-pack", required=True, help="content_pack json 路径")
    p.add_argument("--days", type=int, default=7, help="排期天数")
    p.add_argument("--out-dir", default=".", help="输出目录")
    args = p.parse_args()

    pack_path = Path(args.content_pack).expanduser().resolve()
    out_dir = Path(args.out_dir).expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    pack = json.loads(pack_path.read_text(encoding="utf-8"))
    cal = build(pack, max(args.days, 1))

    stamp = datetime.now().strftime("%Y%m%d")
    json_path = out_dir / f"calendar_{stamp}.json"
    md_path = out_dir / f"calendar_{stamp}.md"

    json_path.write_text(json.dumps(cal, ensure_ascii=False, indent=2), encoding="utf-8")
    md_path.write_text(render_md(cal), encoding="utf-8")

    print(f"✅ calendar json: {json_path}")
    print(f"✅ calendar md:   {md_path}")


if __name__ == "__main__":
    main()
