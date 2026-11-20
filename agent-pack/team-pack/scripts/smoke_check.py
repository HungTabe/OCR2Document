#!/usr/bin/env python3
"""Stage 9 gate: sanity-check the generated prep pack. Exit 0 = OK, 1 = problems.

usage: smoke_check.py --exam NAME --profile ccdvp [--out DIR]
checks: the 4 files exist; every <script> block parses (node --check, when node is installed); no leftover HTML entities;
        none of the profile's banned terms (pipeline internals) appear; the Explanatory page has one article per bank item;
        the Study Guide has a heading for every domain.
"""
import argparse
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from lib_pipeline import load_profile, out_dir, work_dir, read_json


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--exam', required=True)
    ap.add_argument('--profile', default='ccdvp')
    ap.add_argument('--out')
    a = ap.parse_args()
    prof = load_profile(a.profile)
    code = prof['code']
    d = Path(a.out) if a.out else out_dir(a.exam) / 'prep'
    names = [f'{code}_Study_Guide.md', f'{code}_Interactive_Quiz.html', f'{code}_Exam_Simulation.html', f'{code}_Explanatory_Interactive_Study.html']
    errors = []
    texts = {}
    for n in names:
        f = d / n
        if not f.exists():
            errors.append(f'MISSING {n}')
        else:
            texts[n] = f.read_text(encoding='utf-8')
    bank = read_json(work_dir(a.exam) / 'bank' / 'question_bank.json')
    total = bank['total']
    node = shutil.which('node')
    banned = [re.compile(re.escape(b), re.I) for b in prof.get('banned_terms', [])]
    for n, t in texts.items():
        for pat in banned:
            hits = pat.findall(t)
            if hits:
                errors.append(f'{n}: banned term "{hits[0]}" appears {len(hits)}x')
        for ent in ('&#x27;', '&amp;#', '&amp;quot'):
            if ent in t:
                errors.append(f'{n}: leftover entity {ent} x{t.count(ent)}')
        if n.endswith('.html') and node:
            for i, sc in enumerate(re.findall(r'<script>(.*?)</script>', t, re.S)):
                with tempfile.NamedTemporaryFile('w', suffix='.js', delete=False, encoding='utf-8') as tf:
                    tf.write(sc)
                r = subprocess.run([node, '--check', tf.name], capture_output=True, text=True)
                Path(tf.name).unlink(missing_ok=True)
                if r.returncode:
                    errors.append(f'{n}: JS syntax error in script {i}: {r.stderr.strip()[:160]}')
    ex = texts.get(f'{code}_Explanatory_Interactive_Study.html', '')
    if ex and len(re.findall(r'<article class="q"', ex)) != total:
        errors.append(f'Explanatory has {len(re.findall(r"<article class=.q.", ex))} articles, bank has {total}')
    for fn in (f'{code}_Interactive_Quiz.html', f'{code}_Exam_Simulation.html'):
        t = texts.get(fn, '')
        if t:
            m = re.search(r'const RAW_DATA = (\[.*?\]);\n', t, re.S)
            if not m or t.count('"correct":') < total:
                errors.append(f'{fn}: RAW_DATA missing or has fewer than {total} items')
    gd = texts.get(f'{code}_Study_Guide.md', '')
    for k, v in prof['domains'].items():
        if gd and not re.search(rf'^## {k}\. ', gd, re.M):
            errors.append(f'Study Guide: heading for domain {k} missing')
    if not node:
        print('note: node not installed, JS syntax not checked')
    if errors:
        print('\n'.join(errors))
        sys.exit(1)
    print(f'OK smoke: 4 files, {total} items')


if __name__ == '__main__':
    main()
