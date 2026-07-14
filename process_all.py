#!/usr/bin/env python3
"""
1. Delete 百度 from potential clients
2. Check all website links (try HTTP)
3. Report results
"""
import urllib.request
import urllib.error
import ssl
import json

ssl._create_default_https_context = ssl._create_unverified_context

with open('/Users/zzmac/.openclaw/workspace/geo-workbench/index.html', 'r') as f:
    content = f.read()

# ========== 1. Delete 百度 ==========
idx = content.find('company: "百度"')
start = content.rfind('{', idx - 300, idx)
end = content.find('}', idx)
# Find the actual entry end - the }, or }, \n
pos = end
while pos < len(content) and content[pos] != ',':
    pos += 1
end_entry = pos + 1

entry_deleted = content[start:end_entry]
before = content[:start]
after = content[end_entry:]
content = before + after

# ========== 2. Check website links ==========
import re
pc_start = content.find('potentialClients: [')
pc_end = content.find('completedBidding: [')
pc_section = content[pc_start:pc_end]

websites = re.findall(r'website:\s*"([^"]*)"', pc_section)
results = []
for w in websites:
    url = w.strip()
    if not url or url == '—':
        results.append({'url': url, 'status': 'empty'})
        continue
    if not url.startswith('http'):
        url = 'https://' + url
    try:
        req = urllib.request.Request(url, method='HEAD')
        req.add_header('User-Agent', 'Mozilla/5.0')
        resp = urllib.request.urlopen(req, timeout=5)
        results.append({'url': w, 'status': resp.status, 'redirect': resp.url})
    except Exception as e:
        results.append({'url': w, 'status': f'ERROR: {str(e)[:60]}'})

report = []
report.append("=== 删除百度条目 ===")
report.append(f"已删除: {entry_deleted[:200]}...")
report.append("")

report.append("=== 网站链接检查结果 ===")
broken = 0
for r in results:
    s = r['status']
    if isinstance(s, int) and s < 400:
        report.append(f"✅ {r['url']} -> {s}")
    elif r['status'] == 'empty':
        report.append(f"➖ {r['url']} (empty)")
    else:
        report.append(f"❌ {r['url']} -> {r['status']}")
        broken += 1

report.append(f"\n总计检查: {len(results)} 个链接")
report.append(f"异常/打不开: {broken} 个")

report_text = '\n'.join(report)

with open('/tmp/link_check_report.txt', 'w') as f:
    f.write(report_text)

with open('/Users/zzmac/.openclaw/workspace/geo-workbench/index.html', 'w') as f:
    f.write(content)

print("DONE")
print(report_text)
