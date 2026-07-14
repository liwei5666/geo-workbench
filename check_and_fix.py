#!/usr/bin/env python3
"""
Full script: delete Baidu, check all potential client websites, report broken ones.
Writes result to link_check_report.txt
"""

import re, ssl, urllib.request, urllib.error, os

ssl._create_default_https_context = ssl._create_unverified_context

path = '/Users/zzmac/.openclaw/workspace/geo-workbench/index.html'
with open(path, 'r') as f:
    content = f.read()

# === Delete 百度 ===
idx = content.find('company: "百度"')
if idx > 0:
    start = content.rfind('{', idx - 300, idx)
    end = content.find('}', idx)
    pos = end
    while pos < len(content) and content[pos] != ',':
        pos += 1
    end_entry = pos + 1
    content = content[:start] + content[end_entry:]
    print("✅ Deleted Baidu entry")
else:
    print("⚠️ Baidu entry not found")

# === Check all potential client websites ===
pc_start = content.find('potentialClients: [')
pc_end = content.find('completedBidding: [')
pc_section = content[pc_start:pc_end]

# Find all website: fields with surrounding context (for company name)
entries = re.findall(r'company:\s*"([^"]*)"[^}]*website:\s*"([^"]*)"', pc_section)
entries += re.findall(r'website:\s*"([^"]*)"[^}]*company:\s*"([^"]*)"', pc_section)
# Simpler approach - extract both fields separately
companies = re.findall(r'company:\s*"([^"]*)"', pc_section)
websites = re.findall(r'website:\s*"([^"]*)"', pc_section)

# Pair them up (they should be in order)
results = []
for comp, web in zip(companies, websites):
    results.append((comp, web))

# Check URLs
report_lines = []
report_lines.append("=== 潜力客户网站链接检查 ===")
report_lines.append("")

broken_urls = []
for comp, url in results:
    if not url or url == '—':
        report_lines.append(f"  {comp}: (无官网)")
        continue
    try:
        test_url = url
        if not test_url.startswith('http'):
            test_url = 'https://' + test_url
        req = urllib.request.Request(test_url, method='HEAD')
        req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)')
        resp = urllib.request.urlopen(req, timeout=5)
        report_lines.append(f"✅ {comp}: {url} -> {resp.status}")
    except Exception as e:
        err_msg = str(e)[:60]
        report_lines.append(f"❌ {comp}: {url} -> {err_msg}")
        broken_urls.append((comp, url, err_msg))

report_lines.append("")
report_lines.append(f"总计检查: {len(results)} 个链接")
report_lines.append(f"异常/打不开: {len(broken_urls)} 个")
if broken_urls:
    report_lines.append("")
    report_lines.append("=== 异常链接明细 ===")
    for comp, url, err in broken_urls:
        report_lines.append(f"  {comp}: {url} ({err})")

report_text = '\n'.join(report_lines)

# Save to file
with open('/Users/zzmac/.openclaw/workspace/geo-workbench/link_check_report.txt', 'w') as f:
    f.write(report_text)

# Save modified HTML
with open(path, 'w') as f:
    f.write(content)

print("DONE - report saved to link_check_report.txt")
print(report_text[:2000])
