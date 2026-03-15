#!/usr/bin/env python3
"""把经营日志改写成平台内容包。"""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List


def pick(data: Dict[str, Any], key: str, default):
    return data.get(key, default)


def xhs_pack(j: Dict[str, Any]) -> Dict[str, Any]:
    top_items = pick(j, "top_items", [])[:3]
    top_text = "；".join([f"{x['title']}¥{x['price']}" for x in top_items]) or "今天继续优化选品池"
    title = f"第{datetime.now().timetuple().tm_yday}天：我把副业流程再自动化了一步"
    return {
        "title": title[:20],
        "desc": (
            f"今天复盘了闲鱼网盘副业流程。重点商品：{top_text}。\n"
            f"我把选品→文案→上架准备拆成了可复用脚本，效率明显提升。\n"
            f"如果你也在做数字产品副业，建议先把每日复盘标准化。"
        ),
        "topics": ["副业", "闲鱼", "自动化", "效率工具", "自媒体成长"],
    }


def douyin_pack(j: Dict[str, Any]) -> Dict[str, Any]:
    s = pick(j, "summary", {})
    hook = f"我用脚本跑副业第{datetime.now().day}天，今天又省下2小时。"
    return {
        "caption": f"{hook} #副业 #闲鱼 #自动化 #自媒体",
        "script_60s": [
            "0-5s：抛结果——今天上新数量、总货值",
            f"5-20s：展示流程面板——采集{s.get('raw_resources', 0)}条 → 产出{s.get('ready_products', 0)}条",
            "20-40s：展示一个实际商品从资源到文案的变化",
            "40-55s：讲今天踩坑+修复动作",
            "55-60s：CTA：评论区回复“流程”领取模板",
        ],
        "topics": ["副业", "效率", "自动化", "闲鱼"],
    }


def bili_pack(j: Dict[str, Any]) -> Dict[str, Any]:
    s = pick(j, "summary", {})
    return {
        "title": f"闲鱼网盘副业实录：第{datetime.now().day}天，我如何把流程自动化",
        "desc": (
            f"今日数据：采集{s.get('raw_resources', 0)}，上新{s.get('ready_products', 0)}，"
            f"预估货值¥{s.get('total_value', 0)}。\n"
            "本期分享：流程拆解、脚本结构、踩坑复盘、下一步优化。"
        ),
        "outline": [
            "为什么要做经营日志自动化",
            "今日关键数据与变化",
            "脚本流程拆解（采集/文案/发布）",
            "常见错误与容错",
            "后续迭代计划",
        ],
        "tags": ["闲鱼", "副业", "Python", "自动化", "AI工作流"],
    }


def markdown(pack: Dict[str, Any]) -> str:
    x = pack["xiaohongshu"]
    d = pack["douyin"]
    b = pack["bilibili"]
    lines = [
        f"# 多平台内容包 {pack['date']}",
        "",
        "## 小红书",
        f"- 标题：{x['title']}",
        f"- 话题：{' '.join('#'+t for t in x['topics'])}",
        "- 正文：",
        x["desc"],
        "",
        "## 抖音",
        f"- 文案：{d['caption']}",
        "- 60秒脚本：",
    ]
    lines += [f"  - {t}" for t in d["script_60s"]]
    lines += ["", "## B站", f"- 标题：{b['title']}", f"- 标签：{', '.join(b['tags'])}", "- 简介：", b["desc"], "- 提纲："]
    lines += [f"  - {x}" for x in b["outline"]]
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="把 journal.json 转为多平台内容包")
    parser.add_argument("--journal", required=True, help="journal json 路径")
    parser.add_argument("--out-dir", default=".", help="输出目录")
    args = parser.parse_args()

    journal_path = Path(args.journal).expanduser().resolve()
    out_dir = Path(args.out_dir).expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    journal = json.loads(journal_path.read_text(encoding="utf-8"))
    date = journal.get("date", datetime.now().strftime("%Y-%m-%d"))

    pack = {
        "date": date,
        "source": str(journal_path),
        "xiaohongshu": xhs_pack(journal),
        "douyin": douyin_pack(journal),
        "bilibili": bili_pack(journal),
    }

    stamp = date.replace("-", "")
    json_out = out_dir / f"content_pack_{stamp}.json"
    md_out = out_dir / f"content_pack_{stamp}.md"

    json_out.write_text(json.dumps(pack, ensure_ascii=False, indent=2), encoding="utf-8")
    md_out.write_text(markdown(pack), encoding="utf-8")

    print(f"✅ content pack json: {json_out}")
    print(f"✅ content pack md:   {md_out}")


if __name__ == "__main__":
    main()
