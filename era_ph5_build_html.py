#!/usr/bin/env python3
"""era_ph5_build_html.py — Unit 5H-0 (v0) of direction_ph5_html_v1.0.md (Ruling H-1)

This section is intended to BUILD era_ph5_dashboard.html — the single-file
Phase 5 dashboard — from the four grains, the manifest and the style tokens,
using the Python standard library only. v0 (this unit) writes the SKELETON:
header, the two controls in their saved states, six empty data-view slots,
the tokens as CSS custom properties, the manifest and the four grains embedded
as JSON, and one inline script that toggles pre-rendered control states. No
view was drawn in v0. Unit 5H-1 fills V1 and V3 from era_ph5_views.py;
Unit 5H-2 fills V2 (the waterfall, eight pre-rendered metro states and
the excluded band) from G2 via era_ph5_views.render(), which hands each
view the grain it reads instead of G1 unconditionally.
Unit 5H-3 fills V4 (the plate-carree map, G1), V5 (the bands and the two
published pairs as intervals, G1 + G4) and V6 (the caveats table, G4).
NO SLOT REMAINS BUILD-INCOMPLETE: the page gate reaches 0 FAIL here.

Properties the page gate (era_ph5_page_gate.py) asserts and this build is
written to satisfy:
  - the file is well-formed XML as well as HTML5 (the gate parses it with
    xml.etree); void elements are self-closed; text is escaped; the embedded
    JSON writes & < > as \\u0026 \\u003c \\u003e so it is XML text AND JSON;
  - nothing is fetched: no <script src>, <link>, <img>, @import, url();
  - DETERMINISTIC: no timestamp, no random id, sort_keys on every dict; the
    only time in the page is the manifest's own written_utc, embedded verbatim;
  - the saved states are in the MARKUP (checked radios, hidden attributes),
    never produced by script;
  - every hex colour and font-size in the page comes from era_ph5_style_v1.0.md.

Row keys for data-src="<grain-stem>:<row-key>:<column>" (used from 5H-1 on):
  era_ph5_metro  -> metro
  era_ph5_stack  -> metro|component_id
  era_ph5_month  -> metro|stage|month
  era_ph5_caveat -> caveat_id

Usage
-----
  python era_ph5_build_html.py --project .                 # writes era_ph5_dashboard.html
  python era_ph5_build_html.py --project . --out scratch.html
  python era_ph5_build_html.py --project . --style other_tokens.md   # tamper W35 only

Exit code 0 when the page was written.
"""

import argparse
import csv
import hashlib
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import era_ph5_views as VIEWS_MOD          # noqa: E402  (one function per view, 5H-1 on)

STYLE_MD = "era_ph5_style_v1.0.md"
MANIFEST_NAME = "era_ph5_grains_manifest.json"
PAGE_NAME = "era_ph5_dashboard.html"
GRAINS = [
    ("G1", "era_ph5_metro", "era_ph5_metro.csv"),
    ("G2", "era_ph5_stack", "era_ph5_stack.csv"),
    ("G3", "era_ph5_month", "era_ph5_month.csv"),
    ("G4", "era_ph5_caveat", "era_ph5_caveat.csv"),
]
ROW_KEYS = {
    "era_ph5_metro": ["metro"],
    "era_ph5_stack": ["metro", "component_id"],
    "era_ph5_month": ["metro", "stage", "month"],
    "era_ph5_caveat": ["caveat_id"],
}
VIEWS = ["V1", "V2", "V3", "V4", "V5", "V6"]
VIEW_TITLES = {
    "V1": "Ranking",
    "V2": "Waterfall",
    "V3": "Channels",
    "V4": "Map",
    "V5": "Bands",
    "V6": "Caveats",
}
METROS = ["Atlanta", "Austin", "Chicago", "Columbus", "Dallas-Fort Worth",
          "Northern Virginia", "Phoenix", "San Jose / Bay Area"]
BASES = [("IT", "USD per IT-MWh"), ("Metered", "USD per metered-MWh")]
SAVED_METRO = "Columbus"      # F5B-7
SAVED_BASIS = "IT"            # p. Basis OFF = the IT basis (F5B-2)

TOKEN_RE = re.compile(r"^\|\s*`(--era-[a-z0-9-]+)`\s*\|\s*`(#[0-9A-Fa-f]{6})`\s*\|")
SIZE_RE = re.compile(r"^\|\s*(caption|body|label|subhead|title)\s*\|\s*(\d+)\s*\|")
FAMILY_RE = re.compile(r"`(Helvetica Neue[^`]*)`")


# --------------------------------------------------------------------------
def read_tokens(style_path):
    """Read the colour tokens, type sizes and family out of the style md.
    Tokens are returned in FILE ORDER (deterministic)."""
    txt = open(style_path, encoding="utf-8").read()
    colours = []
    sizes = {}
    for line in txt.splitlines():
        m = TOKEN_RE.match(line)
        if m:
            colours.append((m.group(1), m.group(2).upper()))
        m = SIZE_RE.match(line)
        if m:
            sizes[m.group(1)] = int(m.group(2))
    fam = FAMILY_RE.search(txt)
    if len(colours) != 13 or len(sizes) != 5 or not fam:
        raise SystemExit("style tokens unreadable in %s: %d colours, %d sizes, family %s"
                         % (style_path, len(colours), len(sizes), bool(fam)))
    return {"colours": colours, "sizes": sizes, "family": fam.group(1)}


def read_grain(path):
    with open(path, newline="", encoding="utf-8-sig") as fh:
        rd = csv.reader(fh)
        rows = list(rd)
    return rows[0], rows[1:]


def md5_of(path):
    h = hashlib.md5()
    with open(path, "rb") as fh:
        h.update(fh.read())
    return h.hexdigest()


def json_text(obj):
    """JSON that is also XML text: & < > escaped as \\uXXXX, ASCII only,
    keys sorted, fixed separators."""
    s = json.dumps(obj, sort_keys=True, ensure_ascii=True, separators=(",", ":"))
    return s.replace("&", "\\u0026").replace("<", "\\u003c").replace(">", "\\u003e")


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;"))


# --------------------------------------------------------------------------
def css(tokens):
    lines = [":root {"]
    for name, hexv in tokens["colours"]:
        lines.append("  %s: %s;" % (name, hexv))
    for role in ("caption", "body", "label", "subhead", "title"):
        lines.append("  --era-size-%s: %dpx;" % (role, tokens["sizes"][role]))
    lines.append("  --era-base: 8px;")
    lines.append("  --era-margin: 48px;")
    lines.append("  --era-gutter: 24px;")
    lines.append("}")
    lines += [
        "html, body { margin: 0; background: var(--era-surface); color: var(--era-ink); }",
        "body { font-family: %s; font-size: var(--era-size-body); line-height: 1.5; }" % tokens["family"],
        ".era-page { max-width: 1280px; margin: 0 auto; padding: var(--era-margin); }",
        ".era-header { display: flex; flex-direction: column; gap: var(--era-base); "
        "padding-bottom: var(--era-gutter); border-bottom: 1px solid var(--era-rule); }",
        ".era-title { font-size: var(--era-size-title); font-weight: 400; margin: 0; letter-spacing: 0; }",
        ".era-subhead { font-size: var(--era-size-subhead); font-weight: 400; margin: 0; color: var(--era-accent-600); }",
        ".era-caption { font-size: var(--era-size-caption); margin: 0; color: var(--era-muted); }",
        ".era-caption a { color: var(--era-accent-500); text-decoration: none; border-bottom: 1px solid var(--era-rule); }",
        ".era-controls { display: flex; gap: var(--era-gutter); margin: 0; padding: 0; }",
        ".era-controls fieldset { border: 0; margin: 0; padding: 0; display: flex; flex-wrap: wrap; gap: var(--era-base); }",
        ".era-controls legend { font-size: var(--era-size-caption); color: var(--era-muted); padding: 0; margin-bottom: var(--era-base); }",
        ".era-controls label { font-size: var(--era-size-body); color: var(--era-ink); cursor: pointer; }",
        ".era-controls input { accent-color: var(--era-accent-400); margin: 0 var(--era-base) 0 0; }",
        ".era-view { padding-top: var(--era-gutter); }",
        ".era-view h2 { font-size: var(--era-size-label); font-weight: 400; margin: 0 0 var(--era-base) 0; }",
        ".era-view[data-status='build-incomplete'] h2 { color: var(--era-muted); }",
        "[hidden] { display: none; }",
        "svg text { font-family: %s; fill: var(--era-ink); }" % tokens["family"],
        ".era-metro { font-size: var(--era-size-body); }",
        ".era-value { font-size: var(--era-size-caption); fill: var(--era-muted); }",
        ".era-note { font-size: var(--era-size-caption); fill: var(--era-muted); }",
        ".era-mitigation { fill: var(--era-surface); stroke: var(--era-rule); stroke-width: 1; }",
        ".era-axis { stroke: var(--era-rule); stroke-width: 1; }",
        ".era-wf-connector { stroke: var(--era-rule); stroke-width: 1; }",
        ".era-seg { fill: var(--era-accent-400); stroke: var(--era-surface); stroke-width: 1; }",
        ".era-seg-big { fill: var(--era-accent-600); stroke: var(--era-surface); stroke-width: 1; }",
        ".era-wf-level { fill: var(--era-accent-700); }",
        ".era-wf-delta { fill: var(--era-accent-200); }",
        ".era-excluded { fill: var(--era-muted); stroke: var(--era-rule); stroke-width: 1; }",
        ".era-band { fill: var(--era-accent-200); }",
        ".era-bracket { fill: var(--era-surface); stroke: var(--era-accent-600); stroke-width: 1; }",
        ".era-table { border-collapse: collapse; width: 100%; margin-top: var(--era-base); }",
        ".era-table th { font-size: var(--era-size-caption); font-weight: 400; color: var(--era-muted); text-align: left; padding: var(--era-base); border-bottom: 1px solid var(--era-rule); }",
        ".era-table td { font-size: var(--era-size-caption); padding: var(--era-base); border-bottom: 1px solid var(--era-rule); vertical-align: top; }",
        ".era-table th.era-num, .era-table td.era-num { text-align: right; white-space: nowrap; }",
    ] + [
        ".era-ramp-%d { fill: var(--era-accent-%d00); }" % (i, i + 1) for i in range(7)
    ]
    return "\n".join(lines)


SCRIPT = """(function () {
  function bind(control, attr) {
    var fs = document.querySelector('[data-control=\\"' + control + '\\"]');
    if (!fs) { return; }
    var inputs = fs.querySelectorAll('input[type=\\"radio\\"]');
    inputs.forEach(function (inp) {
      inp.addEventListener('change', function () {
        var groups = document.querySelectorAll('[' + attr + ']');
        groups.forEach(function (gr) {
          if (gr.getAttribute(attr) === inp.value) { gr.removeAttribute('hidden'); }
          else { gr.setAttribute('hidden', 'hidden'); }
        });
      });
    });
  }
  bind('p. Metro', 'data-state-metro');
  bind('p. Basis', 'data-state-basis');
})();"""


def controls_html():
    out = ['<nav class="era-controls" aria-label="controls">']
    out.append('<fieldset data-control="p. Metro" data-saved="%s">' % esc(SAVED_METRO))
    out.append("<legend>Metro (V2)</legend>")
    for m in METROS:
        checked = ' checked="checked"' if m == SAVED_METRO else ""
        out.append('<label><input type="radio" name="p-metro" value="%s"%s/>%s</label>'
                   % (esc(m), checked, esc(m)))
    out.append("</fieldset>")
    out.append('<fieldset data-control="p. Basis" data-saved="%s">' % esc(SAVED_BASIS))
    out.append("<legend>Basis (V1)</legend>")
    for val, label in BASES:
        checked = ' checked="checked"' if val == SAVED_BASIS else ""
        out.append('<label><input type="radio" name="p-basis" value="%s"%s/>%s</label>'
                   % (esc(val), checked, esc(label)))
    out.append("</fieldset>")
    out.append("</nav>")
    return "\n".join(out)


def views_html(grains):
    """A BUILT slot carries its <svg data-view="Vn"> and drops data-status;
    an unbuilt slot stays empty and declares data-status="build-incomplete",
    which is what makes the page gate FAIL it as BUILD-INCOMPLETE rather than
    skip it (absence is never a pass, F5B-9). 5H-1 builds V1 and V3."""
    out = []
    for v in VIEWS:
        fn = VIEWS_MOD.VIEWS.get(v)
        if fn is None:
            out.append('<section class="era-view" id="%s" data-view="%s" data-status="build-incomplete">' % (v, v))
            out.append("<h2>%s %s</h2>" % (v, esc(VIEW_TITLES[v])))
            out.append("</section>")
            continue
        out.append('<section class="era-view" id="%s" data-view="%s">' % (v, v))
        out.append("<h2>%s %s</h2>" % (v, esc(VIEW_TITLES[v])))
        out.append(VIEWS_MOD.render(v, grains, METROS, SAVED_METRO))
        out.append("</section>")
    return "\n".join(out)


def build_page(project, style_path=None):
    """Return the page as bytes. Pure function of the files it reads."""
    style_path = style_path or os.path.join(project, STYLE_MD)
    tokens = read_tokens(style_path)
    manifest_path = os.path.join(project, MANIFEST_NAME)
    with open(manifest_path, encoding="utf-8") as fh:
        manifest = json.load(fh)

    grain_blocks = []
    as_dicts = {}
    for gid, stem, fname in GRAINS:
        columns, rows = read_grain(os.path.join(project, fname))
        block = {"grain": gid, "file": fname, "stem": stem, "row_key": ROW_KEYS[stem],
                 "columns": columns, "rows": rows}
        grain_blocks.append((stem, block))
        as_dicts[gid] = [dict(zip(columns, r)) for r in rows]

    parts = []
    parts.append("<!DOCTYPE html>")
    parts.append('<html lang="en">')
    parts.append("<head>")
    parts.append('<meta charset="utf-8"/>')
    parts.append('<meta name="viewport" content="width=device-width, initial-scale=1"/>')
    parts.append("<title>Electrical Rate Analysis</title>")
    parts.append("<style>")
    parts.append(css(tokens))
    parts.append("</style>")
    parts.append("</head>")
    parts.append("<body>")
    parts.append('<div class="era-page">')
    parts.append('<header class="era-header">')
    parts.append('<h1 class="era-title">Electrical Rate Analysis</h1>')
    parts.append('<p class="era-subhead">Giga-scale campus cost per IT-MWh, eight metros, and what is avoidable</p>')
    parts.append('<p class="era-caption" id="era-caption">Facility basis. Frozen contract. '
                 '<a href="#V6">Read the caveats first</a>.</p>')
    parts.append(controls_html())
    parts.append("</header>")
    parts.append("<main>")
    parts.append(views_html(as_dicts))
    parts.append("</main>")
    parts.append("</div>")
    parts.append('<script type="application/json" id="era-manifest">')
    parts.append(json_text(manifest))
    parts.append("</script>")
    for stem, block in grain_blocks:
        parts.append('<script type="application/json" id="era-grain-%s" data-grain="%s">'
                     % (stem, block["grain"]))
        parts.append(json_text(block))
        parts.append("</script>")
    parts.append("<script>")
    parts.append(SCRIPT)
    parts.append("</script>")
    parts.append("</body>")
    parts.append("</html>")
    return ("\n".join(parts) + "\n").encode("utf-8")


def write_atomic(path, data):
    """Never open the live file for writing until the content exists (2F-b)."""
    tmp = path + ".tmp"
    with open(tmp, "wb") as fh:
        fh.write(data)
    os.replace(tmp, path)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", default=".")
    ap.add_argument("--out", default=None)
    ap.add_argument("--style", default=None,
                    help="token file to read (tamper W35 only; default is the project's)")
    ap.add_argument("--quiet", action="store_true")
    a = ap.parse_args()
    data = build_page(a.project, a.style)
    out = a.out or os.path.join(a.project, PAGE_NAME)
    write_atomic(out, data)
    if not a.quiet:
        print("era_ph5_build_html.py  wrote %s  %d bytes  md5 %s"
              % (os.path.abspath(out), len(data), hashlib.md5(data).hexdigest()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
