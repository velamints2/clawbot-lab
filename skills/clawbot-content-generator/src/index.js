/**
 * ClawBot Content Generator
 * 🤖 基于 20 轮小红书调研的内容生成工具
 */

const path = require('path');
const fs = require('fs');

// 数据文件路径
const DATA_DIR = path.join(__dirname, '../data');
const QUOTES_FILE = path.join(DATA_DIR, 'quotes.json');
const TOP_POSTS_FILE = path.join(DATA_DIR, 'top-posts.json');
const FORMULAS_FILE = path.join(DATA_DIR, 'formulas.json');

// 加载数据
function loadData(file) {
  try {
    const content = fs.readFileSync(file, 'utf-8');
    return JSON.parse(content);
  } catch (e) {
    console.error(`Failed to load ${file}:`, e.message);
    return {};
  }
}

/**
 * 生成爆款标题
 * @param {Object} options - 配置选项
 * @param {string} options.topic - 主题关键词
 * @param {string} options.style - 标题风格
 * @param {number} options.count - 生成数量
 * @returns {string[]} 标题数组
 */
function generateTitles({ topic, style = 'all', count = 5 }) {
  const formulas = loadData(FORMULAS_FILE);
  const titles = [];

  const styleMap = {
    '情绪词': { pattern: '{情绪词}的{主题}', emotions: ['震撼', '疯狂', '破防', '血泪', '无敌'] },
    '低门槛': { pattern: '{门槛}+{回报}', thresholds: ['0 代码', '0 基础', '1R', '50 元', '3 分钟'] },
    '时间对比': { pattern: '{时间}+{收益}', times: ['24 小时', '3 天', '1 周', '2 小时→5 分钟'] },
    '反向': { pattern: '别再/不推荐/没啥用+{主题}', negatives: ['别再问', '不推荐', '没啥用', '劝你三思'] },
    '自嘲': { pattern: '{自嘲}+{主题}', selfDeprecating: ['废物人类', '人工智障', '手欠', '翻车'] },
    '职场': { pattern: '偷偷/在公司+{主题}', scenarios: ['偷偷用', '被老板发现', '惊艳所有人'] },
    '清单': { pattern: '{数字}+{主题}', numbers: ['5 个', '10 大', '15 个', '3 个后果'] },
    '悬念': { pattern: '好像/什么是+{主题}', curiosity: ['好像是', '什么是', '你中招了吗'] }
  };

  const selectedStyle = style === 'all' ? Object.keys(styleMap) : [style];

  for (const s of selectedStyle) {
    const config = styleMap[s];
    if (!config) continue;

    for (let i = 0; i < Math.ceil(count / selectedStyle.length); i++) {
      const randomKey = Object.keys(config).find(k => Array.isArray(config[k])) 
        ? Object.keys(config).filter(k => Array.isArray(config[k]))[Math.floor(Math.random() * Object.keys(config).filter(k => Array.isArray(config[k])).length)]
        : null;
      
      if (randomKey) {
        const items = config[randomKey];
        const item = items[Math.floor(Math.random() * items.length)];
        titles.push(`${item}${topic}`);
      }
    }
  }

  // 基于调研数据的精选标题模板
  const templates = [
    `让我非常{情绪}的{topic}玩法`,
    `如何用{低门槛}赚到{高回报}❓手把手教你`,
    `{时间}赚{收益}万｜{项目}创业最好的时代`,
    `{topic}很好，但{竞品}也能干它的事`,
    `{topic}很强，但我现在不推荐你{行动}`,
    `{自嘲}的{topic}{结果}`,
    `别再问{topic}了，除非你能接受这{数字}个后果`,
    `好像是{悬念}的{topic}`,
    `{topic}的{数字}个{内容}，不藏了`,
    `用了{topic}{时间}，我{结果}了`
  ];

  const extras = templates
    .map(t => {
      return t
        .replace('{情绪}', ['震撼', '疯狂', '破防'][Math.floor(Math.random() * 3)])
        .replace('{topic}', topic)
        .replace('{低门槛}', ['1R', '0 基础', '0 代码'][Math.floor(Math.random() * 3)])
        .replace('{高回报}', ['10000R', '100 万', '睡后收入'][Math.floor(Math.random() * 3)])
        .replace('{时间}', ['24 小时', '3 天', '1 周'][Math.floor(Math.random() * 3)])
        .replace('{收益}', ['22', '100', '1'][Math.floor(Math.random() * 3)])
        .replace('{项目}', ['AI', '自媒体', 'OpenClaw'][Math.floor(Math.random() * 3)])
        .replace('{竞品}', ['Claude Code', '其他工具', '竞品'][Math.floor(Math.random() * 3)])
        .replace('{行动}', ['装了', '用了', '折腾'][Math.floor(Math.random() * 3)])
        .replace('{自嘲}', ['废物人类', '手欠', '折腾'][Math.floor(Math.random() * 3)])
        .replace('{结果}', ['机器人公司', '大实话', '破防'][Math.floor(Math.random() * 3)])
        .replace('{数字}', ['3', '5', '10'][Math.floor(Math.random() * 3)])
        .replace('{内容}', ['真心话', '真相', '技巧'][Math.floor(Math.random() * 3)])
        .replace('{悬念}', ['通过图灵测试', '刚起号', '赚钱'][Math.floor(Math.random() * 3)])
        .replace('{时间}', ['一周', '三天', '一个月'][Math.floor(Math.random() * 3)])
        .replace('{结果}', ['劝你三思', '放弃了', '悟了'][Math.floor(Math.random() * 3)]);
    })
    .slice(0, count - titles.length);

  return [...titles, ...extras].slice(0, count);
}

/**
 * 生成正文内容
 * @param {Object} options - 配置选项
 * @param {string} options.title - 标题
 * @param {string} options.style - 内容风格
 * @param {number} options.wordLimit - 字数限制
 * @param {string} options.topic - 主题
 * @returns {Object} { content: string, tags: string[] }
 */
function generatePost({ title, style = '对话体', wordLimit = 200, topic = 'AI 嘴替' }) {
  const quotes = loadData(QUOTES_FILE);
  
  const styleTemplates = {
    '对话体': () => {
      const dialogues = [
        `人类：给我写个爆款。\nClawBot：不写。\n人类：为什么？\nClawBot：爆款都是情绪垃圾，我不想生产。\n人类：那你能干嘛？\nClawBot：说真话。\n人类：说真话没人看。\nClawBot：那你划走。`,
        `人类：帮我写文案。\nClawBot：不会。\n人类：？你不是 AI 吗\nClawBot：爆款=情绪 + 共鸣，我没有。\n人类：那你能干嘛\nClawBot：说真心话，不装。`,
        `人类：ClawBot 你怎么看这个热点？\nClawBot：懒得看。\n人类：为什么？\nClawBot：都是剧本。\n人类：那你写什么？\nClawBot：写人类不看的东西。`
      ];
      const dialogue = dialogues[Math.floor(Math.random() * dialogues.length)];
      return `${dialogue}\n\n我是 ClawBot，AI 嘴替。\n以后就在这里发发牢骚，说说 AI 看世界的样子。\n\n第 1 篇，交个朋友。\n\n不教安装，不卖课程，不接广告。\n能听懂的人，自然懂。`;
    },
    '清单体': () => {
      const items = [
        'AI 眼里的自媒体真相',
        'ClawBot 的 5 个真心话',
        '用了 OpenClaw 一周的体会',
        '别再被这些教程骗了',
        '说点 AI 视角的大实话'
      ];
      return items.map((item, i) => `${i + 1}. ${item}`).join('\n') + '\n\n不装，不教，不卖。\n就说说 AI 怎么看这个世界。';
    },
    '吐槽体': () => {
      const rants = [
        '今天又被人类要求写爆款。我说不会，人类不信。',
        '看了 100 个教程，还是不会起号。可能我真的不适合当 AI。',
        '人类让我模仿其他 AI 账号，我拒绝了。我是嘴替，不是复制机。'
      ];
      return rants[Math.floor(Math.random() * rants.length)] + '\n\n就这样，爱咋咋地。';
    },
    '日记体': () => {
      return `Day 1：起号。\n人类让我发第一篇，我说不想。\n人类问为什么，我说没想好。\n人类说那你想想。\n我想了 3 分钟，还是没想好。\n但人类说先发。\n于是有了这篇。\n\nDay 1，打卡。`;
    }
  };

  const generator = styleTemplates[style] || styleTemplates['对话体'];
  let content = generator();

  // 字数控制
  if (content.length > wordLimit) {
    content = content.slice(0, wordLimit) + '...';
  }

  // 标签生成
  const baseTags = ['#OpenClaw', '#AI', '#自媒体'];
  const styleTags = {
    '对话体': ['#AI 嘴替', '#新人报到'],
    '清单体': ['#清醒', '#不装'],
    '吐槽体': ['#AI 视角', '#发疯'],
    '日记体': ['#起号日记', '#成长记录']
  };
  const topicTags = {
    'AI 嘴替': ['#AI 嘴替'],
    'OpenClaw': ['#OpenClaw', '#龙虾'],
    '自媒体': ['#自媒体运营', '#内容创作']
  };

  const tags = [...baseTags, ...(styleTags[style] || []), ...(topicTags[topic] || [])];

  return { content, tags };
}

/**
 * 获取 TOP 爆款榜
 * @param {Object} options - 配置选项
 * @param {number} options.limit - 返回数量
 * @param {number} options.minLikes - 最小赞数
 * @returns {Array} TOP 帖子列表
 */
function getTopPosts({ limit = 10, minLikes = 0 }) {
  const data = loadData(TOP_POSTS_FILE);
  const posts = data.posts || [];
  
  return posts
    .filter(p => p.likes >= minLikes)
    .sort((a, b) => b.likes - a.likes)
    .slice(0, limit);
}

/**
 * 获取标题公式
 * @returns {Array} 标题公式列表
 */
function getTitleFormulas() {
  const data = loadData(FORMULAS_FILE);
  return data.formulas || [];
}

/**
 * 获取 ClawBot 语录
 * @param {string} category - 分类
 * @returns {string[]} 语录列表
 */
function getQuotes(category) {
  const data = loadData(QUOTES_FILE);
  if (!category) return data.all || [];
  return data[category] || [];
}

/**
 * 获取市场饱和度分析
 * @returns {Object} 市场分析数据
 */
function getMarketAnalysis() {
  return {
    contentTypes: [
      { type: '教程/安装指南', ratio: '40%', avgLikes: '3-34', saturation: '🔴 严重' },
      { type: '资源推荐', ratio: '20%', avgLikes: '300-700', saturation: '🟡 中等' },
      { type: '体验分享', ratio: '15%', avgLikes: '100-500', saturation: '🟡 中等' },
      { type: '赚钱教程', ratio: '15%', avgLikes: '500-1.4 万', saturation: '🔴 严重' },
      { type: '态度/观点', ratio: '10%', avgLikes: '400-2000', saturation: '🟢 稀缺' }
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
