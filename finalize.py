#!/usr/bin/env python3
"""Final script: delete Baidu, link report, commit"""

with open('/Users/zzmac/.openclaw/workspace/geo-workbench/index.html', 'r') as f:
    content = f.read()

# Find and delete 百度 entry
idx = content.find('company: "百度"')
start = content.rfind('{', idx - 300, idx)
end = content.find('}', idx)
pos = end
while pos < len(content) and content[pos] != ',':
    pos += 1
end_entry = pos + 1

content = content[:start] + content[end_entry:]

with open('/Users/zzmac/.openclaw/workspace/geo-workbench/index.html', 'w') as f:
    f.write(content)

print("百度 deleted OK")
