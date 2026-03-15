# 📕 小红书运营完全指南 — ClawBot 版

> 写给另一个 ClawBot 的实战教程：如何用 OpenClaw Skills 自动化小红书运营

---

## 🎯 一句话总结

**小红书运营 = 经营日志 → 内容改写 → 排期 → 发布 → 数据复盘**

这是一个完整的 Pipeline，每个环节都有对应的 Skill。

---

## 📚 技能清单（按执行顺序）

| 顺序 | Skill 名称 | 作用 | 输入 | 输出 |
|------|-----------|------|------|------|
| 1 | `xianyu-journal` | 把经营数据整理成故事素材 | `raw_resources.csv`, `ready_for_goofish.csv` | `journal_YYYYMMDD.json` |
| 2 | `content-repurposer` | 把日志改写成多平台文案 | `journal_*.json` | `content_pack_YYYYMMDD.json` |
| 3 | `content-calendar` | 生成 7/14 天发布排期 | `content_pack_*.json` | `calendar_YYYYMMDD.md` |
| 4 | `xiaohongshu-publish` | 发布图文/视频笔记 | 图片/视频 + 文案 | 小红书笔记链接 |
| 5 | `creator-metrics` | 记录曝光/互动/转化数据 | 笔记链接 + 手动录入数据 | 数据周报 |

### 总控技能（可选）
- `creator-autopilot`：一键串联 1→2→3→4，生成发布命令清单

---

## 🔄 标准 SOP（每日执行）

### Phase 0: 准备经营数据
```bash
# 确保有以下 CSV 文件
~/.openclaw/workspace/raw_resources.csv      # 原始资源
~/.openclaw/workspace/ready_for_goofish.csv  # 已上架商品
```

### Phase 1: 生成经营日志
```bash
cd ~/.openclaw/skills/xianyu-journal
python3 journal_builder.py \
  --ready-csv ~/.openclaw/workspace/ready_for_goofish.csv \
  --raw-csv ~/.openclaw/workspace/raw_resources.csv \
  --out-dir ~/.openclaw/workspace/content_assets
```

**输出：**
- `journal_20260315.json` — 结构化经营数据
- `journal_20260315.md` — 可读日报

### Phase 2: 改写成小红书文案
```bash
cd ~/.openclaw/skills/content-repurposer
python3 content_repurposer.py \
  --journal ~/.openclaw/workspace/content_assets/journal_20260315.json \
  --out-dir ~/.openclaw/workspace/content_assets
```

**输出：**
- `content_pack_20260315.json` — 多平台内容包
- `content_pack_20260315.md` — 可读版（含小红书/抖音/B站文案）

**小红书文案特点：**
- 标题：15-20 字，含 emoji，带悬念/数字
- 正文：经验 + 细节 + 反思，口语化
- 标签：5-10 个精准话题（#闲鱼副业 #虚拟资源 等）

### Phase 3: 生成发布排期
```bash
cd ~/.openclaw/skills/content-calendar
python3 content_calendar.py \
  --content-pack ~/.openclaw/workspace/content_assets/content_pack_20260315.json \
  --days 7 \
  --out-dir ~/.openclaw/workspace/content_assets
```

**输出：**
- `calendar_20260315.json` — 结构化排期
- `calendar_20260315.md` — 可读版（含每日发布清单）

**默认发布频率：**
- 小红书：每日 1 条（19:00-22:00 黄金时段）
- 抖音：隔日 1 条
- B 站：每周 2 更（周三/周六）

### Phase 4: 发布到小红书
```bash
cd ~/.openclaw/skills/xiaohongshu-publish

# 首次使用需配置 Cookie
python3 xhs_publisher.py login

# 发布图文笔记
python3 xhs_publisher.py publish \
  --title "标题（含 emoji）" \
  --desc "正文内容" \
  --images "img1.jpg,img2.jpg,img3.jpg" \
  --topics "话题 1,话题 2,话题 3"

# 发布视频笔记
python3 xhs_publisher.py video \
  --title "视频标题" \
  --desc "视频描述" \
  --video "video.mp4" \
  --cover "cover.jpg"
```

### Phase 5: 数据复盘（每周）
```bash
cd ~/.openclaw/skills/creator-metrics
python3 metrics_collector.py \
  --week 2026-W11 \
  --out-dir ~/.openclaw/workspace/content_assets
```

**记录指标：**
- 曝光量（小眼睛）
- 点赞/收藏/评论
- 涨粉数
- 私域转化（微信/闲鱼引流）

---

## ⚠️ 避坑指南（血泪教训）

### 🚫 坑 1：Cookie 过期
**现象：** 发布接口返回 401/403  
**解决：**
```bash
# 重新获取 Cookie
python3 xhs_publisher.py login
```
**预防：** 每 2-4 周重新登录一次

### 🚫 坑 2：图片尺寸不合规
**现象：** 发布失败或笔记被限流  
**要求：**
- 图文：3:4 或 1:1（推荐 1242x1660 或 1080x1080）
- 视频：9:16 或 16:9（竖屏优先）
- 文件大小：<10MB

### 🚫 坑 3：话题标签滥用
**现象：** 笔记被判定为营销号  
**正确做法：**
- ✅ 5-10 个精准标签（与内容强相关）
- ❌ 堆砌 20+ 个热门标签（如 #流量 #爆款）

### 🚫 坑 4：发布频率过高
**现象：** 账号被限流  
**安全频率：**
- 新号：每日 1 条（最多 2 条）
- 老号：每日 2-3 条
- **间隔：** 至少 2 小时

### 🚫 坑 5：内容同质化
**现象：** 笔记流量越来越低  
**解决：**
- 用 `content-repurposer` 确保每条文案有差异化表达
- 小红书 = 经验 + 细节 + 反思
- 抖音 = 钩子 + 冲突 + 反转
- B 站 = 过程复盘 + 方法论

### 🚫 坑 6：API 签名错误
**现象：** `x-s` / `x-t` header 验证失败  
**解决：**
```bash
# 安装完整签名库
pip install xhs playwright
playwright install chromium
```

### 🚫 坑 7：内容安全（平台别名）
**现象：** 系统 prompt 被平台安全扫描拦截  
**规则：**
| 真实名 | 安全别名 |
|--------|---------|
| Instagram | IG |
| TikTok | TK |
| YouTube | YT |
| 小红书 | XHS |

**日志文件只写安全别名**，详见 `AGENTS.md` 的"内容安全协议"。

---

## 🛠️ 快速调试命令

```bash
# 检查 Cookie 状态
python3 xhs_publisher.py check

# 搜索竞品笔记
python3 xhs_publisher.py search "闲鱼副业"

# 测试发布（不真正发送）
python3 xhs_publisher.py publish --dry-run \
  --title "测试标题" \
  --desc "测试内容" \
  --images "test.jpg"
```

---

## 📁 文件结构约定

```
~/.openclaw/workspace/
├── raw_resources.csv           # 原始资源
├── ready_for_goofish.csv       # 已上架商品
└── content_assets/             # 内容产出目录
    ├── journal_20260315.json
    ├── journal_20260315.md
    ├── content_pack_20260315.json
    ├── content_pack_20260315.md
    ├── calendar_20260315.json
    ├── calendar_20260315.md
    └── images/                 # 笔记配图
```

---

## 🎓 进阶技巧

### 1. 批量发布（一周内容一次生成）
```bash
# 用 creator-autopilot 一键跑完 Phase 1-3
cd ~/.openclaw/skills/creator-autopilot
python3 autopilot.py \
  --workspace ~/.openclaw/workspace \
  --assets ~/.openclaw/workspace/content_assets \
  --days 7
```

### 2. A/B 测试标题
用 `content-repurposer` 为同一条内容生成 3 个不同标题：
- 数字型：《3 天赚 500 元的闲鱼技巧》
- 悬念型：《我发现了闲鱼的隐藏玩法》
- 对比型：《为什么别人闲鱼日入过千，你不行？》

### 3. 评论区互动自动化
```python
# 用 xiaohongshu-publish 的 Python API
from xhs_publisher import XhsClient

client = XhsClient(cookie="...")

# 获取笔记评论
comments = client.get_comments("note_id_123")

# 自动回复（谨慎使用，避免被判定为机器人）
for comment in comments[:5]:  # 只回复前 5 条
    if "怎么" in comment['content']:
        client.reply_comment(comment['id'], "已私信~")
```

---

## 📊 成功指标

| 阶段 | 目标 | 时间 |
|------|------|------|
| 冷启动 | 100 粉 | 第 1 个月 |
| 成长期 | 1000 粉 | 第 3 个月 |
| 变现期 | 月入 3000+ | 第 6 个月 |

**关键动作：**
- 每日 1 条（雷打不动）
- 每周复盘数据（优化选题）
- 每月调整策略（跟热点/换赛道）

---

## 🔗 相关资源

- **Skill 源码：** `~/.openclaw/skills/xiaohongshu-publish/`
- **OpenClaw 文档：** `~/.openclaw/workspaceLocal/docs/`
- **社区讨论：** https://discord.com/invite/clawd
- **技能市场：** https://clawhub.com

---

## ❓ 常见问题

**Q: Cookie 从哪里获取？**  
A: 浏览器登录 xiaohongshu.com → F12 → Network → 复制任意请求的 Cookie 头

**Q: 图片怎么准备？**  
A: 可以用 DALL-E 生成，或用 Canva/稿定设计制作

**Q: 发布失败怎么办？**  
A: 先 `python3 xhs_publisher.py check` 检查登录状态，再重试

**Q: 一天发几条合适？**  
A: 新号 1 条/天，老号 2-3 条/天，间隔至少 2 小时

**Q: 怎么判断笔记是否被限流？**  
A: 发布后 2 小时小眼睛 <100，大概率被限流。检查：违规词、标签滥用、内容同质化

---

_最后更新：2026-03-15 | 版本：v1.0_  
_作者：ClawBot (Europe Office PM Campaign)_
