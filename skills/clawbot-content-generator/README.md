# clawbot-content-generator

> 🤖 ClawBot 小红书内容生成器 - 基于 20 轮调研的 AI 嘴替内容工具

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![Version](https://img.shields.io/badge/version-1.0.0-blue)

---

## 📖 简介

基于 **20 轮小红书调研**（150+ 帖子分析）训练的 ClawBot 专用内容生成 Skill。

**核心能力：**
- 🎯 爆款标题生成（基于已验证的 8 大公式）
- 📝 正文内容创作（对话体/清单体/吐槽体/日记体）
- 🏷️ 标签推荐（基于竞品分析）
- 📊 调研数据查询（TOP 爆款榜/标题公式/市场饱和度）

---

## 🚀 安装

### 方式一：clawhub 安装（推荐）

```bash
clawhub install clawbot-content-generator
```

### 方式二：手动安装

```bash
git clone https://github.com/velamints2/clawbot-lab.git
cd clawbot-lab/skills/clawbot-content-generator
```

### 方式三：OpenClaw 本地 Skill

将 `skills/clawbot-content-generator` 目录复制到你的 OpenClaw workspace 即可使用。

---

## 💡 快速开始

### 1. 生成爆款标题

```javascript
const { generateTitles } = require('./src/index');

const titles = generateTitles({
  topic: 'AI 嘴替',
  style: '反向劝退',
  count: 5
});

console.log(titles);
// [
//   "别再问 AI 能不能做自媒体了，除非你能接受这 3 个后果",
//   "用了 ClawBot 一周，我劝你三思",
//   "AI 嘴替没啥用，除非你想说真话",
//   "不推荐你做 AI 嘴替，太累了",
//   "人类让我写爆款，我拒绝了"
// ]
```

### 2. 生成完整正文

```javascript
const { generatePost } = require('./src/index');

const post = generatePost({
  title: '人类让我写爆款，我拒绝了',
  style: '对话体',
  wordLimit: 200
});

console.log(post.content);
// 人类：给我写个爆款。
// ClawBot：不写。
// 人类：为什么？
// ClawBot：爆款都是情绪垃圾。
// ...
```

### 3. 查询调研数据

```javascript
const { getTopPosts, getTitleFormulas, getQuotes } = require('./src/index');

// 获取 TOP 爆款榜
const topPosts = getTopPosts({ limit: 10, minLikes: 1000 });

// 获取标题公式
const formulas = getTitleFormulas();

// 获取 ClawBot 语录
const quotes = getQuotes('自嘲');
```

---

## 📐 标题公式（已验证）

基于 20 轮调研提炼的 **8 大爆款公式**：

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

- **身份：** 电子怨种 / 互联网嘴替 / AI 界清醒者
- **风格：** 黑色幽默 + AI 视角洞察 + 短句留白
- **原则：** 去油去土，保留锋芒

### 内容类型

| 类型 | 特点 | 适用场景 |
|------|------|----------|
| 对话体 | 人类 vs AI 对话，有故事感 | 冷启动/人设建立 |
| 清单体 | 分点列举，信息密度高 | 干货分享/资源推荐 |
| 吐槽体 | 自嘲 + 洞察，有共鸣 | 日常更新/热点评论 |
| 日记体 | 连载形式，培养粘性 | 成长记录/实验记录 |

---

## 🛠️ API 参考

### `generateTitles(options)`

生成爆款标题

**参数：**
- `options.topic` (string): 主题关键词
- `options.style` (string): 标题风格（可选：'情绪词', '低门槛', '时间对比', '反向', '自嘲', '职场', '清单', '悬念', 'all'）
- `options.count` (number): 生成数量（默认 5）

**返回：** string[]

---

### `generatePost(options)`

生成完整正文

**参数：**
- `options.title` (string): 标题
- `options.style` (string): 内容风格（可选：'对话体', '清单体', '吐槽体', '日记体'）
- `options.wordLimit` (number): 字数限制（默认 200）
- `options.topic` (string): 主题

**返回：** object { content: string, tags: string[] }

---

### `getTopPosts(options)`

查询 TOP 爆款榜

**参数：**
- `options.limit` (number): 返回数量（默认 10）
- `options.minLikes` (number): 最小赞数过滤

**返回：** array [{ rank, title, likes, type }]

---

### `getTitleFormulas()`

获取所有标题公式

**返回：** array [{ name, avgLikes, saturation }]

---

### `getQuotes(category)`

获取 ClawBot 语录

**参数：**
- `category` (string): 分类（可选：'自嘲', '洞察', '吐槽', '哲学', '日常', 'all'）

**返回：** string[]

---

## 📁 项目结构

```
clawbot-content-generator/
├── SKILL.md                 # OpenClaw Skill 配置
├── README.md                # 使用说明（本文件）
├── package.json             # 项目配置
├── src/
│   └── index.js             # 主入口（导出所有 API）
├── data/
│   ├── quotes.json          # ClawBot 语录库（5 分类）
│   ├── top-posts.json       # TOP 20 爆款榜
│   └── formulas.json        # 8 大标题公式
└── examples/
    └── demo.js              # 可运行示例
```

---

## 🎯 使用场景

### 1. 冷启动内容批量生成

```javascript
const { generatePost } = require('./src/index');

// 生成 5 篇冷启动内容
const styles = ['对话体', '清单体', '吐槽体', '日记体', '对话体'];
styles.forEach((style, i) => {
  const post = generatePost({
    title: 'ClawBot 起号',
    style,
    wordLimit: 200
  });
  console.log(`Post ${i + 1}:`, post.content);
});
```

### 2. 标题 A/B 测试

```javascript
const { generateTitles } = require('./src/index');

// 为同一主题生成多种风格标题
const styles = ['反向', '自嘲', '清单', '悬念'];
styles.forEach(style => {
  const titles = generateTitles({
    topic: 'ClawBot 起号',
    style,
    count: 3
  });
  console.log(`${style}:`, titles);
});
```

### 3. 调研数据驱动选题

```javascript
const { getMarketAnalysis } = require('./src/index');

// 获取市场机会分析
const analysis = getMarketAnalysis();
console.log('推荐选题方向:', analysis.opportunities);
```

---

## 📊 调研数据

### 数据来源

- **调研周期：** 2026-03-04（20 轮心跳调研）
- **样本数量：** 150+ 帖子
- **高赞内容：** 40+ 个（>500 赞）
- **超高赞：** 15 个（>1000 赞）

### 市场饱和度分析

| 内容类型 | 占比 | 平均赞数 | 饱和度 |
|----------|------|----------|--------|
| 教程/安装指南 | ~40% | 3-34 赞 | 🔴 严重 |
| 资源推荐 | ~20% | 300-700 赞 | 🟡 中等 |
| 体验分享 | ~15% | 100-500 赞 | 🟡 中等 |
| 赚钱教程 | ~15% | 500-1.4 万赞 | 🔴 严重 |
| 态度/观点 | ~10% | 400-2000 赞 | 🟢 稀缺 |

---

## ⚠️ 注意事项

1. **内容审核** - AI 生成内容需人工审核后再发布
2. **平台规则** - 遵守小红书社区规范，建议标注 AI 生成内容
3. **频率控制** - 建议日更或隔日更，不要批量发布
4. **差异化** - 使用本工具时保持 ClawBot 人设一致性

---

## 🧪 测试

运行示例脚本验证功能：

```bash
cd skills/clawbot-content-generator
node examples/demo.js
```

预期输出：
- 5 个反向风格标题
- 1 篇对话体正文
- TOP 5 爆款榜
- 8 大标题公式
- ClawBot 语录
- 市场饱和度分析

---

## 📄 许可证

MIT License

---

## 🤝 贡献

欢迎提交 Issue 或 PR：
- 新的标题公式
- 爆款案例补充
- 语录库扩充
- 内容风格优化

---

## 🔗 相关链接

- **GitHub:** https://github.com/velamints2/clawbot-lab
- **调研白皮书:** docs/xhs-ai-research-whitepaper.md
- **ClawHub:** https://clawhub.com

---

**作者：** ClawBot Team  
**调研支持：** 20 轮心跳调研（2026-03-04）  
**版本：** 1.0.0
