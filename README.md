<div align="center">

# OCR2Document

**Turn a folder of exam-paper photos into a verified-by-design question bank and a ready-to-use exam-prep pack — with a team of Claude agents.**

Photos → OCR → repaired text → enriched questions → question bank → Study Guide + Quiz + Exam Simulation + Explanatory Study.

![Claude Code agents](https://img.shields.io/badge/Claude%20Code-agent%20team-d97757)
![OCR: Haiku](https://img.shields.io/badge/OCR-Haiku-555)
![Enrich: Sonnet](https://img.shields.io/badge/repair%20%2B%20enrich-Sonnet-555)
![Output: JSON + HTML + MD](https://img.shields.io/badge/output-JSON%20%2B%203%20HTML%20%2B%20MD-3776ab)

[Why](#why) · [Quick start](#quick-start) · [Pipeline](#pipeline) · [Output](#output) · [Profiles](#exam-profiles) · [Agents](#agents) · [Accuracy](#accuracy) · [Troubleshooting](#troubleshooting)

</div>

---

## Why

Photographing exam papers or practice screens gives dozens of images and no text. Plain OCR struggles with blurred, glared, skewed photos and returns a wall of text, not something a learner can study from. Worse, the same question is often photographed several times, each photo missing different words.

OCR2Document chains the steps into one harness:

| | |
|---|---|
| **Automatic** | Drop images in `input/`, run one command. |
| **Repairs, not just reads** | Gaps (`[?]`, cut words) are filled from the photo, from other photos of the **same question**, and from context. Every filled span is recorded. |
| **Enriched** | Each question gets a domain/skill, a keyed answer, an exam pattern and bilingual (EN/VI) explanations for every option. |
| **Cross-checked** | A second agent re-solves every question **blind**; disagreements are flagged, never silently resolved. |
| **Gated** | After every stage a script checks the files. The orchestrator re-issues only what failed (max 2 times) and can **resume** a half-finished run. |
| **Prep pack** | The bank is turned into a Study Guide (`.md`) and three interactive pages (`.html`). |

Two ways to use the repo: the **agent team** in `agent-pack/` (main path) or the **`exam-ocr` plugin** (single skill, Word output).

## Quick start

**Requirements:** [Claude Code](https://docs.claude.com/en/docs/claude-code), Python 3, `sips` (macOS) or Pillow for HEIC/WEBP conversion, Node.js (optional, used by the final JS syntax check).

Put the photos in the input folder (one exam per folder):

```bash
cp ~/Desktop/my-exam/*.jpg agent-pack/team-pack/input/
```

Run the whole pipeline (headless):

```bash
agent-pack/team-pack/scripts/run.sh --exam my-exam --profile ccdvp
```

or from the project root with Claude Code directly:

```bash
claude --agent exam-orchestrator "Run the pipeline. EXAM=my-exam PROFILE=ccdvp"
```

or inside a normal session: `/run-exam-team EXAM=my-exam PROFILE=ccdvp`.

> The orchestrator has to be the **main agent** of the session (`--agent`). Sub-agents in Claude Code cannot spawn other sub-agents, so it cannot be one itself.

`run.sh` options:

| Option | Default | Meaning |
|---|---|---|
| `--input DIR` | `agent-pack/team-pack/input` | folder with the images |
| `--exam NAME` | `de` | name of the work/output folders |
| `--profile NAME` | `ccdvp` | exam profile under `profiles/` |
| `--mode full\|quick` | `full` | `quick` = OCR + one `qa-extractor` → simple JSON only |
| `--from N` / `--to N` | `1` / `10` | stage range |
| `--modules reuse\|build` | `reuse` | `build` = web research + new Study Guide modules (needs web access) |

**Resume:** run the same command again. Every stage first runs its gate; stages that already pass are skipped.

## Pipeline

```text
input/ ──► exam-orchestrator (Sonnet, main agent)
   1 scan      list_images.py ............ natural order, HEIC/WEBP -> JPG
   2 OCR       ocr-reader × N (Haiku) ..... work/<exam>/ocr/page_NNN.md                gate: check_stage ocr
   3 text      ocr-repairer × batches (Sonnet): fill every [?], merge photos of the
               same question ............. work/<exam>/ocr-fullfill/page_NNN.md        gate: check_stage repair
   4 group     prepare_parts.py .......... one entry per question (duplicates merged)
   5 enrich    question-enricher × parts (Sonnet): domain, skill, answer,
               exam pattern, EN/VI explanations ... work/<exam>/enrich/enriched_part_K.json   gate: check_stage enrich
   6 verify    answer-verifier × parts (Sonnet): blind re-solve ... enrich/blind_out_K.json   gate: check_stage blind
   7 bank      merge_bank.py ............. output/<exam>/question_bank.json
   8 modules   (optional) domain-researcher + module-writer: web research -> Study Guide modules
   9 prep pack build_prep_pack.py + smoke_check.py ... output/<exam>/prep/ (3 HTML + 1 MD)
  10 report    counts, reliability, disagreements, failures
```

1. **Scan.** `list_images.py` sorts images naturally (`img2` before `img10`) and converts HEIC/WEBP/TIFF to JPG in `.ocr_cache/`.
2. **OCR.** One `ocr-reader` per image, all in the same turn, with a fixed absolute command (`IMAGE`, `OUT`). It transcribes only; it never solves or corrects. `[?]` marks unreadable text.
3. **Text (repair).** `make_batches.py` groups pages by the question number printed on them, so photos of the same question stay in one batch and become each other's `siblings`. An `ocr-repairer` reads the image, the old OCR and the siblings and writes a complete page plus a `REPAIR-NOTES` block (`question_number`, `confidence`, what came from the image, from a sibling, or was inferred). Duplicates must end with identical text.
4. **Group.** Pages with the same question number become one question; parts of at most 17 questions are cut for the next agents.
5. **Enrich.** A `question-enricher` must read the profile's blueprint, Golden Rules and the research notes of the domains it assigns, then writes for each question: domain, skill, keyed answer, `pattern` ("When X → choose Y because Z"), key signals, why the answer wins, why every wrong option loses (EN + VI) and the Golden Rules triggered.
6. **Verify.** An `answer-verifier` solves the same questions **without seeing** the enricher's answer. `merge_bank.py` compares both; a disagreement downgrades the item to `uncertain` and is listed in the report.
7. **Bank.** `merge_bank.py` writes `question_bank.json` (schema: `bank_schema.json`) and adds the profile's official sample questions.
8. **Modules (optional).** With `--modules build`, `domain-researcher` writes sourced fact sheets and `module-writer` turns them into bilingual Study Guide modules. By default the profile's existing modules are reused.
9. **Prep pack.** `build_prep_pack.py` fills the HTML templates and assembles the Study Guide. `smoke_check.py` then verifies: 4 files exist, every script parses (`node --check`), no leftover HTML entities, none of the profile's banned terms (pipeline internals) leaked, one article per bank item, every domain present in the guide.

### Absolute command

The orchestrator does not negotiate with its workers. Every prompt follows a fixed template with absolute paths:

```text
LỆNH TUYỆT ĐỐI - KHÔNG ĐƯỢC TRÁI.
PROFILE_DIR: /…/profiles/ccdvp
PART: /…/work/<exam>/enrich/bank_part_0.json
OUT:  /…/work/<exam>/enrich/enriched_part_0.json
Thực hiện: theo quy trình của bạn … Chỉ trả lời "DONE <OUT> …" hoặc "FAIL <lý do>".
```

Workers answer with one line (or one line per page). The orchestrator never trusts it: it runs the stage gate and re-issues only failures, quoting the validator's errors verbatim.

## Output

```text
agent-pack/team-pack/output/<exam>/
├── question_bank.json                       questions, options, keyed answers, explanations, domain/skill, reliability flags
└── prep/
    ├── <CODE>_Study_Guide.md                bilingual guide: exam facts, domain modules, traps, Golden Rules, study plan, bank map
    ├── <CODE>_Interactive_Quiz.html         practice by question, instant feedback, filter by domain
    ├── <CODE>_Exam_Simulation.html          timed simulation, flag/navigate, domain breakdown
    └── <CODE>_Explanatory_Interactive_Study.html   pick, then flip: pattern, why each wrong option fails, Golden Rules
```

Intermediate files stay in `work/<exam>/` (`ocr/`, `ocr-fullfill/`, `repair/`, `enrich/`, `bank/`) so every step can be inspected: compare `ocr/page_NNN.md` with `ocr-fullfill/page_NNN.md` and the photo whenever a question looks odd.

### Question bank item

| Field | Meaning |
|---|---|
| `domain`, `skill` | blueprint position (from the profile) |
| `correct` | keyed answer letter(s) |
| `pattern`, `signals`, `why_wins`, `why_others`, `rules` | exam pattern and EN/VI explanations; `rules` = Golden Rule ids |
| `repair_confidence` / `reliability` | how complete the source wording was: `ok`, `partial`, `incomplete` (largely filled in) or `official` |
| `blind_agrees` | independent blind re-solve agrees with the keyed answer |
| `answer_review.verdict` | `confident` or `uncertain` |
| `needs_review` | `true` for every self-collected item: its answer did not come from an official key |

The generated prep pack presents the bank as a **self-collected question bank** and never mentions how it was produced; `incomplete` items carry a visible "provisional" flag.

## Exam profiles

A profile (`agent-pack/team-pack/profiles/<name>/`) holds everything exam-specific: blueprint, Golden Rules, research notes, Study Guide modules and official samples. `ccdvp` (Claude Certified Developer – Professional, 8 domains) is included. To add an exam, copy it and follow [`profiles/_template/README.md`](agent-pack/team-pack/profiles/_template/README.md); `--modules build` can generate the research and modules for you.

## Agents

| Agent | Model | Tools | Job |
|---|---|---|---|
| `exam-orchestrator` | Sonnet | `Agent(...)`, Read, Write, Bash, Glob | Runs the stages, gates, re-issues, reports. Never does the content work itself. |
| `ocr-reader` | Haiku | Read, Write | Transcribes one image into one Markdown file. |
| `ocr-repairer` | Sonnet | Read, Write | Repairs a batch of pages using the photo, sibling photos and context. |
| `question-enricher` | Sonnet | Read, Write | Domain/skill, keyed answer, pattern and EN/VI explanations for a part. |
| `answer-verifier` | Sonnet | Read, Write | Blind re-solve of the same questions. |
| `domain-researcher` | Sonnet | Read, Write, WebSearch, WebFetch | (optional) Sourced fact sheet for a domain group. |
| `module-writer` | Sonnet | Read, Write | (optional) Bilingual Study Guide module from a fact sheet. |
| `qa-extractor` | Haiku | Read, Write | Quick mode only: OCR files → simple JSON. |

Agent definitions live in `agent-pack/team-pack/agents/` and are symlinked into `.claude/agents/`.

## Accuracy

1. **OCR and repair are limited by the photos.** Glare, blur and tiny text are where Haiku slips; the repairer can only fill a gap from another photo of the same question or by inference. Inferred spans are listed in each page's `REPAIR-NOTES`; items whose wording was largely inferred are flagged `incomplete` and their answers are provisional.
2. **Keyed answers are AI-derived.** The enricher and the blind verifier are both Claude models; agreement between them is a consistency check, **not** verification against an official answer key. Review every item before using it for real assessment.
3. **Profile facts age.** Research notes and prices were captured on the date written in each module; re-check against live documentation.
4. In a first full run on 76 photos of a 70-question practice screen the harness produced 67 distinct questions; 30 of them were `incomplete` and the three official samples were added by the profile.

## Privacy and acceptable use

The images are read by Claude, so their content is sent to Anthropic's API like any Claude Code conversation (and web pages are fetched in `--modules build`). Do not process photos with personal data unless that is acceptable. `work/` and `output/` stay on your machine.

Use the harness only on material you are allowed to copy and share, such as your own papers or practice sets. Certification exams are usually confidential: do not photograph or redistribute live exam content.

## Repository

| Path | What |
|---|---|
| `agent-pack/team-pack/agents/` | orchestrator and workers |
| `agent-pack/team-pack/scripts/` | `run.sh`, `list_images.py`, `make_batches.py`, `prepare_parts.py`, `check_stage.py`, `merge_bank.py`, `build_prep_pack.py`, `smoke_check.py`, `lib_pipeline.py`, `validate_json.py` (quick mode) |
| `agent-pack/team-pack/profiles/` | exam profiles (`ccdvp`, `_template`) |
| `agent-pack/team-pack/templates/` | HTML page templates (quiz, simulation, explanatory) |
| `agent-pack/team-pack/schema.json`, `bank_schema.json` | quick-mode JSON, question bank |
| `agent-pack/team-pack/input/` · `work/` · `output/` | photos · intermediate files · final files |
| `.claude/agents/`, `.claude/commands/run-exam-team.md` | symlinks to the agents, `/run-exam-team` |
| `exam-ocr/` | the alternative plugin (images → Word) |

## Develop

Run a gate or a stage by hand (replace `de` with your exam name):

```bash
cd agent-pack/team-pack
python3 scripts/check_stage.py repair --exam de
python3 scripts/prepare_parts.py enrich --exam de
python3 scripts/merge_bank.py --exam de --profile ccdvp
python3 scripts/build_prep_pack.py --exam de --profile ccdvp
python3 scripts/smoke_check.py --exam de --profile ccdvp
```

Re-build the prep pack after editing the bank, a profile module or a template; no agent is needed for stages 7 and 9.

## Troubleshooting

- **The orchestrator cannot start workers** — it was not launched with `--agent exam-orchestrator`, so it has no `Agent` tool. Use `scripts/run.sh` or the command in [Quick start](#quick-start).
- **`No images found`** — the photos are not in the input folder, or have an unsupported extension (jpg, png, heic, webp, tiff, bmp).
- **A stage keeps failing** — the orchestrator re-issues each failure twice and then lists it in the report. Read the quoted gate errors; for OCR open the photo (usually blurry or rotated).
- **`repair` gate: options missing / `[?]` left** — the page format must be `A. `…`D. ` lines and no `[?]`; re-run the stage, only failed batches are repeated.
- **A worker wrote to a different path** — workers must use the absolute paths from the command; the gate reports the page as MISSING and the orchestrator re-issues it.
- **`smoke_check` reports a banned term or entity** — a pipeline word leaked into the prep pack; fix the source text in the bank or profile and rebuild (`build_prep_pack.py`).
- **`--modules build` fails on a page** — some documentation sites block automated fetches; the researcher marks those facts `[unverified]`. Review them before use.
- **`ModuleNotFoundError: docx`** (plugin only) — `pip3 install python-docx`, or `brew install pandoc`.

## Alternative: the `exam-ocr` plugin

If you want a **Word document** instead of a question bank, `exam-ocr/` is a Claude Code plugin with one skill. Claude reads each image itself, saves each page, merges them into Markdown and converts it to `.docx`.

```bash
claude --plugin-dir ./exam-ocr
```

```text
/exam-ocr:exam-ocr ~/Desktop/de-thi-toan-9 de-thi-toan-9
```

`pandoc` turns LaTeX into real Word equations; without it the fallback uses `python-docx` and keeps math as text.
