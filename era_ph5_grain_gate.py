#!/usr/bin/env python3
"""era_ph5_grain_gate.py — Unit 5H-0 of direction_ph5_html_v1.0.md (Ruling H-2)

This section is intended to GATE THE FOUR PHASE 5 GRAINS on their own, with no
page and no workbook present: the 29 data preconditions of group D (D0a-D11c),
including the F5A-9 monthly-shape gate and 5B-x's D11 ties on usd_per_it_mwh.

Group D was MOVED HERE VERBATIM from the retired era_ph5_workbook_gate.py
(md5 689b1354db45c5d88be3b3494dd71170). The blocks marked MOVED below are character-for-character copies
of that file's lines; the retired file is never edited again (H-5). Both
era_ph5_page_gate.py and era_ph5_page_tamper.py import this module.

Usage
-----
  python era_ph5_grain_gate.py --project .
  python era_ph5_grain_gate.py --project . --log era_ph5_5h_grain_run.log

Exit code 0 only when all 29 gates PASS.
"""

import argparse
import csv
import os
import platform
import sys
from collections import defaultdict

SOURCE_FILE = "era_ph5_workbook_gate.py"
SOURCE_MD5 = "689b1354db45c5d88be3b3494dd71170"

# --- MOVED VERBATIM from era_ph5_workbook_gate.py (md5 689b1354db45c5d88be3b3494dd71170) lines 111-116: GRAINS ---
GRAINS = {
    "era_ph5_metro": "era_ph5_metro.csv",
    "era_ph5_stack": "era_ph5_stack.csv",
    "era_ph5_month": "era_ph5_month.csv",
    "era_ph5_caveat": "era_ph5_caveat.csv",
}
# --- end MOVED GRAINS ---
# --- MOVED VERBATIM from era_ph5_workbook_gate.py (md5 689b1354db45c5d88be3b3494dd71170) lines 152-184: D constants ---
METROS = ["Atlanta", "Austin", "Chicago", "Columbus", "Dallas-Fort Worth",
          "Northern Virginia", "Phoenix", "San Jose / Bay Area"]

# --- F5A-9: the monthly shape. These are the facts a reversal destroys. ----
# argmax month of baseline metered kWh, every metro
D_ARGMAX_KWH = {m: 7 for m in METROS}
# argmax month of baseline total_usd
D_ARGMAX_TOTAL = {"Atlanta": 7, "Austin": 7, "Chicago": 5, "Columbus": 7,
                  "Dallas-Fort Worth": 7, "Northern Virginia": 7,
                  "Phoenix": 7, "San Jose / Bay Area": 7}
# argmax month of billed_kw_15min
# REFRESHED AT UNIT 6E-2 on the two_segment_ph6 published basis (P6-R18).  Austin 6 -> 7 and
# Northern Virginia 8 -> 7: F6E-11 measured the FORM moving the billed peak INTERVAL in three of
# eight metros, and in two of them it crosses a month boundary.  The map still takes three
# distinct values, so D2c is still not satisfiable by any constant assignment.
D_ARGMAX_KW = {"Atlanta": 7, "Austin": 7, "Chicago": 8, "Columbus": 8,
               "Dallas-Fort Worth": 6, "Northern Virginia": 7,
               "Phoenix": 8, "San Jose / Bay Area": 6}
# F5A-5: a ratchet is a season, not a boolean
D_RATCHET_MONTHS = {"Northern Virginia": [1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 12]}

# F5A-3 / F4E-3 / the excluded band
# REFRESHED AT UNIT 6E-2 on the two_segment_ph6 published basis (P6-R18).  The pre-6E-2 values,
# on the linear_4a basis, were 6694135866.22 and rider -167099502.51 / energy -87551080.84 /
# demand -37732405.75 / statutory 17239632.05.  mitigation_fixed_usd does not move.
D_PORTFOLIO_BASELINE_USD = 6690861877.21
D_EXCLUDED_BAND_USD = -741104525.28
D_CHANNELS = {
    "mitigation_rider_usd": -166248514.22,
    "mitigation_energy_channel_usd": -87127512.95,
    "mitigation_demand_channel_usd": -36302455.20,
    "mitigation_fixed_usd": 226130.88,
    "mitigation_statutory_usd": 17239583.05,
}
# V3's declared row order: most negative first. This IS F4E-3.
V3_ORDER = ["mitigation_rider_usd", "mitigation_energy_channel_usd",
            "mitigation_demand_channel_usd", "mitigation_fixed_usd",
            "mitigation_statutory_usd"]

CENT = 0.01
# --- end MOVED D constants ---

# --- MOVED VERBATIM from era_ph5_workbook_gate.py (md5 689b1354db45c5d88be3b3494dd71170) lines 227-257: Gate / num / load_csv ---
class Gate:
    def __init__(self):
        self.rows = []

    def check(self, gid, group, ok, msg):
        self.rows.append((gid, group, "PASS" if ok else "FAIL", msg))
        return ok

    def skip(self, gid, group, msg, blind=True):
        self.rows.append((gid, group, "SKIP-BLIND" if blind else "SKIP-OK", msg))

    def note(self, gid, group, msg):
        self.rows.append((gid, group, "NOTE", msg))

    def retired(self, gid, group, msg):
        """A gate that asserted a superseded ruling. Printed, never run, never
        counted as PASS or FAIL; its record lives in git (P5-2b)."""
        self.rows.append((gid, group, "RETIRED", msg))


def num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def load_csv(path):
    with open(path, newline="", encoding="utf-8-sig") as fh:
        rd = csv.DictReader(fh)
        return rd.fieldnames, list(rd)
# --- end MOVED Gate / num / load_csv ---

# --- MOVED VERBATIM from era_ph5_workbook_gate.py (md5 689b1354db45c5d88be3b3494dd71170) lines 263-483: group_d ---
def group_d(g, project):
    paths = {k: os.path.join(project, v) for k, v in GRAINS.items()}
    missing = [v for v in paths.values() if not os.path.isfile(v)]
    if not g.check("D0a", "D", not missing,
                   "all four grains present" if not missing else
                   "MISSING: %s" % missing):
        return None

    hdr, G1 = load_csv(paths["era_ph5_metro"])
    hdr2, G2 = load_csv(paths["era_ph5_stack"])
    hdr3, G3 = load_csv(paths["era_ph5_month"])
    hdr4, G4 = load_csv(paths["era_ph5_caveat"])
    headers = {"era_ph5_metro": hdr, "era_ph5_stack": hdr2,
               "era_ph5_month": hdr3, "era_ph5_caveat": hdr4}

    g.check("D0b", "D", len(G1) == 8 and len(hdr) == 73,
            "G1 is %d x %d (declared 8 x 73)" % (len(G1), len(hdr)))
    g.check("D0c", "D", len(G2) == 33 and len(hdr2) == 16,
            "G2 is %d x %d (declared 33 x 16)" % (len(G2), len(hdr2)))
    g.check("D0d", "D", len(G3) == 384 and len(hdr3) == 24,
            "G3 is %d x %d (declared 384 x 24)" % (len(G3), len(hdr3)))
    g.check("D0e", "D", len(G4) == 21 and len(hdr4) == 12,
            "G4 is %d x %d (declared 21 x 12)" % (len(G4), len(hdr4)))
    g.check("D0f", "D", sorted(set(r["metro"] for r in G1)) == sorted(METROS),
            "G1 metro set matches the declared eight")

    # --- monthly index -----------------------------------------------------
    idx = defaultdict(dict)
    for r in G3:
        idx[(r["metro"], r["stage"])][int(r["month"])] = r

    # D1 file order: months ascend 1..12 within each (metro, stage) block
    seq = defaultdict(list)
    for r in G3:
        seq[(r["metro"], r["stage"])].append(int(r["month"]))
    bad = [k for k, v in seq.items() if v != list(range(1, 13))]
    g.check("D1a", "D", not bad,
            "every (metro, stage) block runs month 1..12 in file order"
            + ("" if not bad else "; violations: %s" % bad[:4]))

    # D2 argmax of metered kWh — F5A-9. A reversed year moves July to June.
    got = {}
    for m in METROS:
        b = idx[(m, "baseline")]
        got[m] = max(b, key=lambda k: num(b[k]["kwh"]))
    g.check("D2a", "D", got == D_ARGMAX_KWH,
            "argmax month of baseline kWh is 7 in all eight metros"
            + ("" if got == D_ARGMAX_KWH else "; got %s" % got))

    got = {}
    for m in METROS:
        b = idx[(m, "baseline")]
        got[m] = max(b, key=lambda k: num(b[k]["total_usd"]))
    g.check("D2b", "D", got == D_ARGMAX_TOTAL,
            "argmax month of baseline total_usd matches the declared map "
            "(Chicago is May, the other seven July)"
            + ("" if got == D_ARGMAX_TOTAL else "; got %s" % got))

    got = {}
    for m in METROS:
        b = idx[(m, "baseline")]
        got[m] = max(b, key=lambda k: num(b[k]["billed_kw_15min"]))
    g.check("D2c", "D", got == D_ARGMAX_KW,
            "argmax month of billed_kw_15min matches the declared map "
            "(6, 7 and 8 all occur, so the map is not a constant)"
            + ("" if got == D_ARGMAX_KW else "; got %s" % got))
    g.check("D2d", "D", len(set(D_ARGMAX_KW.values())) >= 3,
            "the declared demand-peak map takes at least three distinct months, "
            "so D2c is not satisfiable by any constant assignment")

    # D3 F5A-5: a ratchet is a season, not a boolean
    ok = True
    detail = []
    for m in METROS:
        b = idx[(m, "baseline")]
        binding = [k for k in sorted(b) if b[k]["ratchet_binding"] == "1"]
        want = D_RATCHET_MONTHS.get(m, [])
        if binding != want:
            ok = False
            detail.append("%s %s != %s" % (m, binding, want))
    g.check("D3a", "D", ok,
            "Northern Virginia binds its ratchet in exactly 11 months, August "
            "excepted; no other metro binds in any month (F5A-5)"
            + ("" if ok else "; " + "; ".join(detail)))

    # D4 vacuity guards: no monthly series is a flat twelfth
    flat = []
    for m in METROS:
        b = idx[(m, "baseline")]
        vals = [round(num(b[k]["total_usd"]), 2) for k in sorted(b)]
        if len(set(vals)) < 2:
            flat.append(m)
    g.check("D4a", "D", not flat,
            "no metro's baseline monthly total is a flat twelfth"
            + ("" if not flat else "; flat: %s" % flat))
    const = []
    for m in METROS:
        s = idx[(m, "storage")]
        vals = [round(num(s[k]["total_usd"]), 2) for k in sorted(s)]
        if len(set(vals)) < 2:
            const.append(m)
    g.check("D4b", "D", not const,
            "no metro's monthly storage saving is constant across the year "
            "(a pro-rata allocation would satisfy every annual tie and say "
            "nothing)" + ("" if not const else "; constant: %s" % const))

    # D5 level/delta identity, per metro per month, to the cent
    worst = 0.0
    for m in METROS:
        for mo in range(1, 13):
            v = (num(idx[(m, "baseline")][mo]["total_usd"])
                 + num(idx[(m, "measures")][mo]["total_usd"])
                 + num(idx[(m, "storage")][mo]["total_usd"])
                 - num(idx[(m, "mitigated")][mo]["total_usd"]))
            worst = max(worst, abs(v))
    g.check("D5a", "D", worst < CENT,
            "mitigated = baseline + measures + storage in every metro-month; "
            "worst residual $%.9f" % worst)

    vt = {(r["stage"], r["value_type"]) for r in G3}
    g.check("D5b", "D", vt == {("baseline", "level"), ("mitigated", "level"),
                               ("measures", "delta"), ("storage", "delta")},
            "value_type declares baseline and mitigated LEVELS, measures and "
            "storage DELTAS; got %s" % sorted(vt))

    # D6 cross-grain ties to G1, to the cent
    ann = defaultdict(float)
    for r in G3:
        ann[(r["metro"], r["stage"])] += num(r["total_usd"])
    worst_b = worst_m = 0.0
    for r in G1:
        worst_b = max(worst_b, abs(ann[(r["metro"], "baseline")] - num(r["annual_usd"])))
        worst_m = max(worst_m, abs(ann[(r["metro"], "mitigated")]
                                   - num(r["mitigated_annual_usd"])))
    g.check("D6a", "D", worst_b < CENT and worst_m < CENT,
            "G3 sums to G1 per metro on both level stages; worst baseline "
            "$%.9f, worst mitigated $%.9f" % (worst_b, worst_m))

    tot = sum(num(r["annual_usd"]) for r in G1)
    g.check("D6b", "D", abs(tot - D_PORTFOLIO_BASELINE_USD) < CENT,
            "portfolio baseline sums to the declared $%.2f (F5A-3); got $%.2f"
            % (D_PORTFOLIO_BASELINE_USD, tot))

    # D7 G2's excluded band, and its exclusion flag
    ex = [r for r in G2 if r["kind"] == "excluded"]
    exsum = sum(num(r["usd_per_year"]) for r in ex)
    g.check("D7a", "D", len(ex) == 3 and abs(exsum - D_EXCLUDED_BAND_USD) < CENT,
            "three voltage siblings sum to the declared $%.2f; got %d rows, $%.2f"
            % (D_EXCLUDED_BAND_USD, len(ex), exsum))
    flags = {r["included_in_mitigated_total"] for r in ex}
    other = {r["included_in_mitigated_total"] for r in G2 if r["kind"] != "excluded"}
    g.check("D7b", "D", flags == {"0"} and other == {"1"},
            "included_in_mitigated_total is 0 on exactly the three excluded "
            "rows and 1 on every other row")

    # D8 F4E-3: five channels, and the rider carries the mitigation
    got = {c: sum(num(r[c]) for r in G1) for c in D_CHANNELS}
    bad = [c for c in D_CHANNELS if abs(got[c] - D_CHANNELS[c]) >= CENT]
    g.check("D8a", "D", not bad,
            "the five mitigation channels sum to their declared portfolio "
            "figures" + ("" if not bad else "; off: %s" % {c: got[c] for c in bad}))
    order = sorted(D_CHANNELS, key=lambda c: got[c])
    g.check("D8b", "D", order == V3_ORDER,
            "channels ranked ascending are rider, energy, demand, fixed, "
            "statutory - the rider channel carries the mitigation (F4E-3); "
            "got %s" % order)
    csum = sum(got.values())
    msum = sum(num(r["mitigation_annual_usd"]) for r in G1)
    g.check("D8c", "D", abs(csum - msum) < CENT,
            "the five channels sum to mitigation_annual_usd; $%.6f vs $%.6f"
            % (csum, msum))

    # D9 the metered swap has no mitigated column (F5B-2)
    g.check("D9a", "D", "mitigated_usd_per_mwh" not in hdr,
            "the frozen contract carries NO mitigated metered-MWh column, so "
            "V1's remainder is unavailable on the metered swap (F5B-2)")
    g.check("D9b", "D", "usd_per_mwh" in hdr and "usd_per_it_mwh" in hdr,
            "both basis columns the swap needs are present")

    # D10 G1 default-basis sanity: the ranking metric is the IT one
    r1 = sorted(G1, key=lambda r: num(r["mitigated_usd_per_it_mwh"]))
    g.check("D10a", "D", [int(r["rank"]) for r in r1] == list(range(1, 9)),
            "rank is mitigated $/IT-MWh ascending")

    # D11 (Unit 5B-x) the G1 ties on usd_per_it_mwh, the column the reopen
    # probe perturbs. DECLARED: a perturbed Columbus fires D11a, D11b, D11c
    # and nothing else in group D. That firing is the positive control that
    # the perturbation reached the file (F5B-3).
    worst = 0.0
    bad = []
    for r in G1:
        it = num(r["it_annual_mwh"])
        d = abs(num(r["usd_per_it_mwh"]) - num(r["annual_usd"]) / it) if it else 1e9
        worst = max(worst, d)
        if d >= 1e-6:
            bad.append(r["metro"])
    g.check("D11a", "D", not bad,
            "usd_per_it_mwh = annual_usd / it_annual_mwh in every metro to "
            "1e-6; worst residual %.3e" % worst + ("" if not bad else "; off: %s" % bad))
    rb = sorted(G1, key=lambda r: num(r["usd_per_it_mwh"]))
    got = [int(r["rank_baseline"]) for r in rb]
    g.check("D11b", "D", got == list(range(1, 9)),
            "rank_baseline is usd_per_it_mwh ascending; got %s" % got)
    bad = []
    for r in G1:
        if r["is_market_priced"] != "1":
            continue
        ratio = num(r["usd_per_it_mwh"]) / num(r["usd_per_mwh"])
        lo = abs(num(r["band_low_usd_per_mwh"]) * ratio - num(r["band_low_usd_per_it_mwh"]))
        hi = abs(num(r["band_high_usd_per_mwh"]) * ratio - num(r["band_high_usd_per_it_mwh"]))
        if lo >= 1e-6 or hi >= 1e-6:
            bad.append(r["metro"])
    g.check("D11c", "D", not bad,
            "on every market-priced metro the IT-basis band is the metered band "
            "scaled by usd_per_it_mwh / usd_per_mwh (dictionary: 'the band on "
            "the SITING metric')" + ("" if not bad else "; off: %s" % bad))

    return {"headers": headers, "G1": G1, "G2": G2, "G3": G3, "G4": G4}


# ==========================================================================
# --- end MOVED group_d ---


# ==========================================================================
# Standalone runner (Unit 5H-0). The line format is the retired gate's, so the
# 29 lines can be compared byte for byte against era_ph5_5b_gate_run.log.
# ==========================================================================
def run(project):
    g = Gate()
    group_d(g, project)
    return g


def format_rows(g):
    return ["%-10s [%s] %-14s %s" % (status, grp, gid, msg)
            for gid, grp, status, msg in g.rows]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", default=".")
    ap.add_argument("--log", default=None)
    ap.add_argument("--quiet", action="store_true")
    a = ap.parse_args()
    g = run(a.project)
    out = ["era_ph5_grain_gate.py  Unit 5H-0  project=%s  python=%s  platform=%s"
           % (os.path.abspath(a.project), sys.version.split()[0], platform.platform()),
           "DECLARED (era_ph5_5h_results.md §1.2): 29 PASS on the pinned grains, lines identical to the",
           "  29 [D] lines of era_ph5_5b_gate_run.log; W15 -> {D2a,D2b,D2c,D3a}; W16 -> {D5a,D6a};",
           "  W24 -> {D11a,D11b,D11c}.",
           ""]
    out += format_rows(g)
    npass = sum(1 for r in g.rows if r[2] == "PASS")
    nfail = sum(1 for r in g.rows if r[2] == "FAIL")
    out.append("")
    out.append("RESULT %d PASS  %d FAIL  (group D, %d gates)" % (npass, nfail, len(g.rows)))
    txt = "\n".join(out)
    if not a.quiet:
        print(txt)
    if a.log:
        with open(a.log, "a", encoding="utf-8") as fh:
            fh.write(txt + "\n\n")
    return 0 if nfail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
