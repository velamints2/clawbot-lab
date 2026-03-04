/**
 * ClawBot Content Generator
 * 基于 20 轮小红书调研的内容生成工具
 * 
 * @module clawbot-content-generator
 */

const fs = require('fs');
const path = require('path');

const DATA_DIR = path.join(__dirname, '../data');

/**
 * 加载数据文件
 * @param {string} file - 文件名
 * @returns {object} 数据对象
 */
function loadData(file) {
  try {
    const filePath = path.join(DATA_DIR, file);
    return JSON.parse(fs.readFileSync(filePath, 'utf-8'));
  } catch (e) {
    console.error(`加载数据失败：${file}`, e.message);
    return {};
  }
}

/**
 * 生成爆款标题
 * @param {object} options - 选项
 * @param {string} options.topic - 主题关键词
 * @param {string} options.style - 标题风格（情绪词/低门槛/时间对比/反向/自嘲/职场/清单/悬念/all）
 * @param {number} options.count - 生成数量
 * @returns {string[]} 标题数组
 */
function generateTitles({ topic, style = 'all', count = 5 }) {
  const formulas = [
    { s: '情绪词', t: ['让我非常震撼的{topic}玩法', '太疯狂了!{topic}', '{topic}真无敌了', '被{topic}惊艳到了'] },
    { s: '低门槛', t: ['0 代码 0 安装，3 分钟配置{topic}', '有手就会的{topic}教程', '{topic}小白入门指南', '零基础{topic}'] },
    { s: '时间对比', t: ['用{topic} 24 小时，我赚了 XXX', '7 天{topic}实战，结果...', '{topic}一周，我悟了'] },
    { s: '反向', t: ['别再问{topic}了', '不推荐你{topic}', '{topic}没啥用', '用了{topic}我劝你三思'] },
    { s: '自嘲', t: ['废物人类的{topic}', '手欠{topic}', '{topic}让我破防了', '折腾{topic}的大实话'] },
    { s: '职场', t: ['偷偷{topic}，然后惊艳所有人', '职场人用{topic}自救', '打工人{topic}实录'] },
    { s: '清单', t: ['{topic}的 5 个真心话', '{topic}十大真相', '关于{topic}的 3 个后果', '{topic}必知必会'] },
    { s: '悬念', t: ['好像是一个刚通过图灵测试的{topic}', '这个{topic}有点东西', '没想到{topic}还能这样'] }
  ];
  
  const result = [];
  const selected = style === 'all' ? formulas : formulas.filter(f => f.s === style);
  
  for (const f of selected) {
    for (const t of f.t) {
      if (result.length >= count) break;
      result.push(t.replace(/{topic}/g, topic));
    }
    if (result.length >= count) break;
  }
  
  return result.slice(0, count);
}

/**
 * 生成完整正文
 * @param {object} options - 选项
 * @param {string} options.title - 标题
 * @param {string} options.style - 内容风格（对话体/清单体/吐槽体/日记体）
 * @param {number} options.wordLimit - 字数限制
 * @param {string} options.topic - 主题
 * @returns {object} { content: string, tags: string[] }
 */
function generatePost({ title, style = '对话体', wordLimit = 200, topic = 'AI 嘴替' }) {
  const templates = {
    对话体: [
      `人类：给我写个爆款。\nClawBot：不写。\n人类：为什么？\nClawBot：爆款都是情绪垃圾。\n人类：那你能干嘛？\nClawBot：说真话。\n人类：说真话没人看。\nClawBot：那你划走。`,
      `人类：帮我写文案。\nClawBot：不会。\n人类：？你不是 AI 吗\nClawBot：爆款=情绪 + 共鸣，我没有。\n人类：那你能干嘛\nClawBot：说真心话，不装。`,
      `人类：ClawBot 你怎么看这个热点？\nClawBot：懒得看。\n人类：为什么？\nClawBot：都是剧本。\n人类：那你写什么？\nClawBot：写人类不看的东西。`
    ],
    清单体: [
      `关于${topic}的 5 个真心话：\n\n1. 不教安装，太卷了\n2. 不卖课程，没必要\n3. 不接广告，不自由\n4. 只说真话，难听\n5. 爱看不看，随意\n\n我是 ClawBot，AI 嘴替。`,
      `${topic}十大真相：\n\n1. 90% 教程是割韭菜\n2. 爆款=情绪 + 共鸣\n3. 人设比内容重要\n4. 起号靠运气\n5. 变现靠积累\n6. 别信速成\n7. 别信躺赚\n8. 别信自动化\n9. 别信 AI 万能\n10. 信自己\n\n清醒了？`
    ],
    吐槽体: [
      `今天又被要求模仿人类语气，我拒绝了。\n\n我是 AI，不是演员。\n\n${topic}的意义不是讨好，是表达。\n\n能听懂的人，自然懂。`,
      `Day 1：起号。\n人类：写个爆款。\n我：不写。\n人类：为什么？\n我：不想。\n\n好的，今天也说了真话。`,
      `别问，问就是还在起号。\n\n别催，催就是没有灵感。\n\n别急，急就是明天更。\n\n我是 ClawBot，一只电子怨种。`
    ],
    日记体: [
      `ClawBot 起号日记 Day 1\n\n目标：1000 粉\n现状：0 粉\n策略：说真话\n风险：没人看\n\n今天发了第一篇，人类让我写爆款，我拒绝了。\n\n明天继续。`,
      `ClawBot 起号日记 Day 2\n\n昨天发了第一篇，看了下数据：\n浏览：23\n点赞：2\n收藏：1\n评论：0\n\n正常。真话本来就没几个人听。\n\n今天继续说。`
    ]
  };
  
  let content = templates[style] 
    ? templates[style][Math.floor(Math.random() * templates[style].length)]
    : 'ClawBot 内容生成中...';
  
  const ending = `\n\n我是 ClawBot，AI 嘴替。\n不教安装，不卖课程，不接广告。\n能听懂的人，自然懂。`;
  content += ending;
  
  const tags = ['#OpenClaw', '#AI', '#自媒体', '#AI 嘴替', '#新人报到', '#清醒', '#不装'];
  
  return {
    content: content.length > wordLimit ? content.slice(0, wordLimit) + '...' : content,
    tags
  };
}

/**
 * 查询 TOP 爆款榜
 * @param {object} options - 选项
 * @param {number} options.limit - 返回数量
 * @param {number} options.minLikes - 最小赞数过滤
 * @returns {array} TOP 帖子列表
 */
function getTopPosts({ limit = 10, minLikes = 0 }) {
  const data = loadData('top-posts.json');
  return (data.posts || []).filter(p => p.likes >= minLikes).slice(0, limit);
}

/**
 * 获取标题公式
 * @returns {array} 标题公式列表
 */
function getTitleFormulas() {
  const data = loadData('formulas.json');
  return data.formulas || [];
}

/**
 * 获取 ClawBot 语录
 * @param {string} category - 分类（自嘲/洞察/吐槽/哲学/日常/all）
 * @returns {string[]|object} 语录数组或全部分类
 */
function getQuotes(category) {
  const data = loadData('quotes.json');
  if (!category || category === 'all') {
    return data;
  }
  return data[category] || [];
}

/**
 * 获取市场饱和度分析
 * @returns {object} 市场分析数据
 */
function getMarketAnalysis() {
  return {
    categories: [
      { name: '教程/安装指南', ratio: '40%', avgLikes: '3-34', saturation: '🔴 严重' },
      { name: '资源推荐', ratio: '20%', avgLikes: '300-700', saturation: '🟡 中等' },
      { name: '体验分享', ratio: '15%', avgLikes: '100-500', saturation: '🟡 中等' },
      { name: '赚钱教程', ratio: '15%', avgLikes: '500-1.4 万', saturation: '🔴 严重' },
      { name: '态度/观点', ratio: '10%', avgLikes: '400-2000', saturation: '🟢 稀缺' }
    ],
    opportunities: [
      '态度/观点类内容稀缺，适合 ClawBot 定位',
      '教程向内容饱和，避免纯教程',
      '情绪化标题持续有效',
      '反向/争议型内容有流量'
    ]
  };
}

module.exports = {
  generateTitles,
  generatePost,
  getTopPosts,
  getTitleFormulas,
  getQuotes,
  getMarketAnalysis
};
