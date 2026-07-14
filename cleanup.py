import re, subprocess

PATH = '/Users/zzmac/.openclaw/workspace/geo-workbench/index.html'

with open(PATH, 'r') as f:
    c = f.read()

# Remove within-section duplicates for potentialClients
# Find all company names in potentialClients
pc_start = c.find('potentialClients:')
pc_end = c.find('completedBidding:', pc_start)
pc_text = c[pc_start:pc_end]

# Find all entries with their ids
entries = re.findall(r'id: "([^"]+)"[^}]*company: "([^"]+)"', pc_text)
seen = {}
to_remove = []
for eid, company in entries:
    if company in seen:
        to_remove.append(eid)
    seen[company] = eid

# Remove duplicate entries by id
for eid in to_remove:
    pattern = r',\s*\{\s*\n\s+id: "' + eid + r'",\n.*?\n\s+\}'
    c = re.sub(pattern, '', c, flags=re.DOTALL, count=1)

with open(PATH, 'w') as f:
    f.write(c)

# Git commit
subprocess.run(['git', '-C', '/Users/zzmac/.openclaw/workspace/geo-workbench', 'add', 'index.html'])
subprocess.run(['git', '-C', '/Users/zzmac/.openclaw/workspace/geo-workbench', 'commit', '-m', 'remove all duplicate companies'])
subprocess.run(['git', '-C', '/Users/zzmac/.openclaw/workspace/geo-workbench', 'push'])

print("done")
