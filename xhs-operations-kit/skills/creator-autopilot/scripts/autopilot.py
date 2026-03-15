#!/usr/bin/env python3
"""串联 xianyu -> content -> calendar，并生成发布命令清单。"""

from __future__ import annotations

import argparse
import json
import subprocess
from datetime import datetime
from pathlib import Path


def run(cmd: list[str]) -> None:
    print("▶", " ".join(cmd))
    subprocess.run(cmd, check=True)


def latest_file(folder: Path, pattern: str) -> Path:
    files = sorted(folder.glob(pattern), key=lambda p: p.stat().st_mtime)
    if not files:
        raise FileNotFoundError(f"No file matched: {pattern} in {folder}")
    return files[-1]


def main() -> None:
    p = argparse.ArgumentParser(description="自媒体运营总控脚本")
    p.add_argument("--workspace", default="~/.openclaw/workspace", help="闲鱼数据目录")
    p.add_argument("--assets", default="~/.openclaw/workspace/content_assets", help="内容资产目录")
    p.add_argument("--days", type=int, default=7, help="排期天数")
    args = p.parse_args()

    workspace = Path(args.workspace).expanduser().resolve()
    assets = Path(args.assets).expanduser().resolve()
    assets.mkdir(parents=True, exist_ok=True)

    journal_script = Path("~/.openclaw/skills/xianyu-journal/scripts/journal_builder.py").expanduser()
    repurpose_script = Path("~/.openclaw/skills/content-repurposer/scripts/content_repurposer.py").expanduser()
    calendar_script = Path("~/.openclaw/skills/content-calendar/scripts/content_calendar.py").expanduser()

    run([
        "python3", str(journal_script),
        "--ready-csv", str(workspace / "ready_for_goofish.csv"),
        "--raw-csv", str(workspace / "raw_resources.csv"),
        "--out-dir", str(assets),
    ])

    journal = latest_file(assets, "journal_*.json")

    run([
        "python3", str(repurpose_script),
        "--journal", str(journal),
        "--out-dir", str(assets),
    ])

    content_pack = latest_file(assets, "content_pack_*.json")

    run([
        "python3", str(calendar_script),
        "--content-pack", str(content_pack),
        "--days", str(args.days),
        "--out-dir", str(assets),
    ])

    pack = json.loads(content_pack.read_text(encoding="utf-8"))
    stamp = datetime.now().strftime("%Y%m%d")
    plan = assets / f"publish_plan_{stamp}.md"

    x = pack["xiaohongshu"]
    d = pack["douyin"]
    b = pack["bilibili"]

    lines = [
        f"# 发布命令清单 {stamp}",
        "",
        "## 小红书（图文）",
        "```bash",
        "python3 ~/.openclaw/skills/xiaohongshu-publish/scripts/xhs_publisher.py publish \\",
        f"  --title \"{x['title']}\" \\",
        f"  --desc \"{x['desc'].replace(chr(10), ' ')}\" \\",
        "  --images image1.jpg,image2.jpg \\",
        f"  --topics \"{','.join(x['topics'])}\"",
        "```",
        "",
        "## 抖音（视频）",
        "```bash",
        "python3 ~/.openclaw/skills/douyin-publish/scripts/douyin_publisher.py upload \\",
        "  --video video.mp4 \\",
        f"  --title \"{d['caption']}\" \\",
        f"  --topics \"{','.join(d['topics'])}\"",
        "```",
        "",
        "## B站（视频）",
        "```bash",
        "python3 ~/.openclaw/skills/bilibili-upload/scripts/bili_uploader.py upload \\",
        "  --video video.mp4 \\",
        f"  --title \"{b['title']}\" \\",
        f"  --desc \"{b['desc'].replace(chr(10), ' ')}\" \\",
        f"  --tags \"{','.join(b['tags'])}\"",
        "```",
    ]

    plan.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"✅ publish plan: {plan}")


if __name__ == "__main__":
    main()
