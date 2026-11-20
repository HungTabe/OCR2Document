# agent-pack / team-pack

Pipeline: `input/` (ảnh) → **OCR** → **text** (sửa/điền) → **enrich** → **question bank** → **bộ file prep** (3 HTML + 1 MD)

```
exam-orchestrator (Sonnet, agent chính)
  1 scan      list_images.py
  2 OCR       ocr-reader × N (Haiku, song song)         -> work/<đề>/ocr/page_NNN.md
  3 text      ocr-repairer × batch (Sonnet)             -> work/<đề>/ocr-fullfill/page_NNN.md   (thay [?], gộp ảnh trùng câu)
  4 group     prepare_parts.py                          (gộp trang cùng câu, chia part)
  5 enrich    question-enricher × part (Sonnet)         -> work/<đề>/enrich/enriched_part_K.json (domain, đáp án, pattern, giải thích EN/VI)
  6 verify    answer-verifier × part (Sonnet, giải mù)  -> work/<đề>/enrich/blind_out_K.json
  7 bank      merge_bank.py                             -> output/<đề>/question_bank.json
  8 modules   (tuỳ chọn) domain-researcher + module-writer
  9 prep      build_prep_pack.py + smoke_check.py       -> output/<đề>/prep/  (Study Guide .md + Quiz, Simulation, Explanatory .html)
```

Mỗi giai đoạn có cổng kiểm tra bằng script (`check_stage.py`); lỗi thì orchestrator ra lệnh lại đúng phần lỗi (tối đa 2 lần). Chạy lại cùng lệnh sẽ **resume**: giai đoạn đã đạt cổng thì bỏ qua.

Chạy:
```
cp ảnh-đề/*.jpg agent-pack/team-pack/input/
agent-pack/team-pack/scripts/run.sh --exam <tên-đề> --profile ccdvp
# hoặc: claude --agent exam-orchestrator "Run the pipeline. EXAM=<tên-đề> PROFILE=ccdvp"
```
(Orchestrator phải là agent chính của phiên vì sub-agent không spawn được sub-agent khác.) Tuỳ chọn của `run.sh`: `--input`, `--exam`, `--profile`, `--mode full|quick`, `--from N`, `--to N`, `--modules reuse|build`.

Cấu trúc: `agents/` (orchestrator + 7 worker; symlink vào `.claude/agents/`), `profiles/<kỳ thi>/` (blueprint, golden rules, research, module học, câu mẫu chính thức; có sẵn `ccdvp`), `templates/` (3 mẫu HTML), `scripts/`, `schema.json` (chế độ quick), `bank_schema.json` (question bank), `work/` (trung gian), `output/` (kết quả cuối).

Thêm kỳ thi mới: xem `profiles/_template/README.md`. Chi tiết đầy đủ ở `README.md` gốc của dự án.
