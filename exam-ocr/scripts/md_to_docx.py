#!/usr/bin/env python3
"""Markdown -> DOCX. Prefers pandoc (LaTeX math -> native Word equations);
falls back to python-docx (headings, paragraphs, lists, tables; math kept as text)."""
import re, shutil, subprocess, sys
from pathlib import Path

def with_pandoc(md, out):
    subprocess.run(["pandoc", str(md), "-f", "markdown+tex_math_dollars", "-o", str(out)], check=True)

def with_python_docx(md, out):
    try:
        from docx import Document
    except ImportError:
        sys.exit("Need pandoc (brew install pandoc) or python-docx (pip3 install python-docx)")
    doc = Document()
    lines = Path(md).read_text(encoding="utf-8").splitlines()
    i = 0
    while i < len(lines):
        ln = lines[i].rstrip()
        if not ln:
            i += 1; continue
        if ln.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                if not re.match(r"^\|[\s:\-|]+\|?$", lines[i]):
                    rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            t = doc.add_table(rows=len(rows), cols=max(len(r) for r in rows)); t.style = "Table Grid"
            for r, row in enumerate(rows):
                for c, txt in enumerate(row):
                    t.cell(r, c).text = txt
            continue
        m = re.match(r"^(#{1,4})\s+(.*)", ln)
        if m:
            doc.add_heading(m.group(2), level=len(m.group(1)))
        elif re.match(r"^\s*[-*]\s+", ln):
            doc.add_paragraph(re.sub(r"^\s*[-*]\s+", "", ln), style="List Bullet")
        else:
            p = doc.add_paragraph()
            for part in re.split(r"(\*\*[^*]+\*\*)", ln):
                if part.startswith("**") and part.endswith("**"):
                    p.add_run(part[2:-2]).bold = True
                else:
                    p.add_run(part)
        i += 1
    doc.save(out)

def main():
    if len(sys.argv) < 3:
        sys.exit("usage: md_to_docx.py in.md out.docx")
    md, out = sys.argv[1], sys.argv[2]
    (with_pandoc if shutil.which("pandoc") else with_python_docx)(md, out)
    print(out)

if __name__ == "__main__":
    main()
