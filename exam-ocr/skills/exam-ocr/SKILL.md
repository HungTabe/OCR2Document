---
name: exam-ocr
description: Use when the user has a folder of photos/scans of exam papers (đề thi, đề kiểm tra, bài tập) and wants them OCR'd, merged, and turned into a Word/Markdown document. Triggers - "ocr folder ảnh", "gộp đề thi", "tổng hợp đề từ ảnh", "ảnh sang word".
---

# exam-ocr: folder of images -> one exam document

## Workflow

1. **List images** (natural sort, HEIC converted, huge files downscaled):
   ```
   python3 "${CLAUDE_PLUGIN_ROOT}/scripts/list_images.py" "<folder>"
   ```
   It prints one absolute image path per line, in page order, and writes converted copies to `<folder>/.ocr_cache/`.

2. **Transcribe each image** with the Read tool (Claude vision = the OCR). Do pages in order. For each page:
   - Transcribe ALL text faithfully, in Vietnamese with full diacritics. Do not "fix" the teacher's content, do not solve questions, do not add answers unless they appear in the image.
   - Math: use LaTeX, `$...$` inline and `$$...$$` for display. Chemistry/physics units as written.
   - Structure: `#` exam title, `##` sections (Phần I, Câu...), numbered questions, a/b/c/d options as a list, tables as Markdown tables.
   - Figures/diagrams you cannot transcribe: insert `[Hình: <short description>]`.
   - Illegible parts: `[?]` and list them in the report. Never guess silently.
   - Save each page to `<folder>/.ocr_cache/page_NNN.md` right after reading it (so a crash can resume; skip pages whose file already exists).
   - If many images (>10), delegate batches of ~5 pages to parallel subagents that write the page_NNN.md files.

3. **Merge**: concatenate page_*.md in order into `<folder>/<output-name>.md`. Fix questions split across page boundaries, drop repeated headers/footers, keep question numbering continuous. If the images clearly hold several different exams, split into one file per exam.

4. **Convert to Word**:
   ```
   python3 "${CLAUDE_PLUGIN_ROOT}/scripts/md_to_docx.py" "<folder>/<output-name>.md" "<folder>/<output-name>.docx"
   ```
   Uses pandoc if installed (LaTeX becomes real Word equations); otherwise python-docx (`pip3 install python-docx`). Install whichever is missing, preferably `brew install pandoc`.

5. **Report**: output paths, page count, number of questions found, and the list of `[?]` / `[Hình]` spots the teacher should double-check.

## Rules
- Never overwrite an existing output file; add a `-v2` suffix instead.
- Keep student-facing content free of the OCR notes; put notes only in the chat report.
