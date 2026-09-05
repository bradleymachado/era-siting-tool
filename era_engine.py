"""era_engine.py  ("Cost Engine v1.2", Unit 4A)

v1.2 (Unit 4A) adds the FACILITY BASIS and changes nothing else about the billing machinery.
Unit 2E's docstring predicted "this engine bills them with no code change"; that was wrong, and
the reason is worth recording. A facility profile is PER METRO -- it is the IT series times that
metro's own weather-driven PUE -- so the run loop can no longer bill every schedule against one
profile, and assertion A3 ("the 15-minute peak equals the 1,000 MW design peak exactly") is FALSE
on a facility series by construction, because the whole point of Ruling 4 is that the meter peaks
above the IT design peak. Four things change:

  1.  load_facility_profile() reads the Unit 4A per-metro series and re-checks the Unit 2D
      conventions in their facility form, including the PUE stamp.
  2.  run_profiles() dispatches a per-metro profile when --facility-basis is given.
  3.  A3 is REPLACED on the facility basis, not suspended: A3F asserts the UNDERLYING IT peak is
      still exactly 1,000 MW (read from the facility file's own it_mw column, so a corrupt
      overlay cannot hide inside the product) and A3G asserts the facility peak exceeds it.
  4.  Every result row carries it_annual_mwh, usd_per_it_mwh and the PUE stamp, so the Phase 4
      $ per IT-MWh basis is produced by the engine rather than assembled afterwards.

A1 is kept exactly as Unit 2E wrote it -- it FAILS, as it has since Unit 2C-b itemised GS-4's
100 % twelve-month ratchet, and turning a failing assertion into a passing one is how a real
change gets absorbed. A1b is ADDED beside it, declaring the expected binding set, so a ratchet
that starts binding BECAUSE of the facility basis is caught rather than blamed on GS-4.

--- inherited from v1.1 -------------------------------------------------------------------------
"""

_V11_DOCSTRING = """era_engine_v1.1.py  ("Cost Engine v1.1")

v1.1 (Unit 2C-d) differs from v1.0 in THREE lines of substance and nothing else:
the F1 regression target moves from era_acceptance_results_v1.2.csv to
era_acceptance_results_v1.4.csv, the target file is overridable from the command
line so a trial database can be gated without touching the project copy, and the
output CSVs carry the v1.1 name. The billing machinery is byte-for-byte v1.0 --
deliberately, because Chicago's new record must be billed by code that has already
reproduced every other schedule to the cent.

Why the target moved: v1.2 predates the Unit 2C-b itemisation of Dominion GS-4 and
the Unit 2C-d retirement of ComEd Rate BES. v1.4 is the first acceptance output
that contains BESH-HV, which has no v1.2 or v1.3 row to regress against.


This section is intended to bill any 15-minute load profile against any schedule stored in
era_rates.db, charge by charge, reading the billing determinant off each rate row rather than
assuming one per schedule; and to prove it is trustworthy by reproducing the Phase 1 / Unit 2C
acceptance figures on the F1 regression fixture BEFORE it is allowed to read a real profile.

Unit 2E of direction_ph2_cost_engine_v1.0.md.  Read-only with respect to era_rates.db.

-------------------------------------------------------------------------------------------------
THE GATE (direction_ph2_cost_engine_v1.0.md, F1 and Unit 2E)
-------------------------------------------------------------------------------------------------
F1 ratified the 100,000 kW flat / CY2027 / pf 0.99 reference load as a permanent regression
fixture: "every future engine version must reproduce the Phase 1 acceptance numbers on it (within
stated tolerance) before running real profiles."

That gate is enforced in code, not by convention.  run_f1_regression() runs first, always, on
every invocation.  If any schedule's annual total differs from era_acceptance_results_v1.4.csv by
more than F1_TOL_USD, or its all-in rate by more than F1_TOL_USD_PER_MWH, the engine exits
non-zero and NO profile is read.  --f1-only stops after the gate.  There is no override flag; a
gate you can switch off is not a gate.

The fixture is generated here as 35,040 flat 15-minute intervals rather than copied from the
acceptance script, so the gate tests the interval machinery, not a shared shortcut.  If the
interval engine and the hour-grid acceptance query agree to the dollar on a flat load, the
interval classification, the tier ladders, the determinant dispatch and the mechanic evaluation
are all doing what Phase 1 proved they should.

-------------------------------------------------------------------------------------------------
PROFILE CONVENTIONS INHERITED FROM UNIT 2D (project_phase2_unit2d.md).  Binding.
-------------------------------------------------------------------------------------------------
  1. The profile index is LOCAL STANDARD TIME with no DST, matching the EPW/TMYx weather index.
     Tariff TOU windows are published in LOCAL PREVAILING TIME.  THIS ENGINE APPLIES THE SHIFT
     (brief_ph2_unit2d_open_v1.0.md item 3, option A).  Phoenix / APS does not observe DST.
  2. 30-minute companion pairs are (0,1), (2,3), ... from local midnight.  The engine RECOMPUTES
     the pairing from the 15-minute file and asserts it against the committed companion, on the
     Unit 2D T03 precedent: a one-interval slip is invisible in every summary statistic and bills
     the wrong demand in Columbus, Atlanta and Northern Virginia.
  3. IT design peak 1,000 MW; the 15-minute maximum equals it exactly by construction.
  4. Load factor moves energy charges and hours-use ladders only, never a demand charge.

-------------------------------------------------------------------------------------------------
TWO STATED DEFAULTS.  Both are constraints inside an otherwise clear directive, resolved here and
proceeded under; neither invents a ruling the strategy chat has been asked for.
-------------------------------------------------------------------------------------------------
  A. PUE OVERLAY IS GATED (brief_ph2_unit2a_pue_amplitude_v1.0.md, restated by 2D finding F2D-3).
     No facility-side profile exists, so no facility-side profile can be billed.  The engine
     bills the IT series as delivered, i.e. at an implied PUE of exactly 1.00, and stamps
     pue_basis = 'it_only_pue_1.00_GATED' on every profile row it emits.  Every number from a
     profile run is therefore a STRICT LOWER BOUND on the metro's real bill, and the metros are
     NOT yet comparable on facility cost, because PUE differs by climate.  When the amplitude
     ruling lands, 2D emits eight facility series and this engine bills them with no code change.

  B. THE ERCOT 4CP INTERVALS ARE NOT RESOLVABLE TO A CALENDAR FROM THIS SESSION.  Unit 2E's
     brief asks for "ERCOT's published prior-year 4CP intervals, documented".  ERCOT publishes
     the settled 4CP intervals through its data-products portal, which is not reachable here;
     of the secondary sources that are reachable, none carries all four months of any one year
     (see CP4_SOURCE_NOTES).  Rather than invent four dates, the engine computes the 4CP
     determinant as an EXPECTED VALUE over ERCOT's declared 4CP window - the treatment
     brief_ph2_unit2d_open_v1.0.md item 1 asks for, combining its options A and B - and reports
     the single-draw band alongside it.  On a flat load every candidate interval is identical,
     so this is the identity on the F1 fixture and the gate is unaffected by it.

Run from the project folder:

    python .\\era_engine_v1.0.py                 # gate, then all metros on the lf090 baseline
    python .\\era_engine_v1.0.py --f1-only       # gate only
    python .\\era_engine_v1.0.py --variants lf090,lf082,lf095

Exit code 0 = gate PASS and every engine assertion PASS.  1 = at least one failed.
"""

import argparse
import calendar
import csv
import json
import math
import sqlite3
import sys
from datetime import datetime, timedelta
from pathlib import Path

HERE = Path(__file__).parent
DB_FILE = HERE / "era_rates.db"
# v1.2 retargets the F1 gate from v1.4 to v1.5. v1.4 predates Unit 2G's AEP-Dayton correction,
# which moved Columbus by +7.21 $/MWh on every basis; v1.5 is the first acceptance output that
# contains it. Unit 2G already ran the gate against v1.5 from the command line - this makes the
# default match what the project actually gates on, so a bare invocation is not a failing one.
# UNIT 4R, 2026-08-29: the same move again, for the same reason and by the same precedent.
# Ruling 8 (direction_ph4_close_v1.0.md) moved AEP Ohio's competitive-supply parameter, and the
# acceptance CSV stores Columbus's market_usd as a NUMBER, so v1.5 no longer describes the
# database. v1.6 is regenerated from the migrated database by era_acceptance.py and moves exactly
# two rows and five columns (gated at era_ph4r_reissue.py R0e/R0f). v1.5 is Unit 2C-d's cited
# pre-ruling record and is preserved untouched.
ACCEPTANCE_CSV = HERE / "era_acceptance_results_v1.6.csv"
PROFILE_DIR = HERE / "data" / "profiles"
OUT_F1 = HERE / "era_engine_f1_regression.csv"
OUT_RESULTS = HERE / "era_engine_results.csv"
OUT_MONTHLY = HERE / "era_engine_monthly.csv"

REQUIRED_SCHEMA_VERSION = 13

# =================================================================================================
# PARAMETER BLOCK - every number the engine uses that is not read from era_rates.db
# =================================================================================================

FORCE_NO_DST = False                 # set only by the DST sensitivity diagnostic

STUDY_YEAR = 2027
N_INTERVALS = 35_040                 # 365 days x 96
INTERVAL_HOURS = 0.25
HOURS_IN_YEAR = 8_760

# --- F1 regression fixture (direction_ph2_cost_engine_v1.0.md, F1; ratified permanent) ----------
F1_LOAD_KW = 100_000.0
F1_POWER_FACTOR = 0.99
F1_TOL_USD = 1.00                    # dollars per year, on bills of $35M-$177M
F1_TOL_USD_PER_MWH = 0.0005

# --- Named clock divergences (Unit 2C-d) -------------------------------------------------------
# The acceptance script bills on a NAIVE 8,760-hour calendar; this engine bills on the PREVAILING
# clock, where CY2027 March has 743 hours and November 721. For eleven of the twelve schedules the
# two DST transitions fall inside the same rate group and cancel exactly, which is why the gate has
# never seen this before. ComEd Rider CFRA is the first charge in the project whose month groups
# straddle both transitions AT DIFFERENT RATES:
#
#   March      (-1 h) x 100,000 kW x -0.00984 $/kWh (Jan-May window)  = +984
#   November   (+1 h) x 100,000 kW x -0.01057 $/kWh (Oct-Dec window)  = -1,057
#                                                                 net = -73.00 $/yr
#
# That is a difference between two deliberately different clock models, not a defect in either,
# and the engine is the one that is right -- ComEd meters on the prevailing clock. It is EXEMPTED
# from the blanket tolerance and PINNED instead: the gate requires the divergence to equal the
# derived figure to the cent. A structural difference that is merely tolerated drifts silently;
# one that is asserted cannot.
CLOCK_DIVERGENCE_USD = {
    ("Chicago", "BESH-HV", "rider"): -73.00,
}
CLOCK_DIVERGENCE_TOL_USD = 0.01

# Unit 4A. The ratchets that are KNOWN to bind on the library as it now stands. GS-4's 100 %
# twelve-month distribution ratchet has bound since Unit 2C-b itemised it; nothing else does.
# Declared so that A1b can catch a NEW one rather than letting it hide behind A1's known failure.
EXPECTED_BINDING_RATCHETS = ["GS-4"]

# Unit 4A. On the facility basis Unit 2D convention 4 is BROKEN - see A6F. The tolerance below is
# not an invariance tolerance; it BOUNDS a real effect. Set at four times the measured worst
# (0.2561 %, AEP Ohio DCT on the adopted basis) so that A6F-b fails on a structural change rather
# than on the effect it exists to record.
FACILITY_LF_DEMAND_TOL = 0.0100

# --- engine defaults for a profile run ---------------------------------------------------------
POWER_FACTOR = 0.99                  # Ruling 4 engine default, carried from Phase 1
MARKET_PRICE_BAND = 0.25             # Ruling 1 para 3
LF_DEMAND_INVARIANCE_TOL = 0.0005    # 0.05%; measured worst 0.023% (see below)

# Contract capacity for the AEP Ohio DCT capacity-floor ladder.  STATED ASSUMPTION: a campus
# contracts for its design peak.  Sheet 223-1 gives no other anchor and the schema has no column
# for it.  Recorded so the ratchet floor is computable rather than skipped.
CONTRACT_CAPACITY_BASIS = "design_peak"

# Unit 2D convention 4 says load factor moves energy and hours-use ladders only, never a demand
# charge.  Measured here across the three committed variants it holds to 0.023% of the demand
# component, not exactly - and the residue is NOT a load-factor effect.  The annual 15-minute peak
# is 1,000 MW exactly by construction in all three, but a demand charge is billed MONTHLY, and a
# monthly peak is a noise maximum on a plateau that drifts by ~0.02% as the drain regime changes.
# The tolerance is set at twice the measured worst so the assertion fails on a real defect rather
# than on this.  See finding F2E-3.

# Schema gap carried from era_acceptance_v1.2.py verbatim.  The excess-reactive threshold has no
# schema element; it is a documented constant, not an invented rate.
REACTIVE_EXCESS_THRESHOLD_PCT_OF_KW = {
    "DCT": 0.50,
    "DCT-T": 0.50,
    "PLL-18": math.tan(math.acos(0.95)),
}

# Ruling 2 qualification gate.  Declared, with authority, exactly as in the acceptance script -
# a new schedule must not silently inherit a qualification it was never granted.
Q1_TARGET_LEVELS = {"itemised", "verified_aggregate"}
# Set at run time by the Q1 check. v1.0 printed caveat 2 unconditionally, which was true for
# every run it ever made; Unit 2C-d is the first run where it is not.
Q1_GATE_LIFTED = False
NON_QUALIFYING = {
    "MLM-10": "Ruling 2: retained as a non-qualifying reference. Printed vintage January 2016; "
              "rider stack unchecked.",
    "COMM-PRI-20MW-HLF": "Unit 1C / Q2: a Phase 4 measure, not a baseline. Eligibility requires "
                         "a negotiated instrument, not load characteristics alone.",
}

# --- PLL-18 interleaved ladder, Reading A (F2 CLOSED in Unit 2C, decisively) --------------------
INTERLEAVED_MARKER_UNIT = "kWh_per_kW"
INTERLEAVED_INNER_UNIT = "kWh"

# --- Daylight saving time ----------------------------------------------------------------------
# US rule since 2007: begins 02:00 local prevailing on the 2nd Sunday of March, ends 02:00 local
# prevailing on the 1st Sunday of November.  Expressed on the LOCAL STANDARD clock the profile is
# indexed in, that is 02:00 LST on the March Sunday to 01:00 LST on the November Sunday.
METRO_OBSERVES_DST = {
    "Atlanta": True,
    "Austin": True,
    "Chicago": True,
    "Columbus": True,
    "Dallas-Fort Worth": True,
    "Northern Virginia": True,
    "Phoenix": False,                 # Arizona does not observe DST
    "San Jose / Bay Area": True,
}

# --- ERCOT 4CP -----------------------------------------------------------------------------------
# ERCOT's transmission cost allocation bills on the customer's demand at the 15-minute interval of
# ERCOT system peak in each of June, July, August and September.  Oncor Rider TCRF is the only
# charge in the library on this determinant.
CP4_MONTHS = (6, 7, 8, 9)
CP4_HOUR_START = 15                  # local prevailing, inclusive
CP4_HOUR_END = 19                    # local prevailing, exclusive
CP4_WEEKDAY_ONLY = True              # the window Unit 2D's exposure analysis used; see below
CP4_MC_DRAWS = 100_000
CP4_MC_SEED = 20270401
CP4_SOURCE_NOTES = (
    "ERCOT settled 4CP intervals are published through the ERCOT data-products portal, not "
    "reachable from this session. Reachable secondary sources give isolated intervals only: "
    "2025 June = 2025-06-08 HE17 (a SUNDAY), 2025 July = 2025-07-29 HE17 (preliminary), "
    "2024 June = 2024-06-30 17:45 (a Sunday). No reachable source carries all four months of "
    "any one year. The determinant is therefore computed as an expected value over the window "
    "below rather than at four invented dates. The 2025 and 2024 June observations show a "
    "coincident peak CAN fall at a weekend, so the weekday restriction is a stated assumption; "
    "cp4_kw_allday is reported beside cp4_kw as its sensitivity."
)


class Rng:
    """Deterministic 64-bit LCG, identical to era_profile_synth_v1.0.Rng.

    Reused rather than re-invented so that any future ensemble work in this engine and the
    profile it bills draw from the same generator.
    """

    def __init__(self, seed):
        self.s = (seed ^ 0x9E3779B97F4A7C15) & 0xFFFFFFFFFFFFFFFF

    def _next(self):
        self.s = (self.s * 6364136223846793005 + 1442695040888963407) & 0xFFFFFFFFFFFFFFFF
        return self.s

    def random(self):
        return (self._next() >> 11) / float(1 << 53)

    def randrange(self, n):
        return int(self.random() * n)


# =================================================================================================
# Calendar and time basis
# =================================================================================================

def nth_weekday(year, month, weekday, n):
    """Date of the n-th `weekday` (0=Mon) of `month`. n is 1-based."""
    d = datetime(year, month, 1)
    offset = (weekday - d.weekday()) % 7
    return d + timedelta(days=offset + 7 * (n - 1))


def dst_bounds_lst(year):
    """(start, end) of DST expressed on the LOCAL STANDARD clock.

    DST begins 02:00 prevailing = 02:00 standard on the 2nd Sunday of March, and ends
    02:00 prevailing = 01:00 standard on the 1st Sunday of November.
    """
    start = nth_weekday(year, 3, 6, 2) + timedelta(hours=2)
    end = nth_weekday(year, 11, 6, 1) + timedelta(hours=1)
    return start, end


def build_lst_index(year=STUDY_YEAR):
    """15-minute local-standard-time stamps; index k covers minute 15k. Same basis as Unit 2D."""
    start = datetime(year, 1, 1)
    if (datetime(year + 1, 1, 1) - start).days * 96 != N_INTERVALS:
        raise ValueError(f"{year} is not a {N_INTERVALS // 96}-day year; this build assumes it is")
    return [start + timedelta(minutes=15 * k) for k in range(N_INTERVALS)]


def build_billing_calendar(lst_index, observes_dst):
    """Classify every interval on the LOCAL PREVAILING clock the tariff is published in.

    Returns a list of (month, day_type, hour, prevailing_datetime), one per 15-minute interval.

    The map is total and injective on the standard clock - every standard interval receives
    exactly one prevailing stamp - so the year still tiles exactly and no window can gain or lose
    an interval at a transition. What DOES move is which side of a window boundary an interval
    falls on for eight months of the year, which is the whole point.
    """
    if observes_dst:
        dst_start, dst_end = dst_bounds_lst(lst_index[0].year)
    out = []
    for t in lst_index:
        p = t + timedelta(hours=1) if (observes_dst and dst_start <= t < dst_end) else t
        day_type = "weekend" if p.weekday() >= 5 else "weekday"
        out.append((p.month, day_type, p.hour, p))
    return out


# =================================================================================================
# Profiles
# =================================================================================================

class Profile:
    """A 15-minute kW series with its clock-aligned 30-minute companion.

    kw15  : 35,040 interval-average kW, local standard time.
    kw30  : 17,520 half-hour mean kW, pairs (0,1), (2,3), ... from local midnight.
    """

    def __init__(self, name, kw15, kw30, provenance, pue_basis,
                 it_kw15=None, pue_level=None, pue_alpha=None, metro=None):
        if len(kw15) != N_INTERVALS:
            raise ValueError(f"{name}: {len(kw15)} intervals, expected {N_INTERVALS}")
        if len(kw30) != N_INTERVALS // 2:
            raise ValueError(f"{name}: {len(kw30)} half-hours, expected {N_INTERVALS // 2}")
        self.name = name
        self.kw15 = kw15
        self.kw30 = kw30
        self.provenance = provenance
        self.pue_basis = pue_basis
        # The IT series underlying this profile. For an IT profile it IS this profile; for a
        # facility profile it is the pre-overlay series, kept so that $ per IT-MWh is computed
        # from the delivered IT energy rather than from the metered energy divided by a mean PUE.
        self.it_kw15 = kw15 if it_kw15 is None else it_kw15
        self.pue_level = pue_level
        self.pue_alpha = pue_alpha
        self.metro = metro

    @property
    def it_annual_kwh(self):
        return sum(self.it_kw15) * INTERVAL_HOURS

    @property
    def it_peak_kw(self):
        return max(self.it_kw15)

    @property
    def peak_kw(self):
        return max(self.kw15)

    @property
    def annual_kwh(self):
        return sum(self.kw15) * INTERVAL_HOURS


def pair_30_from_15(kw15):
    """Recompute the 30-minute companion from the 15-minute series, pairs (0,1), (2,3), ...

    Unit 2D's T03 tamper is a companion file whose pairs are slipped one interval. No statistic
    of such a file looks wrong and it bills the wrong demand in three metros. The only defence is
    to recompute rather than trust, so the engine never reads the companion for billing - it
    reads it only to assert the committed file agrees with this.
    """
    return [(kw15[2 * j] + kw15[2 * j + 1]) / 2.0 for j in range(len(kw15) // 2)]


def make_f1_fixture():
    """The permanent F1 regression fixture: 100,000 kW flat, CY2027, 8,760 h, pf 0.99.

    Built from 35,040 flat intervals rather than copied from the acceptance script, so that the
    gate exercises the interval machinery instead of sharing a shortcut with what it is testing.
    """
    kw15 = [F1_LOAD_KW] * N_INTERVALS
    return Profile("F1", kw15, pair_30_from_15(kw15),
                   provenance="direction_ph2_cost_engine_v1.0.md F1, ratified regression fixture",
                   pue_basis="n/a (not a data-center profile; a regression fixture)")


def load_2d_profile(variant, failures):
    """Load a Unit 2D IT profile and verify it against the four binding 2D conventions."""
    p15 = PROFILE_DIR / f"era_it_profile_{variant}_15min.csv"
    p30 = PROFILE_DIR / f"era_it_profile_{variant}_30min.csv"
    if not p15.exists() or not p30.exists():
        raise FileNotFoundError(f"Unit 2D profile {variant} not found under {PROFILE_DIR}")

    lst = build_lst_index()
    kw15, stamps = [], []
    with open(p15, newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            kw15.append(float(row["it_mw"]) * 1000.0)
            stamps.append(row["timestamp_lst"])
    kw30_file = []
    with open(p30, newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            kw30_file.append(float(row["it_mw_30min_mean"]) * 1000.0)

    # P1 - interval count and local-standard-time index, exact.
    ok = (len(kw15) == N_INTERVALS
          and all(s == t.strftime("%Y-%m-%d %H:%M") for s, t in zip(stamps, lst)))
    check(ok, f"P1 {variant}: 15-minute index is CY{STUDY_YEAR} local standard time, "
              f"{N_INTERVALS} intervals, no DST", failures)

    # P2 - the 30-minute companion is the (0,1),(2,3) pairing of the 15-minute file. Recomputed,
    #      never trusted. This is the check Unit 2D's T03 exists to defeat.
    kw30 = pair_30_from_15(kw15)
    worst = max(abs(a - b) for a, b in zip(kw30, kw30_file)) if len(kw30) == len(kw30_file) else -1
    check(len(kw30) == len(kw30_file) and worst <= 5e-4 * 1000.0,
          f"P2 {variant}: committed 30-minute companion equals the (0,1),(2,3) pairing "
          f"recomputed from the 15-minute file (worst |delta| {worst:.6f} kW)", failures)

    # P3 - the 15-minute maximum is the declared design peak exactly (2D, by construction).
    peak_mw = max(kw15) / 1000.0
    check(abs(peak_mw - 1000.0) <= 5e-4,
          f"P3 {variant}: 15-minute peak is the declared 1,000 MW design peak exactly "
          f"({peak_mw:.4f} MW)", failures)

    return Profile(variant, kw15, kw30,
                   provenance=f"era_profile_synth_v1.0 ({p15.name}, {p30.name})",
                   pue_basis="it_only_pue_1.00_GATED")


def load_facility_profile(metro, metro_key, variant, tag, failures):
    """Load a Unit 4A per-metro FACILITY series and re-check the 2D conventions in facility form.

    The file carries four columns this loader uses -- it_mw, t_wb_c, pue, facility_mw -- and the
    checks below are written so that the product is verified against its own factors. A corrupt
    overlay that scaled facility_mw without touching it_mw or pue would pass a peak check and
    fail F1F; that is the point.
    """
    p15 = PROFILE_DIR / f"era_facility_profile_{metro_key}_{variant}_15min.csv"
    p30 = PROFILE_DIR / f"era_facility_profile_{metro_key}_{variant}_30min.csv"
    if not p15.exists() or not p30.exists():
        raise FileNotFoundError(f"Unit 4A facility profile {metro_key}/{variant} not found "
                                f"under {PROFILE_DIR}")

    lst = build_lst_index()
    kw15, it15, pue, stamps = [], [], [], []
    stamp_line = ""
    with open(p15, newline="", encoding="utf-8") as fh:
        lines = []
        for raw in fh:
            if raw.startswith("#"):
                if "pue_basis=" in raw:
                    stamp_line = raw.strip("# \n")
                continue
            lines.append(raw)
    for row in csv.DictReader(lines):
        kw15.append(float(row["facility_mw"]) * 1000.0)
        it15.append(float(row["it_mw"]) * 1000.0)
        pue.append(float(row["pue"]))
        stamps.append(row["timestamp_lst"])
    kw30_file = []
    with open(p30, newline="", encoding="utf-8") as fh:
        lines = [r for r in fh if not r.startswith("#")]
    for row in csv.DictReader(lines):
        kw30_file.append(float(row["facility_mw_30min_mean"]) * 1000.0)

    # F1F - the index, exactly as P1 does for an IT profile.
    ok = (len(kw15) == N_INTERVALS
          and all(s == t.strftime("%Y-%m-%d %H:%M") for s, t in zip(stamps, lst)))
    check(ok, f"F1F {metro_key}/{variant}: 15-minute index is CY{STUDY_YEAR} local standard "
              f"time, {N_INTERVALS} intervals, no DST", failures)

    # F2F - the 30-minute companion, recomputed and never trusted (the Unit 2D T03 precedent).
    kw30 = pair_30_from_15(kw15)
    worst = (max(abs(a - b) for a, b in zip(kw30, kw30_file))
             if len(kw30) == len(kw30_file) else -1)
    check(len(kw30) == len(kw30_file) and worst <= 5e-4 * 1000.0,
          f"F2F {metro_key}/{variant}: committed 30-minute companion equals the (0,1),(2,3) "
          f"pairing recomputed from the 15-minute file (worst |delta| {worst:.6f} kW)", failures)

    # F3F - the product is its own factors. facility_mw == it_mw * pue, interval by interval.
    worst_p = max(abs(kw15[i] - it15[i] * pue[i]) for i in range(len(kw15)))
    check(worst_p <= 1.0,
          f"F3F {metro_key}/{variant}: facility kW equals IT kW x PUE interval by interval "
          f"(worst |delta| {worst_p:.6f} kW on a ~1.2e6 kW series)", failures)

    # F4F - the UNDERLYING IT peak is still the declared 1,000 MW design peak. This is Unit 2D
    #       convention 3 surviving the overlay; A3's replacement reads it from here.
    it_peak_mw = max(it15) / 1000.0
    check(abs(it_peak_mw - 1000.0) <= 5e-4,
          f"F4F {metro_key}/{variant}: the IT series inside the facility file still peaks at "
          f"exactly 1,000 MW ({it_peak_mw:.4f} MW)", failures)

    # F5F - the PUE stamp is present and is the one this run asked for. Ruling 6's last line.
    want = f"pue_basis={tag}"
    check(want in stamp_line,
          f"F5F {metro_key}/{variant}: the file carries the requested PUE stamp "
          f"({want!r} in {stamp_line!r})", failures)
    lvl = alp = None
    for tok in stamp_line.split():
        if tok.startswith("L="):
            lvl = float(tok[2:])
        elif tok.startswith("alpha="):
            alp = float(tok[6:])

    return Profile(f"{tag}/{variant}", kw15, kw30,
                   provenance=f"era_ph4a_facility ({p15.name}, {p30.name})",
                   pue_basis=tag, it_kw15=it15, pue_level=lvl, pue_alpha=alp, metro=metro)


# =================================================================================================
# Determinants - the metered quantity each charge bills on
# =================================================================================================

class Determinants:
    """Every billing quantity one schedule needs, for one profile in one metro's clock.

    Built once per (schedule, profile) because the TOU period map is schedule-specific and the
    clock is metro-specific.
    """

    def __init__(self, profile, billing_cal, period_map_energy, period_map_demand,
                 cp4_window_mask, cp4_window_mask_allday, need_cp4_band):
        self.profile = profile
        # ---- monthly energy and monthly non-coincident peaks --------------------------------
        self.kwh_month = {m: 0.0 for m in range(1, 13)}
        self.ncp15_month = {m: 0.0 for m in range(1, 13)}
        for k, kw in enumerate(profile.kw15):
            m = billing_cal[k][0]
            self.kwh_month[m] += kw * INTERVAL_HOURS
            if kw > self.ncp15_month[m]:
                self.ncp15_month[m] = kw
        # A half-hour is billed in the month of its first 15-minute child; both children share a
        # prevailing hour, so the pair never straddles a window boundary either.
        self.ncp30_month = {m: 0.0 for m in range(1, 13)}
        for j, kw in enumerate(profile.kw30):
            m = billing_cal[2 * j][0]
            if kw > self.ncp30_month[m]:
                self.ncp30_month[m] = kw

        # ---- per-TOU-period monthly maxima, both integration intervals ----------------------
        self.period_ncp15 = {}   # (rate_period_id, month) -> kW
        self.period_ncp30 = {}
        self.period_kwh = {}     # (rate_period_id, month) -> kWh
        self.period_intervals = {}
        for k, kw in enumerate(profile.kw15):
            m, day_type, hour, _ = billing_cal[k]
            pid = period_map_energy[k]
            if pid is not None:
                key = (pid, m)
                self.period_kwh[key] = self.period_kwh.get(key, 0.0) + kw * INTERVAL_HOURS
                self.period_intervals[key] = self.period_intervals.get(key, 0) + 1
            pid = period_map_demand[k]
            if pid is not None:
                key = (pid, m)
                if kw > self.period_ncp15.get(key, 0.0):
                    self.period_ncp15[key] = kw
        for j, kw in enumerate(profile.kw30):
            pid = period_map_demand[2 * j]
            if pid is not None:
                key = (pid, billing_cal[2 * j][0])
                if kw > self.period_ncp30.get(key, 0.0):
                    self.period_ncp30[key] = kw

        # ---- ERCOT 4CP: expected value over the declared window, plus the single-draw band ---
        self.cp4_kw, self.cp4_band = self._cp4(profile, billing_cal, cp4_window_mask,
                                               need_cp4_band)
        self.cp4_kw_allday, _ = self._cp4(profile, billing_cal, cp4_window_mask_allday, False)

    @staticmethod
    def _cp4(profile, billing_cal, mask, need_band):
        """Expected 4CP determinant and its single-draw band.

        ERCOT's 4CP charge bills the average of the customer's demand at four intervals, one per
        summer month, chosen by ERCOT system peak - not by the customer. The engine therefore
        treats each month's coincident interval as an unobserved draw from the candidate window
        and reports E[average]. The expectation is exact (the mean of the four monthly means);
        the band is Monte Carlo over CP4_MC_DRAWS four-tuples with a fixed seed, because the
        distribution is heavily left-skewed - almost every draw sits on the plateau, and the
        occasional draw lands inside a drawdown. A normal band would misdescribe it.
        """
        buckets = {m: [] for m in CP4_MONTHS}
        for k, kw in enumerate(profile.kw15):
            if mask[k]:
                buckets[billing_cal[k][0]].append(kw)
        if any(not v for v in buckets.values()):
            raise ValueError("4CP candidate window is empty in at least one summer month")
        means = [sum(v) / len(v) for v in buckets.values()]
        expected = sum(means) / len(means)
        if not need_band:
            return expected, None

        rng = Rng(CP4_MC_SEED)
        cols = [buckets[m] for m in CP4_MONTHS]
        draws = []
        for _ in range(CP4_MC_DRAWS):
            draws.append(sum(c[rng.randrange(len(c))] for c in cols) / 4.0)
        draws.sort()
        band = {
            "p05": draws[int(0.05 * CP4_MC_DRAWS)],
            "p50": draws[int(0.50 * CP4_MC_DRAWS)],
            "p95": draws[int(0.95 * CP4_MC_DRAWS)],
            "min": draws[0],
            "max": draws[-1],
            "mean_mc": sum(draws) / len(draws),
        }
        return expected, band

    def monthly_kw(self, determinant, month):
        if determinant == "ncp_kw_15min":
            return self.ncp15_month[month]
        if determinant == "ncp_kw_30min":
            return self.ncp30_month[month]
        if determinant == "cp4_kw":
            return self.cp4_kw
        raise ValueError(f"monthly_kw called on determinant {determinant}")


def build_period_map(conn, schedule_id, applies_to, billing_cal, failures, label):
    """interval index -> rate_period_id, or None where no period of this kind covers it.

    Asserts, per interval rather than per (month, day_type, hour) cell, that no two windows of
    the same kind claim the same interval. This is the interval-level form of the acceptance
    script's overlap check and it is strictly stronger: it also catches a window that overlaps
    only on the days a DST shift moves.
    """
    periods = conn.execute(
        "SELECT rate_period_id FROM rate_period WHERE schedule_id = ? AND applies_to = ?",
        (schedule_id, applies_to)).fetchall()
    cells = {}
    for p in periods:
        pid = p["rate_period_id"]
        for w in conn.execute(
                "SELECT month_start, month_end, day_type, hour_start, hour_end "
                "FROM rate_period_window WHERE rate_period_id = ?", (pid,)):
            day_types = (["weekday", "weekend"] if w["day_type"] == "all" else [w["day_type"]])
            for month in range(w["month_start"], w["month_end"] + 1):
                for dt in day_types:
                    for hour in range(w["hour_start"], w["hour_end"]):
                        cells.setdefault((month, dt, hour), []).append(pid)

    doubled = sorted(k for k, v in cells.items() if len(v) > 1)
    check(not doubled,
          f"W1 {label} {applies_to}: no interval is claimed by two {applies_to} periods "
          f"({len(doubled)} collisions)", failures)

    out = []
    for m, dt, hr, _ in billing_cal:
        v = cells.get((m, dt, hr))
        out.append(v[0] if v else None)
    return out


def build_cp4_masks(billing_cal):
    """Two boolean masks over intervals: ERCOT's 4CP candidate window, weekday and all-day."""
    weekday, allday = [], []
    for m, dt, hr, _ in billing_cal:
        inside = (m in CP4_MONTHS and CP4_HOUR_START <= hr < CP4_HOUR_END)
        allday.append(inside)
        weekday.append(inside and dt == "weekday")
    return (weekday if CP4_WEEKDAY_ONLY else allday), allday


# =================================================================================================
# Tier ladders - semantics carried verbatim from era_acceptance_v1.2.py
# =================================================================================================

def ladder_cost(rows, quantity, demand_kw):
    """Cost of `quantity` billed through one tier ladder, all rows sharing a tier_unit.

    Bounds in kWh_per_kW are converted to kWh by multiplying by demand_kw. An untiered ladder is
    a flat rate. Returns (cost, priced_quantity).
    """
    if not rows:
        return 0.0, 0.0
    unit = rows[0]["tier_unit"]
    scale = demand_kw if unit == "kWh_per_kW" else 1.0
    total = 0.0
    priced = 0.0
    for row in sorted(rows, key=lambda r: r["tier_index"]):
        lo = 0.0 if row["tier_min"] is None else row["tier_min"] * scale
        hi = None if row["tier_max"] is None else row["tier_max"] * scale
        block_lo = max(lo, 0.0)
        block_hi = quantity if hi is None else min(hi, quantity)
        block = max(0.0, block_hi - block_lo)
        if block <= 0.0:
            continue
        total += block * (row["rate_value"] + row["rate_adj"])
        priced += block
    return total, priced


def energy_cost_for_period(rows, kwh, demand_kw):
    """Cost of `kwh` under one energy period's rate rows, handling PLL-18's interleaved ladder.

    Reading A, CLOSED decisively in Unit 2C by an exact affine decomposition: the kWh_per_kW
    ladder is the outer hours-use ladder; its zero-valued first block is a structural marker
    meaning "priced by the kWh ladder"; the marker's own rate_adj is not applied.
    """
    if not rows:
        return 0.0, ""
    units = {r["tier_unit"] for r in rows}

    if units == {INTERLEAVED_MARKER_UNIT, INTERLEAVED_INNER_UNIT}:
        outer = sorted([r for r in rows if r["tier_unit"] == INTERLEAVED_MARKER_UNIT],
                       key=lambda r: r["tier_index"])
        inner = [r for r in rows if r["tier_unit"] == INTERLEAVED_INNER_UNIT]
        marker = outer[0]
        if marker["rate_value"] != 0.0:
            raise ValueError("interleaved ladder: expected a zero-valued structural marker, "
                             f"found {marker['rate_value']}")
        first_block = min(kwh, (marker["tier_max"] or 0.0) * demand_kw)
        cost_first, _ = ladder_cost(inner, first_block, demand_kw)
        cost_rest, _ = ladder_cost(outer[1:], kwh, demand_kw)
        # The note is deliberately month-INDEPENDENT. An interval engine bills this ladder
        # twelve times a year on twelve different monthly kWh totals, and a note carrying the
        # month's kWh would produce twelve near-identical lines that read like twelve findings.
        return cost_first + cost_rest, (
            f"interleaved ladder, Reading A (F2 closed in 2C): the first "
            f"{marker['tier_max']:.0f} kWh/kW of each month is priced by the kWh ladder and the "
            f"marker row's rate_adj is not applied")

    if len(units) > 1:
        raise ValueError(f"unhandled multi-unit energy ladder: {units}")
    cost, _ = ladder_cost(rows, kwh, demand_kw)
    return cost, ""


# =================================================================================================
# Billing mechanics
# =================================================================================================

def ratchet_floor_kw(params, actual_by_month, design_peak_kw, month):
    """The billing-demand floor a demand_ratchet imposes in `month`, on a steady-state year.

    STEADY-STATE-YEAR ASSUMPTION, stated as the direction requires: the engine bills one year in
    isolation, so the lookback window wraps within CY2027 rather than reaching into a CY2026 the
    study does not model. This is the assumption that the campus is in a repeating operating year,
    which is exactly the regime a siting comparison is about. It is conservative in the direction
    that matters: a ramping campus would see HIGHER ratchet floors relative to its own load, never
    lower, because a real prior year would be smaller than a steady-state one only during ramp.
    """
    lookback = int(params.get("lookback_months") or 0)
    pct = float(params.get("lookback_pct") or 0.0)
    seasonal = params.get("seasonal") or {}

    floors = []

    if seasonal.get("summer_months") and seasonal.get("winter_months"):
        # Georgia Power PLL-18: 95% of the highest prior SUMMER month, 60% of the highest prior
        # WINTER month, both floors live in every month (2C correction 2).
        summer = [actual_by_month[m] for m in seasonal["summer_months"] if m != month]
        winter = [actual_by_month[m] for m in seasonal["winter_months"] if m != month]
        if summer:
            floors.append(float(seasonal.get("pct_of_prior_summer_peak", pct)) * max(summer))
        if winter:
            floors.append(float(seasonal.get("pct_of_prior_winter_peak", 0.0)) * max(winter))
    elif seasonal.get("ratchet_season_months"):
        # APS E-35: anchored on the highest On-Peak kW measured May-October.
        season = [actual_by_month[m] for m in seasonal["ratchet_season_months"]]
        if season:
            floors.append(pct * max(season))
    elif lookback and pct:
        # The `lookback` calendar months IMMEDIATELY PRECEDING `month`, wrapping within the
        # steady-state year. For month 7 with lookback 11 that is months 6,5,4,3,2,1,12,11,10,9,8
        # - it must EXCLUDE month 7 itself and INCLUDE month 6. Written as range(1, lookback + 1)
        # it silently dropped the immediately preceding month and included the billed month; the
        # error is invisible on an 11-of-12 maximum, and was found by the tamper harness's unit
        # assertion P02, not by any outcome. See finding F2E-4.
        prior = [actual_by_month[((month - 1 - i - 1) % 12) + 1] for i in range(lookback)]
        if prior:
            floors.append(pct * max(prior))

    for cf in params.get("capacity_floors") or []:
        up_to = cf.get("up_to_kw")
        if up_to is not None and design_peak_kw > up_to:
            continue
        if up_to is None and design_peak_kw <= 75_000:
            continue
        f = cf["base_kw"] + cf["pct_above_kw"] * max(0.0, design_peak_kw - cf["above_threshold_kw"])
        cap = cf.get("cap_pct_of_contract_capacity")
        if cap is not None:
            f = min(f, cap * design_peak_kw)
        floors.append(f)

    return max(floors) if floors else 0.0


# =================================================================================================
# Costing one schedule against one profile
# =================================================================================================

def bill_schedule(conn, sched, profile, lst_index, failures):
    """Annual bill for one schedule against one profile. Returns a result dict."""
    sid = sched["schedule_id"]
    code = sched["schedule_code"]
    metro = sched["metro"]
    label = f"{metro}/{code}"

    observes_dst = METRO_OBSERVES_DST[metro] and not FORCE_NO_DST
    billing_cal = build_billing_calendar(lst_index, observes_dst)
    pmap_e = build_period_map(conn, sid, "energy", billing_cal, failures, label)
    pmap_d = build_period_map(conn, sid, "demand", billing_cal, failures, label)
    mask_cp4, mask_cp4_allday = build_cp4_masks(billing_cal)

    rates = conn.execute("SELECT * FROM rate WHERE schedule_id = ?", (sid,)).fetchall()
    bills_cp4 = any(r["billing_determinant"] == "cp4_kw" for r in rates)
    det = Determinants(profile, billing_cal, pmap_e, pmap_d, mask_cp4, mask_cp4_allday,
                       need_cp4_band=bills_cp4)
    mechanics = conn.execute(
        "SELECT * FROM billing_mechanic WHERE schedule_id = ?", (sid,)).fetchall()

    design_peak_kw = profile.peak_kw

    # ---- billing demand by determinant, before and after any ratchet --------------------------
    actual = {
        "ncp_kw_15min": dict(det.ncp15_month),
        "ncp_kw_30min": dict(det.ncp30_month),
    }
    billed = {d: dict(v) for d, v in actual.items()}
    ratchet_binding_months = []
    ratchet_params = None
    ratchet_basis_period = None
    for m in mechanics:
        if m["mechanic_type"] != "demand_ratchet":
            continue
        ratchet_params = json.loads(m["params"])
        # Which determinant the floor applies to. The library declares it only where it is
        # unusual (Oncor names distribution kW, exempting Rider TCRF on 4CP kW); otherwise the
        # floor applies to whichever kW determinant the schedule's own demand charges bill on.
        det_names = {r["billing_determinant"] for r in rates
                     if r["charge_type"] in ("demand", "flat_demand")}
        target = "ncp_kw_15min"
        if ratchet_params.get("applies_to_determinant") == "distribution_system_billing_kw":
            target = "ncp_kw_15min"
        elif "ncp_kw_30min" in det_names:
            target = "ncp_kw_30min"
        seasonal = ratchet_params.get("seasonal") or {}
        if seasonal.get("basis", "").lower().find("on-peak") >= 0:
            # APS E-35: the floor is anchored on the ON-PEAK demand series, not the monthly NCP.
            onpeak = [p["rate_period_id"] for p in conn.execute(
                "SELECT rate_period_id FROM rate_period WHERE schedule_id = ? AND "
                "applies_to = 'demand' AND period_index = 1", (sid,))]
            if onpeak:
                ratchet_basis_period = onpeak[0]
        basis = ({mth: det.period_ncp15.get((ratchet_basis_period, mth), 0.0)
                  for mth in range(1, 13)} if ratchet_basis_period is not None
                 else actual[target])
        for mth in range(1, 13):
            floor = ratchet_floor_kw(ratchet_params, basis, design_peak_kw, mth)
            if floor > billed[target][mth] + 1e-9:
                billed[target][mth] = floor
                ratchet_binding_months.append(mth)

    dispatched = set()

    def kw_for(determinant, month):
        dispatched.add(determinant)
        if determinant == "cp4_kw":
            return det.cp4_kw
        return billed[determinant][month]

    energy = demand = fixed = rider = market = 0.0
    notes = []
    interleaved_notes = set()
    monthly_rows = []

    # ---- energy ------------------------------------------------------------------------------
    by_period = {}
    for r in rates:
        if r["charge_type"] == "energy":
            by_period.setdefault(r["rate_period_id"], []).append(r)

    intervals_priced = 0
    for period_id, rows in by_period.items():
        market_rows = [r for r in rows if r["is_market_price"] == 1]
        tariff_rows = [r for r in rows if r["is_market_price"] == 0]
        if period_id is None:
            months = {m: det.kwh_month[m] for m in range(1, 13)}
            counts = {m: 0 for m in range(1, 13)}
            for k in range(N_INTERVALS):
                counts[billing_cal[k][0]] += 1
        else:
            months = {m: det.period_kwh.get((period_id, m), 0.0) for m in range(1, 13)}
            months = {m: v for m, v in months.items() if v > 0.0}
            counts = {m: det.period_intervals.get((period_id, m), 0) for m in months}
        for month, kwh in months.items():
            intervals_priced += counts.get(month, 0)
            # The hours-use ladder scales on the month's BILLED demand, which is what the tariff
            # bills the ladder against - not on the design peak and not on the actual peak where
            # a ratchet has raised it.
            dkw = kw_for("ncp_kw_30min" if any(r["billing_determinant"] == "ncp_kw_30min"
                                               for r in rates
                                               if r["charge_type"] in ("demand", "flat_demand"))
                         else "ncp_kw_15min", month)
            if tariff_rows or market_rows:
                dispatched.add("energy_kwh")
            if tariff_rows:
                cost, note = energy_cost_for_period(tariff_rows, kwh, dkw)
                energy += cost
                if note:
                    interleaved_notes.add(note)
            for mr in market_rows:
                market += kwh * (mr["rate_value"] + mr["rate_adj"])

    # Every schedule's energy periods must tile the year exactly, once. There are at most two
    # independent coverage groups on one schedule: the untiered group (rate_period_id NULL, which
    # covers the whole year by definition) and the TOU group (a set of periods which must between
    # them cover the whole year exactly once). Each group contributes N_INTERVALS interval-slots.
    # This is the interval-level form of the acceptance script's "energy windows tile the year"
    # check, and it is strictly stronger: it is evaluated on the PREVAILING clock, so a window
    # table that only tiles before the DST shift fails here.
    energy_pids = {r["rate_period_id"] for r in rates if r["charge_type"] == "energy"}
    n_groups = (1 if None in energy_pids else 0) + (1 if energy_pids - {None} else 0)
    expected_slots = N_INTERVALS * n_groups
    check(intervals_priced == expected_slots,
          f"E1 {label}: energy periods tile CY{STUDY_YEAR} exactly on the prevailing clock "
          f"({intervals_priced} of {expected_slots} interval-slots)", failures)

    # ---- TOU demand --------------------------------------------------------------------------
    demand_by_period = {}
    for r in rates:
        if r["charge_type"] == "demand":
            demand_by_period.setdefault(r["rate_period_id"], []).append(r)
    for period_id, rows in demand_by_period.items():
        determinant = rows[0]["billing_determinant"]
        table = det.period_ncp30 if determinant == "ncp_kw_30min" else det.period_ncp15
        for month in range(1, 13):
            pkw = table.get((period_id, month), 0.0)
            if pkw <= 0.0:
                continue
            if ratchet_params is not None and period_id == ratchet_basis_period:
                pkw = max(pkw, billed[determinant][month]) if determinant in billed else pkw
            cost, _ = ladder_cost(rows, pkw, pkw)
            demand += cost

    # ---- flat (non-TOU) demand ---------------------------------------------------------------
    for r in rates:
        if r["charge_type"] != "flat_demand":
            continue
        months = (list(range(1, 13)) if not r["applicable_months"]
                  else [int(m) for m in r["applicable_months"].split(",")])
        for month in months:
            bkw = kw_for(r["billing_determinant"], month)
            cost, _ = ladder_cost([r], bkw, bkw)
            demand += cost

    # ---- fixed --------------------------------------------------------------------------------
    days_in_year = 366 if calendar.isleap(STUDY_YEAR) else 365
    for r in rates:
        if r["charge_type"] != "fixed":
            continue
        dispatched.add("fixed")
        if r["unit"] == "USD_per_month":
            fixed += 12 * (r["rate_value"] + r["rate_adj"])
        elif r["unit"] == "USD_per_day":
            fixed += days_in_year * (r["rate_value"] + r["rate_adj"])
        else:
            raise ValueError(f"unhandled fixed unit {r['unit']}")

    # ---- riders, each on its own declared determinant -----------------------------------------
    rider_ladders = {}
    for r in rates:
        if r["charge_type"] == "rider":
            rider_ladders.setdefault(
                (r["component_name"], r["unit"], r["applicable_months"],
                 r["billing_determinant"]), []).append(r)

    reactive_basis = ("ncp_kw_30min"
                      if any(r["billing_determinant"] == "ncp_kw_30min" for r in rates
                             if r["charge_type"] in ("demand", "flat_demand", "rider"))
                      else "ncp_kw_15min")
    tan_phi = math.tan(math.acos(POWER_FACTOR))

    for (comp, unit, months_str, determinant), rows in rider_ladders.items():
        months = (list(range(1, 13)) if not months_str
                  else [int(m) for m in months_str.split(",")])
        rate = rows[0]["rate_value"] + rows[0]["rate_adj"]
        if unit in ("USD_per_kW_month", "USD_per_kVA_month") and determinant != "kvar_excess":
            for month in months:
                bkw = kw_for(determinant, month)
                cost, _ = ladder_cost(rows, bkw, bkw)
                rider += cost
        elif unit == "USD_per_kWh":
            for month in months:
                dkw = kw_for(reactive_basis, month)
                cost, _ = ladder_cost(rows, det.kwh_month[month], dkw)
                rider += cost
        elif unit == "USD_per_kVAr_month":
            threshold = REACTIVE_EXCESS_THRESHOLD_PCT_OF_KW.get(code)
            zero_months = 0
            for month in months:
                bkw = kw_for(reactive_basis, month)
                kvar = bkw * tan_phi
                dispatched.add("kvar_excess")
                billable = kvar if threshold is None else max(0.0, kvar - threshold * bkw)
                rider += rate * billable
                if billable == 0.0:
                    zero_months += 1
            if threshold is not None and zero_months == len(months):
                notes.append(f"{comp}: zero at pf {POWER_FACTOR} in every month "
                             f"(tan phi {tan_phi:.4f} < {threshold:.4f} threshold)")
        elif unit == "USD_per_month":
            dispatched.add("fixed")
            rider += rate * len(months)
        else:
            raise ValueError(f"unhandled rider unit {unit}")

    subtotal = energy + demand + fixed + rider + market

    # ---- mechanics: report every one, binding or not ------------------------------------------
    mech_notes = []
    for m in mechanics:
        params = json.loads(m["params"])
        if m["mechanic_type"] == "demand_ratchet":
            if ratchet_binding_months:
                mech_notes.append(
                    f"demand_ratchet BINDING in month(s) "
                    f"{sorted(set(ratchet_binding_months))}")
            else:
                mech_notes.append("demand_ratchet non-binding: actual billing demand exceeds the "
                                  "floor in every month (F2D-1)")
        elif m["mechanic_type"] == "pf_demand_floor":
            if POWER_FACTOR >= params["pf_threshold"]:
                mech_notes.append(f"pf_demand_floor non-binding: pf {POWER_FACTOR} >= "
                                  f"{params['pf_threshold']}")
            else:
                mech_notes.append("pf_demand_floor BINDING - not modelled at this power factor")
        elif m["mechanic_type"] == "min_monthly_bill":
            floor = params["amount_usd"] * 12
            if subtotal < floor:
                mech_notes.append(f"min_monthly_bill BINDING: raised to {floor:,.0f}")
                subtotal = floor
            else:
                mech_notes.append(
                    f"min_monthly_bill non-binding: {params['amount_usd']:,.2f}/mo floor is "
                    f"{floor / subtotal:.4%} of the computed bill")

    annual_mwh = profile.annual_kwh / 1000.0
    lowest_monthly_peak_pct = (min(det.ncp15_month.values()) / profile.peak_kw
                               if profile.peak_kw else 0.0)

    for month in range(1, 13):
        monthly_rows.append({
            "profile": profile.name, "metro": metro, "schedule_code": code, "month": month,
            "kwh": det.kwh_month[month],
            "ncp_kw_15min": det.ncp15_month[month],
            "ncp_kw_30min": det.ncp30_month[month],
            "billed_kw_15min": billed["ncp_kw_15min"][month],
            "billed_kw_30min": billed["ncp_kw_30min"][month],
            "cp4_kw": det.cp4_kw,
        })

    return {
        "profile": profile.name,
        "metro": metro,
        "utility": sched["utility_name"],
        "schedule_code": code,
        "effective_date": sched["effective_date"],
        "voltage_level": sched["voltage_level"] or "-",
        "supply_basis": sched["supply_basis"],
        "observes_dst": int(observes_dst),
        "pue_basis": profile.pue_basis,
        "qualifies": code not in NON_QUALIFYING,
        "exclusion_reason": NON_QUALIFYING.get(code, ""),
        "rider_coverage": sched["rider_coverage"],
        "energy_usd": energy,
        "market_usd": market,
        "demand_usd": demand,
        "fixed_usd": fixed,
        "rider_usd": rider,
        "total_usd": subtotal,
        "annual_mwh": annual_mwh,
        "usd_per_mwh": subtotal / annual_mwh,
        # PHASE 4 BASIS. annual_mwh is METERED energy; it_annual_mwh is the IT energy delivered,
        # which is identical across metros by construction. $ per IT-MWh is therefore the basis on
        # which two metros are comparable as SITES for the same computer; $ per metered-MWh is the
        # basis on which two TARIFFS are comparable. Both are published; neither supersedes the
        # other (direction_ph4_scenario_layer_v1.0.md, "what this ruling does NOT change").
        "it_annual_mwh": profile.it_annual_kwh / 1000.0,
        "usd_per_it_mwh": subtotal / (profile.it_annual_kwh / 1000.0),
        "mean_pue_energy_weighted": (profile.annual_kwh / profile.it_annual_kwh),
        "pue_level_L": profile.pue_level,
        "pue_alpha": profile.pue_alpha,
        "it_peak_kw": profile.it_peak_kw,
        "facility_over_it_peak": profile.peak_kw / profile.it_peak_kw,
        "band_low_usd_per_mwh": ((subtotal - market * MARKET_PRICE_BAND) / annual_mwh
                                 if market else None),
        "band_high_usd_per_mwh": ((subtotal + market * MARKET_PRICE_BAND) / annual_mwh
                                  if market else None),
        "peak_kw": profile.peak_kw,
        "load_factor": profile.annual_kwh / (profile.peak_kw * HOURS_IN_YEAR),
        "lowest_monthly_peak_pct_of_annual": lowest_monthly_peak_pct,
        "cp4_kw": det.cp4_kw,
        "cp4_kw_allday": det.cp4_kw_allday,
        "bills_cp4": int(bills_cp4),
        "_dispatched": sorted(dispatched),
        "cp4_p05_kw": det.cp4_band["p05"] if det.cp4_band else None,
        "cp4_p95_kw": det.cp4_band["p95"] if det.cp4_band else None,
        "cp4_min_kw": det.cp4_band["min"] if det.cp4_band else None,
        "ratchet_binding": int(bool(ratchet_binding_months)),
        "notes": "; ".join(sorted(interleaved_notes) + notes + mech_notes),
        "_monthly": monthly_rows,
    }


# =================================================================================================
# Reporting helpers
# =================================================================================================

def check(condition, message, failures):
    print(f"  {'PASS' if condition else 'FAIL':<8} {message}")
    if not condition:
        failures.append(message)


SCHEDULE_SQL = """
SELECT s.*, u.metro, u.utility_name, u.market_structure
  FROM schedule s JOIN utility u ON u.utility_id = s.utility_id
 WHERE s.end_date IS NULL
 ORDER BY u.metro, s.schedule_code
"""


def results_by_key(results):
    return {(r["metro"], r["schedule_code"]): r for r in results}


def select_cheapest(results):
    selection = {}
    for r in results:
        if not r["qualifies"]:
            continue
        cur = selection.get(r["metro"])
        if cur is None or r["usd_per_mwh"] < cur["usd_per_mwh"]:
            selection[r["metro"]] = r
    return selection


# =================================================================================================
# The F1 regression gate
# =================================================================================================

def run_f1_regression(conn, lst_index):
    """Reproduce the Phase 1 / Unit 2C acceptance figures on the F1 fixture. Hard gate."""
    print("=" * 96)
    print("F1 REGRESSION GATE - direction_ph2_cost_engine_v1.0.md, F1")
    print(f"Fixture: {F1_LOAD_KW:,.0f} kW flat, CY{STUDY_YEAR}, {N_INTERVALS:,} x 15-minute "
          f"intervals, pf {F1_POWER_FACTOR}")
    print(f"Target : {ACCEPTANCE_CSV.name} (era_acceptance.py, Unit 2C-d)")
    print(f"Tolerance: |delta total| <= ${F1_TOL_USD:,.2f}/yr and "
          f"|delta rate| <= {F1_TOL_USD_PER_MWH} $/MWh")
    print("=" * 96)

    if not ACCEPTANCE_CSV.exists():
        print(f"ERROR: {ACCEPTANCE_CSV.name} not found; the gate has no target to reproduce.")
        return False, []

    target = {}
    with open(ACCEPTANCE_CSV, newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            target[(row["metro"], row["schedule_code"])] = row

    global POWER_FACTOR
    saved_pf = POWER_FACTOR
    POWER_FACTOR = F1_POWER_FACTOR
    fixture = make_f1_fixture()
    failures = []
    rows = []
    try:
        for sched in conn.execute(SCHEDULE_SQL):
            r = bill_schedule(conn, sched, fixture, lst_index, failures)
            t = target.get((r["metro"], r["schedule_code"]))
            if t is None:
                failures.append(f"{r['schedule_code']}: no acceptance row to regress against")
                continue
            rows.append({
                "metro": r["metro"], "schedule_code": r["schedule_code"],
                "acceptance_total_usd": float(t["total_usd"]),
                "engine_total_usd": r["total_usd"],
                "delta_usd": r["total_usd"] - float(t["total_usd"]),
                "acceptance_usd_per_mwh": float(t["usd_per_mwh"]),
                "engine_usd_per_mwh": r["usd_per_mwh"],
                "delta_usd_per_mwh": r["usd_per_mwh"] - float(t["usd_per_mwh"]),
                "acceptance_energy_usd": float(t["energy_usd"]),
                "engine_energy_usd": r["energy_usd"],
                "acceptance_market_usd": float(t["market_usd"]),
                "engine_market_usd": r["market_usd"],
                "acceptance_demand_usd": float(t["demand_usd"]),
                "engine_demand_usd": r["demand_usd"],
                "acceptance_fixed_usd": float(t["fixed_usd"]),
                "engine_fixed_usd": r["fixed_usd"],
                "acceptance_rider_usd": float(t["rider_usd"]),
                "engine_rider_usd": r["rider_usd"],
            })
    finally:
        POWER_FACTOR = saved_pf

    print("")
    hdr = (f"{'Metro':<20}{'Schedule':<18}{'acceptance $/MWh':>18}{'engine $/MWh':>14}"
           f"{'delta $/MWh':>13}{'delta $/yr':>14}")
    print(hdr)
    print("-" * len(hdr))
    for row in sorted(rows, key=lambda x: (x["metro"], x["schedule_code"])):
        print(f"{row['metro']:<20}{row['schedule_code']:<18}"
              f"{row['acceptance_usd_per_mwh']:>18.4f}{row['engine_usd_per_mwh']:>14.4f}"
              f"{row['delta_usd_per_mwh']:>13.6f}{row['delta_usd']:>14.4f}")

    with open(OUT_F1, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    print("")
    print("Gate checks:")
    check(len(rows) == len(target),
          f"G1 every acceptance row is regressed ({len(rows)} of {len(target)})", failures)
    def expected(row, comp):
        return CLOCK_DIVERGENCE_USD.get((row["metro"], row["schedule_code"], comp), 0.0)

    # G2 is evaluated on the delta NET of any named clock divergence, and each named divergence is
    # then asserted in its own right by G5 below.
    worst_usd = max((abs(r["delta_usd"] - expected(r, "rider")) for r in rows), default=0.0)
    worst_rate = max((abs(r["delta_usd_per_mwh"]) for r in rows), default=0.0)
    check(worst_usd <= F1_TOL_USD,
          f"G2 every schedule's annual total reproduces within ${F1_TOL_USD:,.2f}, net of named "
          f"clock divergences (worst ${worst_usd:,.6f})", failures)
    check(worst_rate <= F1_TOL_USD_PER_MWH,
          f"G3 every schedule's all-in rate reproduces within {F1_TOL_USD_PER_MWH} $/MWh "
          f"(worst {worst_rate:.8f})", failures)
    comps = [("energy", "energy_usd"), ("market", "market_usd"), ("demand", "demand_usd"),
             ("fixed", "fixed_usd"), ("rider", "rider_usd")]
    for name, key in comps:
        worst = max((abs(r[f"engine_{key}"] - r[f"acceptance_{key}"] - expected(r, name))
                     for r in rows), default=0.0)
        check(worst <= F1_TOL_USD,
              f"G4.{name} the {name} component reproduces line by line, not just in total, net "
              f"of named clock divergences (worst ${worst:,.6f})", failures)

    # G5 -- each named divergence must actually be there, at the derived magnitude. If a future
    # change removes the divergence, or moves it, this fails: the exception is not a licence.
    for (metro, code, comp), want in sorted(CLOCK_DIVERGENCE_USD.items()):
        hit = [r for r in rows if r["metro"] == metro and r["schedule_code"] == code]
        if not hit:
            check(False, f"G5 named clock divergence {metro}/{code}/{comp}: schedule not in the "
                         f"regression at all", failures)
            continue
        got = hit[0][f"engine_{comp}_usd"] - hit[0][f"acceptance_{comp}_usd"]
        check(abs(got - want) <= CLOCK_DIVERGENCE_TOL_USD,
              f"G5 named clock divergence {metro}/{code} {comp}: ${got:,.2f} against the derived "
              f"${want:,.2f} (DST, Rider CFRA month groups)", failures)

    ok = not failures
    print("")
    print(f"F1 REGRESSION GATE: {'PASS' if ok else 'FAIL'}"
          + ("" if ok else f" - {len(failures)} failure(s); NO profile will be read"))
    print("")
    return ok, failures


# =================================================================================================
# Profile runs
# =================================================================================================

# Unit 4A. The weather key each metro's facility series is filed under. Same map as
# era_ph2f_analysis_v1.0.py and era_ph4a_facility.py; asserted against the database, not assumed.
METRO_WEATHER_KEY = {
    "Atlanta": "atlanta", "Austin": "austin", "Chicago": "chicago", "Columbus": "columbus",
    "Dallas-Fort Worth": "dfw", "Northern Virginia": "northern_va", "Phoenix": "phoenix",
    "San Jose / Bay Area": "san_jose",
}


def run_profiles(conn, lst_index, variants, failures, facility_tag=None):
    all_results = []
    all_monthly = []
    metros_in_db = sorted({r["metro"] for r in conn.execute(SCHEDULE_SQL)})
    if facility_tag:
        check(set(metros_in_db) == set(METRO_WEATHER_KEY),
              f"F0F the weather-key map covers exactly the metros in the active library "
              f"({len(metros_in_db)} metros)", failures)
    for variant in variants:
        print("=" * 96)
        print(f"PROFILE RUN - {variant}" + (f" on facility basis {facility_tag}"
                                            if facility_tag else ""))
        print("=" * 96)
        if facility_tag:
            by_metro = {m: load_facility_profile(m, METRO_WEATHER_KEY[m], variant,
                                                 facility_tag, failures)
                        for m in metros_in_db}
            profile = by_metro[metros_in_db[0]]
            for m in metros_in_db:
                pr = by_metro[m]
                print(f"  {m:22s} peak {pr.peak_kw / 1000:9,.4f} MW · "
                      f"{pr.annual_kwh / 1e6:7,.1f} GWh · "
                      f"LF {pr.annual_kwh / (pr.peak_kw * HOURS_IN_YEAR):.4f} · "
                      f"mean PUE {pr.annual_kwh / pr.it_annual_kwh:.6f}")
            print(f"  PUE basis {profile.pue_basis} (L = {profile.pue_level}, "
                  f"alpha = {profile.pue_alpha})")
        else:
            profile = load_2d_profile(variant, failures)
            by_metro = None
            print(f"  peak {profile.peak_kw / 1000:,.4f} MW · "
                  f"{profile.annual_kwh / 1e6:,.1f} GWh · "
                  f"LF {profile.annual_kwh / (profile.peak_kw * HOURS_IN_YEAR):.4f} · "
                  f"PUE basis {profile.pue_basis}")
        print("")

        results = [bill_schedule(conn, s, (by_metro[s["metro"]] if by_metro else profile),
                                 lst_index, failures)
                   for s in conn.execute(SCHEDULE_SQL)]
        for r in results:
            all_monthly.extend(r.pop("_monthly"))
        all_results.extend(results)

        hdr = (f"{'Metro':<20}{'Schedule':<18}{'Cover':<20}{'Qual':<6}{'$/MWh':>9}"
               f"{'$/IT-MWh':>11}{'Band':>18}")
        print(hdr)
        print("-" * len(hdr))
        for r in results:
            band = ("" if r["band_low_usd_per_mwh"] is None
                    else f"{r['band_low_usd_per_mwh']:.2f}-{r['band_high_usd_per_mwh']:.2f}")
            print(f"{r['metro']:<20}{r['schedule_code']:<18}{r['rider_coverage']:<20}"
                  f"{('yes' if r['qualifies'] else 'no'):<6}{r['usd_per_mwh']:>9.2f}"
                  f"{r['usd_per_it_mwh']:>11.2f}{band:>18}")

        print("")
        print("Cost composition, $ per year:")
        comp = (f"{'Schedule':<18}{'Energy':>15}{'Market':>15}{'Demand':>15}{'Fixed':>12}"
                f"{'Rider':>15}{'Total':>16}")
        print(comp)
        print("-" * len(comp))
        for r in results:
            print(f"{r['schedule_code']:<18}{r['energy_usd']:>15,.0f}{r['market_usd']:>15,.0f}"
                  f"{r['demand_usd']:>15,.0f}{r['fixed_usd']:>12,.0f}{r['rider_usd']:>15,.0f}"
                  f"{r['total_usd']:>16,.0f}")

        print("")
        print("Per-schedule notes:")
        for r in results:
            if r["notes"]:
                print(f"  {r['schedule_code']}: {r['notes']}")

        print("")
        print("Ruling 2 - cheapest QUALIFYING schedule per metro:")
        selection = select_cheapest(results)
        for metro in sorted(selection):
            r = selection[metro]
            n = len([x for x in results if x["metro"] == metro and x["qualifies"]])
            caveat = ("   [transmission voltage: substation and interconnection capex is "
                      "transferred to the customer and is NOT priced here]"
                      if r["voltage_level"] == "transmission" else "")
            print(f"  {metro:<20}{r['schedule_code']:<18}{r['usd_per_mwh']:>8.2f} $/MWh   "
                  f"({n} qualifying){caveat}")

        print("")
        print("Engine assertions:")

        # F2D-1: Unit 2D established that every ratchet in the library is non-binding on the
        # baseline. 2E asserts it rather than rediscovering it.
        binding = sorted({r["schedule_code"] for r in results if r["ratchet_binding"]})
        lowest = min(r["lowest_monthly_peak_pct_of_annual"] for r in results)
        check(not binding,
              f"A1 F2D-1 holds: no ratchet in the library binds on this profile "
              f"(lowest monthly peak {lowest:.2%} of the annual peak; binding: "
              f"{binding or 'none'})", failures)

        # A1b - Unit 4A. A1 has FAILED since Unit 2C-b itemised Dominion GS-4's 100 % twelve-month
        # ratchet, and it is left failing on purpose: rewriting a failing assertion to match the
        # library is how a real regression gets absorbed. What A1b adds is a DECLARED expected
        # set, so that a ratchet which starts binding because the facility peak now lands in a
        # different month is caught instead of being read as "the known GS-4 failure".
        check(binding == EXPECTED_BINDING_RATCHETS,
              f"A1b the binding-ratchet set is exactly the declared one {EXPECTED_BINDING_RATCHETS} "
              f"(observed {binding or 'none'}) - a NEW binding ratchet on the facility basis "
              f"would fail here, not hide behind A1", failures)

        # F2D-4: the 30-minute window is not a measure. Reconfirmed at billing level, on the
        # quantity that is actually billed rather than on a summary statistic.
        p15 = max(profile.kw15)
        p30 = max(profile.kw30)
        check(1.0 <= p15 / p30 <= 1.02,
              f"A2 F2D-4 holds: 15-min / 30-min peak ratio {p15 / p30:.4f} - the longer meter "
              f"interval is worth under 2% and is not a measure", failures)

        # The demand determinant must be seed-independent: the 15-minute peak is the design peak
        # exactly by construction, so every 15-minute NCP charge bills a number no draw can move.
        if not facility_tag:
            check(abs(p15 - 1_000_000.0) <= 0.5,
                  f"A3 the 15-minute peak equals the 1,000 MW design peak exactly "
                  f"({p15:,.2f} kW) - 15-minute demand determinants are seed-independent",
                  failures)
        else:
            # A3 is FALSE on a facility series by construction: Ruling 4's whole content is that
            # the meter peaks above the IT design peak. It is REPLACED, not suspended.
            it_peaks = {round(pr.it_peak_kw, 3) for pr in by_metro.values()}
            check(it_peaks == {1_000_000.0},
                  f"A3F the UNDERLYING IT peak is still exactly 1,000 MW in every metro's "
                  f"facility file ({sorted(it_peaks)}) - the overlay changed the meter, not the "
                  f"computer", failures)
            ratios = {m: by_metro[m].peak_kw / by_metro[m].it_peak_kw for m in by_metro}
            check(all(v > 1.0 for v in ratios.values()),
                  f"A3G every metro's facility peak EXCEEDS its IT peak (Ruling 4): "
                  f"{min(ratios.values()):.4f} to {max(ratios.values()):.4f} x", failures)
            # A3H - the ranking basis must not depend on which basis selects. Within a metro every
            # schedule shares one profile, so the cheapest schedule is the same under $/MWh and
            # $/IT-MWh. Asserted rather than assumed, because the republish depends on it.
            sel_m = {m: r["schedule_code"] for m, r in select_cheapest(results).items()}
            sel_it = {}
            for r in results:
                if not r["qualifies"]:
                    continue
                cur = sel_it.get(r["metro"])
                if cur is None or r["usd_per_it_mwh"] < cur[0]:
                    sel_it[r["metro"]] = (r["usd_per_it_mwh"], r["schedule_code"])
            sel_it = {m: v[1] for m, v in sel_it.items()}
            check(sel_m == sel_it,
                  f"A3H the cheapest qualifying schedule per metro is the SAME under $/metered-MWh "
                  f"and $/IT-MWh ({len(sel_m)} metros) - the republish changes the basis, not the "
                  f"selection", failures)

        # F2D-2: the 4CP determinant is the one number a single draw can move materially.
        dfw = [r for r in results if r["metro"] == "Dallas-Fort Worth"]
        for r in dfw:
            spread = (r["cp4_p95_kw"] - r["cp4_p05_kw"]) / r["cp4_kw"]
            print(f"  NOTE     F2D-2 {r['schedule_code']}: 4CP expected "
                  f"{r['cp4_kw'] / 1000:,.2f} MW, p05-p95 "
                  f"{r['cp4_p05_kw'] / 1000:,.2f}-{r['cp4_p95_kw'] / 1000:,.2f} MW "
                  f"({spread:.2%} of expected), worst single draw "
                  f"{r['cp4_min_kw'] / 1000:,.2f} MW; all-day window "
                  f"{r['cp4_kw_allday'] / 1000:,.2f} MW")

        # Convention 1 (local standard time in, prevailing time for TOU) must be materially
        # applied, not silently inert. Measured two ways: how many intervals the shift
        # reclassifies, and what it is worth in dollars. The F1 gate CANNOT test this - on a flat
        # load the shift is provably neutral, because the only aggregate cell counts it changes
        # are weekend 02:00 in March and weekend 01:00 in November, and every window in the
        # library that contains one contains the other at the same price. So the DST logic needs
        # its own evidence, and this is it.
        global FORCE_NO_DST
        FORCE_NO_DST = True
        try:
            no_dst = {(x["metro"], x["schedule_code"]): x["usd_per_mwh"]
                      for x in (bill_schedule(conn, s2,
                                               (by_metro[s2["metro"]] if by_metro else profile),
                                               lst_index, [])
                                for s2 in conn.execute(SCHEDULE_SQL))}
        finally:
            FORCE_NO_DST = False
        moved = sum(1 for a, b in zip(build_billing_calendar(lst_index, True),
                                      build_billing_calendar(lst_index, False))
                    if a[:3] != b[:3])
        dst_deltas = {k: results_by_key(results)[k]["usd_per_mwh"] - v
                      for k, v in no_dst.items()}
        worst_dst = max(dst_deltas.items(), key=lambda kv: abs(kv[1]))
        phoenix = [d for (m, _), d in dst_deltas.items() if m == "Phoenix"]
        observing = [d for (m, _), d in dst_deltas.items() if METRO_OBSERVES_DST[m]]
        largest_observing = max((abs(d) for d in observing), default=0.0)
        # Three conditions, and the middle one is the load-bearing one. The first draft asserted
        # only that the CALENDAR function can produce a shift, which a tamper that disabled the
        # shift inside the biller passed straight through. What must be true is that the BILL
        # moves: DST-observing metros bill differently with the shift than without it, and
        # Phoenix bills identically.
        check(moved > 20_000 and largest_observing > 1e-9
              and all(abs(d) < 1e-12 for d in phoenix),
              f"A5 the DST shift is applied BY THE BILLER and Phoenix is exempt: it reclassifies "
              f"{moved:,} of {N_INTERVALS:,} intervals, moves the bill by up to "
              f"{largest_observing:.4f} $/MWh in DST-observing metros, and moves Phoenix by "
              f"{max((abs(d) for d in phoenix), default=0.0):.2e} $/MWh", failures)
        print(f"  NOTE     DST materiality: largest effect {worst_dst[0][0]}/{worst_dst[0][1]} "
              f"{worst_dst[1]:+.4f} $/MWh; sum |delta| over all schedules "
              f"{sum(abs(d) for d in dst_deltas.values()):.4f} $/MWh")

        # A5b - the DST boundary itself, restated independently from the statute rather than
        # trusted from nth_weekday(). A one-WEEK slip in the boundary still reclassifies ~22,000
        # intervals, so A5 passes straight through it; only a check that reads the calendar can
        # see it. This check exists because a tamper found that blind spot.
        ds, de = dst_bounds_lst(STUDY_YEAR)
        statutory = (ds.month == 3 and ds.weekday() == 6 and 8 <= ds.day <= 14 and ds.hour == 2
                     and de.month == 11 and de.weekday() == 6 and 1 <= de.day <= 7
                     and de.hour == 1)
        check(statutory,
              f"A5b the DST boundary matches the statute: begins 02:00 standard on the 2nd "
              f"Sunday of March ({ds}), ends 01:00 standard on the 1st Sunday of November "
              f"({de})", failures)

        # A7 - every billing determinant the library actually contains was dispatched on. A
        # determinant that quietly stops being billed - a rate row retyped, a branch that stops
        # firing - is otherwise invisible: the bill just gets smaller.
        in_db = {row[0] for row in conn.execute(
            "SELECT DISTINCT r.billing_determinant FROM rate r JOIN schedule s "
            "ON s.schedule_id = r.schedule_id WHERE s.end_date IS NULL")}
        used = set()
        for r in results:
            used |= set(r["_dispatched"])
        check(in_db <= used,
              f"A7 every billing determinant in the active library was dispatched on "
              f"(in database but never billed: {sorted(in_db - used) or 'none'})", failures)

        # Ruling 1: banded metros.
        # AMENDED IN UNIT 2C-d. The band belongs to the MARKET PRICE, not to the delivery-only
        # label: ComEd Rate BESH is a bundled tariff whose energy price is the hourly PJM
        # ComEd-zone price, so Chicago is banded while remaining bundled. R2 of
        # direction_ph2_chicago_structure_v1.0.md overturned the Phase 1 "ComEd bundled -- no
        # market price" ruling; three metros now carry a parameter.
        banded = sorted({r["metro"] for r in results if r["band_low_usd_per_mwh"] is not None})
        market_metros = sorted({r["metro"] for r in results if r["market_usd"] > 0})
        check(banded == ["Chicago", "Columbus", "Dallas-Fort Worth"] and banded == market_metros,
              f"A4 Ruling 1 bands land on exactly the market-priced metros "
              f"(banded {banded}; market-priced {market_metros})", failures)

        # Q1 ranking gate - carried forward unchanged. It is NOT this unit's to lift.
        qualifying = [r for r in results if r["qualifies"]]
        blocking = sorted({r["schedule_code"] for r in qualifying
                           if r["rider_coverage"] not in Q1_TARGET_LEVELS})
        if blocking:
            print(f"  GATE     Q1 ranking gate ENGAGED: {', '.join(blocking)} below "
                  f"itemised/verified_aggregate. NO metro cost ranking is published.")
        else:
            global Q1_GATE_LIFTED
            Q1_GATE_LIFTED = True
            print("  PASS     Q1 ranking gate LIFTED: every qualifying schedule is at "
                  "itemised or verified_aggregate.")
        print("")

    # Convention 4 (Unit 2D): load factor moves energy charges and hours-use ladders only, never
    # a demand charge. Asserted directly rather than believed: the three variants share a peak of
    # exactly 1,000 MW by construction, so if the convention holds, every schedule's DEMAND
    # component must be bit-identical across them while its ENERGY component must not be.
    if len(variants) > 1:
        print("=" * 96)
        print("CROSS-VARIANT ASSERTION - Unit 2D convention 4"
              + (" (REPLACED on the facility basis: A6F)" if facility_tag else ""))
        print("=" * 96)
        by_sched = {}
        for r in all_results:
            by_sched.setdefault((r["metro"], r["schedule_code"]), []).append(r)
        worst_rel = 0.0
        worst_rel_code = ""
        worst_rel_abs = 0.0
        worst_abs = 0.0
        energy_moves = 0
        for key, rs in by_sched.items():
            d = max(x["demand_usd"] for x in rs) - min(x["demand_usd"] for x in rs)
            base = max(x["demand_usd"] for x in rs)
            worst_abs = max(worst_abs, d)
            if base > 0 and d / base > worst_rel:
                worst_rel, worst_rel_code, worst_rel_abs = d / base, key[1], d
            e = max(x["energy_usd"] + x["market_usd"] for x in rs) \
                - min(x["energy_usd"] + x["market_usd"] for x in rs)
            if e > 1.0:
                energy_moves += 1
        if not facility_tag:
            check(worst_rel <= LF_DEMAND_INVARIANCE_TOL,
                  f"A6 load factor moves no demand charge, to "
                  f"{LF_DEMAND_INVARIANCE_TOL:.2%}: worst demand spread across "
                  f"{len(variants)} variants is {worst_rel:.4%} of the demand component "
                  f"({worst_rel_code}, ${worst_rel_abs:,.0f}/yr; largest absolute spread "
                  f"${worst_abs:,.0f}/yr)", failures)
        else:
            # A6 is REPLACED on the facility basis, and the replacement records a real finding
            # rather than relaxing a tolerance. Unit 2D convention 4 held because the IT peak is
            # exactly 1,000 MW in all three variants by construction, so no demand determinant
            # could move. On the facility basis the billed peak is max(IT x PUE) and lands on a
            # DIFFERENT interval in each variant, so load factor now moves demand charges too.
            # The convention does not survive the overlay. Bounded, not waved through: the spread
            # must be non-zero (or the overlay is inert) and under FACILITY_LF_DEMAND_TOL.
            check(worst_rel > 0.0,
                  f"A6F-a on the FACILITY basis load factor DOES move demand: worst spread "
                  f"{worst_rel:.4%} ({worst_rel_code}) is non-zero, so Unit 2D convention 4 does "
                  f"not survive the overlay - a zero here would mean the overlay was inert",
                  failures)
            check(worst_rel <= FACILITY_LF_DEMAND_TOL,
                  f"A6F-b and the breakage is BOUNDED: {worst_rel:.4%} of the demand component "
                  f"({worst_rel_code}, ${worst_rel_abs:,.0f}/yr; largest absolute spread "
                  f"${worst_abs:,.0f}/yr) is inside the declared "
                  f"{FACILITY_LF_DEMAND_TOL:.2%}. EVERY Phase 4 measure that changes load factor "
                  f"now moves a demand charge as well as an energy charge.", failures)
        check(energy_moves == len(by_sched),
              f"A6b load factor DOES move the energy charge, as it must - a demand component "
              f"that never moves would otherwise be consistent with a broken variant loader "
              f"({energy_moves} of {len(by_sched)} schedules move)", failures)
        print("")

    return all_results, all_monthly


# =================================================================================================
# CLI
# =================================================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Cost engine v1.2 (Unit 2E machinery; Unit 4A facility basis).")
    parser.add_argument("--db", default=None)
    parser.add_argument("--f1-only", action="store_true",
                        help="Run the F1 regression gate and stop.")
    parser.add_argument("--variants", default="lf090,lf082,lf095",
                        help="Comma-separated Unit 2D profile variants. Default: all three "
                             "(lf090 is the Unit 2D baseline; lf082 and lf095 are its "
                             "documented sensitivity, and running all three is what makes "
                             "assertion A6 possible).")
    parser.add_argument("--facility-basis", default=None,
                        help="Unit 4A PUE stamp label, e.g. plant_derived_4a. When given, each "
                             "schedule is billed against ITS OWN metro's facility series "
                             "(era_facility_profile_<metro>_<variant>_15min.csv) instead of the "
                             "single IT series, and the file's stamp must match this label.")
    parser.add_argument("--profile-dir", default=None,
                        help="Where the profile CSVs live. Overridable so an alpha excursion can "
                             "be billed out of a scratch directory without writing to the "
                             "project copy.")
    parser.add_argument("--results-csv", default=None)
    parser.add_argument("--monthly-csv", default=None)
    parser.add_argument("--f1-csv", default=None)
    parser.add_argument("--acceptance-csv", default=None,
                        help="F1 regression target. Overridable so a TRIAL database can be "
                             "gated against its own acceptance output without touching the "
                             "project copy. It is not an override of the gate itself -- the "
                             "gate still runs, still first, and still has no off switch.")
    args = parser.parse_args()

    global DB_FILE, OUT_RESULTS, OUT_MONTHLY, OUT_F1, ACCEPTANCE_CSV, PROFILE_DIR
    if args.profile_dir:
        PROFILE_DIR = Path(args.profile_dir)
    if args.acceptance_csv:
        ACCEPTANCE_CSV = Path(args.acceptance_csv)
    if args.db:
        DB_FILE = Path(args.db)
    if args.results_csv:
        OUT_RESULTS = Path(args.results_csv)
    if args.monthly_csv:
        OUT_MONTHLY = Path(args.monthly_csv)
    if args.f1_csv:
        OUT_F1 = Path(args.f1_csv)

    if not DB_FILE.exists():
        print(f"ERROR: {DB_FILE.name} not found.")
        sys.exit(1)
    # The engine is READ-ONLY with respect to the tariff library, and says so at the connection
    # rather than in a docstring. One consequence has to be handled explicitly: if a stale
    # rollback journal is sitting beside the database, SQLite treats it as HOT, tries to roll it
    # back, and cannot - because rolling back is a write. This is not hypothetical; a stale
    # `era_rates.db-journal` from the Unit 2B fuse-mount incident sat beside the database for
    # three units without anyone noticing, because every script before this one opened the
    # database read-write and silently rolled it back on open.
    #
    # Refuse rather than reopen read-write. A hot journal means the database MAY be mid-transaction
    # and a cost engine has no business deciding that for itself.
    journal = DB_FILE.with_name(DB_FILE.name + "-journal")
    if journal.exists() and journal.stat().st_size > 0:
        print(f"ERROR: {journal.name} is present beside {DB_FILE.name}.")
        print("SQLite treats it as a hot rollback journal and this engine opens the database")
        print("READ-ONLY, so it cannot roll it back. Two possibilities, and they are different:")
        print("  * a write is genuinely in progress in another process - wait for it; or")
        print("  * it is stale debris from an interrupted write (a known one exists in this")
        print("    project's history: the Unit 2B fuse-mount incident, 2026-08-21).")
        print("Verify the database with era_acceptance_v1.2.py, then move the journal aside.")
        sys.exit(1)

    conn = sqlite3.connect(f"file:{DB_FILE}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    version = conn.execute("PRAGMA user_version").fetchone()[0]
    if version < REQUIRED_SCHEMA_VERSION:
        print(f"ERROR: {DB_FILE.name} is at user_version {version}; the engine reads "
              f"rate.billing_determinant, which schema v1.3 introduces.")
        sys.exit(1)

    print("era_engine (Cost Engine v1.2, Unit 4A) - billing machinery unchanged since v1.0")
    print(f"Database: {DB_FILE.name} (schema v{version}, opened read-only)")
    print(f"Profiles: {PROFILE_DIR}")
    if args.facility_basis:
        print(f"Basis:    FACILITY, PUE stamp {args.facility_basis!r} "
              f"(direction_ph4_scenario_layer_v1.0.md Rulings 1-6)")
    else:
        print("Basis:    IT only, implied PUE 1.00 (the Phase 2 metered basis)")
    print("")

    lst_index = build_lst_index()
    dst_start, dst_end = dst_bounds_lst(STUDY_YEAR)
    print(f"Time basis: profile index is local STANDARD time; TOU windows are mapped on the "
          f"local PREVAILING clock.")
    print(f"  CY{STUDY_YEAR} DST on the standard clock: {dst_start} to {dst_end}. "
          f"Phoenix does not observe it.")
    print("")

    gate_ok, gate_failures = run_f1_regression(conn, lst_index)
    if not gate_ok:
        conn.close()
        sys.exit(1)
    if args.f1_only:
        conn.close()
        print("--f1-only: gate passed, no profile read.")
        sys.exit(0)

    failures = []
    variants = [v.strip() for v in args.variants.split(",") if v.strip()]
    results, monthly = run_profiles(conn, lst_index, variants, failures,
                                    facility_tag=args.facility_basis)

    for r in results:
        r["dispatched_determinants"] = "|".join(r.pop("_dispatched"))
    with open(OUT_RESULTS, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(results[0].keys()))
        w.writeheader()
        w.writerows(results)
    with open(OUT_MONTHLY, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(monthly[0].keys()))
        w.writeheader()
        w.writerows(monthly)
    print(f"Results  -> {OUT_RESULTS.name} ({len(results)} rows)")
    print(f"Monthly  -> {OUT_MONTHLY.name} ({len(monthly)} rows)")
    print(f"F1 gate  -> {OUT_F1.name}")
    print("")
    print("STANDING CAVEATS ON EVERY PROFILE FIGURE ABOVE")
    if args.facility_basis:
        print(f"  1. FACILITY basis, PUE stamp {args.facility_basis!r}. The PUE amplitude is a")
        print("     DERIVED quantity from a stated cooling-plant basis, not a measurement; see")
        print("     era_ph4a_plant_basis.md for its six cited parameters and the excursion in")
        print("     alpha across every one of them. $ per IT-MWh is the siting basis; $ per")
        print("     metered-MWh is the tariff basis; both are published and neither supersedes")
        print("     the other.")
    else:
        print("  1. PUE overlay is GATED. These bills price the IT series at an implied PUE of")
        print("     1.00 and are a STRICT LOWER BOUND. Metros are not yet comparable on facility")
        print("     cost, because PUE differs by climate. See brief_ph2_unit2a_pue_amplitude_v1.0.")
    if Q1_GATE_LIFTED:
        print("  2. The Q1 ranking gate is LIFTED (Unit 2C-d): every qualifying schedule is at")
        print("     itemised or verified_aggregate. A ranking may be published, subject to the")
        print("     other caveats here and to the parameter bands.")
    else:
        print("  2. The Q1 ranking gate is engaged. No ranking is published.")
    print("  3. A transmission-voltage selection transfers substation and interconnection capex")
    print("     to the customer; the tool prices the tariff only.")
    print(f"  4. 4CP: {CP4_SOURCE_NOTES}")

    conn.close()
    if failures:
        print("")
        print(f"{len(failures)} engine assertion(s) FAILED.")
        sys.exit(1)
    print("")
    print("All engine assertions PASS.")


if __name__ == "__main__":
    main()
