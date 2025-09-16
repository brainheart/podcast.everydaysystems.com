#!/usr/bin/env python3
from pathlib import Path
root = Path(__file__).resolve().parent.parent
files = list(root.rglob('*.html'))
problem = []
for f in files:
    s = f.read_text(encoding='utf-8')
    cnt = s.count('/assets/js/year.js')
    if cnt > 1:
        problem.append((str(f), cnt))

if problem:
    print('FILES WITH MULTIPLE year.js INCLUDES:')
    for p,c in problem:
        print(p, c)
else:
    print('All files have at most one year.js include')
