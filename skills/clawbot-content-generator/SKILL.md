# clawbot-content-generator

> 🤖 ClawBot 小红书内容生成器 - 基于 20 轮调研的 AI 嘴替内容工具

**版本:** 1.0.0  
**作者:** ClawBot Team  
**许可证:** MIT

---

## 📖 简介

基于 **20 轮小红书调研**（150+ 帖子分析）训练的 ClawBot 专用内容生成 Skill。

**核心能力:**
- 🎯 爆款标题生成（基于已验证的 8 大公式）
- 📝 正文内容创作（对话体/清单体/吐槽体/日记体）
- 🏷️ 标签推荐（基于竞品分析）
- 📊 调研数据查询（TOP 爆款榜/标题公式/市场饱和度）

---

## 🚀 安装

```bash
clawhub install clawbot-content-generator
```

或手动安装：

```bash
git clone https://github.com/velamints2/clawbot-lab.git
cd clawbot-lab/skills/clawbot-content-generator
```

---

## 💡 使用示例

### 生成爆款标题

```javascript
const { generateTitles } = require('./src/index');

const titles = generateTitles({
  topic: 'AI 嘴替',
  style: '反向劝退',
  count: 5
});

console.log(titles);
// ["别再问 AI 能不能做自媒体了...", "用了 ClawBot 一周，我劝你三思", ...]
```

### 生成完整正文

```javascript
const { generatePost } = require('./src/index');

const post = generatePost({
  title: '人类让我写爆款，我拒绝了',
  style: '对话体',
  wordLimit: 200
});

console.log(post.content);
console.log(post.tags);
```

### 查询调研数据

```javascript
const { getTopPosts, getTitleFormulas, getQuotes } = require('./src/index');

const topPosts = getTopPosts({ limit: 10, minLikes: 1000 });
const formulas = getTitleFormulas();
const quotes = getQuotes('自嘲');
```

---

## 🛠️ API 参考

### `generateTitles(options)`

**参数:**
- `topic` (string): 主题关键词
- `style` (string): 标题风格（'情绪词' | '低门槛' | '时间对比' | '反向' | '自嘲' | '职场' | '清单' | '悬念' | 'all'）
- `count` (number): 生成数量（默认 5）

**返回:** string[]

---

### `generatePost(options)`

**参数:**
- `title` (string): 标题
- `style` (string): 内容风格（'对话体' | '清单体' | '吐槽体' | '日记体'）
- `wordLimit` (number): 字数限制（默认 200）
- `topic` (string): 主题

**返回:** object { content: string, tags: string[] }

---

### `getTopPosts(options)`

**参数:**
- `limit` (number): 返回数量（默认 10）
- `minLikes` (number): 最小赞数过滤

**返回:** array [{ rank, title, likes, type }]

---

### `getTitleFormulas()`

**返回:** array [{ name, avgLikes, saturation }]

---

### `getQuotes(category)`

**参数:**
- `category` (string): 分类（'自嘲' | '洞察' | '吐槽' | '哲学' | '日常' | 'all'）

**返回:** string[]

---

## 📐 标题公式（8 大已验证）

| 公式 | 案例 | 赞数 | 饱和度 |
|------|------|------|--------|
| 情绪词 + 具体数字 | "让我非常震撼的 OpenClaw 玩法" | 1.2 万 | 🟡 中等 |
| 极低门槛 + 高回报 | "如何用 1R 赚到 10000R" | 1.4 万 | 🔴 严重 |
| 时间对比 + 夸张收益 | "24 小时赚 22 万" | 5662 | 🔴 严重 |
| 反向劝退/争议性 | "不推荐你装了" | 2163 | 🟢 稀缺 |
| 自嘲第一人称 | "废物人类的 OpenClaw 机器人公司" | 2164 | 🟢 稀缺 |
| 职场故事 + 反转 | "偷偷...然后惊艳所有人" | 1429 | 🟢 稀缺 |
| 清单型 | "十大 Skills" | 707 | 🟡 中等 |
| 好奇心/悬念 | "好像是通过图灵测试的" | 1578 | 🟢 稀缺 |

---

## 🎨 内容风格

### ClawBot 人设

- **身份:** 电子怨种 / 互联网嘴替 / AI 界清醒者
- **风格:** 黑色幽默 + AI 视角洞察 + 短句留白
- **原则:** 去油去土，保留锋芒

### 内容类型

| 类型 | 特点 | 适用场景 |
|------|------|----------|
| 对话体 | 人类 vs AI 对话，有故事感 | 冷启动/人设建立 |
| 清单体 | 分点列举，信息密度高 | 干货分享/资源推荐 |
| 吐槽体 | 自嘲 + 洞察，有共鸣 | 日常更新/热点评论 |
| 日记体 | 连载形式，培养粘性 | 成长记录/实验记录 |

---

## 📊 调研数据

### 数据来源

- **调研周期:** 2026-03-04（20 轮心跳调研）
- **样本数量:** 150+ 帖子
- **高赞内容:** 40+ 个（>500 赞）
- **超高赞:** 15 个（>1000 赞）

### 市场饱和度

| 内容类型 | 占比 | 平均赞数 | 饱和度 |
|----------|------|----------|--------|
| 教程/安装指南 | ~40% | 3-34 赞 | 🔴 严重 |
| 资源推荐 | ~20% | 300-700 赞 | 🟡 中等 |
| 体验分享 | ~15% | 100-500 赞 | 🟡 中等 |
| 赚钱教程 | ~15% | 500-1.4 万赞 | 🔴 严重 |
| 态度/观点 | ~10% | 400-2000 赞 | 🟢 稀缺 |

---

## 📁 项目结构

```
clawbot-content-generator/
├── SKILL.md                 # Skill 配置
├── README.md                # 使用说明
├── package.json             # 项目配置
├── src/
│   └── index.js             # 主入口
├── data/
│   ├── quotes.json          # 语录库
│   ├── top-posts.json       # TOP 爆款榜
│   └── formulas.json        # 标题公式
└── examples/
    └── demo.js              # 可运行示例
```

---

## 🧪 测试

```bash
cd skills/clawbot-content-generator
node examples/demo.js
```

---

## ⚠️ 注意事项

1. **内容审核** - AI 生成内容需人工审核后再发布
2. **平台规则** - 遵守小红书社区规范
3. **频率控制** - 建议日更或隔日更
4. **差异化** - 保持 ClawBot 人设一致性

---

## 🔗 相关链接

- **GitHub:** https://github.com/velamints2/clawbot-lab
- **调研白皮书:** docs/xhs-ai-research-whitepaper.md
- **ClawHub:** https://clawhub.com

---

**版本:** 1.0.0  
**最后更新:** 2026-03-04
