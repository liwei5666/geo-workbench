import re

with open('/Users/zzmac/.openclaw/workspace/geo-workbench/index.html', 'r') as f:
    c = f.read()

# Remove duplicate entries from each section by company name
# For potentialClients: keep first occurrence, remove later duplicates

sections = [
    ('currentBidding:', 'potentialClients:'),
    ('potentialClients:', 'completedBidding:'),
    ('completedBidding:', 'competitorClients:'),
    ('competitorClients:', 'software:'),
    ('software:', 'lastUpdated:')
]

for sec_name, next_sec in sections:
    s = c.find(sec_name)
    e = c.find(next_sec, s)
    if s < 0 or e < 0:
        continue
    sec = c[s:e]
    
    # Parse entries by finding pattern: \n    { or \n{
    # Extract company name from each entry
    entries = re.split(r'\n\s*\{', sec)
    if len(entries) <= 1:
        continue
    
    # First entry is the section header
    seen = {}
    new_entries = [entries[0]]
    dups_removed = 0
    
    for entry in entries[1:]:
        m = re.search(r'company: "([^"]+)"', entry)
        if m:
            name = m.group(1)
            if name in seen:
                dups_removed += 1
                continue
            seen[name] = True
        
        if dups_removed == 0:
            new_entries.append(entry)
        else:
            new_entries.append('    {' + entry)
    
    new_sec = '\n'.join(new_entries)
    if dups_removed > 0:
        c = c[:s] + new_sec + c[e:]
    print(f'{sec_name} removed {dups_removed} dups')

with open('/Users/zzmac/.openclaw/workspace/geo-workbench/index.html', 'w') as f:
    f.write(c)
