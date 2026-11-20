---
description: OCR a folder of exam images (đề thi) and compile them into one document
argument-hint: <folder-path> [output-name]
allowed-tools: Bash, Read, Write, Edit, Glob
---

Use the `exam-ocr` skill to process the folder `$1` (default: current directory).
Output name: `$2` (default: `de-thi`).
Follow the skill workflow exactly and report the final file paths.
