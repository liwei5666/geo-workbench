#!/usr/bin/env node
/**
 * GEO商机工作台 · 每周数据更新脚本
 * =======================================
 * 用法: node weekly-update.js [--deploy]
 * 每周自动运行一次，更新招标数据、潜力客户、复联客户和新软件
 *
 * --deploy 参数: 更新后自动 push 到 GitHub Pages
 *
 * 数据来源:
 *   - 招标信息: 政府采购网、招标投标公共服务平台等
 *   - 新软件: 钛媒体、36氪、Product Hunt 等科技媒体
 *   - 标注 ⚠️ 的信息表示需人工核实
 */

const fs = require('fs');
const path = require('path');
const https = require('https');
const http = require('http');
const { execSync } = require('child_process');

const HTML_FILE = path.join(__dirname, 'index.html');
const CACHE_DIR = path.join(__dirname, '.cache');

// ============================================================
// 配置
// ============================================================
const CONFIG = {
  // 行业商机概率排名 (优先级由高到低)
  industryPriority: [
    '医疗', '游戏', '机械设备', '本地生活', '企业服务',
    '教育', '科技3C', '金融理财', '电商快销', 'IT软件'
  ],
  // 招标信息源 (URL前缀)
  biddingSources: [
    { name: '中国政府采购网', url: 'https://www.ccgp.gov.cn/cggg/zygg/gkzb/index.htm' },
    { name: '中国招标投标公共服务平台', url: 'https://www.cebpubservice.com' },
  ],
  // 科技媒体源 (找新软件)
  techSources: [
    { name: '钛媒体', url: 'https://www.tmtpost.com/' },
    { name: 'IT桔子', url: 'https://www.itjuzi.com/' },
  ],
  // crawl timeout
  timeout: 15000,
};

// ============================================================
// 工具函数
// ============================================================
function fetchUrl(url) {
  return new Promise((resolve, reject) => {
    const client = url.startsWith('https') ? https : http;
    const req = client.get(url, {
      timeout: CONFIG.timeout,
      headers: {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
      }
    }, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => resolve({ status: res.statusCode, data }));
    });
    req.on('error', reject);
    req.on('timeout', () => { req.destroy(); reject(new Error('timeout')); });
  });
}

function formatDate(date) {
  const d = date || new Date();
  return d.toISOString().split('T')[0];
}

function randomId(prefix) {
  return prefix + Date.now().toString(36) + Math.random().toString(36).slice(2, 6);
}

// ============================================================
// 数据收集模块
// ============================================================

/**
 * 收集正在招标的客户信息
 * 从政府招标平台获取最新招标公告
 * 匹配SEO/营销/品牌推广相关的项目
 */
async function collectBiddingData() {
  console.log('[📋] 收集招标信息...');
  const results = [];

  try {
    // 尝试从中国政府采购网获取公开招标公告
    const resp = await fetchUrl('https://www.ccgp.gov.cn/cggg/zygg/gkzb/index.htm');
    if (resp.status === 200 && resp.data.length > 100) {
      console.log('  ✓ 中国政府采购网 访问成功');
      // 尝试解析招标列表 - 简单提取标题和链接
      const titleMatches = resp.data.match(/<a[^>]*href="([^"]*)"[^>]*>([^<]+)<\/a>/g) || [];
      // 需要具体解析，这里作为基础框架
      console.log(`  → 找到 ${titleMatches.length} 个招标条目（待解析）`);
    } else {
      console.log('  ⚠ 中国政府采购网 返回状态码: ' + resp.status);
    }
  } catch (err) {
    console.log('  ⚠ 中国政府采购网 访问失败: ' + err.message);
  }

  // 如果无法爬取，返回基础模板并标注 ⚠️
  console.log('  ⚠️ 部分数据需人工核实补充');
  return results;
}

/**
 * 收集新发布的软件产品
 * 从科技媒体获取最新产品发布信息
 */
async function collectSoftwareData() {
  console.log('[📡] 收集软件产品信息...');
  const results = [];

  try {
    const resp = await fetchUrl('https://www.tmtpost.com/');
    if (resp.status === 200 && resp.data.length > 100) {
      console.log('  ✓ 钛媒体 访问成功');
      // 提取文章标题和摘要
      const lines = resp.data.split('\n');
      const titles = lines.filter(l => l.includes('"title"')).slice(0, 20);
      console.log(`  → 获取到 ${titles.length} 篇相关文章`);
    }
  } catch (err) {
    console.log('  ⚠ 钛媒体 访问失败: ' + err.message);
  }

  return results;
}

/**
 * 生成本周的完整数据集
 */
async function generateWeeklyData() {
  console.log('\n========================================');
  console.log('  GEO商机工作台 · 每周数据更新');
  console.log('  日期: ' + formatDate());
  console.log('========================================\n');

  // 1. 读取现有数据
  let existingHtml = fs.readFileSync(HTML_FILE, 'utf-8');
  const dataMatch = existingHtml.match(/var __DATA__ = (\{[\s\S]*?\});\s*\n\s*var D = __DATA__;/);
  let existingData = null;
  if (dataMatch) {
    try {
      // 使用 Function 构造器安全解析
      existingData = new Function('return ' + dataMatch[1])();
      console.log('[✓] 读取到现有数据');
      console.log('    正在招标: ' + (existingData.currentBidding?.length || 0) + ' 条');
      console.log('    潜力客户: ' + (existingData.potentialClients?.length || 0) + ' 条');
      console.log('    已招标复联: ' + (existingData.completedBidding?.length || 0) + ' 条');
      console.log('    软件追踪: ' + (existingData.software?.length || 0) + ' 条');
    } catch (e) {
      console.log('[✗] 解析现有数据失败: ' + e.message);
      existingData = null;
    }
  }

  // 2. 收集新数据
  const newBidding = await collectBiddingData();
  const newSoftware = await collectSoftwareData();

  // 3. 如果爬取到新数据，融合更新
  // 否则保留现有数据并更新日期
  const now = new Date();
  const weekLater = new Date(now.getTime() + 7 * 24 * 60 * 60 * 1000);

  const updatedData = {
    currentBidding: existingData?.currentBidding || [],
    potentialClients: existingData?.potentialClients || [],
    completedBidding: existingData?.completedBidding || [],
    software: existingData?.software || [],
    lastUpdated: now.toISOString(),
    nextUpdate: weekLater.toISOString(),
  };

  // 如果有新数据，合并
  if (newBidding.length > 0) {
    updatedData.currentBidding = [...newBidding, ...updatedData.currentBidding].slice(0, 50);
  }
  if (newSoftware.length > 0) {
    updatedData.software = [...newSoftware, ...updatedData.software].slice(0, 30);
  }

  // 更新截止日期过期的招标条目状态
  updatedData.currentBidding = updatedData.currentBidding.map(item => {
    const deadline = new Date(item.deadline);
    if (deadline < now) {
      return { ...item, status: '⚠️ 已过期 - 建议跟进', notes: (item.notes || '') + ' [已过截止日期]' };
    }
    return item;
  });

  // 更新复联系目的"可接触时间"
  updatedData.completedBidding = updatedData.completedBidding.map(item => {
    const endDate = new Date(item.serviceEnd);
    const daysLeft = Math.ceil((endDate - now) / 86400000);
    if (daysLeft <= 0) {
      return { ...item, priority: '紧急', recontactTiming: '⚠️ 已到期，请立即联系！' };
    } else if (daysLeft <= 60) {
      return { ...item, priority: '高', recontactTiming: `⏰ ${daysLeft}天后到期，建议近日联系` };
    } else if (daysLeft <= 120) {
      return { ...item, priority: '中', recontactTiming: `📅 ${daysLeft}天后到期，${formatDate(new Date(now.getTime() + (daysLeft - 60) * 86400000))}起可接触` };
    }
    return item;
  });

  console.log('\n[✓] 数据更新完成');
  console.log('    正在招标: ' + updatedData.currentBidding.length + ' 条');
  console.log('    潜力客户: ' + updatedData.potentialClients.length + ' 条');
  console.log('    已招标复联: ' + updatedData.completedBidding.length + ' 条');
  console.log('    软件追踪: ' + updatedData.software.length + ' 条');

  return { updatedData, existingHtml };
}

/**
 * 将数据写入 HTML 文件
 */
function writeHtml(existingHtml, data) {
  console.log('\n[✏] 写入更新后的 HTML...');

  // 找到 __DATA__ 定义并替换
  const dataStr = JSON.stringify(data, null, 2);
  // 格式化成缩进的 JS 对象 (去掉 JSON 的引号键名)
  const jsDataStr = dataStr
    .replace(/"([^"]+)":/g, '$1:')  // 去掉键的引号
    .replace(/"(\\"|[^"])*?"/g, match => match);  // 保留字符串值的引号

  // 构建新的 __DATA__ 赋值
  const newDataBlock = `var __DATA__ = ${dataStr.replace(/"([^"]+)":/g, '$1:')};\n\nvar D = __DATA__;`;

  // 替换 HTML 中的 __DATA__ 部分
  const updatedHtml = existingHtml.replace(
    /var __DATA__ = \{[\s\S]*?\};\s*\n\s*var D = __DATA__;/,
    newDataBlock
  );

  fs.writeFileSync(HTML_FILE, updatedHtml, 'utf-8');
  console.log('[✓] HTML 文件已更新');
  return updatedHtml;
}

/**
 * 部署到 GitHub Pages
 */
function deploy() {
  console.log('\n[🚀] 部署到 GitHub Pages...');
  try {
    execSync('git add index.html', { cwd: __dirname, stdio: 'pipe' });
    const dateStr = formatDate();
    execSync(`git commit -m "chore: 周报更新 - ${dateStr}"`, { cwd: __dirname, stdio: 'pipe' });
    execSync('git push origin main', { cwd: __dirname, stdio: 'pipe' });
    console.log('[✓] 部署成功！');
    console.log(`    访问: https://liwei5666.github.io/geo-workbench/`);
  } catch (err) {
    console.log('[✗] 部署失败: ' + err.message);
    console.log('    请手动运行: cd geo-workbench && git push');
  }
}

// ============================================================
// 主流程
// ============================================================
async function main() {
  const args = process.argv.slice(2);
  const shouldDeploy = args.includes('--deploy');

  try {
    const { updatedData, existingHtml } = await generateWeeklyData();
    writeHtml(existingHtml, updatedData);

    if (shouldDeploy) {
      deploy();
    } else {
      console.log('\n[💡] 提示: 运行 node weekly-update.js --deploy 可自动部署');
    }

    // 输出摘要报告
    console.log('\n========================================');
    console.log('  📊 本周商机摘要');
    console.log('========================================');
    console.log('');
    console.log('  🤖 AI创新商机');
    console.log('  ├─ 正在招标: ' + updatedData.currentBidding.length + ' 家客户');
    console.log('  ├─ 潜力客户: ' + updatedData.potentialClients.length + ' 家');
    console.log('  └─ 已招标复联: ' + updatedData.completedBidding.length + ' 家');
    console.log('');
    console.log('  📡 传统广告商机');
    console.log('  └─ 软件追踪: ' + updatedData.software.length + ' 款');
    console.log('');
    console.log('  📅 下一次更新: ' + (updatedData.nextUpdate || '7天后'));
    console.log('========================================\n');

  } catch (err) {
    console.error('\n[✗] 更新失败:', err.message);
    process.exit(1);
  }
}

main();
