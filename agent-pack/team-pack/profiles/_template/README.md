# Exam profile template

A **profile** tells the harness what exam the photos belong to: which domains and skills exist, which Golden Rules to apply, what the research notes say and how to present the prep pack. One profile per exam. The built-in example is `../ccdvp/` (Claude Certified Developer – Professional).

```
profiles/<name>/
├── profile.json          exam identity + domains + file map (see below)
├── blueprint.md          official blueprint: domains, weights, skills (skill names are copied verbatim into the bank)
├── golden_rules.json     [{"id": 1, "domain": 2, "en": "...", "vi": "..."}, ...]  ids must be 1..N
├── research/             one fact sheet per domain group (used by question-enricher and answer-verifier)
├── guide/                hand-written or generated Study Guide parts (head, modules, traps, plan, refs)
└── official_samples.json official sample questions, same fields as a bank item (optional)
```

## profile.json

| Field | Meaning |
|---|---|
| `code` | short code used in file names, e.g. `CCDV-P` -> `CCDV-P_Study_Guide.md` |
| `name`, `exam_code`, `kicker`, `title_short`, `guide_label` | texts shown in the HTML pages and footers |
| `items`, `scored_items`, `minutes`, `pass_scaled`, `readiness_percent` | exam facts shown in the simulation |
| `domains` | `{"1": {"en": "...", "vi": "...", "weight": 17, "quota": 12}, ...}`; `quota` = items per domain in the weighted simulation set |
| `files` | `blueprint`, `golden_rules`, `research_dir`, `official_samples` |
| `research_files` | domain -> research file (read by the enricher/verifier) |
| `research_groups` | `[{"domains": [3, 4], "file": "d3_d4.md"}]` used when `MODULES=build` |
| `guide` | `head`, `modules` (ordered list), `traps`, `plan`, `refs`, `golden_section`, `bank_map_section`; omit the whole key to get an auto-generated digest instead |
| `banned_terms` | words that must not appear in the generated prep pack (checked by `smoke_check.py`) |

## Create a profile for another exam

1. Copy `../ccdvp/` to `profiles/<name>/` and edit `profile.json`, `blueprint.md`, `golden_rules.json`; delete `research/` and `guide/`; remove `official_samples.json` if you have none.
2. Run once with `--modules build`: `domain-researcher` writes `research/*.md` (web research with sources) and `module-writer` writes `guide/*.md`. Review them, add `head.md`, `traps.md`, `plan.md`, `refs.md` by hand and set the `guide` key.
3. Run the pipeline with `--profile <name>`.

The harness assumes multiple-choice items with options `A.`–`D.` (the repair stage enforces this format) and an English or bilingual (EN/VI) presentation.
