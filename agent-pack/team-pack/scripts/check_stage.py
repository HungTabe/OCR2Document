#!/usr/bin/env python3
"""Deterministic gate after each agent stage. Exit 0 = OK, 1 = problems (printed one per line, quotable to the agent).

usage: check_stage.py STAGE --exam NAME [--profile ccdvp]
  ocr      every work/<exam>/ocr/page_NNN.md exists and is not empty
  repair   every ocr-fullfill page exists, has no [?] in the body, has A-D options and REPAIR-NOTES with a question number
  enrich   enriched_part_K.json valid + complete for every question of part K
  blind    blind_out_K.json valid + complete for every question of part K
"""
import argparse
import json
import sys
from lib_pipeline import work_dir, load_profile, read_json, parse_repaired, NOTES_MARK


def err(errors, msg):
    errors.append(msg)


def check_ocr(w, errors):
    imgs = [l for l in open(w / 'images.txt', encoding='utf-8') if l.strip()]
    for i in range(1, len(imgs) + 1):
        f = w / 'ocr' / f'page_{i:03d}.md'
        if not f.exists():
            err(errors, f'MISSING ocr page_{i:03d}.md')
        elif not f.read_text(encoding='utf-8').strip():
            err(errors, f'EMPTY ocr page_{i:03d}.md')


def check_repair(w, errors):
    batches = read_json(w / 'repair' / 'batches.json')
    for b in batches:
        for p in b:
            f = w / 'ocr-fullfill' / f"page_{p['page']}.md"
            name = f.name
            if not f.exists():
                err(errors, f'MISSING {name}')
                continue
            t = f.read_text(encoding='utf-8')
            body = t.partition(NOTES_MARK)[0]
            if '[?]' in body:
                err(errors, f'{name}: still contains [?] in the question text')
            r = parse_repaired(t)
            if not r['has_notes']:
                err(errors, f'{name}: REPAIR-NOTES block missing')
            if r['number'] is None:
                err(errors, f'{name}: question_number missing or not a number in REPAIR-NOTES')
            missing = [o for o in 'ABCD' if o not in r['options']]
            if missing:
                err(errors, f"{name}: options missing {','.join(missing)} (format must be lines starting 'A. ', 'B. ', 'C. ', 'D. ')")
            if len(r['stem']) < 20:
                err(errors, f'{name}: question text too short')
    # duplicates of the same question must hold identical text
    seen = {}
    for b in batches:
        for p in b:
            f = w / 'ocr-fullfill' / f"page_{p['page']}.md"
            if f.exists():
                r = parse_repaired(f.read_text(encoding='utf-8'))
                if r['number'] is not None:
                    seen.setdefault(r['number'], []).append((f.name, r['stem'] + json.dumps(r['options'], sort_keys=True)))
    for n, lst in seen.items():
        if len({x[1] for x in lst}) > 1:
            err(errors, f'question {n}: pages {", ".join(x[0] for x in lst)} are the same question but their repaired text differs; use one merged text')


def part_numbers(w, k):
    return [str(q['number']) for q in read_json(w / 'enrich' / f'bank_part_{k}.json')]


def check_enrich(w, errors, prof, k):
    f = w / 'enrich' / f'enriched_part_{k}.json'
    if not f.exists():
        return err(errors, f'MISSING {f.name}')
    try:
        d = read_json(f)
    except Exception as e:
        return err(errors, f'{f.name}: invalid JSON ({e})')
    part = {str(q['number']): q for q in read_json(w / 'enrich' / f'bank_part_{k}.json')}
    nrules = len(read_json(prof['_dir'] / prof['files']['golden_rules']))
    doms = set(prof['domains'])
    for n, q in part.items():
        x = d.get(n)
        if x is None:
            err(errors, f'{f.name}: question {n} missing')
            continue
        for key in ['domain', 'skill', 'correct', 'answer_review', 'pattern', 'signals', 'why_wins', 'why_others', 'rules', 'research_read']:
            if key not in x:
                err(errors, f'{f.name} q{n}: field "{key}" missing')
        if str(x.get('domain')) not in doms:
            err(errors, f'q{n}: domain {x.get("domain")} not in profile domains {sorted(doms)}')
        corr = x.get('correct') or []
        if not corr or any(c not in q['options'] for c in corr):
            err(errors, f'q{n}: "correct" must be letters present in the options, got {corr}')
        for key in ['pattern', 'signals', 'why_wins']:
            v = x.get(key) or {}
            if not (isinstance(v, dict) and v.get('en') and v.get('vi')):
                err(errors, f'q{n}: "{key}" needs non-empty "en" and "vi"')
        wo = x.get('why_others') or {}
        for o in q['options']:
            if o not in corr and not (isinstance(wo.get(o), dict) and wo[o].get('en') and wo[o].get('vi')):
                err(errors, f'q{n}: why_others missing for wrong option {o}')
        for r in x.get('rules') or []:
            if not isinstance(r, int) or not 1 <= r <= nrules:
                err(errors, f'q{n}: rule id {r} outside 1..{nrules}')
        if not x.get('rules'):
            err(errors, f'q{n}: "rules" is empty')
        if (x.get('answer_review') or {}).get('verdict') not in ('confident', 'uncertain'):
            err(errors, f'q{n}: answer_review.verdict must be "confident" or "uncertain"')
        if not x.get('research_read'):
            err(errors, f'q{n}: "research_read" is empty; Read the profile research files before answering')


def check_blind(w, errors, k):
    f = w / 'enrich' / f'blind_out_{k}.json'
    if not f.exists():
        return err(errors, f'MISSING {f.name}')
    try:
        d = read_json(f)
    except Exception as e:
        return err(errors, f'{f.name}: invalid JSON ({e})')
    opts = {str(q['number']): q['options'] for q in read_json(w / 'enrich' / f'bank_part_{k}.json')}
    for n, o in opts.items():
        x = d.get(n)
        if x is None:
            err(errors, f'{f.name}: question {n} missing')
        elif x.get('answer') not in o:
            err(errors, f'q{n}: "answer" must be one letter present in the options, got {x.get("answer")}')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('stage', choices=['ocr', 'repair', 'enrich', 'blind'])
    ap.add_argument('--exam', required=True)
    ap.add_argument('--profile', default='ccdvp')
    ap.add_argument('--part', type=int, default=None)
    a = ap.parse_args()
    w = work_dir(a.exam)
    errors = []
    if a.stage == 'ocr':
        check_ocr(w, errors)
    elif a.stage == 'repair':
        check_repair(w, errors)
    else:
        prof = load_profile(a.profile) if a.stage == 'enrich' else None
        parts = [a.part] if a.part is not None else sorted(int(p.stem.split('_')[-1]) for p in (w / 'enrich').glob('bank_part_*.json'))
        for k in parts:
            (check_enrich(w, errors, prof, k) if a.stage == 'enrich' else check_blind(w, errors, k))
    if errors:
        print('\n'.join(errors))
        sys.exit(1)
    print(f'OK {a.stage}')


if __name__ == '__main__':
    main()
