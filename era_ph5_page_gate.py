#!/usr/bin/env python3
"""era_ph5_page_gate.py — Unit 5H-0 of direction_ph5_html_v1.0.md (Ruling H-2)

This section is intended to be THE ONLY ACCEPTANCE for era_ph5_dashboard.html:
it parses the page as XML and asserts, group by group, that the page is a
faithful, fresh, self-contained, on-token rendering of the four grains, with
every typed figure credited to a cell. It reads the ARTEFACT, never a spec that
drives a runtime (H-1, §0.5). Standard library only; runs in the device VM
(3.10) under 45 s and in Brad's shell with nothing installed.

Groups (letters kept where the duty is the same as the retired workbook gate,
so the findings still read):
  D    the four grains, 29 gates, via era_ph5_grain_gate.group_d (moved verbatim)
  H    page hygiene: parses; nothing fetched; manifest + grain blocks present
       and internally consistent; H5 DETERMINISM (build twice into scratch,
       identical); H6 REPRODUCTION (scratch build == page on disk); size <= 4 MB
  H13  freshness BY CONSTRUCTION: embedded manifest == disk manifest == md5 of
       each CSV on disk; embedded rows == CSV rows as group D parses them.
       Manifest absent -> FAIL, never SKIP (F5B-9)
  P    the two controls: exist; saved states Columbus / IT read from the
       MARKUP; every state pre-rendered (8 V2 groups, 2 V1 groups)
  V    per-view structure (build-incomplete slots FAIL, labelled); V1b/V1c
       are quantified per pre-rendered basis state (5H-1, F5H1-1); V2c is
       quantified over the DRAWING and the page's own CSS, not over the
       build's self-describing attributes (5H-2)
  B    basis (F5B-2, F5A-4)
  S    style: every hex in the page is one of the 13 tokens read out of
       era_ph5_style_v1.0.md at run time (HEX, not name); every font-size in
       {11,13,16,22,34}; one family; 8 px base, 48 px margin, 24 px gutter;
       every <svg> dimension a multiple of 8; no vacuous pass
  T    typed figures: every text element whose own text contains a figure
       carries data-src="<grain>:<row-key>:<column>" and equals that cell to
       the precision shown; the count of UNCREDITED numeric text is ZERO

A gate that cannot run because the view it reads is not built yet FAILS with
the label BUILD-INCOMPLETE (the slot declares it); a gate that has nothing to
quantify over on a partial page is SKIP-OK with the reason, never PASS.

Usage
-----
  python era_ph5_page_gate.py --project .
  python era_ph5_page_gate.py --project . --log era_ph5_5h_gate_run.log
  python era_ph5_page_gate.py --project . --groups D,H,H13
  python era_ph5_page_gate.py --project . --page other.html
  python era_ph5_page_gate.py --project . --style <tokens.md>   # tamper W35 only
  python era_ph5_page_gate.py --summary --log era_ph5_5h_gate_run.log

Exit code 0 only when every selected gate PASSES and none is SKIP-BLIND.
"""

import argparse
import hashlib
import json
import os
import platform
import re
import sys
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import era_ph5_grain_gate as GG          # noqa: E402  (group D, moved verbatim)
import era_ph5_build_html as BUILD       # noqa: E402  (H5 / H6 rebuild)

PAGE_NAME = "era_ph5_dashboard.html"
MANIFEST_NAME = "era_ph5_grains_manifest.json"
STYLE_MD = "era_ph5_style_v1.0.md"
MAX_BYTES = 4 * 1024 * 1024
SIZES = {11, 13, 16, 22, 34}
METROS = GG.METROS
V3_ORDER = GG.V3_ORDER
VIEWS = ["V1", "V2", "V3", "V4", "V5", "V6"]

HEX_RE = re.compile(r"#[0-9A-Fa-f]{6}\b")
FONT_SIZE_CSS_RE = re.compile(r"font-size\s*:\s*(\d+(?:\.\d+)?)\s*(px|pt|em|rem|%)?", re.I)
FONT_SIZE_VAR_RE = re.compile(r"--era-size-[a-z]+\s*:\s*(\d+)px")
FONT_FAMILY_RE = re.compile(r"font-family\s*:\s*([^;}\"]+)", re.I)
FETCH_RE = re.compile(r"(https?:)?//[A-Za-z0-9.-]+\.[A-Za-z]{2,}", re.I)
FIGURE_RE = re.compile(r"(\d{3,}|\d+[.,]\d+|\$\s?\d+)")
NUMBER_RE = re.compile(r"^[-+−]?\$?\s?[\d,]*\.?\d+\s?%?$")
BANNED_METERED_LITERALS = ["0.9742", "0.97"]      # F5A-4: the metered crossing
BUILD_INCOMPLETE = "BUILD-INCOMPLETE (slot declares data-status=build-incomplete; declared in era_ph5_5h_results.md)"


# --------------------------------------------------------------------------
def md5_bytes(b):
    return hashlib.md5(b).hexdigest()


def md5_of(path):
    with open(path, "rb") as fh:
        return md5_bytes(fh.read())


def own_text(el):
    """The element's own text (not descendants'), including tails of children
    that are rendered inline. Enough for figure detection."""
    parts = [el.text or ""]
    for ch in el:
        parts.append(ch.tail or "")
    return "".join(parts)


def iter_text_elements(root):
    for el in root.iter():
        if el.tag in ("script", "style"):
            continue
        t = own_text(el).strip()
        if t:
            yield el, t


def find_view(root, v):
    """Return (slot, svg_or_table, incomplete)."""
    slot = None
    for el in root.iter():
        if el.tag == "section" and el.get("data-view") == v:
            slot = el
            break
    if slot is None:
        return None, None, True
    incomplete = slot.get("data-status") == "build-incomplete"
    body = None
    for el in slot.iter():
        if el is slot:
            continue
        if el.get("data-view") == v and el.tag in ("svg", "table"):
            body = el
            break
    return slot, body, incomplete or body is None


# --------------------------------------------------------------------------
class Page:
    def __init__(self, path):
        self.path = path
        self.bytes = open(path, "rb").read()
        self.text = self.bytes.decode("utf-8")
        self.root = None
        self.error = None
        try:
            self.root = ET.fromstring(self.bytes)
        except ET.ParseError as e:
            self.error = str(e)
        self.manifest = None
        self.grains = {}
        if self.root is not None:
            for s in self.root.iter("script"):
                if s.get("type") != "application/json":
                    continue
                sid = s.get("id") or ""
                try:
                    obj = json.loads(s.text or "")
                except ValueError:
                    obj = None
                if sid == "era-manifest":
                    self.manifest = obj
                elif sid.startswith("era-grain-"):
                    self.grains[sid[len("era-grain-"):]] = obj

    def grain_rows_as_dicts(self, stem):
        blk = self.grains.get(stem)
        if not isinstance(blk, dict) or "columns" not in blk or "rows" not in blk:
            return None
        cols = blk["columns"]
        return [dict(zip(cols, r)) for r in blk["rows"]]

    def style_text(self):
        if self.root is None:
            return ""
        return "\n".join((s.text or "") for s in self.root.iter("style"))


# --------------------------------------------------------------------------
def group_h(g, page, project, style_path):
    g.check("H1", "H", page.root is not None and page.root.tag == "html",
            "page present at %s, single file, parses as well-formed XML (root <html>)"
            % os.path.basename(page.path) if page.root is not None else
            "page does NOT parse as XML: %s" % page.error)
    if page.root is None:
        for gid in ("H2", "H3", "H4", "H5", "H6", "H7"):
            g.check(gid, "H", False, "page unparseable")
        return

    # H2 nothing fetched
    bad = []
    for el in page.root.iter():
        if el.tag == "script" and el.get("src") is not None:
            bad.append("<script src>")
        if el.tag in ("link", "iframe", "object", "embed", "video", "audio", "source"):
            bad.append("<%s>" % el.tag)
        if el.tag == "img" and not (el.get("src") or "").startswith("data:"):
            bad.append("<img> without data: src")
        for k, v in el.attrib.items():
            if k in ("href", "src", "xlink:href", "{http://www.w3.org/1999/xlink}href", "poster", "action"):
                if v.startswith("#") or v.startswith("data:"):
                    continue
                if FETCH_RE.search(v) or v.startswith("/") or "." in v.split("?")[0]:
                    bad.append("%s=%s" % (k, v[:40]))
    css = page.style_text()
    if "@import" in css:
        bad.append("@import in CSS")
    for m in re.finditer(r"url\(\s*['\"]?([^'\")]+)", css):
        if not m.group(1).startswith("data:"):
            bad.append("url(%s) in CSS" % m.group(1)[:40])
    g.check("H2", "H", not bad,
            "nothing is fetched: no <script src>, <link>, <iframe>, @import, non-data url(), "
            "external href/src" + ("" if not bad else "; found %s" % bad[:6]))

    # H3 manifest block
    man = page.manifest
    ok = (isinstance(man, dict) and isinstance(man.get("grains"), dict)
          and set(man["grains"]) == set(v for _, _, v in BUILD.GRAINS)
          and all(isinstance(x, dict) and {"md5", "rows", "cols"} <= set(x)
                  for x in man["grains"].values())
          and "db_md5" in man and "written_utc" in man)
    g.check("H3", "H", ok,
            "embedded manifest block present, JSON, four grains each with md5/rows/cols, db_md5 and written_utc"
            + ("" if ok else "; got %s" % (type(man).__name__ if not isinstance(man, dict) else sorted(man))))

    # H4 grain blocks vs embedded manifest
    bad = []
    for gid, stem, fname in BUILD.GRAINS:
        blk = page.grains.get(stem)
        if not isinstance(blk, dict) or "columns" not in blk or "rows" not in blk:
            bad.append("%s block missing or malformed" % stem)
            continue
        if not ok:
            bad.append("%s: no manifest to compare" % stem)
            continue
        m = man["grains"][fname]
        if len(blk["rows"]) != m["rows"] or len(blk["columns"]) != m["cols"]:
            bad.append("%s %dx%d vs manifest %sx%s" % (stem, len(blk["rows"]), len(blk["columns"]),
                                                      m["rows"], m["cols"]))
        if any(len(r) != len(blk["columns"]) for r in blk["rows"]):
            bad.append("%s ragged rows" % stem)
    g.check("H4", "H", not bad,
            "four embedded grain blocks present; each block's rows x cols equal the EMBEDDED manifest's"
            + ("" if not bad else "; " + "; ".join(bad)))

    # H5 determinism, H6 reproduction
    try:
        # The rebuild reads the PROJECT'S inputs, never the --style override:
        # --style changes what S compares against, not what the build read.
        b1 = BUILD.build_page(project, None)
        b2 = BUILD.build_page(project, None)
        g.check("H5", "H", b1 == b2,
                "DETERMINISM: two scratch builds from the project's inputs are byte-identical (%d B, md5 %s)"
                % (len(b1), md5_bytes(b1)))
        g.check("H6", "H", b1 == page.bytes,
                "REPRODUCTION: the scratch build equals the page on disk byte for byte"
                if b1 == page.bytes else
                "REPRODUCTION FAILS: scratch build %d B md5 %s, page on disk %d B md5 %s"
                % (len(b1), md5_bytes(b1), len(page.bytes), md5_bytes(page.bytes)))
    except Exception as e:      # noqa: BLE001 — a build that cannot run is a FAIL, not a crash
        g.check("H5", "H", False, "build raised: %r" % (e,))
        g.check("H6", "H", False, "build raised: %r" % (e,))

    g.check("H7", "H", len(page.bytes) <= MAX_BYTES,
            "page is %d B (<= %d B)" % (len(page.bytes), MAX_BYTES))


def group_h13(g, page, project, data):
    mp = os.path.join(project, MANIFEST_NAME)
    disk = None
    if os.path.isfile(mp):
        try:
            with open(mp, encoding="utf-8") as fh:
                disk = json.load(fh)
        except ValueError:
            disk = None
    if disk is None:
        g.check("H13a", "H13", False, "%s ABSENT or unreadable on disk — FAIL, never SKIP (F5B-9)" % MANIFEST_NAME)
        g.check("H13b", "H13", False, "%s ABSENT or unreadable on disk — FAIL, never SKIP (F5B-9)" % MANIFEST_NAME)
    else:
        same = page.manifest == disk
        detail = ""
        if not same and isinstance(page.manifest, dict) and isinstance(disk, dict):
            diffs = []
            for fname in sorted(set(disk.get("grains", {})) | set(page.manifest.get("grains", {}))):
                a = disk.get("grains", {}).get(fname)
                b = page.manifest.get("grains", {}).get(fname)
                if a != b:
                    diffs.append("%s embedded md5 %s vs disk %s"
                                 % (fname, (b or {}).get("md5"), (a or {}).get("md5")))
            detail = "; " + "; ".join(diffs) if diffs else "; top-level fields differ"
        g.check("H13a", "H13", same,
                "embedded manifest == %s on disk (whole document)%s" % (MANIFEST_NAME, "" if same else detail))
        bad = []
        for gid, stem, fname in BUILD.GRAINS:
            p = os.path.join(project, fname)
            m = disk.get("grains", {}).get(fname, {})
            if not os.path.isfile(p):
                bad.append("%s missing" % fname)
                continue
            d = md5_of(p)
            if d != m.get("md5"):
                bad.append("%s disk md5 %s != manifest %s" % (fname, d, m.get("md5")))
        g.check("H13b", "H13", not bad,
                "for each grain, the manifest's md5 equals the md5 of the CSV on disk"
                + ("" if not bad else "; " + "; ".join(bad)))

    # H13c embedded rows == CSV rows as group D parses them
    bad = []
    for gid, stem, fname in BUILD.GRAINS:
        emb = page.grain_rows_as_dicts(stem)
        if emb is None:
            bad.append("%s block missing" % stem)
            continue
        p = os.path.join(project, fname)
        if not os.path.isfile(p):
            bad.append("%s missing on disk" % fname)
            continue
        hdr, rows = GG.load_csv(p)
        if emb != rows:
            n = sum(1 for a, b in zip(emb, rows) if a != b) + abs(len(emb) - len(rows))
            first = next(((i, a, b) for i, (a, b) in enumerate(zip(emb, rows)) if a != b), None)
            cell = ""
            if first:
                i, a, b = first
                ks = [k for k in b if a.get(k) != b.get(k)]
                cell = " first: row %d %s embedded=%s disk=%s" % (i, ks[:2], [a.get(k) for k in ks[:2]],
                                                                 [b.get(k) for k in ks[:2]])
            bad.append("%s: %d row(s) differ (embedded %d, disk %d)%s" % (stem, n, len(emb), len(rows), cell))
    g.check("H13c", "H13", not bad,
            "embedded rows == the CSV rows on disk as group D parses them, all four grains, cell for cell"
            + ("" if not bad else "; " + "; ".join(bad)))


def group_p(g, page):
    root = page.root
    ctl = {}
    for el in root.iter("fieldset"):
        c = el.get("data-control")
        if c:
            ctl[c] = el
    g.check("P1", "P", {"p. Metro", "p. Basis"} <= set(ctl),
            "both controls exist as <fieldset data-control>: got %s" % sorted(ctl))

    def saved(fs):
        checked = [i.get("value") for i in fs.iter("input") if i.get("checked") is not None]
        return fs.get("data-saved"), checked, [i.get("value") for i in fs.iter("input")]

    if "p. Metro" in ctl:
        ds, ch, opts = saved(ctl["p. Metro"])
        g.check("P2", "P", ds == "Columbus" and ch == ["Columbus"],
                "p. Metro saved state read from the MARKUP: data-saved=%s, checked=%s (F5B-7: Columbus)" % (ds, ch))
        g.check("P4", "P", opts == METROS,
                "p. Metro options are the eight metros in declared order" + ("" if opts == METROS else "; got %s" % opts))
    else:
        g.check("P2", "P", False, "p. Metro control absent")
        g.check("P4", "P", False, "p. Metro control absent")
    if "p. Basis" in ctl:
        ds, ch, opts = saved(ctl["p. Basis"])
        g.check("P3", "P", ds == "IT" and ch == ["IT"],
                "p. Basis saved state read from the MARKUP: data-saved=%s, checked=%s (swap OFF = IT)" % (ds, ch))
        g.check("P5", "P", opts == ["IT", "Metered"],
                "p. Basis options are [IT, Metered]" + ("" if opts == ["IT", "Metered"] else "; got %s" % opts))
    else:
        g.check("P3", "P", False, "p. Basis control absent")
        g.check("P5", "P", False, "p. Basis control absent")

    # P6 / P7 pre-rendered state groups
    for gid, v, attr, want, saved_val in (("P6", "V2", "data-state-metro", 8, "Columbus"),
                                          ("P7", "V1", "data-state-basis", 2, "IT")):
        slot, body, incomplete = find_view(root, v)
        if incomplete:
            g.skip(gid, "P", "slot %s declares build-incomplete: %d pre-rendered %s groups not yet gateable"
                   % (v, want, attr), blind=False)
            continue
        groups = [el for el in body.iter() if el.get(attr) is not None]
        vals = [el.get(attr) for el in groups]
        visible = [el.get(attr) for el in groups if el.get("hidden") is None]
        ok = len(groups) == want and len(set(vals)) == want and visible == [saved_val]
        g.check(gid, "P", ok,
                "%s has %d pre-rendered %s groups (want %d); the one NOT hidden in the markup is %s (want [%s])"
                % (v, len(groups), attr, want, visible, saved_val))



RAMP_STEPS = 7
GRID = 8            # --era-base, the page's grid unit (S4 gates the CSS declaration)
SLOT_ORDER = ["V1", "V2", "V3", "V4", "V5", "V6"]   # 5H-4: V1 leads, V6 below the anchor
LABEL_GAP = 8       # 5H-4: one grid unit between a V5 value label and its own mark


def gate_ordinal_ramp(values, n=RAMP_STEPS):
    """V4b's ramp clause, RE-DERIVED in Unit 5H-4 to the new rule (F5H3-7; the
    conventions in era_ph5_5h_results.md section 14 require the clause to be
    re-derived and re-fired by W13, never relaxed). Re-implemented here on
    purpose, exactly as its linear predecessor was: importing
    era_ph5_views.ordinal_ramp would make the clause assert only that the build
    agrees with itself.

    Step by ORDINAL position over the distinct values, not by linear magnitude.
    int(x + 0.5), not round(), so 3.10 / 3.11 / 3.13 agree (F5H0-5)."""
    order = sorted(set(values))
    N = len(order)
    if N == 0:
        return {}
    if N == 1:
        return {order[0]: 0}
    return {v: int(i * (n - 1) / (N - 1) + 0.5) for i, v in enumerate(order)}


INK_TAGS = ("rect", "circle", "line", "path", "text")


def view_ink(body):
    """The marks a view actually draws. Used by V4b's least-ink clause (5H-4)."""
    return sum(1 for el in body.iter() if el.tag in INK_TAGS)


def _affine_bad(marks, tol=1.5):
    """marks = [(pixel, value, label)]. Returns the pairs that do not lie on ONE
    affine map from value to pixel, within tol px of integer rounding. This is
    what 'the intervals span band_low/band_high' and 'the points are a plate
    carree of the station columns' actually MEAN, and it cannot be satisfied by
    an element that carries an attribute and draws nothing."""
    pairs = [(a, b) for i, a in enumerate(marks) for b in marks[i + 1:]
             if abs(a[1] - b[1]) > 1e-9]
    if not pairs:
        return ["no two marks with different values"], None
    wide = max(pairs, key=lambda ab: abs(ab[0][1] - ab[1][1]))
    slope = (wide[0][0] - wide[1][0]) / (wide[0][1] - wide[1][1])
    bad = []
    for a, b in pairs:
        if abs((a[0] - b[0]) - slope * (a[1] - b[1])) > tol:
            bad.append("%s/%s" % (a[2], b[2]))
    return bad, slope


def gate_wf_pairs(rows):
    """Unit 5H-4: the indices i of one metro's walk whose row i and row i+1
    SHARE a step. Re-implemented in the gate, and NOT imported from
    era_ph5_views, for the same reason gate_ordinal_ramp is.

    Row i+1 shares row i's end if either of its own endpoints equals it. The
    test is on the VALUES; no pixel, no scale and no view constant enters this
    gate at all — the connector's position is then asserted against the two
    bars the page actually drew, not against a pixel the gate recomputed.
    """
    out = []
    for i in range(len(rows) - 1):
        a, b = rows[i], rows[i + 1]
        if not (_walks(a) and _walks(b)):
            continue
        e = float(a["waterfall_end_usd"])
        if e == float(b["waterfall_start_usd"]) or e == float(b["waterfall_end_usd"]):
            out.append(i)
    return out


def _walks(r):
    return bool(r["waterfall_start_usd"]) and bool(r["waterfall_end_usd"])


def _row_rect(el):
    return next((c for c in el.iter() if c.tag == "rect"), None)


def band_crossings(G1):
    """The adjacency (or adjacencies) the +/-25 % bands touch, DERIVED from G1:
    a banded metro whose upper edge reaches past the central figure of a metro
    ranked below it. C-BAND-25 asserts there is exactly one anywhere in the
    table, so the count is itself a gate."""
    rank = sorted(G1, key=lambda r: int(r["rank"]))
    hits = []
    for a in rank:
        if a["is_market_priced"] != "1":
            continue
        for b in rank:
            if int(b["rank"]) > int(a["rank"]) and \
                    float(a["band_high_usd_per_it_mwh"]) > float(b["usd_per_it_mwh"]):
                hits.append((a["metro"], b["metro"]))
    return hits


def group_v(g, page, data):
    root = page.root
    G1 = data["G1"] if data else None
    G2 = data["G2"] if data else None
    G4 = data["G4"] if data else None

    def inc(gid, what):
        g.check(gid, "V", False, "%s — %s" % (what, BUILD_INCOMPLETE))

    # ---- V1
    slot, svg, incomplete = find_view(root, "V1")
    if incomplete:
        inc("V1a", "<svg data-view=V1> exists")
        inc("V1b", "V1 has 8 bar groups in rank order")
        inc("V1c", "V1 bars bound to usd_per_it_mwh (remainder + mitigation)")
    else:
        g.check("V1a", "V", True, "<svg data-view=V1> exists")
        want = [r["metro"] for r in sorted(G1, key=lambda r: int(r["rank"]))]
        states = {el.get("data-state-basis"): el
                  for el in svg.iter() if el.get("data-state-basis") is not None}
        # V1b / V1c are quantified PER PRE-RENDERED BASIS STATE (Unit 5H-1, F5H1-1).
        # The 5H-0 form quantified over the whole V1 svg, which cannot express the
        # two states 5H-0's own markup conventions require: it compared a 16-item
        # bar list against an 8-item one and took the UNION of the two states'
        # bindings. The per-state form is strictly stronger — it asserts the order
        # of BOTH states and tells the two bindings apart. Not a loosening.
        detail = []
        ok = bool(states)
        for name in sorted(states):
            bars = [el for el in states[name].iter()
                    if el.get("data-metro") is not None and el.get("data-role") == "bar"]
            order = [el.get("data-metro") for el in bars]
            if order != want:
                ok = False
            detail.append("%s: %d bar(s), rank order %s" % (name, len(order), order == want))
        g.check("V1b", "V", ok, "each basis state has its 8 bar groups in rank order — %s"
                % ("; ".join(detail) if detail else "NO data-state-basis group in V1"))
        wantf = {"IT": {"usd_per_it_mwh", "mitigated_usd_per_it_mwh", "mitigation_usd_per_it_mwh"},
                 "Metered": {"usd_per_mwh"}}
        got = {name: {el.get("data-field") for el in states[name].iter() if el.get("data-field")}
               for name in states}
        g.check("V1c", "V", got == wantf,
                "each basis state bound to its own basis and nothing else: %s"
                % {k: sorted(v) for k, v in sorted(got.items())})

    # ---- V2
    slot, svg, incomplete = find_view(root, "V2")
    if incomplete:
        inc("V2a", "<svg data-view=V2> exists")
        inc("V2b", "V2 has 8 metro groups each following waterfall_order with G2's row count")
        inc("V2c", "the three excluded siblings present in V2, muted fill + hairline")
    else:
        g.check("V2a", "V", True, "<svg data-view=V2> exists")
        bad = []
        for m in METROS:
            grp = [el for el in svg.iter() if el.get("data-state-metro") == m]
            if len(grp) != 1:
                bad.append("%s: %d groups" % (m, len(grp)))
                continue
            rows = [el for el in grp[0].iter() if el.get("data-component") is not None]
            want = sorted((r for r in G2 if r["metro"] == m), key=lambda r: int(r["waterfall_order"] or 0))
            if [el.get("data-component") for el in rows] != [r["component_id"] for r in want]:
                bad.append("%s order/count" % m)
            # CONNECTOR CLAUSE, NEW in Unit 5H-4 (F5H2-4, declared section 15.2
            # before the build). The pairs are RE-DERIVED from G2 here: two
            # consecutive walking rows are joined at the x they share, where
            # row i+1 shares row i's end if either of its own endpoints lands
            # on it. An excluded sibling has no position in the walk and is
            # never joined. Both the COUNT and each connector's x are asserted,
            # so an element carrying data-role="connector" and drawing nothing
            # cannot satisfy this.
            conn = [el for el in grp[0].iter() if el.get("data-role") == "connector"]
            pairs = gate_wf_pairs(want)
            if len(conn) != len(pairs):
                bad.append("%s: %d connector(s) for %d joined step pair(s)"
                           % (m, len(conn), len(pairs)))
            else:
                free = list(conn)
                for i in pairs:
                    # guard declared in era_ph5_5h_results.md section 15.3a: the
                    # pair indices come from G2, the rows come from the DRAWING,
                    # and a page that dropped a row from the middle of a walk
                    # would raise IndexError here. A gate that crashes has
                    # measured nothing (F5B-9). It fails instead.
                    if i + 1 >= len(rows):
                        bad.append("%s: G2 joins steps %d/%d but the page draws only %d row(s)"
                                   % (m, i, i + 1, len(rows)))
                        break
                    ra, rb = _row_rect(rows[i]), _row_rect(rows[i + 1])
                    if ra is None or rb is None:
                        bad.append("%s: a joined step has no drawn bar" % m)
                        break
                    ea = {int(ra.get("x")), int(ra.get("x")) + int(ra.get("width"))}
                    eb = {int(rb.get("x")), int(rb.get("x")) + int(rb.get("width"))}
                    ya = int(ra.get("y")) + int(ra.get("height"))
                    yb = int(rb.get("y"))
                    hit = next((el for el in free
                                if el.get("x1") == el.get("x2")
                                and int(el.get("x1")) in ea and int(el.get("x1")) in eb
                                and int(el.get("y1")) == ya and int(el.get("y2")) == yb), None)
                    if hit is None:
                        bad.append("%s: steps %d/%d share a value but no hairline joins the two "
                                   "drawn bars at a shared edge (x in %s and %s, y %d to %d)"
                                   % (m, i, i + 1, sorted(ea), sorted(eb), ya, yb))
                        break
                    free.remove(hit)
        g.check("V2b", "V", not bad,
                "8 V2 metro groups following waterfall_order, each joining its walk with one "
                "hairline connector per shared step (%d over the eight states)"
                % sum(1 for el in svg.iter() if el.get("data-role") == "connector")
                + ("" if not bad else "; " + "; ".join(bad)))
        ex = [r for r in G2 if r["included_in_mitigated_total"] == "0"]
        marks = [el for el in svg.iter() if el.get("data-excluded") == "1"]
        # V2c is quantified over the DRAWING as well as the attributes (Unit 5H-2,
        # declared in era_ph5_5h_results.md 10.2 BEFORE the correction was written).
        # The 5H-1 form asserted only the mark COUNT and data-muted="1" on each --
        # both attributes the build writes about itself, which three empty <g>
        # elements carrying two attributes and no mark at all would satisfy. Style
        # rule 3 requires the excluded siblings to be DRAWN in --era-muted with an
        # --era-rule hairline. The three added clauses assert that the mark is in
        # the waterfall order (it is never omitted), that a real <rect> carries the
        # class, and that the page's OWN CSS gives that class the muted fill and
        # the hairline stroke. Strictly stronger; no threshold moved; V2c passes
        # before and after, and the correction is what makes the pass mean what
        # the ruling says (F5H1-1, second form).
        muted = all(el.get("data-muted") == "1" for el in marks)
        in_order = all(el.get("data-component") is not None for el in marks)
        drawn = all(any(k.tag == "rect" and k.get("class") == "era-excluded"
                        for k in el.iter()) for el in marks)
        rule = re.search(r"\.era-excluded\s*\{([^}]*)\}", page.style_text())
        painted = bool(rule) and "fill: var(--era-muted)" in rule.group(1) \
            and "stroke: var(--era-rule)" in rule.group(1)
        g.check("V2c", "V",
                len(marks) == len(ex) and muted and in_order and drawn and painted,
                "excluded siblings drawn: %d marks for %d rows; all data-muted=%s; all in the "
                "waterfall order=%s; all carrying <rect class=era-excluded>=%s; .era-excluded is "
                "fill var(--era-muted) + stroke var(--era-rule) in the page CSS=%s"
                % (len(marks), len(ex), muted, in_order, drawn, painted))

    # ---- V3
    slot, svg, incomplete = find_view(root, "V3")
    if incomplete:
        inc("V3a", "<svg data-view=V3> exists")
        inc("V3b", "V3 five channels in F4E-3 order, rider first")
    else:
        g.check("V3a", "V", True, "<svg data-view=V3> exists")
        ch = [el.get("data-channel") for el in svg.iter() if el.get("data-channel")]
        ok = ch == V3_ORDER
        detail = []
        # SUB-GRID-UNIT CLAUSE, NEW in Unit 5H-4 (F5H1-4, declared section 15.2
        # before the build). A channel whose whole walk is narrower than one
        # grid unit put its credited label on top of the zero rule - measured,
        # the fixed channel's drawn extent is ONE pixel and its label landed on
        # the rule to the pixel. Everything below is read from the DRAWING: the
        # row's extent from its own rects, the rule's x from the drawn axis
        # line, the label's x from the label. No view constant enters here.
        axis = next((el for el in svg.iter()
                     if el.tag == "line" and el.get("class") == "era-axis"), None)
        if axis is None:
            ok = False
            detail.append("V3 draws no zero rule")
        else:
            zx = int(axis.get("x1"))
            narrow = []
            for grp in [el for el in svg.iter() if el.get("data-channel")]:
                rs = [c for c in grp.iter() if c.tag == "rect"]
                labs = [c for c in grp.iter()
                        if c.tag == "text" and c.get("class") == "era-value"]
                if not rs or not labs:
                    continue
                x0 = min(int(c.get("x")) for c in rs)
                x1 = max(int(c.get("x")) + int(c.get("width")) for c in rs)
                if x1 - x0 >= GRID:
                    continue
                narrow.append(grp.get("data-channel"))
                for lab in labs:
                    if abs(int(lab.get("x")) - zx) < GRID:
                        ok = False
                        detail.append("%s spans %d px (< one grid unit) and its credited label "
                                      "sits at x %s, %d px from the zero rule at %d"
                                      % (grp.get("data-channel"), x1 - x0, lab.get("x"),
                                         abs(int(lab.get("x")) - zx), zx))
        g.check("V3b", "V", ok,
                "V3 channel order %s; every row narrower than one grid unit carries its credited "
                "label clear of the zero rule" % ch
                + ("" if ok else "; " + "; ".join(detail[:3])))

    # ---- V4
    slot, svg, incomplete = find_view(root, "V4")
    if incomplete:
        inc("V4a", "<svg data-view=V4> exists")
        inc("V4b", "V4 has 8 points")
    else:
        g.check("V4a", "V", True, "<svg data-view=V4> exists")
        # V4b, RE-SCOPED in Unit 5H-3 (declared in era_ph5_5h_results.md §13.2
        # BEFORE the build and BEFORE this was written). The 5H-2 stub counted
        # eight elements carrying data-role="point" — an attribute the build
        # writes ABOUT ITSELF (F5H2-1) — and would have passed on eight empty
        # <g> with no circle, no coordinates and no colour. It asserted nothing
        # about the projection the ruling names. This form asserts the DRAWING,
        # re-derived from the grain: the metro set; plate-carree consistency on
        # both axes over all 28 pairs; ONE shared degrees-to-pixels scale;
        # north up; and the ramp step of each point against usd_per_it_mwh.
        # Scope, not threshold: it asserts strictly more.
        pts = [el for el in svg.iter() if el.get("data-role") == "point"]
        byname = {}
        for el in pts:
            byname[el.get("data-metro")] = el
        idx = {r["metro"]: r for r in G1}
        detail = []
        ok = len(pts) == 8 and sorted(byname) == sorted(idx)
        if not ok:
            detail.append("point set %s vs grain %s" % (sorted(byname), sorted(idx)))
        P = []
        if ok:
            for m in sorted(byname):
                el = byname[m]
                try:
                    P.append((m, float(el.get("cx")), float(el.get("cy")),
                              float(idx[m]["station_longitude"]), float(idx[m]["station_latitude"])))
                except (TypeError, ValueError):
                    ok = False
                    detail.append("%s: no numeric cx/cy" % m)
        sx = sy = None
        if ok:
            xbad, sx = _affine_bad([(a[1], a[3], a[0]) for a in P])
            ybad, sy = _affine_bad([(a[2], a[4], a[0]) for a in P])
            if xbad:
                ok = False
                detail.append("x not linear in longitude: %s" % xbad[:4])
            if ybad:
                ok = False
                detail.append("y not linear in latitude: %s" % ybad[:4])
        if ok:
            if abs(abs(sx) - abs(sy)) > 0.01 * max(abs(sx), abs(sy)):
                ok = False
                detail.append("degrees-per-pixel differs by axis: x %.4f, y %.4f (not plate carree)"
                              % (sx, sy))
            if sy >= 0:
                ok = False
                detail.append("y increases with latitude: north is DOWN")
        if ok:
            # RAMP CLAUSE, RE-DERIVED in Unit 5H-4 to the ORDINAL rule (F5H3-7,
            # declared in era_ph5_5h_results.md section 15.1/15.2 before the
            # build). The rule changed; the clause was re-derived to the new
            # rule and W13 re-fires it. Nothing was relaxed: it still asserts
            # every point's drawn colour against a step the gate derives from
            # the grain by its own implementation.
            steps = gate_ordinal_ramp([float(r["usd_per_it_mwh"]) for r in G1])
            for m in sorted(byname):
                want = "era-ramp-%d" % steps[float(idx[m]["usd_per_it_mwh"])]
                if want not in (byname[m].get("class") or "").split():
                    ok = False
                    detail.append("%s class %r, ramp wants %s" % (m, byname[m].get("class"), want))
        # NO-FRAME CLAUSE, NEW in Unit 5H-4 (F5H3-9, declared section 15.2). The
        # frame bounded the plot box rather than the projected extent and read
        # as an arbitrary rectangle; it is gone, and its absence is asserted of
        # the DRAWING, not of an attribute the build writes about itself.
        frame = [el for el in svg.iter() if el.tag == "line"]
        if frame:
            ok = False
            detail.append("V4 draws %d <line>; the frame was dropped in 5H-4 (F5H3-9)" % len(frame))
        # LEAST-INK CLAUSE, NEW in Unit 5H-4 (section 15.2, amended 15.2a). The
        # ruling's own words for this view are "V4 gets the least ink"; this is
        # that sentence made measurable. Comparison set: the other four SVG
        # views. V6 is a <table> and draws no marks at all, so including it
        # would make the clause unsatisfiable for every view (15.2a).
        v4_ink = view_ink(svg)
        others = {}
        for other in ("V1", "V2", "V3", "V5"):
            _s, obody, oinc = find_view(root, other)
            if oinc or obody is None or obody.tag != "svg":
                continue
            others[other] = view_ink(obody)
        heavier = sorted(k for k, n in others.items() if n <= v4_ink)
        if others and heavier:
            ok = False
            detail.append("V4 ink %d is not strictly least: %s" % (v4_ink, heavier))
        g.check("V4b", "V", ok,
                "V4 %d points = the grain's eight, plate carree on station_longitude/"
                "station_latitude (one scale %s px/deg, north up), ORDINAL ramp step from "
                "usd_per_it_mwh, no frame line, least ink %d vs %s"
                % (len(pts), "%.4f" % abs(sx) if sx else "n/a", v4_ink,
                   {k: others[k] for k in sorted(others)})
                + ("" if ok else "; " + "; ".join(detail[:4])))

    # ---- V5
    slot, svg, incomplete = find_view(root, "V5")
    if incomplete:
        inc("V5a", "<svg data-view=V5> exists")
        inc("V5b", "V5 intervals span band_low/band_high")
    else:
        g.check("V5a", "V", True, "<svg data-view=V5> exists")
        # V5b, RE-SCOPED in Unit 5H-3 (declared §13.2 before the build). The
        # 5H-2 stub was named "V5 intervals span band_low/band_high" and
        # asserted len(iv) >= 3 — no span, no membership, and a >= that accepts
        # any surplus. Three empty <g data-role="interval"> would have PASSED.
        # This form asserts the SET (re-derived from is_market_priced and
        # has_bracket, never listed) and the SPAN (one affine map from cell to
        # pixel over every low edge, high edge and central mark).
        iv = [el for el in svg.iter() if el.get("data-role") == "interval"]
        idx = {r["metro"]: r for r in G1}
        want = sorted([(r["metro"], "band") for r in G1 if r["is_market_priced"] == "1"] +
                      [(r["metro"], "bracket") for r in G1 if r["has_bracket"] == "1"])
        got = sorted((el.get("data-metro"), el.get("data-kind")) for el in iv)
        detail = []
        ok = got == want
        if not ok:
            detail.append("interval set %s, grain wants %s" % (got, want))
        marks = []
        if ok:
            for el in iv:
                m, kind = el.get("data-metro"), el.get("data-kind")
                lof, hif = el.get("data-low-field"), el.get("data-high-field")
                rect = next((c for c in el.iter() if c.get("data-edge") == "span"), None)
                if rect is None or not lof or not hif or lof not in idx[m] or hif not in idx[m]:
                    ok = False
                    detail.append("%s/%s: no spanning rect or unusable fields" % (m, kind))
                    continue
                try:
                    x, w = float(rect.get("x")), float(rect.get("width"))
                except (TypeError, ValueError):
                    ok = False
                    detail.append("%s/%s: rect has no numeric x/width" % (m, kind))
                    continue
                marks.append((x, float(idx[m][lof]), "%s/%s.low" % (m, kind)))
                marks.append((x + w, float(idx[m][hif]), "%s/%s.high" % (m, kind)))
        centrals = {}
        for el in svg.iter():
            if el.get("data-role") != "central":
                continue
            cell, err = resolve_src(el.get("data-src") or "", data)
            if err or el.get("x1") is None:
                ok = False
                detail.append("central mark %s: %s" % (el.get("data-metro"), err or "no x1"))
                continue
            centrals[el.get("data-metro")] = el
            marks.append((float(el.get("x1")), float(cell), "%s.central" % el.get("data-metro")))
        for m, kind in want:
            if kind == "band" and m not in centrals:
                ok = False
                detail.append("band row %s carries no central mark" % m)
        if ok:
            bad, slope = _affine_bad(marks)
            if bad:
                ok = False
                detail.append("marks not on one scale: %s" % bad[:4])
        # LABEL-ANCHOR CLAUSE, NEW in Unit 5H-4 (F5H3-8, declared section 15.2
        # before the build). The value labels used to sit at two fixed ROW
        # positions, so a 14 px bracket read as spanning the row and the
        # crossing guide overprinted a central label. Every term below is a
        # DRAWN coordinate compared to a DRAWN coordinate: the label's x
        # against the rect it belongs to, and against the tick it belongs to.
        # THIS IS ALSO THE OVERPRINT CLAUSE — there is no second one, because
        # anchoring the central label a grid unit right of its own tick is what
        # makes the guide unable to cross the glyphs.
        anch = []
        for el in iv:
            m, kind = el.get("data-metro"), el.get("data-kind")
            rect = next((c for c in el.iter() if c.get("data-edge") == "span"), None)
            lo_l = next((c for c in el.iter() if c.get("data-role") == "label-low"), None)
            hi_l = next((c for c in el.iter() if c.get("data-role") == "label-high"), None)
            if rect is None or lo_l is None or hi_l is None:
                anch.append("%s/%s: missing rect or edge label" % (m, kind))
                continue
            rx, rw = int(rect.get("x")), int(rect.get("width"))
            if int(lo_l.get("x")) != rx - LABEL_GAP or lo_l.get("text-anchor") != "end":
                anch.append("%s/%s low label at %s/%s, wants %d/end"
                            % (m, kind, lo_l.get("x"), lo_l.get("text-anchor"), rx - LABEL_GAP))
            if int(hi_l.get("x")) != rx + rw + LABEL_GAP or hi_l.get("text-anchor") != "start":
                anch.append("%s/%s high label at %s/%s, wants %d/start"
                            % (m, kind, hi_l.get("x"), hi_l.get("text-anchor"), rx + rw + LABEL_GAP))
            cen = next((c for c in el.iter() if c.get("data-role") == "central"), None)
            cl = next((c for c in el.iter() if c.get("data-role") == "label-central"), None)
            if cen is None and cl is None:
                continue
            if cen is None or cl is None:
                anch.append("%s/%s has a central tick without its label, or the reverse" % (m, kind))
                continue
            if int(cl.get("x")) != int(cen.get("x1")) + LABEL_GAP or cl.get("text-anchor") != "start":
                anch.append("%s/%s central label at %s/%s, wants %d/start"
                            % (m, kind, cl.get("x"), cl.get("text-anchor"),
                               int(cen.get("x1")) + LABEL_GAP))
        if anch:
            ok = False
            detail.append("labels not anchored to their marks: %s" % anch[:3])
        g.check("V5b", "V", ok,
                "V5 %d intervals = the grain's %d (3 bands + 2 published pairs); every low edge, "
                "high edge and central mark on ONE scale against its own cell; every value label "
                "anchored to its own mark at %d px" % (len(iv), len(want), LABEL_GAP)
                + ("" if ok else "; " + "; ".join(detail[:4])))

    # ---- V6
    slot, tbl, incomplete = find_view(root, "V6")
    if incomplete:
        inc("V6a", "<table data-view=V6> exists")
        inc("V6b", "V6 21 rows by sort_rank, unpriced above limitations, C-FERC-* first with no dollar")
    else:
        g.check("V6a", "V", True, "<table data-view=V6> exists")
        # V6b, RE-SCOPED in Unit 5H-3 (declared §13.2 before the build). The
        # 5H-2 stub asserted order, count and FERC-first only; TWO of the three
        # things its own text claimed ("unpriced above limitations", "with no
        # dollar") were asserted nowhere, and 21 <tr data-caveat> carrying that
        # attribute and NO TEXT would have PASSED (F5H2-1). Clauses 4-6 added.
        rows = [el for el in tbl.iter() if el.get("data-caveat") is not None]
        ids = [el.get("data-caveat") for el in rows]
        want = [r["caveat_id"] for r in sorted(G4, key=lambda r: int(r["sort_rank"]))]
        first_ok = bool(ids) and ids[0].startswith("C-FERC-")
        detail = []
        ok = ids == want and len(ids) == 21 and first_ok
        if not ok:
            detail.append("order == sort_rank: %s, %d rows, FERC first: %s"
                          % (ids == want, len(ids), first_ok))
        # (4) every row carries >= 5 cells, each credited to that row's OWN id
        for el in rows:
            cid = el.get("data-caveat")
            cells = [c for c in el.iter() if c.get("data-src")]
            if len(cells) < 5:
                ok = False
                detail.append("%s: %d credited cells" % (cid, len(cells)))
            for c in cells:
                if not (c.get("data-src") or "").startswith("era_ph5_caveat:%s:" % cid):
                    ok = False
                    detail.append("%s: cell credited to %r" % (cid, c.get("data-src")))
        # (5) the FERC floor shows NO dollar — which is the point (5C)
        for el in rows:
            if not (el.get("data-caveat") or "").startswith("C-FERC-"):
                continue
            for c in el.iter():
                col = (c.get("data-src") or "").rsplit(":", 1)[-1]
                if col in ("usd_per_year", "usd_per_it_mwh") and own_text(c).strip():
                    ok = False
                    detail.append("FERC row shows %s = %r" % (col, own_text(c).strip()))
        # (6) unpriced strictly above limitations, read off the DRAWN category
        cats = []
        for i, el in enumerate(rows):
            c = next((x for x in el.iter()
                      if (x.get("data-src") or "").endswith(":category")), None)
            cats.append((i, own_text(c).strip() if c is not None else ""))
        unp = [i for i, c in cats if c == "unpriced"]
        lim = [i for i, c in cats if c == "limitation"]
        if unp and lim and max(unp) >= min(lim):
            ok = False
            detail.append("an unpriced row at %d sits below a limitation row at %d"
                          % (max(unp), min(lim)))
        g.check("V6b", "V", ok,
                "V6 %d rows in sort_rank order, FERC first with no dollar, every cell credited to "
                "its own caveat_id, %d unpriced all above %d limitation rows"
                % (len(ids), len(unp), len(lim))
                + ("" if ok else "; " + "; ".join(detail[:4])))
    anchors = [a for a in root.iter("a") if a.get("href") == "#V6"]
    header = None
    for el in root.iter("header"):
        header = el
        break
    in_header = header is not None and any(a.get("href") == "#V6" for a in header.iter("a"))
    # COMPOSITION CLAUSE, NEW in Unit 5H-4 (declared era_ph5_5h_results.md
    # section 15.2 before the build). The ruling's assembly sentence is "V1
    # leads, V4 gets the least ink, V6 below the anchor"; V4's half is gated in
    # V4b, and this is V1's and V6's. Why it is not redundant with H5/H6: those
    # rebuild the page from the same era_ph5_build_html.py they are checking, so
    # a reordering of that file's VIEWS constant reproduces itself exactly and
    # H6 stays PASS. H6 sees page edits; it cannot see build-code edits — which
    # is the same reason every drawing clause in this unit exists.
    order = [el.get("data-view") for el in root.iter()
             if el.tag == "section" and el.get("data-view")]
    composed = order == SLOT_ORDER
    g.check("V6c", "V", bool(anchors) and in_header and composed,
            "a one-click anchor href=#V6 exists in the header (P5-3): %d anchor(s), in header %s; "
            "slots in document order %s (V1 leads, V6 below the anchor)"
            % (len(anchors), in_header, order)
            + ("" if composed else "; declared order is %s" % SLOT_ORDER))


def group_b(g, page, data):
    root = page.root

    def inc(gid, what):
        g.check(gid, "B", False, "%s — %s" % (what, BUILD_INCOMPLETE))

    slot, svg, incomplete = find_view(root, "V1")
    if incomplete:
        inc("B1", "V1's saved (not hidden) state is the IT basis on usd_per_it_mwh")
        inc("B2", "the metered-swap state's remainder is 0 and its label says so (F5B-2)")
    else:
        states = [el for el in svg.iter() if el.get("data-state-basis") is not None]
        vis = [el for el in states if el.get("hidden") is None]
        g.check("B1", "B", len(vis) == 1 and vis[0].get("data-state-basis") == "IT"
                and vis[0].get("data-axis-field") == "usd_per_it_mwh",
                "V1 visible state %s, axis field %s"
                % ([v.get("data-state-basis") for v in vis], [v.get("data-axis-field") for v in vis]))
        met = [el for el in states if el.get("data-state-basis") == "Metered"]
        ok = bool(met) and met[0].get("data-remainder") == "0" and "baseline tariff rate only" in \
            " ".join(own_text(e) for e in met[0].iter()).lower()
        g.check("B2", "B", ok, "metered swap: remainder 0 and label says 'baseline tariff rate only'")

    hits = []
    for el, t in iter_text_elements(root):
        for lit in BANNED_METERED_LITERALS:
            if re.search(r"(?<![\d.])" + re.escape(lit) + r"(?![\d])", t):
                hits.append((lit, t[:40]))
    g.check("B3", "B", not hits,
            "the metered band-crossing literals %s never appear as page text (F5A-4; the FACILITY figure is 0.8042)"
            % BANNED_METERED_LITERALS + ("" if not hits else "; found %s" % hits[:3]))

    slot, svg, incomplete = find_view(root, "V5")
    if incomplete:
        inc("B4", "any shown band-crossing figure carries data-src to G4 C-BAND-25 (FACILITY figure)")
    else:
        # B4, RE-SCOPED in Unit 5H-3 (declared §13.2 before the build). The
        # 5H-2 stub required one element carrying data-role="crossing" with a
        # C-BAND-25 credit — an attribute the build writes about itself — and
        # would have PASSED on a page that showed no crossing at all (F5H2-1).
        # Clauses added: the annotation's TEXT equals the cell it cites; both
        # endpoint cells of the derived adjacency are shown and credited; and
        # THE CROSSING IS ASSERTED AS GEOMETRY — the drawn upper edge of the
        # crossing band lies strictly right of the drawn central mark it
        # crosses. The adjacency itself is derived from G1, never named here,
        # and C-BAND-25's "the ONLY adjacency" is gated as a count.
        # NOTE (§13.1): no crossing FIGURE is printed. C-BAND-25's 0.8042 is on
        # the $/MWh axis and V5 is drawn on $/IT-MWh, where the same adjacency
        # crosses by 1.0810 — a difference of two cells, which exists in no
        # cell (F5H1-5). The figure is carried by the two endpoint cells and by
        # the drawing. Do not "improve" this into 0.8042 (B3 also forbids the
        # metered 0.9742 as page text and that stands).
        G1 = data["G1"] if data else None
        cross = [el for el in svg.iter() if el.get("data-role") == "crossing"]
        detail = []
        ok = bool(cross)
        if not ok:
            detail.append("no data-role=crossing element in V5")
        for el in cross:
            src = el.get("data-src") or ""
            if not src.startswith("era_ph5_caveat:C-BAND-25:"):
                ok = False
                detail.append("crossing credited %r" % src)
                continue
            cell, err = resolve_src(src, data)
            if err or own_text(el).strip() != str(cell).strip():
                ok = False
                detail.append("crossing shows %r, cell %r" % (own_text(el).strip()[:40], str(cell)[:40]))
        hits = band_crossings(G1) if G1 else []
        if len(hits) != 1:
            ok = False
            detail.append("G1 yields %d band adjacencies; C-BAND-25 says exactly one" % len(hits))
        if len(hits) == 1:
            hi_m, lo_m = hits[0]
            shown = set()
            for el in root.iter():
                if el.get("data-src") and own_text(el).strip():
                    shown.add(el.get("data-src"))
            need = {"era_ph5_metro:%s:band_high_usd_per_it_mwh" % hi_m,
                    "era_ph5_metro:%s:usd_per_it_mwh" % lo_m}
            missing = need - shown
            if missing:
                ok = False
                detail.append("endpoint cell(s) not shown and credited: %s" % sorted(missing))
            band = next((el for el in svg.iter() if el.get("data-metro") == hi_m
                         and el.get("data-kind") == "band"), None)
            cen = next((el for el in svg.iter() if el.get("data-role") == "central"
                        and el.get("data-metro") == lo_m), None)
            rect = next((c for c in band.iter() if c.get("data-edge") == "span"), None) \
                if band is not None else None
            if rect is None or cen is None:
                ok = False
                detail.append("cannot read the drawn %s band or the drawn %s central mark" % (hi_m, lo_m))
            else:
                right = float(rect.get("x")) + float(rect.get("width"))
                cx = float(cen.get("x1"))
                if not right > cx:
                    ok = False
                    detail.append("%s band ends at %g, %s central at %g — no crossing is DRAWN"
                                  % (hi_m, right, lo_m, cx))
        g.check("B4", "B", ok,
                "the one derived band adjacency %s is drawn crossing and named from "
                "era_ph5_caveat:C-BAND-25 (%d annotation(s)); no crossing figure is typed (§13.1)"
                % (hits[0] if len(hits) == 1 else "n/a", len(cross))
                + ("" if ok else "; " + "; ".join(detail[:4])))


def read_style(g, style_path):
    if not os.path.isfile(style_path):
        g.check("S0a", "S", False, "%s not found" % style_path)
        return None
    txt = open(style_path, encoding="utf-8").read()
    hexes = {h.upper() for h in HEX_RE.findall(txt)}
    sizes = set()
    for line in txt.splitlines():
        m = re.match(r"^\|\s*(caption|body|label|subhead|title)\s*\|\s*(\d+)\s*\|", line)
        if m:
            sizes.add(int(m.group(2)))
    fam = re.search(r"`(Helvetica Neue[^`]*)`", txt)
    g.check("S0a", "S", len(hexes) == 13, "%s declares %d colour tokens (13 expected)" % (os.path.basename(style_path), len(hexes)))
    g.check("S0b", "S", sizes == SIZES, "%s declares five type sizes %s" % (os.path.basename(style_path), sorted(sizes)))
    g.check("S0c", "S", fam is not None, "%s declares one type family" % os.path.basename(style_path))
    return {"hex": hexes, "sizes": sizes,
            "family": (fam.group(1).strip() if fam else None)}


def group_s(g, page, style):
    root = page.root
    css = page.style_text()
    if style is None:
        for gid in ("S1", "S2", "S3", "S4", "S5"):
            g.check(gid, "S", False, "no token file")
        return
    # S1 every hex in the page
    found = []
    for h in HEX_RE.findall(css):
        found.append((h.upper(), "css"))
    for el in root.iter():
        for k in ("fill", "stroke", "color", "stop-color", "flood-color", "style", "bgcolor"):
            v = el.get(k)
            if v:
                for h in HEX_RE.findall(v):
                    found.append((h.upper(), "%s@%s" % (k, el.tag)))
    off = [(h, w) for h, w in found if h not in style["hex"]]
    g.check("S1", "S", bool(found) and not off,
            "%d hex colours in the page, all among the 13 tokens" % len(found)
            + ("" if not off else "; OFF-TOKEN: %s" % off[:5])
            + ("" if found else "; VACUOUS — no colour declared"))
    # S2 every font-size
    sizes = []
    for m in FONT_SIZE_CSS_RE.finditer(css):
        sizes.append((float(m.group(1)), m.group(2) or "", "css"))
    for m in FONT_SIZE_VAR_RE.finditer(css):
        sizes.append((float(m.group(1)), "px", "css-var"))
    for el in root.iter():
        v = el.get("font-size")
        if v:
            m = re.match(r"(\d+(?:\.\d+)?)(px)?", v)
            if m:
                sizes.append((float(m.group(1)), m.group(2) or "", "attr@%s" % el.tag))
        st = el.get("style") or ""
        for m in FONT_SIZE_CSS_RE.finditer(st):
            sizes.append((float(m.group(1)), m.group(2) or "", "style@%s" % el.tag))
    off = [s for s in sizes if not (s[0] in SIZES and s[1] in ("px", ""))]
    g.check("S2", "S", bool(sizes) and not off,
            "%d font-size declarations, all in %s px" % (len(sizes), sorted(SIZES))
            + ("" if not off else "; OFF-SCALE: %s" % off[:5])
            + ("" if sizes else "; VACUOUS — no size declared"))
    # S3 one family
    fams = set()
    for m in FONT_FAMILY_RE.finditer(css):
        fams.add(re.sub(r"\s+", " ", m.group(1).strip().rstrip(";")))
    for el in root.iter():
        v = el.get("font-family")
        if v:
            fams.add(re.sub(r"\s+", " ", v.strip()))
    want = re.sub(r"\s+", " ", style["family"] or "")
    g.check("S3", "S", fams == {want},
            "exactly one font-family and it is the token family: %s" % sorted(fams))
    # S4 grid constants
    ok = (re.search(r"--era-base\s*:\s*8px", css) and re.search(r"--era-margin\s*:\s*48px", css)
          and re.search(r"--era-gutter\s*:\s*24px", css))
    g.check("S4", "S", bool(ok), "CSS declares --era-base 8px, --era-margin 48px, --era-gutter 24px")
    # S5 svg dimensions
    svgs = list(root.iter("svg"))
    if not svgs:
        g.skip("S5", "S", "0 <svg> elements on the page (slots build-incomplete); dimension gate not exercised", blind=False)
    else:
        bad = []
        for s in svgs:
            for k in ("width", "height"):
                v = s.get(k)
                if v is None or not v.isdigit() or int(v) % 8 != 0:
                    bad.append("%s=%s on svg[data-view=%s]" % (k, v, s.get("data-view")))
        g.check("S5", "S", not bad, "%d svg(s), every width/height a multiple of 8" % len(svgs)
                + ("" if not bad else "; " + "; ".join(bad[:4])))


def resolve_src(src, data):
    try:
        stem, key, col = src.split(":", 2)
    except ValueError:
        return None, "malformed data-src %r" % src
    stemmap = {"era_ph5_metro": "G1", "era_ph5_stack": "G2", "era_ph5_month": "G3", "era_ph5_caveat": "G4"}
    if stem not in stemmap or data is None:
        return None, "unknown grain %r" % stem
    keycols = BUILD.ROW_KEYS[stem]
    for r in data[stemmap[stem]]:
        if "|".join(r[k] for k in keycols) == key:
            if col not in r:
                return None, "no column %r in %s" % (col, stem)
            return r[col], None
    return None, "no row %r in %s" % (key, stem)


def group_t(g, page, data):
    root = page.root
    scanned = 0
    numeric = []
    for el, t in iter_text_elements(root):
        scanned += 1
        if FIGURE_RE.search(t) or NUMBER_RE.match(t):
            numeric.append((el, t))
    uncredited = [(el.tag, t[:30]) for el, t in numeric if not el.get("data-src")]
    g.check("T1", "T", scanned >= 1 and len(uncredited) == 0,
            "uncredited numeric text count = %d (%d numeric of %d text elements scanned)"
            % (len(uncredited), len(numeric), scanned)
            + ("" if not uncredited else "; UNCREDITED: %s" % uncredited[:5])
            + ("" if scanned else "; VACUOUS — nothing scanned"))
    # T2, WIDENED in Unit 5H-3 from "every credited NUMERIC text" to "every
    # credited text" (declared in era_ph5_5h_results.md §13.4b BEFORE it was
    # written, after W12 MISSED because nothing in group T ever read a
    # non-numeric credited label). SCOPE, not threshold: no tolerance moves and
    # no gate id is added. §12's convention "credit every label drawn from a
    # grain" put ~159 credited labels on this page that nothing compared to the
    # cells they cite; a build could have named any cell beside any text.
    credited = [(el, own_text(el).strip()) for el in root.iter()
                if el.get("data-src") and el.tag not in ("script", "style")
                and own_text(el).strip()]
    if not credited:
        g.skip("T2", "T", "0 credited text elements on the page (no view built); cell-equality gate not exercised", blind=False)
        return
    bad = []
    for el, t in credited:
        cell, err = resolve_src(el.get("data-src"), data)
        if err:
            bad.append(err)
            continue
        # F5H1-3, closed in Unit 5H-4 (declared section 15.1 before the run).
        # U+2212 used to sit INSIDE the stripped class, so the .replace that
        # followed could never see one. The silent pass that created is not the
        # obvious one: a NEGATIVE cell shown with a typographic minus still
        # failed on magnitude, but a POSITIVE cell shown as "-X" normalised to
        # "X" and COMPARED EQUAL. The page could print the negation of a cell
        # and T2 would call it the cell. Translate first, strip second. No
        # figure on this page moves - fmt2/fmt6 emit the ASCII hyphen-minus -
        # so this is a hardening, and W20 is the positive that proves it is one.
        shown = re.sub(r"[,$%\s]", "", t.replace("−", "-"))
        try:
            sv = float(shown)
            cv = float(cell)
        except ValueError:
            if t.strip() != str(cell).strip():
                bad.append("%s shows %r, cell %r" % (el.get("data-src"), t[:20], cell))
            continue
        dec = len(shown.split(".")[1]) if "." in shown else 0
        if abs(sv - cv) > 0.5 * 10 ** (-dec) + 1e-9:
            bad.append("%s shows %s, cell %s" % (el.get("data-src"), shown, cell))
    g.check("T2", "T", not bad,
            "%d credited text elements equal the cells they cite (figures to the precision shown)" % len(credited)
            + ("" if not bad else "; " + "; ".join(bad[:5])))


# --------------------------------------------------------------------------
def summarize(logpath):
    if not os.path.isfile(logpath):
        print("no log at %s" % logpath)
        return 1
    rows = [l.rstrip() for l in open(logpath, encoding="utf-8")
            if l.startswith(("PASS ", "FAIL ", "SKIP", "NOTE "))]
    p = sum(1 for r in rows if r.startswith("PASS"))
    f = sum(1 for r in rows if r.startswith("FAIL"))
    sb = sum(1 for r in rows if r.startswith("SKIP-BLIND"))
    so = sum(1 for r in rows if r.startswith("SKIP-OK"))
    print("SUMMARY %s: %d PASS, %d FAIL, %d SKIP-BLIND, %d SKIP-OK" % (logpath, p, f, sb, so))
    for r in rows:
        if r.startswith(("FAIL", "SKIP-BLIND")):
            print("  " + r)
    return 0 if (f == 0 and sb == 0) else 1


def run(project, page_path, groups, style_path):
    g = GG.Gate()
    data = None
    if "D" in groups:
        data = GG.group_d(g, project)
    else:
        try:
            data = {"headers": {}}
            for gid, stem, fname in BUILD.GRAINS:
                data[gid] = GG.load_csv(os.path.join(project, fname))[1]
        except OSError:
            data = None
    style = read_style(g, style_path) if "S" in groups else None
    if not os.path.isfile(page_path):
        for grp in ("H", "H13", "P", "V", "B", "S", "T"):
            if grp in groups:
                g.check(grp + "*", grp, False, "PAGE NOT PRESENT at %s — FAIL, never SKIP" % page_path)
        return g
    page = Page(page_path)
    if "H" in groups:
        group_h(g, page, project, style_path)
    if page.root is None:
        for grp in ("H13", "P", "V", "B", "S", "T"):
            if grp in groups:
                g.check(grp + "*", grp, False, "page unparseable: %s" % page.error)
        return g
    if "H13" in groups:
        group_h13(g, page, project, data)
    if "P" in groups:
        group_p(g, page)
    if "V" in groups:
        group_v(g, page, data)
    if "B" in groups:
        group_b(g, page, data)
    if "S" in groups:
        group_s(g, page, style)
    if "T" in groups:
        group_t(g, page, data)
    return g


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", default=".")
    ap.add_argument("--page", default=None)
    ap.add_argument("--groups", default=None)
    ap.add_argument("--log", default=None)
    ap.add_argument("--summary", action="store_true")
    ap.add_argument("--quiet", action="store_true")
    ap.add_argument("--style", default=None,
                    help="token file group S compares against (tamper W35 only; default is the "
                         "project's era_ph5_style_v1.0.md). The H5/H6 rebuild always reads the project's.")
    a = ap.parse_args()
    if a.summary:
        return summarize(a.log or "era_ph5_5h_gate_run.log")

    groups = set((a.groups or "D,H,H13,P,V,B,S,T").split(","))
    page_path = a.page or os.path.join(a.project, PAGE_NAME)
    if not os.path.isabs(page_path) and os.path.dirname(page_path) == "":
        page_path = os.path.join(a.project, page_path)
    style_path = a.style or os.path.join(a.project, STYLE_MD)

    out = ["era_ph5_page_gate.py  Unit 5H-4  project=%s  page=%s  python=%s  platform=%s%s"
           % (os.path.abspath(a.project), os.path.basename(page_path), sys.version.split()[0],
              platform.platform(), "" if a.style is None else "  style=%s (OVERRIDDEN on the command line)" % a.style),
           "DECLARED (era_ph5_5h_results.md §15.3, assembly + the six drawing findings): 75 PASS; 0 FAIL; 0 SKIP-OK; 0 SKIP-BLIND.",
           "  V4b (ordinal ramp, no frame, least ink), V5b (labels anchored to their marks), V3b (sub-grid-unit",
           "  label clear of the zero rule), V2b (waterfall connectors) and V6c (slot order) assert the DRAWING;",
           "  T2's normaliser now TRANSLATES U+2212 instead of stripping it (F5H1-3). No id added, no threshold moved.",
           ""]
    if os.path.isfile(page_path):
        out[0] += "  page_md5=%s" % md5_of(page_path)
    g = run(a.project, page_path, groups, style_path)
    for gid, grp, status, msg in g.rows:
        out.append("%-10s [%s] %-14s %s" % (status, grp, gid, msg))
    npass = sum(1 for r in g.rows if r[2] == "PASS")
    nfail = sum(1 for r in g.rows if r[2] == "FAIL")
    nblind = sum(1 for r in g.rows if r[2] == "SKIP-BLIND")
    nskip = sum(1 for r in g.rows if r[2] == "SKIP-OK")
    fails = sorted(r[0] for r in g.rows if r[2] == "FAIL")
    out.append("")
    out.append("RESULT %d PASS  %d FAIL  %d SKIP-BLIND  %d SKIP-OK" % (npass, nfail, nblind, nskip))
    out.append("FAIL SET %s" % (" ".join(fails) if fails else "(empty)"))
    txt = "\n".join(out)
    if not a.quiet:
        print(txt)
    if a.log:
        with open(a.log, "a", encoding="utf-8") as fh:
            fh.write(txt + "\n\n")
    return 0 if (nfail == 0 and nblind == 0) else 1


if __name__ == "__main__":
    sys.exit(main())
