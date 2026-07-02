#!/usr/bin/env node
/**
 * GEO商机工作台 · 每周数据更新脚本
 * ====================================
 * 用法: node weekly-update.js [--deploy]
 *
 * 1) 读取 index.html 中的 __DATA__（JS对象）
 * 2) 刷新动态字段（到期状态、复联优先级）
 * 3) 写回 HTML（JS对象格式、保留键无引号）
 * 4) --deploy 自动 commit + push
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const HTML_FILE = path.join(__dirname, 'index.html');

function pad(n) { return String(n).padStart(2, '0'); }
function today() {
  const d = new Date();
  return `${d.getFullYear()}-${pad(d.getMonth()+1)}-${pad(d.getDate())}`;
}

// ----- 解析 HTML 中的 __DATA__ (JS对象) -----
function parseData(html) {
  const MARKER = 'var __DATA__ = ';
  const idx = html.indexOf(MARKER);
  if (idx === -1) return null;
  let pos = idx + MARKER.length;
  let depth = 0, inStr = false, strChar = null, end = pos;
  for (let i = pos; i < html.length; i++) {
    const c = html[i];
    if (inStr) {
      if (c === '\\') { i++; continue; }
      if (c === strChar) inStr = false;
      continue;
    }
    if (c === '"' || c === "'") { inStr = true; strChar = c; continue; }
    if (c === '{') depth++;
    if (c === '}') { depth--; if (depth === 0) { end = i + 1; break; } }
  }
  const src = html.substring(pos, end);
  try {
    return { data: new Function('return ' + src)(), start: pos, end };
  } catch (e) {
    console.error('[✗] 数据解析失败:', e.message);
    return null;
  }
}

// ----- JS对象 → 缩进字符串 (键无引号) -----
function formatData(obj, indent) {
  indent = indent || '  ';
  if (obj === null || obj === undefined) return String(obj);
  const t = typeof obj;
  if (t === 'string') return JSON.stringify(obj);
  if (t === 'number' || t === 'boolean') return String(obj);
  if (Array.isArray(obj)) {
    if (obj.length === 0) return '[]';
    const items = obj.map(v => formatData(v, indent + '  '));
    // 如果所有项都是简单值，一行
    const oneLine = obj.every(v => typeof v === 'string' || typeof v === 'number' || typeof v === 'boolean');
    if (oneLine && items.join(', ').length < 80) {
      return '[' + items.join(', ') + ']';
    }
    // 尽量紧凑对简单对象
    const allSimpleObj = obj.every(v => typeof v === 'object' && v !== null && !Array.isArray(v) && Object.keys(v).length <= 8);
    if (allSimpleObj) {
      const compactItems = obj.map(v => {
        const keys = Object.keys(v);
        const pairs = keys.map(k => k + ':' + JSON.stringify(v[k]));
        return indent + '  {' + pairs.join(', ') + '}';
      });
      return '[\n' + compactItems.join(',\n') + '\n' + indent + ']';
    }
    return '[\n' + items.join(',\n') + '\n' + indent + ']';
  }
  if (t === 'object') {
    const keys = Object.keys(obj);
    if (keys.length === 0) return '{}';
    const pairs = keys.map(k => {
      // pricing 对象也保持简写
      if (k === 'pricing') {
        const pkeys = Object.keys(obj[k]);
        const ppairs = pkeys.map(pk => pk + ':' + JSON.stringify(obj[k][pk]));
        return indent + '  ' + k + ': {\n' +
               ppairs.map(p => indent + '    ' + p).join(',\n') + '\n' +
               indent + '  }';
      }
      return indent + '  ' + k + ': ' + formatData(obj[k], indent + '  ');
    });
    return '{\n' + pairs.join(',\n') + '\n' + indent + '}';
  }
  return String(obj);
}

// ----- 刷新动态字段 -----
function refresh(data) {
  const now = new Date();

  // 招标过期检查
  data.currentBidding = (data.currentBidding || []).map(item => {
    const dl = new Date(item.deadline);
    if (dl < now) {
      return { ...item, status: '⚠️ 已过期', notes: (item.notes || '') + ' [已过截止日期]' };
    }
    return item;
  });

  // 复联优先级
  data.completedBidding = (data.completedBidding || []).map(item => {
    const end = new Date(item.serviceEnd);
    const days = Math.ceil((end - now) / 86400000);
    if (days <= 0) {
      return { ...item, priority: '紧急', recontactTiming: '🔥 已到期，立即联系！' };
    } else if (days <= 60) {
      return { ...item, priority: '高', recontactTiming: `⏰ ${days}天后到期，建议近日联系` };
    } else if (days <= 120) {
      return { ...item, priority: '中', recontactTiming: `📅 ${days}天后到期` };
    }
    return item;
  });

  data.lastUpdated = now.toISOString();
  return data;
}

// ----- 写回 HTML -----
function writeBack(html, data, range) {
  const formatted = formatData(data, '  ');
  return html.substring(0, range.start) + formatted + html.substring(range.end);
}

// ----- 部署 -----
function deploy() {
  console.log('\n[🚀] 部署中...');
  try {
    execSync('git add index.html weekly-update.js', { cwd: __dirname, stdio: 'pipe' });
    execSync(`git commit -m "chore: 周报更新 - ${today()}"`, { cwd: __dirname, stdio: 'pipe' });
    execSync('git push origin main', { cwd: __dirname, stdio: 'pipe' });
    console.log('[✓] 已部署 → https://liwei5666.github.io/geo-workbench/');
  } catch (e) {
    console.log('[✗] 部署失败:', e.message);
  }
}

// ===== main =====
function main() {
  const args = process.argv.slice(2);
  const doDeploy = args.includes('--deploy');

  console.log('📊 GEO商机工作台 · 周报更新');
  console.log(`   日期: ${today()}\n`);

  const html = fs.readFileSync(HTML_FILE, 'utf-8');
  const parsed = parseData(html);
  if (!parsed) { process.exit(1); }

  const { data, start, end } = parsed;
  console.log(`[✓] 当前数据:`);
  console.log(`   正在招标: ${data.currentBidding?.length || 0}`);
  console.log(`   潜力客户: ${data.potentialClients?.length || 0}`);
  console.log(`   已招标复联: ${data.completedBidding?.length || 0}`);
  console.log(`   软件追踪: ${data.software?.length || 0}`);

  refresh(data);

  const newHtml = writeBack(html, data, { start, end });
  fs.writeFileSync(HTML_FILE, newHtml, 'utf-8');
  console.log(`\n[✓] HTML 已更新 (lastUpdated: ${data.lastUpdated})`);

  // 紧急提醒
  const urgent = (data.completedBidding || []).filter(c => c.priority === '紧急');
  if (urgent.length) {
    console.log(`\n⚠️ 紧急事项:`);
    urgent.forEach(u => console.log(`   🚨 ${u.company} - ${u.contractAmount} - ${u.recontactTiming}`));
  }

  if (doDeploy) deploy();
  else console.log('\n💡 node weekly-update.js --deploy 可自动部署');
}

main();
