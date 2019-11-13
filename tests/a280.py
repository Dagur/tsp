import gzip
import re
from collections import deque

rex = re.compile(r'\s*(\d+)\s+(\d+)\s+(\d+)')
lines = deque([])

with gzip.open('tests/data/a280.tsp.gz') as f:
    data = f.read()

for line in data.split('\n'):
    m = rex.match(line)
    if m:
        lines.append((m.group(2), m.group(3)))

print(len(lines))