import re
import subprocess

path = '/Users/zzmac/.openclaw/workspace/geo-workbench/index.html'
with open(path) as f:
    c = f.read()

# Find pc015 and remove it
m = re.search(r',\s*\{\s*\n\s+id: "pc015",\n.*?\n\s+\}', c, re.DOTALL)
if m:
    c = c[:m.start()] + c[m.end():]
    with open(path, 'w') as f:
        f.write(c)
    subprocess.run(['git', '-C', '/Users/zzmac/.openclaw/workspace/geo-workbench', 'add', 'index.html'])
    subprocess.run(['git', '-C', '/Users/zzmac/.openclaw/workspace/geo-workbench', 'commit', '-m', 'remove 欧莱雅中国 from potential (already in bidding)'])
    subprocess.run(['git', '-C', '/Users/zzmac/.openclaw/workspace/geo-workbench', 'push'])
