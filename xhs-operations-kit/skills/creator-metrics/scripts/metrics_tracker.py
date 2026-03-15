#!/usr/bin/env python3
"""自媒体数据台账与周报。"""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path

COLUMNS = [
    "date", "platform", "content_id", "title", "views", "likes", "comments", "follows", "leads"
]


def ensure_file(path: Path) -> None:
    if path.exists():
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS)
        w.writeheader()


def log_row(path: Path, row: dict) -> None:
    ensure_file(path)
    with path.open("a", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS)
        w.writerow(row)


def parse_int(x: str) -> int:
    try:
        return int(float(x))
    except Exception:
        return 0


def weekly_report(path: Path) -> dict:
    ensure_file(path)
    cutoff = (datetime.now() - timedelta(days=7)).date()
    stats = defaultdict(lambda: {"views": 0, "likes": 0, "comments": 0, "follows": 0, "leads": 0, "count": 0})

    with path.open("r", encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            try:
                d = datetime.strptime(row.get("date", ""), "%Y-%m-%d").date()
            except Exception:
                continue
            if d < cutoff:
                continue
            p = row.get("platform", "unknown")
            s = stats[p]
            s["views"] += parse_int(row.get("views", "0"))
            s["likes"] += parse_int(row.get("likes", "0"))
            s["comments"] += parse_int(row.get("comments", "0"))
            s["follows"] += parse_int(row.get("follows", "0"))
            s["leads"] += parse_int(row.get("leads", "0"))
            s["count"] += 1

    for p, s in stats.items():
        views = max(s["views"], 1)
        s["like_rate"] = round(s["likes"] / views, 4)
        s["comment_rate"] = round(s["comments"] / views, 4)
        s["follow_rate"] = round(s["follows"] / views, 4)
        s["lead_rate"] = round(s["leads"] / views, 4)

    return dict(stats)


def render_md(data: dict) -> str:
    lines = ["# 自媒体周复盘", ""]
    if not data:
        return "# 自媒体周复盘\n\n本周暂无数据。\n"

    for p, s in data.items():
        lines += [
            f"## {p}",
            f"- 发布数：{s['count']}",
            f"- 曝光：{s['views']}",
            f"- 点赞率：{s['like_rate']*100:.2f}%",
            f"- 评论率：{s['comment_rate']*100:.2f}%",
            f"- 关注率：{s['follow_rate']*100:.2f}%",
            f"- 线索率：{s['lead_rate']*100:.2f}%",
            "",
        ]

    lines += [
        "## 下周建议",
        "- 保留最高关注率平台的叙事模板",
        "- 将低线索率内容改为强CTA版本做AB测试",
        "- 每个平台固定1条‘过程复盘’内容用于建立信任",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    p = argparse.ArgumentParser(description="自媒体数据记录与周复盘")
    sub = p.add_subparsers(dest="cmd")

    logp = sub.add_parser("log", help="记录单条内容数据")
    logp.add_argument("--csv", default="~/.openclaw/workspace/content_assets/metrics.csv")
    logp.add_argument("--date", default=datetime.now().strftime("%Y-%m-%d"))
    logp.add_argument("--platform", required=True)
    logp.add_argument("--content-id", required=True)
    logp.add_argument("--title", required=True)
    logp.add_argument("--views", default="0")
    logp.add_argument("--likes", default="0")
    logp.add_argument("--comments", default="0")
    logp.add_argument("--follows", default="0")
    logp.add_argument("--leads", default="0")

    weekp = sub.add_parser("weekly", help="生成近7天周报")
    weekp.add_argument("--csv", default="~/.openclaw/workspace/content_assets/metrics.csv")
    weekp.add_argument("--out-dir", default="~/.openclaw/workspace/content_assets")

    args = p.parse_args()
    if not args.cmd:
        p.print_help()
        return

    csv_path = Path(args.csv).expanduser().resolve()

    if args.cmd == "log":
        row = {
            "date": args.date,
            "platform": args.platform,
            "content_id": args.content_id,
            "title": args.title,
            "views": parse_int(args.views),
            "likes": parse_int(args.likes),
            "comments": parse_int(args.comments),
            "follows": parse_int(args.follows),
            "leads": parse_int(args.leads),
        }
        log_row(csv_path, row)
        print(f"✅ logged to: {csv_path}")

    elif args.cmd == "weekly":
        out_dir = Path(args.out_dir).expanduser().resolve()
        out_dir.mkdir(parents=True, exist_ok=True)
        data = weekly_report(csv_path)
        stamp = datetime.now().strftime("%Y%m%d")
        md = out_dir / f"metrics_weekly_{stamp}.md"
        md.write_text(render_md(data), encoding="utf-8")
        print(f"✅ weekly report: {md}")


if __name__ == "__main__":
    main()
