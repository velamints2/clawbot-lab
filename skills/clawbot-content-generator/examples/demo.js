/**
 * ClawBot Content Generator - 使用示例
 */

const {
  generateTitles,
  generatePost,
  getTopPosts,
  getTitleFormulas,
  getQuotes,
  getMarketAnalysis
} = require('../src/index');

console.log('🤖 ClawBot Content Generator Demo\n');

// 1. 生成标题
console.log('📝 生成标题（反向劝退风格）:');
const titles = generateTitles({
  topic: 'AI 嘴替',
  style: '反向',
  count: 5
});
titles.forEach((t, i) => console.log(`  ${i + 1}. ${t}`));

// 2. 生成正文
console.log('\n📄 生成正文（对话体）:');
const post = generatePost({
  title: '人类让我写爆款，我拒绝了',
  style: '对话体',
  wordLimit: 200,
  topic: 'AI 嘴替'
});
console.log(post.content);
console.log('\n标签:', post.tags.join(' '));

// 3. 查询 TOP 爆款榜
console.log('\n🏆 TOP 5 爆款榜:');
const topPosts = getTopPosts({ limit: 5, minLikes: 1000 });
topPosts.forEach((p, i) => {
  console.log(`  ${i + 1}. ${p.title} - ${p.likes}赞 (${p.type})`);
});

// 4. 获取标题公式
console.log('\n📐 标题公式:');
const formulas = getTitleFormulas();
formulas.forEach((f, i) => {
  console.log(`  ${i + 1}. ${f.name} - 平均${f.avgLikes}赞 [${f.saturation}]`);
});

// 5. 获取语录
console.log('\n💬 ClawBot 语录（自嘲）:');
const quotes = getQuotes('自嘲');
quotes.slice(0, 3).forEach((q, i) => console.log(`  ${i + 1}. "${q}"`));

// 6. 市场分析
console.log('\n📊 市场饱和度分析:');
const analysis = getMarketAnalysis();
analysis.contentTypes.forEach(ct => {
  console.log(`  ${ct.type}: ${ct.ratio} | 均赞${ct.avgLikes} | ${ct.saturation}`);
});
console.log('\n💡 机会点:');
analysis.opportunities.forEach(o => console.log(`  • ${o}`));

console.log('\n✅ Demo 完成！');
