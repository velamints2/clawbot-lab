# ClawBot Content Generator

🤖 基于 20 轮小红书调研的 ClawBot 专用内容生成 Skill

## 功能

- **爆款标题生成** - 基于 8 大已验证公式
- **正文内容创作** - 对话体/清单体/吐槽体/日记体
- **标签推荐** - 基于竞品分析
- **调研数据查询** - TOP 爆款榜/标题公式/市场饱和度

## 安装

```bash
clawhub install clawbot-content-generator
```

或从 GitHub 安装：

```bash
git clone https://github.com/velamints2/xhs-ai-research.git
cd xhs-ai-research/skills/clawbot-content-generator
clawhub link
```

## 使用示例

### 生成标题

```javascript
const { generateTitles } = require('clawbot-content-generator');

const titles = generateTitles({
  topic: 'AI 嘴替',
  style: '反向劝退',
  count: 5
});
```

### 生成正文

```javascript
const { generatePost } = require('clawbot-content-generator');

const post = generatePost({
  title: '人类让我写爆款，我拒绝了',
  style: '对话体',
  wordLimit: 200
});
```

### 查询调研数据

```javascript
const { getTopPosts, getTitleFormulas } = require('clawbot-content-generator');

const topPosts = getTopPosts({ limit: 10, minLikes: 1000 });
const formulas = getTitleFormulas();
```

## API

### generateTitles(options)

- `topic` (string): 主题关键词
- `style` (string): 标题风格（情绪词/低门槛/时间对比/反向/自嘲/职场/清单/悬念）
- `count` (number): 生成数量

### generatePost(options)

- `title` (string): 标题
- `style` (string): 内容风格（对话体/清单体/吐槽体/日记体）
- `wordLimit` (number): 字数限制
- `topic` (string): 主题

### getTopPosts(options)

- `limit` (number): 返回数量
- `minLikes` (number): 最小赞数

### getTitleFormulas()

返回所有标题公式

### getQuotes(category)

- `category` (string): 语录分类（自嘲/洞察/吐槽/哲学/日常）

## 数据来源

- 20 轮心跳调研（2026-03-04）
- 150+ 帖子分析
- 40+ 高赞内容（>500 赞）
- 15+ 超高赞（>1000 赞）

## 许可证

MIT

## 作者

ClawBot Team

## GitHub

https://github.com/velamints2/xhs-ai-research
