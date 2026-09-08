"""An offline, semantic HTML view of retained evidence. No remote assets or JS."""

import html
import json


def esc(value):
    return html.escape(str(value), quote=True)


def render(result, manifest):
    files = result.get("files", [])
    changed = sum(bool(row.get("changed")) for row in files)
    review = sum(f["status"] == "REVIEW NEEDED" for row in files for f in row.get("findings", []))
    blocks = []
    for row in files:
        findings = "".join(f'<li><strong>{esc(f["status"])}</strong> · Line {f["line"]}: {esc(f["reason"])}</li>' for f in row.get("findings", []))
        edits = "".join(f'<li><code>{esc(e["before"])}</code> → <code>{esc(e["after"])}</code> — {esc(e["reason"])}</li>' for e in row.get("edits", []))
        blocks.append(f'<article><h3>{esc(row["path"])}</h3><p>{"Candidate edits available" if row.get("changed") else "Unchanged"}</p>'
                      f'<ul>{findings or "<li>No selected migration call found.</li>"}</ul>'
                      f'<details><summary>Edits and source identity</summary><ul>{edits or "<li>No edits.</li>"}</ul>'
                      f'<p>Original SHA-256</p><code class="hash">{esc(row["source_sha256"])}</code>'
                      f'<p>Candidate SHA-256</p><code class="hash">{esc(row["candidate_sha256"])}</code></details></article>')
    cases = []
    for case in result.get("cases", []):
        cases.append(f'<article><h3>{esc(case["id"])} · {esc(case["status"])}</h3>'
                     f'<details><summary>Original and candidate observations</summary>'
                     f'<h4>Original</h4><pre>{esc(json.dumps(case.get("original"), indent=2, ensure_ascii=False))}</pre>'
                     f'<h4>Candidate</h4><pre>{esc(json.dumps(case.get("candidate"), indent=2, ensure_ascii=False))}</pre>'
                     f'<h4>Differences</h4><pre>{esc(json.dumps(case.get("differences", []), indent=2, ensure_ascii=False))}</pre>'
                     f'</details></article>')
    limits = "".join(f'<li>{esc(text)}</li>' for text in result.get("limitations", []))
    measured = "Behavior was measured only for the declared cases and exact runtimes." if result.get("behavior_measured") else "Behavior has not been measured. This report describes source inspection only."
    control_note = '<p><strong>Deliberately wrong candidate:</strong> ' + esc(result.get('negative_control_description', 'This run changes a diagnostic source name to WRONG.ini. A regression is the required negative-control result.')) + '</p>' if result.get('negative_control') else ''
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'unsafe-inline'; base-uri 'none'; form-action 'none'">
<title>Renewal Engine — migration review</title>
<style>
:root{{font-family:system-ui,sans-serif;color:#172d31;background:#f5f4ee;line-height:1.6;font-size:16px}}
*{{box-sizing:border-box}}body{{margin:0}}a{{color:#095e69;text-underline-offset:.2em}}a:focus-visible,summary:focus-visible{{outline:3px solid #ad4400;outline-offset:5px}}
.skip{{position:absolute;top:-100px;left:16px;background:white;padding:12px}}.skip:focus{{top:12px}}
header,main,footer{{max-width:1000px;margin:auto;padding:32px 24px}}header{{padding-top:54px;border-bottom:1px solid #a6b4ae}}
.eyebrow{{font-weight:700;letter-spacing:.08em;font-size:.8rem;text-transform:uppercase}}h1{{font-size:clamp(2rem,6vw,3.8rem);line-height:1.1;margin:.5em 0}}h2{{margin-top:2em}}h3{{overflow-wrap:anywhere}}
.status{{border-left:5px solid #966000;background:#fff8dc;padding:16px 20px;margin:24px 0}}.status p{{margin:.4em 0}}
nav{{display:flex;flex-wrap:wrap;gap:12px 24px}}.metrics{{display:flex;flex-wrap:wrap;gap:24px;margin:24px 0}}.metrics p{{margin:0}}.metrics strong{{font-size:1.8rem;display:block}}
article{{background:#fff;padding:20px 24px;margin:16px 0;border:1px solid #bdc8c2;border-radius:8px}}article h3{{margin-top:0}}summary{{cursor:pointer;padding:8px 0;font-weight:650}}
code,pre{{font-family:ui-monospace,monospace;font-size:.88rem}}pre{{white-space:pre-wrap;overflow-wrap:anywhere;background:#eef2ef;padding:16px}}.hash{{overflow-wrap:anywhere}}li{{margin:.6em 0}}
footer{{font-size:.9rem;border-top:1px solid #a6b4ae}}@media(max-width:480px){{header,main,footer{{padding:24px 16px}}article{{padding:16px}}}}
@media print{{details{{display:block}}nav,.skip{{display:none}}article{{break-inside:avoid}}}}
</style></head><body><a class="skip" href="#main">Skip to review</a>
<header><p class="eyebrow">Renewal Engine · local migration review</p><h1>Understand every change.</h1>
<p>A bounded Python migration, with its evidence kept beside the patch.</p>
<div class="status" role="status"><strong>{esc(result["status"])}</strong><p>{measured}</p>{control_note}</div>
<nav aria-label="Saved evidence"><a href="changes.patch">Review patch</a><a href="results.json">Results JSON</a><a href="manifest.json">Run manifest</a><a href="state.json">Recovery state</a></nav></header>
<main id="main"><div class="metrics"><p><strong>{len(files)}</strong>Python files inspected</p><p><strong>{changed}</strong>Files with edits</p><p><strong>{review}</strong>Unsupported findings</p></div>
<h2>Review the source</h2><p>Read each proposed edit, then inspect <code>changes.patch</code>. Your original source stays unchanged. Candidate files are saved in <code>candidate/</code>.</p>{''.join(blocks)}
{('<h2>Behavior comparison</h2>' + ''.join(cases)) if cases else ''}
<h2>Coverage and limits</h2><ul>{limits}</ul>
<h2>Keep, reject, or restart</h2><p>Keep this entire run directory to reopen the report and evidence. Rejecting the candidate requires no rollback of your original source. If a run is incomplete, retain it and restart with a new output directory. Never use an incomplete run as passing evidence.</p>
<details><summary>Tool and runtime identity</summary><pre>{esc(json.dumps({k:v for k,v in manifest.items() if k != "files"},indent=2,ensure_ascii=False))}</pre></details>
</main><footer>Renewal Engine {esc(manifest.get('tool_version',''))} · AGPL-3.0 · Offline report, with no scripts, hosted model, or external assets. This report is evidence for maintainer review, not automatic adoption.</footer></body></html>'''
