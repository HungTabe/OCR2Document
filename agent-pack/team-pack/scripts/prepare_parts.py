#!/usr/bin/env python3
"""Stages 4 and 6 prep: group repaired pages into questions and split them into parts for the enrich/verify agents.

usage:
  prepare_parts.py enrich --exam NAME [--max 17]   -> work/<exam>/enrich/questions.json + bank_part_K.json
  prepare_parts.py blind  --exam NAME              -> work/<exam>/enrich/blind_in_K.json (needs enriched_part_K.json)

A question = all repaired pages that carry the same question_number (duplicates are merged, the first page's text is used).
"""
import argparse
import collections
import sys
from lib_pipeline import work_dir, parse_repaired, split_even, write_json, read_json


def group(exam):
    w = work_dir(exam)
    groups = collections.defaultdict(list)
    unknown = []
    for f in sorted((w / 'ocr-fullfill').glob('page_*.md')):
        r = parse_repaired(f.read_text(encoding='utf-8'))
        r['page'] = f.stem.split('_')[1]
        r['file'] = str(f)
        (unknown if r['number'] is None else groups[r['number']]).append(r)
    qs = []
    for n in sorted(groups):
        pg = groups[n]
        conf_rank = {'high': 0, 'medium': 1, 'low': 2}
        worst = max((p['confidence'] for p in pg), key=lambda c: conf_rank.get(c, 2))
        first = pg[0]
        qs.append(dict(number=n, file=first['file'], pages=[p['page'] for p in pg], question=first['stem'],
                       options=first['options'], repair_confidence=first['confidence'] if len(pg) == 1 else worst))
    nxt = (max(groups) if groups else 0) + 1
    for p in unknown:                                   # pages whose number could not be read: one question each
        qs.append(dict(number=nxt, file=p['file'], pages=[p['page']], question=p['stem'], options=p['options'],
                       repair_confidence=p['confidence']))
        nxt += 1
    return qs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('mode', choices=['enrich', 'blind'])
    ap.add_argument('--exam', required=True)
    ap.add_argument('--max', type=int, default=17)
    a = ap.parse_args()
    w = work_dir(a.exam)
    e = w / 'enrich'
    if a.mode == 'enrich':
        qs = group(a.exam)
        if not qs:
            sys.exit('no repaired pages found')
        write_json(e / 'questions.json', qs)
        parts = split_even(qs, a.max)
        for k, part in enumerate(parts):
            write_json(e / f'bank_part_{k}.json', part)
        print(f'{len(qs)} questions -> {len(parts)} parts', [(p[0]['number'], p[-1]['number'], len(p)) for p in parts])
    else:
        qs = {q['number']: q for q in read_json(e / 'questions.json')}
        k = 0
        while (e / f'bank_part_{k}.json').exists():
            part = read_json(e / f'bank_part_{k}.json')
            en = read_json(e / f'enriched_part_{k}.json')
            rows = []
            for q in part:
                x = en[str(q['number'])]
                rows.append(dict(number=q['number'], domain=x['domain'], skill=x['skill'], question=q['question'],
                                 options=q['options'], repair_confidence=q['repair_confidence']))
            write_json(e / f'blind_in_{k}.json', rows)
            k += 1
        print(f'blind inputs written for {k} parts')


if __name__ == '__main__':
    main()
