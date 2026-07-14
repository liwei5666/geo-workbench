import re, json, subprocess

PATH = '/Users/zzmac/.openclaw/workspace/geo-workbench/index.html'

with open(PATH, 'r') as f:
    c = f.read()

# Helper to extract entries from a section
def get_section(text, start_marker, end_marker):
    s = text.find(start_marker)
    e = text.find(end_marker, s)
    return s, e, text[s:e]

def parse_entries(section_text):
    """Parse entries from a section text, return list of dicts"""
    entries = []
    # Split by { and } patterns
    blocks = re.findall(r'\{([^}]*)\}', section_text)
    for block in blocks:
        d = {}
        for line in block.split('\n'):
            line = line.strip()
            if not line or line == ',':
                continue
            m = re.match(r'(\w+):\s*(.*?)\s*(?:,?\s*$)', line)
            if m:
                key = m.group(1)
                val = m.group(2).strip().strip('"').strip(',')
                d[key] = val
        if 'company' in d or 'name' in d:
            entries.append(d)
    return entries

# Get all sections
sec_start = c.find('currentBidding:')
pc_start = c.find('potentialClients:', sec_start)
cb_start = c.find('completedBidding:', pc_start)
comp_start = c.find('competitorClients:', cb_start)
sw_start = c.find('software:', comp_start)
lu_start = c.find('lastUpdated:', sw_start)

sections = [
    ('bidding', sec_start, pc_start),
    ('potential', pc_start, cb_start),
    ('completed', cb_start, comp_start),
    ('competitor', comp_start, sw_start),
    ('software', sw_start, lu_start),
]

# Find all cross-section duplicates
company_map = {}  # company -> list of (section_name, id)
for sec_name, s, e in sections:
    text = c[s:e]
    entries = parse_entries(text)
    for entry in entries:
        company = entry.get('company', entry.get('name', ''))
        if not company:
            continue
        eid = entry.get('id', '')
        if company not in company_map:
            company_map[company] = []
        company_map[company].append((sec_name, eid, entry))

cross_dups = {k: v for k, v in company_map.items() if len(v) > 1}
print(f"Cross-section duplicates: {len(cross_dups)}")

# Within-section duplicates - clean potentialClients
# Find duplicates within the same section
for sec_name, s, e in sections:
    text = c[s:e]
    entries = parse_entries(text)
    seen_in_section = {}
    to_remove_ids = []
    
    for entry in entries:
        company = entry.get('company', entry.get('name', ''))
        if not company:
            continue
        eid = entry.get('id', '')
        if company in seen_in_section:
            to_remove_ids.append(eid)
            print(f"  REMOVE {sec_name}: {eid} {company}")
        else:
            seen_in_section[company] = eid
    
    if to_remove_ids:
        # Remove duplicates by removing their entry blocks
        for eid in to_remove_ids:
            # Find and remove the entry block
            pattern = r',\s*\{\s*\n\s+id: "' + eid + r'",\n.*?\n\s+\}'
            c = re.sub(pattern, '', c, flags=re.DOTALL, count=1)

with open(PATH, 'w') as f:
    f.write(c)

print("Fixed. Now validating...")

# Validate
with open(PATH, 'r') as f:
    c = f.read()

m = re.search(r'<script>([\s\S]*?)</script>', c)
dm = re.search(r'var __DATA__ = \{([\s\S]*?)\n  \};', m.group(1))
if dm:
    exec('D = {' + dm.group(1) + '\n}')
    print(f"PC: {len(D.potentialClients)}, CB: {len(D.currentBidding)}, Done: {len(D.completedBidding)}, Comp: {len(D.competitorClients)}, SW: {len(D.software)}")
    
    # Verify no more duplicates
    seen = {}
    for item in D.potentialClients:
        n = item.company
        if n in seen:
            print(f"  STILL DUPLICATE: {n}")
        seen[n] = True
else:
    print("JS PARSE ERROR")
