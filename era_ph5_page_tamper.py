#!/usr/bin/env python3
"""era_ph5_page_tamper.py — Unit 5H-0 of direction_ph5_html_v1.0.md (H-2, F5B-3)

This section is intended to PROVE THE PAGE GATE IS CONNECTED by injecting
declared defects into a temp copy of the project and requiring the gate to
fire on EXACTLY the declared set of gate ids — no undeclared firing, nothing
declared but silent. Every case's firing set is declared in this file and in
era_ph5_5h_results.md BEFORE the suite runs. The firing set of a case is
FAIL(case) minus FAIL(clean baseline), so the build-incomplete FAILs of a
partial page cancel; the baseline must itself equal the declared
build-incomplete set or the suite aborts NOT CONNECTED.

Order (F5B-3): W01 FIRST, always — the positive that proves the harness is
wired. It was NOT RUNNABLE in 5H-0 (V1 was a build-incomplete slot) and printed
so; from 5H-1, with V1 built, it runs and leads the suite. W02 is 5H-1's
positive for V3. W03/W04/W05 are 5H-2's positives for V2 and the metro control;
W06 is the positive for V2c's 5H-2 clauses (see era_ph5_5h_results.md §10.3a).
Then W-cases in id order; controls N* LAST. A --cases list that begins with a
control is REFUSED.

Kinds
  grain   mutate a CSV in the temp copy, run era_ph5_grain_gate.py alone
  page    build the clean page in the temp copy, edit the PAGE, run the page gate
  input   build the clean page, then perturb an INPUT on disk, run the page gate
  build   rebuild the page under altered conditions (W34 twice; W35 altered tokens)
  control clean copy, nothing fires

Usage
-----
  python era_ph5_page_tamper.py --project . --log era_ph5_5h_tamper_run.log
  python era_ph5_page_tamper.py --project . --cases W01,W30,W31 --log ...
  python era_ph5_page_tamper.py --summary --log era_ph5_5h_tamper_run.log
"""

import argparse
import csv
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
GRAIN_FILES = ["era_ph5_metro.csv", "era_ph5_stack.csv", "era_ph5_month.csv", "era_ph5_caveat.csv"]
SUPPORT = ["era_ph5_grains_manifest.json", "era_ph5_style_v1.0.md", "era_ph5_dictionary_v1.0.md"]
STYLE_MD = "era_ph5_style_v1.0.md"
PAGE = "era_ph5_dashboard.html"

# THE BASELINE IS NOW EMPTY (Unit 5H-3). All six views are built, the page gate
# reaches 0 FAIL and the page is ACCEPTED, so every firing set below is ABSOLUTE
# rather than relative to a build-incomplete remainder. EVERY carried set was
# RE-DERIVED against the six-view page, case by case, in era_ph5_5h_results.md
# §13.4 — a declared set is not inherited (F5H1-2). Fifteen held; W31 GREW by
# {V4b, V5b}, because a colour and a position are freshness assertions in
# exactly the way 5H-1 found a credited figure to be.
BASELINE = set()

# case: (kind, declared firing set, why)
CASES = {
    "W01": ("page", {"V1c", "H6"},
            "V1's IT-state bars rebound from mitigated_usd_per_it_mwh to mitigated_annual_usd. The "
            "geometry the build already wrote does not move (F5B-4), so only the BINDING gate can "
            "see it; V1b stays PASS, which is what proves the edit is scoped. H6 by construction "
            "(F5H0-3): the page no longer equals its rebuild. RUNS FIRST from 5H-1 on (F5B-3)."),
    "W02": ("page", {"V3b", "H6"},
            "V3's first two data-channel values swapped (rider <-> energy). V3b compares the five "
            "against V3_ORDER, which IS F4E-3; nothing else on the page reads data-channel. H6 by "
            "F5H0-3."),
    "W03": ("page", {"V2b", "V2c", "H6"},
            "Columbus's excluded sibling row <g> is DELETED from its state group — the ruling's literal "
            "'sibling row dropped'. V2c sees 2 marks for 3 rows; V2b ALSO fires, because Columbus then "
            "carries 4 data-component ids against G2's 5. Both are true consequences of dropping a row "
            "and both are declared. H6 by F5H0-3."),
    "W04": ("page", {"V2c", "H6"},
            "Columbus's excluded sibling is LEFT IN PLACE and only its data-excluded=\"1\" marking is "
            "removed. This is the case that delivers the ruling's 'V2's exclusion gate alone': V2b still "
            "sees 5 ids in waterfall order and PASSES, so the firing is scoped to the exclusion gate and "
            "V2c is proven connected independently of V2b. H6 by F5H0-3."),
    "W05": ("page", {"P6", "H6"},
            "the saved metro is moved to Chicago INSIDE the svg: Columbus's state group gains hidden, "
            "Chicago's loses it. The control fieldset is untouched, so the markup's saved state and the "
            "svg's visible state disagree — exactly the defect P6 exists to catch. P2 and P4 stay PASS; "
            "V2b/V2c ignore hidden and stay PASS. The ruling's 'P alone' is P6. H6 by F5H0-3."),
    "W06": ("page", {"V2c", "H6"},
            "the .era-excluded rule is DELETED from the page's own <style>; the markup is untouched — all "
            "three marks, all three data-excluded, all three data-muted, all three <rect class=era-excluded>, "
            "the waterfall order intact. Only the paint is gone. This is the positive for V2c's 5H-2 clauses "
            "(era_ph5_5h_results.md §10.3a): the 5H-1 form of V2c PASSES on this page and the 5H-2 form FAILS. "
            "The deleted rule carries no hex, no font-size, no family and no grid constant, so S1-S4 stay PASS. "
            "H6 by F5H0-3."),
    "W07": ("page", {"V4b", "H6"},
            "5H-3 positive for V4b's PROJECTION clause: Columbus's point cy is shifted +40 px. Plate-carree "
            "consistency breaks on every pair involving Columbus; the point count, the metro set and every "
            "ramp class are untouched, so the firing is scoped to the projection. The slope is estimated from "
            "the widest LATITUDE pair (Chicago/Austin), which Columbus is not in. H6 by F5H0-3."),
    "W08": ("page", {"V5b", "H6"},
            "5H-3 positive for V5b's SPAN clause: Dallas-Fort Worth's band rect width is halved, so its high "
            "edge no longer lands on its own cell and the one affine map breaks. DFW is chosen deliberately — "
            "B4 STAYS PASS, because the crossing geometry B4 gates is Columbus against Chicago, and DFW's low "
            "edge (the domain minimum, and the anchor of the widest pair) does not move. The interval SET is "
            "untouched. H6 by F5H0-3."),
    "W09": ("page", {"B4", "H6"},
            "5H-3 positive for B4, fired ALONE: the data-role=crossing annotation element is DELETED. The "
            "intervals, the central marks and the guide hairline are untouched, so V5a and V5b stay PASS; the "
            "annotation is credited NON-NUMERIC text, so T1 and T2 stay PASS. This is the case that puts B4 "
            "live — B4 was the last build-incomplete gate on the page. H6 by F5H0-3."),
    "W10": ("page", {"V6b", "H6"},
            "5H-3 positive for V6b's ORDER clause: two adjacent <tr> blocks are swapped WHOLE, cells and "
            "credits moving with their ids. Row order no longer equals sort_rank. Because each row still "
            "carries its own credits, clause (4) does NOT fire and T2 stays PASS — the firing is scoped to "
            "order. H6 by F5H0-3."),
    "W11": ("page", {"V6b", "H6"},
            "5H-3 positive for V6b's FERC-DOLLAR and OWN-ROW-CREDIT clauses: C-FERC-H13's empty $/yr cell is "
            "replaced by one showing 0.00 credited to C-F4B-3. The FERC floor now shows a dollar (clause 5) and "
            "a row borrows another row's credit (clause 4). T1 and T2 STAY PASS — the figure is credited and it "
            "does equal C-F4B-3's cell — which is the point: V6b's new clauses are live independently of group "
            "T. H6 by F5H0-3."),
    "W12": ("page", {"V6b", "T2", "H6"},
            "5H-3 positive for V6b's CLASS-ORDER clause: C-STATION-POINT's drawn category text is changed from "
            "limitation to unpriced with no row moved, putting an unpriced row at index 18 below limitation "
            "rows starting at index 8. T2 fires alongside and THAT IS A TRUE CONSEQUENCE, declared: the drawn "
            "text no longer equals the cell it cites. Declared as a two-gate firing rather than engineered into "
            "a one-gate firing — rewording the credit to make it fire alone is exactly what F5H2-5 forbids. "
            "The row was CORRECTED from C-CHI-5CP before the run (era_ph5_5h_results.md §13.4a): C-CHI-5CP is "
            "itself the first limitation row and re-marking it could not fire the clause. H6 by F5H0-3."),
    "W13": ("page", {"V4b", "H6"},
            "5H-3 positive for V4b's RAMP clause: Columbus's class is swapped era-ramp-1 -> era-ramp-6. It is "
            "still a token class, so S1 STAYS PASS, and no coordinate moves, so the projection clauses stay "
            "PASS. W07 and W13 fire V4b through two different clauses, which is how 'V4 has 8 points' stops "
            "being one assertion pretending to be five. H6 by F5H0-3."),
    # ---- Unit 5H-4: one positive for each clause this unit introduced.
    # Declared in era_ph5_5h_results.md section 15.4 BEFORE the suite ran,
    # each with the F5H3-2 question answered against the artefact: can the
    # mark I chose fire the clause it was written for, at all?
    "W14": ("page", {"V4b", "H6"},
            "5H-4 positive for V4b's NO-FRAME and LEAST-INK clauses: the four frame hairlines F5H3-9 "
            "removed are re-inserted at the head of the V4 svg. BOTH clauses fire and that is declared, "
            "not engineered around - the no-frame clause sees 4 <line> where it requires 0, and V4 goes "
            "from 24 marks to 28 against V5's 28, which is not strictly less. The lines carry a token "
            "class and no text, so S1 and T1 stay PASS. H6 by F5H0-3."),
    "W17": ("page", {"V5b", "H6"},
            "5H-4 positive for V5b's LABEL-ANCHOR clause: Dallas-Fort Worth's high value label is moved "
            "from x 510 to x 550. The rect does not move, so the affine SPAN clause stays PASS; the text "
            "does not change, so T2 stays PASS; the crossing is Columbus against Chicago, so B4 stays "
            "PASS. The clause wants rect_x + width + 8 = 288 + 214 + 8 = 510. H6 by F5H0-3."),
    "W18": ("page", {"V3b", "H6"},
            "5H-4 positive for V3b's SUB-GRID-UNIT clause: the fixed channel's credited label is moved "
            "from x 1074 back onto the zero rule at x 1086. W02 and W18 fire V3b through two different "
            "clauses. The fixed channel is the ONLY row under one grid unit (drawn extent 1 px), checked "
            "against the artefact before the run (F5H3-2) - a label moved on any other row would leave "
            "the clause silent. The text is unchanged, so T2 stays PASS. H6 by F5H0-3."),
    "W19": ("page", {"V2b", "H6"},
            "5H-4 positive for V2b's CONNECTOR clause: one data-role=connector hairline is deleted from "
            "Columbus's state group, which draws 3 for the 3 joined pairs G2 yields. The component rows, "
            "their ids and their order are untouched, so the order/count clause is silent and V2c stays "
            "PASS. H6 by F5H0-3."),
    "W20": ("page", {"T2", "H6"},
            "5H-4 positive for F5H1-3, AND THE ONE CASE IN THIS SUITE THAT CANNOT FIRE AGAINST THE GATE "
            "AS 5H-3 LEFT IT - which is the measurement. San Jose's V1 value label becomes -180.96 with "
            "U+2212, against a cell of 180.9616556284141. The OLD normaliser STRIPPED U+2212 and the "
            "shown value normalised to 180.96, equal to the cell to the precision shown: T2 passed on "
            "the negation of a positive cell. The hardened normaliser translates it and the comparison "
            "fails by 361.92. T1 stays PASS - NUMBER_RE already accepts U+2212 and the element still "
            "carries its data-src. H6 by F5H0-3."),
    "W21": ("page", {"V6c", "H6"},
            "5H-4 positive for V6c's COMPOSITION clause: the V1 and V3 <section> slots are swapped "
            "WHOLE, so document order becomes V3 V2 V1 V4 V5 V6 and V1 no longer leads. Every other "
            "gate finds its view by data-view and is order-blind. Not redundant with H6: H6 fires here "
            "because the PAGE moved, but the clause exists for a change to era_ph5_build_html.VIEWS, "
            "which H6 would rebuild and pass. H6 by F5H0-3."),
    "W15": ("grain", {"D2a", "D2b", "D2c", "D3a"},
            "THE TWELVE MONTHS ARE REVERSED within each (metro, stage) block. Every annual sum is "
            "unchanged (F5A-9). Same set as 5B; X13a's slot is now H13 in the page gate."),
    "W16": ("grain", {"D5a", "D6a"},
            "Chicago's monthly mitigated level scaled by 1 + 1e-6: level/delta identity and the tie to G1."),
    "W24": ("grain", {"D11a", "D11b", "D11c"},
            "Columbus usd_per_it_mwh + 200.0 (the 5B-x article): the three G1 ties, nothing else in D."),
    "W30": ("page", {"H13a", "H6"},
            "ruling (a): ONE EMBEDDED MD5 edited in the page copy (G1's last hex digit flipped). H13a sees "
            "embedded != disk manifest; H6 sees the page != its rebuild. H5, T1, S1 stay PASS."),
    "W31": ("input", {"H13b", "H13c", "D11a", "D11b", "D11c", "H6", "T2", "V4b", "V5b"},
            "ruling (b): ONE CSV CELL perturbed ON DISK after the build (Columbus usd_per_it_mwh + 200); "
            "page untouched. H13b md5, H13c rows, the three D11 ties, H6 rebuild-differs. H13a stays PASS. "
            "T2 was ADDED in 5H-1 (F5H1-2): V1 credits Columbus at 69.26 against this very cell, so a "
            "credited figure is a freshness assertion the moment a view exists — 5H-0's six-id set was "
            "measured on a page with no views on it. V4b AND V5b were ADDED in 5H-3 (F5H1-2 again): V4b "
            "re-derives every point's ramp step from this very cell and V5b re-derives the interval scale "
            "against Columbus's central mark, so a COLOUR and a POSITION are freshness assertions too. "
            "B4 stays PASS — its two cells did not move and the drawn crossing did not move."),
    "W32": ("page", {"T1", "H6"},
            "ruling (c): the literal 47.67 typed into the header caption. T1 counts one uncredited figure; "
            "H6 because the page moved. S1 stays PASS."),
    "W33": ("page", {"S1", "H6"},
            "ruling (d): style=\"color:#FF0000\" on the title element. S1 off-token; H6 because the page moved. "
            "T1 stays PASS."),
    "W34": ("build", set(),
            "ruling (e), first half: the page rebuilt TWICE in the temp copy from clean inputs; the harness "
            "compares the two builds (EQUAL) and the gate's H5/H6 PASS. Nothing fires."),
    "W35": ("build", {"S1"},
            "ruling (e), second half: the temp copy's token file has --era-accent-400 #4585C4 -> #4585C5; the "
            "page is rebuilt from it; the gate reads the ORIGINAL tokens via --style. S1 fires; H5 and H6 PASS "
            "(deterministic GIVEN its inputs)."),
    "N01": ("control", set(), "clean copy, nothing changed: nothing fires beyond the baseline."),
}
ORDER = ["W01"] + sorted(c for c in CASES if c.startswith("W") and c != "W01") + \
        sorted(c for c in CASES if c.startswith("N"))

FAIL_RE = re.compile(r"^FAIL\s+\[[\w]+\]\s+(\S+)", re.M)
PASS_RE = re.compile(r"^PASS\s+\[[\w]+\]\s+(\S+)", re.M)


def md5_of(path):
    with open(path, "rb") as fh:
        return hashlib.md5(fh.read()).hexdigest()


def build_copy(project, tmp):
    for f in GRAIN_FILES + SUPPORT:
        shutil.copy2(os.path.join(project, f), os.path.join(tmp, f))


def run_build(tmp, style=None, out=None):
    cmd = [sys.executable, os.path.join(HERE, "era_ph5_build_html.py"), "--project", tmp, "--quiet"]
    if style:
        cmd += ["--style", style]
    if out:
        cmd += ["--out", out]
    subprocess.run(cmd, check=True, capture_output=True)


def run_page_gate(tmp, style=None):
    cmd = [sys.executable, os.path.join(HERE, "era_ph5_page_gate.py"), "--project", tmp]
    if style:
        cmd += ["--style", style]
    r = subprocess.run(cmd, capture_output=True, text=True)
    return set(FAIL_RE.findall(r.stdout)), set(PASS_RE.findall(r.stdout)), r.stdout


def run_grain_gate(tmp):
    cmd = [sys.executable, os.path.join(HERE, "era_ph5_grain_gate.py"), "--project", tmp]
    r = subprocess.run(cmd, capture_output=True, text=True)
    return set(FAIL_RE.findall(r.stdout)), set(PASS_RE.findall(r.stdout)), r.stdout


def _rewrite_rows(p, hdr, rows):
    tp = p + ".tmp"
    with open(tp, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=hdr)
        w.writeheader()
        w.writerows(rows)
    os.replace(tp, p)


def _read_rows(p):
    with open(p, newline="", encoding="utf-8-sig") as fh:
        rd = csv.DictReader(fh)
        return rd.fieldnames, list(rd)


def mutate_csv(tmp, case):
    if case in ("W24", "W31"):
        p = os.path.join(tmp, "era_ph5_metro.csv")
        hdr, rows = _read_rows(p)
        for r in rows:
            if r["metro"] == "Columbus":
                r["usd_per_it_mwh"] = repr(float(r["usd_per_it_mwh"]) + 200.0)
        _rewrite_rows(p, hdr, rows)
        return
    p = os.path.join(tmp, "era_ph5_month.csv")
    hdr, rows = _read_rows(p)
    if case == "W15":
        keyed = {(r["metro"], r["stage"], int(r["month"])): r for r in rows}
        out = []
        for r in rows:
            src = dict(keyed[(r["metro"], r["stage"], 13 - int(r["month"]))])
            src["month"] = r["month"]
            src["month_name"] = r["month_name"]
            out.append(src)
        rows = out
    elif case == "W16":
        for r in rows:
            if r["metro"] == "Chicago" and r["stage"] == "mitigated":
                r["total_usd"] = "%.8f" % (float(r["total_usd"]) * 1.000001)
    _rewrite_rows(p, hdr, rows)


def mutate_page(tmp, case):
    p = os.path.join(tmp, PAGE)
    txt = open(p, encoding="utf-8").read()
    if case == "W30":
        man = json.load(open(os.path.join(tmp, "era_ph5_grains_manifest.json"), encoding="utf-8"))
        old = man["grains"]["era_ph5_metro.csv"]["md5"]
        new = old[:-1] + ("0" if old[-1] != "0" else "1")
        # the md5 string appears once inside the embedded manifest block; flip it there only
        i = txt.index('id="era-manifest"')
        j = txt.index("</script>", i)
        seg = txt[i:j]
        assert seg.count(old) == 1, "embedded md5 not unique in the manifest block"
        txt = txt[:i] + seg.replace(old, new) + txt[j:]
    elif case == "W32":
        needle = "Frozen contract."
        assert txt.count(needle) == 1
        txt = txt.replace(needle, "Frozen contract. DFW 47.67 per IT-MWh.")
    elif case == "W33":
        needle = '<h1 class="era-title">'
        assert txt.count(needle) == 1
        txt = txt.replace(needle, '<h1 class="era-title" style="color:#FF0000">')
    elif case == "W01":
        old = 'data-field="mitigated_usd_per_it_mwh"'
        assert txt.count(old) == 8, "expected 8 IT-state remainder bindings, got %d" % txt.count(old)
        txt = txt.replace(old, 'data-field="mitigated_annual_usd"')
    elif case == "W03":
        head = '<g data-component="M-COL-VOLT" data-excluded="1" data-muted="1">'
        assert txt.count(head) == 1, "Columbus excluded row not unique"
        i = txt.index(head)
        j = txt.index("</g>", i) + len("</g>")
        txt = txt[:i] + txt[j:]
    elif case == "W04":
        head = '<g data-component="M-COL-VOLT" data-excluded="1" data-muted="1">'
        assert txt.count(head) == 1
        txt = txt.replace(head, '<g data-component="M-COL-VOLT" data-muted="1">')
    elif case == "W05":
        a = '<g data-state-metro="Columbus">'
        b = '<g data-state-metro="Chicago" hidden="hidden">'
        assert txt.count(a) == 1 and txt.count(b) == 1
        txt = txt.replace(a, '<g data-state-metro="Columbus" hidden="hidden">')
        txt = txt.replace(b, '<g data-state-metro="Chicago">')
    elif case == "W06":
        rule = ".era-excluded { fill: var(--era-muted); stroke: var(--era-rule); stroke-width: 1; }"
        assert txt.count(rule) == 1, "the .era-excluded rule is not unique in the page"
        txt = txt.replace(rule, "")
    elif case == "W07":
        head = '<circle class="era-ramp-1" data-role="point" data-metro="Columbus"'
        assert txt.count(head) == 1, "Columbus point not unique"
        i = txt.index(head)
        j = txt.index(">", i)
        seg = txt[i:j]
        m = re.search(r'cy="(\d+)"', seg)
        assert m, "Columbus point has no cy"
        txt = txt[:i] + seg.replace(m.group(0), 'cy="%d"' % (int(m.group(1)) + 40)) + txt[j:]
    elif case == "W13":
        head = '<circle class="era-ramp-1" data-role="point" data-metro="Columbus"'
        assert txt.count(head) == 1
        txt = txt.replace(head, '<circle class="era-ramp-6" data-role="point" data-metro="Columbus"')
    elif case == "W08":
        head = '<g data-role="interval" data-metro="Dallas-Fort Worth" data-kind="band"'
        assert txt.count(head) == 1, "DFW band group not unique"
        i = txt.index(head)
        j = txt.index("</g>", i)
        seg = txt[i:j]
        m = re.search(r'(<rect class="era-band" data-edge="span" x="\d+" y="\d+" width=")(\d+)(")', seg)
        assert m, "DFW spanning rect not found"
        txt = txt[:i] + seg.replace(m.group(0), m.group(1) + str(max(int(m.group(2)) // 2, 1)) + m.group(3)) + txt[j:]
    elif case == "W09":
        m = re.search(r'<text class="era-note" data-role="crossing"[^>]*>[^<]*</text>\n?', txt)
        assert m, "the crossing annotation is not on the page"
        assert len(re.findall(r'data-role="crossing"', txt)) == 1
        txt = txt[:m.start()] + txt[m.end():]
    elif case == "W10":
        rows = re.findall(r'<tr data-caveat="[^"]+">.*?</tr>', txt, re.S)
        assert len(rows) == 21, "expected 21 V6 rows, got %d" % len(rows)
        a, b = rows[5], rows[6]
        assert txt.count(a) == 1 and txt.count(b) == 1
        txt = txt.replace(a, "\x00A\x00").replace(b, a).replace("\x00A\x00", b)
    elif case == "W11":
        old = '<td class="era-num" data-src="era_ph5_caveat:C-FERC-H13:usd_per_year"></td>'
        assert txt.count(old) == 1, "the FERC empty $/yr cell is not unique"
        txt = txt.replace(old, '<td class="era-num" data-src="era_ph5_caveat:C-F4B-3:usd_per_year">0.00</td>')
    elif case == "W12":
        old = '<td data-src="era_ph5_caveat:C-STATION-POINT:category">limitation</td>'
        assert txt.count(old) == 1, "the C-STATION-POINT category cell is not unique"
        txt = txt.replace(old, '<td data-src="era_ph5_caveat:C-STATION-POINT:category">unpriced</td>')
    elif case == "W14":
        head = '<svg data-view="V4"'
        assert txt.count(head) == 1, "V4 svg not unique"
        i = txt.index(head)
        j = txt.index(">", i) + 1
        frame = "".join('<line class="era-axis" x1="%d" y1="%d" x2="%d" y2="%d"/>' % q
                        for q in ((48, 48, 1136, 48), (1136, 48, 1136, 384),
                                  (1136, 384, 48, 384), (48, 384, 48, 48)))
        txt = txt[:j] + frame + txt[j:]
    elif case == "W17":
        # x RE-DECLARED AT UNIT 6E-2: the label's x is DERIVED from the value it draws, and the
        # two-segment publication moved DFW's band_high_usd_per_it_mwh, so 510 -> 513.  The case
        # is unchanged - it still nudges this exact element by +40 px and must still fire the
        # same set.  A tamper anchor that encodes a published value is re-declared with the
        # refresh, never loosened (F5H1-2: a declared tamper set is never inherited).
        head = ('<text class="era-value" x="513" y="56" text-anchor="start" data-role="label-high" '
                'data-src="era_ph5_metro:Dallas-Fort Worth:band_high_usd_per_it_mwh">')
        assert txt.count(head) == 1, "the DFW high label is not where the declaration says (%d)" % txt.count(head)
        txt = txt.replace(head, head.replace('x="513"', 'x="553"'))
    elif case == "W18":
        head = ('<text class="era-value" x="1074" y="216" text-anchor="end" '
                'data-src="era_ph5_metro:Austin:mitigation_fixed_usd">')
        assert txt.count(head) == 1, "the fixed-channel label is not where the declaration says (%d)" % txt.count(head)
        txt = txt.replace(head, head.replace('x="1074"', 'x="1086"').replace('"end"', '"middle"'))
    elif case == "W19":
        head = '<g data-state-metro="Columbus">'
        assert txt.count(head) == 1
        i = txt.index(head)
        j = txt.index('<g data-state-metro="Dallas-Fort Worth"', i)
        seg = txt[i:j]
        m = re.search(r'<line class="era-wf-connector" data-role="connector"[^>]*/>\n?', seg)
        assert m, "Columbus draws no connector"
        assert len(re.findall(r'data-role="connector"', seg)) == 3, "Columbus should draw 3 connectors"
        txt = txt[:i] + seg[:m.start()] + seg[m.end():] + txt[j:]
    elif case == "W20":
        head = '<text class="era-value" x="1072" y="389" data-src="era_ph5_metro:San Jose / Bay Area:usd_per_it_mwh">180.96</text>'
        assert txt.count(head) == 1, "San Jose's V1 value label is not where the declaration says (%d)" % txt.count(head)
        txt = txt.replace(head, head.replace(">180.96<", ">\u2212180.96<"))
    elif case == "W21":
        a = re.search(r'<section class="era-view" id="V1" data-view="V1">.*?</section>', txt, re.S)
        b = re.search(r'<section class="era-view" id="V3" data-view="V3">.*?</section>', txt, re.S)
        assert a and b, "V1 or V3 slot not found"
        sa, sb = a.group(0), b.group(0)
        assert txt.count(sa) == 1 and txt.count(sb) == 1
        txt = txt.replace(sa, "\x00A\x00").replace(sb, sa).replace("\x00A\x00", sb)
    elif case == "W02":
        a = 'data-channel="mitigation_rider_usd"'
        b = 'data-channel="mitigation_energy_channel_usd"'
        assert txt.count(a) == 1 and txt.count(b) == 1
        txt = txt.replace(a, "\x00SWAP\x00").replace(b, a).replace("\x00SWAP\x00", b)
    tp = p + ".tmp"
    with open(tp, "w", encoding="utf-8", newline="") as fh:
        fh.write(txt)
    os.replace(tp, p)


def v1_built(project):
    p = os.path.join(project, PAGE)
    if not os.path.isfile(p):
        return False
    txt = open(p, encoding="utf-8").read()
    return 'data-view="V1"' in txt and 'data-view="V1" data-status="build-incomplete"' not in txt


def emit(log, txt):
    print(txt)
    if log:
        with open(log, "a", encoding="utf-8") as fh:
            fh.write(txt + "\n\n")


def run_case(project, case, log, baseline):
    kind, declared, why = CASES[case]
    if case == "W01" and not v1_built(project):
        emit(log, "\n".join([
            "CASE W01  NOT RUNNABLE  (V1 is build-incomplete on the page in %s; declared, not run, not a miss)" % project,
            "  declared: %s" % sorted(declared),
            "  why     : %s" % why]))
        return True
    tmp = tempfile.mkdtemp(prefix="ph5h_%s_" % case)
    extra_lines = []
    try:
        build_copy(project, tmp)
        if kind == "grain":
            mutate_csv(tmp, case)
            fails, passes, _ = run_grain_gate(tmp)
            fired = fails
        elif kind == "control":
            run_build(tmp)
            fails, passes, _ = run_page_gate(tmp)
            fired = fails - baseline
        elif kind == "page":
            run_build(tmp)
            mutate_page(tmp, case)
            fails, passes, _ = run_page_gate(tmp)
            fired = fails - baseline
        elif kind == "input":
            run_build(tmp)
            mutate_csv(tmp, case)
            fails, passes, _ = run_page_gate(tmp)
            fired = fails - baseline
        elif kind == "build":
            if case == "W34":
                a = os.path.join(tmp, "build_a.html")
                b = os.path.join(tmp, "build_b.html")
                run_build(tmp, out=a)
                run_build(tmp, out=b)
                same = open(a, "rb").read() == open(b, "rb").read()
                extra_lines.append("  two builds: %s (md5 %s / %s)" % ("EQUAL" if same else "DIFFER", md5_of(a), md5_of(b)))
                shutil.copy2(a, os.path.join(tmp, PAGE))
                fails, passes, _ = run_page_gate(tmp)
                fired = fails - baseline
                if not same:
                    fired = fired | {"HARNESS:two-builds-differ"}
            else:   # W35
                sp = os.path.join(tmp, STYLE_MD)
                st = open(sp, encoding="utf-8").read()
                assert st.count("#4585C4") == 1
                open(sp, "w", encoding="utf-8").write(st.replace("#4585C4", "#4585C5"))
                run_build(tmp)          # built from the ALTERED tokens in tmp
                fails, passes, _ = run_page_gate(tmp, style=os.path.join(project, STYLE_MD))
                fired = fails - baseline
                extra_lines.append("  gate read tokens from %s; build read %s" % (os.path.join(project, STYLE_MD), sp))
        else:
            raise RuntimeError(kind)
        # explicit PASS assertions the declaration names
        must_pass = {"W01": {"V1a", "V1b", "T1", "T2", "S1"}, "W02": {"V3a", "T1", "T2", "S1"},
                     "W03": {"V2a", "P6", "T1", "T2", "S1"},
                     "W04": {"V2a", "V2b", "P6", "T1", "T2", "S1"},
                     "W05": {"V2a", "V2b", "V2c", "P2", "P4", "T1", "T2", "S1"},
                     "W06": {"V2a", "V2b", "P6", "T1", "T2", "S1", "S2", "S3", "S4"},
                     # 5H-3: each new positive also asserts that the OTHER five views'
                     # gates stay PASS, which is what makes "fired alone" mean anything
                     # on a page where six views now share one gate run.
                     "W07": {"V4a", "V5a", "V5b", "V6a", "V6b", "B4", "T1", "T2", "S1"},
                     "W13": {"V4a", "V5a", "V5b", "V6a", "V6b", "B4", "T1", "T2", "S1", "S2"},
                     "W08": {"V5a", "V4a", "V4b", "V6a", "V6b", "B4", "T1", "T2", "S1"},
                     "W09": {"V5a", "V5b", "V4a", "V4b", "V6a", "V6b", "T1", "T2", "S1"},
                     "W10": {"V6a", "V4a", "V4b", "V5a", "V5b", "B4", "T1", "T2", "S1"},
                     "W11": {"V6a", "V4a", "V4b", "V5a", "V5b", "B4", "T1", "T2", "S1"},
                     "W12": {"V6a", "V4a", "V4b", "V5a", "V5b", "B4", "T1", "S1"},
                     # 5H-4's six, each asserting the views it must NOT disturb
                     "W14": {"V4a", "V1a", "V2a", "V3a", "V5a", "V5b", "V6a", "V6b", "V6c", "B4",
                             "T1", "T2", "S1", "S2", "S5"},
                     "W17": {"V5a", "V4a", "V4b", "V1a", "V2a", "V3a", "V3b", "V6a", "V6b", "B4",
                             "T1", "T2", "S1"},
                     "W18": {"V3a", "V1a", "V2a", "V2b", "V4a", "V4b", "V5a", "V5b", "V6a", "V6b",
                             "B4", "T1", "T2", "S1"},
                     "W19": {"V2a", "V2c", "P6", "V1a", "V3a", "V3b", "V4a", "V4b", "V5a", "V5b",
                             "V6a", "V6b", "B4", "T1", "T2", "S1"},
                     "W20": {"T1", "V1a", "V1b", "V1c", "V2a", "V2b", "V3a", "V3b", "V4a", "V4b",
                             "V5a", "V5b", "V6a", "V6b", "B4", "S1"},
                     "W21": {"V1a", "V1b", "V1c", "V3a", "V3b", "V2a", "V2b", "V4a", "V4b", "V5a",
                             "V5b", "V6a", "V6b", "B1", "B2", "B3", "B4", "P6", "P7", "T1", "T2", "S1"},
                     "W30": {"H5", "T1", "S1"}, "W31": {"H13a", "B4", "V6b"}, "W32": {"S1"}, "W33": {"T1"},
                     "W34": {"H5", "H6"}, "W35": {"H5", "H6", "S0a"}}.get(case, set())
        missing_pass = must_pass - passes
        if missing_pass:
            extra_lines.append("  ALSO-ASSERTED PASS NOT SEEN: %s" % sorted(missing_pass))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    ok = fired == declared and not any("NOT SEEN" in l for l in extra_lines)
    lines = ["CASE %s  %s  (%s)" % (case, "AS DECLARED" if ok else "MISS", kind),
             "  declared: %s" % (sorted(declared) or "(nothing fires)"),
             "  actual  : %s" % (sorted(fired) or "(nothing fired)")] + extra_lines + \
            ["  why     : %s" % why]
    if not ok:
        extra = sorted(fired - declared)
        short = sorted(declared - fired)
        if extra:
            lines.append("  UNDECLARED FIRINGS: %s" % extra)
        if short:
            lines.append("  DECLARED BUT SILENT: %s" % short)
    emit(log, "\n".join(lines))
    return ok


def summarize(log):
    if not os.path.isfile(log):
        print("no log at %s" % log)
        return 1
    txt = open(log, encoding="utf-8").read()
    ok = len(re.findall(r"^CASE \S+  AS DECLARED", txt, re.M))
    miss = len(re.findall(r"^CASE \S+  MISS", txt, re.M))
    nr = len(re.findall(r"^CASE \S+  NOT RUNNABLE", txt, re.M))
    print("SUMMARY %s: %d AS DECLARED, %d MISS, %d NOT RUNNABLE" % (log, ok, miss, nr))
    for m in re.finditer(r"^CASE (\S+)  MISS.*$", txt, re.M):
        print("  " + m.group(0))
    return 0 if miss == 0 else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", default=".")
    ap.add_argument("--cases", default=None)
    ap.add_argument("--log", default=None)
    ap.add_argument("--summary", action="store_true")
    a = ap.parse_args()
    if a.summary:
        return summarize(a.log or "era_ph5_5h_tamper_run.log")
    cases = a.cases.split(",") if a.cases else ORDER
    unknown = [c for c in cases if c not in CASES]
    if unknown:
        print("unknown case(s): %s" % unknown)
        return 2
    if cases[0].startswith("N"):
        print("REFUSED: a control (%s) may not run first. Run W01 first (F5B-3)." % cases[0])
        return 2
    if cases[0] != "W01":
        print("REFUSED: W01 must lead every run (F5B-3); got %s. Run W01 first." % cases[0])
        return 2

    project = os.path.abspath(a.project)
    emit(a.log, "era_ph5_page_tamper.py  Unit 5H-4  project=%s  python=%s" % (project, sys.version.split()[0]))

    # baseline: clean copy, built, gated — must equal the declared v0 build-incomplete set
    tmp = tempfile.mkdtemp(prefix="ph5h_base_")
    try:
        build_copy(project, tmp)
        run_build(tmp)
        base_fails, base_passes, _ = run_page_gate(tmp)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    if base_fails != BASELINE:
        emit(a.log, "\n".join([
            "BASELINE MISMATCH — NOT CONNECTED. The clean page's FAIL set is not the declared set (5H-3 declares EMPTY).",
            "  declared: %s" % sorted(BASELINE),
            "  actual  : %s" % sorted(base_fails)]))
        return 3
    emit(a.log, "BASELINE  clean page FAIL set is EMPTY as declared (%d ids); the page is ACCEPTED and every firing set below is ABSOLUTE"
         % len(BASELINE))

    results = [run_case(project, c, a.log, base_fails) for c in cases]
    n_ok = sum(1 for r in results if r)
    emit(a.log, "RESULT %d of %d AS DECLARED (W01 %s)" % (n_ok, len(cases),
         "NOT RUNNABLE — V1 not built" if not v1_built(project) else "ran first, V1 built"))
    return 0 if all(results) else 1


if __name__ == "__main__":
    sys.exit(main())
