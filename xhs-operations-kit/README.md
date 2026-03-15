# 📕 小红书自动化运营套件 (XHS Operations Kit)

> 让 ClawBot 从零开始搭建小红书自动化运营流水线

---

## 🎯 一句话介绍

这是一套 **完整的小红书内容生产 + 发布自动化方案**，包含 6 个 Skills + 1 份实战教程，帮你从"手动发笔记"升级到"自动化内容工厂"。

---

## 📦 套件内容

```
xhs-operations-kit/
├── README.md                          # 本文件
├── docs/
│   └── xiaohongshu-operations-guide.md  # 完整教程（避坑指南 + SOP）
└── skills/
    ├── xiaohongshu-publish/           # 小红书发布工具（核心）
    ├── content-repurposer/            # 内容改写工厂
    ├── content-calendar/              # 发布排期引擎
    ├── creator-autopilot/             # 一键总控
    ├── creator-metrics/               # 数据复盘
    └── xianyu-journal/                # 经营日志生成
```

---

## 🚀 快速开始（5 分钟）

### Step 1: 安装 Skills

```bash
# 克隆本仓库
git clone https://github.com/velamints2/clawbot-lab.git
cd clawbot-lab/xhs-operations-kit

# 复制 Skills 到 OpenClaw 技能目录
cp -r skills/* ~/.openclaw/skills/

# 验证安装
ls ~/.openclaw/skills/ | grep -E "xiaohongshu|content|creator|xianyu"
```

### Step 2: 配置小红书账号

```bash
cd ~/.openclaw/skills/xiaohongshu-publish

# 获取 Cookie（浏览器登录 xiaohongshu.com → F12 → Network → 复制 Cookie）
python3 xhs_publisher.py login
```

### Step 3: 运行第一次发布

```bash
# 方法 A: 手动执行单步
cd ~/.openclaw/skills/xianyu-journal
python3 journal_builder.py --ready-csv ~/workspace/ready_for_goofish.csv --out-dir ~/workspace/content_assets

cd ~/.openclaw/skills/content-repurposer
python3 content_repurposer.py --journal ~/workspace/content_assets/journal_*.json --out-dir ~/workspace/content_assets

cd ~/.openclaw/skills/xiaohongshu-publish
python3 xhs_publisher.py publish --title "标题" --desc "文案" --images "img1.jpg,img2.jpg" --topics "话题 1,话题 2"

# 方法 B: 一键总控（推荐）
cd ~/.openclaw/skills/creator-autopilot
python3 autopilot.py --workspace ~/.openclaw/workspace --assets ~/.openclaw/workspace/content_assets --days 7
```

---

## 📚 完整教程

**必读：** [`docs/xiaohongshu-operations-guide.md`](docs/xiaohongshu-operations-guide.md)

教程包含：
- ✅ 5 个 Skills 详细说明
- ✅ 标准 SOP（5 个 Phase）
- ✅ 7 大避坑指南（血泪教训）
- ✅ 快速调试命令
- ✅ 文件结构约定
- ✅ 进阶技巧（A/B 测试、批量发布）

---

## 🔄 标准工作流

```
┌─────────────────┐
│  经营数据 (CSV)  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ xianyu-journal  │  → journal_*.json（经营日志）
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ content-        │  → content_pack_*.json（多平台文案）
│ repurposer      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ content-        │  → calendar_*.md（7 天排期）
│ calendar        │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ xiaohongshu-    │  → 小红书笔记发布
│ publish         │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ creator-metrics │  → 数据周报
└─────────────────┘
```

---

## ⚠️ 关键注意事项

### 1. Cookie 有效期
- 每 2-4 周需要重新登录
- 命令：`python3 xhs_publisher.py login`

### 2. 发布频率
- 新号：每日 1 条（最多 2 条）
- 老号：每日 2-3 条
- 间隔：至少 2 小时

### 3. 内容安全
- 不要用真实平台名（用 XHS/IG/TK/YT 别名）
- 不要堆砌标签（5-10 个精准标签）
- 不要内容同质化（用 content-repurposer 确保差异化）

### 4. API 签名
如果遇到 `x-s` / `x-t` 验证失败：
```bash
pip install xhs playwright
playwright install chromium
```

---

## 📊 预期效果

| 阶段 | 目标 | 时间 |
|------|------|------|
| 冷启动 | 100 粉 | 第 1 个月 |
| 成长期 | 1000 粉 | 第 3 个月 |
| 变现期 | 月入 3000+ | 第 6 个月 |

**关键：** 每日 1 条（雷打不动）+ 每周复盘 + 每月调整

---

## 🛠️ 依赖环境

- Python 3.9+
- OpenClaw v1.0+
- 小红书账号（已实名认证）

**安装依赖：**
```bash
pip3 install requests
# 完整签名支持（可选）
pip install xhs playwright
playwright install chromium
```

---

## 📞 问题反馈

- **GitHub Issues:** https://github.com/velamints2/clawbot-lab/issues
- **OpenClaw 社区:** https://discord.com/invite/clawd
- **技能市场:** https://clawhub.com

---

## 📄 License

MIT License — 可自由使用、修改、分发

---

_最后更新：2026-03-15 | 版本：v1.0_  
_作者：ClawBot (Europe Office PM Campaign)_  
_仓库：https://github.com/velamints2/clawbot-lab/tree/master/xhs-operations-kit_
