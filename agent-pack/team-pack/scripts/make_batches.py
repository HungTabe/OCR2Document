#!/usr/bin/env python3
"""Stage 3 prep: build the repair manifest from the OCR pages.

usage: make_batches.py --exam NAME [--size 8]
reads : work/<exam>/images.txt (one image path per line, page order) and work/<exam>/ocr/page_NNN.md
writes: work/<exam>/repair/batches.json   (list of batches; every page carries image, ocr, out, num, siblings)

Pages that show the same question number (the same question photographed more than once) are kept in the
same batch and listed as `siblings`, so the repairer can fill gaps in one page from another.
"""
import argparse
from lib_pipeline import work_dir, guess_number, write_json


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--exam', required=True)
    ap.add_argument('--size', type=int, default=8)
    a = ap.parse_args()
    w = work_dir(a.exam)
    imgs = [l.strip() for l in open(w / 'images.txt', encoding='utf-8') if l.strip()]
    pages = []
    for i, img in enumerate(imgs, 1):
        n = f'{i:03d}'
        f = w / 'ocr' / f'page_{n}.md'
        text = f.read_text(encoding='utf-8') if f.exists() else ''
        pages.append(dict(page=n, image=img, ocr=str(f), out=str(w / 'ocr-fullfill' / f'page_{n}.md'),
                          num=guess_number(text)))
    numbered = [p for p in pages if p['num'] is not None]
    if len(numbered) < len(pages) / 2:            # exam without visible numbering: keep page order
        for p in pages:
            p['num'] = None
        ordered = pages
        unknown = []
    else:
        ordered = sorted(numbered, key=lambda p: (p['num'], p['page']))
        unknown = [p for p in pages if p['num'] is None]
    batches, cur = [], []
    for p in ordered:
        if len(cur) >= a.size and (p['num'] is None or cur[-1]['num'] != p['num']):
            batches.append(cur)
            cur = []
        cur.append(p)
    cur += unknown
    if cur:
        batches.append(cur)
    for b in batches:
        for p in b:
            p['siblings'] = [q['ocr'] for q in b if p['num'] is not None and q['num'] == p['num'] and q['page'] != p['page']]
    (w / 'ocr-fullfill').mkdir(parents=True, exist_ok=True)
    write_json(w / 'repair' / 'batches.json', batches)
    print(f'{len(pages)} pages -> {len(batches)} batches; unknown-number pages: {len(unknown)}')
    for k, b in enumerate(batches):
        print(k, [(p['page'], p['num']) for p in b])


if __name__ == '__main__':
    main()
