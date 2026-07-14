#!/usr/bin/env python3
"""Delete Baidu potential client entry and save result"""

with open('index.html', 'r') as f:
    content = f.read()

# Find Baidu entry
idx = content.find('company: "百度"')
if idx < 0:
    # Try with different formatting
    idx = content.find('"百度"')
    if idx < 0:
        # Write error to marker file
        with open('/tmp/script_result.txt', 'w') as e:
            e.write('ERROR: Could not find 百度 entry')
        exit(1)

# Find the opening { of this entry (go back from the company field)
start = content.rfind('{', idx - 300, idx)
# Find the closing } followed by comma
end = content.find('}', idx)
# Find the entry end - look for }, or }\n,
snippet = content[end:end+5]
end_entry = end + 1
while end_entry < len(content) and content[end_entry] in ' \n\r,':
    end_entry += 1

# Remove the entry
before = content[:start]
after = content[end_entry:]
new_content = before + after

with open('index.html', 'w') as f:
    f.write(new_content)

with open('/tmp/script_result.txt', 'w') as r:
    r.write(f'OK: Deleted Baidu entry. Start={start}, end_entry={end_entry}')
    r.write(f'\nOriginal context: ...{content[max(0,idx-20):idx+30]}...')
