import re, subprocess, json

PATH = '/Users/zzmac/.openclaw/workspace/geo-workbench/index.html'

with open(PATH, 'r') as f:
    c = f.read()

# Build index of all entries by section
sections = {
    'currentBidding': ['currentBidding:', 'potentialClients:'],
    'potentialClients': ['potentialClients:', 'completedBidding:'],
    'completedBidding': ['completedBidding:', 'competitorClients:'],
    'competitorClients': ['competitorClients:', 'software:'],
    'software': ['software:', 'lastUpdated:']
}

all_data = {}
for name, (start_str, end_str) in sections.items():
    s = c.find(start_str)
    e = c.find(end_str, s)
    all_data[name] = (s, e)

# Parse all entries from each section
def parse_entries(text):
    entries = []
    # Find all blocks starting with {\n
    blocks = re.findall(r'\{(.*?)\}', text, re.DOTALL)
    for block in blocks:
        d = {}
        for line in block.split('\n'):
            line = line.strip()
            m = re.match(r'(\w+):\s*(.+?)(?:,?\s*$)', line)
            if m:
                key, val = m.group(1), m.group(2).strip().strip('"').strip(',')
                d[key] = val
        if 'company' in d:
            entries.append(d)
    return entries

# Find ALL duplicates across ALL sections
all_companies = {}  # company -> [(section, id)]
for sec_name, (start, end) in all_data.items():
    text = c[start:end]
    entries = parse_entries(text)
    for entry in entries:
        company = entry.get('company', '')
        if not company:
            continue
        eid = entry.get('id', '')
        if company not in all_companies:
            all_companies[company] = []
        all_companies[company].append((sec_name, eid, entry))

# Cross-section duplicates
dups = {k: v for k, v in all_companies.items() if len(v) > 1}
print(f"Cross-section duplicates found: {len(dups)}")
for name, occ in sorted(dups.items()):
    secs = [o[0] for o in occ]
    ids = [o[1] for o in occ]
    print(f"  {name}: {', '.join(f'{s}({i})' for s,i in zip(secs, ids))}")
