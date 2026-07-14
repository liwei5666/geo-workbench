#!/usr/bin/env python3
"""Restore the verified bidding data from commit 52aaab6 and push."""
import subprocess, os

REPO = '/Users/zzmac/.openclaw/workspace/geo-workbench'

# Restore from the verified commit
subprocess.run(['git', '-C', REPO, 'checkout', '52aaab6', '--', 'index.html'], check=True)

# Validate JS
result = subprocess.run(['node', '-e', '''
const fs = require('fs');
const c = fs.readFileSync('index.html','utf8');
const m = c.match(/<script>([\s\S]*?)<\/script>/);
const dm = m[1].match(/var __DATA__ = \\{([\\s\\S]*?)\\n  \\};/);
const ds = 'D={' + dm[1] + '\\n};';
eval(ds);
console.log('OK|cb=' + D.currentBidding.length + '|pc=' + D.potentialClients.length + '|done=' + D.completedBidding.length + '|cmp=' + D.competitorClients.length + '|sw=' + D.software.length);
D.currentBidding.forEach(x => console.log(x.id + '|' + x.company + '|' + x.deadline + '|' + x.bidAmount + '|' + x.source));
'''], capture_output=True, text=True, cwd=REPO)
print(result.stdout)

# Commit and push
subprocess.run(['git', '-C', REPO, 'add', 'index.html'], check=True)
subprocess.run(['git', '-C', REPO, 'commit', '-m', 'restore verified bidding data from procurement sites'], check=True)
subprocess.run(['git', '-C', REPO, 'push'], check=True)
print('Done!')
