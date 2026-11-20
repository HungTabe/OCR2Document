#!/usr/bin/env python3
"""Stage 9: build the exam-prep pack (3 HTML + 1 Markdown) from the question bank, the profile and the HTML templates.

usage: build_prep_pack.py --exam NAME --profile ccdvp [--bank PATH] [--out DIR]
writes: <out>/<CODE>_Study_Guide.md
        <out>/<CODE>_Interactive_Quiz.html
        <out>/<CODE>_Exam_Simulation.html
        <out>/<CODE>_Explanatory_Interactive_Study.html
Deliberately says nothing about how the bank was produced: items are presented as a self-collected question bank,
with an "incomplete" flag on items whose source wording was not complete.
"""
import argparse
import html
import json
import re
from lib_pipeline import TEAM, load_profile, work_dir, out_dir, read_json

REL_TEXT = {
    'official': ('Official sample from the Exam Guide.', 'Câu mẫu chính thức từ Exam Guide.'),
    'ok': ('Source wording for this item is complete.', 'Nội dung nguồn của câu này đầy đủ.'),
    'partial': ('Part of the source wording for this item is incomplete; wording may differ slightly from the original.',
                'Một phần nội dung nguồn của câu này chưa đầy đủ; câu chữ có thể lệch nhẹ so với bản gốc.'),
    'incomplete': ('⚠ The source wording for this item is largely incomplete: wording and options may differ from the original, so the keyed answer is provisional.',
                   '⚠ Nội dung nguồn của câu này chưa đầy đủ phần lớn: câu chữ và đáp án có thể khác bản gốc, nên đáp án chỉ mang tính tạm thời.'),
}
VERDICT = {
    'confident': 'Answer review: working answer, not verified against an official answer key.',
    'confirmed': 'Answer review: working answer, not verified against an official answer key.',
    'uncertain': 'Answer review: provisional — the source wording is incomplete or two options are close.',
    'changed': 'Answer review: updated after re-checking.',
}


def rep(text, old, new, count=1):
    assert old in text, f'template pattern not found: {old[:90]!r}'
    return text.replace(old, new, count)


def rep_re(text, pattern, new, flags=re.S):
    assert re.search(pattern, text, flags), f'template regex not found: {pattern[:90]!r}'
    return re.sub(pattern, lambda m: new, text, count=1, flags=flags)


def js_safe(s):
    return s.replace('</', '<\\/')


def esc(x):
    return html.escape(x, quote=True).replace('&#x27;', "'")


def norm(x):
    return re.sub(r'[^a-z0-9]+', ' ', x.lower()).strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--exam', required=True)
    ap.add_argument('--profile', default='ccdvp')
    ap.add_argument('--bank')
    ap.add_argument('--out')
    a = ap.parse_args()
    prof = load_profile(a.profile)
    pdir = prof['_dir']
    code = prof['code']
    bank_path = a.bank or str(work_dir(a.exam) / 'bank' / 'question_bank.json')
    outp = __import__('pathlib').Path(a.out) if a.out else out_dir(a.exam) / 'prep'
    outp.mkdir(parents=True, exist_ok=True)
    items = read_json(bank_path)['items']
    golden = read_json(pdir / prof['files']['golden_rules'])
    GR = {g['id']: g for g in golden}
    D = {int(k): v for k, v in prof['domains'].items()}
    DOMS = sorted(D)
    nq = len(items)
    n_bank = sum(1 for i in items if i['source'] == 'bank')
    n_samples = nq - n_bank
    dom_counts = {d: sum(1 for i in items if i['domain'] == d) for d in DOMS}
    eff = sum(min(D[d]['quota'], dom_counts[d]) for d in DOMS)
    TPL = TEAM / 'templates'

    # ---- RAW_DATA for quiz / simulation
    def explanation_text(it):
        parts = [f"Domain {it['domain']} · {it['skill']}", f"Exam pattern: {it['pattern']['en']}", f"Why it wins: {it['why_wins']['en']}"]
        parts += [f"Why {k} loses: {it['why_others'][k]['en']}" for k in sorted(it['why_others'])]
        parts += ['', f"VI — Exam pattern: {it['pattern']['vi']}", f"VI — Vì sao đáp án đúng thắng: {it['why_wins']['vi']}"]
        parts += [f"VI — Vì sao {k} sai: {it['why_others'][k]['vi']}" for k in sorted(it['why_others'])]
        if it['reliability'] in ('incomplete', 'partial'):
            parts += ['', REL_TEXT[it['reliability']][0], REL_TEXT[it['reliability']][1]]
        return '\n'.join(parts)

    raw = [dict(id=it['id'], ref=it['ref'] + (' · ⚠ incomplete' if it['reliability'] == 'incomplete' else ''), domain=it['domain'],
                question=it['question'], options=it['options'], correct=sorted(it['correct']), explanation=explanation_text(it))
           for it in items]
    RAW_JSON = js_safe(json.dumps(raw, ensure_ascii=False))
    opts_html = '<option value="">All domains</option>' + ''.join(
        f'<option value="{d}">Domain {d}: {html.escape(D[d]["en"], quote=False)} ({D[d]["weight"]}%)</option>' for d in DOMS)
    weights = '/'.join(str(D[d]['weight']) for d in DOMS)
    kicker, title_short = prof['kicker'], prof['title_short']

    # ---- Interactive Quiz
    q = (TPL / 'quiz.html').read_text(encoding='utf-8')
    q = rep(q, '<title>CCAR-P Certified Architect Professional - Practice Quiz</title>', f'<title>{code} {title_short} - Practice Quiz</title>')
    q = rep(q, '<div class="kicker">Claude Certified Architect</div>', f'<div class="kicker">{kicker}</div>')
    q = rep(q, '<h1>CCAR-P Professional Practice Quiz</h1>', f'<h1>{code} Professional Practice Quiz</h1>')
    q = rep(q, '<p>Test your knowledge across all seven official CCAR-P domains</p>',
            f'<p>Test your knowledge across all {len(DOMS)} official {code} domains · Bilingual explanations (EN/VI)</p>')
    q = rep_re(q, r'<div class="num">7</div>(\s*)<div class="label">Domains</div>', f'<div class="num">{len(DOMS)}</div>\n        <div class="label">Domains</div>')
    q = rep_re(q, r'<select id="domain-filter">.*?</select>', f'<select id="domain-filter">{opts_html}</select>')
    q = rep(q, 'Question 1 of 120', f'Question 1 of {nq}')
    q = rep(q, '<footer class="foot">CCAR-P Practice Quiz &middot; Mock questions plus authored practice items &middot; For self-study purposes only</footer>',
            f'<footer class="foot">{code} Practice Quiz &middot; Self-collected question bank (items marked incomplete are provisional) plus {n_samples} official samples &middot; Independent study tool, not affiliated with Anthropic</footer>')
    short = json.dumps({str(d): D[d]['en'] for d in DOMS})
    q = rep(q, "qDomain.textContent = 'Domain ' + q.domain;", f"qDomain.textContent = 'Domain ' + q.domain + ' · ' + ({short})[q.domain];")
    q = rep(q, '</style>', '#hint-text{white-space:pre-line;line-height:1.5}\n</style>')
    q = rep_re(q, r'const RAW_DATA = \[.*?\];\n</script>', 'const RAW_DATA = ' + RAW_JSON + ';\n</script>')
    (outp / f'{code}_Interactive_Quiz.html').write_text(q, encoding='utf-8')

    # ---- Exam Simulation
    s = (TPL / 'simulation.html').read_text(encoding='utf-8')
    s = rep(s, '<title>CCAR-P Certified Architect Professional - Exam Simulation</title>', f'<title>{code} {title_short} - Exam Simulation</title>')
    s = rep(s, '<div class="kicker">Claude Certified Architect</div>', f'<div class="kicker">{kicker}</div>')
    s = rep(s, '<h1>CCAR-P Exam Simulation</h1>', f'<h1>{code} Exam Simulation</h1>')
    s = rep(s, '63 items &middot; 120 minutes &middot; no feedback until you submit', f'up to {prof["items"]} items &middot; {prof["minutes"]} minutes &middot; no feedback until you submit')
    s = rep(s, '<div class="num">63</div><div class="label">Items</div>', f'<div class="num">{eff}</div><div class="label">Items (weighted set)</div>')
    s = rep(s, '<div class="num">120</div><div class="label">Minutes</div>', f'<div class="num">{prof["minutes"]}</div><div class="label">Minutes</div>')
    s = rep(s, '<div class="num">72%</div>', f'<div class="num">{prof["readiness_percent"]}%</div>')
    s = rep(s, '<small>63 items drawn from the whole bank in the official domain weights (17/13/19/16/14/14/7%). Different every attempt.</small>',
            f'<small>{eff} items drawn from the bank in the official domain weights ({weights}%); a domain with fewer bank items than its quota contributes all it has. Different every attempt.</small>')
    s = rep(s, '<strong>Original mock set</strong><small>The 63 mock-exam items in their original order.</small>',
            f'<strong>Full bank in original order</strong><small>All {nq} items ({n_bank} self-collected bank items + {n_samples} official samples) in order.</small>')
    s = rep(s, 'Multiple-response items score only when every required option is chosen.',
            f'Multiple-response items score only when every required option is chosen. On the real exam {prof["items"] - prof["scored_items"]} of {prof["items"]} items are unscored and unmarked, so treat every item as scored. Bank items flagged "incomplete" are provisional.')
    s = rep(s, 'QUESTION 1 OF 63', f'QUESTION 1 OF {nq}')
    s = rep(s, '0 / 63', f'0 / {nq}')
    s = rep(s, '<footer class="foot">CCAR-P Exam Simulation &middot; Independent study tool, not affiliated with Anthropic &middot; For self-study purposes only</footer>',
            f'<footer class="foot">{code} Exam Simulation &middot; Independent study tool, not affiliated with Anthropic &middot; For self-study purposes only</footer>')
    s = rep(s, "q => /^Mock Q/.test(q.ref)", "q => /^Bank Q|^Official Sample/.test(q.ref)")
    blue = json.dumps({str(d): D[d]['quota'] for d in DOMS})
    names = json.dumps({str(d): D[d]['en'] for d in DOMS})
    s = rep_re(s, r'const RAW_DATA = \[.*?\];\nconst BLUEPRINT = .*?\nconst DOMAIN_NAMES = .*?\n</script>',
               'const RAW_DATA = ' + RAW_JSON + f';\nconst BLUEPRINT = {blue};\nconst DOMAIN_NAMES = {names};\n</script>')
    s = rep(s, '</style>', '#question-text{white-space:normal} .review-list{white-space:pre-line}\n</style>')
    (outp / f'{code}_Exam_Simulation.html').write_text(s, encoding='utf-8')

    # ---- Explanatory Study
    e = (TPL / 'explanatory.html').read_text(encoding='utf-8')
    e = rep(e, '<title>CCAR-P Interactive Study – Pattern Explanations</title>', f'<title>{code} Interactive Study – Pattern Explanations</title>')
    cut = e.find('<section class="scenario"')
    prefix, rest = e[:cut], e[cut:]
    suffix = rest[rest.rfind('<p class="foot">'):]
    prefix = rep_re(prefix, r'<section class="hero">.*?</section>',
                    f'<section class="hero"><h1>{code} Scenario and Reasoning Map</h1><p>{nq} question patterns across the {len(DOMS)} official {code} domains: {n_bank} self-collected bank items and {n_samples} official Exam Guide samples.</p>'
                    '<p>Choose an answer first, then flip to reveal why the winning answer wins, why each wrong option fails, the exam pattern and the Golden Rules it triggers (English and Vietnamese). Notes and flags are saved locally in your browser.</p></section>')
    prefix = rep_re(prefix, r'<select id="domain">.*?</select>', f'<select id="domain">{opts_html}</select>')
    prefix = rep_re(prefix, r'<select id="source">.*?</select>',
                    '<select id="source"><option value="">All sources</option><option value="bank">Self-collected question bank</option><option value="sample">Official samples</option></select>')
    prefix = rep(prefix, '<strong id="shownCount">120</strong>', f'<strong id="shownCount">{nq}</strong>')
    prefix = rep_re(prefix, r'<div class="legend-row">.*?</div>',
                    '<div class="legend-row"><span style="background:#ece9ff;color:#5b4bc4">Self-collected question bank</span><span style="background:#ecfdf3;color:#067647">Official Exam Guide sample</span><span style="background:#fff4d6;color:#8a5a00">⚠ incomplete = provisional</span></div>')

    def article(it):
        qid = f'q{it["id"]:03d}'
        rel, corr, rules = it['reliability'], ''.join(sorted(it['correct'])), it['rules']
        search = norm(' '.join([it['question']] + list(it['options'].values()) + [it['skill'], it['pattern']['en'], it['signals']['en']]))
        CORRECT_CLS = ' class="correct"'
        lis = ''.join(f'<li data-option="{k}" role="radio" tabindex="0"{CORRECT_CLS if k in it["correct"] else ""}>'
                      f'<input aria-label="Choose {k}" name="{qid}" type="radio" value="{k}"/><strong>{k}.</strong> {esc(v)}</li>'
                      for k, v in it['options'].items())
        rule_li = ''.join(f'<li>{esc(GR[r]["en"])}<br/><span class="vi">{esc(GR[r]["vi"])}</span></li>' for r in rules)
        rule_span = ''.join(f'<span class="exam-rule" data-rule="{r}">✅ {esc(GR[r]["en"])}</span> ' for r in rules)
        warn = ''
        if rel in ('incomplete', 'partial'):
            warn = f'<p class="rel-warn {rel}">{esc(REL_TEXT[rel][0])}<br/><span class="vi">{esc(REL_TEXT[rel][1])}</span></p>'
        verdict = ('Answer review: official answer key (Exam Guide).' if it['source'] == 'official-sample'
                   else VERDICT.get(it['answer_review']['verdict'], VERDICT['confident']))
        full = f'<p><strong>{esc(it["skill"])}</strong> (Domain {it["domain"]})</p><p>{esc(verdict)}</p>' + warn
        srcname = 'Official Exam Guide sample' if it['source'] == 'official-sample' else 'Self-collected question bank (' + it['ref'] + ')'
        return (
            f'<article class="q" id="{qid}" data-correct="{corr}" data-domain="{it["domain"]}" data-source="{it["source"]}" '
            f'data-rules="{",".join(map(str, rules))}" data-why="{esc(json.dumps(it["why_others"], ensure_ascii=False))}" data-search="{esc(search)}">'
            f'<details><summary><span class="qid">{esc(it["ref"])}{" ⚠" if rel == "incomplete" else ""}</span><span>{esc(it["question"])} </span></summary>'
            f'<div class="body"><ul class="opts">{lis}</ul>'
            '<div class="actions"><button class="reveal" type="button">Flip / Show Answer</button><button class="clear-one" type="button">Clear Selection</button></div>'
            '<div aria-live="polite" class="status"></div>'
            '<div aria-live="polite" class="answer study-answer"><div class="choice-feedback"><h4>❌ Why your choice loses</h4><p class="choice-feedback-text"></p></div>'
            f'<div class="study-block winning"><h4>✅ Why the winning answer wins</h4><p>{esc(it["why_wins"]["en"])}</p><p class="vi">{esc(it["why_wins"]["vi"])}</p></div>'
            f'<div class="study-block pattern"><h4>🧠 Exam Pattern</h4><p>{esc(it["pattern"]["en"])}</p><p class="vi">{esc(it["pattern"]["vi"])}</p>'
            f'<p class="signals">Key signals: {esc(it["signals"]["en"])}</p><p class="signals vi">Tín hiệu then chốt: {esc(it["signals"]["vi"])}</p></div>'
            f'<div class="study-block explain"><h4>📝 Answer review &amp; reliability</h4>{full}</div>'
            f'<div class="study-block related"><h4>📌 Related Rules</h4><ul>{rule_li}</ul></div></div>'
            f'<div class="map"><div class="label">1. Domain</div><div>Domain {it["domain"]}: {esc(D[it["domain"]]["en"])}</div>'
            f'<div class="label">2. Skill</div><div>{esc(it["skill"])}</div>'
            f'<div class="label">3. Exam Rules Triggered</div><div>{rule_span}</div></div>'
            f'<p class="refs"><strong>Source:</strong> {esc(srcname)}</p>'
            '<div class="note-tools"><label class="flag-wrap"><input class="flag" type="checkbox"/> Flag question</label>'
            '<textarea aria-label="Question note" class="note" placeholder="Add your note for this question..."></textarea></div></div></details></article>')

    sections = ''.join(
        f'<section class="scenario" data-domain-section="{d}"><h2>Domain {d}: {esc(D[d]["en"])} ({D[d]["weight"]}%) <small>({dom_counts[d]} questions)</small></h2>'
        + ''.join(article(it) for it in items if it['domain'] == d) + '</section>' for d in DOMS)
    suffix = rep_re(suffix, r'<p class="foot">.*?</p>',
                    f'<p class="foot">Question bank items are self-collected for practice; keyed answers are working answers and have not been verified against an official answer key. '
                    f'Official samples come from the {prof["guide_label"]}. Independent study tool, not affiliated with Anthropic.</p>')
    gold_li = ''.join(f'<li data-rule="{g["id"]}">{esc(g["en"])}<br/><span class="vi">{esc(g["vi"])}</span></li>' for g in golden)
    suffix = rep_re(suffix, r'<ol class="golden-list">.*?</ol>', f'<ol class="golden-list">{gold_li}</ol>')
    suffix = rep(suffix, 'CCAR-P Golden Rules', f'{code} Golden Rules', 2)
    prefix = rep(prefix, '/* CCAR-P additions */', f'/* {code} additions */')
    extra_css = ('.vi{color:#667085;font-style:italic}.choice-feedback-text{white-space:pre-line}'
                 '.rel-warn{padding:8px 10px;border-radius:8px;background:#f4f6fb;font-size:13px}.rel-warn.incomplete{background:#fff4d6;border:1px solid #e5b94c}'
                 '.golden-list li .vi{font-size:12.5px}')
    page = prefix.replace('</style>', extra_css + '</style>', 1) + sections + suffix
    page = rep(page, "const KEY='ccarp-study-state-v1';", f"const KEY='{code.lower().replace('-', '')}-study-state-v1';")
    page = rep_re(page, r"fbt\.textContent=`Option \$\{wrong\.join\(' and '\)\} does not address[^`]*`",
                  "fbt.textContent=wrong.map(w=>{const o=(JSON.parse(q.dataset.why||'{}')[w])||{};return 'Option '+w+': '+(o.en||'')+'\\n'+(o.vi||'')}).join('\\n\\n')")
    assert 'CCAR' not in page
    (outp / f'{code}_Explanatory_Interactive_Study.html').write_text(page, encoding='utf-8')

    # ---- Study guide
    g = []
    gcfg = prof.get('guide')
    gdir = pdir / 'guide'
    gn = (gcfg or {}).get('golden_section', 10)
    bn = (gcfg or {}).get('bank_map_section', 12)

    def golden_md():
        lines = [f'## {gn}. The {len(golden)} Golden Rules', f'## {gn}. {len(golden)} Quy tắc vàng', '']
        for x in golden:
            lines += [f'{x["id"]}. {x["en"]}', f'   - {x["vi"]}']
        return '\n'.join(lines) + '\n'

    def bank_map_md():
        counts = collections_counter(items)
        lines = [f'## {bn}. Question bank map', f'## {bn}. Bản đồ ngân hàng câu hỏi', '',
                 'Every practice item is mapped to a blueprint domain and skill. *Reliability*: **official** = Exam Guide sample; **ok / partial** = source wording complete or partly incomplete; **incomplete** = source wording largely incomplete (provisional).',
                 'Mỗi câu luyện tập được ánh xạ vào domain và skill của blueprint. *Độ tin cậy*: **official** = câu mẫu chính thức; **ok / partial** = nội dung nguồn đầy đủ hoặc chưa đầy đủ một phần; **incomplete** = nội dung nguồn chưa đầy đủ phần lớn (tạm thời).', '',
                 '| Domain | Items / Câu | Bank numbers / Số câu trong bank | Incomplete |', '|---|---|---|---|']
        for d in DOMS:
            its = [i for i in items if i['domain'] == d]
            nums = ', '.join(('S' + str(i['id'] - 100)) if i['source'] == 'official-sample' else str(i['id']) for i in its)
            lines.append(f'| {d}. {D[d]["en"]} ({D[d]["weight"]}%) | {len(its)} | {nums} | {sum(1 for i in its if i["reliability"] == "incomplete")} |')
        lines += ['', '*S1–S3 = official samples. / S1–S3 = câu mẫu chính thức.*', '',
                  f'Reliability summary: {counts.get("incomplete", 0)} incomplete, {counts.get("partial", 0)} partial, {counts.get("ok", 0)} ok, {counts.get("official", 0)} official.',
                  f'Tóm tắt độ tin cậy: {counts.get("incomplete", 0)} incomplete, {counts.get("partial", 0)} partial, {counts.get("ok", 0)} ok, {counts.get("official", 0)} official.']
        return '\n'.join(lines) + '\n'

    def collections_counter(its):
        c = {}
        for i in its:
            c[i['reliability']] = c.get(i['reliability'], 0) + 1
        return c

    if gcfg:
        rd = lambda n: (gdir / n).read_text(encoding='utf-8').strip() + '\n'
        g.append(rd(gcfg['head']))
        g += [rd(m) for m in gcfg['modules']]
        g.append(rd(gcfg['traps']))
        g.append(golden_md())
        g.append(rd(gcfg['plan']))
        g.append(bank_map_md())
        g.append(rd(gcfg['refs']))
    else:                                              # fallback: no hand-written modules in the profile
        g.append(f'# {code} Study Guide\n\nAuto-generated digest: no research modules are configured in this profile. Add `guide` to profile.json to include full modules.\n')
        for d in DOMS:
            g.append(f'## {d}. {D[d]["en"]} ({D[d]["weight"]}%)\n')
            for it in [i for i in items if i['domain'] == d]:
                g.append(f'- **{it["ref"]} · {it["skill"]}:** {it["pattern"]["en"]}\n  - {it["pattern"]["vi"]}')
            g.append('')
        g.append(golden_md())
        g.append(bank_map_md())
    (outp / f'{code}_Study_Guide.md').write_text('\n'.join(g), encoding='utf-8')
    print(f'prep pack written to {outp}: ' + ', '.join(sorted(p.name for p in outp.iterdir())))
    print(f'items {nq} (bank {n_bank}, samples {n_samples}); domains {dom_counts}; weighted simulation set {eff}')


if __name__ == '__main__':
    main()
