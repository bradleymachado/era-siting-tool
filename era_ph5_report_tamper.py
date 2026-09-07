#!/usr/bin/env python3
"""era_ph5_report_tamper.py — Unit 5H-5 of direction_ph5_html_v1.0.md

This section is intended to PROVE THAT era_ph5_report_gate.py IS CONNECTED —
to the data on one side and to the report file on the other — by firing each of
its groups from a declared positive control and requiring exactly the declared
set, nothing more and nothing less.

Discipline, unchanged from the page harness:
  * BASELINE is the clean copy's FAIL set. It is EMPTY, so every firing set
    below is ABSOLUTE rather than a delta (F5H3 onward).
  * X01 RUNS FIRST and the harness REFUSES a control-first run (F5B-3): a
    suite whose first evidence is "nothing fired" is not evidence.
  * N01, the unmodified control, RUNS LAST.
  * Every mutation asserts its needle is UNIQUE in the file before it edits,
    so a case that silently edits the wrong thing is impossible (5H-4 s16.2).

Each case is run in a fresh temporary copy of the project, in a SUBPROCESS, so
no module state and no cached gate run leaks between cases.

Usage
-----
  python era_ph5_report_tamper.py --project .
  python era_ph5_report_tamper.py --project . --log era_ph5_5h_report_tamper_run.log
"""

import argparse
import os
import platform
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))

REPORT = "era_ph5_report_v1.0.md"
GATE = "era_ph5_report_gate.py"
GRAIN_FILES = ["era_ph5_metro.csv", "era_ph5_stack.csv",
               "era_ph5_month.csv", "era_ph5_caveat.csv"]
SUPPORT = GRAIN_FILES + [
    REPORT, GATE,
    "era_ph5_grains_manifest.json", "era_ph5_dashboard.html",
    "era_ph5_style_v1.0.md", "era_ph5_dictionary_v1.0.md",
    "era_ph5_grain_gate.py", "era_ph5_build_html.py", "era_ph5_views.py",
    "era_ph5_page_gate.py", "era_ph5_page_tamper.py",
    "era_rates.db",
    "direction_ph5_tableau_v1.0.md", "direction_ph5_html_v1.0.md",
    "direction_ph4_close_v1.0.md",
]

BASELINE = set()

# case: (kind, declared firing set, why)
# The sets below are era_ph5_5h_results.md section 17.5's table, written BEFORE
# this harness existed. They are run as declared. A declaration that turns out
# to be incomplete is recorded as a MISS and amended beside itself, never
# edited to match the run (4A).
CASES = {
    "X01": ("data", {"D11a", "D11c", "R1", "R4", "R7", "C3"},
            "Chicago's usd_per_it_mwh is perturbed by +1.00 in a COPY of era_ph5_metro.csv. "
            "AMENDED after the first run MISSED (era_ph5_5h_results.md section 17.5a): D11a is the "
            "identity usd_per_it_mwh = annual_usd / it_annual_mwh; D11c scales the IT-basis band by "
            "usd_per_it_mwh / usd_per_mwh; R1 and R4 are the two blocks that DRAW the cell; R7 is "
            "the block that names each CSV's md5, which is the report's own freshness clause and "
            "the id the guess never considered; C3 is band_crossing_it, the one derivation that "
            "reads it. The four blocks on other grains and the credit gate on other cells stay "
            "PASS, and that is what scopes the case. RUNS FIRST (F5B-3)."),
    "X02": ("text", {"R1"},
            "one digit of Chicago's mitigated $/IT-MWh is changed INSIDE the ranking block in a "
            "copy of the report. The block no longer equals its regeneration from the grains. "
            "This is the case that proves R is connected to the FILE and not only to the data; "
            "the figure sits inside a block, so no credit gate reads it."),
    "X03": ("text", {"C1"},
            "a bare 47.67 with no credit comment is typed into a prose sentence. The uncredited "
            "count goes to one. C2/C3/C4 stay PASS because no existing credit moved, which is "
            "what scopes the firing."),
    "X04": ("text", {"C2"},
            "one credited figure's digits are changed while its credit comment is left alone: "
            "Austin's mitigation_pct_of_baseline is shown as a number that is not the cell it "
            "cites. C1 stays PASS - the figure is still credited - and that is the whole reason "
            "there are two gates and not one."),
    "X05": ("text", {"X1"},
            "H-3's forbidden sentence is typed into the report verbatim. The prohibition fires "
            "and nothing else does."),
    "N01": ("control", set(),
            "an unmodified copy: nothing fires beyond the baseline. RUNS LAST."),
}
ORDER = ["X01", "X02", "X03", "X04", "X05", "N01"]

FAILSET_RE = re.compile(r"^FAIL SET (.*)$", re.M)
RESULT_RE = re.compile(r"^RESULT (\d+) PASS  (\d+) FAIL", re.M)


def stage(project):
    d = tempfile.mkdtemp(prefix="ph5h5_")
    for name in SUPPORT:
        src = os.path.join(project, name)
        if os.path.isfile(src):
            shutil.copy2(src, os.path.join(d, name))
    rsrc = os.path.join(project, "renders")
    if os.path.isdir(rsrc):
        shutil.copytree(rsrc, os.path.join(d, "renders"))
    return d


def read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def write(path, txt):
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(txt)


def replace_unique(path, old, new):
    """Every mutation goes through here. The uniqueness assertion is what makes
    a stale needle a pre-run failure instead of a silently wrong edit."""
    txt = read(path)
    n = txt.count(old)
    if n != 1:
        raise AssertionError("needle %r occurs %d times in %s, expected 1"
                             % (old[:60], n, os.path.basename(path)))
    write(path, txt.replace(old, new))


def mutate(case, d):
    if case == "X01":
        p = os.path.join(d, "era_ph5_metro.csv")
        txt = read(p)
        # NEEDLE RE-DECLARED AT UNIT 6E-2 (F5H1-2: a declared tamper set is never inherited,
        # and neither is a needle that encodes a published value).  Chicago's
        # usd_per_it_mwh moved 81.53954845026165 -> 81.51756774397158 on the two_segment_ph6
        # basis.  The case is unchanged: +1.0 on the same cell of the same grain.
        old = "81.51756774397158"
        new = "82.51756774397158"
        n = txt.count(old)
        if n != 1:
            raise AssertionError("X01 needle %r occurs %d times, expected 1" % (old, n))
        write(p, txt.replace(old, new))
    elif case == "X02":
        p = os.path.join(d, REPORT)
        # Needle widened before the first suite run, not after: the two-cell form
        # occurs twice - the ranking row and the stack block's mitigated total -
        # and replace_unique refused it. Mechanics, not a declared-set change
        # (5H-4 s16.2).
        # RE-DECLARED AT UNIT 6E-2, same widened two-cell form, refreshed values.
        replace_unique(p, "| 81.52 | 591,516,515.88 | 74.94 | 8.07 |",
                       "| 81.52 | 591,516,515.88 | 74.95 | 8.07 |")
    elif case == "X03":
        p = os.path.join(d, REPORT)
        replace_unique(p, "Siting beats mitigating, and it is not close.",
                       "Siting beats mitigating by 47.67 and it is not close.")
    elif case == "X04":
        p = os.path.join(d, REPORT)
        # RE-DECLARED AT UNIT 6E-2: Austin's mitigation_pct_of_baseline 12.46 -> 12.37.
        replace_unique(p, "12.37<!--G:G1:Austin:mitigation_pct_of_baseline-->",
                       "12.47<!--G:G1:Austin:mitigation_pct_of_baseline-->")
    elif case == "X05":
        p = os.path.join(d, REPORT)
        replace_unique(
            p, "**Phase 5 is closed.**",
            "The chain reproduces the committed page to the byte.\n\n**Phase 5 is closed.**")
    elif case == "N01":
        pass
    else:
        raise AssertionError("unknown case %r" % case)


def run_gate(d):
    proc = subprocess.run(
        [sys.executable, os.path.join(d, GATE), "--project", d],
        capture_output=True, text=True)
    out = proc.stdout + proc.stderr
    m = FAILSET_RE.search(out)
    if not m:
        raise AssertionError("no FAIL SET line in gate output:\n%s" % out[-2000:])
    body = m.group(1).strip()
    fails = set() if body == "(empty)" else set(body.split())
    r = RESULT_RE.search(out)
    tally = (int(r.group(1)), int(r.group(2))) if r else (0, 0)
    return fails, tally, proc.returncode


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", default=".")
    ap.add_argument("--log", default=None)
    ap.add_argument("--only", default=None)
    a = ap.parse_args()
    project = os.path.abspath(a.project)

    out = ["era_ph5_report_tamper.py  Unit 5H-5  project=%s  python=%s  platform=%s"
           % (project, sys.version.split()[0], platform.platform()), ""]

    order = ORDER if not a.only else a.only.split(",")
    if order[0] != "X01":
        print("REFUSED: X01 runs first (F5B-3). A suite whose first evidence is a control "
              "is not evidence.")
        return 2

    base_dir = stage(project)
    try:
        base_fails, base_tally, base_rc = run_gate(base_dir)
    finally:
        shutil.rmtree(base_dir, ignore_errors=True)
    ok_base = base_fails == BASELINE
    out.append("BASELINE  clean report FAIL set is %s as declared (%d ids); %d PASS / %d FAIL, "
               "exit %d; the report is ACCEPTED and every firing set below is ABSOLUTE"
               % ("EMPTY" if not base_fails else sorted(base_fails), len(base_fails),
                  base_tally[0], base_tally[1], base_rc))
    out.append("")
    if not ok_base:
        out.append("REFUSED: the clean report does not gate clean; no tamper result would mean "
                   "anything. FAIL SET %s" % sorted(base_fails))
        txt = "\n".join(out)
        print(txt)
        if a.log:
            with open(a.log, "a", encoding="utf-8") as fh:
                fh.write(txt + "\n\n")
        return 2

    asdeclared = 0
    for cid in order:
        kind, declared, why = CASES[cid]
        d = stage(project)
        try:
            mutate(cid, d)
            fails, tally, rc = run_gate(d)
        finally:
            shutil.rmtree(d, ignore_errors=True)
        actual = fails - BASELINE
        hit = actual == declared
        asdeclared += 1 if hit else 0
        out.append("CASE %s  %s  (%s)" % (cid, "AS DECLARED" if hit else "MISS", kind))
        out.append("  declared: %s" % (sorted(declared) if declared else "(nothing fires)"))
        out.append("  actual  : %s" % (sorted(actual) if actual else "(nothing fired)"))
        if not hit:
            out.append("  UNDECLARED FIRING : %s" % (sorted(actual - declared) or "(none)"))
            out.append("  DECLARED BUT SILENT: %s" % (sorted(declared - actual) or "(none)"))
        out.append("  gate    : %d PASS / %d FAIL, exit %d" % (tally[0], tally[1], rc))
        out.append("  why     : %s" % why)
        out.append("")

    out.append("RESULT %d of %d AS DECLARED (%s ran first, %s last)"
               % (asdeclared, len(order), order[0], order[-1]))
    txt = "\n".join(out)
    print(txt)
    if a.log:
        with open(a.log, "a", encoding="utf-8") as fh:
            fh.write(txt + "\n\n")
    return 0 if asdeclared == len(order) else 1


if __name__ == "__main__":
    sys.exit(main())
