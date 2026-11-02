#!/usr/bin/env python3
"""Genera il PDF di un deliverable da Markdown.

Uso: python3 scripts/build-pdf.py [D1-Requirements]  (nome del file .md senza estensione)
Richiede: Node (npx marked) e Google Chrome.
"""
import html
import sys
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STEM = sys.argv[1] if len(sys.argv) > 1 else "D1-Requirements"
DOCS = ROOT / "docs"
SRC = DOCS / f"{STEM}.md"
OUT_HTML = DOCS / "build" / f"{STEM}.html"
OUT_PDF = DOCS / f"{STEM}.pdf"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

md = SRC.read_text(encoding="utf-8")
doc_title = re.search(r"^# (.+)$", md, re.M).group(1).strip()

# --- metadata from the header block (before the first ---) ---
head, body = md.split("\n---\n", 1)
def meta(label):
    m = re.search(rf"\*\*{label}:\*\*\s*(.+)", head)
    return m.group(1).strip() if m else ""
title_line = meta("Progetto")
name, _, tagline = title_line.partition(" – ")
course = meta("Corso")
group = meta("Gruppo")
version = meta("Versione")

# --- markdown -> html ---
body_html = subprocess.run(
    ["npx", "-y", "marked", "--gfm"], input=body, capture_output=True, text=True, check=True, cwd=ROOT
).stdout

# ids on h2/h3 + table of contents from h2
toc = []
def add_id(m):
    level, text = m.group(1), m.group(2)
    slug = re.sub(r"[^a-z0-9]+", "-", re.sub(r"<[^>]+>", "", text).lower()).strip("-")
    if level == "2":
        toc.append((slug, re.sub(r"<[^>]+>", "", text)))
    return f'<h{level} id="{slug}">{text}</h{level}>'
body_html = re.sub(r"<h([23])>(.*?)</h\1>", add_id, body_html)

# figures: wrap standalone images with caption
body_html = re.sub(
    r'<p><img src="([^"]+)" alt="([^"]*)"></p>',
    lambda m: f'<figure><img src="{m.group(1)}" alt="{m.group(2)}"><figcaption>{m.group(2)}</figcaption></figure>',
    body_html,
)
# GAP / placeholders highlight
body_html = re.sub(r"\[(GAP\d+[^\]]*)\]", r'<span class="gap">\1</span>', body_html)
body_html = re.sub(r"\[(da [^\]]+|canale: GAP|[^\]<]*: GAP)\]", r'<span class="gap">\1</span>', body_html)

toc_html = "".join(f'<li><a href="#{s}">{html.escape(t)}</a></li>' for s, t in toc)

page = f"""<!DOCTYPE html>
<html lang="it"><head><meta charset="utf-8">
<title>{html.escape(doc_title)} · {html.escape(name)}</title>
<style>
@page {{ size: A4; margin: 20mm 18mm 20mm 18mm;
  @bottom-left {{ content: "{html.escape(name)} · {doc_title.replace(chr(34), "")} · v{html.escape(version.split(' ')[0])}"; font: 8pt -apple-system, Helvetica, sans-serif; color: #7A8781; }}
  @bottom-right {{ content: counter(page) " / " counter(pages); font: 8pt -apple-system, Helvetica, sans-serif; color: #7A8781; }} }}
@page :first {{ margin: 0; @bottom-left {{ content: none; }} @bottom-right {{ content: none; }} }}
:root {{ --ink:#14322A; --leaf:#2F7D4F; --mint:#EAF4E8; --line:#D6DED4; --muted:#5E6E67; }}
* {{ box-sizing: border-box; }}
body {{ font-family: -apple-system, "Helvetica Neue", Helvetica, Arial, sans-serif; font-size: 10pt; line-height: 1.5; color: var(--ink); margin: 0; }}

.cover {{ height: 297mm; padding: 34mm 22mm 22mm; display: flex; flex-direction: column; background: var(--ink); color: #fff; page-break-after: always; position: relative; overflow: hidden; }}
.cover .leaf {{ position: absolute; right: -40mm; top: 60mm; width: 170mm; height: 170mm; border-radius: 50% 50% 50% 0; background: var(--leaf); opacity: .35; transform: rotate(-45deg); }}
.cover .leaf2 {{ position: absolute; right: 25mm; top: 150mm; width: 70mm; height: 70mm; border-radius: 50% 50% 50% 0; background: #8FD19E; opacity: .25; transform: rotate(-45deg); }}
.cover .kicker {{ font-size: 11pt; letter-spacing: .18em; text-transform: uppercase; color: #8FD19E; font-weight: 700; }}
.cover h1 {{ font-size: 46pt; margin: 8mm 0 3mm; line-height: 1; letter-spacing: -.01em; }}
.cover h1 span {{ color: #8FD19E; }}
.cover .tag {{ font-size: 15pt; max-width: 125mm; line-height: 1.35; color: #DDE8E0; }}
.cover .doc {{ margin-top: 22mm; font-size: 20pt; font-weight: 700; }}
.cover .meta {{ margin-top: auto; font-size: 10.5pt; line-height: 1.8; color: #DDE8E0; position: relative; }}
.cover .meta b {{ color: #fff; display: inline-block; width: 26mm; }}

.toc {{ page-break-after: always; padding-top: 4mm; }}
.toc h2 {{ border: 0; margin-top: 0; }}
.toc ol {{ padding-left: 0; list-style: none; counter-reset: t; }}
.toc li {{ padding: 2.4mm 0; border-bottom: 1px solid var(--line); font-size: 11pt; }}
.toc a {{ color: var(--ink); text-decoration: none; }}
.toc .note {{ margin-top: 10mm; background: var(--mint); border-left: 3px solid var(--leaf); padding: 4mm 5mm; font-size: 9.5pt; color: var(--muted); }}

h2 {{ font-size: 16pt; color: var(--ink); border-bottom: 2px solid var(--leaf); padding-bottom: 1.5mm; margin: 9mm 0 4mm; page-break-after: avoid; }}
h2:not(:first-of-type) {{ }}
h3 {{ font-size: 12pt; color: var(--leaf); margin: 6mm 0 2mm; page-break-after: avoid; }}
p {{ margin: 0 0 2.5mm; }}
ul, ol {{ margin: 0 0 3mm; padding-left: 6mm; }}
li {{ margin-bottom: 1mm; }}
strong {{ color: var(--ink); }}
a {{ color: var(--leaf); }}
blockquote {{ margin: 0 0 4mm; padding: 3mm 5mm; background: var(--mint); border-left: 3px solid var(--leaf); color: var(--muted); }}
blockquote p {{ margin: 0; }}
hr {{ display: none; }}
code {{ font-family: "SF Mono", Menlo, monospace; font-size: 8.8pt; background: #F1F4EF; padding: .2mm 1mm; border-radius: 2px; }}
pre {{ background: #F4F7F2; border: 1px solid var(--line); border-radius: 4px; padding: 3mm 4mm; font-size: 8.6pt; line-height: 1.45; page-break-inside: avoid; white-space: pre; overflow: hidden; }}
pre code {{ background: none; padding: 0; }}

table {{ width: 100%; border-collapse: collapse; margin: 1mm 0 5mm; font-size: 9pt; page-break-inside: auto; }}
thead {{ display: table-header-group; }}
tr {{ page-break-inside: avoid; }}
th {{ background: var(--ink); color: #fff; text-align: left; font-weight: 600; padding: 1.8mm 2.2mm; }}
td {{ border-bottom: 1px solid var(--line); padding: 1.6mm 2.2mm; vertical-align: top; }}
tr:nth-child(even) td {{ background: #F7FAF6; }}
td:first-child {{ font-weight: 600; min-width: 12mm; }}
td:last-child:not(:first-child) {{ }}

figure {{ margin: 4mm 0 6mm; text-align: center; page-break-inside: avoid; }}
figure img {{ max-width: 100%; max-height: 205mm; border: 1px solid var(--line); border-radius: 4px; }}
figcaption {{ font-size: 8.5pt; color: var(--muted); margin-top: 1.5mm; font-style: italic; }}
img[src$="mockup-1-cittadino.png"] {{ max-height: 175mm; }}

.gap {{ background: #FCEFD9; color: #8A5A10; border-radius: 2px; padding: 0 1mm; font-size: 8.8pt; font-weight: 600; white-space: nowrap; }}

/* user stories: keep each story with its ACs */
p:has(+ ul), p:has(+ figure) {{ page-break-after: avoid; break-after: avoid; }}
figure + p {{ margin-top: 6mm; }}
[id="5-user-story-e-acceptance-criteria"] ~ p strong:first-child {{ color: var(--leaf); }}
[id="6-use-case-principali"], [id="7-user-flow"], [id="10-dati"], [id="11-gap-e-questioni-aperte"] {{ page-break-before: always; }}
</style></head>
<body>
<section class="cover">
  <div class="leaf"></div><div class="leaf2"></div>
  <div class="kicker">Ingegneria del Software · A.A. 2026-27</div>
  <h1>Canopia</h1>
  <div class="tag">{html.escape(tagline)}</div>
  <div class="doc">{html.escape(doc_title)}</div>
  <div class="meta">
    <div><b>Corso</b>{html.escape(course)}</div>
    <div><b>Gruppo</b>{html.escape(group)}</div>
    <div><b>Committente</b>Comune di Trento</div>
    <div><b>Versione</b>{html.escape(version)}</div>
  </div>
</section>
<section class="toc">
  <h2>Indice</h2>
  <ol>{toc_html}</ol>
  <div class="note">Bozza di lavoro. Le parti evidenziate come <span class="gap">GAP</span> sono questioni aperte segnalate, non dati inventati. Nei mockup nomi, ID e valori sono di esempio.</div>
</section>
<main>
{body_html}
</main>
</body></html>
"""

OUT_HTML.parent.mkdir(exist_ok=True)
# images are referenced relative to the project root
page = page.replace('src="diagrammi/', 'src="../diagrammi/')
OUT_HTML.write_text(page, encoding="utf-8")

subprocess.run(
    [CHROME, "--headless=new", "--no-pdf-header-footer", f"--print-to-pdf={OUT_PDF}", OUT_HTML.as_uri()],
    check=True, capture_output=True,
)
print(f"OK → {OUT_PDF}")
