/**
 * ClawBot Content Generator - Demo
 * 运行此脚本验证所有功能
 */

const { generateTitles, generatePost, getTopPosts, getTitleFormulas, getQuotes, getMarketAnalysis } = require('../src/index');

console.log('🤖 ClawBot Content Generator Demo\n');
console.log('=' .repeat(50));

// 1. 生成标题
console.log('\n📝 生成标题（反向劝退风格）:');
generateTitles({ topic: 'AI 嘴替', style: '反向', count: 5 }).forEach((t, i) => 
  console.log(`  ${i + 1}. ${t}`)
);

// 2. 生成正文
console.log('\n📄 生成正文（对话体）:');
const post = generatePost({ title: '人类让我写爆款，我拒绝了', style: '对话体' });
console.log(post.content);
console.log('\n标签:', post.tags.join(' '));

// 3. TOP 爆款榜
console.log('\n🏆 TOP 5 爆款榜:');
getTopPosts({ limit: 5 }).forEach((p, i) => 
  console.log(`  ${i + 1}. ${p.title} - ${p.likes}赞 (${p.type})`)
);

// 4. 标题公式
console.log('\n📐 标题公式:');
getTitleFormulas().forEach((f, i) => 
  console.log(`  ${i + 1}. ${f.name} - 平均${f.avgLikes}赞 [${f.saturation}]`)
);

// 5. 语录
console.log('\n💬 ClawBot 语录（自嘲）:');
getQuotes('自嘲').slice(0, 3).forEach((q, i) => 
  console.log(`  ${i + 1}. "${q}"`)
);

// 6. 市场分析
console.log('\n📊 市场饱和度分析:');
const analysis = getMarketAnalysis();
analysis.categories.forEach(c => 
  console.log(`  ${c.name}: ${c.ratio} | 均赞${c.avgLikes} | ${c.saturation}`)
);

console.log('\n💡 机会点:');
analysis.opportunities.forEach((o, i) => 
  console.log(`  • ${o}`)
);

console.log('\n' + '='.repeat(50));
console.log('✅ Demo 完成！\n');
