#!/usr/bin/env python3
"""Validate an exam JSON produced by qa-extractor. Exit 0 = OK, 1 = errors (printed)."""
import json, sys
TYPES = {"multiple_choice", "true_false", "short_answer", "essay"}
SRC = {"key_in_document", "solved_by_model", "missing"}

def main():
    path = sys.argv[1]
    errs = []
    try:
        d = json.load(open(path, encoding="utf-8"))
    except Exception as e:
        print(f"INVALID JSON: {e}"); sys.exit(1)
    for k in ("exam_title", "source_pages", "questions"):
        if k not in d: errs.append(f"missing top-level '{k}'")
    qs = d.get("questions") or []
    if not qs: errs.append("questions is empty")
    for i, q in enumerate(qs):
        t = f"questions[{i}]"
        for k in ("number", "type", "question", "correct_answer", "answer_source", "needs_review"):
            if k not in q: errs.append(f"{t} missing '{k}'")
        if q.get("type") not in TYPES: errs.append(f"{t}.type invalid: {q.get('type')}")
        if q.get("answer_source") not in SRC: errs.append(f"{t}.answer_source invalid")
        if not str(q.get("question", "")).strip(): errs.append(f"{t}.question empty")
        if q.get("type") == "multiple_choice" and not q.get("options"): errs.append(f"{t} multiple_choice without options")
        if q.get("answer_source") != "key_in_document" and q.get("needs_review") is not True:
            errs.append(f"{t} must have needs_review=true when answer_source != key_in_document")
        if q.get("answer_source") == "missing" and q.get("correct_answer") is not None:
            errs.append(f"{t} answer_source=missing requires correct_answer=null")
    if errs:
        print("\n".join(errs)); sys.exit(1)
    print(f"OK: {len(qs)} questions, {sum(1 for q in qs if q['needs_review'])} need review")

if __name__ == "__main__":
    main()
