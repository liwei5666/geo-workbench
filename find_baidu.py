#!/usr/bin/env python3
"""Find and delete 百度 potential client, check all website links"""

import re

with open('index.html', 'r') as f:
    content = f.read()

# Find all potential client entries
# They start with id: "pcXXX" and end with "}"
pc_pattern = re.compile(r'\{\s*id:\s*"[^"]+",\s*company:\s*"[^"]*百度[^"]*"[^}]*\}')
baidu_entries = pc_pattern.findall(content)
for entry in baidu_entries:
    # Extract company name
    m = re.search(r'company:\s*"([^"]+)"', entry)
    if m:
        print(f"Found: {m.group(1)}")

# Also check for company containing 度
pc_pattern2 = re.compile(r'\{\s*id:\s*"[^"]+",\s*company:\s*"[^"]*度[^"]*"[^}]*\}')
baidu2 = pc_pattern2.findall(content)
for entry in baidu2:
    m = re.search(r'company:\s*"([^"]+)"', entry)
    if m:
        print(f"Found 度: {m.group(1)}")
