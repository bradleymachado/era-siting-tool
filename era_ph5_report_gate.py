#!/usr/bin/env python3
"""era_ph5_report_gate.py — Unit 5H-5 of direction_ph5_html_v1.0.md

This section is intended to be THE ACCEPTANCE for era_ph5_report_v1.0.md: it
re-derives every figure the report shows from the four grains and asserts the
report agrees, group by group. It reads the ARTEFACT — the markdown file on
disk — and the DATA, and it shares no constant with the prose it is checking.

Two duties, taken from the page gate's group T because the failure mode is the
same one (F5H3-1):

  * every figure the report shows is CREDITED to something re-derivable, and
    the count of UNCREDITED figures is ZERO (T1's duty);
  * every credited figure EQUALS what it cites, to the precision shown
    (T2's duty, with T2's hardened normaliser: U+2212 is TRANSLATED, never
    stripped — F5H1-3).

Credit kinds, the markdown analogue of the page's data-src, written as HTML
comments so they are invisible when the file renders:

  G   <!--G:G1:Chicago:usd_per_it_mwh-->    a grain cell, by ROW_KEYS and column
  D   <!--D:portfolio_baseline_usd-->       a named derivation over the grains
  F   <!--F:era_ph5_dashboard.html:md5-->   a fact about a file on disk

A credit comment must IMMEDIATELY follow the token it credits, with nothing
between, so "which comment credits which figure" is never a judgement call.

Blocks carry the tables. A region delimited by

  <!--ERA-BLOCK:name-->  ...  <!--/ERA-BLOCK:name-->

is REGENERATED here from the grains and must equal the file's content byte for
byte. A block is stronger than a credit, so every table in the report is a
block and blocks are not scanned for credits.

Groups
------
  D    the four grains, 29 gates, via era_ph5_grain_gate.group_d (unchanged)
  A    assembly: the required sections, the block delimiters, ASCII minus only
  R    one gate per block: the block equals its regeneration from the grains
  C    credits: uncredited count ZERO; every G/D/F credit resolves and equals
  Q    the Phase 6 queue: ruled order, pinned to the direction files by md5
  X    the prohibitions, each naming the exact string it forbids

Usage
-----
  python era_ph5_report_gate.py --project .
  python era_ph5_report_gate.py --project . --log era_ph5_5h_report_gate_run.log
  python era_ph5_report_gate.py --project . --report other.md
  python era_ph5_report_gate.py --project . --emit ranking      # block content
  python era_ph5_report_gate.py --project . --emit ALL

Exit code 0 only when every gate PASSES and none is SKIP-BLIND.
"""

import argparse
import hashlib
import os
import platform
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import era_ph5_grain_gate as GG          # noqa: E402  (group D, unchanged)
import era_ph5_build_html as BUILD       # noqa: E402  (ROW_KEYS — one definition)

REPORT_NAME = "era_ph5_report_v1.0.md"
PAGE_NAME = "era_ph5_dashboard.html"
MANIFEST_NAME = "era_ph5_grains_manifest.json"

STEMS = {"G1": "era_ph5_metro", "G2": "era_ph5_stack",
         "G3": "era_ph5_month", "G4": "era_ph5_caveat"}

# ---- the ruled Phase 6 pre-flight queue -----------------------------------
# RULING CONSTANT, not a measurement constant: it cites the two direction files
# it is derived from and Q2 pins both by md5, so this gate fails the moment a
# ruling text moves under it (session-tiers, "the measurement constant and the
# ruling constant are different things"). Order is
# direction_ph5_tableau_v1.0.md Unit 5E's list, AS AMENDED by
# direction_ph5_html_v1.0.md Ruling H-4: licensing review FIRST, subdomain
# deployment of era_ph5_dashboard.html SECOND, X13c STRUCK (H13 made it
# unconditional).
QUEUE_SOURCES = {
    "direction_ph5_tableau_v1.0.md": "43b3cfe7b975acd03ec212082f140bd0",
    "direction_ph5_html_v1.0.md": "d9f17e127fa8ad7ace74d9c15630da4a",
    "direction_ph4_close_v1.0.md": "bdf5250d97263d86c1d5494bb380b3ed",
}
QUEUE = [
    ("Q6-01", "Licensing review before any visibility change",
     "P5-5 / H-4", "-"),
    ("Q6-02", "Subdomain deployment of era_ph5_dashboard.html on bradmachado.com",
     "H-4", "-"),
    ("Q6-03", "Chicago's 5CP derivation, then rule the bracket",
     "Ruling 17", "F4C-7"),
    ("Q6-04", "Northern Virginia's third ratchet construction, priced then ruled",
     "Ruling 16", "F4B-2"),
    ("Q6-05", "The two-segment PUE form; it moves all eight metros",
     "Ruling 14", "-"),
    ("Q6-06", "Schema v1.5 whole: node_class plus billing_determinant",
     "Ruling 11", "F4M-14"),
    ("Q6-07", "Docket R",
     "Ruling 11", "-"),
    ("Q6-08", "The two false lines in era_tariff_read_log_v1.3.md, with Unit 4E's declared set",
     "Ruling 18", "-"),
    ("Q6-09", "The Atlanta and Phoenix library gap",
     "Ruling 19", "F4D-8"),
    ("Q6-10", "PG&E Peak Day Pricing, the one elective that is a risk trade",
     "Ruling 11", "F4M-13"),
    ("Q6-11", "F4M-12's latent seasonal flat-demand defect",
     "Ruling 11", "F4M-12"),
    ("Q6-12", "Atlanta's missing voltage_level",
     "-", "-"),
]
STRUCK = ["X13c"]

# ---- the prohibitions, each naming the exact string it forbids -------------
FORBIDDEN_CHAIN = "reproduces the committed page to the byte"
BANNED_METERED = ["0.9742"]          # F5A-4; "0.97" alone is too short to forbid
RENDER_DIR = "renders"

REQUIRED_SECTIONS = [
    "1 — What the page is",
    "2 — What the page shows",
    "3 — What the page deliberately does not show",
    "4 — The four grains and their bases",
    "5 — Gate coverage",
    "6 — The chain, as measured",
    "7 — Why the renderer is ours: the Tableau record",
    "8 — Phase 5's own findings",
    "9 — The Phase 6 pre-flight queue",
    "10 — Open ruling questions carried out of Phase 5",
]

BLOCKS = ["ranking", "channels", "stack", "bands", "excluded", "caveats",
          "grains", "monthly", "gatecoverage", "tampercoverage"]
BLOCK_GATE = {name: "R%d" % (i + 1) for i, name in enumerate(BLOCKS)}

BLOCK_OPEN = "<!--ERA-BLOCK:%s-->"
BLOCK_CLOSE = "<!--/ERA-BLOCK:%s-->"
BLOCK_RE = re.compile(r"<!--ERA-BLOCK:([a-z]+)-->\n(.*?)\n<!--/ERA-BLOCK:\1-->", re.S)

CREDIT_RE = re.compile(r"<!--(G|D|F):([^>]+?)-->")
# A value token: a hex digest fragment (tried first, and it must carry at least
# one digit so an English word of hex letters is not a figure), or a
# money/percent/decimal/integer run that STANDS ALONE — the lookarounds are what
# stop the "5" inside era_ph5_metro.csv or the "1" inside v1.0 from being read
# as a figure, without any of those needing an exclusion pattern.
VALUE_RE = re.compile(
    r"\b(?=[0-9a-f]*\d)[0-9a-f]{8,32}\b"
    r"|(?<![\w.])\$?-?\d[\d,]*(?:\.\d+)?%?(?!\w)")
CODE_SPAN_RE = re.compile(r"`[^`]*`")
BARE_NUMBER_RE = re.compile(r"^[\d,.$%+-]+$")

# WHOLE-TOKEN identifier patterns. Masked out before the value scan. None of
# them matches a bare decimal: every one carries a letter, a symbol or a fixed
# prefix, which is what stops a wrong figure from hiding inside an exclusion.
IDENT_PATTERNS = [
    r"F\d[A-Za-z0-9]*-\d+",                   # F4C-7, F5H4-1, F2Fb-4, F5Bx-8, F5H5-1
    r"C-[A-Z0-9]+(?:-[A-Z0-9]+)*",            # C-BAND-25, C-FERC-H13
    r"M-[A-Z0-9]+(?:-[A-Z0-9]+)*",            # M-COL-VOLT
    r"Q6-\d\d",                               # this file's queue ids
    r"[WXN]\d\d",                             # tamper case ids
    r"5H-\d", r"5B-[xy]", r"P5-\d[a-z]?", r"H-\d", r"E-\d(?:\.\d)?",
    r"Ruling \d+", r"Rulings \d+[^ ]*", r"Phase \d", r"Unit \d[A-Za-z]?-?\d?",
    r"Section \d+",
    r"[Vv]\d+\.\d+",                          # v1.0, V1.2
    r"\d{4}-\d{2}-\d{2}",                     # dates
    r"§\d+(?:\.\d+)*[a-z]?",                  # section refs
    r"D\d+[a-z]?", r"V\d[a-z]?", r"H13[a-z]?", r"[PSTBRACQ]\d+[a-z]?",
    r"X13[a-c]?", r"X\d+",
    r"ORC 5727\.81\(?[A-Z]?\)?",
    r"Attachment H-13",
    r"DCT-T", r"B-20-T", r"B-20", r"GS-4", r"E-35", r"PLL-18", r"BESH-HV",
    r"BESH", r"BES", r"B100-4H", r"COMM-PRI-20MW", r"TRANS-SVC", r"WIN53",
    r"PRI-GT10KW-SUB", r"[45]CP", r"lf090",
    r"schema v\d\.\d",
    r"Python 3\.\d+(?:\.\d+)?",
    r"UTF-8", r"U\+2212", r"OATT",
    r"25-0677", r"25-0679",                   # the two ComEd docket numbers
    r"[A-Za-z_][A-Za-z0-9_]*\.(?:md|py|csv|json|html|log|png|twb|db|sql)",
    r"ph\d-[a-z]+",                           # ph5-closed, ph4-closed
]
IDENT_RE = re.compile("|".join("(?:%s)" % p for p in IDENT_PATTERNS))
HEADING_NUM_RE = re.compile(r"^(#{1,6} )(\d{1,2} — )")


# --------------------------------------------------------------------------
def md5_of(path):
    with open(path, "rb") as fh:
        return hashlib.md5(fh.read()).hexdigest()


def num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def f2(v):
    return "{:,.2f}".format(v)


def f6(v):
    return "{:,.6f}".format(v)


def load_grains(project):
    out = {}
    for g, stem in STEMS.items():
        _, rows = GG.load_csv(os.path.join(project, stem + ".csv"))
        out[g] = rows
    return out


def row_key(stem, r):
    return "|".join(r[k] for k in BUILD.ROW_KEYS[stem])


# ---- derivations over the four grains -------------------------------------
def derivations(project, data):
    G1, G2, G3, G4 = data["G1"], data["G2"], data["G3"], data["G4"]
    base = sum(num(r["annual_usd"]) for r in G1)
    mit = sum(num(r["mitigated_annual_usd"]) for r in G1)
    excl = sum(num(r["usd_per_year"]) for r in G2
               if r["included_in_mitigated_total"] == "0")
    it = [num(r["usd_per_it_mwh"]) for r in G1]
    gaps = [num(r["gap_to_next_usd_per_it_mwh"]) for r in G1
            if r["gap_to_next_usd_per_it_mwh"].strip()]
    colu = [r for r in G1 if r["metro"] == "Columbus"][0]
    chi = [r for r in G1 if r["metro"] == "Chicago"][0]
    d = {
        "portfolio_baseline_usd": base,
        "portfolio_baseline_usd_b": base / 1e9,
        "portfolio_mitigated_usd": mit,
        "portfolio_mitigated_usd_b": mit / 1e9,
        "portfolio_mitigation_usd": mit - base,
        "portfolio_mitigation_pct": 100.0 * (base - mit) / base,
        "portfolio_it_mwh": sum(num(r["it_annual_mwh"]) for r in G1),
        "spread_ratio_it": max(it) / min(it),
        "spread_low_it": min(it),
        "spread_high_it": max(it),
        "excluded_total_usd": excl,
        "excluded_over_mitigation": abs(excl) / abs(mit - base),
        "tightest_gap_it": min(gaps),
        "channel_rider_usd": sum(num(r["mitigation_rider_usd"]) for r in G1),
        "channel_energy_usd": sum(num(r["mitigation_energy_channel_usd"]) for r in G1),
        "channel_demand_usd": sum(num(r["mitigation_demand_channel_usd"]) for r in G1),
        "channel_fixed_usd": sum(num(r["mitigation_fixed_usd"]) for r in G1),
        "channel_statutory_usd": sum(num(r["mitigation_statutory_usd"]) for r in G1),
        "band_crossing_facility": (num(colu["band_high_usd_per_mwh"])
                                   - num(chi["usd_per_mwh"])),
        "band_crossing_it": (num(colu["band_high_usd_per_it_mwh"])
                             - num(chi["usd_per_it_mwh"])),
        "nova_ratchet_months": float(sum(
            1 for r in G3 if r["metro"] == "Northern Virginia"
            and r["stage"] == "baseline" and r["ratchet_binding"] == "1")),
        "metro_count": float(len(G1)),
        "market_priced_count": float(sum(1 for r in G1 if r["is_market_priced"] == "1")),
        "bracket_count": float(sum(1 for r in G1 if r["has_bracket"] == "1")),
        "excluded_count": float(sum(1 for r in G2
                                    if r["included_in_mitigated_total"] == "0")),
        "caveat_count": float(len(G4)),
        "caveat_unpriced_count": float(sum(1 for r in G4 if r["category"] == "unpriced")),
        "caveat_limitation_count": float(sum(1 for r in G4 if r["category"] == "limitation")),
        "measures_total_usd": sum(num(r["measures_annual_usd"]) for r in G1),
        "storage_total_usd": sum(num(r["storage_annual_usd"]) for r in G1),
        "measure_row_count": float(sum(1 for r in G2 if r["kind"] == "measure")),
        "queue_length": float(len(QUEUE)),
    }
    cov = page_gate_coverage(project)
    d["page_gate_total"] = float(sum(cov.values()))
    d["tamper_case_count"] = float(len(tamper_cases()))
    return d


# ---- file facts -----------------------------------------------------------
def file_fact(project, fname, fact):
    path = os.path.join(project, fname)
    if not os.path.isfile(path):
        return None, "no file %r" % fname
    if fact == "md5":
        return md5_of(path), None
    if fact == "md5_8":
        return md5_of(path)[:8], None
    if fact == "bytes":
        return str(os.path.getsize(path)), None
    if fact == "lines":
        with open(path, "rb") as fh:
            return str(fh.read().count(b"\n")), None
    if fact == "rows":
        _, rows = GG.load_csv(path)
        return str(len(rows)), None
    return None, "unknown fact %r" % fact


# ---- the live page gate and the tamper module -----------------------------
_COV = {}


def page_gate_coverage(project):
    """Run the page gate IN PROCESS and count its gates by group. The report's
    coverage table is therefore re-derived from the gate that actually runs,
    not from a number typed into this file."""
    if _COV:
        return _COV
    import era_ph5_page_gate as PG
    g = PG.run(project, os.path.join(project, PAGE_NAME),
               set("D,H,H13,P,V,B,S,T".split(",")),
               os.path.join(project, PG.STYLE_MD))
    for gid, grp, status, msg in g.rows:
        _COV[grp] = _COV.get(grp, 0) + 1
    return _COV


def tamper_cases():
    import era_ph5_page_tamper as TP
    return [(cid, TP.CASES[cid][0], sorted(TP.CASES[cid][1])) for cid in TP.ORDER]


# ---- block generators -----------------------------------------------------
def blk_ranking(project, data, d):
    rows = sorted(data["G1"], key=lambda r: int(r["rank"]))
    out = ["| # | metro | utility | schedule | baseline $/yr | baseline $/IT-MWh "
           "| mitigated $/yr | mitigated $/IT-MWh | mitigated % |",
           "| --: | --- | --- | --- | --: | --: | --: | --: | --: |"]
    for r in rows:
        out.append("| %s | %s | %s | %s | %s | %s | %s | %s | %s |" % (
            r["rank"], r["metro"], r["utility"], r["schedule_code"],
            f2(num(r["annual_usd"])), f2(num(r["usd_per_it_mwh"])),
            f2(num(r["mitigated_annual_usd"])), f2(num(r["mitigated_usd_per_it_mwh"])),
            f2(num(r["mitigation_pct_of_baseline"]))))
    out.append("| | **portfolio** | | | **%s** | | **%s** | | **%s** |" % (
        f2(d["portfolio_baseline_usd"]), f2(d["portfolio_mitigated_usd"]),
        f2(d["portfolio_mitigation_pct"])))
    return "\n".join(out)


def blk_channels(project, data, d):
    rows = sorted(data["G1"], key=lambda r: int(r["rank"]))
    cols = [("mitigation_rider_usd", "rider"),
            ("mitigation_energy_channel_usd", "energy"),
            ("mitigation_demand_channel_usd", "demand"),
            ("mitigation_fixed_usd", "fixed"),
            ("mitigation_statutory_usd", "statutory")]
    out = ["| metro | " + " | ".join("%s $/yr" % lbl for _, lbl in cols) + " |",
           "| --- | " + " | ".join("--:" for _ in cols) + " |"]
    for r in rows:
        out.append("| %s | %s |" % (
            r["metro"], " | ".join(f2(num(r[c])) for c, _ in cols)))
    out.append("| **portfolio** | %s |" % " | ".join(
        "**%s**" % f2(d["channel_%s_usd" % lbl]) for _, lbl in cols))
    return "\n".join(out)


def blk_stack(project, data, d):
    order = {r["metro"]: int(r["rank"]) for r in data["G1"]}
    rows = [r for r in data["G2"] if r["included_in_mitigated_total"] == "1"]
    rows.sort(key=lambda r: (order[r["metro"]], int(r["waterfall_order"])))
    out = ["| metro | step | kind | component | $/yr | $/IT-MWh |",
           "| --- | --: | --- | --- | --: | --: |"]
    for r in rows:
        out.append("| %s | %s | %s | %s | %s | %s |" % (
            r["metro"], r["waterfall_order"], r["kind"], r["component_name"],
            f2(num(r["usd_per_year"])), f2(num(r["usd_per_it_mwh"]))))
    return "\n".join(out)


def blk_bands(project, data, d):
    rows = sorted(data["G1"], key=lambda r: int(r["rank"]))
    out = ["| metro | kind | low $/IT-MWh | central $/IT-MWh | high $/IT-MWh | what the interval is |",
           "| --- | --- | --: | --: | --: | --- |"]
    for r in rows:
        if r["is_market_priced"] == "1":
            out.append("| %s | band | %s | %s | %s | +/-25 %% of the market component |" % (
                r["metro"], f2(num(r["band_low_usd_per_it_mwh"])),
                f2(num(r["usd_per_it_mwh"])), f2(num(r["band_high_usd_per_it_mwh"]))))
    for r in rows:
        if r["has_bracket"] == "1":
            lo = min(num(r["mitigated_usd_per_it_mwh"]), num(r["mitigated_alt_usd_per_it_mwh"]))
            hi = max(num(r["mitigated_usd_per_it_mwh"]), num(r["mitigated_alt_usd_per_it_mwh"]))
            out.append("| %s | published pair | %s | | %s | %s, unruled (%s) |" % (
                r["metro"], f2(lo), f2(hi), r["bracket_reading"], r["open_ruling_ids"]))
    return "\n".join(out)


def blk_excluded(project, data, d):
    order = {r["metro"]: int(r["rank"]) for r in data["G1"]}
    rows = [r for r in data["G2"] if r["included_in_mitigated_total"] == "0"]
    rows.sort(key=lambda r: order[r["metro"]])
    out = ["| metro | component | $/yr | $/IT-MWh |",
           "| --- | --- | --: | --: |"]
    for r in rows:
        out.append("| %s | %s | %s | %s |" % (
            r["metro"], r["component_name"],
            f2(num(r["usd_per_year"])), f2(num(r["usd_per_it_mwh"]))))
    out.append("| **total** | **excluded from every mitigated figure** | **%s** | |"
               % f2(d["excluded_total_usd"]))
    return "\n".join(out)


def blk_caveats(project, data, d):
    rows = sorted(data["G4"], key=lambda r: int(r["sort_rank"]))
    out = ["| # | id | category | scope | priced | $/yr | $/IT-MWh | ruling |",
           "| --: | --- | --- | --- | --: | --: | --: | --- |"]
    for r in rows:
        uy = f2(num(r["usd_per_year"])) if r["usd_per_year"].strip() else ""
        ui = f6(num(r["usd_per_it_mwh"])) if r["usd_per_it_mwh"].strip() else ""
        out.append("| %s | %s | %s | %s | %s | %s | %s | %s |" % (
            r["sort_rank"], r["caveat_id"], r["category"], r["metro_scope"],
            r["priced"], uy, ui, r["ruling_ref"]))
    return "\n".join(out)


def blk_grains(project, data, d):
    out = ["| grain | file | rows | columns | md5 | what it is |",
           "| --- | --- | --: | --: | --- | --- |"]
    what = {
        "G1": "one row per metro: the ranking, the bases, the bands, the brackets",
        "G2": "the mitigation walk, one row per component, excluded siblings included",
        "G3": "twelve months x four stages per metro, levels and deltas",
        "G4": "the honesty layer: every caveat, priced or not",
    }
    for g in ("G1", "G2", "G3", "G4"):
        stem = STEMS[g]
        rows = data[g]
        out.append("| %s | %s.csv | %d | %d | %s | %s |" % (
            g, stem, len(rows), len(rows[0]),
            md5_of(os.path.join(project, stem + ".csv")), what[g]))
    out.append("| | `%s` | | | %s | the pins every row above is read against |" % (
        MANIFEST_NAME, md5_of(os.path.join(project, MANIFEST_NAME))))
    return "\n".join(out)


def blk_monthly(project, data, d):
    G3 = data["G3"]
    order = {r["metro"]: int(r["rank"]) for r in data["G1"]}
    out = ["| metro | peak kWh month | peak baseline $ month | peak billed kW month | ratchet months |",
           "| --- | --: | --: | --: | --: |"]
    for metro in sorted(order, key=lambda m: order[m]):
        base = [r for r in G3 if r["metro"] == metro and r["stage"] == "baseline"]
        pk = max(base, key=lambda r: num(r["kwh"]))["month"]
        pu = max(base, key=lambda r: num(r["total_usd"]))["month"]
        pd = max(base, key=lambda r: num(r["billed_kw_15min"]))["month"]
        rt = sum(1 for r in base if r["ratchet_binding"] == "1")
        out.append("| %s | %s | %s | %s | %d |" % (metro, pk, pu, pd, rt))
    return "\n".join(out)


def blk_gatecoverage(project, data, d):
    cov = page_gate_coverage(project)
    duty = {
        "D": "the four grains, imported unchanged by this gate too",
        "H": "page hygiene, determinism, and the scratch-rebuild reproduction",
        "H13": "freshness by construction: embedded manifest == disk == the CSVs",
        "P": "the two controls, read from the markup with script disabled",
        "V": "the six views, asserted against the DRAWING",
        "B": "basis: the siting metric, the metered swap, the band crossing",
        "S": "the thirteen tokens, five sizes, one family, the 8 px grid",
        "T": "typed figures: uncredited count zero, credited equal their cells",
    }
    out = ["| group | gates | duty |", "| --- | --: | --- |"]
    for grp in ("D", "H", "H13", "P", "V", "B", "S", "T"):
        out.append("| %s | %d | %s |" % (grp, cov.get(grp, 0), duty[grp]))
    out.append("| **total** | **%d** | **all PASS, empty FAIL set, exit 0** |"
               % sum(cov.values()))
    return "\n".join(out)


def blk_tampercoverage(project, data, d):
    cases = tamper_cases()
    out = ["| case | kind | gates it must fire |", "| --- | --- | --- |"]
    for cid, kind, fires in cases:
        out.append("| %s | %s | %s |" % (
            cid, kind, ", ".join(fires) if fires else "(nothing fires)"))
    out.append("| **%d cases** | | **all AS DECLARED, %s first, %s last** |" % (
        len(cases), cases[0][0], cases[-1][0]))
    return "\n".join(out)


GENERATORS = {
    "ranking": blk_ranking, "channels": blk_channels, "stack": blk_stack,
    "bands": blk_bands, "excluded": blk_excluded, "caveats": blk_caveats,
    "grains": blk_grains, "monthly": blk_monthly,
    "gatecoverage": blk_gatecoverage, "tampercoverage": blk_tampercoverage,
}


# ---- credit resolution ----------------------------------------------------
def resolve_credit(kind, ref, project, data, derivs):
    if kind == "G":
        try:
            g, key, col = ref.split(":", 2)
        except ValueError:
            return None, "malformed G credit %r" % ref
        if g not in STEMS:
            return None, "unknown grain %r" % g
        stem = STEMS[g]
        for r in data[g]:
            if row_key(stem, r) == key:
                if col not in r:
                    return None, "no column %r in %s" % (col, g)
                return r[col], None
        return None, "no row %r in %s" % (key, g)
    if kind == "D":
        if ref not in derivs:
            return None, "unknown derivation %r" % ref
        return derivs[ref], None
    if kind == "F":
        try:
            fname, fact = ref.rsplit(":", 1)
        except ValueError:
            return None, "malformed F credit %r" % ref
        return file_fact(project, fname, fact)
    return None, "unknown credit kind %r" % kind


def equal_to_precision(shown, cell):
    """T2's rule, unchanged: TRANSLATE U+2212, strip separators, compare to the
    precision the report actually shows (F5H1-3)."""
    s = re.sub(r"[,$%\s]", "", str(shown).replace("−", "-"))
    try:
        sv = float(s)
        cv = float(cell)
    except (TypeError, ValueError):
        return str(shown).strip() == str(cell).strip()
    dec = len(s.split(".")[1]) if "." in s else 0
    return abs(sv - cv) <= 0.5 * 10 ** (-dec) + 1e-9


# ---- prose scanning -------------------------------------------------------
def prose_lines(text):
    """Every line of the report that is not inside a block and not a fenced
    code line. Returns (lineno, line)."""
    spans = [(m.start(), m.end()) for m in BLOCK_RE.finditer(text)]
    out = []
    pos = 0
    fenced = False
    for i, line in enumerate(text.split("\n"), 1):
        start = pos
        pos += len(line) + 1
        if line.startswith("```"):
            fenced = not fenced
            continue
        if fenced:
            continue
        if any(a <= start < b for a, b in spans):
            continue
        out.append((i, line))
    return out


def scan_line(line):
    """Mask identifiers and code spans, then return (tokens, credits, spans).
    A token is (text, end_index); a credit is (kind, ref, start_index)."""
    code = [m.group(0) for m in CODE_SPAN_RE.finditer(line)]
    masked = CODE_SPAN_RE.sub(lambda m: " " * len(m.group(0)), line)
    masked = HEADING_NUM_RE.sub(lambda m: m.group(1) + " " * len(m.group(2)), masked)
    credits = [(m.group(1), m.group(2), m.start(), m.end())
               for m in CREDIT_RE.finditer(masked)]
    masked = CREDIT_RE.sub(lambda m: " " * len(m.group(0)), masked)
    idents = []
    def _mask_ident(m):
        idents.append(m.group(0))
        return " " * len(m.group(0))
    masked = IDENT_RE.sub(_mask_ident, masked)
    tokens = [(m.group(0), m.start(), m.end()) for m in VALUE_RE.finditer(masked)]
    return tokens, credits, idents, code


# --------------------------------------------------------------------------
def group_a(g, text, path):
    missing = [s for s in REQUIRED_SECTIONS if ("## " + s) not in text]
    g.check("A1", "A", not missing,
            "all %d required sections present, in the ruled order" % len(REQUIRED_SECTIONS)
            if not missing else "MISSING SECTIONS: %s" % missing)
    order = [text.find("## " + s) for s in REQUIRED_SECTIONS if ("## " + s) in text]
    g.check("A2", "A", order == sorted(order) and len(order) == len(REQUIRED_SECTIONS),
            "the sections appear in the declared order (%d found)" % len(order))
    found = [m.group(1) for m in BLOCK_RE.finditer(text)]
    dup = [b for b in set(found) if found.count(b) > 1]
    g.check("A3", "A", sorted(found) == sorted(BLOCKS) and not dup,
            "exactly the %d declared blocks, each opened and closed once: %s"
            % (len(BLOCKS), found)
            if sorted(found) == sorted(BLOCKS) and not dup else
            "block set is %s against declared %s (duplicates %s)" % (found, BLOCKS, dup))
    stray = re.findall(r"<!--/?ERA-BLOCK:([a-z]+)-->", text)
    balanced = len(stray) == 2 * len(BLOCKS)
    g.check("A4", "A", balanced,
            "%d block delimiters for %d blocks — every open has its close"
            % (len(stray), len(BLOCKS)))
    minus = text.count("−")
    g.check("A5", "A", minus == 0,
            "zero U+2212 in the report; every figure prints the ASCII hyphen-minus (F5H1-3)"
            if minus == 0 else "%d U+2212 characters in the report" % minus)


def group_r(g, text, project, data, derivs):
    present = {m.group(1): m.group(2) for m in BLOCK_RE.finditer(text)}
    for name in BLOCKS:
        gid = BLOCK_GATE[name]
        if name not in present:
            g.check(gid, "R", False, "block %r absent from the report" % name)
            continue
        want = GENERATORS[name](project, data, derivs)
        got = present[name]
        if want == got:
            g.check(gid, "R", True,
                    "block %r equals its regeneration from the grains (%d lines, %d chars)"
                    % (name, want.count("\n") + 1, len(want)))
        else:
            wl, gl = want.split("\n"), got.split("\n")
            diff = [i + 1 for i in range(max(len(wl), len(gl)))
                    if (wl[i] if i < len(wl) else None) != (gl[i] if i < len(gl) else None)]
            first = diff[0] if diff else 0
            g.check(gid, "R", False,
                    "block %r DIFFERS from its regeneration on %d line(s); first is line %d: "
                    "report %r vs grains %r" % (
                        name, len(diff), first,
                        (gl[first - 1][:90] if first - 1 < len(gl) else "<absent>"),
                        (wl[first - 1][:90] if first - 1 < len(wl) else "<absent>")))


def group_c(g, text, project, data, derivs):
    lines = prose_lines(text)
    scanned = 0
    tokens_all = []
    uncredited = []
    credited = []
    idents_all = []
    bare_code = []
    orphans = []
    for lineno, line in lines:
        if not line.strip():
            continue
        scanned += 1
        tokens, credits, idents, code = scan_line(line)
        idents_all += idents
        for c in code:
            inner = c.strip("`")
            if BARE_NUMBER_RE.match(inner) and inner.strip("$%,.+-"):
                bare_code.append((lineno, c))
        cstart = {c[2]: c for c in credits}
        ends = set()
        for tok, s, e in tokens:
            tokens_all.append(tok)
            ends.add(e)
            if e in cstart:
                credited.append((lineno, tok, cstart[e]))
            else:
                uncredited.append((lineno, tok))
        # SCOPE clause added in this unit before the run, recorded in
        # era_ph5_5h_results.md section 17.5a: a credit comment that follows no
        # figure credits NOTHING, and it is silently ignored by the two
        # comparison gates, so a spelled-out number wearing a credit would read
        # as gated and be gated by nothing. It is the orphan half of C1's own
        # duty and it moves no threshold.
        for kind, ref, cs, ce in credits:
            if cs not in ends:
                orphans.append((lineno, kind, ref))
    g.check("C1", "C",
            scanned >= 1 and not uncredited and not bare_code and not orphans,
            "uncredited figure count = %d and orphan-credit count = %d (%d figures in %d prose "
            "lines scanned; %d identifier tokens masked, %d distinct forms; %d bare-number code spans)"
            % (len(uncredited), len(orphans), len(tokens_all), scanned, len(idents_all),
               len(set(idents_all)), len(bare_code))
            + ("" if not uncredited else "; UNCREDITED: %s" % uncredited[:6])
            + ("" if not orphans else "; ORPHAN CREDITS: %s" % orphans[:6])
            + ("" if not bare_code else "; BARE IN BACKTICKS: %s" % bare_code[:4])
            + ("" if scanned else "; VACUOUS — nothing scanned"))

    bad_g, bad_d, bad_f = [], [], []
    used = set()
    n = {"G": 0, "D": 0, "F": 0}
    for lineno, tok, cr in credited:
        kind, ref = cr[0], cr[1]
        n[kind] += 1
        used.add((kind, ref))
        cell, err = resolve_credit(kind, ref, project, data, derivs)
        bucket = {"G": bad_g, "D": bad_d, "F": bad_f}[kind]
        if err:
            bucket.append("line %d: %s" % (lineno, err))
        elif not equal_to_precision(tok, cell):
            bucket.append("line %d: %s shows %s, %s is %s"
                          % (lineno, ref, tok, kind, cell))
    g.check("C2", "C", not bad_g and n["G"] >= 1,
            "%d G credits resolve to a grain cell and equal it to the precision shown" % n["G"]
            + ("" if n["G"] else "; VACUOUS — no G credit in the report")
            + ("" if not bad_g else "; " + "; ".join(bad_g[:5])))
    g.check("C3", "C", not bad_d and n["D"] >= 1,
            "%d D credits equal their derivation over the grains, to the precision shown" % n["D"]
            + ("" if n["D"] else "; VACUOUS — no D credit in the report")
            + ("" if not bad_d else "; " + "; ".join(bad_d[:5])))
    g.check("C4", "C", not bad_f and n["F"] >= 1,
            "%d F credits equal the file fact they name, on disk, now" % n["F"]
            + ("" if n["F"] else "; VACUOUS — no F credit in the report")
            + ("" if not bad_f else "; " + "; ".join(bad_f[:5])))
    dead = sorted(k for k in derivs if ("D", k) not in used
                  and k not in ("portfolio_baseline_usd_b", "portfolio_mitigated_usd_b"))
    used_in_blocks = {"portfolio_baseline_usd", "portfolio_mitigated_usd",
                      "portfolio_mitigation_pct", "excluded_total_usd",
                      "channel_rider_usd", "channel_energy_usd", "channel_demand_usd",
                      "channel_fixed_usd", "channel_statutory_usd", "page_gate_total",
                      "tamper_case_count"}
    dead = [k for k in dead if k not in used_in_blocks]
    g.check("C5", "C", not dead,
            "every derivation in the table is cited by the report or drawn in a block "
            "(%d derivations, %d cited by a D credit)" % (len(derivs), n["D"])
            if not dead else "DEAD DERIVATIONS, defined but never cited: %s" % dead)


def group_q(g, text, project):
    bad_pin = []
    for fname, want in QUEUE_SOURCES.items():
        path = os.path.join(project, fname)
        if not os.path.isfile(path):
            bad_pin.append("%s absent" % fname)
        else:
            got = md5_of(path)
            if got != want:
                bad_pin.append("%s is %s, the queue constant was derived from %s"
                               % (fname, got, want))
    g.check("Q2", "Q", not bad_pin,
            "the queue constant is pinned to the two direction files it cites: %s"
            % ", ".join("%s %s" % (f, m[:8]) for f, m in sorted(QUEUE_SOURCES.items()))
            if not bad_pin else "; ".join(bad_pin))

    found = re.findall(r"\|\s*(Q6-\d\d)\s*\|\s*([^|]+?)\s*\|", text)
    ids = [f[0] for f in found]
    want_ids = [q[0] for q in QUEUE]
    g.check("Q1", "Q", ids == want_ids,
            "the report's queue is the ruled queue, in order: %d items, %s first, %s last"
            % (len(ids), ids[0] if ids else "-", ids[-1] if ids else "-")
            if ids == want_ids else "report queue %s against ruled %s" % (ids, want_ids))
    titles_ok = all(q[1] in text for q in QUEUE)
    first_two = (ids[:2] == ["Q6-01", "Q6-02"]
                 and QUEUE[0][1] in text and QUEUE[1][1] in text)
    g.check("Q5", "Q", titles_ok and first_two,
            "every queue item's title appears verbatim; the licensing review is first and the "
            "subdomain deployment second, per H-4"
            if titles_ok and first_two else
            "titles_ok=%s first_two=%s" % (titles_ok, first_two))
    # Line-anchored on purpose: a character class excluding "|" still spans
    # newlines, so an unanchored search found X13c in the PROSE that explains
    # why it was struck by reaching back to a pipe in a table above it. The
    # gate asks whether a struck item is a QUEUE ROW, which is a line that
    # begins with a pipe.
    struck = [s for s in STRUCK
              if any(ln.lstrip().startswith("|") and s in ln
                     for ln in text.split("\n"))]
    g.check("Q4", "Q", not struck,
            "X13c is struck: it appears in no queue row (H13 made it unconditional)"
            if not struck else "STRUCK ITEM STILL IN THE QUEUE: %s" % struck)


def group_q_open(g, text, data):
    ids = set()
    for r in data["G1"]:
        for x in r["open_ruling_ids"].split(";"):
            if x.strip():
                ids.add(x.strip())
    missing = sorted(i for i in ids if i not in text)
    g.check("Q3", "Q", ids and not missing,
            "every open_ruling_id carried in G1 (%s) is named in the report's queue"
            % ", ".join(sorted(ids))
            if ids and not missing else
            "G1 carries %s; the report does not name %s" % (sorted(ids), missing))


def group_x(g, text, project):
    hit = FORBIDDEN_CHAIN in text
    g.check("X1", "X", not hit,
            "H-3's unmeetable sentence is absent: the report never says %r "
            "(F5H4-1 is unruled; the report states what section 16.3 measured)" % FORBIDDEN_CHAIN
            if not hit else "THE FORBIDDEN CHAIN CLAIM IS IN THE REPORT: %r" % FORBIDDEN_CHAIN)
    banned = [b for b in BANNED_METERED if b in text]
    g.check("X2", "X", not banned,
            "the metered band-crossing literal %s never appears; the report quotes the FACILITY "
            "figure (F5A-4)" % BANNED_METERED
            if not banned else "BANNED METERED LITERAL PRESENT: %s" % banned)
    rd = os.path.join(project, RENDER_DIR)
    md5s = []
    if os.path.isdir(rd):
        md5s = [md5_of(os.path.join(rd, f)) for f in sorted(os.listdir(rd))
                if f.endswith(".png")]
    present = [m for m in md5s if m in text or m[:8] in text]
    g.check("X3", "X", not present,
            "no render md5 appears in the report: the renders are PIXEL-stable and BYTE-unstable "
            "across a device commit, so md5 is not a claim to make about them (F5H4-8); %d render(s) checked"
            % len(md5s)
            if not present else "RENDER MD5 IN THE REPORT: %s" % present)
    urls = re.findall(r"https?://[^\s)\]]+", text)
    g.check("X4", "X", not urls,
            "the report contains no http URL: the public link 5E asked for does not exist yet — "
            "the subdomain deployment is the second Phase 6 item, and a stated absence is the "
            "honest discharge of that clause"
            if not urls else "URL(S) IN THE REPORT: %s" % urls[:4])


# --------------------------------------------------------------------------
def run(project, report_path):
    g = GG.Gate()
    GG.group_d(g, project)
    text = open(report_path, encoding="utf-8").read()
    data = load_grains(project)
    derivs = derivations(project, data)
    group_a(g, text, report_path)
    group_r(g, text, project, data, derivs)
    group_c(g, text, project, data, derivs)
    group_q(g, text, project)
    group_q_open(g, text, data)
    group_x(g, text, project)
    return g


ORDER = {"D": 0, "A": 1, "R": 2, "C": 3, "Q": 4, "X": 5}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", default=".")
    ap.add_argument("--report", default=None)
    ap.add_argument("--log", default=None)
    ap.add_argument("--quiet", action="store_true")
    ap.add_argument("--emit", default=None,
                    help="print one block's regenerated content (or ALL) and exit")
    a = ap.parse_args()

    if a.emit:
        data = load_grains(a.project)
        derivs = derivations(a.project, data)
        names = BLOCKS if a.emit == "ALL" else [a.emit]
        for nm in names:
            print(BLOCK_OPEN % nm)
            print(GENERATORS[nm](a.project, data, derivs))
            print(BLOCK_CLOSE % nm)
            print()
        return 0

    report_path = a.report or os.path.join(a.project, REPORT_NAME)
    if not os.path.isabs(report_path) and os.path.dirname(report_path) == "":
        report_path = os.path.join(a.project, report_path)

    out = ["era_ph5_report_gate.py  Unit 5H-5  project=%s  report=%s  python=%s  platform=%s"
           % (os.path.abspath(a.project), os.path.basename(report_path),
              sys.version.split()[0], platform.platform()),
           "DECLARED (era_ph5_5h_results.md section 17.5): 58 PASS; 0 FAIL; 0 SKIP-OK; 0 SKIP-BLIND.",
           "  D 29 (era_ph5_grain_gate.group_d, unchanged) + A 5 + R 10 + C 5 + Q 5 + X 4.",
           "  R regenerates every table from the four grains and compares byte for byte; C is the page",
           "  gate's group T applied to markdown: uncredited figures ZERO, credited equal their cells.",
           ""]
    if os.path.isfile(report_path):
        out[0] += "  report_md5=%s" % md5_of(report_path)
    g = run(a.project, report_path)
    g.rows.sort(key=lambda r: (ORDER.get(r[1], 9), ))
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
