# ERA — Electrical Rate Analysis

A data center siting tool that ranks US metropolitan areas by delivered electricity cost.
Utility tariffs are normalised into a SQL database, a synthesised 15-minute load profile for a
giga-scale campus is billed against every qualifying schedule, and the resulting all-in $/MWh is
compared across metros. Eight metros are modelled: Dallas-Fort Worth, Columbus, Austin, Chicago,
Northern Virginia, Phoenix, Atlanta, San Jose.

**Live page:** https://era.bradmachado.com/era_ph5_dashboard.html

Author: Brad Machado · Illinois School of Architecture (M.Arch)

**Status:** Phases 1, 2, 4 and 5 are closed. Phase 6 (portfolio packaging and the carried model
work) is open. This repository carries the Phase 5 deliverable and the chain that verifies it.

---

## The dashboard page

`era_ph5_dashboard.html` is the Phase 5 deliverable: **one self-contained file** that opens from disk
in any browser, with no server, no network fetch and no library. Python's standard library writes
every mark as inline SVG, so what the browser paints is what the build wrote — which is what lets an
automated gate read the artefact itself rather than a spec that drives a runtime. Six views: V1 the
ranking by cost per IT-MWh, V2 the mitigation waterfall per metro, V3 the five mitigation channels,
V4 the weather stations, V5 the market bands and published pairs, V6 the caveats table the header
links to. The page carries **no typed figure**: every number on it is drawn from an embedded grain
cell and credited to it, and the gate re-checks all 289 of them against those cells on every run.
Two controls (metro, basis) switch between states that are pre-rendered in the markup, so the page
shows its saved state with JavaScript disabled.

**To rebuild it** — Python 3.10 or newer, standard library only for the last two steps, from the
project folder in Anaconda PowerShell:

```powershell
python era_ph5_extract.py     # the four grain CSVs + the manifest, from era_rates.db (needs pandas)
python era_ph5_build_html.py  # era_ph5_dashboard.html, from those CSVs
python era_ph5_page_gate.py   # 75 gates; exit 0 means the page is accepted
```

There is no second copy of the data to go stale: the page embeds the grains and the gate proves the
embedded copy equals the CSVs on disk. The build is deterministic across interpreters — 3.10, 3.11
and 3.13 produce the same bytes — and `era_ph5_page_gate.py` rebuilds the page in a scratch directory
and compares it to the file on disk, so a hand-edited page fails. `era_ph5_page_tamper.py` runs 29
declared positive controls that each fire a named gate and nothing else. `renders/era_ph5_v*.png` are
2× screenshots of the six views, committed as portfolio artefacts.

**One caveat on step 1.** Re-running the extract rewrites `era_ph5_grains_manifest.json` with a fresh
`written_utc` stamp, and the page embeds the manifest, so the rebuilt page differs from the committed
one in exactly those five timestamps and nowhere else. The four grain CSVs are byte-identical.

---

## Running the gates from a clone

Everything below is Python **3.10 or newer, standard library only** — no third-party package is
needed to run any gate or tamper suite. The commands are identical on Windows, macOS and Linux;
use `python` or `python3` as your installation names it. Run them from the root of a clone.

```
python era_ph5_grain_gate.py     # 29 gates over the four grain CSVs and the manifest
python era_ph5_page_gate.py      # 75 gates over the page; exit 0 means the page is accepted
python era_ph5_report_gate.py    # 58 gates over the report; exit 0 means the report is accepted
```

The two tamper suites prove the gates are connected rather than merely quiet. Each case injects
one declared fault and asserts that a named gate fires and nothing else does:

```
python era_ph5_page_tamper.py    # 29 declared positive controls
python era_ph5_report_tamper.py  # 6 declared positive controls
```

A check that has never failed has not been shown to work. That is the discipline this repository
exists to show, and it is why the tamper suites ship alongside the gates.

`.gitattributes` in this repository is the single line `* -text`. Git performs no line-ending
normalisation on commit or checkout, so every file's md5 is the same in any clone on any platform
as it is in the working copy the pins were measured on. The grain gate compares the four CSVs
against the md5s recorded in `era_ph5_grains_manifest.json`; without that attribute, a checkout
that rewrote line endings would fail the gate for a reason that has nothing to do with the data.

## What this repository is, and is not

This is a **curated public subset** of a private working repository. It carries the Phase 5
deliverable, the chain that builds and verifies it, and the model files needed to read the work:
the database, the schema, the engine and the extract. It does not carry the working record —
briefs, read logs, other direction files, run logs, database snapshots — and it does not carry
any third-party tariff document or bulk dataset.

A fresh clone of **either** repository will not run the model end-to-end, for the same reason in
both cases. In the words of the private repository's README:

> Consequence: **a fresh clone will not run end-to-end.** The database, the schema, the engine,
> and every verification transcript are versioned; the bulk inputs are not.

What a clone of this repository *can* do is open the page, rebuild it from the shipped grains,
and run all five harnesses to completion. That is the claim, and the gates are how you check it.

## Sources

Rate schedules are normalised from tariffs on file with each utility's regulator. No tariff
document is redistributed here; each is cited.

- **Commonwealth Edison Co** (Chicago, IL) — ILL. C.C. No. 10 — Illinois Commerce Commission
- **AEP Ohio (Ohio Power Co)** (Columbus, OH) — P.U.C.O. No. 22 — Public Utilities Commission of Ohio
- **Pacific Gas & Electric Co** (San Jose / Bay Area, CA) — CPUC Advice Letter 7921-E, Schedule E-1 — California Public Utilities Commission
- **Oncor Electric Delivery Company LLC** (Dallas-Fort Worth, TX) — Tariff for Retail Delivery Service, approved by the Public Utility Commission of Texas
- **Virginia Electric & Power Co** (Northern Virginia, VA) — Virginia State Corporation Commission
- **Georgia Power Co** (Atlanta, GA) — Georgia Public Service Commission
- **Arizona Public Service Co** (Phoenix, AZ) — Arizona Corporation Commission
- **Austin Energy** (Austin, TX) — municipally owned; rates approved by Austin City Council

Each schedule's `source_url` and effective date are recorded in `era_rates.db`; a sources manifest
with regulator citations follows in Unit 6I.

## Attribution

```
Utility rate data: Utility Rate Database, Zimny-Schmitt, D. and Huggins, J.,
  NREL / Open Energy Data Initiative. CC BY 4.0. https://data.openei.org/submissions/5
HPC facility PUE data: Clark, S. and Strelka, J., HPC Facility Power Usage
  Effectiveness (PUE) Data. CC BY 4.0. https://data.openei.org/submissions/8616
Weather: Lawrie, L.K. and Crawley, D.B. (2022), "Development of Global Typical
  Meteorological Years (TMYx)." climate.onebuilding.org
Tariff sources: see §Sources above - each schedule's regulator-filed origin and
  utility URL, with effective dates, are recorded in era_rates.db.
```

GenAI workload power profiles: Vercellino et al., "Measurement of Generative AI Workload Power
Profiles for Whole-Facility Data Center Infrastructure Planning," arXiv:2604.07345 (2026).
*Dataset catalog entry and hosting organisation: pending verification (gate G5).*

The two Utility Rate Database files redistributed here — `era_urdb_selected_raw.json` and
`era_urdb_candidates_v1.0.csv` — are used under the CC BY 4.0 grant on the submission cited above.
No other third-party file is redistributed in this repository.

## Licence

Code (`.py`, `.sql`) is released under the MIT License — see `LICENSE`. Documentation, figures,
the dashboard page, the report and the derived data files are released under CC BY 4.0 — see
`LICENSE-CONTENT.md`. Third-party tariff documents and datasets are **not** redistributed here;
they are cited in §Sources and §Attribution and remain under their own terms.
