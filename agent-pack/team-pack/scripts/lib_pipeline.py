#!/usr/bin/env python3
"""Shared helpers for the exam-prep harness (profiles, paths, repaired-page parsing)."""
import json
import re
import sys
from pathlib import Path

TEAM = Path(__file__).resolve().parent.parent          # .../agent-pack/team-pack
NOTES_MARK = '---REPAIR-NOTES---'
REL_BY_CONF = {'high': 'ok', 'medium': 'partial', 'low': 'incomplete'}


def load_profile(name):
    """Load profiles/<name>/profile.json (or a profile directory path)."""
    p = Path(name)
    if not p.is_dir():
        p = TEAM / 'profiles' / name
    f = p / 'profile.json'
    if not f.exists():
        sys.exit(f'profile not found: {f}')
    prof = json.load(open(f, encoding='utf-8'))
    prof['_dir'] = p
    return prof


def work_dir(exam):
    return TEAM / 'work' / exam


def out_dir(exam):
    return TEAM / 'output' / exam


def read_json(path):
    return json.load(open(path, encoding='utf-8'))


def write_json(path, obj):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(obj, ensure_ascii=False, indent=1), encoding='utf-8')


NUM_PATTERNS = [r'Question\s+(\d+)\s+of', r'Câu\s*(?:hỏi\s*)?(\d+)\b', r'Question\s+(\d+)\b']


def guess_number(text):
    """Question number written on a page (from OCR text), or None."""
    head = '\n'.join(text.splitlines()[:6])
    for pat in NUM_PATTERNS:
        m = re.search(pat, head, re.I)
        if m:
            return int(m.group(1))
    return None


def parse_repaired(text):
    """Split a repaired page into number / stem / options / notes."""
    body, _, notes = text.partition(NOTES_MARK)
    body = body.strip()
    body = re.sub(r'^(?:Question|Câu)\s*\d+(?:\s*of\s*\d+)?\s*', '', body, count=1, flags=re.I)
    m = re.search(r'^A\. ', body, re.M)
    stem, options = (body[:m.start()].strip(), {}) if m else (body, {})
    if m:
        for o, nxt in zip('ABCD', ['B', 'C', 'D', None]):
            pat = rf'^{o}\. (.*?)(?=^{nxt}\. |\Z)' if nxt else rf'^{o}\. (.*)\Z'
            mo = re.search(pat, body, re.M | re.S)
            if mo:
                options[o] = mo.group(1).strip()
    nm = re.search(r'question_number:\s*([^\s\n]+)', notes)
    cm = re.search(r'confidence:\s*(\w+)', notes)
    sm = re.search(r'same_question_as:\s*(.*)', notes)
    number = None
    if nm:
        try:
            number = int(nm.group(1))
        except ValueError:
            number = None
    return dict(number=number, stem=stem, options=options,
                confidence=(cm.group(1).lower() if cm else 'low'),
                same=(sm.group(1).strip() if sm else ''), has_notes=bool(notes.strip()), body=body)


def reliability(confidence, source='bank'):
    if source == 'official-sample':
        return 'official'
    return REL_BY_CONF.get(confidence, 'incomplete')


def split_even(items, max_size):
    """Split a list into the fewest parts of at most max_size, sizes balanced."""
    n = len(items)
    if n == 0:
        return []
    k = -(-n // max_size)
    base, extra = divmod(n, k)
    out, i = [], 0
    for j in range(k):
        s = base + (1 if j < extra else 0)
        out.append(items[i:i + s])
        i += s
    return out
