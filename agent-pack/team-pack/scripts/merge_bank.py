#!/usr/bin/env python3
"""Stage 7: merge repaired questions + enrichment + blind verification (+ the profile's official samples) into the question bank.

usage: merge_bank.py --exam NAME --profile ccdvp
writes: work/<exam>/bank/question_bank.json   and   output/<exam>/question_bank.json
        work/<exam>/bank/report.json           (domain counts, reliability, blind-vs-enrich disagreements)
Every non-official item keeps needs_review=true (answers are not from an official key).
"""
import argparse
import collections
from lib_pipeline import load_profile, work_dir, out_dir, read_json, write_json, reliability

FIELDS = ['id', 'ref', 'source', 'domain', 'skill', 'question', 'options', 'correct', 'pattern', 'signals', 'why_wins',
          'why_others', 'rules', 'answer_review', 'repair_confidence', 'blind_agrees', 'blind_confidence',
          'blind_answer', 'source_pages', 'reliability', 'needs_review']


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--exam', required=True)
    ap.add_argument('--profile', default='ccdvp')
    a = ap.parse_args()
    prof = load_profile(a.profile)
    w = work_dir(a.exam)
    e = w / 'enrich'
    qs = {str(q['number']): q for q in read_json(e / 'questions.json')}
    enriched, blind = {}, {}
    k = 0
    while (e / f'enriched_part_{k}.json').exists():
        enriched.update(read_json(e / f'enriched_part_{k}.json'))
        if (e / f'blind_out_{k}.json').exists():
            blind.update(read_json(e / f'blind_out_{k}.json'))
        k += 1
    items, disagree = [], []
    for n in sorted(qs, key=int):
        q, x = qs[n], enriched[n]
        b = blind.get(n)
        correct = sorted(x['correct'])
        agrees = (b['answer'] in correct) if b else None
        review = dict(x['answer_review'])
        if b is not None and not agrees:
            review = dict(verdict='uncertain', note=f"Independent re-solve chose {b['answer']} instead of {','.join(correct)}. {review.get('note', '')}".strip())
            disagree.append(dict(number=int(n), enriched=correct, blind=b['answer'], runner_up=b.get('runner_up'), reason=b.get('reason')))
        items.append(dict(id=int(n), ref=f'Bank Q{n}', source='bank', domain=int(x['domain']), skill=x['skill'],
                          question=q['question'], options=q['options'], correct=correct, pattern=x['pattern'],
                          signals=x['signals'], why_wins=x['why_wins'], why_others=x['why_others'],
                          rules=[int(r) for r in x['rules']], answer_review=review,
                          repair_confidence=q['repair_confidence'], blind_agrees=agrees,
                          blind_confidence=(b or {}).get('confidence'), blind_answer=(b or {}).get('answer'),
                          source_pages=q['pages'], reliability=reliability(q['repair_confidence']), needs_review=True))
    sp = prof['_dir'] / prof['files']['official_samples']
    if sp.exists():
        for s in read_json(sp):
            s = dict(s)
            s.update(source='official-sample', repair_confidence='high', blind_agrees=True, blind_confidence='high',
                     blind_answer=None, source_pages=[], reliability='official', needs_review=False)
            items.append({k: s.get(k) for k in FIELDS})
    bank = dict(exam=prof['name'], profile=prof['code'], total=len(items),
                note='Self-collected practice items plus the official samples. Keyed answers of self-collected items are working answers, not verified against an official answer key.',
                items=items)
    write_json(w / 'bank' / 'question_bank.json', bank)
    write_json(out_dir(a.exam) / 'question_bank.json', bank)
    rep = dict(total=len(items),
               by_domain=dict(sorted(collections.Counter(i['domain'] for i in items).items())),
               by_reliability=dict(collections.Counter(i['reliability'] for i in items)),
               blind_checked=sum(1 for i in items if i['blind_agrees'] is not None and i['source'] == 'bank'),
               disagreements=disagree)
    write_json(w / 'bank' / 'report.json', rep)
    print(f"bank: {len(items)} items | by_domain {rep['by_domain']} | reliability {rep['by_reliability']} | disagreements {len(disagree)}")
    for d in disagree:
        print('  DISAGREE', d)


if __name__ == '__main__':
    main()
