#!/usr/bin/env python3
from pathlib import Path
import sys
root=Path(__file__).resolve().parents[1]
pkg=root/'kristaldiag/resources'
pairs=[(root/'contracts/v7',pkg/'contracts/v7'),(root/'contracts/v6',pkg/'contracts/v6'),(root/'tck/v7',pkg/'tck/v7'),(root/'tck/v6',pkg/'tck/v6'),(root/'tck/jcs',pkg/'tck/jcs')]
bad=[]
for a,b in pairs:
    an={p.name:p.read_bytes() for p in a.iterdir() if p.is_file()};bn={p.name:p.read_bytes() for p in b.iterdir() if p.is_file()}
    if an!=bn:bad.append((str(a),str(b),sorted(set(an)^set(bn))))
if bad:
    print('MIRROR MISMATCH',bad);raise SystemExit(1)
print('KristalDiag contract/TCK mirrors: PASS')
