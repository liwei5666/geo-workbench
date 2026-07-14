#!/usr/bin/env python3
"""Delete 百度 potential client and extract all website URLs"""
import re

with open('index.html', 'r') as f:
    content = f.read()

# Find all PC entries with their context
# Find the Baidu entry specifically
idx = content.find('company: "百度"')
if idx < 0:
    print("ERROR: Could not find 百度 entry")
    exit(1)

# Find the start of this entry (the opening {)
start = content.rfind('{', idx - 200, idx)
# Find the end of this entry (the closing })
end = content.find('}', idx)
# Find the next } to ensure we get the full entry
end2 = content.find('}', end + 1)
if end2 > 0 and content[end2-5:end2+1] not in [' },', '}\n,']:
    end = end2

# Get more context to find the exact block
block = content[start:end+2]
print(f"Entry to delete: {block[:200]}...")

# Extract the ID
id_match = re.search(r'id:\s*"([^"]+)"', block)
if id_match:
    entry_id = id_match.group(1)
    print(f"Entry ID: {entry_id}")

# Now extract all website URLs from potential clients
print("\n=== All website URLs from potential clients ===")
pc_start = content.find('potentialClients: [')
pc_end = content.find('completedBidding: [')
pc_section = content[pc_start:pc_end]

# Find all website: fields
websites = re.findall(r'website:\s*"([^"]*)"', pc_section)
for i, w in enumerate(websites):
    if w and w != '—':
        print(f"  URL {i+1}: {w}")
    else:
        print(f"  URL {i+1}: (empty/—)")

print(f"\nTotal URLs found: {len(websites)}")
