"""era_ph5_extract -- Unit 5A of direction_ph5_tableau_v1.0.md.

This section is intended to build the FOUR Phase 5 extract grains, gate them
against Unit 4R's frozen contract and against era_ph4_report_v1.1.md, and write
them beside the data dictionary and the style token spec.  NO TABLEAU WORK.

  G1  era_ph5_metro.csv    metro (8 rows)                 -- the frozen contract
                                                             plus derived fields,
                                                             nothing removed
  G2  era_ph5_stack.csv    metro x component               -- waterfall + channels
  G3  era_ph5_month.csv    metro x month x stage           -- seasonality, ratchet,
                                                             dispatch
  G4  era_ph5_caveat.csv   one row per caveat              -- Ruling P5-3, as DATA

Unit 5B-y (direction_ph5_branch_b_v1.0.md, Ruling E-5.1) EXTENDS this script, not rebuilds it:
the same run that writes the four CSVs also writes era_ph5_grains_manifest.json - per grain
md5, rows x cols, bytes and a UTC write stamp; plus db md5, user_version and this script's own
md5 - and gate P8a reads it back.  The manifest is the committed reference the workbook gate's
X13a (content) and X13b (order) assert against.  Commit it with the CSVs, always together.

NOTHING HERE RE-DERIVES A PHASE 4 FIGURE FROM SCRATCH.  The baseline, the
measures and the storage dispatch are produced by Unit 4B/4C/4D/4E's own
primitives and era_engine.py, called here, and every published figure is gated
against era_ph4e_published_v1.1.csv rather than recomputed independently.  The
one thing this unit genuinely derives is the MONTHLY decomposition, because the
engine does not produce one; era_ph5_monthly.py transcribes the engine's own
accumulation and P1 gates the transcription to the cent on every bill taken.

NO SQLITE WRITE ANYWHERE.  Read-only on era_rates.db.

Usage
  python era_ph5_extract.py                          # every group, write the four grains
  python era_ph5_extract.py --groups P0,P1           # cheap provenance + pin check
  python era_ph5_extract.py --no-write               # gates only (the tamper harness)
  python era_ph5_extract.py --log era_ph5_run.log    # APPEND mode, for batched runs
  python era_ph5_extract.py --summary --log era_ph5_run.log
"""

import argparse
import calendar
import contextlib
import csv
import hashlib
import importlib.util
import io
import json
import math
import re
import os
import sqlite3
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
QUIET = io.StringIO()


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


# =================================================================================================
# DECLARED CONSTANTS.  Everything a gate compares against is written down here, before the run.
# =================================================================================================

# Unit 4R's migrated database.  A session holding a different database is told that first.
DB_MD5 = "1c72e7a1b32c99a650d2e1fba17ae21e"
DB_USER_VERSION = 14
ACCEPTANCE_CSV_NAME = "era_acceptance_results_v1.6.csv"
# Unit 5B-y (direction_ph5_branch_b_v1.0.md, Ruling E-5.1): the manifest is the committed
# reference the workbook gate's X13 compares against - CONTENT (md5) and a UTC write stamp,
# never an mtime, so a git checkout cannot reset it. Written in the same run as the CSVs.
MANIFEST_NAME = "era_ph5_grains_manifest.json"
GRAIN_FILES = ["era_ph5_metro.csv", "era_ph5_stack.csv", "era_ph5_month.csv", "era_ph5_caveat.csv"]

CONTRACT_CSV = "era_ph4e_published_v1.1.csv"
CONTRACT_WIDTH = 52                    # Ruling 13, frozen by Unit 4R
PH4_REPORT = "era_ph4_report_v1.1.md"
PH2_REPORT = "era_ph2_report_v1.2.md"
PH4_STACK = "era_ph4e_stack.csv"
PH4_REPORT_CAVEAT_COUNT = 8            # section 8, after Unit 4R added Rulings 14 and 15

# Ruling 13's frozen 52 columns, in order.  A shape change fails P0d.
CONTRACT_COLUMNS = [
    "rank", "metro", "utility", "schedule_code", "voltage_level", "rider_coverage",
    "usd_per_mwh", "band_low_usd_per_mwh", "band_high_usd_per_mwh", "annual_usd", "annual_mwh",
    "market_pct", "demand_pct", "rider_pct", "energy_pct", "fixed_pct", "ratchet_binding",
    "pue_basis", "pue_level_L", "pue_alpha", "usd_per_it_mwh", "it_annual_mwh",
    "mean_pue_energy_weighted", "facility_peak_kw", "measure_ids", "measures_annual_usd",
    "measures_usd_per_it_mwh", "storage_config", "storage_strategy", "storage_annual_usd",
    "storage_usd_per_it_mwh", "mitigated_pre_storage_usd_per_it_mwh", "mitigated_annual_usd",
    "mitigated_usd_per_it_mwh", "mitigation_energy_channel_usd", "mitigation_demand_channel_usd",
    "mitigation_rider_usd", "mitigation_fixed_usd", "mitigation_statutory_usd",
    "mitigation_pct_of_baseline", "bracket_reading", "bracket_baseline_move_usd",
    "bracket_alt_storage_strategy", "mitigated_alt_usd_per_it_mwh", "mitigated_alt_annual_usd",
    "capex_caveat", "unpriced_caveat", "market_node_class", "market_construction", "pue_form",
    "pue_alpha_domain_max", "open_ruling_ids",
]

# G1's derived presentation fields.  DECLARED, so an addition that nobody documented fails P6a.
G1_DERIVED_COLUMNS = [
    "metro_key", "state", "station_name", "station_latitude", "station_longitude",
    "rank_baseline", "is_market_priced", "band_half_width_usd_per_mwh",
    "band_low_usd_per_it_mwh", "band_high_usd_per_it_mwh",
    "mitigation_usd_per_it_mwh", "mitigation_annual_usd",
    "measure_count", "has_bracket", "bracket_low_usd_per_it_mwh", "bracket_high_usd_per_it_mwh",
    "bracket_width_usd_per_it_mwh", "has_open_ruling", "open_ruling_count",
    "gap_to_next_usd_per_it_mwh", "pct_of_portfolio_baseline",
]

G2_COLUMNS = [
    "metro", "kind", "component_id", "component_name", "usd_per_year", "usd_per_it_mwh",
    "energy_channel_usd", "demand_channel_usd", "rider_usd", "fixed_usd", "statutory_usd",
    "included_in_mitigated_total", "waterfall_order", "waterfall_start_usd", "waterfall_end_usd",
    "note",
]

G3_COLUMNS = [
    "metro", "month", "month_name", "stage", "value_type", "load_series",
    "energy_usd", "market_usd", "demand_usd", "rider_usd", "fixed_usd", "statutory_usd",
    "total_usd", "kwh", "ncp_kw_15min", "ncp_kw_30min", "billed_kw_15min", "billed_kw_30min",
    "cp4_kw", "ratchet_binding", "storage_discharge_mwh", "storage_charge_mwh",
    "storage_cap_kw", "pue_basis",
]

G4_COLUMNS = [
    "caveat_id", "sort_rank", "category", "title", "metro_scope", "priced",
    "usd_per_year", "usd_per_it_mwh", "direction", "ruling_ref", "source_ref", "statement",
]

G3_STAGES = ["baseline", "measures", "storage", "mitigated"]
MONTH_NAME = {i: calendar.month_abbr[i] for i in range(1, 13)}

FACILITY_TAG = "plant_derived_4a"
BASE_VARIANT = "lf090"
STORAGE_CONFIG = "B100-4H"
CENT = 0.005
IT_TOL = 0.001
MWH_TOL = 0.0005

# Unit 4E's own declared exclusion.  Imported below from Unit 4D rather than retyped where it can
# be; this literal is the gate's independent quantity (4R's rule: a tamper that bends the
# declaration and the derivation together tests nothing).
VOLTAGE_SIBLING_EXCLUSION_USD = -741104525.28
VOLTAGE_SIBLING_EXCLUSION_IT = -93.894938

# Unit 4E's PRE-RULING portfolio literal, left exactly as 4E declared it, plus Unit 4M's MEASURED
# Columbus delta.  The post-ruling figure is DERIVED from the two rather than retyped - 4R's rule.
# era_ph4e_publish.py still holds the pre-ruling literal and its E4e is one of the eleven gates
# Unit 4R declared must fail on the migrated database.
PORTFOLIO_BASELINE_PRE_RULING_USD = 6687874026.81       # era_ph4e_publish.PORTFOLIO_BASELINE_USD
COLUMBUS_RULING8_BASELINE_DELTA_USD = 6261839.41        # Unit 4M, measured, not re-derived
PORTFOLIO_TOL_USD = 1.0

# The two metros the frozen contract carries an open ruling on.  DERIVED from G1 at P2g; this
# literal is what the derivation is checked against.
OPEN_RULING_METROS = {"Chicago": "F4C-7", "Northern Virginia": "F4B-2"}

# The three market-priced metros (Ruling 8's ratified construction applies to exactly these).
MARKET_PRICED_METROS = ["Chicago", "Columbus", "Dallas-Fort Worth"]
MARKET_PRICE_BAND_PCT = 0.25

# Metro -> (state, weather key).  The weather key is the engine's own; the state is the EPW
# LOCATION line's own field, read from the file, not typed.
METRO_STATE_FROM_EPW = True

# P1's declared count: the number of distinct (connection, schedule, profile) bills this unit
# takes a monthly decomposition of.  8 baselines + FIVE measure scenarios + 8 storage scenarios.
# Five, not six: M-SJ-PF is a CORRECTION applied outside the engine, because the engine does not
# evaluate the mechanic the database holds (F4D-6).  The one measure that takes no bill is the one
# that is not a tariff election, and the count is where that shows.
MONTHLY_BILLS_EXPECTED = 21

PREDICTIONS = [
    ("Q1", "G3's baseline stage will tie to G1 to the cent on all eight metros, because the "
           "monthly transcription is the engine's own accumulation and P1 gates it first."),
    ("Q2", "The stale-Columbus problem in the two existing monthly CSVs is NOT a stale "
           "DETERMINANT problem: a market energy rate does not enter kWh or kW, so "
           "era_ph4a_engine_monthly.csv's determinants are still correct on the migrated "
           "database. They are unusable for G3 anyway because neither file carries a dollar."),
    ("Q3", "The published basis is the FACILITY basis (plant_derived_4a), so "
           "era_ph4a_engine_monthly.csv is the determinant series on the published basis and "
           "era_engine_v1.2_monthly.csv is not."),
    ("Q4", "Northern Virginia will be the only metro with a binding ratchet month in G3."),
    ("Q5", "No min_monthly_bill will bind on any metro, so every dollar in G3 decomposes."),
    ("Q6", "G4 will hold more UNPRICED rows than the report's section 8 holds caveats, because "
           "section 8 is a caveat list and G4 is a caveat list plus the unpriced items and the "
           "open rulings."),
]

# =================================================================================================
# Gate machinery: groups, an append-mode log, and a summary pass (the 45-second cap)
# =================================================================================================

FAILURES = []
RESULTS = []
_LOG = [None]


def emit(line):
    print(line)
    if _LOG[0] is not None:
        _LOG[0].write(line + "\n")


def hr(t):
    emit("=" * 100)
    emit(t)
    emit("=" * 100)


def gate(gid, condition, message):
    ok = bool(condition)
    RESULTS.append((gid, ok))
    emit(f"  {'PASS' if ok else 'FAIL':<6} {gid}  {message}")
    if not ok:
        FAILURES.append(f"{gid} {message}")
    return ok


def close(a, b, tol):
    if a is None or b is None:
        return False
    return abs(a - b) <= tol


def fnum(s):
    if s is None or s == "":
        return None
    return float(s)


# =================================================================================================
# Build helpers
# =================================================================================================

def epw_location(weather_dir, metro_key):
    """(station_name, state, lat, lon) from the metro's OWN EPW LOCATION line.

    The map point is the WEATHER STATION this project's PUE overlay is driven by, not a site.
    The column names say so and the dictionary says so.
    """
    hits = sorted(Path(weather_dir).glob(f"{metro_key}_*.epw"))
    if not hits:
        return None
    parts = hits[0].open(encoding="latin-1").readline().strip().split(",")
    if len(parts) < 8 or parts[0].upper() != "LOCATION":
        return None
    return parts[1], parts[2], float(parts[6]), float(parts[7])


def read_contract(project):
    rows = list(csv.DictReader((project / CONTRACT_CSV).open(encoding="utf-8")))
    cols = list(csv.reader((project / CONTRACT_CSV).open(encoding="utf-8")))[0]
    return rows, cols


def md5_of(path):
    h = hashlib.md5()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def money_strings(x):
    """Every formatting this project uses for a dollar figure, so a reconciliation against a
    published document is a search for the DOCUMENT'S OWN rendering and not for a float."""
    a = abs(x)
    return {f"{a:,.0f}", f"{a:,.2f}", f"{a / 1e6:,.1f}", f"{a:.4f}", f"{a:,.4f}",
            f"{a:.6f}", f"{a:.2f}", f"{a:,.1f}"}


def write_csv(path, columns, rows, no_write):
    if no_write:
        return
    tmp = Path(str(path) + ".tmp")
    with tmp.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=columns)
        w.writeheader()
        for r in rows:
            w.writerow({c: r.get(c, "") for c in columns})
    os.replace(tmp, path)


def write_text(path, text, no_write):
    if no_write:
        return
    tmp = Path(str(path) + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    os.replace(tmp, path)


def utc_now_iso():
    """ISO 8601, UTC, whole seconds, 'Z' suffix.  Floored to the second so that a Tableau
    extract stamped in the same second (Tableau writes seconds) compares >= and not <."""
    import datetime
    return datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).strftime(
        "%Y-%m-%dT%H:%M:%SZ")


def write_manifest(project, conn, grains):
    """Unit 5B-y, Ruling E-5.1.  `grains` maps G1..G4 to (rows, columns) as just written.
    The md5 is taken from the FILE ON DISK after os.replace, not from the rows in memory, and
    written_utc is taken AFTER the last CSV landed, so 'extract update-time >= written_utc'
    (X13b) can only hold for an extract built from these bytes or later ones."""
    files = dict(zip(("G1", "G2", "G3", "G4"), GRAIN_FILES))
    entries = {}
    for gk, fn in files.items():
        rows, cols = grains[gk]
        p = project / fn
        entries[fn] = {"grain": gk, "md5": md5_of(p), "rows": len(rows), "cols": len(cols),
                       "bytes": p.stat().st_size}
    stamp = utc_now_iso()
    for e in entries.values():
        e["written_utc"] = stamp
    manifest = {
        "manifest": MANIFEST_NAME,
        "ruling": "direction_ph5_branch_b_v1.0.md E-5.1 (P5-2b)",
        "written_by": Path(__file__).name,
        "script_md5": md5_of(Path(__file__).resolve()),
        "written_utc": stamp,
        "db_file": Path(str(conn.execute("pragma database_list").fetchone()[2])).name,
        "db_md5": md5_of(conn.execute("pragma database_list").fetchone()[2]),
        "user_version": conn.execute("pragma user_version").fetchone()[0],
        "grains": entries,
    }
    write_text(project / MANIFEST_NAME, json.dumps(manifest, indent=2) + "\n", False)
    return manifest


# =================================================================================================
# main
# =================================================================================================

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", default=None,
                    help="the project folder (defaults to this file's own parent)")
    ap.add_argument("--groups", default=None,
                    help="comma-separated group ids to run, e.g. P0,P1 (default: all)")
    ap.add_argument("--log", default=None, help="APPEND the run to this file")
    ap.add_argument("--summary", action="store_true",
                    help="read the log and print the pass/fail tally, running nothing")
    ap.add_argument("--no-write", action="store_true", help="run every gate, emit no file")
    ap.add_argument("--profile-dir", default=None,
                    help="Unit 2D/4A profile directory (defaults to <project>/data/profiles); "
                         "the tamper harness points a small working copy of the project at the "
                         "real one rather than copying 79 MB of profiles per case")
    ap.add_argument("--weather-dir", default=None,
                    help="EPW directory (defaults to <project>/data/weather)")
    args = ap.parse_args()

    project = Path(args.project).resolve() if args.project else HERE
    log_path = Path(args.log) if args.log else None

    if args.summary:
        if not log_path or not log_path.exists():
            print("--summary needs an existing --log")
            sys.exit(2)
        seen, bad = {}, []
        for line in log_path.read_text(encoding="utf-8").splitlines():
            m = re.match(r"\s+(PASS|FAIL)\s+(P\d+[a-z]*)\s", line)
            if m:
                seen[m.group(2)] = m.group(1)
        for gid, st in sorted(seen.items()):
            if st == "FAIL":
                bad.append(gid)
        print(f"era_ph5_extract summary from {log_path.name}: {len(seen)} distinct gates, "
              f"{len(seen) - len(bad)} PASS, {len(bad)} FAIL")
        if bad:
            print("  FAIL: " + ", ".join(bad))
        sys.exit(1 if bad else 0)

    if log_path:
        _LOG[0] = log_path.open("a", encoding="utf-8")
        _LOG[0].write(f"\n\n### era_ph5_extract.py groups={args.groups or 'ALL'} "
                      f"no_write={args.no_write}\n")

    want = None if not args.groups else {g.strip() for g in args.groups.split(",")}

    def run(g):
        return want is None or g in want

    E = _load("era_engine", project / "era_engine.py")
    S = _load("era_ph4b_scenario", project / "era_ph4b_scenario.py")
    Z = _load("era_ph4c_storage", project / "era_ph4c_storage.py")
    D = _load("era_ph4d_measures", project / "era_ph4d_measures.py")
    M = _load("era_ph5_monthly", HERE / "era_ph5_monthly.py")
    if args.profile_dir:
        E.PROFILE_DIR = Path(args.profile_dir)
    weather_dir = Path(args.weather_dir) if args.weather_dir else project / "data" / "weather"

    emit("")
    hr("Unit 5A predictions, written down before the run")
    for pid, text in PREDICTIONS:
        emit(f"  {pid}  {text}")

    conn = sqlite3.connect(E.DB_FILE)
    conn.row_factory = sqlite3.Row
    lst = E.build_lst_index()

    # ---------------------------------------------------------------------------------------
    # P0 - provenance.  A session holding the wrong database is told that before anything else.
    # ---------------------------------------------------------------------------------------
    contract_rows, contract_cols = read_contract(project)
    report_text = (project / PH4_REPORT).read_text(encoding="utf-8")
    ph2_text = (project / PH2_REPORT).read_text(encoding="utf-8")

    if run("P0"):
        emit("")
        hr("P0 - provenance: the migrated database, the frozen contract, the published report")
        db_md5 = md5_of(E.DB_FILE)
        gate("P0a", db_md5 == DB_MD5,
             f"era_rates.db is Unit 4R's migrated image, md5 {db_md5} against the declared "
             f"{DB_MD5}. Every figure below is a function of this file")
        uv = conn.execute("pragma user_version").fetchone()[0]
        integ = conn.execute("pragma integrity_check").fetchone()[0]
        gate("P0b", uv == DB_USER_VERSION and integ == "ok",
             f"user_version {uv} (declared {DB_USER_VERSION}, Ruling 11 forbids a schema change "
             f"here) and integrity_check '{integ}'")
        gate("P0c", E.ACCEPTANCE_CSV.name == ACCEPTANCE_CSV_NAME,
             f"era_engine.py's ACCEPTANCE_CSV default is {E.ACCEPTANCE_CSV.name}, the target "
             f"Unit 4R re-aimed it at (F4R-1). No --acceptance-csv is passed anywhere in this "
             f"unit and passing one would be the defect")
        with contextlib.redirect_stdout(QUIET):
            f1_ok, f1_fail = E.run_f1_regression(conn, lst)
        gate("P0d", f1_ok,
             f"the engine's own F1 correctness gate PASSES against {E.ACCEPTANCE_CSV.name} "
             f"({len(f1_fail)} failing check(s)) - the project's gate is stronger than this "
             f"unit's and it fires first")
        gate("P0e", contract_cols == CONTRACT_COLUMNS and len(contract_cols) == CONTRACT_WIDTH,
             f"{CONTRACT_CSV} is the frozen Ruling 13 contract: {len(contract_cols)} columns "
             f"against the declared {CONTRACT_WIDTH}, in the declared order")
        gate("P0f", len(contract_rows) == 8,
             f"the contract carries {len(contract_rows)} metro rows (8 expected)")
        cav = re.findall(r"^(\d+)\.\s+\*\*", report_text.split("## 8 ")[1].split("## 9 ")[0],
                         flags=re.M)
        gate("P0g", len(cav) == PH4_REPORT_CAVEAT_COUNT,
             f"{PH4_REPORT} section 8 holds {len(cav)} numbered caveats against the declared "
             f"{PH4_REPORT_CAVEAT_COUNT} - Unit 4R added Ruling 14's bias and Ruling 15's alpha "
             f"domain, so a unit written against v1.0's five would be reconciling the wrong list")

    # ---------------------------------------------------------------------------------------
    # Bills.  Everything below uses era_engine.py and Units 4B/4C/4D's own primitives.
    # ---------------------------------------------------------------------------------------
    scheds = [dict(s) for s in conn.execute(E.SCHEDULE_SQL)]
    by_code = {s["schedule_code"]: s for s in scheds}
    metros = sorted({s["metro"] for s in scheds})
    codes_by_metro = {}
    for s in scheds:
        codes_by_metro.setdefault(s["metro"], []).append(s["schedule_code"])
    SELECTED = dict(Z.SELECTED)

    fl = []
    GEO, PROF = {}, {}
    with contextlib.redirect_stdout(QUIET):
        for m in metros:
            PROF[m] = E.load_facility_profile(m, E.METRO_WEATHER_KEY[m], BASE_VARIANT,
                                              FACILITY_TAG, fl)
            cal = E.build_billing_calendar(lst, E.METRO_OBSERVES_DST[m])
            cp4m, _ = E.build_cp4_masks(cal)
            pmap = {c: E.build_period_map(conn, by_code[c]["schedule_id"], "demand", cal, fl, m)
                    for c in codes_by_metro[m]}
            GEO[m] = {"cal": cal, "cp4": cp4m, "pmap": pmap, "days": Z.day_index_for(cal)}
    pin = {m: PROF[m].peak_kw for m in metros}

    monthly_taken = []          # (label, engine_result, monthly_result)

    def take(label, cn, sched, prof, pin_kw):
        """One bill, taken twice: the engine's annual and this unit's monthly. Both are kept so
        P1b can gate the transcription on EVERY bill the unit uses, not on a sample."""
        with contextlib.redirect_stdout(QUIET), S.contract_pinned(pin_kw):
            ann = E.bill_schedule(cn, sched, prof, lst, [])
            mon = M.bill_monthly(E, cn, sched, prof, lst)
        monthly_taken.append((label, ann, mon))
        return ann, mon

    base, base_m = {}, {}
    for m in metros:
        base[m], base_m[m] = take(f"baseline/{m}", conn, by_code[SELECTED[m]], PROF[m], pin[m])

    # --- the six mitigated-stack measures, re-priced here exactly as Unit 4E prices them -------
    resolved = {mid: D.rate_ids_for(conn, code, comps)
                for mid, (code, comps, n) in D.RATE_EDITS.items()}
    il_row = {"rate_id": 1 + max(r[0] for r in conn.execute("SELECT MAX(rate_id) FROM rate")),
              "schedule_id": by_code["BESH-HV"]["schedule_id"], "rate_period_id": None,
              "charge_type": "rider", "component_name": "rider_rea_self_direct_adjustment",
              "tier_index": 0, "rate_value": -D.IL_SELF_DIRECT_CREDIT_USD_PER_KWH,
              "rate_adj": 0.0, "unit": "USD_per_kWh", "billing_determinant": "energy_kwh",
              "determinant_is_assumption": 0, "tier_min": None, "tier_max": None,
              "tier_unit": None, "applicable_months": None, "effective_date": "2026-06-01",
              "is_assumption": 0, "is_market_price": 0,
              "source_note": "Unit 4D, re-derived by Unit 5A."}

    MEAS = {}

    def zero_month():
        return {mth: {"energy_usd": 0.0, "market_usd": 0.0, "demand_usd": 0.0,
                      "rider_usd": 0.0, "fixed_usd": 0.0, "statutory_usd": 0.0}
                for mth in range(1, 13)}

    def month_delta(scn_m, bas_m):
        out = zero_month()
        for mth in range(1, 13):
            for c in M.COMPONENTS:
                out[mth][c] = scn_m["monthly"][mth][c] - bas_m["monthly"][mth][c]
        return out

    def put(mid, metro, scn_total, channels, monthly, note):
        b = base[metro]
        MEAS[mid] = {
            "measure_id": mid, "metro": metro,
            "delta_total_usd": scn_total - b["total_usd"],
            "delta_usd_per_it_mwh": (scn_total - b["total_usd"]) / b["it_annual_mwh"],
            "delta_energy_channel_usd": channels[0], "delta_demand_channel_usd": channels[1],
            "delta_rider_usd": channels[2], "delta_fixed_usd": channels[3],
            "delta_statutory_usd": channels[4], "monthly": monthly, "note": note}

    def chan(b, s):
        return (s["energy_usd"] + s["market_usd"] - b["energy_usd"] - b["market_usd"],
                s["demand_usd"] - b["demand_usd"], s["rider_usd"] - b["rider_usd"],
                s["fixed_usd"] - b["fixed_usd"], 0.0)

    for mid, code in (("M-NOVA-RPS", "GS-4"), ("M-CHI-EEPP", "BESH-HV")):
        mt = by_code[code]["metro"]
        v = D.variant_db(conn, drop_ids=resolved[mid], add_rows=[])
        r, rm = take(f"{mid}/{mt}", v, by_code[code], PROF[mt], pin[mt])
        put(mid, mt, r["total_usd"], chan(base[mt], r), month_delta(rm, base_m[mt]),
            "rider removed from an in-memory rate-table clone")

    v_il = D.variant_db(conn, drop_ids=[], add_rows=[il_row])
    r_il, rm_il = take("M-CHI-RPS/Chicago", v_il, by_code["BESH-HV"], PROF["Chicago"],
                       pin["Chicago"])
    put("M-CHI-RPS", "Chicago", r_il["total_usd"], chan(base["Chicago"], r_il),
        month_delta(rm_il, base_m["Chicago"]),
        "credit row added to an in-memory rate-table clone")

    r_hlf, rm_hlf = take("M-AUS-HLF/Austin", conn, by_code["COMM-PRI-20MW-HLF"], PROF["Austin"],
                         pin["Austin"])
    put("M-AUS-HLF", "Austin", r_hlf["total_usd"], chan(base["Austin"], r_hlf),
        month_delta(rm_hlf, base_m["Austin"]),
        "schedule swap COMM-PRI-20MW -> COMM-PRI-20MW-HLF")

    v_ex = D.variant_db(conn, drop_ids=resolved["M-COL-EXCISE"], add_rows=[])
    r_ex, rm_ex = take("M-COL-EXCISE/Columbus", v_ex, by_code["DCT-T"], PROF["Columbus"],
                       pin["Columbus"])
    kwh_year = sum(PROF["Columbus"].kw15) * E.INTERVAL_HOURS
    sa = (min(kwh_year, D.OHIO_SA_RATE_LOW_KWH) * D.OHIO_SA_RATE_FIRST
          + max(0.0, kwh_year - D.OHIO_SA_RATE_LOW_KWH) * D.OHIO_SA_RATE_EXCESS
          + D.OHIO_SA_ANNUAL_FEE_USD * D.OHIO_SA_METERS)
    ch_ex = chan(base["Columbus"], r_ex)
    md_ex = month_delta(rm_ex, base_m["Columbus"])
    # ORC 5727.81(C) is an ANNUAL self-assessment with an annual 500 GWh tier breakpoint and an
    # annual per-location fee. It has no monthly form in the statute, so G3 carries it as a
    # DECLARED ALLOCATION on the month's share of metered kWh. The dictionary says so and G4
    # carries it as a caveat; the annual total is exact either way.
    kwh_by_month = {mth: base_m["Columbus"]["determinants"][mth]["kwh"] for mth in range(1, 13)}
    kwh_tot = sum(kwh_by_month.values())
    for mth in range(1, 13):
        md_ex[mth]["statutory_usd"] = sa * kwh_by_month[mth] / kwh_tot
    put("M-COL-EXCISE", "Columbus", r_ex["total_usd"] + sa,
        (ch_ex[0], ch_ex[1], ch_ex[2], ch_ex[3], sa), md_ex,
        "ORC 5727.81(C) self-assessment: tariff rider removed, statutory liability booked "
        "separately because it is not a tariff quantity")

    par = json.loads([dict(r) for r in conn.execute(
        "SELECT m.* FROM billing_mechanic m JOIN schedule s ON s.schedule_id = m.schedule_id "
        "WHERE m.mechanic_type = ? AND s.schedule_code = 'B-20-T'",
        (D.PF_MECHANIC_TYPE,))][0]["params"])
    pf_points = int(round(abs(E.POWER_FACTOR - par["basis_pf"]) * 100))
    pf_usd_per_kwh = -pf_points * par["usd_per_kwh_per_point"]
    sj = "San Jose / Bay Area"
    pf_usd = pf_usd_per_kwh * base[sj]["annual_mwh"] * 1000.0
    md_pf = zero_month()
    for mth in range(1, 13):
        md_pf[mth]["rider_usd"] = pf_usd_per_kwh * base_m[sj]["determinants"][mth]["kwh"]
    put("M-SJ-PF", sj, base[sj]["total_usd"] + pf_usd, (0.0, 0.0, pf_usd, 0.0, 0.0), md_pf,
        "correction applied outside the engine; the engine does not evaluate the mechanic")

    # --- storage, re-dispatched here through Unit 4C's own primitives --------------------------
    CFG = next(c for c in Z.CONFIGS if c["id"] == STORAGE_CONFIG)
    for m in metros:
        p = PROF[m]
        tg = Z.kw_targets(conn, by_code[SELECTED[m]], max(p.kw15))
        mk = [Z.target_mask(t, GEO[m]["pmap"][SELECTED[m]], GEO[m]["cp4"], GEO[m]["cal"])
              for t in tg]
        GEO[m]["targets"], GEO[m]["masks"] = tg, mk
        GEO[m]["ceil"] = Z.build_ceilings(tg, mk, p.kw15, p.kw30, GEO[m]["cal"])
        GEO[m]["strats"] = Z.strategies_for(m, tg, mk, GEO[m]["cal"])

    def dispatch(m, strat, keep_monthly):
        p = PROF[m]
        bat = Z.Battery(CFG["p_kw"], CFG["e_kwh"])
        caps, _ = Z.deepest_caps(p.kw15, GEO[m]["cal"], strat["mask"], GEO[m]["ceil"], bat,
                                 GEO[m]["days"])
        changes, per_day = Z.dispatch_days(p.kw15, GEO[m]["cal"], strat["mask"], GEO[m]["ceil"],
                                           bat, caps, GEO[m]["days"])
        if changes is None:
            return None
        new15 = Z.apply_changes(p.kw15, changes)
        scn = S.rebuild(p, new15)
        if keep_monthly:
            r_on, m_on = take(f"storage/{m}/{strat['id']}", conn, by_code[SELECTED[m]], scn,
                              pin[m])
        else:
            with contextlib.redirect_stdout(QUIET), S.contract_pinned(pin[m]):
                r_on = E.bill_schedule(conn, by_code[SELECTED[m]], scn, lst, [])
            m_on = None
        by_month_dis, by_month_chg = {mth: 0.0 for mth in range(1, 13)}, \
                                     {mth: 0.0 for mth in range(1, 13)}
        for d in per_day:
            by_month_dis[d["month"]] += d["discharge_kwh"] / 1000.0
            by_month_chg[d["month"]] += d["charge_kwh"] / 1000.0
        return {"strategy": strat["id"], "scn": scn, "r_on": r_on, "m_on": m_on, "caps": caps,
                "delta_total_usd": r_on["total_usd"] - base[m]["total_usd"],
                "delta_usd_per_it_mwh": ((r_on["total_usd"] - base[m]["total_usd"])
                                         / base[m]["it_annual_mwh"]),
                "delta_energy_channel_usd": (r_on["energy_usd"] + r_on["market_usd"]
                                             - base[m]["energy_usd"] - base[m]["market_usd"]),
                "delta_demand_channel_usd": r_on["demand_usd"] - base[m]["demand_usd"],
                "delta_rider_usd": r_on["rider_usd"] - base[m]["rider_usd"],
                "delta_fixed_usd": r_on["fixed_usd"] - base[m]["fixed_usd"],
                "discharge_mwh_by_month": by_month_dis, "charge_mwh_by_month": by_month_chg,
                "discharge_mwh": sum(d["discharge_kwh"] for d in per_day) / 1000.0,
                "charge_mwh": sum(d["charge_kwh"] for d in per_day) / 1000.0,
                "days": len(per_day)}

    STOR = {}
    for m in metros:
        cand = [o for o in (dispatch(m, st, False) for st in GEO[m]["strats"]) if o is not None]
        best = min(cand, key=lambda o: o["delta_total_usd"])
        st = next(s for s in GEO[m]["strats"] if s["id"] == best["strategy"])
        STOR[m] = dispatch(m, st, True)         # re-run the winner, this time keeping monthly

    # ---------------------------------------------------------------------------------------
    # P1 - the monthly transcription is the only thing this unit derives that the engine does
    #      not. It is pinned to the engine's source and gated on EVERY bill, not a sample.
    # ---------------------------------------------------------------------------------------
    if run("P1"):
        emit("")
        hr("P1 - the monthly decomposition, pinned to era_engine.bill_schedule and gated on it")
        live = hashlib.sha256(M.bill_schedule_source(E).encode()).hexdigest()
        gate("P1a", live == M.BILL_SCHEDULE_SHA256,
             f"era_ph5_monthly.py is a transcription of era_engine.bill_schedule and PINS its "
             f"source by content hash: live {live[:16]}... against the declared "
             f"{M.BILL_SCHEDULE_SHA256[:16]}... If the engine's billing changes, this file is "
             f"stale and this gate says so before any number is published")
        worst, worstn = 0.0, ""
        for label, ann, mon in monthly_taken:
            for c in M.COMPONENTS + ("total_usd",):
                d = abs(mon["annual"][c] - ann[c])
                if d > worst:
                    worst, worstn = d, f"{label}/{c}"
        gate("P1b", worst <= CENT and len(monthly_taken) == MONTHLY_BILLS_EXPECTED,
             f"the twelve monthly figures sum to era_engine.bill_schedule's own annual figure on "
             f"every one of {len(monthly_taken)} bills this unit takes (declared "
             f"{MONTHLY_BILLS_EXPECTED}), for every component: worst ${worst:.9f} on {worstn}. "
             f"A second implementation of one arithmetic is a second thing to drift; this is the "
             f"gate that makes the drift unpublishable")
        binding = [lab for lab, _, mon in monthly_taken if mon["min_bill_binding"]]
        gate("P1c", not binding,
             f"no min_monthly_bill binds on any bill taken here ({len(binding)} binding). The "
             f"engine applies that floor to the ANNUAL subtotal, so a binding floor is the one "
             f"charge in the library with no monthly form - PREDICTION Q5")
        flat = []
        for m in metros:
            tot = [base_m[m]["monthly"][mth]["total_usd"] for mth in range(1, 13)]
            if (max(tot) - min(tot)) / (sum(tot) / 12.0) < 0.01:
                flat.append(m)
        gate("P1d", not flat,
             f"VACUITY GUARD: no metro's monthly series is a flat twelfth of its annual bill "
             f"({len(flat)} flat). A decomposition that returned annual/12 would satisfy every "
             f"tie in P4 and carry no information")
        # P1e/P1f - the basis question the direction file says is the unit's real problem.
        e12 = list(csv.DictReader((project / "era_engine_v1.2_monthly.csv").open()))
        p4a = list(csv.DictReader((project / "era_ph4a_engine_monthly.csv").open()))
        dollar_cols = [c for f in (e12, p4a) for c in f[0].keys() if "usd" in c.lower()]
        gate("P1e", not dollar_cols,
             f"NEITHER existing monthly CSV carries a dollar column ({len(dollar_cols)} found): "
             f"era_engine_v1.2_monthly.csv and era_ph4a_engine_monthly.csv are DETERMINANT "
             f"series (kWh and kW), not cost series. Whichever basis they are on, neither can be "
             f"G3, and that - not staleness - is why G3 is re-derived here")
        p4a_fac = all(FACILITY_TAG in r["profile"] for r in p4a)
        e12_fac = any(FACILITY_TAG in r["profile"] for r in e12)
        w4, w4n = 0.0, ""
        w1, w1n = 0.0, ""
        for r in p4a:
            if BASE_VARIANT not in r["profile"] or r["schedule_code"] != SELECTED[r["metro"]]:
                continue
            d = abs(float(r["kwh"]) - base_m[r["metro"]]["determinants"][int(r["month"])]["kwh"])
            if d > w4:
                w4, w4n = d, f"{r['metro']}/{r['month']}"
        for r in e12:
            if BASE_VARIANT not in r["profile"] or r["schedule_code"] != SELECTED[r["metro"]]:
                continue
            d = abs(float(r["kwh"]) - base_m[r["metro"]]["determinants"][int(r["month"])]["kwh"])
            if d > w1:
                w1, w1n = d, f"{r['metro']}/{r['month']}"
        gate("P1f", p4a_fac and not e12_fac and w4 <= 1e-6 and w1 > 1e6,
             f"THE BASIS QUESTION, ANSWERED BY MEASUREMENT: era_ph4a_engine_monthly.csv is on the "
             f"PUBLISHED facility basis ({FACILITY_TAG}) and its monthly kWh reproduces this "
             f"run's baseline determinants on the MIGRATED database to {w4:.9f} kWh (worst "
             f"{w4n}); era_engine_v1.2_monthly.csv is on the Phase 2 metered basis and differs by "
             f"{w1:,.0f} kWh (worst {w1n}). PREDICTIONS Q2 AND Q3: the facility determinant "
             f"series is NOT stale under Ruling 8 - a market ENERGY RATE does not enter a kWh or "
             f"a kW - so 'Columbus is stale in both' is true of the two files' DOLLARS, which "
             f"neither of them has")

    # ---------------------------------------------------------------------------------------
    # G1 - the frozen contract plus derived presentation fields. NOTHING REMOVED.
    # ---------------------------------------------------------------------------------------
    portfolio_base = sum(fnum(r["annual_usd"]) for r in contract_rows)
    by_metro_c = {r["metro"]: r for r in contract_rows}
    order = sorted(contract_rows, key=lambda r: fnum(r["mitigated_usd_per_it_mwh"]))
    base_order = sorted(contract_rows, key=lambda r: fnum(r["usd_per_it_mwh"]))
    base_rank = {r["metro"]: i + 1 for i, r in enumerate(base_order)}

    g1 = []
    for i, r in enumerate(order):
        m = r["metro"]
        row = dict(r)
        key = E.METRO_WEATHER_KEY[m]
        loc = epw_location(weather_dir, key)
        mkt_usd = fnum(r["market_pct"]) / 100.0 * fnum(r["annual_usd"])
        bl, bh = fnum(r["band_low_usd_per_mwh"]), fnum(r["band_high_usd_per_mwh"])
        itm = fnum(r["it_annual_mwh"])
        mit = fnum(r["mitigated_usd_per_it_mwh"])
        alt = fnum(r["mitigated_alt_usd_per_it_mwh"])
        ids = [x for x in (r["open_ruling_ids"] or "").split(";") if x]
        mids = [x for x in (r["measure_ids"] or "").split(";") if x]
        nxt = order[i + 1] if i + 1 < len(order) else None
        row.update({
            "metro_key": key,
            "station_name": loc[0] if loc else "",
            "state": loc[1] if loc else "",
            "station_latitude": f"{loc[2]:.5f}" if loc else "",
            "station_longitude": f"{loc[3]:.5f}" if loc else "",
            "rank_baseline": base_rank[m],
            "is_market_priced": 1 if mkt_usd > 0 else 0,
            "band_half_width_usd_per_mwh": (f"{(bh - bl) / 2.0:.8f}" if bl is not None else ""),
            "band_low_usd_per_it_mwh": (f"{(fnum(r['annual_usd']) - mkt_usd * MARKET_PRICE_BAND_PCT) / itm:.8f}"
                                        if bl is not None else ""),
            "band_high_usd_per_it_mwh": (f"{(fnum(r['annual_usd']) + mkt_usd * MARKET_PRICE_BAND_PCT) / itm:.8f}"
                                         if bl is not None else ""),
            "mitigation_annual_usd": f"{fnum(r['measures_annual_usd']) + fnum(r['storage_annual_usd']):.8f}",
            "mitigation_usd_per_it_mwh": f"{fnum(r['measures_usd_per_it_mwh']) + fnum(r['storage_usd_per_it_mwh']):.8f}",
            "measure_count": len(mids),
            "has_bracket": 1 if alt is not None else 0,
            "bracket_low_usd_per_it_mwh": f"{min(mit, alt):.8f}" if alt is not None else f"{mit:.8f}",
            "bracket_high_usd_per_it_mwh": f"{max(mit, alt):.8f}" if alt is not None else f"{mit:.8f}",
            "bracket_width_usd_per_it_mwh": f"{abs(mit - alt):.8f}" if alt is not None else "0",
            "has_open_ruling": 1 if ids else 0,
            "open_ruling_count": len(ids),
            "gap_to_next_usd_per_it_mwh": (f"{fnum(nxt['mitigated_usd_per_it_mwh']) - mit:.8f}"
                                           if nxt is not None else ""),
            "pct_of_portfolio_baseline": f"{100.0 * fnum(r['annual_usd']) / portfolio_base:.8f}",
        })
        g1.append(row)
    G1_COLUMNS = CONTRACT_COLUMNS + G1_DERIVED_COLUMNS

    if run("P2"):
        emit("")
        hr("P2 - G1: the frozen contract plus derived fields, nothing removed, nothing re-shaped")
        same = all(g1[i][c] == by_metro_c[g1[i]["metro"]][c]
                   for i in range(len(g1)) for c in CONTRACT_COLUMNS)
        gate("P2a", same and len(g1) == 8,
             f"every one of the {len(CONTRACT_COLUMNS)} contract columns survives into G1 "
             f"CELL FOR CELL, as the string the frozen file holds, on all {len(g1)} rows. G1 is "
             f"the contract PLUS fields; Ruling 13 forbids it being anything else")
        gate("P2b", set(G1_COLUMNS) == set(CONTRACT_COLUMNS) | set(G1_DERIVED_COLUMNS)
             and len(G1_COLUMNS) == CONTRACT_WIDTH + len(G1_DERIVED_COLUMNS),
             f"G1 is {len(G1_COLUMNS)} columns: the frozen {CONTRACT_WIDTH} plus exactly the "
             f"{len(G1_DERIVED_COLUMNS)} DECLARED derived fields and no others")
        w, wn = 0.0, ""
        for r in g1:
            d = abs(fnum(r["mitigated_annual_usd"])
                    - (fnum(r["annual_usd"]) + fnum(r["measures_annual_usd"])
                       + fnum(r["storage_annual_usd"])))
            if d > w:
                w, wn = d, r["metro"]
        gate("P2c", w <= CENT,
             f"the contract's own waterfall closes: baseline + measures + storage = mitigated to "
             f"the cent on all eight metros (worst ${w:.6f} on {wn})")
        w2, w2n = 0.0, ""
        for r in g1:
            for a, b in (("usd_per_it_mwh", "annual_usd"),
                         ("mitigated_usd_per_it_mwh", "mitigated_annual_usd")):
                d = abs(fnum(r[a]) * fnum(r["it_annual_mwh"]) - fnum(r[b]))
                if d > w2:
                    w2, w2n = d, f"{r['metro']}/{a}"
        gate("P2d", w2 <= CENT,
             f"$ per IT-MWh x IT-MWh reproduces the annual dollar on both the baseline and the "
             f"mitigated total, every metro (worst ${w2:.6f} on {w2n}) - the ranking metric and "
             f"the dollar are the same number")
        ranks = [int(r["rank"]) for r in g1]
        vals = [fnum(r["mitigated_usd_per_it_mwh"]) for r in g1]
        gate("P2e", ranks == list(range(1, 9)) and vals == sorted(vals),
             f"G1 is written in MITIGATED rank order 1..8 and the metric increases strictly "
             f"({ranks})")
        banded = sorted(r["metro"] for r in g1 if r["band_low_usd_per_mwh"])
        bad_band = []
        for r in g1:
            if not r["band_low_usd_per_mwh"]:
                continue
            mkt = fnum(r["market_pct"]) / 100.0 * fnum(r["annual_usd"])
            half = fnum(r["band_half_width_usd_per_mwh"]) * fnum(r["annual_mwh"])
            if abs(half - MARKET_PRICE_BAND_PCT * mkt) > 1.0:
                bad_band.append(r["metro"])
        gate("P2f", banded == sorted(MARKET_PRICED_METROS) and not bad_band,
             f"the +/-25 % band exists on exactly the three market-priced metros {banded} and "
             f"its half-width IS 25 % of that metro's market component in every one "
             f"({len(bad_band)} mismatch) - the band is a property of the parameter, which is "
             f"why F2Fb-4 makes the cheapest three the least certain three")
        opens = {r["metro"]: r["open_ruling_ids"] for r in g1 if int(r["has_open_ruling"])}
        gate("P2g", opens == OPEN_RULING_METROS,
             f"exactly two metros carry an open ruling and G1 DERIVES the set from the contract's "
             f"open_ruling_ids rather than declaring it: {opens} against {OPEN_RULING_METROS}. "
             f"F4R-12 recorded that Ruling 13's prose said five empty and it is six")
        wb, wbn, wm, wmn, ws, wsn = 0.0, "", 0.0, "", 0.0, ""
        for m in metros:
            r = by_metro_c[m]
            d = abs(base[m]["total_usd"] - fnum(r["annual_usd"]))
            if d > wb:
                wb, wbn = d, m
            mu = sum(v["delta_total_usd"] for v in MEAS.values() if v["metro"] == m)
            d = abs(mu - fnum(r["measures_annual_usd"]))
            if d > wm:
                wm, wmn = d, m
            d = abs(STOR[m]["delta_total_usd"] - fnum(r["storage_annual_usd"]))
            if d > ws:
                ws, wsn = d, m
        bad_strat = [m for m in metros if STOR[m]["strategy"] != by_metro_c[m]["storage_strategy"]]
        gate("P2h", wb <= CENT and wm <= CENT and ws <= 5000.0 and not bad_strat,
             f"THE LIVE CHAIN STILL PRODUCES THE FROZEN CONTRACT on the migrated database: "
             f"baseline worst ${wb:.6f} ({wbn}), measures worst ${wm:.6f} ({wmn}), storage worst "
             f"${ws:,.2f} ({wsn}), and the best storage strategy is re-DERIVED per metro and "
             f"matches the contract on all eight ({len(bad_strat)} mismatch). Phase 5 displays a "
             f"file; this is the gate that the file is still the database's answer")
        exp_port = PORTFOLIO_BASELINE_PRE_RULING_USD + COLUMBUS_RULING8_BASELINE_DELTA_USD
        gate("P2i", close(portfolio_base, exp_port, PORTFOLIO_TOL_USD),
             f"the portfolio baseline summed from G1 is ${portfolio_base:,.2f}, and the figure it "
             f"is checked against is DERIVED - Unit 4E's own pre-ruling literal "
             f"${PORTFOLIO_BASELINE_PRE_RULING_USD:,.2f} plus Unit 4M's measured Columbus delta "
             f"${COLUMBUS_RULING8_BASELINE_DELTA_USD:,.2f} = ${exp_port:,.2f}, agreeing to "
             f"${abs(portfolio_base - exp_port):.2f}. 4E's literal is left where it is; it is the "
             f"pre-ruling record and its own E4e is one of the eleven gates Unit 4R declared must "
             f"fail")
        bad_it = []
        for r in g1:
            if not r["band_low_usd_per_it_mwh"]:
                continue
            lo, hi = fnum(r["band_low_usd_per_it_mwh"]), fnum(r["band_high_usd_per_it_mwh"])
            ctr = fnum(r["usd_per_it_mwh"])
            half_it = (hi - lo) / 2.0
            half_met = fnum(r["band_half_width_usd_per_mwh"])
            expect = half_met * fnum(r["annual_mwh"]) / fnum(r["it_annual_mwh"])
            if not (lo < ctr < hi) or abs(half_it - expect) > 1e-6:
                bad_it.append(r["metro"])
        gate("P2k", not bad_it,
             f"the band carried onto the SITING metric brackets that metro's own $ per IT-MWh "
             f"and is the metered half-width rescaled by the PUE ratio, on all three banded "
             f"metros ({len(bad_it)} wrong). Ruling P5-1's V1 defaults to $ per IT-MWh, so a "
             f"band drawn on the other basis would be a band around a number that is not on the "
             f"chart")
        locs = [(r["metro"], fnum(r["station_latitude"]), fnum(r["station_longitude"]))
                for r in g1]
        okloc = all(l is not None and 24.0 <= l <= 49.0 and -125.0 <= o <= -66.0
                    for _, l, o in locs) and len({(l, o) for _, l, o in locs}) == 8
        gate("P2j", okloc,
             f"all eight map points are read from the metro's OWN EPW LOCATION line - the "
             f"weather station this project's PUE overlay is driven by - are distinct, and fall "
             f"inside the continental United States. The columns are named station_* because "
             f"that is what they are: a station, not a site")

    # ---------------------------------------------------------------------------------------
    # G2 - metro x component. The waterfall, the five channels, and the EXCLUDED band.
    # ---------------------------------------------------------------------------------------
    MEASURE_NAMES = {r["measure_id"]: r["name"]
                     for r in csv.DictReader((project / "era_ph4b_measures.csv").open())}
    g2 = []
    for r in g1:
        m = r["metro"]
        run_usd = fnum(r["annual_usd"])
        itm = fnum(r["it_annual_mwh"])
        g2.append({"metro": m, "kind": "baseline", "component_id": r["schedule_code"],
                   "component_name": MEASURE_NAMES.get(r["schedule_code"], r["schedule_code"]),
                   "usd_per_year": f"{run_usd:.8f}", "usd_per_it_mwh": r["usd_per_it_mwh"],
                   "energy_channel_usd": "", "demand_channel_usd": "", "rider_usd": "",
                   "fixed_usd": "", "statutory_usd": "",
                   "included_in_mitigated_total": 1, "waterfall_order": 0,
                   "waterfall_start_usd": "0", "waterfall_end_usd": f"{run_usd:.8f}",
                   "note": "Unit 4A facility baseline on the selected schedule"})
        k = 1
        for mid in sorted((x for x in MEAS if MEAS[x]["metro"] == m),
                          key=lambda x: MEAS[x]["delta_total_usd"]):
            v = MEAS[mid]
            end = run_usd + v["delta_total_usd"]
            g2.append({"metro": m, "kind": "measure", "component_id": mid,
                       "component_name": MEASURE_NAMES.get(mid, mid),
                       "usd_per_year": f"{v['delta_total_usd']:.8f}",
                       "usd_per_it_mwh": f"{v['delta_usd_per_it_mwh']:.8f}",
                       "energy_channel_usd": f"{v['delta_energy_channel_usd']:.8f}",
                       "demand_channel_usd": f"{v['delta_demand_channel_usd']:.8f}",
                       "rider_usd": f"{v['delta_rider_usd']:.8f}",
                       "fixed_usd": f"{v['delta_fixed_usd']:.8f}",
                       "statutory_usd": f"{v['delta_statutory_usd']:.8f}",
                       "included_in_mitigated_total": 1, "waterfall_order": k,
                       "waterfall_start_usd": f"{run_usd:.8f}",
                       "waterfall_end_usd": f"{end:.8f}", "note": v["note"]})
            run_usd = end
            k += 1
        so = STOR[m]
        end = run_usd + so["delta_total_usd"]
        g2.append({"metro": m, "kind": "storage",
                   "component_id": f"M-ALL-STORAGE/{STORAGE_CONFIG}/{so['strategy']}",
                   "component_name": f"{STORAGE_CONFIG} battery, {so['strategy']} dispatch",
                   "usd_per_year": f"{so['delta_total_usd']:.8f}",
                   "usd_per_it_mwh": f"{so['delta_usd_per_it_mwh']:.8f}",
                   "energy_channel_usd": f"{so['delta_energy_channel_usd']:.8f}",
                   "demand_channel_usd": f"{so['delta_demand_channel_usd']:.8f}",
                   "rider_usd": f"{so['delta_rider_usd']:.8f}",
                   "fixed_usd": f"{so['delta_fixed_usd']:.8f}", "statutory_usd": "0",
                   "included_in_mitigated_total": 1, "waterfall_order": k,
                   "waterfall_start_usd": f"{run_usd:.8f}", "waterfall_end_usd": f"{end:.8f}",
                   "note": f"{so['days']} days dispatched"})
        g2.append({"metro": m, "kind": "mitigated", "component_id": "TOTAL",
                   "component_name": "mitigated total",
                   "usd_per_year": f"{end:.8f}",
                   "usd_per_it_mwh": f"{end / itm:.8f}",
                   "energy_channel_usd": r["mitigation_energy_channel_usd"],
                   "demand_channel_usd": r["mitigation_demand_channel_usd"],
                   "rider_usd": r["mitigation_rider_usd"], "fixed_usd": r["mitigation_fixed_usd"],
                   "statutory_usd": r["mitigation_statutory_usd"],
                   "included_in_mitigated_total": 1, "waterfall_order": k + 1,
                   "waterfall_start_usd": "0", "waterfall_end_usd": f"{end:.8f}",
                   "note": "baseline + measures + storage"})

    # the three voltage siblings: SHOWN, and shown as EXCLUDED. Ruling P5-1's V2 requires the
    # band to be present rather than absent, so the exclusion is a ROW, not a missing row.
    sib_metro = {mid: v[0] for mid, v in D.VOLTAGE_SIBLINGS.items()}
    for mid in sorted(D.VOLTAGE_SIBLINGS):
        usd, itv, _ = D.PUBLISHED_4D[mid]
        mt = sib_metro[mid]
        frm, to = D.VOLTAGE_SIBLINGS[mid][1], D.VOLTAGE_SIBLINGS[mid][2]
        g2.append({"metro": mt, "kind": "excluded", "component_id": mid,
                   "component_name": f"voltage sibling {frm} -> {to}",
                   "usd_per_year": f"{usd:.8f}", "usd_per_it_mwh": f"{itv:.8f}",
                   "energy_channel_usd": "", "demand_channel_usd": "", "rider_usd": "",
                   "fixed_usd": "", "statutory_usd": "",
                   "included_in_mitigated_total": 0, "waterfall_order": 99,
                   "waterfall_start_usd": "", "waterfall_end_usd": "",
                   "note": "BASELINE-SIDE: the published baseline is already billed on the TO "
                           "schedule, so counting this again would double-count it. " +
                           D.CAPEX_CAVEAT})

    if run("P3"):
        emit("")
        hr("P3 - G2: the waterfall closes on G1, and the excluded band is a ROW not a gap")
        n_meas = sum(1 for x in g2 if x["kind"] == "measure")
        gate("P3a", len(g2) == 8 * 3 + n_meas + 3 and n_meas == len(MEAS),
             f"G2 holds {len(g2)} rows: eight baselines, {n_meas} measures, eight storage rows, "
             f"eight mitigated totals and three EXCLUDED voltage siblings")
        bad_chain, wend, wendn = [], 0.0, ""
        for m in metros:
            rows = sorted((x for x in g2 if x["metro"] == m and x["kind"] in
                           ("baseline", "measure", "storage")),
                          key=lambda x: x["waterfall_order"])
            for a, b in zip(rows, rows[1:]):
                if abs(fnum(a["waterfall_end_usd"]) - fnum(b["waterfall_start_usd"])) > CENT:
                    bad_chain.append(f"{m}/{b['component_id']}")
            d = abs(fnum(rows[-1]["waterfall_end_usd"])
                    - fnum(by_metro_c[m]["mitigated_annual_usd"]))
            if d > wend:
                wend, wendn = d, m
        gate("P3b", not bad_chain and wend <= CENT,
             f"the waterfall is CONTIGUOUS in every metro ({len(bad_chain)} break) and its last "
             f"bar lands on G1's mitigated_annual_usd to the cent (worst ${wend:.6f} on "
             f"{wendn}) - a waterfall whose bars do not chain is a picture, not a decomposition")
        wc, wcn = 0.0, ""
        for m in metros:
            r = by_metro_c[m]
            for col, gcol in (("energy_channel_usd", "mitigation_energy_channel_usd"),
                              ("demand_channel_usd", "mitigation_demand_channel_usd"),
                              ("rider_usd", "mitigation_rider_usd"),
                              ("fixed_usd", "mitigation_fixed_usd"),
                              ("statutory_usd", "mitigation_statutory_usd")):
                s = sum(fnum(x[col]) or 0.0 for x in g2
                        if x["metro"] == m and x["kind"] in ("measure", "storage") and x[col])
                d = abs(s - fnum(r[gcol]))
                if d > wc:
                    wc, wcn = d, f"{m}/{col}"
        gate("P3c", wc <= CENT,
             f"G2's five channels sum, per metro, to G1's own five mitigation_* columns to the "
             f"cent (worst ${wc:.6f} on {wcn}). F4E-3's result - the RIDER channel carries the "
             f"mitigation - is therefore a property of the extract, not of a chart")
        ex = [x for x in g2 if x["kind"] == "excluded"]
        ex_usd = sum(fnum(x["usd_per_year"]) for x in ex)
        ex_it = sum(fnum(x["usd_per_it_mwh"]) for x in ex)
        gate("P3d", len(ex) == 3 and close(ex_usd, VOLTAGE_SIBLING_EXCLUSION_USD, 5000.0)
             and close(ex_it, VOLTAGE_SIBLING_EXCLUSION_IT, MWH_TOL)
             and all(int(x["included_in_mitigated_total"]) == 0 for x in ex)
             and all(D.CAPEX_CAVEAT in x["note"] for x in ex),
             f"the three voltage siblings are PRESENT and flagged excluded, at "
             f"${-ex_usd:,.0f}/yr = {-ex_it:.4f} $ per IT-MWh against the declared "
             f"${-VOLTAGE_SIBLING_EXCLUSION_USD:,.0f} - 2.7x the entire real stack - and every "
             f"one of them carries Unit 4D's capex caveat string, imported not retyped")
        gate("P3e", all(x["waterfall_start_usd"] == "" for x in ex),
             f"no excluded row sits inside a metro's waterfall chain: the band is drawn beside "
             f"the bars, never in them (Ruling P5-1's V2)")
        wbb, wbbn = 0.0, ""
        for m in metros:
            b = next(x for x in g2 if x["metro"] == m and x["kind"] == "baseline")
            d = abs(fnum(b["usd_per_year"]) - fnum(by_metro_c[m]["annual_usd"]))
            if d > wbb:
                wbb, wbbn = d, m
        gate("P3f", wbb <= CENT,
             f"G2's baseline bar is G1's annual_usd to the cent on every metro (worst "
             f"${wbb:.6f} on {wbbn})")

    # ---------------------------------------------------------------------------------------
    # G3 - metro x month x stage. The only thing in Phase 5 that is genuinely re-derived.
    # ---------------------------------------------------------------------------------------
    g3 = []
    for m in metros:
        r = by_metro_c[m]
        so = STOR[m]
        mids = [x for x in MEAS if MEAS[x]["metro"] == m]
        for mth in range(1, 13):
            bd = base_m[m]["determinants"][mth]
            bm = base_m[m]["monthly"][mth]
            sd = so["m_on"]["determinants"][mth]
            sm = so["m_on"]["monthly"][mth]
            mm = {c: sum(MEAS[x]["monthly"][mth][c] for x in mids)
                  for c in list(M.COMPONENTS) + ["statutory_usd"]}
            stm = {c: sm[c] - bm[c] for c in M.COMPONENTS}
            mit = {c: bm[c] + mm[c] + stm.get(c, 0.0) for c in M.COMPONENTS}
            mit["statutory_usd"] = mm["statutory_usd"]

            def emit_row(stage, vt, comp, det, series, extra=None):
                row = {"metro": m, "month": mth, "month_name": MONTH_NAME[mth], "stage": stage,
                       "value_type": vt, "load_series": series, "pue_basis": FACILITY_TAG}
                tot = 0.0
                for c in ("energy_usd", "market_usd", "demand_usd", "rider_usd", "fixed_usd",
                          "statutory_usd"):
                    v = comp.get(c, 0.0)
                    row[c] = f"{v:.8f}"
                    tot += v
                row["total_usd"] = f"{tot:.8f}"
                for c in ("kwh", "ncp_kw_15min", "ncp_kw_30min", "billed_kw_15min",
                          "billed_kw_30min", "cp4_kw"):
                    row[c] = f"{det[c]:.6f}" if det else ""
                row["ratchet_binding"] = det["ratchet_binding"] if det else ""
                row["storage_discharge_mwh"] = ""
                row["storage_charge_mwh"] = ""
                row["storage_cap_kw"] = ""
                if extra:
                    row.update(extra)
                g3.append(row)

            emit_row("baseline", "level", bm, bd, "baseline")
            emit_row("measures", "delta", mm, None, "baseline")
            cap = so["caps"].get(mth)
            emit_row("storage", "delta", stm, sd, "dispatched",
                     {"storage_discharge_mwh": f"{so['discharge_mwh_by_month'][mth]:.6f}",
                      "storage_charge_mwh": f"{so['charge_mwh_by_month'][mth]:.6f}",
                      "storage_cap_kw": f"{cap:.6f}" if cap is not None else ""})
            emit_row("mitigated", "level", mit, None, "dispatched")

    if run("P4"):
        emit("")
        hr("P4 - G3: the monthly grain, and the tie to G1 to the cent per metro per stage")
        gate("P4a", len(g3) == 8 * 12 * len(G3_STAGES)
             and sorted({x["stage"] for x in g3}) == sorted(G3_STAGES),
             f"G3 is {len(g3)} rows = 8 metros x 12 months x {len(G3_STAGES)} stages "
             f"{sorted(set(x['stage'] for x in g3))}, complete with no gaps")
        ties = {"baseline": "annual_usd", "measures": "measures_annual_usd",
                "storage": "storage_annual_usd", "mitigated": "mitigated_annual_usd"}
        for stage, col in ties.items():
            w, wn = 0.0, ""
            for m in metros:
                s = sum(fnum(x["total_usd"]) for x in g3
                        if x["metro"] == m and x["stage"] == stage)
                d = abs(s - fnum(by_metro_c[m][col]))
                if d > w:
                    w, wn = d, m
            gate({"baseline": "P4b", "measures": "P4c", "storage": "P4d",
                  "mitigated": "P4e"}[stage], w <= CENT,
                 f"G3's '{stage}' stage summed over the twelve months equals G1's {col} TO THE "
                 f"CENT on every metro (worst ${w:.6f} on {wn})")
        wk, wkn = 0.0, ""
        for m in metros:
            s = sum(fnum(x["kwh"]) for x in g3
                    if x["metro"] == m and x["stage"] == "baseline")
            d = abs(s / 1000.0 - fnum(by_metro_c[m]["annual_mwh"]))
            if d > wk:
                wk, wkn = d, m
            g3sum = sum(fnum(x["kwh"]) for x in g3
                        if x["metro"] == m and x["stage"] == "storage")
        gate("P4f", wk <= MWH_TOL,
             f"G3's baseline monthly kWh sums to G1's annual_mwh on every metro (worst "
             f"{wk:.6f} MWh on {wkn}) - the determinant series and the cost series describe the "
             f"same year")
        rb = sorted({x["metro"] for x in g3
                     if x["stage"] == "baseline" and str(x["ratchet_binding"]) == "1"})
        cb = sorted(m for m in metros if int(by_metro_c[m]["ratchet_binding"]))
        gate("P4g", rb == cb,
             f"the months in which a demand ratchet BINDS are derived here and the metro set "
             f"{rb} equals the contract's own ratchet_binding flag {cb} - PREDICTION Q4. G3 is "
             f"what makes the ratchet visible as a season rather than a boolean")
        wd, wdn = 0.0, ""
        for m in metros:
            s = sum(fnum(x["storage_discharge_mwh"]) for x in g3
                    if x["metro"] == m and x["stage"] == "storage"
                    and x["storage_discharge_mwh"])
            d = abs(s - STOR[m]["discharge_mwh"])
            if d > wd:
                wd, wdn = d, m
        gate("P4h", wd <= 1e-3,
             f"G3's monthly discharge sums to the annual discharge of the dispatch that produced "
             f"the storage saving to within 1 kWh (worst {wd * 1000.0:.6f} kWh on {wdn}, against "
             f"annual discharges of thousands of MWh) - the dispatch view and the dollar come "
             f"from ONE dispatch")
        seasonal = []
        for m in metros:
            v = [fnum(x["total_usd"]) for x in g3
                 if x["metro"] == m and x["stage"] == "storage"]
            if max(v) - min(v) < 1.0:
                seasonal.append(m)
        gate("P4i", not seasonal,
             f"VACUITY GUARD on the delta stages: no metro's monthly STORAGE saving is constant "
             f"across the year ({len(seasonal)} constant). A delta allocated pro-rata would tie "
             f"to G1 exactly and say nothing")
        levels = all(x["value_type"] == ("level" if x["stage"] in ("baseline", "mitigated")
                                         else "delta") for x in g3)
        gate("P4j", levels,
             f"every G3 row declares whether it is a LEVEL or a DELTA. The baseline and the "
             f"mitigated total are levels; measures and storage are deltas. Summing the four "
             f"stages of one month is a double count and value_type is what stops a view doing "
             f"it")

    # ---------------------------------------------------------------------------------------
    # G4 - the caveats, as DATA (Ruling P5-3). Every dollar is DERIVED and then reconciled
    # against the published report, so a caveat cannot drift from the document it caveats.
    # ---------------------------------------------------------------------------------------
    ALL = "all"
    ex_rows = [x for x in g2 if x["kind"] == "excluded"]
    ex_usd_d = sum(fnum(x["usd_per_year"]) for x in ex_rows)
    ex_it_d = sum(fnum(x["usd_per_it_mwh"]) for x in ex_rows)
    sib_metros = ";".join(sorted({x["metro"] for x in ex_rows}))
    chi = by_metro_c["Chicago"]
    nva = by_metro_c["Northern Virginia"]
    col = by_metro_c["Columbus"]
    band_metros = ";".join(sorted(MARKET_PRICED_METROS))
    band_half = {r["metro"]: fnum(r["band_half_width_usd_per_mwh"])
                 for r in g1 if r["band_half_width_usd_per_mwh"]}
    col_hi = fnum(by_metro_c["Columbus"]["band_high_usd_per_mwh"])
    chi_ctr = fnum(by_metro_c["Chicago"]["usd_per_mwh"])
    # F5A-4: the band crossing is BASIS-DEPENDENT. era_ph2_report_v1.2.md's 0.97 is on the Phase 2
    # METERED basis; on the published FACILITY basis the same crossing is smaller. Both are
    # derived here, from the two published extracts, and G4 carries both with their bases.
    ph2 = {r["metro"]: r for r in
           csv.DictReader((project / "era_ph2fb_published_v1.1.csv").open(encoding="utf-8"))}
    col_hi_met = fnum(ph2["Columbus"]["band_high_usd_per_mwh"])
    chi_ctr_met = fnum(ph2["Chicago"]["usd_per_mwh"])
    cross_fac = col_hi - chi_ctr
    cross_met = col_hi_met - chi_ctr_met

    G4 = [
        ("C-FERC-H13", 1, "unpriced", "ComEd FERC OATT Attachment H-13 take-or-pay floor",
         "Chicago", 0, None, None, "understates", "Dockets 25-0677/25-0679",
         f"{PH4_REPORT} section 6",
         "A ten-year FERC-jurisdictional Transmission Security Agreement guaranteeing that annual "
         "PJM transmission payments under OATT Attachment H-13 do not fall below what the "
         "submitted load ramp implies, with any shortfall recovered from the customer. It is the "
         "single largest UNPRICED item in this project and it carries no dollar figure here, "
         "which is the point."),
        ("C-CAPEX", 2, "unpriced", "Substation and interconnection capex transfer",
         sib_metros, 0, None, None, "understates", "-", f"{PH4_REPORT} section 8 caveat 1",
         "Every voltage sibling is " + D.CAPEX_CAVEAT + ". It is stated wherever a sibling "
         "appears and it is in no total."),
        ("C-RETAIL-PROXY", 3, "unpriced", "Retail schedules stand proxy for a >100 MW contract",
         ALL, 0, None, None, "unknown", "direction_ph1_tariff_db_v1.0.md",
         "direction_ph1_tariff_db_v1.0.md; semester-plan.md",
         "A giga-scale campus exceeds every published retail schedule in the library. The largest "
         "published schedule is used as a documented proxy for a negotiated large-load contract, "
         "and the negotiated contract is what a real campus would sign."),
        ("C-VOLT-EXCL", 4, "excluded", "Three voltage siblings, priced and deliberately EXCLUDED",
         sib_metros, 1, ex_usd_d, ex_it_d, "would overstate", "-",
         f"{PH4_REPORT} section 4",
         "M-COL-VOLT, M-DFW-VOLT and M-SJ-VOLT are BASELINE-SIDE: the published baseline is "
         "already billed on the higher-voltage schedule. Counting them again would overstate the "
         "mitigation by 2.7x the entire real stack. They are shown as an excluded band, never as "
         "an absence."),
        ("C-PGE-OPT-R", 5, "unavailable", "PG&E Option R is unavailable to a load of this shape",
         "San Jose / Bay Area", 1, 91828409.0, 11.6343, "overstates cost if elected", "Ruling 10",
         f"{PH4_REPORT} section 4",
         "The modelled battery is 8.32 % of the 1,201,596 kW facility peak against an eligibility "
         "floor of 20 %. Priced anyway it is a net LOSS, and the dominant term is the shared "
         "energy uplift rather than the demand structure."),
        ("C-PGE-OPT-S", 6, "unavailable", "PG&E Option S is unavailable to a load of this shape",
         "San Jose / Bay Area", 1, 103339369.0, 13.0927, "overstates cost if elected", "Ruling 10",
         f"{PH4_REPORT} section 4",
         "Against a 10 % floor, and Option S's smallest qualifying system is 2.403x the entire "
         "50 MW B-20 programme cap - unreachable by construction, and barred on day one at a new "
         "location by the sheet's own words."),
        ("C-F4C-7", 7, "open_ruling", "ComEd Rate BESH's determinants are UNRULED (Chicago pair)",
         "Chicago", 1, -7934035.0, None, "either", "Ruling 17", f"{PH4_REPORT} section 5",
         "Three Rate BESH rows carry determinant_is_assumption = 1. The tariff reading is "
         "probably right, but adopting it means ratifying a five-hour coincident-peak expected "
         "value, which is a work unit. Chicago publishes as a PAIR until it lands."),
        ("C-F4B-2", 8, "open_ruling", "Dominion GS-4's ratchet is UNRULED (Northern Virginia pair)",
         "Northern Virginia", 1, 7901881.12, None, "either", "Ruling 16",
         f"{PH4_REPORT} section 5",
         "GS-4 puts one 100 % ratchet on one distribution demand charge and the schema folds that "
         "charge into two TOU rows. NEITHER priced end is believed to be the tariff's answer; the "
         "tariff's own reading is a third construction nobody has priced."),
        ("C-CHI-5CP", 9, "limitation", "Chicago's PJM coincident-peak window is DECLARED and UNRATIFIED",
         "Chicago", 0, None, None, "unknown", "Ruling 17", f"{PH4_REPORT} section 8 caveat 2",
         "June-September, 15:00-19:00 prevailing clock, weekdays, mirroring the ratified ERCOT "
         "4CP construction. It is the alternative end of the Chicago bracket and the strategy "
         "that end dispatches against."),
        ("C-PUE-BIAS", 10, "limitation", "The PUE overlay OVERSTATES PUE at the hottest intervals",
         ALL, 0, None, None, "upper bound", "Ruling 14", f"{PH4_REPORT} section 8 caveat 6",
         "Above the 25.556 C design wet bulb the economiser is fully out and the only remaining "
         "channel is the chiller's own 1.5 %/F - a marginal slope of 0.00198 PUE/C against the "
         "chord's 0.00471. The bias is up to 0.0184 at Phoenix, 0.0171 at Austin and 0.0122 at "
         "Dallas-Fort Worth, and that interval sets the demand charge in five of eight metros. "
         "Every figure is an UPPER bound in that channel; the two-segment form is scheduled and "
         "cannot change the order."),
        ("C-ALPHA-DOMAIN", 11, "limitation", "The alpha elasticity domain was silently narrowed",
         ALL, 0, None, None, "record", "Ruling 15", f"{PH4_REPORT} section 8 caveat 7",
         "Unit 2F published 4.947 at its own reporting level L = 1.20; at the ruled L = 1.150 the "
         "same construction gives 4.7405, which Unit 4A's gate has been enforcing. The operative "
         "alpha is 2.8311."),
        ("C-BAND-25", 12, "limitation", "The +/-25 % market bands, and the one adjacency they touch",
         band_metros, 0, None, None, "either", "F2Fb-2 / F2Fb-4",
         f"{PH2_REPORT} section 4",
         f"The three CHEAPEST metros are exactly the three banded ones, so the top of the "
         f"ranking is its least certain part. Columbus's upper edge crosses Chicago's central, "
         f"and that pair is the ONLY adjacency the bands touch anywhere in the table. THE SIZE "
         f"OF THE CROSSING DEPENDS ON THE BASIS: {cross_met:.4f} $/MWh on the Phase 2 METERED "
         f"basis, which is the {cross_met:.2f} era_ph2_report_v1.2.md publishes, against "
         f"{cross_fac:.4f} $/MWh on the PUBLISHED FACILITY basis these extracts are on. A view "
         f"built on G1 must quote the facility figure. Both parameters now come from one table "
         f"and one statistic, so moving them independently is not a scenario that can happen."),
        ("C-F4D-8", 13, "limitation", "Atlanta and Phoenix are a LIBRARY GAP, not a tariff finding",
         "Atlanta;Phoenix", 0, None, None, "understates mitigation", "Ruling 19",
         f"{PH4_REPORT} section 4",
         "Georgia Power's and APS's tariff books have not been read for electives with the "
         "thoroughness ComEd's and Dominion's have. That is a statement about this project's "
         "reading, not about those tariffs. It cannot move the order."),
        ("C-F4M-13", 14, "limitation", "PG&E Peak Day Pricing is absent from the library",
         "San Jose / Bay Area", 0, None, None, "either", "Ruling 11",
         f"{PH4_REPORT} section 4",
         "Worth $32.48/kW-yr of summer demand credit against a $0.90/kWh event charge. It is the "
         "ONLY elective in the library that is a RISK TRADE and could go the wrong way for an "
         "uncurtailable load."),
        ("C-F4M-3", 15, "limitation", "Dallas-Fort Worth's parameter deserves less confidence",
         "Dallas-Fort Worth", 1, None, 0.885680, "either", "Ruling 9",
         f"{PH4_REPORT} section 8 caveat 8",
         "ERCOT North's implied load-weighting premium is +0.198 % against a PJM minimum of "
         "+5.72 %. Either the corroborating annual figure is itself load-weighted - in which case "
         "parity is already broken inside DFW's own source - or ERCOT North's 2025 duration curve "
         "really was that flat. Re-targeting to $35.34/MWh was priced and declined."),
        ("C-SJ-PF", 16, "limitation", "M-SJ-PF is a CORRECTION, not an election",
         "San Jose / Bay Area", 1, -6422042.34, -0.813647, "corrects an overstatement", "F4D-6",
         f"{PH4_REPORT} section 8 caveat 4",
         "San Jose reads 0.70 $/metered-MWh high because the engine does not evaluate a mechanic "
         "the database holds. It is in the mitigated stack on that footing, not as a tariff "
         "election the customer chooses."),
        ("C-OHIO-EXCISE", 17, "limitation", "The recorded Ohio kWh excise figure was wrong by 1.95x",
         "Columbus", 1, -16187651.92, -2.050910, "corrected", "F4D-1",
         f"{PH4_REPORT} section 8 caveat 5",
         "The published stack carries the DERIVED value, not the recorded estimate. An estimate "
         "flagged as one is a debt, and it came due."),
        ("C-EXCISE-ALLOC", 18, "limitation",
         "The Ohio statutory liability has no monthly form and G3 ALLOCATES it",
         "Columbus", 1, sa, None, "allocation", "Unit 5A",
         "era_ph5_dictionary_v1.0.md",
         "ORC 5727.81(C) is an ANNUAL self-assessment with an annual 500 GWh tier breakpoint and "
         "an annual per-location fee. G3 spreads it across the twelve months on the month's share "
         "of metered kWh. The annual total is exact; the monthly split is a DECLARED ALLOCATION "
         "and the only one in the four grains."),
        ("C-STATION-POINT", 19, "limitation", "The map point is a weather STATION, not a site",
         ALL, 0, None, None, "presentation", "Unit 5A", "era_ph5_dictionary_v1.0.md",
         "G1's station_latitude and station_longitude are read from the metro's own EPW LOCATION "
         "line - the station this project's PUE overlay is driven by. No site has been chosen in "
         "any metro and the columns are named so that they cannot be read as one."),
        ("C-F4C-8", 20, "discharged", "The PG&E instrument question is DISCHARGED on eligibility",
         "San Jose / Bay Area", 1, None, None, "closed", "Ruling 10",
         f"{PH4_REPORT} section 8 caveat 3",
         "Closed on eligibility rather than on value: the advertised storage tariff does not "
         "reach a load this size. That is a siting finding, not a gap."),
        ("C-F4B-3", 21, "discharged", "DCT-T's inert ratchet is DISCHARGED on measurement",
         "Columbus", 1, 0.0, 0.0, "closed", "Ruling 12", f"{PH4_REPORT} section 5",
         "$0.00 measured four times. DCT-T's 85 % capacity floor is 1,040,584 kW against a lowest "
         "monthly 30-minute peak of 1,140,126 kW - 99,542 kW of headroom - and the floor is "
         "anchored on a CONTRACT, so shaving the peak does not move it."),
    ]

    g4 = []
    for (cid, rank, cat, title, scope, priced, usd, itv, direction, ruling, src, stmt) in G4:
        g4.append({"caveat_id": cid, "sort_rank": rank, "category": cat, "title": title,
                   "metro_scope": scope, "priced": priced,
                   "usd_per_year": ("" if usd is None else f"{usd:.2f}"),
                   "usd_per_it_mwh": ("" if itv is None else f"{itv:.6f}"),
                   "direction": direction, "ruling_ref": ruling, "source_ref": src,
                   "statement": stmt})

    if run("P5"):
        emit("")
        hr("P5 - G4: the caveats as DATA, reconciled against the documents they caveat")
        gate("P5a", len(g4) == len(G4) and len({x["caveat_id"] for x in g4}) == len(g4),
             f"G4 holds {len(g4)} rows with distinct ids, covering every item Ruling P5-3's "
             f"minimum membership names plus the two caveats Unit 5A itself produced "
             f"(C-EXCISE-ALLOC, C-STATION-POINT)")
        both = report_text + "\n" + ph2_text
        miss = []
        for x in g4:
            for c in ("usd_per_year", "usd_per_it_mwh"):
                if not x[c]:
                    continue
                v = float(x[c])
                if v == 0.0:
                    continue
                if not (money_strings(v) & set(re.findall(r"[0-9][0-9,\.]*", both))):
                    miss.append(f"{x['caveat_id']}/{c}={v}")
        gate("P5b", not miss,
             f"EVERY dollar figure in G4 is found, in one of this project's own renderings, in "
             f"{PH4_REPORT} or {PH2_REPORT} ({len(miss)} unreconciled: {miss[:3]}). A typed "
             f"caveat drifts from the report; a reconciled one cannot")
        ferc = next(x for x in g4 if x["caveat_id"] == "C-FERC-H13")
        unp = [x for x in g4 if x["category"] == "unpriced"]
        gate("P5c", int(ferc["sort_rank"]) == 1 and ferc["usd_per_year"] == ""
             and int(ferc["priced"]) == 0
             and all(x["usd_per_year"] == "" and int(x["priced"]) == 0 for x in unp),
             f"the FERC Attachment H-13 floor sits FIRST with no dollar figure, and all "
             f"{len(unp)} unpriced rows carry priced = 0 and an empty usd_per_year. The largest "
             f"number in this project is the one that is not there")
        order_ok = [x["sort_rank"] for x in g4] == sorted(x["sort_rank"] for x in g4)
        cats = [x["category"] for x in sorted(g4, key=lambda y: y["sort_rank"])]
        first_lim = cats.index("limitation") if "limitation" in cats else 10 ** 6
        last_unp = max(i for i, c in enumerate(cats) if c == "unpriced")
        gate("P5d", order_ok and last_unp < first_lim,
             f"G4 is written in sort_rank order and every UNPRICED row outranks every stated "
             f"LIMITATION (last unpriced at {last_unp}, first limitation at {first_lim}) - "
             f"Ruling P5-3's ordering, carried as data rather than as a sort the workbook has to "
             f"remember")
        g4_open = {x["metro_scope"]: x["ruling_ref"] for x in g4
                   if x["category"] == "open_ruling"}
        g1_open = {r["metro"]: r["open_ruling_ids"] for r in g1 if int(r["has_open_ruling"])}
        ids_ok = ({x["caveat_id"][2:] for x in g4
                   if x["category"] == "open_ruling"} == set(g1_open.values()))
        gate("P5e", set(g4_open) == set(g1_open) and ids_ok,
             f"G4's open_ruling rows are exactly the metros G1's own open_ruling_ids names "
             f"{sorted(g1_open)}, and the ids match. The caveats sheet and the ranking cannot "
             f"disagree about what is still open")
        gate("P5f", cross_fac > 0 and cross_met > 0 and abs(cross_met - cross_fac) > 0.1
             and f"{cross_met:.2f}" in ph2_text
             and sorted(band_half) == sorted(MARKET_PRICED_METROS),
             f"F5A-4: THE BAND CROSSING IS BASIS-DEPENDENT AND BOTH FIGURES ARE DERIVED HERE. On "
             f"the Phase 2 METERED basis Columbus's upper edge {col_hi_met:.4f} crosses Chicago's "
             f"central {chi_ctr_met:.4f} by {cross_met:.4f}, which rounds to the "
             f"{cross_met:.2f} era_ph2_report_v1.2.md publishes and is found in it. On the "
             f"PUBLISHED FACILITY basis the same crossing is {col_hi:.4f} against "
             f"{chi_ctr:.4f} = {cross_fac:.4f} - smaller by {cross_met - cross_fac:.4f}. Neither "
             f"is wrong and the two are {abs(cross_met - cross_fac):.4f} apart, so a Phase 5 view "
             f"drawn on G1 that quoted the published 0.97 would be quoting the other basis's "
             f"number. The banded set is G1's own, not a list")
        vx = next(x for x in g4 if x["caveat_id"] == "C-VOLT-EXCL")
        gate("P5g", close(float(vx["usd_per_year"]), ex_usd_d, CENT)
             and close(float(vx["usd_per_year"]), VOLTAGE_SIBLING_EXCLUSION_USD, 5000.0),
             f"the excluded-band caveat's dollars are SUMMED FROM G2's own excluded rows "
             f"(${-ex_usd_d:,.2f}) and agree with the declared "
             f"${-VOLTAGE_SIBLING_EXCLUSION_USD:,.2f}. The declaration and the derivation are "
             f"independent quantities here - a tamper that bends one is caught by the other")
        toks = {t for x in g4 for t in x["metro_scope"].split(";")}
        gate("P5h", toks <= set(metros) | {ALL},
             f"every metro_scope token in G4 is a G1 metro or '{ALL}' ({sorted(toks - set(metros) - {ALL})} "
             f"unknown) - a caveat scoped to a metro that is not in the ranking is a caveat "
             f"nothing can filter")

    # ---------------------------------------------------------------------------------------
    # The data dictionary and the style tokens
    # ---------------------------------------------------------------------------------------
    CONTRACT_DOC = {
        "rank": ("ordinal", "mitigated $ per IT-MWh, ascending"),
        "metro": ("text", "the eight study metros; the join key of every grain"),
        "utility": ("text", "utility.utility_name in era_rates.db"),
        "schedule_code": ("text", "the schedule the metro is billed on"),
        "voltage_level": ("text", "transmission / primary / - (Atlanta's is missing, Phase 6)"),
        "rider_coverage": ("text", "itemised or verified_aggregate"),
        "usd_per_mwh": ("USD/metered-MWh", "baseline bill over metered energy"),
        "band_low_usd_per_mwh": ("USD/metered-MWh", "baseline less 25 % of the market component"),
        "band_high_usd_per_mwh": ("USD/metered-MWh", "baseline plus 25 % of the market component"),
        "annual_usd": ("USD/year", "the baseline bill"),
        "annual_mwh": ("MWh/year", "METERED energy, facility side of the PUE overlay"),
        "market_pct": ("%", "market-priced energy share of the baseline bill"),
        "demand_pct": ("%", "demand share"),
        "rider_pct": ("%", "rider share"),
        "energy_pct": ("%", "tariff energy share"),
        "fixed_pct": ("%", "fixed share"),
        "ratchet_binding": ("0/1", "a demand ratchet binds in at least one month"),
        "pue_basis": ("text", "plant_derived_4a; the Unit 4A facility overlay"),
        "pue_level_L": ("ratio", "the ruled reporting level, 1.150"),
        "pue_alpha": ("dimensionless", "the ruled elasticity, 2.8311"),
        "usd_per_it_mwh": ("USD/IT-MWh", "THE SITING METRIC: sites compared at equal IT capacity"),
        "it_annual_mwh": ("MWh/year", "IT energy delivered; identical across metros by construction"),
        "mean_pue_energy_weighted": ("ratio", "metered over IT energy"),
        "facility_peak_kw": ("kW", "facility peak, the contract-capacity anchor"),
        "measure_ids": ("text;", "the metro's tariff electives, semicolon delimited"),
        "measures_annual_usd": ("USD/year", "sum of the metro's elective deltas, negative = saving"),
        "measures_usd_per_it_mwh": ("USD/IT-MWh", "the same on the siting metric"),
        "storage_config": ("text", "B100-4H: 100 MW / 400 MWh"),
        "storage_strategy": ("text", "the dispatch target, DERIVED per metro by re-dispatch"),
        "storage_annual_usd": ("USD/year", "the storage delta, negative = saving"),
        "storage_usd_per_it_mwh": ("USD/IT-MWh", "the same on the siting metric"),
        "mitigated_pre_storage_usd_per_it_mwh": ("USD/IT-MWh", "baseline plus electives only"),
        "mitigated_annual_usd": ("USD/year", "baseline + measures + storage"),
        "mitigated_usd_per_it_mwh": ("USD/IT-MWh", "the ranking metric"),
        "mitigation_energy_channel_usd": ("USD/year", "F4A-1 energy channel of the mitigation"),
        "mitigation_demand_channel_usd": ("USD/year", "F4A-1 demand channel of the mitigation"),
        "mitigation_rider_usd": ("USD/year", "rider channel; F4E-3 says this one carries it"),
        "mitigation_fixed_usd": ("USD/year", "fixed channel"),
        "mitigation_statutory_usd": ("USD/year", "ORC 5727.81, paid to the state, not a tariff"),
        "mitigation_pct_of_baseline": ("%", "mitigation over baseline"),
        "bracket_reading": ("text", "the determinant reading the alternative end swaps in"),
        "bracket_baseline_move_usd": ("USD/year", "what the alternative reading moves the baseline"),
        "bracket_alt_storage_strategy": ("text", "best strategy RE-DERIVED at the alternative end"),
        "mitigated_alt_usd_per_it_mwh": ("USD/IT-MWh", "the alternative end; blank = no bracket"),
        "mitigated_alt_annual_usd": ("USD/year", "the alternative end in dollars"),
        "capex_caveat": ("text", "the unpriced capex transfer, where a sibling is involved"),
        "unpriced_caveat": ("text", "F4D-8's library gap, where it applies"),
        "market_node_class": ("text", "zone or hub, per Ruling 8; carries F4M-4 downstream"),
        "market_construction": ("text", "da_zone_simple: the ratified construction, as a field"),
        "pue_form": ("text", "linear_4a today; two_segment_ph6 after Ruling 14 executes"),
        "pue_alpha_domain_max": ("dimensionless", "4.7405 at L = 1.150, per Ruling 15"),
        "open_ruling_ids": ("text;", "rulings still capable of moving this row"),
    }
    DERIVED_DOC = {
        "metro_key": ("text", "era_engine.METRO_WEATHER_KEY", "derived"),
        "state": ("text", "the metro's EPW LOCATION line, field 3", "derived"),
        "station_name": ("text", "the metro's EPW LOCATION line, field 2", "derived"),
        "station_latitude": ("degrees", "the metro's EPW LOCATION line, field 7. A WEATHER "
                             "STATION, not a site: no site has been chosen", "derived"),
        "station_longitude": ("degrees", "the metro's EPW LOCATION line, field 8. Station, not "
                              "site", "derived"),
        "rank_baseline": ("ordinal", "rank on usd_per_it_mwh, ascending", "derived"),
        "is_market_priced": ("0/1", "market_pct > 0", "derived"),
        "band_half_width_usd_per_mwh": ("USD/metered-MWh", "(band_high - band_low) / 2", "derived"),
        "band_low_usd_per_it_mwh": ("USD/IT-MWh", "the band on the SITING metric", "derived"),
        "band_high_usd_per_it_mwh": ("USD/IT-MWh", "the band on the SITING metric", "derived"),
        "mitigation_usd_per_it_mwh": ("USD/IT-MWh", "measures + storage", "derived"),
        "mitigation_annual_usd": ("USD/year", "measures + storage", "derived"),
        "measure_count": ("count", "len(measure_ids)", "derived"),
        "has_bracket": ("0/1", "mitigated_alt_usd_per_it_mwh is populated", "derived"),
        "bracket_low_usd_per_it_mwh": ("USD/IT-MWh", "min of the two ends; = mitigated when no "
                                       "bracket, so V5 can draw an interval on every metro",
                                       "derived"),
        "bracket_high_usd_per_it_mwh": ("USD/IT-MWh", "max of the two ends", "derived"),
        "bracket_width_usd_per_it_mwh": ("USD/IT-MWh", "the bracket's own size", "derived"),
        "has_open_ruling": ("0/1", "open_ruling_ids is non-empty", "derived"),
        "open_ruling_count": ("count", "tokens in open_ruling_ids", "derived"),
        "gap_to_next_usd_per_it_mwh": ("USD/IT-MWh", "adjacency to the next-ranked metro; blank "
                                       "on rank 8", "derived"),
        "pct_of_portfolio_baseline": ("%", "this metro's share of the eight-metro baseline",
                                      "derived"),
    }
    G2_DOC = {
        "metro": ("text", "join key to G1, G3 and G4's metro_scope"),
        "kind": ("text", "baseline|measure|storage|mitigated|excluded"),
        "component_id": ("text", "schedule code, measure id, or storage config/strategy"),
        "component_name": ("text", "the component's published name"),
        "usd_per_year": ("USD/year", "level for baseline and mitigated, DELTA for the others"),
        "usd_per_it_mwh": ("USD/IT-MWh", "the same quantity on the siting metric"),
        "energy_channel_usd": ("USD/year", "F4A-1 energy channel; blank where not decomposed"),
        "demand_channel_usd": ("USD/year", "F4A-1 demand channel"),
        "rider_usd": ("USD/year", "rider channel"), "fixed_usd": ("USD/year", "fixed channel"),
        "statutory_usd": ("USD/year", "ORC 5727.81; not a tariff quantity"),
        "included_in_mitigated_total": ("0/1", "0 on the three EXCLUDED voltage siblings"),
        "waterfall_order": ("ordinal", "0 baseline, then measures, then storage; 99 = excluded"),
        "waterfall_start_usd": ("USD/year", "running total before this bar; blank when excluded"),
        "waterfall_end_usd": ("USD/year", "running total after this bar"),
        "note": ("text", "the component's own published note"),
    }
    G3_DOC = {
        "metro": ("text", "join key to G1, G2 and G4's metro_scope"),
        "month": ("1-12", "calendar month of the study year"),
        "month_name": ("text", "abbreviated month label"),
        "stage": ("text", "baseline|measures|storage|mitigated"),
        "value_type": ("text", "level or delta. SUMMING ALL FOUR STAGES DOUBLE-COUNTS"),
        "load_series": ("text", "baseline or dispatched: which meter series the row describes"),
        "energy_usd": ("USD/month", "tariff energy"), "market_usd": ("USD/month", "market energy"),
        "demand_usd": ("USD/month", "TOU and flat demand"),
        "rider_usd": ("USD/month", "riders on their own declared determinants"),
        "fixed_usd": ("USD/month", "USD_per_month billed monthly; USD_per_day by calendar days"),
        "statutory_usd": ("USD/month", "ORC 5727.81, DECLARED ALLOCATION on the month's kWh "
                          "share - the only allocation in the four grains (C-EXCISE-ALLOC)"),
        "total_usd": ("USD/month", "the six components, summed"),
        "kwh": ("kWh", "metered energy in the month"),
        "ncp_kw_15min": ("kW", "actual 15-minute monthly peak"),
        "ncp_kw_30min": ("kW", "actual 30-minute monthly peak"),
        "billed_kw_15min": ("kW", "after any ratchet floor"),
        "billed_kw_30min": ("kW", "after any ratchet floor"),
        "cp4_kw": ("kW", "the coincident-peak determinant; annual, repeated on each month"),
        "ratchet_binding": ("0/1", "the ratchet floor exceeded the actual peak in this month"),
        "storage_discharge_mwh": ("MWh", "storage stage only"),
        "storage_charge_mwh": ("MWh", "storage stage only; includes the round-trip buy-back"),
        "storage_cap_kw": ("kW", "the month's binding dispatch cap"),
        "pue_basis": ("text", "plant_derived_4a on every row"),
    }
    G4_DOC = {
        "caveat_id": ("text", "stable id; cited by the workbook, never by row number"),
        "sort_rank": ("ordinal", "unpriced first, then excluded, open rulings, limitations, "
                      "discharged"),
        "category": ("text", "unpriced|excluded|unavailable|open_ruling|limitation|discharged"),
        "title": ("text", "one line, as the report states it"),
        "metro_scope": ("text;", "semicolon-delimited metros, or 'all'"),
        "priced": ("0/1", "whether a dollar figure exists at all"),
        "usd_per_year": ("USD/year", "blank where UNPRICED; reconciled against the reports"),
        "usd_per_it_mwh": ("USD/IT-MWh", "blank where unpriced or not a per-energy quantity"),
        "direction": ("text", "which way the omission or bias moves the published figure"),
        "ruling_ref": ("text", "the ruling or finding that governs it"),
        "source_ref": ("text", "the document and section it reconciles against"),
        "statement": ("text", "the caveat itself, in the report's own terms"),
    }

    # --- the style tokens.  ONE accent hue; every token is a tint, tone or shade of it, and the
    # gate RECOMPUTES the hue from the hex rather than trusting the name (Ruling P5-4).
    ACCENT_HUE = 210.0
    HUE_TOL_DEG = 4.0
    MIN_RECOVERABLE_CHROMA = 8      # 8-bit channel spread below which a hue is not recoverable
    TOKENS = [
        ("--era-surface", 0.00, 1.000, "page and sheet background: stark white"),
        ("--era-surface-alt", 0.40, 0.955, "banded row / panel fill, barely off white"),
        ("--era-grid", 0.35, 0.930, "gridlines, where a gridline is unavoidable"),
        ("--era-rule", 0.30, 0.845, "hairline rules and axis lines"),
        ("--era-muted", 0.18, 0.600, "secondary labels, footnotes, EXCLUDED and UNPRICED marks"),
        ("--era-accent-100", 0.52, 0.880, "lightest ramp step: smallest magnitude"),
        ("--era-accent-200", 0.52, 0.760, "ramp step 2"),
        ("--era-accent-300", 0.52, 0.640, "ramp step 3"),
        ("--era-accent-400", 0.52, 0.520, "ramp step 4: the primary accent"),
        ("--era-accent-500", 0.52, 0.420, "ramp step 5"),
        ("--era-accent-600", 0.52, 0.320, "ramp step 6"),
        ("--era-accent-700", 0.52, 0.220, "darkest ramp step: largest magnitude"),
        ("--era-ink", 0.35, 0.100, "primary type"),
    ]
    TYPE_SCALE = [("caption", 11), ("body", 13), ("label", 16), ("subhead", 22), ("title", 34)]
    TYPE_FAMILY = ("Helvetica Neue", "Helvetica", "Arial", "sans-serif")
    GRID_BASE_PX = 8
    MARGIN_PX = 48
    GUTTER_PX = 24

    def hsl_hex(h, s, l):
        c = (1 - abs(2 * l - 1)) * s
        x = c * (1 - abs(((h / 60.0) % 2) - 1))
        m = l - c / 2
        r, g, b = {0: (c, x, 0), 1: (x, c, 0), 2: (0, c, x),
                   3: (0, x, c), 4: (x, 0, c), 5: (c, 0, x)}[int(h // 60) % 6]
        return "#" + "".join(f"{int(round((v + m) * 255)):02X}" for v in (r, g, b))

    def hex_hue(hx):
        r, g, b = (int(hx[i:i + 2], 16) / 255.0 for i in (1, 3, 5))
        mx, mn = max(r, g, b), min(r, g, b)
        if abs(mx - mn) < 1e-9:
            return None
        if mx == r:
            h = 60 * (((g - b) / (mx - mn)) % 6)
        elif mx == g:
            h = 60 * (((b - r) / (mx - mn)) + 2)
        else:
            h = 60 * (((r - g) / (mx - mn)) + 4)
        return h

    STYLE_TOKENS = [(n, hsl_hex(ACCENT_HUE, s, l), s, l, note) for n, s, l, note in TOKENS]

    if run("P6"):
        emit("")
        hr("P6 - the dictionary covers every column both ways; the style tokens are ONE hue")
        grains = {"G1": G1_COLUMNS, "G2": G2_COLUMNS, "G3": G3_COLUMNS, "G4": G4_COLUMNS}
        docs = {"G1": set(CONTRACT_DOC) | set(DERIVED_DOC), "G2": set(G2_DOC),
                "G3": set(G3_DOC), "G4": set(G4_DOC)}
        undoc, orphan = [], []
        for g, cols in grains.items():
            undoc += [f"{g}.{c}" for c in cols if c not in docs[g]]
            orphan += [f"{g}.{c}" for c in docs[g] if c not in cols]
        gate("P6a", not undoc and not orphan,
             f"the data dictionary covers every column of all four grains and documents nothing "
             f"that does not exist: {len(undoc)} undocumented {undoc[:4]}, {len(orphan)} orphan "
             f"{orphan[:4]}. Both directions, because a dictionary with a stale entry is how a "
             f"workbook gets bound to a column that was renamed")
        thin = [k for k, v in list(CONTRACT_DOC.items()) + list(G2_DOC.items())
                + list(G3_DOC.items()) + list(G4_DOC.items()) if not v[0] or len(v[1]) < 10]
        thin += [k for k, v in DERIVED_DOC.items() if not v[0] or len(v[1]) < 10]
        gate("P6b", not thin,
             f"every dictionary entry states a UNIT and a provenance of more than ten characters "
             f"({len(thin)} thin: {thin[:4]})")
        def chroma(hx):
            ch = [int(hx[i:i + 2], 16) for i in (1, 3, 5)]
            return max(ch) - min(ch)

        nonwhite = [(n, hx) for n, hx, *_ in STYLE_TOKENS if hx != "#FFFFFF"]
        thin_c = [n for n, hx in nonwhite if chroma(hx) < MIN_RECOVERABLE_CHROMA]
        off = [(n, hex_hue(hx)) for n, hx in nonwhite
               if hex_hue(hx) is None or abs(hex_hue(hx) - ACCENT_HUE) > HUE_TOL_DEG]
        worst_h = max(abs(hex_hue(hx) - ACCENT_HUE) for _, hx in nonwhite)
        gate("P6c", STYLE_TOKENS[0][1] == "#FFFFFF" and not off and not thin_c
             and len(STYLE_TOKENS) == len(TOKENS),
             f"the surface is stark #FFFFFF and every one of the other {len(nonwhite)} tokens "
             f"carries enough chroma for a hue to be RECOVERABLE from its 8-bit hex "
             f"({len(thin_c)} below {MIN_RECOVERABLE_CHROMA} levels) and recomputes to the single "
             f"accent hue {ACCENT_HUE:.0f} deg within {HUE_TOL_DEG:.0f} deg (worst "
             f"{worst_h:.2f} deg, which is 8-bit quantisation of a low-chroma tone and not a "
             f"second hue). The gate recomputes the hue rather than trusting the token's name, "
             f"and the near-neutrals are given chroma deliberately so that they CAN be checked "
             f"rather than exempted")
        ls = [l for _, _, _, l, _ in STYLE_TOKENS]
        gate("P6d", len(set(ls)) == len(ls) and len(TYPE_SCALE) == 5
             and len(TYPE_FAMILY) >= 2 and GRID_BASE_PX == 8,
             f"every token is a DISTINCT lightness ({len(set(ls))} of {len(ls)}), the type scale "
             f"is {len(TYPE_SCALE)} sizes on one sans-serif family, and the grid is "
             f"{GRID_BASE_PX} px with {MARGIN_PX} px margins and {GUTTER_PX} px gutters")
        div = [t for t in STYLE_TOKENS if "accent" in t[0]]
        gate("P6e", hex_hue(div[0][1]) == hex_hue(div[-1][1]) and len(div) == 7,
             f"a DIVERGING measure uses the two ends of this one {len(div)}-step ramp "
             f"({div[0][1]} to {div[-1][1]}), never two hues - saving and cost are one quantity "
             f"with a sign, and two hues would say they are two quantities")

    if run("P7"):
        emit("")
        hr("P7 - the four grains agree with each other")
        w, wn = 0.0, ""
        for m in metros:
            for stage, kind in (("measures", "measure"), ("storage", "storage")):
                a = sum(fnum(x["total_usd"]) for x in g3
                        if x["metro"] == m and x["stage"] == stage)
                b = sum(fnum(x["usd_per_year"]) for x in g2
                        if x["metro"] == m and x["kind"] == kind)
                d = abs(a - b)
                if d > w:
                    w, wn = d, f"{m}/{stage}"
        gate("P7a", w <= CENT,
             f"G2 and G3 agree, per metro per stage, to the cent (worst ${w:.6f} on {wn}) - the "
             f"waterfall and the seasonality are two views of ONE decomposition")
        sets_ok = ({r["metro"] for r in g1} == {x["metro"] for x in g2}
                   == {x["metro"] for x in g3} == set(metros))
        gate("P7b", sets_ok,
             f"G1, G2 and G3 carry the identical eight-metro set and it is the database's set, "
             f"not a list")
        n_unpriced = sum(1 for x in g4 if int(x["priced"]) == 0)
        gate("P7c", n_unpriced > PH4_REPORT_CAVEAT_COUNT - 4,
             f"PREDICTION Q6: G4 carries {n_unpriced} rows with no dollar figure against "
             f"{PH4_REPORT_CAVEAT_COUNT} numbered caveats in the report. G4 is a caveat list PLUS "
             f"the unpriced items PLUS the open rulings, which is why Ruling P5-3 makes it a "
             f"grain and not a text box")

    # ---------------------------------------------------------------------------------------
    # Write
    # ---------------------------------------------------------------------------------------
    write_csv(project / "era_ph5_metro.csv", G1_COLUMNS, g1, args.no_write)
    write_csv(project / "era_ph5_stack.csv", G2_COLUMNS, g2, args.no_write)
    write_csv(project / "era_ph5_month.csv", G3_COLUMNS, g3, args.no_write)
    write_csv(project / "era_ph5_caveat.csv", G4_COLUMNS, g4, args.no_write)

    # ---------------------------------------------------------------------------------------
    # P8 - the manifest (Unit 5B-y, Ruling E-5.1).  Written in the SAME run as the four CSVs,
    # from the bytes now on disk, so X13a in era_ph5_workbook_gate.py has a committed reference
    # for content and X13b has a UTC stamp that no checkout can reset.  Then read back: the
    # gate asserts against what is on disk, not what this process meant to write.
    # ---------------------------------------------------------------------------------------
    manifest = None
    if not args.no_write:
        manifest = write_manifest(project, conn, {"G1": (g1, G1_COLUMNS), "G2": (g2, G2_COLUMNS),
                                                  "G3": (g3, G3_COLUMNS), "G4": (g4, G4_COLUMNS)})
    if run("P8"):
        emit("")
        hr("P8 - the grains manifest: content and UTC write stamp, committed with the CSVs")
        if args.no_write:
            emit("  (--no-write: no manifest is written, so P8a is not asserted)")
        else:
            back = json.loads((project / MANIFEST_NAME).read_text(encoding="utf-8"))
            bad = []
            for fn, entry in back["grains"].items():
                on_disk = md5_of(project / fn)
                if on_disk != entry["md5"]:
                    bad.append(f"{fn} {on_disk} != manifest {entry['md5']}")
            short = ", ".join("%s %s" % (k, v["md5"][:8]) for k, v in back["grains"].items())
            gate("P8a", not bad and back == manifest,
                 f"{MANIFEST_NAME} read back from disk names the md5 of every grain as it now sits "
                 f"beside it ({short}), "
                 f"written_utc {back['written_utc']}, db {back['db_md5'][:8]} user_version "
                 f"{back['user_version']}" + ("" if not bad else f"; MISMATCH {bad}"))

    def dict_rows(grain, columns, doc, kind_default):
        out = [f"### {grain} — `era_ph5_{ {'G1': 'metro', 'G2': 'stack', 'G3': 'month', 'G4': 'caveat'}[grain] }.csv`",
               "", "| column | units | basis | provenance | derived or declared |",
               "| --- | --- | --- | --- | --- |"]
        for c in columns:
            if grain == "G1" and c in DERIVED_DOC:
                u, prov, kind = DERIVED_DOC[c]
                basis = "facility (`plant_derived_4a`), L = 1.150, alpha = 2.8311"
            else:
                u, prov = doc[c]
                kind = kind_default
                basis = ("facility (`plant_derived_4a`)" if grain != "G4" else "—")
            out.append(f"| `{c}` | {u} | {basis} | {prov} | {kind} |")
        out.append("")
        return out

    dic = [
        "# Phase 5 data dictionary — the four extract grains",
        "",
        "`era_ph5_dictionary_v1.0.md` · Unit 5A of `direction_ph5_tableau_v1.0.md` · "
        "generated by `era_ph5_extract.py`",
        "",
        "Every column of every grain, with its units, its basis, its provenance and whether it is "
        "**derived** in this unit, **carried** unchanged from Unit 4R's frozen contract, or "
        "**declared** here. Gate `P6a` asserts the coverage in both directions: no column without "
        "an entry, and no entry without a column.",
        "",
        "## Bases, stated once",
        "",
        "- **The published basis is the FACILITY basis, `plant_derived_4a`, at L = 1.150 and "
        "alpha = 2.8311, variant `lf090`.** Every dollar in all four grains is on it.",
        "- **`$ per IT-MWh` is the siting metric** — sites are compared at equal IT capacity, and "
        "IT energy is identical across metros by construction. `$ per metered-MWh` compares "
        "TARIFFS, not sites, and is available as a swap, never as a default.",
        "- **G3 is the only grain this unit genuinely re-derives.** The two existing monthly "
        "files, `era_engine_v1.2_monthly.csv` and `era_ph4a_engine_monthly.csv`, are DETERMINANT "
        "series and carry no dollar column at all (gate `P1e`), so neither could be G3 whatever "
        "basis it were on. `era_ph4a_engine_monthly.csv` is the one on the published facility "
        "basis and gate `P1f` shows its determinants are still correct on the migrated database, "
        "because a market energy rate does not enter a kWh or a kW.",
        "- **G3's monthly costs come from `era_ph5_monthly.py`**, a transcription of "
        "`era_engine.bill_schedule`'s own accumulation with each scalar replaced by a "
        "twelve-element dict. It is pinned to the engine's source by content hash (`P1a`) and "
        "every bill it takes is required to sum to the engine's own annual figure to the cent "
        "(`P1b`).",
        "- **One declared allocation exists in the four grains and it is named**: ORC 5727.81(C)'s "
        "annual self-assessment has no monthly form, so G3 spreads it on the month's share of "
        "metered kWh. `C-EXCISE-ALLOC` in G4 says so.",
        "",
        "## Reading G3 without double-counting",
        "",
        "`stage` takes four values and `value_type` says what each one is. `baseline` and "
        "`mitigated` are **levels**; `measures` and `storage` are **deltas**. "
        "`mitigated = baseline + measures + storage` in every month, so **summing all four stages "
        "double-counts**. A view shows one stage, or shows `baseline` and `mitigated` together.",
        "",
    ]
    dic += dict_rows("G1", G1_COLUMNS, CONTRACT_DOC, "carried from the frozen contract")
    dic += dict_rows("G2", G2_COLUMNS, G2_DOC, "derived")
    dic += dict_rows("G3", G3_COLUMNS, G3_DOC, "derived")
    dic += dict_rows("G4", G4_COLUMNS, G4_DOC, "declared, reconciled against the reports")
    write_text(project / "era_ph5_dictionary_v1.0.md", "\n".join(dic) + "\n", args.no_write)

    sty = [
        "# Phase 5 style tokens", "",
        "`era_ph5_style_v1.0.md` · Unit 5A of `direction_ph5_tableau_v1.0.md` · "
        "generated by `era_ph5_extract.py` · **Ruling P5-4**", "",
        "Austere architectural presentation: maximum negative space, structural alignment, one "
        "sans-serif, **strict monochromatic — one accent, distinction by tint, tone and shade "
        "only, on stark white**, text reduced to labels. `era_ph5_workbook_gate.py` (Unit 5B) "
        "asserts that the colours in the saved `.twb` are drawn from this list and nothing else.",
        "",
        f"## Colour — one hue, {ACCENT_HUE:.0f}°",
        "",
        f"Every token below is generated from HSL hue **{ACCENT_HUE:.0f}°**. Gate `P6c` "
        f"recomputes the hue back out of each hex and requires them all to agree, so a token "
        f"cannot be off-hue and still be named on-hue.",
        "",
        "| token | hex | S | L | use |", "| --- | --- | --: | --: | --- |",
    ]
    for n, hx, s, l, note in STYLE_TOKENS:
        sty.append(f"| `{n}` | `{hx}` | {s:.2f} | {l:.3f} | {note} |")
    sty += [
        "", "**Rules.**", "",
        "1. **No second hue, anywhere.** A diverging measure (saving against cost) uses the two "
        "ends of the accent ramp — `--era-accent-100` to `--era-accent-700` — never two hues. "
        "Saving and cost are one quantity with a sign.",
        "2. **Sequential measures** use the ramp in order; **categorical** distinctions use "
        "position and label, not colour. If a view needs more than seven colour steps it needs a "
        "different view.",
        "3. **Excluded and unpriced quantities are drawn in `--era-muted` with a hairline "
        "outline**, never filled in accent — they are present and they are not in the total.",
        "4. **`--era-surface` is the only background.** No panel fills except "
        "`--era-surface-alt`; no shadows; no borders except `--era-rule`.",
        "", "## Type", "",
        f"One family: `{', '.join(TYPE_FAMILY)}`. Five sizes and no others.", "",
        "| role | px |", "| --- | --: |",
    ]
    for role, px in TYPE_SCALE:
        sty.append(f"| {role} | {px} |")
    sty += [
        "", "## Grid", "",
        f"- Base unit **{GRID_BASE_PX} px**; every dimension is a multiple of it.",
        f"- Outer margin **{MARGIN_PX} px**; gutter between panes **{GUTTER_PX} px**.",
        "- Axis rules `--era-rule` at 1 px. **Gridlines off by default**; where a value must be "
        "read off an axis, `--era-grid` at 1 px and nothing heavier.",
        "- Titles left-aligned to the content edge. No centred text.",
        "", "## Text", "",
        "Text is reduced to labels. The images and the graphics carry the argument; explanation "
        "belongs in the caveats sheet (G4) and in the report, not on the marks. **Ruling P5-3's "
        "caveats sheet is DATA, and Unit 5C's hard requirement is zero typed figures anywhere in "
        "the workbook** — every number on screen resolves to a field.",
        "",
    ]
    write_text(project / "era_ph5_style_v1.0.md", "\n".join(sty) + "\n", args.no_write)

    emit("")
    hr("Unit 5A result")
    npass = sum(1 for _, ok in RESULTS if ok)
    emit(f"  {npass} of {len(RESULTS)} gates PASS"
         + ("" if not FAILURES else f";  FAILING: {[f.split()[0] for f in FAILURES]}"))
    emit(f"  G1 {len(g1)} rows x {len(G1_COLUMNS)} cols   G2 {len(g2)} x {len(G2_COLUMNS)}   "
         f"G3 {len(g3)} x {len(G3_COLUMNS)}   G4 {len(g4)} x {len(G4_COLUMNS)}")
    emit(f"  written: {'NOTHING (--no-write)' if args.no_write else 'era_ph5_metro.csv, era_ph5_stack.csv, era_ph5_month.csv, era_ph5_caveat.csv, era_ph5_grains_manifest.json, era_ph5_dictionary_v1.0.md, era_ph5_style_v1.0.md'}")
    if _LOG[0] is not None:
        _LOG[0].close()
    sys.exit(1 if FAILURES else 0)


if __name__ == "__main__":
    main()
