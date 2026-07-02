#!/usr/bin/env node
/**
 * GEO商机工作台 · 每周数据更新脚本
 * ====================================
 * 用法: node weekly-update.js
 *
 * 功能:
 *   1. 读取 index.html 中的现有数据
 *   2. 更新截止日期、复联状态等动态字段
 *   3. 写回 HTML
 *   4. 支持 --deploy 参数自动提交到 GitHub
 *
 * 注意: 招标和新软件数据需通过 web_fetch/手动方式收集后填入。
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const HTML_FILE = path.join(__dirname, 'index.html');

function formatDate(d) {
  const pad = n => String(n).padStart(2, '0');
  return `${d.getFullYear()}-${pad(d.getMonth()+1)}-${pad(d.getDate())}`;
}

/**
 * 从 HTML 中安全提取 __DATA__ 对象 (处理嵌套大括号)
 */
function extractData(html) {
  const startMarker = 'var __DATA__ = ';
  const idx = html.indexOf(startMarker);
  if (idx === -1) return null;

  let pos = idx + startMarker.length;
  let depth = 0;
  let inStr = false;
  let strChar = null;

  for (let i = pos; i < html.length; i++) {
    const ch = html[i];
    if (inStr) {
      if (ch === '\\') { i++; continue; }
      if (ch === strChar) inStr = false;
      continue;
    }
    if (ch === '"' || ch === "'") { inStr = true; strChar = ch; continue; }
    if (ch === '{') depth++;
    if (ch === '}') {
      depth--;
      if (depth === 0) {
        const raw = html.substring(pos, i + 1);
        try {
          return { data: new Function('return ' + raw)(), raw, start: idx, end: i + 1 };
        } catch (e) {
          console.error('[✗] 解析失败:', e.message);
          return null;
        }
      }
    }
  }
  return null;
}

/**
 * 更新数据中的动态字段
 * - 已过截止日期的招标条目标注过期
 * - 更新复联系目的优先级和可联系时间
 */
function refreshDynamicFields(data) {
  const now = new Date();

  // 招标条目 - 检查截止日期
  data.currentBidding = (data.currentBidding || []).map(item => {
    const dl = new Date(item.deadline);
    if (dl < now && item.status !== '⚠️ 已过期') {
      return { ...item, status: '⚠️ 已过期', notes: (item.notes || '') + ' [已过截止日期]' };
    }
    return item;
  });

  // 复联系目
  data.completedBidding = (data.completedBidding || []).map(item => {
    const end = new Date(item.serviceEnd);
    const daysLeft = Math.ceil((end - now) / 86400000);
    if (daysLeft <= 0) {
      return { ...item, priority: '紧急', recontactTiming: '🔥 已到期，立即联系！' };
    } else if (daysLeft <= 60) {
      return { ...item, priority: '高', recontactTiming: `⏰ ${daysLeft}天后到期，建议近日联系` };
    } else if (daysLeft <= 120) {
      return { ...item, priority: '中', recontactTiming: `📅 ${daysLeft}天后到期，请在60天前开始接触` };
    }
    return item; // priority: '低' 保持不变
  });

  data.lastUpdated = now.toISOString();
  // 保留 nextUpdate 但移除如果存在
  delete data.nextUpdate;
  return data;
}

/**
 * 将数据写回 HTML，保留原格式
 */
function writeData(html, data, rawStr) {
  const newRaw = JSON.stringify(data, null, 2)
    .replace(/"([^"]+)":/g, '$1:')       // 去掉键引号
    .replace(/"(\\"|[^"])*?"/g, m => m); // 保留值引号

  // 找到 var __DATA__ = ... 的结束位置, 替换为新的数据
  const startMarker = 'var __DATA__ = ';
  const startIdx = html.indexOf(startMarker);
  if (startIdx === -1) return html;

  // 同样用深度匹配找到结束
  let pos = startIdx + startMarker.length;
  let depth = 0, inStr = false, strChar = null, endIdx = pos;
  for (let i = pos; i < html.length; i++) {
    const ch = html[i];
    if (inStr) { if (ch === '\\') { i++; continue; } if (ch === strChar) inStr = false; continue; }
    if (ch === '"' || ch === "'") { inStr = true; strChar = ch; continue; }
    if (ch === '{') depth++;
    if (ch === '}') { depth--; if (depth === 0) { endIdx = i + 1; break; } }
  }

  const before = html.substring(0, pos);
  const after = html.substring(endIdx);
  return before + newRaw + after;
}

/**
 * 部署到 GitHub
 */
function deploy() {
  console.log('\n[🚀] 部署到 GitHub Pages...');
  try {
    execSync('git add -A', { cwd: __dirname, stdio: 'pipe' });
    execSync(`git commit -m "chore: 周报更新 - ${formatDate(new Date())}"`, { cwd: __dirname, stdio: 'pipe' });
    execSync('git push origin main', { cwd: __dirname, stdio: 'pipe' });
    console.log('[✓] 部署成功！https://liwei5666.github.io/geo-workbench/');
    return true;
  } catch (err) {
    console.log('[✗] 部署失败:', err.message);
    return false;
  }
}

function main() {
  const args = process.argv.slice(2);
  const shouldDeploy = args.includes('--deploy');

  console.log('📊 GEO商机工作台 · 数据更新');
  console.log(`   日期: ${formatDate(new Date())}\n`);

  // 1. 读取 HTML
  const html = fs.readFileSync(HTML_FILE, 'utf-8');
  const result = extractData(html);
  if (!result) {
    console.error('[✗] 无法提取数据');
    process.exit(1);
  }

  console.log('[✓] 读取成功');
  console.log(`   正在招标: ${result.data.currentBidding?.length || 0} 条`);
  console.log(`   潜力客户: ${result.data.potentialClients?.length || 0} 条`);
  console.log(`   已招标复联: ${result.data.completedBidding?.length || 0} 条`);
  console.log(`   软件追踪: ${result.data.software?.length || 0} 条`);

  // 2. 刷新动态字段
  const updated = refreshDynamicFields(result.data);

  // 3. 写回 HTML
  const newHtml = writeData(html, updated, result.raw);
  fs.writeFileSync(HTML_FILE, newHtml, 'utf-8');
  console.log('\n[✓] HTML 已更新');

  // 4. 输出摘要
  console.log('\n========================================');
  console.log('  📊 本周商机摘要');
  console.log('========================================\n');
  console.log('  🤖 AI创新商机');
  console.log('  ├─ 正在招标: ' + updated.currentBidding.length + ' 家');
  console.log('  ├─ 潜力客户: ' + updated.potentialClients.length + ' 家');
  console.log('  └─ 已招标复联: ' + updated.completedBidding.length + ' 家');
  console.log('');
  console.log('  📡 传统广告商机');
  console.log('  └─ 软件追踪: ' + updated.software.length + ' 款');
  console.log('');

  // 紧急事项提醒
  const urgent = updated.completedBidding.filter(c => c.priority === '紧急');
  if (urgent.length > 0) {
    console.log('  ⚠️ 紧急事项:');
    urgent.forEach(u => console.log('     🚨 ' + u.company + ' - ' + u.contractAmount + ' - ' + u.recontactTiming));
  }

  // 5. 部署
  if (shouldDeploy) {
    deploy();
  } else {
    console.log('\n[💡] 提示: node weekly-update.js --deploy 可自动部署到 GitHub Pages');
  }
}

main();
