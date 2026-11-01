#!/usr/bin/env python3
"""Verify provenance and core numerical reproduction; run from any working directory."""
from pathlib import Path
import csv, json, hashlib, math
ROOT=Path(__file__).resolve().parents[1]
sha=lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
manifest=json.loads((ROOT/'SHA256SUMS.json').read_text(encoding='utf-8'))
for rel,expected in manifest.items():
    assert sha(ROOT/rel)==expected, f'Hash divergiu: {rel}'
with (ROOT/'dados/m.csv').open(newline='',encoding='utf-8-sig') as f:
    rows=list(csv.DictReader(f))
assert len(rows)==5571, len(rows)
assert len({r['ibge_code'] for r in rows})==5571
stats=json.loads((ROOT/'resultados/resultados.json').read_text(encoding='utf-8'))
assert sha(ROOT/'dados/m.csv')==stats['raw_sha256']
assert sum(int(float(r['empregos_formais'])) for r in rows)==60688704
assert math.isclose(stats['correlations']['pearson_raw'],.760,abs_tol=.001)
assert math.isclose(stats['correlations']['pearson_partial_logjobs_UF'],.565,abs_tol=.001)
print('OK: hashes, 5.571 códigos, estoque interno e resultados de referência.')
print('Nota: isto não valida a conciliação do total com o MTE.')
