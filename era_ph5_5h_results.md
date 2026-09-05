# Unit 5H results — `era_ph5_5h_results.md`

Append-only across Units 5H-0 … 5H-5 (`direction_ph5_html_v1.0.md`, one § block per unit). Every
declared expectation is written BEFORE the run it predicts; a run result is appended below its
declaration and never edits it. Container runs are the session's checks; the committed logs are the
runs from Brad's shell (F5B-9).

---

# Unit 5H-0 — retirement, the grain-gate move, the page skeleton, the positive controls

Session opened 2026-09-04 ~23:04 UTC. Execution session (Tier 2). Direction files read: `direction_ph5_html_v1.0.md`
(whole), `direction_ph5_tableau_v1.0.md` (§0, P5-3, P5-4, P5-5, V1–V6 text), `direction_session_protocol_v1.2.md`.

## §0 — What this session checked before anything else (step 1)

`device_bash` probe 23:04:58 UTC: **ALIVE** (VM Python 3.10.12; 327 entries in the project root). Everything
below was read off the mount by this session; nothing was taken from a prompt or from memory as fact.

| artefact | measured | matches the ruling's §0.1 |
| --- | --- | --- |
| `direction_ph5_html_v1.0.md` | md5 `d9f17e127fa8ad7ace74d9c15630da4a`, 23,089 B | yes |
| `direction_ph5_tableau_v1.0.md` | md5 `43b3cfe7b975acd03ec212082f140bd0` | (not stated there) |
| `direction_session_protocol_v1.2.md` | md5 `ca381c4d5da9d52dc137b1e5c4db1a7c` | (not stated there) |
| `era_rates.db` | md5 `1c72e7a1b32c99a650d2e1fba17ae21e` | yes |
| `era_ph5_metro.csv` (G1) | md5 `84fe4dbff836a169ec29d9f38281b683`, 7,776 B | yes — E-1.4 pin |
| `era_ph5_stack.csv` (G2) | md5 `3e8825ac3755a67fdcd882c32ba6da2d`, 7,494 B | yes — E-1.4 pin |
| `era_ph5_month.csv` (G3) | md5 `f5b3638a2f9cc942b8d6835014043048`, 84,637 B | yes — E-1.4 pin |
| `era_ph5_caveat.csv` (G4) | md5 `fc1fa4b10c5f536faeb5850647317db7`, 9,097 B | yes — E-1.4 pin |
| `era_ph5_grains_manifest.json` | md5 `d28ed3404fab100d8bb31d0e0bc95323`, `written_utc 2026-09-04T22:18:28Z`, `db_md5 1c72e7a1…`, `user_version 14`; the four grain md5s/rows/bytes inside it equal the four CSVs above | yes |
| `era_ph5_extract.py` | md5 `5737ec292b6a6376e46c99407925246b` (= manifest `script_md5`) | yes |
| `era_ph5_dashboard.twb` (RETIRED) | md5 `20dcb01d13ee609861e9fbd8d0a22abb`, 220,761 B — the E-5.7 refresh never ran | yes |
| `era_ph5_workbook_gate.py` (RETIRED) | md5 `689b1354db45c5d88be3b3494dd71170`, 69,907 B | yes |
| `era_ph5_style_v1.0.md` | md5 `88704aa9b7e2e1c72bc1f567b2559ec0` — 13 hex tokens, sizes {11,13,16,22,34}, one family | — |
| `era_ph5_dictionary_v1.0.md` | md5 `41d01c8472725ed704fb322541d51275` | — |
| `era_ph5_5by_results.md` | md5 `bbd9257c2780264f8d784010b03d78ca`, 12,244 B; §0–§4b written; §5/§6/§7 are EMPTY headings | yes |
| 5H files (`era_ph5_5h_results.md`, `era_ph5_grain_gate.py`, `era_ph5_build_html.py`, `era_ph5_page_gate.py`, `era_ph5_page_tamper.py`, `era_ph5_dashboard.html`) | none present before this session | — |

**Two things the ruling states that the folder does NOT confirm — recorded here, not repaired:**

- **§0-a. Group D has 29 gate ids, not 26.** `era_ph5_workbook_gate.py` `group_d()` emits D0a–D0f (6), D1a, D2a–D2d (4),
  D3a, D4a–D4b, D5a–D5b, D6a–D6b, D7a–D7b, D8a–D8c (3), D9a–D9b, D10a, D11a–D11c (3) = **29**. The committed Brad's-shell
  log `era_ph5_5b_gate_run.log` carries **29 `[D]` PASS lines**. 26 was 5B's count; 5B-x added D11a–D11c and the ruling's
  "26" predates that. The ruling says *"any difference is a finding, not a fix"* — so the move carries all 29 and the
  count is finding F5H0-1 (§6).
- **§0-b. Brad's-shell Python "3.13.5 … verbatim in its results file" is NOT in `era_ph5_5by_results.md`.** The string
  `3.13.5` occurs on the mount only in `direction_ph5_html_v1.0.md`. 5B-y's §5 heading reads *"(to be appended, verbatim)"*
  and is empty. Project memory carries the P1 line; the file does not. This session did not observe P1 and does not
  assert it. The 5H gate prints `sys.version` in its log header, so Brad's committed `era_ph5_5h_gate_run.log` becomes
  the on-disk measurement of his interpreter. Finding F5H0-2 (§6).

## §1 — Declared expectations, written before any run

### §1.1 — Step 2, the 5B-y §5 note

One block is inserted under the existing empty heading `## §5 — Probes P1 / P2 and the X13c branch (to be appended,
verbatim)` in `era_ph5_5by_results.md`. No other byte of that file changes: the §0–§4b text, and the §6/§7 headings,
are byte-identical before and after. **Declared exactly:** the file is 12,244 B; bytes [0, 12122) — everything up to
and including the §5 heading line and its blank line — are unchanged; bytes [12122, 12244) — the §6 and §7 heading
lines — are unchanged and remain the file's tail; the inserted block sits between them and is the ONLY difference.

### §1.2 — Step 3, the group-D move → `era_ph5_grain_gate.py`

- The moved text is `group_d()`, `Gate`, `num()`, `load_csv()` and the constants they reference (`GRAINS`, `METROS`,
  `D_ARGMAX_KWH`, `D_ARGMAX_TOTAL`, `D_ARGMAX_KW`, `D_RATCHET_MONTHS`, `D_PORTFOLIO_BASELINE_USD`, `D_EXCLUDED_BAND_USD`,
  `D_CHANNELS`, `V3_ORDER`, `CENT`), copied character-for-character out of `era_ph5_workbook_gate.py` md5 `689b1354…`.
  **Declared: a `diff` of each moved block against the retired file's text is empty.** The retired file is read, never
  written.
- **Declared: standalone `python era_ph5_grain_gate.py --project .` on the pinned grains → 29 PASS / 0 FAIL, and the
  29 result lines (status, group, id, message) are byte-identical to the 29 `[D]` lines of `era_ph5_5b_gate_run.log`.**
  (The ruling's "26/26" is the count finding above; identical-text is the test that matters and it is declared exact.)
- Tamper cases on the standalone grain gate, declared firing sets (exact, at gate-id level, relative to a clean run):
  **W15** (twelve months reversed within each metro-stage block) → `{D2a, D2b, D2c, D3a}`;
  **W16** (Chicago mitigated monthly level × 1.000001) → `{D5a, D6a}`;
  **W24** (Columbus `usd_per_it_mwh` + 200.0, the 5B-x article) → `{D11a, D11b, D11c}`.
  X13a's slot is gone from these sets: the freshness duty is H13 in the page gate and is exercised there (§1.4).

### §1.3 — Step 4, the v0 page and the page gate

**Build (`era_ph5_build_html.py` v0, stdlib only, 3.10-compatible).** One file `era_ph5_dashboard.html`, written
atomically (temp then `os.replace`). Contents: well-formed XML-parseable HTML5; `<style>` with the thirteen tokens as
CSS custom properties read out of `era_ph5_style_v1.0.md` at build time (`--era-surface` … `--era-ink`), the five type
sizes, one family, `--era-base: 8px`, `--era-margin: 48px`, `--era-gutter: 24px`; a header (title / subhead / caption,
the caption carrying the one-click anchor `href="#V6"` — P5-3); the two controls as `<fieldset data-control="p. Metro"
data-saved="Columbus">` (eight radios in `METROS` order, Columbus `checked`) and `<fieldset data-control="p. Basis"
data-saved="IT">` (radios IT `checked`, Metered); six empty `<section data-view="V1".."V6" data-status="build-incomplete">`
slots; the manifest embedded verbatim as `<script type="application/json" id="era-manifest">`; the four grains embedded
as `<script type="application/json" id="era-grain-<stem>">` `{"grain","file","columns","rows"}` with every cell the CSV
string; one inline `<script>` (no `src`) that toggles `[data-state-metro]` / `[data-state-basis]` groups and does nothing
when there are none. JSON is serialised `sort_keys=True, ensure_ascii=True` with the characters `&`, `<`, `>` written as the JSON escapes `\u0026`, `\u003c`, `\u003e` so the same bytes parse as
XML text and as JSON. No timestamp is written by the build; the only time in the
page is the manifest's own `written_utc`. **Declared: two builds are byte-identical; the page is under 4 MB (estimate
150–300 KB, weak).**

**Row keys for `data-src="<grain-stem>:<row-key>:<column>"`** (declared here, asserted by T2 from 5H-1 on): G1 `metro`;
G2 `metro|component_id`; G3 `metro|stage|month`; G4 `caveat_id`.

**Page gate (`era_ph5_page_gate.py`) — gate ids, and the declared tally on the v0 page:**

| group | ids | declared on v0 |
| --- | --- | --- |
| D | the 29 via `era_ph5_grain_gate.group_d` | 29 PASS |
| H | H1 page present, single file, parses as XML; H2 no `<script src>`, `<link>`, `<iframe>`, `@import`, `url(` other than `data:`, no `http(s)://` or `//` fetchable reference, every `<img>` is `data:`; H3 manifest block present, JSON, four grains with `md5`/`rows`/`cols`; H4 four grain blocks present, JSON, each block's row count and column count equal the EMBEDDED manifest's `rows`/`cols`; H5 determinism — the build run twice into scratch from the project's inputs gives identical bytes; H6 reproduction — that scratch build equals the page on disk byte for byte; H7 size ≤ 4 MB | H1–H7 PASS |
| H13 | H13a embedded manifest == `era_ph5_grains_manifest.json` on disk (whole document equal); H13b for each grain, disk manifest `md5`/`rows` == md5/rows of the CSV on disk; H13c embedded rows == the CSV rows as `group_d` parses them (list of dicts, all four). Manifest absent → H13a AND H13b FAIL, never SKIP | H13a–c PASS |
| P | P1 both controls exist; P2 p. Metro saved state read from markup (`checked` radio AND `data-saved`) == Columbus; P3 p. Basis saved == IT (swap OFF); P4 p. Metro options == the eight `METROS` in order; P5 p. Basis options == [IT, Metered]; P6 V2 has 8 pre-rendered `[data-state-metro]` groups, Columbus the one not hidden; P7 V1 has 2 pre-rendered `[data-state-basis]` groups, IT the one not hidden | P1–P5 PASS; **P6, P7 SKIP-OK** ("slot V2/V1 declares build-incomplete") |
| S | S0a/S0b/S0c the token file (13 hex, five sizes, one family — read at run time, HEX not name); S1 every hex in the page (CSS text, `fill`/`stroke`/`color`/`stop-color`/`style` attributes) ∈ the 13, count ≥ 1; S2 every `font-size` (CSS and attribute) ∈ {11,13,16,22,34} px, count ≥ 1; S3 exactly one `font-family` and it is the token family; S4 CSS declares base 8 px, margin 48 px, gutter 24 px; S5 every `<svg>` `width`/`height` a multiple of 8 | S0a–S4 PASS; **S5 SKIP-OK** ("0 svg elements; slots build-incomplete") |
| T | T1 the count of text-bearing elements (outside `<script>`/`<style>`) whose own text contains a figure token (`\d{3,}`, `\d+[.,]\d+`, `\$\s?\d+`, or the whole text a number) and that carry NO `data-src` is **0**, with ≥ 1 text element scanned (else FAIL, vacuous); T2 every `data-src` resolves to an existing grain:row:column and the shown number equals the cell to the precision shown | T1 PASS (0 uncredited of 0 numeric, N ≥ 8 scanned); **T2 SKIP-OK** ("0 credited figures on v0") |
| V | V1a svg exists; V1b 8 bar groups in `rank` order; V1c bars bound to `usd_per_it_mwh` (parts remainder + mitigation) · V2a exists; V2b 8 metro groups, each following `waterfall_order` with G2's row count; V2c the three excluded siblings present, `--era-muted` fill + hairline · V3a exists; V3b five channels in `V3_ORDER` (rider first) · V4a exists; V4b 8 points · V5a exists; V5b intervals span `band_low`/`band_high` · V6a table exists; V6b 21 rows by `sort_rank`, unpriced above limitations, `C-FERC-*` first with no dollar; V6c a `href="#V6"` anchor exists in the header | **FAIL build-incomplete ×14**: V1a V1b V1c V2a V2b V2c V3a V3b V4a V4b V5a V5b V6a V6b; **V6c PASS** (the anchor is in v0's header) |
| B | B1 V1's saved (not hidden) state is the IT basis, axis field `usd_per_it_mwh`; B2 the metered-swap state's remainder is 0 and its label says so (F5B-2); B3 the metered band-crossing literals `0.9742` / `0.97` never appear as page text (F5A-4, negative half); B4 any shown band-crossing figure carries `data-src` to G4 `C-BAND-25` (the FACILITY figure) | **FAIL build-incomplete ×3**: B1 B2 B4; **B3 PASS** |

**Declared tally on v0:** `PASS` = 29 (D) + 7 (H) + 3 (H13) + 5 (P) + 7 (S: S0a,S0b,S0c,S1,S2,S3,S4) + 1 (T1) + 1 (V6c) + 1 (B3)
= **54 PASS**; **17 FAIL**, all labelled `BUILD-INCOMPLETE`, set exactly {V1a V1b V1c V2a V2b V2c V3a V3b V4a V4b V5a V5b
V6a V6b B1 B2 B4}; **4 SKIP-OK** {P6, P7, S5, T2}; **0 SKIP-BLIND**. Exit code 1 (FAILs exist — the v0 page is not
accepted, by design). Runtime on the VM under 45 s (estimate 2–6 s, weak — the rebuild for H5/H6 runs the build twice).

### §1.4 — Step 5, the positive controls (`era_ph5_page_tamper.py`), declared before the suite runs

Mechanics: for each case the harness copies the project's four grains + manifest + style md + dictionary into a temp
project, builds the v0 page there (clean), applies the case, runs the page gate on the temp project, and reports
**fired = FAIL set(case) − FAIL set(clean baseline)**. The baseline FAIL set must equal the 17 declared above or the
suite aborts NOT CONNECTED. Run order: **W01 first** (F5B-3), then the W-cases in id order, controls N last; a
`--cases` list that starts with a control is refused.

| case | article | declared firing set (exact, gate ids) | also asserted |
| --- | --- | --- | --- |
| **W01** | V1 rebound to `mitigated_annual_usd` | **NOT RUNNABLE in 5H-0** — V1 is build-incomplete; declared, printed, not counted as a miss. Becomes the leading positive in 5H-1 (fires V1c alone). | — |
| **W15** | grain gate standalone, months reversed | {D2a, D2b, D2c, D3a} | — |
| **W16** | grain gate standalone, Chicago mitigated × 1.000001 | {D5a, D6a} | — |
| **W24** | grain gate standalone, Columbus `usd_per_it_mwh` + 200 | {D11a, D11b, D11c} | — |
| **W30** (ruling's a) | one embedded md5 edited in the page copy (G1's, last hex digit flipped) | **{H13a, H6}** | H5 PASS; T1, S1 PASS |
| **W31** (ruling's b) | one CSV cell perturbed on disk in the temp project — Columbus `usd_per_it_mwh` + 200; page untouched | **{H13b, H13c, D11a, D11b, D11c, H6}** | H13a PASS |
| **W32** (ruling's c) | literal `47.67` typed into the header caption | **{T1, H6}** | S1 PASS |
| **W33** (ruling's d) | `style="color:#FF0000"` on the title element | **{S1, H6}** | T1 PASS |
| **W34** (ruling's e, first half) | the page rebuilt twice in the temp project (clean inputs) | **∅** — and the harness's own byte comparison of the two builds is EQUAL; H5 and H6 PASS | — |
| **W35** (ruling's e, second half) | the temp project's `era_ph5_style_v1.0.md` has `--era-accent-400` `#4585C4` → `#4585C5`; the page is rebuilt from it; the gate reads the ORIGINAL tokens via `--style <project>/era_ph5_style_v1.0.md` | **{S1}** — H5 PASS and H6 PASS (deterministic given its inputs) | S0a PASS (13 tokens still) |
| **N01** | clean copy, nothing changed | ∅ | — |

**On the ruling's word "alone".** The ruling declares (a) → "H13 alone", (c) → "T alone", (d) → "S alone". This gate has an
H6 that rebuilds the page from the inputs on disk and compares bytes; **every edit to the page or to an input that the
build reads moves H6 by construction** — that is what a reproduction gate is. So the declared sets above carry H6 beside
the ruling's gate for W30–W33, and the ruling's expectation is met at the granularity the ruling named (H13 / T / S fire,
nothing else in their own or any other group). This is written here BEFORE the run and is finding F5H0-3, not a
loosening: no gate is dropped to make a set smaller. If H6 turns out NOT to fire on one of W30–W33 that is a MISS.

**W35's `--style` override** exists for this control only (as `--branch`/`--ruling` did in the retired gate): it lets the
gate read the committed tokens while the build in the temp project read altered ones. Without it S would read the altered
file and pass, and the control would prove nothing.

### §1.5 — Checkpoint conditions (from the ruling), restated as things this session will measure

1. grain gate 29/29 standalone (ruling: 26/26 — F5H0-1) with lines identical to the committed 5B log's D lines;
2. page gate on v0: FAIL set == the 17 build-incomplete ids and nothing else; SKIP-OK == {P6, P7, S5, T2}; no SKIP-BLIND;
3. controls fired on their declared sets; W01 printed NOT RUNNABLE first; control-first refused;
4. §5 note present in `era_ph5_5by_results.md`, nothing else in it changed;
5. `era_ph5_5h_gate_run.log` and `era_ph5_5h_tamper_run.log` exist FROM BRAD'S SHELL — this session cannot produce
   them; it hands Brad the commands and the checkpoint stays OPEN on that item until he runs them (a prompt may
   instruct, not assert);
6. `era_rates.db` md5 `1c72e7a1b32c99a650d2e1fba17ae21e` unchanged after every run.

## §2 — Step 2 result: the 5B-y §5 note — DECLARATION HIT (23:19 UTC)

`era_ph5_5by_results.md` 12,244 B → 14,434 B (md5 `bbd9257c…` → `1d353ad447fdd3d590bd84df73e02287`). Measured on the mount
after the write: bytes [0, 12122) md5 `67c30fa34251ca18a26692622de666df` before AND after; the 122-byte tail (§6, §7
headings) md5 `529710100c34da299e7ebd8de3033949` before AND after; heading count 9 → 9. The inserted block is the only
difference. Written with `device_commit_files` against the file's staged mtime (a newer edit would have been refused).

## §3 — Step 3 result: the group-D move — DECLARATION HIT, with the count finding (23:21 UTC)

- `era_ph5_grain_gate.py` md5 `7c1cf9a3f43d68e49acd48751636e1c2` (377 lines). Its four MOVED blocks were compared on the
  mount against `era_ph5_workbook_gate.py` (`689b1354…`, unchanged) at the line ranges each block names — GRAINS 111–116,
  D constants 152–184, Gate/num/load_csv 227–257, group_d 263–483: **ALL IDENTICAL**, character for character.
- Standalone on the mount, VM Python 3.10.12, 0.035 s: **RESULT 29 PASS 0 FAIL (group D, 29 gates)**. The 29 result lines
  are **byte-identical to the 29 `[D]` lines of the committed `era_ph5_5b_gate_run.log` modulo line terminators** — the
  committed log is CRLF (Windows text-mode append); `diff --strip-trailing-cr` is empty. F5H0-1 stands: 29, not 26.
- Grain-gate tampers (§4 suite, kind `grain`): **W15 → {D2a, D2b, D2c, D3a}; W16 → {D5a, D6a}; W24 → {D11a, D11b, D11c} —
  ALL AS DECLARED**, container and mount.

## §4 — Step 4 result: the v0 page and the page gate — DECLARATION HIT (23:22 UTC)

- `era_ph5_build_html.py` md5 `f3530fb8218ce460973b232334c98b0a` (297 lines); `era_ph5_page_gate.py` md5
  `c6365865846ef8b3cd2201b6423f7245` (780 lines). Stdlib only; both import `era_ph5_grain_gate`; the gate imports the build
  for H5/H6.
- Build on the mount from the project folder (VM 3.10.12, 0.053 s): `era_ph5_dashboard.html` **137,920 B, md5
  `5e084f91b756ab4b29b31046f09d1884`** — the SAME bytes the container (Python 3.11.15) produced. Two interpreters, one page.
  Size estimate (150–300 KB, marked weak) was high; 135 KB.
- Page gate on the mount (0.123 s, exit 1 by design): **RESULT 54 PASS 17 FAIL 0 SKIP-BLIND 4 SKIP-OK. FAIL SET = B1 B2 B4
  V1a V1b V1c V2a V2b V2c V3a V3b V4a V4b V5a V5b V6a V6b** — exactly the declared build-incomplete set, every FAIL line
  labelled BUILD-INCOMPLETE. SKIP-OK = {P6, P7, S5, T2} as declared. T1: `uncredited numeric text count = 0 (0 numeric of 23
  text elements scanned)`. S1: 13 hex colours, all tokens. S2: 5 font-size declarations, all on the scale. H5 and H6 PASS;
  H13a/b/c PASS. Container run identical in every line except the header's path/python/platform.
- Render check (container, Playwright Chromium, `file://`): title `Electrical Rate Analysis`; checked inputs `['Columbus',
  'IT']` — the saved states, from markup; console errors none; network requests: the file itself only. A CHECK, not an
  acceptance (F5Bx-8). The v0 render shows the header, the two controls, six muted slot headings; nothing else, as built.

## §5 — Step 5 result: the positive controls — 11 of 11 AS DECLARED on the mount; ONE MISS in the container's first run, recorded (23:22 UTC)

`era_ph5_page_tamper.py` md5 `4c015617ed16a117d773081a76cffe44` (355 lines). Refusals verified: `--cases N01` → `REFUSED: a
control (N01) may not run first`; `--cases W30` → `REFUSED: W01 must lead every run`. Baseline: clean page FAIL set ==
the 17 declared ids (else NOT CONNECTED, exit 3).

**Container, first full run (Python 3.11.15) — 10 of 11 AS DECLARED, W35 MISS:** actual `{H6, S1}`, declared `{S1}`;
`ALSO-ASSERTED PASS NOT SEEN: H6`. Cause, read from the gate: the `--style` override was plumbed into the H5/H6 rebuild as
well as into group S, so the rebuild read the ORIGINAL tokens while the page had been built from the altered ones — H6
compared two pages built from different inputs. That is not what §1.4 declared (*"the gate reads the ORIGINAL tokens via
--style"* for S; *"H5 and H6 PASS (deterministic given its inputs)"*). **The fix is to the override's scope, not to any
assertion:** `--style` now changes only what S compares against; H5/H6 always rebuild from the project's own inputs. No
gate was rewritten, no set was shrunk. Finding F5H0-4. Re-run `--cases W01,W35` → AS DECLARED; then the full suite:

**Container, second full run — 11 of 11 AS DECLARED.** **Mount, from the project folder (VM 3.10.12, 0.894 s) — 11 of 11
AS DECLARED**, W01 printed NOT RUNNABLE first, N01 last:

| case | declared | actual (mount) | also asserted, seen |
| --- | --- | --- | --- |
| W01 | NOT RUNNABLE (V1 build-incomplete) | NOT RUNNABLE, printed first | — |
| W15 | {D2a, D2b, D2c, D3a} | same | — |
| W16 | {D5a, D6a} | same | — |
| W24 | {D11a, D11b, D11c} | same | — |
| W30 (a) | {H13a, H6} | same | H5, T1, S1 PASS |
| W31 (b) | {H13b, H13c, D11a, D11b, D11c, H6} | same | H13a PASS |
| W32 (c) | {T1, H6} | same | S1 PASS |
| W33 (d) | {S1, H6} | same | T1 PASS |
| W34 (e₁) | ∅; two builds EQUAL | ∅; `two builds: EQUAL (md5 5e084f91… / 5e084f91…)` | H5, H6 PASS |
| W35 (e₂) | {S1} | same | H5, H6, S0a PASS |
| N01 | ∅ | ∅ | — |

No UNDECLARED FIRING, nothing DECLARED BUT SILENT, on the mount run. The ruling's five controls (a)–(e) fired on the
gates the ruling named — H13, H13+D11, T, S, determinism — with H6 beside them where the page or an input moved (§1.4).

## §6 — State after the unit, and findings

**Unchanged after every run, measured on the mount at 23:22 UTC:** `era_rates.db` `1c72e7a1b32c99a650d2e1fba17ae21e`
(`era_rates.db-journal` still the 0-byte file of Aug 29); the four grains at their pins; manifest `d28ed340…`;
`era_ph5_workbook_gate.py` `689b1354…`; `era_ph5_dashboard.twb` `20dcb01d…`. No retired file was written. No `.tmp` left
on the mount. New on the mount: `era_ph5_grain_gate.py`, `era_ph5_build_html.py`, `era_ph5_page_gate.py`,
`era_ph5_page_tamper.py`, `era_ph5_dashboard.html` (v0), this file; `__pycache__/` (gitignored) gained the module caches.

**Checkpoint (§1.5):** items 1, 2, 3, 4, 6 MEASURED HIT. **Item 5 is OPEN**: `era_ph5_5h_gate_run.log` and
`era_ph5_5h_tamper_run.log` must come from Brad's shell (F5B-9). This session did not and cannot write them; the
closeout hands Brad the two commands. The next session checks whether the two logs exist and carry
`project=C:\Users\...` headers before it treats 5H-0 as complete.

### Findings

- **F5H0-1. Group D is 29 gates, not 26.** The HTML ruling's "26" is 5B's pre-5B-x count; D11a–D11c (the ties the 5B-x
  probe needed) make 29, and the committed 5B log has 29 `[D]` lines. Recorded, not fixed; every 5H declaration uses 29.
  Memory's "26/26 identical" should read 29/29.
- **F5H0-2. A "verbatim in its results file" citation pointed at an empty heading.** Brad's-shell Python (3.13.5) exists
  in project memory and in the HTML ruling; `era_ph5_5by_results.md` §5 never received it. Nothing about the version is
  doubted; the RECORD was missing. The 5H gate and tamper print `sys.version` in their headers so Brad's committed logs
  carry the measurement themselves. **A citation to a file is checked by opening the file (F5B-10, applied to a citation).**
- **F5H0-3. A reproduction gate fires on every tamper, by construction.** H6 (scratch rebuild == page on disk) moved on
  W30, W31, W32, W33 beside the gate each control targets, because every one of them makes the page and its inputs
  disagree. The ruling's "alone" holds at the level of the gate it names. Consequence for 5H-1 on: any page tamper's
  declared set carries H6; a tamper that fires ONLY H6 is one no other group sees — that is the case worth writing.
- **F5H0-4. A tamper-only override must be scoped to the one thing it overrides.** The first `--style` plumbing reached the
  rebuild and made H6 a false positive on W35. The control caught it in the container before anything reached the mount;
  the fix narrowed the override. **The retired gate's `--branch`/`--ruling` overrides had the same shape; the lesson is
  general: an override that changes the gate's REFERENCE must not change the gate's ARTEFACT.**
- **F5H0-5. One page, two interpreters, one md5.** Python 3.11.15 (container) and 3.10.12 (device VM) built
  `5e084f91b756ab4b29b31046f09d1884` from the same inputs. Determinism across interpreters is what lets Brad's shell
  (3.13.x) be the committed builder in 5H-4's chain; it is a prediction there, not yet a measurement.
- **F5H0-6. The committed logs are CRLF.** Windows text-mode append writes `\r\n`; comparisons across logs need
  `--strip-trailing-cr` or a normalising reader. Cosmetic; recorded so no later session reads it as a content difference.
- **F5H0-7. `P6`/`P7`, `S5`, `T2` are SKIP-OK on v0 and must become PASS or FAIL as the slots fill.** A later session that
  sees any of them still SKIP-OK on a page with the relevant view built has found a gate that stopped looking.

### Routed

**NOTHING.** No ruling is pending with the strategy chat. Two notes for the strategy chat's next memory pass, not rulings:
the "26" in `direction_ph5_html_v1.0.md` / memory reads 29 on disk (F5H0-1); the 5B-y P1 citation (F5H0-2).

### Handoff conventions for 5H-1 (declared here so the view code and the gate agree)

- A built view replaces its slot's body with `<svg data-view="Vn" width height>` (or `<table data-view="V6">`) and DROPS
  `data-status="build-incomplete"`. `find_view()` then gates it.
- V1: bars carry `data-role="bar" data-metro="<metro>" data-field="<column>"`; the two basis states are sibling groups
  `data-state-basis="IT"|"Metered"` with `data-axis-field`, the Metered one `hidden="hidden"` and `data-remainder="0"` with the
  text "baseline tariff rate only" (F5B-2). V3: `data-channel="<column>"` in F4E-3 order. Every numeric `<text>` carries
  `data-src="era_ph5_metro:<metro>:<column>"` and shows the cell to the precision printed. W01 rebinds `data-field` to
  `mitigated_annual_usd` and must fire V1c alone (plus H6 by F5H0-3 — declare it).
- Gate runtime with the build inside it: 0.12 s on the VM; the 45 s cap is not near.

---

# Unit 5H-1 — V1 the ranking and V3 the channel decomposition

Session 2026-09-05, cloud execution session on Brad's mounted project folder. Scope: `direction_ph5_html_v1.0.md`
Unit 5H-1 only — V1 and V3, both from G1. No SQLite write. No retired file written. Record appended below; nothing
above this line is edited.

## §7 — Declared expectations, written before any run of this unit

### §7.0 — Step 0, the state this unit checked before anything else (the handoff's "gate the page on disk first")

Measured on the mount before a line was written:

- `era_ph5_5h_gate_run.log` PRESENT, 10,276 B, header `era_ph5_page_gate.py  Unit 5H-0  project=C:\Users\User\Claude\Projects\Electrical Rate Analysis  page=era_ph5_dashboard.html  python=3.13.5  platform=Windows-11-10.0.26200-SP0  page_md5=5e084f91b756ab4b29b31046f09d1884`.
- `era_ph5_5h_tamper_run.log` PRESENT, 3,457 B, header `era_ph5_page_tamper.py  Unit 5H-0  project=C:\Users\User\Claude\Projects\Electrical Rate Analysis  python=3.13.5`.
- **5H-0 checkpoint item 5 is therefore CLOSED, and Brad's shell is measured at Python 3.13.5 in his own committed
  logs — the record F5H0-2 said was missing now exists.** 5H-0 is complete on every item.
- `era_ph5_dashboard.html` md5 `5e084f91b756ab4b29b31046f09d1884` (137,920 B), as declared.
- Page gate re-run on the mount from the device VM: **54 PASS / 17 FAIL / 0 SKIP-BLIND / 4 SKIP-OK**, FAIL set
  `B1 B2 B4 V1a V1b V1c V2a V2b V2c V3a V3b V4a V4b V5a V5b V6a V6b` — exactly §1.3's declared set. **NOT BLOCKED.**

### §7.1 — Step 1, V1 and V3 built, gated by 5H-0's page gate UNCHANGED

**`era_ph5_views.py` (new, stdlib, one function per view).** `view_v1(G1)` and `view_v3(G1)`; `era_ph5_build_html.py`
imports it and a slot with a view function drops `data-status="build-incomplete"` and carries its `<svg>`.

**V1.** Eight metros by `rank`; the bar is `usd_per_it_mwh` split into the mitigated remainder
(`mitigated_usd_per_it_mwh`, solid, ramp step by magnitude over the 7 accent steps) and the mitigation
(`mitigation_usd_per_it_mwh`, drawn hollow with an `--era-rule` hairline) so the avoidable part is a REMAINDER, not a
second chart. Both `p. Basis` states pre-rendered as `<g data-state-basis>` with `data-axis-field`; IT visible,
Metered `hidden="hidden" data-remainder="0"` carrying the text "baseline tariff rate only" (F5B-2 — the frozen
contract has no mitigated metered column, D9a). `svg` 1184 x 432. One credited label per bar.

**V3.** The five channels in `V3_ORDER`, rider first (F4E-3), portfolio-wide, no metro filter, one colour. Each row is
the eight metros walked from a zero line, so the row's end point IS the channel total and every mark resolves to a
cell. `data-channel` on exactly the five row groups. `svg` 1184 x 288. The largest single contribution in each row is
drawn a shade darker and carries its own cell as a credited label.

**Figures are printed with the ASCII hyphen-minus, never U+2212**: the gate's T2 strips U+2212 from the shown text
instead of translating it, so a typographic minus would silently drop the sign of a negative figure.

**DECLARED TALLY on the rebuilt page, with `era_ph5_page_gate.py` EXACTLY AS 5H-0 LEFT IT — 62 PASS / 12 FAIL /
1 SKIP-OK / 0 SKIP-BLIND**, FAIL set exactly

    {V1b, V1c, V2a, V2b, V2c, V4a, V4b, V5a, V5b, V6a, V6b, B4}

**Two of those twelve are DECLARED FAILURES OF THE GATE, NOT OF THE VIEW, and they are declared here before the run
so the measurement decides:** 5H-0 wrote V1b and V1c to quantify over the WHOLE `V1` svg, while 5H-0's own §6 markup
conventions require TWO pre-rendered basis states inside that svg. The honest page therefore holds 16 elements with
`data-role="bar"`, not 8 (V1b compares a 16-item list against an 8-item one), and the set of `data-field` values over
the whole svg is the IT triple PLUS `usd_per_mwh` (V1c compares against the IT triple alone). **Predicted: V1b and
V1c FAIL, and every other V1/B/P/S/T gate PASSES.** Newly live and predicted PASS: **P7** (2 basis states, IT the one
not hidden), **B1** (visible state IT, axis field `usd_per_it_mwh`), **B2** (remainder 0 and the label says so),
**S5** (2 svgs, all dimensions multiples of 8), **T2** (every credited figure equals its cell to the precision shown).
**P6 stays SKIP-OK** (V2 unbuilt). **T1 stays PASS at 0 uncredited numerics with the two views drawn** — this is the
gate that matters most in this unit and it is asserted over the whole page, not over the new views only.

### §7.2 — Step 2, the gate scope correction, declared before it is written

If and only if §7.1 measures V1b/V1c exactly as predicted, the correction is to the gate's SCOPE and it makes the gate
STRICTLY STRONGER, never looser (a failing assertion is not rewritten to pass — 4A):

- **V1b** — every `data-state-basis` group inside V1 has its `data-role="bar"` elements in `rank` order, and there are
  eight of them per state. (Before: one list over the whole svg, which asserted nothing about the second state.)
- **V1c** — the IT state's `data-field` values are exactly `{usd_per_it_mwh, mitigated_usd_per_it_mwh,
  mitigation_usd_per_it_mwh}` AND the Metered state's are exactly `{usd_per_mwh}`. (Before: one union over the whole
  svg, which could not tell the two states apart.)

**DECLARED TALLY after the correction — 64 PASS / 10 FAIL / 1 SKIP-OK / 0 SKIP-BLIND**, FAIL set exactly

    {V2a, V2b, V2c, V4a, V4b, V5a, V5b, V6a, V6b, B4}

which is the ruling's checkpoint "the build-incomplete set is exactly {V2, V4, V5, V6}" (B4 reads V5).

### §7.3 — Step 3, the tamper suite, declared before it runs

`era_ph5_page_tamper.py` is re-pointed: `BASELINE_V0` becomes the §7.2 set of ten (the harness aborts NOT CONNECTED
unless the clean baseline equals it), **W01 becomes RUNNABLE and leads the suite (F5B-3), and W02 is added.**

| case | kind | declared firing set | why |
| --- | --- | --- | --- |
| **W01** | page | **{V1c, H6}** | V1's IT-state bars rebound from `mitigated_usd_per_it_mwh` to `mitigated_annual_usd`. **No bar moves** (F5B-4: the binding changes, the geometry the build already wrote does not), so only the BINDING gate can see it. H6 by construction (F5H0-3): the page no longer equals its rebuild. |
| **W02** | page | **{V3b, H6}** | V3's first two `data-channel` values swapped (rider ↔ energy). V3b compares against `V3_ORDER`; nothing else reads `data-channel`. H6 by F5H0-3. |
| W15 | grain | {D2a, D2b, D2c, D3a} | unchanged from 5H-0 |
| W16 | grain | {D5a, D6a} | unchanged from 5H-0 |
| W24 | grain | {D11a, D11b, D11c} | unchanged from 5H-0 |
| W30 | page | {H13a, H6} | unchanged from 5H-0 |
| W31 | input | {H13b, H13c, D11a, D11b, D11c, H6} | unchanged from 5H-0 |
| W32 | page | {T1, H6} | unchanged from 5H-0 |
| W33 | page | {S1, H6} | unchanged from 5H-0 |
| W34 | build | (nothing fires) | unchanged from 5H-0 |
| W35 | build | {S1} | unchanged from 5H-0 |
| N01 | control | (nothing fires) | unchanged from 5H-0; runs LAST |

**Declared: 13 of 13 AS DECLARED, W01 first, control last, and the harness REFUSES a control-first or non-W01-first
run.** Weak prediction, marked weak: W01's "no bar moves" is a claim about the build, and the harness cannot see
geometry — the evidence for it is that W01 edits only `data-field` attributes in the page text and the rects' `x`,
`width` are untouched by the edit.

### §7.4 — Step 4, the render read (a check, never an acceptance — F5Bx-8)

The cloud container renders the page with Playwright Chromium from `file://` at 2x and the session READS the two PNGs.
**Declared: zero network fetches, zero console errors, V1 showing the ranking DFW 47.67 at the top to
San Jose / Bay Area 180.96 at the bottom, the Metered state not visible, and V3 showing the rider row as the longest
of the five.** The renders are the session's check; `renders/*.png` are committed from 5H-4 (ruling H-4).

### §7.5 — Checkpoint conditions (from the ruling), restated as things this session will measure

1. V1 and V3 pass every V, B, S, T gate that reads them.
2. The build-incomplete set is exactly {V2, V4, V5, V6} (ten ids, B4 included as V5's dependant).
3. W01 and W02 fired as declared, W01 first.
4. The container's render of V1 and V3 was read and shows DFW 47.67 -> San Jose 180.96 with no typed number outside a
   `data-src`.
5. Logs `era_ph5_5h_gate_run.log` and `era_ph5_5h_tamper_run.log` re-written from BRAD'S shell (F5B-9). This session
   cannot write them; the closeout hands him the commands. **5H-2 checks for the 5H-1 headers before it treats this
   unit as complete.**
6. `era_rates.db` md5 `1c72e7a1b32c99a650d2e1fba17ae21e` unchanged; the four grains and the manifest at their pins.

## §8 — Results, in the order the runs happened

### §8.1 — Step 1, V1 and V3 built, 5H-0's gate UNCHANGED — DECLARATION HIT (scratch, device VM, Python 3.10.12)

**62 PASS / 12 FAIL / 0 SKIP-BLIND / 1 SKIP-OK**, FAIL set `B4 V1b V1c V2a V2b V2c V4a V4b V5a V5b V6a V6b` —
exactly §7.1. The two predicted gate-scope failures printed their reason in full:

- `FAIL [V] V1b  V1 bar groups in rank order: ['Dallas-Fort Worth', ... 'San Jose / Bay Area', 'Dallas-Fort Worth',
  ... 'San Jose / Bay Area']` — the sixteen bars of two correct states, compared against an eight-item list.
- `FAIL [V] V1c  V1 bound to usd_per_it_mwh and its parts; got ['mitigated_usd_per_it_mwh',
  'mitigation_usd_per_it_mwh', 'usd_per_it_mwh', 'usd_per_mwh']` — the union of two correct bindings.

Newly live and PASS as declared: **P7**, **B1**, **B2**, **S5** (2 svgs, dimensions multiples of 8), **T2**
(21 credited figures equal their cells to the precision shown). **T1 PASS: 0 uncredited numerics of 21 numeric text
elements in 122 scanned** — the two views added 99 text elements and not one typed figure. P6 SKIP-OK (V2 unbuilt).

### §8.2 — Step 2, the gate scope correction — DECLARATION HIT

`era_ph5_page_gate.py` V1b/V1c re-quantified per pre-rendered basis state, per §7.2. **64 PASS / 10 FAIL /
0 SKIP-BLIND / 1 SKIP-OK**, FAIL set `B4 V2a V2b V2c V4a V4b V5a V5b V6a V6b` — exactly §7.2, and exactly the
ruling's checkpoint set {V2, V4, V5, V6}. The two corrected gates now report what they measure:

    PASS [V] V1b  each basis state has its 8 bar groups in rank order — IT: 8 bar(s), rank order True;
                  Metered: 8 bar(s), rank order True
    PASS [V] V1c  each basis state bound to its own basis and nothing else:
                  {'IT': ['mitigated_usd_per_it_mwh', 'mitigation_usd_per_it_mwh', 'usd_per_it_mwh'],
                   'Metered': ['usd_per_mwh']}

The gate's declared-tally header was re-pointed from §1.3's v0 line to §7.2's, and its unit label from 5H-0 to 5H-1.

### §8.3 — Step 3, the tamper suite, first run — 11 of 12 AS DECLARED, ONE MISS ON W31, RECORDED

Baseline clean-page FAIL set == the §7.2 set of ten: **CONNECTED.** W01 ran first; the control ran last.

**W01 AS DECLARED, fired exactly {H6, V1c}** — and `V1a`, `V1b`, `T1`, `T2`, `S1` were separately asserted PASS in
the same run, which is what proves the rebinding is scoped: **the binding moved and no bar moved (F5B-4).**
**W02 AS DECLARED, fired exactly {H6, V3b}.** W15, W16, W24, W30, W32, W33, W34, W35, N01 all AS DECLARED, sets
unchanged from 5H-0.

**W31 MISS — UNDECLARED FIRING {T2}. The gate is right and §7.3's declaration was wrong.** W31 perturbs Columbus's
`usd_per_it_mwh` on disk by +200 AFTER the build and leaves the page alone. Before this unit no view credited a
figure, so T2 had nothing to compare and the case fired six ids. Now V1 prints Columbus at `69.26` with
`data-src="era_ph5_metro:Columbus:usd_per_it_mwh"`, and T2 resolves that against the CSV **on disk**, which now reads
`269.26`. **T2 is a freshness gate the moment a view credits a figure** (F5H1-2). The declaration was carried forward
from 5H-0 without re-deriving it against a page that had views on it.

**Amended declaration for W31, written here BEFORE the re-run:**

    W31  input  {H13b, H13c, D11a, D11b, D11c, H6, T2}

with `H13a` still separately asserted PASS. Nothing else in the suite changes. **Declared on the re-run: 12 of 12
AS DECLARED.**

### §8.4 — Step 3, the tamper suite, re-run — 12 of 12 AS DECLARED

Scratch and then the mount, both AS DECLARED on every case, W01 first, N01 last, baseline CONNECTED both times.
W31 fired the amended seven-id set exactly.

### §8.5 — Step 4, the render — DECLARATION HIT (cloud container, Playwright Chromium 1194, file://, 2x)

- **network requests other than the `file://` page itself: ZERO. console errors and page errors: ZERO.**
- basis states in the DOM: `IT` not hidden, `Metered` hidden; the Metered group's rendered height is **0 px** — the
  saved state is the markup's, not the script's.
- **V1, top to bottom, read off the rendered labels: Dallas-Fort Worth 47.67, Columbus 69.26, Chicago 81.54,
  Austin 94.85, Northern Virginia 107.56, Phoenix 123.57, Atlanta 142.71, San Jose / Bay Area 180.96.** The 5B-x pins,
  in rank order, and every one of them a credited figure.
- V3 row extents in px, measured off the rendered rects: rider **870**, energy **457**, demand **196**, fixed **1**,
  statutory **90**. **F4E-3 is legible without a click: the rider row is nearly twice the energy row and more than
  four times the demand row.**
- Renders read by the session as `renders/era_ph5_v1.png` and `renders/era_ph5_v3.png` in the container. **NOT
  committed** — ruling H-4 commits renders from 5H-4 on. A screenshot measures the render; the gate measures the file
  (F5Bx-8).

### §8.6 — Cross-interpreter determinism, with views on the page

`era_ph5_dashboard.html` md5 **`821e1cbb0e151c68a18ea8b6abbd2257`**, 153,760 B, built identically by the device VM
(Python 3.10.12) in scratch, by the device VM from the project folder, and by the cloud container (Python 3.11.15).
Three builds, one md5. H5 and H6 PASS in every run. (Page grew from v0's 137,920 B; H7's ceiling is 4 MB, so the page
is at 3.7 % of it with two views drawn.)

## §9 — State after the unit, and findings

**Unchanged, measured on the mount after every run:** `era_rates.db` `1c72e7a1b32c99a650d2e1fba17ae21e`; the four
grains at their E-1.4 pins (`84fe4dbf…`, `3e8825ac…`, `f5b3638a…`, `fc1fa4b1…`); manifest `d28ed340…`. No SQLite
write. No retired file written. No `.tmp` left on the mount.

**Changed or new on the mount:**

| file | md5 | what |
| --- | --- | --- |
| `era_ph5_views.py` | `91edf17d1cdaf707b6d210c07b498bee` | NEW. `view_v1`, `view_v3`, stdlib, one function per view |
| `era_ph5_build_html.py` | `c31ac03c9c47f7bd44f0f2bce85dc06d` | imports the views; a built slot drops `data-status`; seven ramp classes + mark classes added to the token CSS |
| `era_ph5_page_gate.py` | `00b12bd3ee7f3fbdcdfed74e0331af8d` | V1b/V1c re-quantified PER BASIS STATE (F5H1-1); header now declares §7.2's tally |
| `era_ph5_page_tamper.py` | `85d2af562f4772c10ad474ef0953fddb` | baseline = the ten; **W01 runnable and leading**; **W02 added**; W31 amended to seven (F5H1-2) |
| `era_ph5_dashboard.html` | `821e1cbb0e151c68a18ea8b6abbd2257` | 153,760 B, V1 and V3 drawn |

**Checkpoint (§7.5):** items 1, 2, 3, 4 and 6 MEASURED HIT. **Item 5 is OPEN**: `era_ph5_5h_gate_run.log` and
`era_ph5_5h_tamper_run.log` must be re-written from Brad's shell (F5B-9). This session did not and cannot write them;
the closeout hands him the commands. **5H-2 checks for headers reading `Unit 5H-1` before it treats this unit as
complete.**

### Findings

- **F5H1-1. A gate written before its artefact existed is a prediction about markup, and the first built view is what
  measures it.** 5H-0's V1b/V1c quantified over the whole `V1` svg while 5H-0's OWN §6 markup conventions required two
  pre-rendered basis states inside it: V1b compared a sixteen-item bar list against an eight-item one, and V1c took
  the union of the two states' bindings, so `usd_per_mwh` looked like a stray. **Both were declared FAIL in §7.1
  before the run and both failed for exactly the declared reason.** The correction is to SCOPE and is strictly
  stronger: V1b now asserts rank order in BOTH states (the 5H-0 form asserted nothing about the second), V1c asserts
  each state is bound to its own basis and nothing else (the 5H-0 form could not tell them apart). **Nothing was
  loosened and no assertion was rewritten to pass.**
- **F5H1-2. A credited figure is a freshness assertion, so T2 joins the firing set of every input tamper the moment a
  view exists.** W31 (Columbus `usd_per_it_mwh` + 200 on disk, page untouched) fired `{H13b, H13c, D11a, D11b, D11c,
  H6, T2}` against a declared six. **The gate was right; the declaration was carried forward from 5H-0 without being
  re-derived against a page with views on it.** Recorded as a MISS, amended in writing before the re-run, re-run
  recorded (§8.3, §8.4). **Rule for 5H-2 and 5H-3: re-derive every carried tamper set against the CURRENT page; a
  declared set is not inherited.**
- **F5H1-3. The gate's T2 STRIPS the typographic minus instead of translating it.** `re.sub(r"[,$%\s\u2212]", "", t)`
  deletes U+2212 and the following `.replace("\u2212", "-")` is then a no-op, so a figure printed with a typographic
  minus would be read as POSITIVE and a negative cell would silently mismatch — or, worse on some other rounding,
  silently match. **Views print the ASCII hyphen-minus, and `era_ph5_views.py` says so in its docstring.** The
  normaliser itself is a one-line hardening candidate for 5H-4; it is not touched here because changing it would
  change what three declared-and-hit measurements measured.
- **F5H1-4. V3's `Fixed` row is one pixel at portfolio scale and its credited label is bisected by the zero-line
  rule.** `mitigation_fixed_usd` totals $226,130.88 against the rider channel's $167.1 M, so a proportional mark IS
  one pixel — the drawing is honest and the collision is cosmetic. **Routed to 5H-4**, whose scope is assembly and
  aesthetic conformance: nudge a credited label clear of the axis when its row's extent is under one grid unit. No
  gate sees it.
- **F5H1-5. The frozen contract carries no portfolio-total cell for the three headline channels, so V3 cannot print
  one without typing a figure.** G1 holds the five channels PER METRO; G4 holds exactly one channel total as a cell
  (`C-EXCISE-ALLOC`, $17,239,632.05, the statutory one). The rider, energy and demand totals that F4E-3 is about
  (-$167.1 M / -$87.6 M / -$37.7 M) exist in no cell. **V3 therefore makes its claim by LENGTH and labels each row's
  largest single contribution from that contribution's own cell.** The claim survives — the render measures rider 870
  px against energy 457 and demand 196 — but the three headline figures are not on the page. **Routed as a note to
  the strategy chat, not a ruling request:** printing them would need a portfolio-total column or a fifth grain, which
  is a change to the extract contract that Ruling 4R froze; the alternative is to leave them to the Phase 5 report.
- **F5H1-6. Cross-interpreter determinism holds with views on the page.** Python 3.10.12 (device VM, twice, from two
  directories) and 3.11.15 (cloud container) built `821e1cbb…`. Extends F5H0-5; Brad's 3.13.x remains 5H-4's
  measurement.
- **F5H1-7. 5H-0's checkpoint item 5 is CLOSED and it closed F5H0-2 with it.** Brad's committed
  `era_ph5_5h_gate_run.log` and `era_ph5_5h_tamper_run.log` carry `project=C:\Users\User\Claude\Projects\
  Electrical Rate Analysis` and `python=3.13.5`. **The version that F5H0-2 found asserted everywhere and recorded
  nowhere is now a measurement in a committed file.** The header-prints-`sys.version` decision is what did it.

### Routed

**NO RULING IS PENDING.** Two notes for the strategy chat's next memory pass:

1. **F5H1-5** — the three headline channel totals cannot be printed on the page under the frozen 52-column contract
   and the zero-typed-figures rule. If they must appear, that is a contract change (Ruling 4R) or a Phase 5 report
   item; this session did neither.
2. **F5H1-1** — `direction_ph5_html_v1.0.md`'s group-V table describes V1 as "mark counts equal the row counts they
   derive from", which is true per state and false over the svg once two states are pre-rendered. The ruling text is
   not wrong, it is under-specified; the gate now carries the specification.

### Conventions 5H-2 must follow (V2)

- A built slot drops `data-status="build-incomplete"`; `era_ph5_views.py` gains `view_v2(G2)` and registers it in
  `VIEWS`. Nothing else in the build changes.
- V2's eight metro states are `<g data-state-metro="<metro>">` inside the V2 svg, Columbus the only one without
  `hidden` (P6 goes live and must turn PASS — F5H0-7). Rows carry `data-component="<component_id>"` in
  `waterfall_order`; excluded siblings carry `data-excluded="1" data-muted="1"` and are drawn `--era-muted` with an
  `--era-rule` hairline (style rule 3).
- Row key for a credited G2 figure is `era_ph5_stack:<metro>|<component_id>:<column>`. **ASCII hyphen-minus** (F5H1-3).
- Marks carry CSS classes; no hex and no `font-size` is written into the markup (S1/S2/S3). Every `<svg>` dimension a
  multiple of 8 (S5).
- **Re-derive every tamper set against the page as it then stands (F5H1-2).** The declared baseline after 5H-2 is
  `{V4a, V4b, V5a, V5b, V6a, V6b, B4}`; W01 still leads.

---

# Unit 5H-2 — V2 the waterfall, eight states, the excluded band

Session 2026-09-05, cloud execution session on Brad's mounted project folder. Scope: `direction_ph5_html_v1.0.md`
Unit 5H-2 only — V2, from G2. No SQLite write. No retired file written. Record appended below; nothing above this
line is edited.

## §10 — Declared expectations, written before any run of this unit

### §10.0 — Step 0, the state this unit checked before anything else (the handoff's "gate the page on disk first")

The handoff named four things to verify and said the unit is BLOCKED, not repairable, if any fails. All four were
read off the folder before a line of this unit's code was written:

| checked | required | measured | verdict |
| --- | --- | --- | --- |
| `era_ph5_5h_gate_run.log` header | reads `Unit 5H-1` | `era_ph5_page_gate.py  Unit 5H-1  project=C:\Users\User\Claude\Projects\Electrical Rate Analysis  page=era_ph5_dashboard.html  python=3.13.5  platform=Windows-11-10.0.26200-SP0  page_md5=821e1cbb0e151c68a18ea8b6abbd2257` | HIT |
| `era_ph5_5h_tamper_run.log` header | reads `Unit 5H-1` | `era_ph5_page_tamper.py  Unit 5H-1  project=C:\Users\User\Claude\Projects\Electrical Rate Analysis  python=3.13.5` | HIT |
| `era_ph5_dashboard.html` md5 | `821e1cbb0e151c68a18ea8b6abbd2257` | `821e1cbb0e151c68a18ea8b6abbd2257` | HIT |
| gate tally in that log | 64 PASS / 10 FAIL / 1 SKIP-OK, FAIL set `{V2a V2b V2c V4a V4b V5a V5b V6a V6b B4}`, P6 the only SKIP-OK | `RESULT 64 PASS  10 FAIL  0 SKIP-BLIND  1 SKIP-OK`; `FAIL SET B4 V2a V2b V2c V4a V4b V5a V5b V6a V6b`; the single `SKIP-OK [P] P6` | HIT |

Tamper log tail reads `RESULT 12 of 12 AS DECLARED (W01 ran first, V1 built)`; 12 `CASE` headers, 12 `AS DECLARED`.
**Both committed logs run from `C:\Users\User\...` on `python=3.13.5` — Brad's shell.**

**Therefore 5H-1's checkpoint item 5 is CLOSED and Unit 5H-1 is complete on every item.** 5H-2 is not blocked and
proceeds. The unit did NOT take the handoff's description as fact; every line of the table above is a read
(F5B-10, and the standing "check the file yourself, every time").

### §10.1 — Step 1, V2 built, gated by 5H-1's page gate UNCHANGED

`era_ph5_views.py` gains `view_v2(G2)` and a `VIEW_GRAIN` map; `era_ph5_build_html.py` passes each view the grain
it declares instead of G1 unconditionally. **That map is the whole build change** — it is required, because V2 is
the first view that does not read G1, and the 5H-1 build hard-codes `fn(grains["G1"])`.

**Markup V2 will carry** (the §9 conventions, restated as the thing the gate will read):

- `<svg data-view="V2" width="1184" height="288">` inside `<section data-view="V2">` with `data-status` DROPPED.
- Eight `<g data-state-metro="<metro>">` children, one per metro in `era_ph5_build_html.METROS` order. Columbus
  carries no `hidden`; the other seven carry `hidden="hidden"`. All eight draw from the same top, so switching
  states does not reflow the page.
- Inside a state, one `<g data-component="<component_id>">` per G2 row for that metro, in `waterfall_order`
  order — **the excluded sibling included, sorting last on its order 99**. Each row group holds one `<title>`
  (the component name), one `<rect>`, one label `<text>` and one value `<text>`.
- The excluded row's `<g>` and ONLY that `<g>` carries `data-excluded="1" data-muted="1"`; its `<rect>` carries
  `class="era-excluded"`, which the build's CSS defines as `fill: var(--era-muted); stroke: var(--era-rule)`
  (style rule 3). Three such groups exist — Columbus, Dallas-Fort Worth, San Jose / Bay Area — and no others.
- Levels (`kind` baseline and mitigated) draw `class="era-wf-level"` = `--era-accent-700`; deltas (`kind` measure
  and storage, every one of them negative) draw `class="era-wf-delta"` = `--era-accent-200`. **That is style rule
  1's diverging pair — the two ends of the one ramp, sign carried by the label, no second hue.** Baseline and
  total are told apart by position and label, per style rule 2, not by tint.
- Every `<text>` and every `<title>` carries `data-src="era_ph5_stack:<metro>|<component_id>:<column>"`:
  labels and titles to `component_name`, value figures to `usd_per_year`. **Titles and labels are credited
  because they must be**: eight component names contain `B100`, which is a three-digit run, so `FIGURE_RE` reads
  them as figures and T1 would count them uncredited. Crediting them is the truthful fix — the text IS the cell —
  and T2 then string-compares them.
- **ASCII hyphen-minus** in every figure (F5H1-3). No hex and no `font-size` in the markup (S1/S2/S3). Both svg
  dimensions multiples of 8 (S5).

**Geometry, declared with its reasoning so the drawing is not a preference:**

- One scale for all eight states, `x = 688 px / $1,428,314,506.82` (the largest `waterfall_end_usd` on the page,
  San Jose's baseline). **A per-metro scale would rescale the bars when the control is switched, which is the one
  thing a pre-rendered state control must not do.**
- Baseline and mitigated-total rows run from zero to `waterfall_end_usd`. Measure and storage rows are floating
  bars from `waterfall_start_usd` to `waterfall_end_usd` — the classic waterfall step.
- **The excluded band is anchored at ZERO and drawn to `|usd_per_year|`, below a hairline separator.** G2 gives
  the excluded rows an EMPTY `waterfall_start_usd` and `waterfall_end_usd` — they have no position in the walk.
  Anchoring the band at the mitigated total and extending it leftward would draw a "what the total would have
  been", which asserts additivity the contract does not carry. **A magnitude anchored at zero makes the weakest
  claim the data supports**: this quantity exists, at this size, and it is not in the total.
- A bar whose true width rounds below one pixel is drawn one pixel wide (`max(w, 1)`), as V1 already does for the
  mitigation segment. **This is disclosed, not hidden**: the proportional truth is that DFW's storage step is
  1.2 px of 688.
- No axis figures. A tick label is not a cell, and the zero-typed-figures rule is page-wide; each row carries its
  own credited figure instead. One zero line, `class="era-axis"`.

**DECLARED TALLY, step 1 — the gate UNCHANGED from 5H-1:**

> **68 PASS; 7 FAIL, all BUILD-INCOMPLETE, = `{V4a V4b V5a V5b V6a V6b B4}`; 0 SKIP-OK; 0 SKIP-BLIND.**
> 75 rows, as now. V2a, V2b and V2c turn FAIL → PASS. **P6 turns SKIP-OK → PASS (F5H0-7: a SKIP-OK must turn
> PASS or FAIL as its slot fills), and it is the last SKIP-OK on the page — the page gate ends this unit with
> nothing skipped.** B4 stays FAIL: it reads V5, which is still a slot. Exit code stays 1.

Also declared for step 1, WEAK (an exact count; a miss here is arithmetic, not a defect):

- T1 reads `uncredited numeric text count = 0 (70 numeric of 221 text elements scanned)` — 99 text elements added
  (33 rows x title + label + value), of which 49 are numeric (33 values, plus the 8 `B100` labels and their 8
  titles). T2 reads `70 credited figures`.
- S5 reads `3 svg(s)`.
- H5/H6 PASS: the page is byte-identical to its rebuild.

**PREDICTED GATE BEHAVIOUR THAT IS NOT A PASS/FAIL — declared before the run (F5H1-1).** V2c as 5H-1 left it
asserts `len(marks) == len(ex)` and `data-muted == "1"` on each. **Both are attributes the build writes about
itself.** The ruling's requirement is that the excluded siblings are DRAWN in `--era-muted` with an `--era-rule`
hairline; an attribute is a claim, not paint. V2c will PASS at step 1 and it will PASS while asserting less than
the ruling requires. **This is the F5H1-1 pattern in its second form — the first form was a gate that failed for a
declared reason; this is a gate that passes for an insufficient one — and it is declared here, before the run, so
that the correction in §10.2 is on record as a correction of SCOPE and not a reaction to a result.**

### §10.2 — Step 2, the V2c scope correction, declared before it is written

After step 1's run is recorded, `era_ph5_page_gate.py`'s V2c is re-scoped to assert, in addition to the two
things it asserts now:

3. every `data-excluded="1"` mark also carries `data-component` — it is IN the waterfall order, never omitted;
4. every such mark contains a `<rect class="era-excluded">` — the paint is carried by a real mark;
5. the page's own CSS defines `.era-excluded` with `fill: var(--era-muted)` AND `stroke: var(--era-rule)` — the
   muted fill and the hairline are declared in the artefact, not asserted by an attribute.

**This is strictly stronger and nothing is loosened.** The 5H-1 form could be satisfied by three empty `<g>`
elements carrying two attributes and no mark at all. The corrected form cannot. **No threshold moves; no failing
assertion is rewritten to pass** (4A) — V2c passes before and after, and the correction is what makes the pass
mean what the ruling says.

The header's DECLARED line is re-written to §10.1's tally at the same time. That line is printed text, not an
assertion; it is updated because a run log that declares the wrong unit's tally is a lie in a committed file.

**DECLARED TALLY, step 2:** identical to §10.1 — **68 PASS; 7 FAIL `{V4a V4b V5a V5b V6a V6b B4}`; 0 SKIP-OK;
0 SKIP-BLIND**, 75 rows. A scope correction that changed the tally would mean the markup was wrong, not the gate.

### §10.3 — Step 3, the tamper suite, declared before it runs

**Every carried set below was re-derived against the page as it stands WITH V2 ON IT (F5H1-2). A declared set is
not inherited.** The derivation for each carried case is stated, not assumed.

`BASELINE` in `era_ph5_page_tamper.py` becomes `{V4a, V4b, V5a, V5b, V6a, V6b, B4}` — seven, from ten. W01 still
leads and the harness still refuses a control-first or non-W01-first run (F5B-3).

| case | kind | declared firing set | re-derivation against the V2 page |
| --- | --- | --- | --- |
| W01 | page | `{V1c, H6}` | UNCHANGED. The edit rewrites the 8 occurrences of `data-field="mitigated_usd_per_it_mwh"`. **V2 writes no `data-field` attribute at all**, so the count assertion of 8 still holds and no V2 gate reads that attribute. V1c alone, H6 by F5H0-3. |
| W02 | page | `{V3b, H6}` | UNCHANGED. The edit swaps two `data-channel` values. **V2 writes no `data-channel`.** V3b alone, H6 by F5H0-3. |
| W03 | page | `{V2b, V2c, H6}` | **NEW.** Columbus's excluded sibling row `<g>` is DELETED from its state group — the ruling's literal "sibling row dropped". V2c sees 2 marks for 3 rows; **V2b ALSO fires, because `data-component` for Columbus is then 4 ids against G2's 5.** Both are true consequences of dropping a row and both are declared. H6 by F5H0-3. |
| W04 | page | `{V2c, H6}` | **NEW.** Columbus's excluded sibling is left in place and only its `data-excluded="1"` marking is removed. **This is the case that delivers the ruling's "V2's exclusion gate alone"**: V2b still sees 5 ids in order and PASSES, so the firing is scoped to the exclusion gate and proves V2c is connected independently of V2b. H6 by F5H0-3. |
| W05 | page | `{P6, H6}` | **NEW.** The saved metro is moved to Chicago inside the svg: Columbus's state group gains `hidden="hidden"`, Chicago's loses it. P6 sees the visible state as Chicago against Columbus. **P2 and P4 stay PASS — the control fieldset is untouched, so the markup's saved state and the svg's visible state disagree, which is exactly the defect P6 exists to catch.** The ruling's "P alone" is P6. V2b/V2c ignore `hidden` and stay PASS. H6 by F5H0-3. |
| W15 | grain | `{D2a, D2b, D2c, D3a}` | UNCHANGED. Kind `grain` runs `era_ph5_grain_gate.py` ALONE against the CSVs; **the page is never built or read in this case**, so no view can enter its set. |
| W16 | grain | `{D5a, D6a}` | UNCHANGED, same reason as W15. |
| W24 | grain | `{D11a, D11b, D11c}` | UNCHANGED, same reason as W15. |
| W30 | page | `{H13a, H6}` | UNCHANGED. One embedded md5 in the manifest block is flipped; nothing on the page's marks changes and no CSV moves, so no D, V or T gate can see it. |
| W31 | input | `{H13b, H13c, D11a, D11b, D11c, H6, T2}` | UNCHANGED — **and this is the case F5H1-2 was written about, so it is re-derived, not carried.** The perturbed cell is Columbus's `usd_per_it_mwh` in `era_ph5_metro.csv`. **V2 reads `era_ph5_stack.csv` and credits only `component_name` and `usd_per_year`, so V2 adds no member to this set.** T2 remains in it for V1's Columbus figure. |
| W32 | page | `{T1, H6}` | UNCHANGED. `47.67` typed into the header caption; one uncredited figure. V2's own figures are all credited, so the count is 1, not more. |
| W33 | page | `{S1, H6}` | UNCHANGED. `#FF0000` inlined on the title. **V2 writes no hex** — its four new CSS rules are all `var(--era-*)` — so S1 sees exactly the one off-token colour. |
| W34 | build | `(nothing)` | UNCHANGED. Two builds compared; V2 is deterministic (fixed metro list, `sorted` on `waterfall_order`, no timestamp, no id). |
| W35 | build | `{S1}` | UNCHANGED. `--era-accent-400` altered in the temp token file. **V2 uses `--era-accent-700`, `--era-accent-200`, `--era-muted` and `--era-rule` — not `--era-accent-400` — so the altered token still reaches the page through the `:root` block only, and S1 fires once.** H5/H6 PASS. |
| N01 | control | `(nothing)` | UNCHANGED. Control, runs LAST. |

**DECLARED RESULT, step 3: 15 of 15 AS DECLARED, W01 first.** Twelve carried, three new.

### §10.4 — Step 4, the render read (a check, never an acceptance — F5Bx-8)

The page is staged into the cloud container and opened under Playwright Chromium at `file://`. Declared:
zero non-`file://` network requests; zero console errors; **exactly one V2 state group with a non-zero rendered
height and it is Columbus**; the excluded band visible on Columbus and separated by its rule. **The file, not the
screenshot, is the measurement.** A render that disagrees with the gate is a finding about the gate, never an
acceptance of the page.

### §10.5 — Checkpoint conditions (from the ruling), restated as things this session will measure

1. eight V2 groups exist — measured by P6 and V2b;
2. Columbus is the visible saved state **with script disabled** — measured from the markup by P6 (the `hidden`
   attributes are in the file) and confirmed by the render, which runs no page script that changes them;
3. the excluded band is present on Columbus, Dallas-Fort Worth and San Jose / Bay Area **only** — measured by
   V2c's count of 3 against G2's three `included_in_mitigated_total = 0` rows;
4. the build-incomplete set is exactly `{V4, V5, V6}` — measured by the FAIL set `{V4a V4b V5a V5b V6a V6b B4}`;
5. the render was read — §11.4;
6. logs from Brad's shell — **this session cannot write them and will not pretend to.** Carried to the closeout
   as an OPEN item exactly as 5H-1 carried it.

### §10.3a — Amendment to §10.3, written after step 2's run and BEFORE the suite runs

**Reason for the amendment.** §10.2's correction is only proven if a page exists that satisfies the 5H-1 form of
V2c and fails the 5H-2 form. W04 is not that page: removing `data-excluded="1"` breaks the mark COUNT, which the
5H-1 form already saw. **A sixteenth case is added so the added clauses have a positive of their own** (F5B-3:
only a declared positive firing proves a gate is connected — and clauses 3 to 5 of V2c are, as of step 2, gates
that nothing has ever fired).

| case | kind | declared firing set | why |
| --- | --- | --- | --- |
| W06 | page | `{V2c, H6}` | The `.era-excluded { ... }` rule is deleted from the page's own `<style>`. **The markup is untouched — all three marks, all three `data-excluded="1"`, all three `data-muted="1"`, all three `<rect class="era-excluded">`, the waterfall order intact.** Only the paint declaration is gone, so the excluded siblings are no longer drawn muted with a hairline. Clause 5 fires and nothing else can: the deleted rule carries no hex (S1), no `font-size` (S2), no family (S3) and none of the grid constants (S4). H6 by F5H0-3. |

**DECLARED sub-measurement, W06's decisive evidence:** the 5H-1 page gate (`era_ph5_page_gate.py`, md5
`00b12bd3ee7f3fbdcdfed74e0331af8d`, kept aside for this) run against W06's page will report **V2c PASS**, and the
5H-2 gate against the same page will report **V2c FAIL**. That pair is what makes "strictly stronger" a
measurement instead of a claim.

**DECLARED RESULT, step 3, superseding §10.3's: 16 of 16 AS DECLARED, W01 first.** Twelve carried, four new.

## §11 — Results, in the order the runs happened

### §11.1 — Step 1, V2 built, 5H-1's gate UNCHANGED — DECLARATION HIT (scratch, device VM, Python 3.10.12)

Gate binary identity at the moment of the run: `era_ph5_page_gate.py` md5 `00b12bd3ee7f3fbdcdfed74e0331af8d`,
byte-for-byte 5H-1's. **Nothing in the gate was touched before this run.**

```
RESULT 68 PASS  7 FAIL  0 SKIP-BLIND  0 SKIP-OK
FAIL SET B4 V4a V4b V5a V5b V6a V6b
```

Every line of §10.1 hit, including all four WEAK counts:

| declared | measured |
| --- | --- |
| 68 PASS / 7 FAIL / 0 SKIP-BLIND / 0 SKIP-OK, 75 rows | exactly that |
| FAIL set `{V4a V4b V5a V5b V6a V6b B4}` | `B4 V4a V4b V5a V5b V6a V6b` |
| V2a, V2b, V2c FAIL → PASS | all three PASS |
| **P6 SKIP-OK → PASS**, the page's last SKIP-OK | `PASS [P] P6  V2 has 8 pre-rendered data-state-metro groups (want 8); the one NOT hidden in the markup is ['Columbus'] (want [Columbus])` |
| T1 `= 0 (70 numeric of 221 text elements scanned)` (WEAK) | verbatim |
| T2 `70 credited figures` (WEAK) | verbatim |
| S5 `3 svg(s)` (WEAK) | verbatim |
| H5/H6 PASS | both PASS |
| exit code 1 | 1 |

**One declaration in §10.3 is wrong and is corrected here rather than edited (this file is append-only and it is
the measurement).** The W33 row says "its four new CSS rules"; **three** were added — `.era-wf-level`,
`.era-wf-delta`, `.era-excluded` — because the excluded band's separator reuses the existing `.era-axis`. The
claim that row actually makes, that V2 writes no hex, is untouched and was measured: W33 fired `{S1, H6}` AS
DECLARED. Recorded as F5H2-7.

### §11.2 — Step 2, the V2c scope correction — DECLARATION HIT

V2c re-scoped exactly as §10.2 declared, before the run and in those five clauses. Header DECLARED line re-written
to §10.1's tally and the unit tag moved to `Unit 5H-2`.

```
RESULT 68 PASS  7 FAIL  0 SKIP-BLIND  0 SKIP-OK
FAIL SET B4 V4a V4b V5a V5b V6a V6b
```

**The per-gate-id status diff between step 1 and step 2 is EMPTY** — identical status on all 75 ids. A scope
correction that moved the tally would have meant the markup was wrong, not the gate. V2c now reads:

```
PASS [V] V2c  excluded siblings drawn: 3 marks for 3 rows; all data-muted=True; all in the waterfall order=True;
              all carrying <rect class=era-excluded>=True; .era-excluded is fill var(--era-muted) + stroke
              var(--era-rule) in the page CSS=True
```

### §11.3 — Step 3, the tamper suite — 16 of 16 AS DECLARED, first run, W01 leading

`BASELINE  clean page FAIL set == declared build-incomplete set (7 ids)` — the harness was connected before a case
ran. Then `RESULT 16 of 16 AS DECLARED (W01 ran first, V1 built)`, 0.86 s for the suite on the VM.

**Twelve carried sets, every one re-derived in §10.3 against the page with V2 on it, every one HIT unchanged.**
The re-derivation was not decoration: W31 is the case F5H1-2 was written about, and the derivation this time
states WHY V2 adds no member (V2 reads `era_ph5_stack.csv` and credits only `component_name` and `usd_per_year`;
the perturbed cell is `usd_per_it_mwh` in `era_ph5_metro.csv`).

Four new, all AS DECLARED on the first run: **W03** `{V2b, V2c, H6}`, **W04** `{V2c, H6}`, **W05** `{P6, H6}`,
**W06** `{V2c, H6}`. W04 is the ruling's "V2's exclusion gate alone" — V2b stayed PASS on it, which is what makes
the firing scoped. W05 is the ruling's "P alone" — P2 and P4 stayed PASS, so the case proves P6 catches a control
and an svg that disagree, which is the only defect it exists for.

**The W06 sub-measurement, declared in §10.3a and decisive:** the two gates run against the SAME page, whose
markup is untouched (3 `data-excluded="1"`, 3 `data-muted="1"`, 3 `<rect class="era-excluded">`, waterfall order
intact) and whose `.era-excluded` CSS rule is deleted —

```
5H-1 gate (kept aside, md5 00b12bd3ee7f3fbdcdfed74e0331af8d):  PASS [V] V2c  ... 3 marks for 3 rows, all muted
5H-2 gate                                                   :  FAIL [V] V2c  ... .era-excluded is fill
                                                               var(--era-muted) + stroke var(--era-rule) in the
                                                               page CSS=False
```

**"Strictly stronger" is now a measurement, not a claim.** A page on which the excluded siblings are not drawn
muted at all satisfied the gate this unit inherited.

### §11.4 — Step 4, the render — DECLARATION HIT (cloud container, Playwright Chromium 1194, `file://`)

Run twice on the staged page (md5 `5cc46cd8…`), once with **JavaScript disabled** and once enabled. **Identical
results in both**, which is the point: the saved state is in the markup.

| declared | measured (both runs) |
| --- | --- |
| zero non-`file://` network requests | `[]` |
| zero console errors | `[]` |
| exactly one V2 state group with non-zero rendered height, and it is Columbus | 8 groups, one with height: `["Columbus", 216]` — **with script disabled** |
| the excluded band visible on Columbus, separated by its rule | see below |

Columbus's five rows, read out of the rendered DOM in document order — the waterfall order, the excluded sibling
last:

| `data-component` | class | rect x, w (px) | computed fill / stroke | label | value |
| --- | --- | --: | --- | --- | --- |
| `DCT-T` | `era-wf-level` | 364, 263 | `#1B3855` / none | DCT-T | 546,655,609.92 |
| `M-COL-EXCISE` | `era-wf-delta` | 620, 7 | `#A2C2E2` / none | Ohio kWh excise self-assessment | -16,187,651.92 |
| `M-ALL-STORAGE/B100-4H/FLAT` | `era-wf-delta` | 619, 1 | `#A2C2E2` / none | B100-4H battery, FLAT dispatch | -1,396,828.58 |
| `TOTAL` | `era-wf-level` | 364, 255 | `#1B3855` / none | mitigated total | 529,071,129.42 |
| `M-COL-VOLT` | `era-excluded` | 364, **89** | **`#8799AB` / `#CCD7E3`** | voltage sibling DCT -> DCT-T | -184,527,629.75 |

**Style rule 3 is verified in COMPUTED style, not in CSS text:** `rgb(135,153,171)` is `--era-muted` and
`rgb(204,215,227)` is `--era-rule`. Levels resolve to `--era-accent-700` and deltas to `--era-accent-200` — style
rule 1's two ends of the one ramp, and no second hue anywhere. One separator line inside Columbus's group,
`y=216`, `x 0 → 1184`, stroke `--era-rule`.

The excluded rect is 89 px: `|-184,527,629.75| / 1,428,314,506.82 x 688 = 88.9`. **The scale is arithmetic that
can be checked off the page, which is the point of drawing it at all.** The storage step is the declared one
pixel — the disclosed `max(w, 1)`.

**The file, not the screenshot, is the measurement (F5Bx-8).** The render agreed with the gate on every point.

### §11.5 — Cross-interpreter determinism, with three views on the page

`5cc46cd85c25a6c34a14de0e7004fd18`, 170,232 B, from **Python 3.10.12 twice on the device VM from two different
directories** (scratch, then the project folder) **and from Python 3.11.15 in the cloud container**, which also
reproduced `68 PASS / 7 FAIL / 0 SKIP-BLIND / 0 SKIP-OK` and the same FAIL set. Extends F5H1-6 and F5H0-5.

## §12 — State after the unit, and findings

**Unchanged, measured on the mount after every run:** `era_rates.db` `1c72e7a1b32c99a650d2e1fba17ae21e`; the four
grains at their E-1.4 pins (`84fe4dbf…`, `3e8825ac…`, `f5b3638a…`, `fc1fa4b1…`); manifest `d28ed340…`; style
`88704aa9…`; dictionary `41d01c84…`. **Retired files untouched and unread by anything this unit ran:**
`era_ph5_dashboard.twb` `20dcb01d…`, `era_ph5_workbook_gate.py` `689b1354…`. `era_ph5_grain_gate.py` `7c1cf9a3…`
unchanged. No SQLite write. No `.tmp` left on the mount. **Brad's committed 5H-1 logs untouched** (`29735baf…`,
`a386d55e…`) — this session wrote no log to the mount.

**Changed or new on the mount:**

| file | md5 | what |
| --- | --- | --- |
| `era_ph5_views.py` | `2c8b77c10da5e99279df13939ee93de6` | `view_v2` + the V2 geometry constants + `render()` dispatch |
| `era_ph5_build_html.py` | `f8f5d642a67b65913f2aa3f680b75c45` | dispatch via `render()` (each view gets the grain it reads); three CSS mark classes |
| `era_ph5_page_gate.py` | `b2dfb2ef2b4e2ba215558836933fd62f` | **V2c re-scoped to the DRAWING and the page's own CSS (F5H2-1)**; header declares §10.1's tally, tagged `Unit 5H-2` |
| `era_ph5_page_tamper.py` | `b7c01cb0297965ba1a1ee062fe61040f` | `BASELINE` = the seven; **W03, W04, W05, W06 added**; every carried set re-derived (F5H1-2) |
| `era_ph5_dashboard.html` | `5cc46cd85c25a6c34a14de0e7004fd18` | 170,232 B, V1 + V2 + V3 drawn |

**Checkpoint (§10.5):** items 1, 2, 3, 4 and 5 MEASURED HIT. **Item 6 is OPEN**: `era_ph5_5h_gate_run.log` and
`era_ph5_5h_tamper_run.log` must be re-written from Brad's shell (F5B-9). This session did not and cannot write
them; the closeout hands him the commands. **5H-3 checks for headers reading `Unit 5H-2` before it treats this
unit as complete, and does not take this paragraph as fact.**

### Findings

- **F5H2-1. A gate written before its artefact can also PASS for an insufficient reason, not only fail for a
  declared one — and that is harder to see.** F5H1-1 caught the first form: V1b/V1c failed, loudly, for reasons
  declared in advance. V2c did the opposite. It asserted the mark COUNT and `data-muted="1"` — **both attributes
  the build writes about itself** — and it would have been satisfied by three empty `<g>` elements carrying two
  attributes and no mark at all, on a page where the excluded siblings were not drawn muted anywhere.
  **Measured, not argued (§11.3):** the 5H-1 gate reports V2c PASS on W06's page; the 5H-2 gate reports FAIL.
  The correction was declared in §10.2 BEFORE it was written and BEFORE step 1 ran, so it is on record as a
  correction of scope and not a reaction to a result; the tally did not move; W06 is its positive control.
  **Rule for 5H-3 and every unit after: when the first built instance of a view arrives, ask not only "does this
  gate fire when I break the view" but "could this gate be satisfied by markup that does not do what the ruling
  says". An attribute the build writes is a claim; assert the drawing and the page's own CSS.**
- **F5H2-2. The §9 convention "nothing else in the build changes" was not achievable, and the reason is
  structural.** The 5H-1 build calls every view as `fn(grains["G1"])`. **V2 is the first view that does not read
  G1**, so a dispatch change was required, not optional. It is `era_ph5_views.render(view_id, grains, metros,
  saved_metro)`. The convention was written by 5H-1 before V2's grain was in view — it is under-specified in the
  same way F5H1-1's ruling text was, not wrong. **The change is also a net reduction in risk:** the metro order
  and the saved metro now have exactly ONE definition reaching the page (the build's `METROS` / `SAVED_METRO`),
  which is the same list P4 gates the control against, so P4 and P6 cannot drift apart. V4 (G1), V5 (G1) and V6
  (G4) each get one line in `render()`.
- **F5H2-3. The excluded siblings have no position in the walk, and the drawing must not invent one.** G2 leaves
  `waterfall_start_usd` and `waterfall_end_usd` EMPTY on exactly the three `included_in_mitigated_total = 0`
  rows. Anchoring the band at the mitigated total and extending it leftward would draw "what the total would have
  been", asserting an additivity the frozen contract does not carry — the sibling is a different service, not a
  line item. **The band is anchored at zero: this quantity exists, at this size, and it is not in the total.**
  Recorded so that no later unit "improves" it into a would-be total.
- **F5H2-4. The waterfall's step bars read as isolated ticks without connectors.** Columbus's excise step is 7 px
  and its storage step 1 px against level bars of 263 and 255 px, and the steps sit at the right-hand end of the
  levels where the walk actually happens. **The geometry is correct and the proportions are honest** — the whole
  argument of the view is that the avoidable part is small — but "this comes off that" is currently carried by
  position alone. A hairline connector from each step's end down to the next step's start would carry it
  visually. **Routed to 5H-4** (assembly and aesthetic conformance), beside F5H1-4. It is a drawing change, not a
  data change, and no gate sees it.
- **F5H2-5. The zero-typed-figures rule is not only about dollars: a component NAME can be a figure.** Eight of
  G2's `component_name` values contain `B100`, a three-digit run, which `FIGURE_RE` reads as a figure — so a
  plain row label would have counted as an uncredited figure in T1. **The truthful fix is to credit the label and
  the `<title>`: `data-src="era_ph5_stack:<metro>|<component_id>:component_name"`.** The text IS the cell, T2
  then string-compares it, and nothing was suppressed or reworded to get past a gate. **5H-3 must credit every
  label it draws from a grain the same way; V6's caveat table, which is nothing but grain text, will hit this
  hardest.**
- **F5H2-6. Cross-interpreter determinism holds with three views on the page.** `5cc46cd8…` from Python 3.10.12
  on the device VM twice from two different directories and from Python 3.11.15 in the cloud container, with the
  same gate tally on both. Extends F5H1-6 and F5H0-5. **Brad's 3.13.x remains 5H-4's measurement.**
- **F5H2-7. This session's own §10.3 said "four new CSS rules"; three were added.** The excluded band's separator
  reuses `.era-axis` rather than declaring a fourth rule. The claim that row makes — V2 writes no hex — is
  unaffected and was measured (W33 AS DECLARED). **Recorded, not edited:** the results file is append-only
  because it is the measurement, and a declaration that missed is corrected beside itself, never in place.
- **F5H2-8. P6 was the page's last SKIP-OK and it turned PASS.** The page gate now reports **0 SKIP-OK and 0
  SKIP-BLIND**; every remaining FAIL is a build-incomplete slot and nothing on the page is unmeasured. F5H0-7
  ("a SKIP-OK must turn PASS or FAIL as its slot fills") has now been exercised on every slot it was written for
  — P7, S5 and T2 by 5H-1, P6 by this unit.

### Routed

**NO RULING IS PENDING.** Two items for the strategy chat's next memory pass, neither a ruling request:

1. **F5H2-2** — the handoff convention "nothing else in the build changes" could not hold; the dispatch change was
   structural and is recorded above with its reasoning.
2. **F5H1-5 still stands** from 5H-1 (the three headline channel totals exist in no cell). Nothing in this unit
   touched it.

**To 5H-4:** F5H2-4 (waterfall connectors) joins F5H1-3 (harden T2's U+2212 normaliser to translate, not strip)
and F5H1-4 (nudge a credited label clear of the zero rule when its row extent is under one grid unit).

### Conventions 5H-3 must follow (V4, V5, V6)

- A built slot drops `data-status="build-incomplete"`; `era_ph5_views.py` gains `view_v4`, `view_v5`, `view_v6`,
  registers each in `VIEWS`, **and adds one line each to `render()`** — V4 and V5 read G1, V6 reads G4. That is
  the whole build change; the CSS gains only `var(--era-*)` classes.
- **Credit every label drawn from a grain, not only every dollar (F5H2-5).** V6 is a table of grain text and will
  be almost entirely credited text; a `<title>` counts as text and is scanned.
- Row key for a credited G4 figure is `era_ph5_caveat:<caveat_id>:<column>`; for G1 it is `era_ph5_metro:<metro>`.
  **ASCII hyphen-minus** in every figure (F5H1-3).
- **B4 goes live with V5 and must turn PASS**: any band-crossing figure the page shows carries `data-src` to G4
  `C-BAND-25`, the FACILITY figure (F5A-4). B3 already forbids the metered literals as page text — do not undo it.
- **V6 must be reachable in one click from the page top (P5-3).** V6c already PASSES on the header anchor; do not
  move or rename the `#V6` target.
- **Ask of every new V gate: could it be satisfied by markup that does not do what the ruling says (F5H2-1)?**
  Declare the answer in writing before the run, and correct SCOPE, never a threshold.
- **Re-derive every tamper set against the page as it then stands (F5H1-2).** The declared baseline after 5H-3 is
  **empty** — 5H-3 is the unit in which the page gate first reaches 0 FAIL and the page is accepted (exit 0), so
  the harness's `BASELINE` becomes `set()` and every firing set is absolute. W01 still leads.

---

# Unit 5H-3 — the honesty layer: V4 the map, V5 the intervals, V6 the caveats

`direction_ph5_html_v1.0.md` Unit 5H-3; view text from `direction_ph5_tableau_v1.0.md` Unit 5C (V4, V5, V6);
conventions from §12 of this file. Append-only: every declaration below was written BEFORE the run it predicts.

## §13 — Declared expectations, written before any run of this unit

### §13.0 — Step 0, the state this unit checked before anything else (the handoff's "gate the page on disk first")

Read off the mount by this session, not taken from any description:

| item | measured | declared by 5H-2 | verdict |
| --- | --- | --- | --- |
| `era_ph5_dashboard.html` md5 | `5cc46cd85c25a6c34a14de0e7004fd18` | `5cc46cd8…` | MATCH |
| page gate, re-run by this session | 68 PASS / 7 FAIL / 0 SKIP-BLIND / 0 SKIP-OK | same | MATCH |
| FAIL set | `B4 V4a V4b V5a V5b V6a V6b` | `{V4a V4b V5a V5b V6a V6b B4}` | MATCH |
| `era_ph5_5h_gate_run.log` header | `era_ph5_page_gate.py  Unit 5H-2  project=C:\Users\User\Claude\Projects\Electrical Rate Analysis  python=3.13.5  page_md5=5cc46cd8…` | must read `Unit 5H-2` | **PRESENT** |
| `era_ph5_5h_tamper_run.log` header | `era_ph5_page_tamper.py  Unit 5H-2  project=C:\Users\User\…  python=3.13.5`, `RESULT 16 of 16 AS DECLARED` | must read `Unit 5H-2` | **PRESENT** |
| `era_ph5_views.py` / `era_ph5_build_html.py` / `era_ph5_page_gate.py` / `era_ph5_page_tamper.py` | `2c8b77c1…` / `f8f5d642…` / `b2dfb2ef…` / `b7c01cb0…` | same four | MATCH |
| `direction_ph5_html_v1.0.md` | `d9f17e127fa8ad7ace74d9c15630da4a` | in force | MATCH |

**5H-2 checkpoint item 6 is CLOSED, not open.** The handoff instructed this session to record it as still open if the
headers did not read `Unit 5H-2`. They do, on both logs, with `project=C:\Users\User\…` and `python=3.13.5` — Brad's
shell, not a session's. **5H-2 is therefore closed on every item**, and this unit is not blocked. Recorded here because
the handoff prompt required the check and the answer is the opposite of the one it was written for.

### §13.1 — What V4, V5 and V6 will draw, and the basis question V5 forces

**V4 — the map.** Eight `<circle data-role="point" data-metro>` on a plate-carrée (plain equirectangular) frame:
`x` linear in `station_longitude`, `y` linear in `station_latitude` with north up, **one degrees-to-pixels scale
shared by both axes** — that is what makes it plate carrée rather than an arbitrary stretch. Frame drawn as four
`<line class="era-axis">`; **no basemap, no outline file vendored — the ruling's default: none.** Colour by
`usd_per_it_mwh` on the seven-step ramp (`era-ramp-0…6`), the same ramp V1 uses. Each point carries a metro label
and a **state label in caption size**, both credited (F5H2-5). Least ink: eight dots, four rules, sixteen labels,
no graticule, no axis figures. `station_latitude`/`station_longitude` are a weather STATION and not a site —
C-STATION-POINT says so and V6 prints it.

**V5 — the intervals.** Five interval rows, one shared linear scale:
three **bands** (`is_market_priced = 1`: Dallas-Fort Worth, Columbus, Chicago) from
`band_low_usd_per_it_mwh` → `band_high_usd_per_it_mwh` with a central mark at `usd_per_it_mwh`;
two **published pairs** (`has_bracket = 1`: Chicago, Northern Virginia) from
`bracket_low_usd_per_it_mwh` → `bracket_high_usd_per_it_mwh`, **drawn as intervals, not as two bars** (5C).
Bands first in `rank` order, then brackets in `rank` order. Domain measured off G1: 37.4607 … 98.5005.
Chicago appears twice because it is two different objects — a market band and an unratified pair.

**THE BASIS PROBLEM, DECLARED BEFORE THE BUILD.** The ruling asks V5's one touched adjacency to be annotated
"by name and by number" from `C-BAND-25`, and F5A-4 fixes that number as **the FACILITY figure, 0.8042**.
Measured this session off G1:

- Columbus `band_high_usd_per_mwh` 70.81617743 − Chicago `usd_per_mwh` 70.01194141 = **0.80423602** → this IS
  C-BAND-25's facility figure, and it confirms G1's `usd_per_mwh` is the published facility basis, not Phase 2's
  metered one (whose crossing, 0.9742, B3 bans as page text and G1 does not carry).
- Columbus `band_high_usd_per_it_mwh` 82.62057382 − Chicago `usd_per_it_mwh` 81.53954845 = **1.08102537**.

**V5 is ruled to be drawn on the $/IT-MWh axis.** 0.8042 is the crossing on the $/MWh axis. **Printing 0.8042 beside
an IT-basis drawing would be a basis mismatch — precisely the error F5A-4 exists to prevent** — and printing 1.0810
would be a derived figure that exists in NO cell of any grain (it is a difference of two cells), which is F5H1-5's
shape exactly. **Declared resolution: V5 prints neither.** The crossing is carried by
(i) the **two endpoint cells themselves**, each printed and each credited to its own G1 column — Columbus's
`band_high_usd_per_it_mwh` and Chicago's `usd_per_it_mwh` — and
(ii) the **drawing**: Columbus's band rect extends strictly past Chicago's central mark.
The annotation names the adjacency from G4, credited `era_ph5_caveat:C-BAND-25:title`, rendered verbatim.
This is the same ruling F5H1-5 already made for V3's channel totals and F5H2-3 made for the excluded band: a figure
whose basis the contract cannot express is a figure this page does not type. **Do not "improve" it into 0.8042.**

**V6 — the caveats.** `<table data-view="V6">`, 21 `<tr data-caveat>` in `sort_rank` order, C-FERC-H13 first with no
dollar. Columns: `caveat_id`, `category`, `title`, `metro_scope`, `priced`, `usd_per_year`, `usd_per_it_mwh` —
**every cell credited `era_ph5_caveat:<caveat_id>:<column>` and rendered from that row's own cell.**
`usd_per_year` at two decimals with comma groups; `usd_per_it_mwh` at **six** decimals, which is the grain's own
precision — four decimals would put C-SJ-PF (−0.813647 → −0.8136, error 0.000047) at 94 % of T2's tolerance, and a
gate that passes by 6 % of a margin is not a gate. ASCII hyphen-minus throughout (F5H1-3).

**`statement` IS DELIBERATELY NOT A COLUMN OF V6.** C-BAND-25's `statement` cell contains the literal `0.9742`,
which B3 forbids as page text (F5A-4). Rendering the statement column would fire B3 on the honesty table itself.
The statements remain on the page in full, in the embedded G4 JSON, where H13 proves them fresh — nothing is hidden,
it is not rendered as text. 5C asks for "scope, dollars where they exist, and priced/unpriced"; those are the seven
columns above.

### §13.2 — The gate scope corrections, declared BEFORE they are written and BEFORE any build (F5H2-1)

**The question F5H2-1 requires of every new V gate — "could this gate be satisfied by markup that does not do what
the ruling says?" — asked and answered for all five gates this unit turns live. Four of the five answers are YES as
the stubs stand.** Corrections are of SCOPE, never of a threshold; each makes the gate assert MORE.

| gate | stub as 5H-2 left it | could markup that does not do what the ruling says satisfy it? | correction |
| --- | --- | --- | --- |
| **V4a** | `<svg data-view=V4>` exists | **NO.** `find_view` requires a body element of tag `svg` carrying `data-view="V4"` inside a slot that has dropped `data-status`. An existence gate is all it claims to be. | none |
| **V4b** | `len(pts) == 8` where `data-role="point"` | **YES, badly.** Eight empty `<g data-role="point">` — an attribute the build writes about itself — with no circle, no coordinates and no colour would PASS. It asserts nothing about the projection the ruling names. | re-scoped to assert the DRAWING: (1) the eight points' `data-metro` set equals G1's eight; (2) **plate-carrée consistency, re-derived from the grain, not from the build's constants** — over all 28 point pairs, `Δcx / Δlon` is one constant and `Δcy / Δlat` is one constant (±1.5 px for integer rounding); (3) `scale_x == scale_y` to within 1 % — equal degrees per pixel on both axes; (4) `cy` DECREASES as latitude increases (north up); (5) each point's `era-ramp-N` class index equals `ramp_index(usd_per_it_mwh)` re-derived from G1. Clause (2) catches a swapped lat/lon, a sign error and a constant position; clause (5) catches a decorative palette. |
| **V5a** | `<svg data-view=V5>` exists | **NO.** Same as V4a. | none |
| **V5b** | `len(iv) >= 3` | **YES, and the gate's own description misstates it.** It is named "V5 intervals span band_low/band_high" and asserts no such thing: three empty `<g data-role="interval">` would PASS, and `>=` would accept any number. | re-scoped: (1) the interval set equals **exactly** `{(metro,"band") : is_market_priced=1} ∪ {(metro,"bracket") : has_bracket=1}` re-derived from G1 — 3 + 2 = 5, no more, no fewer; (2) **one affine map**: over every low edge, high edge and central mark drawn in V5, `Δx / Δvalue` is one constant against the cells those marks cite (±1.5 px), which is what "the intervals span band_low/band_high" actually means; (3) every band row carries a central mark credited to `usd_per_it_mwh`. |
| **V6a** | `<table data-view=V6>` exists | **NO.** Same as V4a, tag `table`. | none |
| **V6b** | ids == sort_rank order, 21 rows, FERC first | **YES.** A table of 21 `<tr data-caveat>` carrying that attribute and NO text at all would PASS — `data-caveat` is again an attribute the build writes about itself — and two of the three things the gate's description claims ("unpriced above limitations", "with no dollar") are not asserted anywhere in it. | re-scoped, keeping the three existing clauses and adding: (4) every row carries ≥ 5 cells, **each credited to that row's OWN `caveat_id`** — a row may not borrow another row's credit; (5) the `C-FERC-H13` row shows **no dollar figure** in either dollar column; (6) every row whose drawn `category` text is `unpriced` sits strictly above every row whose drawn `category` text is `limitation`. |
| **B4** | `bool(cross)` and all crossing `data-src` start `era_ph5_caveat:C-BAND-25:` | **YES.** One `<g data-role="crossing" data-src="era_ph5_caveat:C-BAND-25:title">` with no text and no position would PASS while the page showed no crossing at all. | re-scoped: (1) ≥ 1 `data-role="crossing"` element, every one credited to a `C-BAND-25` column **and its rendered text equal to that cell**; (2) the page shows, credited, **both endpoint cells** — Columbus `band_high_usd_per_it_mwh` and Chicago `usd_per_it_mwh`; (3) **the crossing as GEOMETRY**: the drawn right edge of Columbus's band rect is strictly right of the drawn x of Chicago's central mark. Clause (3) is what makes B4 a gate on the drawing rather than on a claim. |

**None of the six corrections moves a threshold; every one makes its gate assert more.** The declared tally in
§13.3 is the tally AFTER these corrections are written, so a correction cannot be a reaction to a result.

### §13.3 — Step 1 and 2, the build and the corrected gate. Declared tally.

Build change, per §12's convention: `era_ph5_views.py` gains `view_v4`, `view_v5`, `view_v6`, registers each in
`VIEWS`, and `render()` gains one line each — V4 and V5 read G1, V6 reads G4. The CSS gains only `var(--era-*)`
classes (declared: **two** — `.era-band` and `.era-bracket`; V4 reuses `.era-axis` and `.era-ramp-N`, V6 reuses the
existing type classes plus `.era-t*` table rules that carry no hex and no px). No other build change.

**DECLARED, before the run: 75 PASS / 0 FAIL / 0 SKIP-BLIND / 0 SKIP-OK. FAIL SET EMPTY. The page gate exits 0 and
the page is ACCEPTED for the first time.** 68 + the seven that were build-incomplete = 75, no gate added, none removed.

Secondary declarations, all WEAK where marked:

- T1's uncredited numeric count is **0** page-wide over six views (the hard requirement of the unit).
- T1's scanned/numeric tally (**WEAK**, an exact count of a thing being built for the first time): scanned rises from
  221 by V4's 16 labels + 8 titles, V5's 13 value labels + 5 titles + 1 crossing annotation, and V6's 21 × 7 cells +
  7 headers ≈ **418**; numeric rises from 70 by V5's 13 and V6's 21 `priced` + 9 `usd_per_year` + 7
  `usd_per_it_mwh` + one title containing `1.95` ≈ **121**. **Both counts are weak; the ZERO is not.**
- S5 counts **5** svgs (V1, V2, V3, V4, V5), every width/height a multiple of 8. V6 is a table and adds no svg.
- B3 stays PASS: `0.9742` and `0.97` appear nowhere as page text — the reason `statement` is not a V6 column.
- V6c stays PASS on the header `#V6` anchor, unmoved and unrenamed.
- D, H, H13, P groups unchanged and PASS; the page stays one file, under 4 MB, with nothing fetched.
- Page size rises from 170,232 B by roughly 30 KB of V6 table markup (**WEAK**).

### §13.4 — Step 3, the tamper suite, declared before it runs

**`BASELINE` becomes `set()`** — 5H-3 is the unit in which the clean page's FAIL set is empty, so every firing set
below is ABSOLUTE, not relative. The harness aborts NOT CONNECTED if the clean baseline is not empty.

**Every carried case re-derived against the page as it will then stand (F5H1-2). A declared set is not inherited.**
Sixteen carried; **fifteen hold and ONE GROWS**:

| case | carried set | re-derivation against a six-view page | 5H-3 set |
| --- | --- | --- | --- |
| W01 | {V1c, H6} | asserts `data-field="mitigated_usd_per_it_mwh"` occurs exactly 8 times. V4 writes `usd_per_it_mwh`, V5 writes `band_low/high_usd_per_it_mwh` and `usd_per_it_mwh`, V6 writes G4 columns — **none writes `mitigated_usd_per_it_mwh`**, so the count is still 8 and the edit stays scoped to V1. | unchanged |
| W02 | {V3b, H6} | `data-channel` is written by V3 alone; no new view writes it. | unchanged |
| W03 | {V2b, V2c, H6} | keys on `<g data-component="M-COL-VOLT" …>`; no new view writes `data-component`. | unchanged |
| W04 | {V2c, H6} | as W03. | unchanged |
| W05 | {P6, H6} | keys on `data-state-metro`; V4/V5/V6 pre-render no control state. | unchanged |
| W06 | {V2c, H6} | deletes the `.era-excluded` CSS rule; the two new rules are `.era-band`/`.era-bracket` and neither contains that string. | unchanged |
| W15 | {D2a, D2b, D2c, D3a} | `grain` kind — runs the grain gate alone; no page is built. | unchanged |
| W16 | {D5a, D6a} | as W15. | unchanged |
| W24 | {D11a, D11b, D11c} | as W15. | unchanged |
| W30 | {H13a, H6} | edits one embedded md5; independent of what is drawn. | unchanged |
| **W31** | {H13b, H13c, D11a, D11b, D11c, H6, T2} | **GROWS.** Columbus `usd_per_it_mwh` +200 on disk after the build. T2 still fires (V1 credits 69.26 against that cell). **But V4b's clause (5) now re-derives Columbus's ramp index from the perturbed cell and gets a different index than the class the clean build drew → V4b FIRES. And V5b's clause (2) re-derives the affine map with Columbus's central mark citing a cell that moved 200 while its drawn x did not → V5b FIRES.** B4 stays PASS: its cells (`band_high_usd_per_it_mwh`, Chicago's central) were not touched and the geometry did not move. V1/V2/V3 gates stay PASS. **This is F5H1-2 repeating exactly as it did in 5H-1: a credited figure is a freshness assertion, and now so is a colour and a position.** | **{H13b, H13c, D11a, D11b, D11c, H6, T2, V4b, V5b}** |
| W32 | {T1, H6} | types `47.67` into the header caption; unaffected by the views. | unchanged |
| W33 | {S1, H6} | `#FF0000` on the title; the new CSS carries no hex. | unchanged |
| W34 | (nothing) | two builds compared; determinism is unaffected by view count. | unchanged |
| W35 | {S1} | rebuild from altered tokens, gate reads the originals; new views paint only through `var(--era-*)`. | unchanged |
| N01 | (nothing) | clean control, runs last. | unchanged |

**Seven new positives, one per new clause — a clause nothing has ever fired is not yet a gate (5H-2's W06 rule):**

| case | kind | declared firing set | what it proves |
| --- | --- | --- | --- |
| **W07** | page | {V4b, H6} | Columbus's point `cy` shifted +40 px. Plate-carrée consistency (clause 2) breaks on every pair involving Columbus; the point count, the metro set and the ramp classes are untouched, so the firing is scoped to the PROJECTION. V4a, T1, T2, S1 stay PASS. |
| **W13** | page | {V4b, H6} | Columbus's `class="era-ramp-3"` swapped for `era-ramp-6` — still a token class, so **S1 stays PASS** — and no coordinate moves. Fires clause (5) alone. W07 and W13 fire V4b through two different clauses, which is how "V4 has 8 points" stops being one assertion pretending to be five. |
| **W08** | page | {V5b, H6} | Dallas-Fort Worth's band rect width halved: the rect no longer spans its two cells, so the affine map (clause 2) breaks. DFW is chosen deliberately — **B4 stays PASS**, because the crossing geometry it gates is Columbus against Chicago. V5a and the interval SET stay PASS. |
| **W09** | page | {B4, H6} | the `data-role="crossing"` annotation element is DELETED. `bool(cross)` fails. V5a/V5b stay PASS (the intervals are untouched), T1/T2 stay PASS (the annotation is non-numeric credited text). **This is B4 fired alone**, and it is the positive that puts B4 live. |
| **W10** | page | {V6b, H6} | two adjacent `data-caveat` row ids swapped. Clause (1) — order equals `sort_rank` — fires. The cells and their credits move with the ids, so **T2 stays PASS**: the firing is scoped to ORDER. |
| **W11** | page | {V6b, H6} | the `C-FERC-H13` row's empty `$/yr` cell is replaced by `<td data-src="era_ph5_caveat:C-F4B-3:usd_per_year">0.00</td>`. Fires clause (5) — the FERC row now shows a dollar — and clause (4) — a cell credited to another row. **T1 and T2 stay PASS** (it is credited, and 0.00 does equal C-F4B-3's cell), which is the point: V6b's new clauses are live and independent of group T. |
| **W12** | page | {V6b, T2, H6} | `C-CHI-5CP`'s drawn `category` text changed from `limitation` to `unpriced`, no row moved. Fires clause (6) — an `unpriced` row now sits below `limitation` rows. **T2 fires alongside and that is a true consequence**, declared: the drawn text no longer equals the cell it cites. Declared as a two-gate firing rather than engineered into a one-gate firing, because rewording the credit to make it fire alone would be exactly the "reword a label to slip past a gate" F5H2-5 forbids. |

**Order:** W01 first, always (F5B-3); then W02…W35 in id order; N01 last. A run that does not lead with W01 is refused.
**Declared: 23 of 23 AS DECLARED.**

### §13.4a — Amendment to §13.4, written after step 2's run and BEFORE the suite runs

**W12's declared row cannot fire the clause it was written for.** §13.4 named `C-CHI-5CP`. Measured off G4 after
step 2: the drawn `category` sequence puts the three `unpriced` rows at indices 0, 1, 2 and the ELEVEN
`limitation` rows at indices **8 through 18** — `C-CHI-5CP` is itself the FIRST limitation row, at index 8.
Re-marking it `unpriced` gives `max(unpriced) = 8` against `min(limitation) = 9`, which still satisfies clause (6).
The case would have fired `{T2, H6}` and NOT `V6b`, and would have been recorded as a MISS.

**Corrected before the run, beside the original and not in place of it (F5H2-7): W12 re-marks
`C-STATION-POINT` (index 18, the LAST limitation row) from `limitation` to `unpriced`.** Then
`max(unpriced) = 18` against `min(limitation) = 8` and clause (6) fires. Declared set is unchanged:
**{V6b, T2, H6}** — V6b by clause (6), T2 because the drawn text no longer equals the cell it cites, H6 by
construction (F5H0-3). This is the same failure mode 5H-2 recorded as F5H2-1 seen from the other side: a clause
can be *unfirable by the tamper chosen for it* as easily as it can be *satisfiable by markup that does nothing*,
and only writing the positive down and checking it against the artefact finds either.

No other case changes. §13.4's table stands as written.


### §13.4b — W12 MISSED on its first run. The miss, its cause, and the T2 scope correction, written BEFORE the re-run

**Recorded as a MISS, not repaired into a pass (4A).** First run of the 23-case suite: **22 of 23 AS DECLARED**.

```
CASE W12  MISS  (page)
  declared: ['H6', 'T2', 'V6b']
  actual  : ['H6', 'V6b']
  DECLARED BUT SILENT: ['T2']
```

**Cause — and it is a gate gap, not a tamper defect.** §13.4 declared that re-marking a drawn `category` cell
would fire T2 "because the drawn text no longer equals the cell it cites". It does not. **Group T only ever looks
at NUMERIC text.** `T1` counts text matching `FIGURE_RE`/`NUMBER_RE` that carries no `data-src`; `T2` then
compares *that same numeric subset* against its cells. A credited label whose content is not numeric is collected
by neither. `limitation` → `unpriced` is not numeric, so nothing in group T ever read it.

**This is F5H2-1's question asked of group T instead of a V gate, and group T fails it.** §12's own convention —
"credit every label drawn from a grain, not only every dollar (F5H2-5); a `<title>` counts as text and is
scanned" — rests on a premise that was only half true: such labels are scanned for the PRESENCE of a credit
(and only when numeric), never for whether they equal the cell they claim. **V6 is 21 rows × 4 non-numeric
credited columns = 84 labels, plus V4's 24 and V5's 11 and V2's 40 — roughly 159 credited labels on this page,
none of them checked against its cell.** A build could have cited any cell it liked beside any text it liked.

**Correction, declared here before it is written, and it is SCOPE not threshold (F5H1-1):**

> **T2 is widened from "every credited NUMERIC text" to "every credited text".** The comparison already branches:
> content that parses as a number is compared to the cell within the precision shown (unchanged, to the cent);
> content that does not is compared to the cell as a string (the branch that already existed for figures embedded
> in prose, such as C-OHIO-EXCISE's title). **No tolerance moves and no id is added — the gate count stays 75.**
> T1 is untouched: its duty is the uncredited-numeric ZERO, and that is the unit's hard requirement.

**Asking F5H2-1's question of the corrected T2: could it be satisfied by markup that does not do what the ruling
says?** A credited label could still be placed anywhere, or hidden — T2 asserts identity of text to cell, not
position or visibility. That much is genuinely outside T's duty and inside V's, and V4b, V5b and V6b now assert
placement for the three views this unit builds. What T2 can no longer be satisfied by is **a label that cites one
cell and shows another** — which is the specific thing the page's whole "zero typed figures" claim depends on and
which nothing on this page tested until now.

**Every carried tamper set re-derived against the widened T2 (F5H1-2), before the re-run.** W12 gains the
declared T2. **Nothing else moves:** W01/W02 touch `data-field`/`data-channel`, not `data-src`; W03 deletes a
whole credited group so the survivors still equal their cells; W04/W05/W06 change attributes and CSS only;
W07/W08/W13 change geometry and a class; W09 deletes a credited element; W10 moves whole rows with their credits;
W11's substituted cell shows `0.00` and C-F4B-3's cell *is* `0.00`; W31 already fires T2; W30/W32/W33/W34/W35 do
not touch a credited label. **Declared for the re-run: 23 of 23 AS DECLARED, and the page gate still 75 PASS /
0 FAIL / 0 SKIP-BLIND / 0 SKIP-OK, with T2's credited count rising from 122 to roughly 280 (WEAK).**


### §13.5 — Step 4, the render read (a check, never an acceptance — F5Bx-8)

Cloud container, Playwright Chromium, `file://`, **run twice — `java_script_enabled=True` and `False`** (5H-2's
method). Declared: with script disabled the page still shows Columbus in V2 and the IT basis in V1, and V4, V5 and
V6 render identically in both runs because none of them has a control state. Computed style measured on a V5 rect
and a V6 cell, not a bounding box (measure the RECT, not the row `<g>` — 5H-2).

### §13.6 — Checkpoint conditions (from the ruling), restated as things this session will measure

1. the build-incomplete set is **empty**;
2. T's uncredited-numeric count is **0** over the whole page, six views;
3. V6's 21 rows reconcile against G4, and G4 against the two published reports (5A's reconciliation gate re-run);
4. the renders of V4, V5 and V6 were read by the session;
5. Brad's-shell logs re-written (his shell, not this session's — F5B-9).


## §14 — Results, in the order the runs happened, and the state after the unit

### §14.1 — Step 1, V4 + V5 + V6 built; Step 2, the six gate scope corrections — DECLARATION HIT

Device VM scratch, Python 3.10.12, then re-run from the project folder (4A).

**`RESULT 75 PASS  0 FAIL  0 SKIP-BLIND  0 SKIP-OK` / `FAIL SET (empty)` — §13.3 hit exactly.** The
build-incomplete set is EMPTY and **the page gate exits 0: `era_ph5_dashboard.html` is ACCEPTED for the first
time.** No gate id was added and none removed; the six corrections in §13.2 each made their gate assert more.

Secondary declarations, scored honestly:

| declared (§13.3) | measured | verdict |
| --- | --- | --- |
| T1 uncredited-numeric count **0**, page-wide, six views | **0** | **HIT — the unit's hard requirement** |
| T1 scanned ≈ 418 (WEAK) | 397 | WEAK MISS, over by 21 |
| T1 numeric ≈ 121 (WEAK) | 122 | WEAK MISS, under by 1 |
| S5 counts **5** svgs, all dimensions multiples of 8 | 5 | **EXACT HIT** |
| B3 stays PASS; `0.9742` / `0.97` nowhere as page text | PASS | HIT — and the reason `statement` is not a V6 column |
| V6c stays PASS on the unmoved header `#V6` anchor | PASS | HIT |
| D / H / H13 / P unchanged and PASS | PASS | HIT |
| page size ≈ 200 KB (WEAK) | 191,505 B | WEAK MISS, over by ~9 KB |
| CSS gains `.era-band`, `.era-bracket`, plus `.era-t*` table rules | those two + `.era-table`, `… th`, `… td`, `… th.era-num, … td.era-num` | HIT on shape |

`_affine_bad()` and `band_crossings()` are new gate-side helpers; `gate_ramp_index()` is **re-implemented in the
gate on purpose** — importing `era_ph5_views.ramp_index` would make V4b's colour clause assert only that the
build agrees with itself.

### §14.2 — Step 3, the tamper suite. FIRST RUN 22 of 23, W12 MISS (recorded §13.4b). RE-RUN 23 of 23.

`BASELINE  clean page FAIL set is EMPTY as declared (0 ids); the page is ACCEPTED and every firing set below is
ABSOLUTE.` W01 ran first on both runs; the control N01 ran last.

First run: **22 of 23 AS DECLARED**, W12 `DECLARED BUT SILENT: ['T2']`. Cause, correction and re-derivation in
§13.4b, written before the re-run. Re-run after T2's widening: **23 of 23 AS DECLARED**, every set as written,
including the fifteen carried sets that §13.4 predicted would not move and **W31's, which §13.4 predicted would
grow to nine ids and did**: `['D11a','D11b','D11c','H13b','H13c','H6','T2','V4b','V5b']`.

Every gate this unit turned live now has at least one positive that fires it: **V4b twice** through two different
clauses (W07 projection, W13 ramp), **V5b** once (W08 span, with B4 held PASS by choosing DFW), **V6b** three
times (W10 order, W11 FERC-dollar + own-row credit, W12 class order), **B4** once and alone (W09), **T2** widened
and fired (W12, W31).

### §14.3 — Step 4, the render — DECLARATION HIT (cloud container, Playwright Chromium 1194, `file://`, 2x)

Rendered twice, `java_script_enabled=True` and `False`. **Every measured value is identical between the two
runs.** With script disabled: V1 shows `IT` (Metered carries `hidden` in the markup), V2 shows `Columbus`, and
V4, V5 and V6 render identically because none of them carries a control state. Computed style read off the
marks, not bounding boxes: a V5 band rect is `fill rgb(162,194,226)` / `stroke none`, a bracket rect is
`fill rgb(255,255,255)` / `stroke rgb(39,82,124)`, a V6 cell is `11px` `Helvetica Neue` with a
`rgb(204,215,227)` rule — all tokens. V5's crossing annotation renders as the C-BAND-25 title verbatim. V6 shows
21 rows, `C-FERC-H13` first, `unpriced`, both dollar cells empty. **Renders were READ, not committed — the
ruling commits them from 5H-4 on (H-4).**

### §14.4 — Checkpoint (§13.6), measured

1. build-incomplete set **EMPTY** — MEASURED HIT (`FAIL SET (empty)`, exit 0);
2. T1 uncredited-numeric **0** page-wide over six views — MEASURED HIT;
3. V6's 21 rows reconcile against G4 (order == `sort_rank`, every drawn cell equal to its own G4 cell, zero
   mismatches) and G4's every `source_ref` file is present on the mount (`era_ph4_report_v1.1.md`,
   `era_ph2_report_v1.2.md`, `era_ph5_dictionary_v1.0.md`, `direction_ph1_tariff_db_v1.0.md`); the grain gate
   re-run standalone reports **29 PASS / 0 FAIL** — MEASURED HIT;
4. renders of V4, V5 and V6 read by the session — MEASURED HIT;
5. **OPEN: `era_ph5_5h_gate_run.log` and `era_ph5_5h_tamper_run.log` must be RE-WRITTEN from Brad's shell**
   (F5B-9). This session wrote no log to the mount. The closeout hands him the commands. **5H-4 checks for
   headers reading `Unit 5H-3` and does not take this paragraph as fact.**

### §14.5 — State after the unit

**Unchanged, measured on the mount after every run:** `era_rates.db` `1c72e7a1b32c99a650d2e1fba17ae21e`; the four
grains at their E-1.4 pins (`84fe4dbf…`, `3e8825ac…`, `f5b3638a…`, `fc1fa4b1…`); manifest `d28ed340…`; style
`88704aa9…`; `era_ph5_grain_gate.py` `7c1cf9a3…`. **Retired files untouched and unread:** `era_ph5_dashboard.twb`
`20dcb01d…`, `era_ph5_workbook_gate.py` `689b1354…`. No SQLite write. No `.tmp` left on the mount. No log written
to the mount. Brad's committed 5H-2 logs untouched.

| file | md5 | what |
| --- | --- | --- |
| `era_ph5_views.py` | `b40b190a2bdcc3348f447ce1cc797ad4` | `view_v4` + `view_v5` + `view_v6`, their geometry constants, `_v5_rows`, `_v5_crossing`, `fmt6`; three lines in `render()` |
| `era_ph5_build_html.py` | `6cd34506ec969d52c8eb4a046ed30b1c` | six CSS rules (`.era-band`, `.era-bracket`, four `.era-table*`) |
| `era_ph5_page_gate.py` | `396d3e8d6b26f8af9bdfa88ec371ab08` | **V4b, V5b, V6b, B4 re-scoped to the DRAWING; T2 widened to all credited text**; `_affine_bad`, `band_crossings`, `gate_ramp_index`; `group_b` takes the grains; header declares §13.3 |
| `era_ph5_page_tamper.py` | `4f4236f64914a0d91bc3dfa8fbe35897` | `BASELINE = set()`; **W07–W13 added**; W31 grown by `{V4b, V5b}`; every carried set re-derived |
| `era_ph5_dashboard.html` | `1cf07c30886c29b421bee5586ccc0d9a` | **191,505 B, all six views drawn, gate-accepted** |

### Findings

- **F5H3-1. Group T never read a NON-NUMERIC credited label, and §12's own convention rested on that half-truth.**
  `T1` collects text matching `FIGURE_RE`/`NUMBER_RE` without a credit; `T2` then compared *that same numeric
  subset* against its cells. F5H2-5's rule — "credit every label drawn from a grain, not only every dollar; a
  `<title>` counts as text and is scanned" — put roughly **159 credited labels** on this page (V6's 84, V2's 40,
  V4's 24, V5's 11) that **nothing ever compared to the cells they cite**. A build could have named any cell
  beside any text and every gate would have passed. Corrected by widening T2's SCOPE, declared in writing before
  it was written (§13.4b): 122 checked → **289**. No tolerance moved, no id added, the tally stayed 75.
  **How it was found is the point: the declaration that located it is the one that was WRONG.** W12 declared T2
  would fire and T2 was silent. This is the second time in Phase 5 (after F5H1-1) that writing a prediction down
  and watching it fail found a real gap — and the first time the gap was in the gate that was supposed to be the
  page's strongest claim.
- **F5H3-2. A tamper case can be UNFIRABLE for the clause it was written for — F5H2-1 from the other side.**
  §13.4 chose `C-CHI-5CP` as W12's row. Measured against G4 before the run: `C-CHI-5CP` **is** the first
  `limitation` row (index 8), so re-marking it `unpriced` leaves `max(unpriced) = 8 < min(limitation) = 9` and
  clause (6) still holds. The case would have fired `{T2, H6}` and been recorded a MISS for the wrong reason.
  Corrected to `C-STATION-POINT`, the LAST limitation row, in writing before the run (§13.4a). **Rule: ask of
  every new positive not only "does this fire the clause" but "can the row or mark I chose fire it at all", and
  answer it against the artefact, not from the ruling's prose.**
- **F5H3-3. The figure C-BAND-25 names is on a different axis from the one V5 is ruled to draw. Measured, not
  argued.** Columbus `band_high_usd_per_mwh` − Chicago `usd_per_mwh` = **0.80423602** — that IS the caveat's
  FACILITY figure, and it confirms G1's `usd_per_mwh` is the published facility basis. On the `$/IT-MWh` axis
  the ruling puts V5 on, the same adjacency crosses by **1.08102537**. Printing 0.8042 there is the basis
  mismatch F5A-4 exists to prevent; printing 1.0810 is a derived figure that exists in no cell (F5H1-5).
  **V5 prints neither.** The crossing is carried by the two endpoint cells, each printed and credited to its own
  G1 column, and by the drawing — Columbus's band ends 11 px right of Chicago's central mark, under a guide
  hairline — and **B4 now gates that geometry.** Third instance of one rule (F5B-2, F5H1-5, F5H2-3): a figure
  whose basis the frozen contract cannot express is a figure this page does not type. **DO NOT "IMPROVE" IT.**
- **F5H3-4. Four of the five gates this unit turned live could have passed on a claim rather than a drawing.**
  Asked before the build (§13.2) and answered in writing: V4b counted eight elements carrying `data-role="point"`
  and would have passed on eight empty `<g>`; V5b was NAMED "intervals span band_low/band_high" and asserted
  `len >= 3`; V6b asserted neither of the two things its own text claimed; B4 required one element with two
  attributes **the build writes about itself** and would have passed on a page showing no crossing at all. Only
  the three existence gates (V4a, V5a, V6a) survived the question. **The stub gates written by 5H-0 for views
  that did not exist were, without exception, weaker than their own descriptions** — F5H1-1 said a gate written
  before its artefact is a prediction about markup; this unit measured that ALL FOUR non-trivial predictions
  were false-pass-shaped, not fail-shaped.
- **F5H3-5. A ruled prose claim became a gate.** C-BAND-25 asserts its adjacency is "the ONLY adjacency the bands
  touch anywhere in the table". `band_crossings(G1)` re-derives every such pair from `is_market_priced`, `rank`,
  `band_high_usd_per_it_mwh` and `usd_per_it_mwh`, and **B4 asserts the COUNT is exactly one**. Measured: one,
  `(Columbus, Chicago)`. The adjacency is nowhere named in the view code or the gate code. If a future extract
  creates a second crossing, B4 fails and the caveat's sentence has to be rewritten — which is the correct
  coupling.
- **F5H3-6. Cross-interpreter determinism holds with all six views.** `1cf07c30886c29b421bee5586ccc0d9a`,
  191,505 B, from Python 3.10.12 on the device VM from two different directories, and W34 measured two builds
  EQUAL inside the harness's own temp copy. Extends F5H2-6, F5H1-6, F5H0-5. **Brad's 3.13.x remains 5H-4's
  measurement.**
- **F5H3-7. The V4 ramp collapses exactly where the ranking is least certain. Routed to 5H-4.** The seven-step
  ramp is linear over 47.67 … 180.96, a range San Jose alone stretches. Steps actually used: **0, 1, 1, 2, 3, 3,
  4, 6 — step 5 never appears, Columbus and Chicago are the same colour, and so are Northern Virginia and
  Phoenix.** The three banded metros at the top of the ranking are the ones the map cannot tell apart. A
  rank- or quantile-assigned step would separate them and would still be a function of `usd_per_it_mwh`.
  **No gate sees it: V4b asserts the step matches the rule, and it is the RULE that is weak.**
- **F5H3-8. V5's value labels are anchored to the row, not to the mark. Routed to 5H-4.** `73.65 … [14 px box]
  … 74.95` reads as though the box spanned the row; the narrower the interval, the more the fixed labels
  overstate it — the opposite of what the view is for. The crossing guide also overprints Chicago's `81.54`
  central label. Same class as F5H1-4 and F5H2-4: label placement, no data change, no gate sees it.
- **F5H3-9. V4's frame is the plot box, not the map. Routed to 5H-4.** The four hairlines bound the 1088 × 336
  plot area while the projected extent is 966 × 256, so the frame reads as an arbitrary rectangle around the
  points rather than an edge of anything. Hug the extent or drop the frame; either is less ink than the current
  compromise.

### Routed

**NO RULING IS PENDING.** Nothing in this unit changed a figure, a basis, the extract contract or the database.

**To 5H-4** (assembly and aesthetic conformance): **F5H3-7** (the V4 ramp collapse — the largest of the three),
**F5H3-8** (V5 label anchoring + the guide/label overprint) and **F5H3-9** (the V4 frame), joining the carried
**F5H1-3** (harden T2's shown-value normaliser to translate U+2212 rather than strip it), **F5H1-4** (nudge a
credited label clear of the zero rule when its row extent is under one grid unit) and **F5H2-4** (hairline
connectors between waterfall steps).

**Notes to the strategy chat, no ruling requested:** **F5H3-3** joins F5H1-5 and F5H2-3 as the third measured
instance of "a figure whose basis the contract cannot express is not typed" — the pattern is now stable enough
to be a standing rule rather than three findings. **F5H3-1** is worth the strategy chat's attention for a
different reason: the project's oldest claim about this page — zero typed figures — was, until this unit, only
half gated.

### Conventions 5H-4 must follow (assembly, the chain, the renders)

- **Check the log headers read `Unit 5H-3` before treating this unit as complete, and take no paragraph above as
  fact** (F5B-10). The page on disk should be `1cf07c30886c29b421bee5586ccc0d9a`, the gate 75 PASS / 0 FAIL /
  0 SKIP-BLIND / 0 SKIP-OK with an EMPTY FAIL set, the tamper suite 23 of 23. **If the gate reports anything
  else, the unit is blocked: report, do not repair.**
- The tamper harness's `BASELINE` is `set()` from here on and every firing set is absolute. **W01 still leads.**
- **The six drawing findings (F5H1-3, F5H1-4, F5H2-4, F5H3-7, F5H3-8, F5H3-9) are 5H-4's actual work.** None of
  them is seen by a gate, which is precisely why they were written down.
- **A style-gate correction must be a declared-set assertion, never a loosened threshold** (the ruling's own
  words for 5H-4). The same holds for anything F5H3-7's re-ramp touches: V4b's ramp clause must be re-derived to
  the NEW rule and re-fired by W13, not relaxed.
- Brad's shell is the measurement for H-3's end-to-end chain and for Python 3.13.x determinism. Renders for all
  six views are committed from 5H-4 on.


---

# Unit 5H-4 — assembly, aesthetic conformance, the end-to-end chain, renders

Session 2026-09-05, cloud execution session on Brad's mounted project folder. Scope:
`direction_ph5_html_v1.0.md` Unit 5H-4 only. No SQLite write. No retired file written. Record appended
below; nothing above this line is edited.

## §15 — Declared expectations, written before any run of this unit

### §15.0 — Step 0, the state this unit checked before anything else, and the handoff premise it did NOT take as fact

Measured on the mount before a line was written (the handoff prompt says "take no description of these
files as fact", and §14.4 item 5 said the two logs were still to be written):

- `era_ph5_5h_gate_run.log` PRESENT, header
  `era_ph5_page_gate.py  Unit 5H-3  project=C:\Users\User\Claude\Projects\Electrical Rate Analysis  page=era_ph5_dashboard.html  python=3.13.5  platform=Windows-11-10.0.26200-SP0  page_md5=1cf07c30886c29b421bee5586ccc0d9a`.
- `era_ph5_5h_tamper_run.log` PRESENT, header
  `era_ph5_page_tamper.py  Unit 5H-3  project=C:\Users\User\Claude\Projects\Electrical Rate Analysis  python=3.13.5`.
- **5H-3 CHECKPOINT ITEM 5 IS THEREFORE CLOSED. 5H-3 is complete on every item.** The handoff premise
  ("record 5H-3's checkpoint item 5 as still open if the headers do not read `Unit 5H-3`") did not hold;
  it was checked, not assumed, and what was found is recorded. Second instance of the same shape 5H-3
  recorded against its own prompt.
- `era_ph5_dashboard.html` md5 `1cf07c30886c29b421bee5586ccc0d9a`, 191,505 B — as §14.5 states.
- The committed gate log ends `RESULT 75 PASS  0 FAIL  0 SKIP-BLIND  0 SKIP-OK` / `FAIL SET (empty)`.
  The committed tamper log ends `RESULT 23 of 23 AS DECLARED (W01 ran first, V1 built)` with
  `BASELINE  clean page FAIL set is EMPTY as declared (0 ids)`. **NOT BLOCKED.**
- Code pins as §14.5 declares: `era_ph5_views.py` `b40b190a2bdcc3348f447ce1cc797ad4`,
  `era_ph5_build_html.py` `6cd34506ec969d52c8eb4a046ed30b1c`, `era_ph5_page_gate.py`
  `396d3e8d6b26f8af9bdfa88ec371ab08`, `era_ph5_page_tamper.py` `4f4236f64914a0d91bc3dfa8fbe35897`.

### §15.1 — Step 1, the six drawing findings. What each becomes, and the facts each was derived from

These six are the unit's real work (§14, Conventions). **Every one of them is a DRAWING change, and every
one of them is given a gate clause in §15.2, because H5/H6 cannot see a view-code regression: H6 rebuilds
the page from the same `era_ph5_views.py` it is checking.** That is the whole reason a drawing rule needs
a gate of its own and not a reproduction hash.

**(1) F5H3-7 — the V4 ramp is RE-RAMPED, ordinally.** Facts measured off G1 before the rule was chosen:
the eight `usd_per_it_mwh` values are 47.672601, 69.259049, 81.539548, 94.845422, 107.564621, 123.565051,
142.711919, 180.961656; the current linear rule `int((v-lo)/(hi-lo)*7)` gives steps **0, 1, 1, 2, 3, 3, 4, 6**
in rank order — step 5 unused, Columbus == Chicago, Northern Virginia == Phoenix. **New rule, and it is
still a function of `usd_per_it_mwh` alone:**

    order = sorted(set(values)); N = len(order); i = order.index(v)
    step  = int(i * (RAMP_STEPS - 1) / (N - 1) + 0.5)          # N >= 2, else 0

`int(x + 0.5)` and not `round()`: `round()` is banker's rounding and this must be identical on 3.10, 3.11
and 3.13 (F5H0-5 is the reason). Measured steps under the new rule, ascending: DFW 0, **Columbus 1,
Chicago 2**, Austin 3, Northern Virginia 3, Phoenix 4, Atlanta 5, San Jose 6. **All seven steps are used
and the three banded metros at the top of the ranking are three different colours**, which is what
F5H3-7 asked for. Eight values into seven steps forces exactly one collision; the ordinal rule puts it at
Austin/Northern Virginia (ranks 4 and 5, neither banded), where the linear rule put two collisions and one
of them among the top three.

**V1 IS RE-RAMPED TOO, and that is deliberate.** V1's IT state ramps the SAME field with the SAME linear
rule and therefore carries the SAME collapse. Leaving V1 linear would put two different colour semantics
on one page for one column — the exact opposite of "aesthetic conformance", which is this unit's remit.
`ramp_index(v, lo, hi)` is REPLACED by `ordinal_ramp(values)`; both call sites move. No gate reads V1's
ramp classes (checked: `era-ramp` appears in the gate only inside V4b), so this is a drawing change with
one gated consequence, in V4.

**(2) F5H3-9 — V4's frame is DROPPED.** The finding offers "hug the extent or drop the frame". Hugging
puts the four extreme stations' `r=7` circles half outside their own frame, so it trades an arbitrary
rectangle for a broken one. Dropping is the ruling's own word for V4 ("V4 gets the least ink") and it
leaves nothing arbitrary to defend. Measured ink now (rect+circle+line+path+text inside each view body):
V1 57, V2 103, V3 51, **V4 28, V5 28**, V6 0 marks (a table). V4 is TIED, not least. **With the four
hairlines gone V4 is 24 and is strictly the least-inked of the five svg views** — so "V4 gets the least
ink" stops being a sentence in a ruling and becomes a measurable fact, which §15.2 gates.

**(3) F5H3-8 — every V5 value label anchors to its own mark, at one grid unit.** Today the low and high
labels sit at fixed row positions `V5_LOW_X` / `V5_HIGH_X`, so a 14 px bracket reads as spanning the row.
New rule, uniform across all three label kinds, one constant `V5_LABEL_GAP = 8` (one grid unit):
low label `x = rect_x - 8`, `text-anchor="end"`; high label `x = rect_x + width + 8`, `text-anchor="start"`;
band central label `x = tick_x + 8`, `text-anchor="start"`. **The guide/label overprint is solved BY this
rule and not by a special case**: the crossing guide is a vertical hairline at the crossed metro's central
tick `x`, and that metro's central label now begins 8 px to the RIGHT of the tick instead of being centred
on it, so the guide cannot cross the glyphs. No conditional placement, no guide splitting, no change to
the guide's geometry — which matters, because B4 gates the crossing geometry and must not move.

**(4) F5H1-4 — a credited label on a sub-grid-unit row is nudged clear of the zero rule.** Measured on V3
with its own scale (`lo -167,099,502.51`, `hi 17,239,632.05`, zero rule at x = 1086): row extents in px
are rider 870, energy 457, demand 196, **fixed 1**, statutory 90. The fixed row's label lands at x = 1086
— **on the zero rule, to the pixel**. New rule: a channel row whose drawn extent is under one grid unit
(8 px) places its credited label at `x = x_of(row_min) - 12`, `text-anchor="end"` — one and a half grid
units clear, to the left, which keeps it inside the plot (1074, running left to ≈1019) rather than pushing
it against the 1184 px edge.

**(5) F5H2-4 — hairline connectors between waterfall steps.** Rule, and it is derived from the grain, not
from the drawing order: consecutive rows of one metro's walk are joined by a vertical hairline at the
x-value they SHARE, where row i+1 shares row i's end if either its `waterfall_start_usd` or its
`waterfall_end_usd` maps to the same pixel. The second half is what lets the `mitigated` TOTAL row — which
starts at zero, not at the previous end — be connected at the value the walk actually landed on, while a
row that shares nothing is not connected at all. **Excluded siblings have no position in the walk and get
no connector**, which is the same refusal §10.1 made when it anchored them at zero. Counted from G2 before
the code was written: Atlanta 2, Austin 3, Chicago 4, Columbus 3, Dallas-Fort Worth 2, Northern Virginia 3,
Phoenix 2, San Jose 3 — **22 connectors over the eight pre-rendered states**, taking V2's `<line>` count
from 4 to 26 and its ink from 103 to 125. New CSS rule `.era-wf-connector { stroke: var(--era-rule);
stroke-width: 1; }` — a var, so no hex and no font-size enters the page and S1–S4 cannot move.

**(6) F5H1-3 — T2's shown-value normaliser TRANSLATES U+2212.** The defect, read off the gate:
`re.sub(r"[,$%\s−]", "", t).replace("−", "-")` puts U+2212 INSIDE the stripped class, so the `.replace`
that follows it can never see one. **The false pass this creates is not the one the finding's wording
suggests.** A NEGATIVE cell shown with a typographic minus still fails (the sign is dropped from the shown
value and the magnitudes disagree). What passes silently is a POSITIVE cell shown as `−X`: strip the
minus and the comparison succeeds. So the page could print the negation of a positive cell and T2 would
call it equal. Fix: translate first, strip second —

    shown = t.replace("\u2212", "-"); shown = re.sub(r"[,$%\s]", "", shown)

**No figure on the page moves**: `fmt2`/`fmt6` are `"{:,.2f}"`/`"{:,.6f}"`, which emit the ASCII
hyphen-minus. This is a hardening, and §15.4's W20 is the positive that proves it is one — **W20 cannot
fire against the current normaliser, which is precisely the measurement.**

### §15.2 — The gate scope corrections, declared BEFORE they are written and BEFORE any build (F5H2-1, F5H3-4)

Asked of every clause below: **could markup that does not do what §15.1 says still satisfy it?** And of
every positive: **can the mark I chose fire this clause at all (F5H3-2)?** Answers in writing, here, first.
**No gate id is added or removed and no threshold moves. Every correction makes its gate assert strictly
more.**

- **V4b, ramp clause RE-DERIVED to the new rule (mandated by §14's conventions — re-derived, never
  relaxed).** `gate_ramp_index(v, lo, hi)` is replaced by `gate_ordinal_ramp(values)`, **re-implemented in
  the gate and not imported from `era_ph5_views`** — importing it would make the clause assert only that
  the build agrees with itself (the reason §14.1 gives for the existing re-implementation, and it still
  holds). Could it false-pass? Only if the gate and the view shared an implementation; they do not.
- **V4b, NEW no-frame clause: V4 contains zero `<line>` elements.** Could markup that does not do what
  §15.1 says satisfy it? No — this is an assertion of absence about the drawing itself, not about an
  attribute the build writes.
- **V4b, NEW least-ink clause: V4's mark count (`rect`+`circle`+`line`+`path`+`text` inside the V4 svg) is
  STRICTLY LESS than every other view's.** This is the ruling's "V4 gets the least ink" made measurable.
  Could it false-pass? It is a comparison of drawn-element counts across five views; nothing the build
  says about itself enters it. **Declared now: W14 fires the no-frame clause AND this clause together**
  (restoring the four hairlines takes V4 to 28 against V5's 28, which is not strictly less). The two
  clauses are not separable by a positive, and that is recorded rather than engineered around: the
  no-frame clause is the stronger of the two and the least-ink clause is the ruling's sentence.
- **V5b, NEW label-anchor clause.** For each of the five intervals: the low label's `x` equals
  `rect_x - 8` with `text-anchor="end"`; the high label's `x` equals `rect_x + width + 8` with
  `text-anchor="start"`; and for each band row the central label's `x` equals the central tick's `x1 + 8`
  with `text-anchor="start"`. Could markup that does not do what §15.1 says satisfy it? No — every term is
  read from a DRAWN coordinate (the rect, the tick) and compared to a DRAWN coordinate (the text). This is
  the clause that makes the guide/label overprint impossible; there is no separate overprint clause,
  because the anchoring rule is what removes the overprint.
- **V3b, NEW sub-grid-unit clause, derived entirely from the drawing.** For every `data-channel` row: read
  the row's drawn extent from its own rects (`min x` to `max x+width`) and the zero rule's `x` from the V3
  axis line; if the extent is under one grid unit (8 px), the row's credited label's `x` must be at least
  one grid unit clear of the zero rule. No view constant enters the gate.
- **V2b, NEW connector clause.** For every one of the eight `data-state-metro` groups: re-derive from G2
  the set of consecutive walking-row pairs that share an x, and assert that the state draws exactly one
  `data-role="connector"` line per such pair, each at the shared value's pixel and vertically between the
  two bars. Could it false-pass? The count and the x are both re-derived from the grain; an element
  carrying `data-role="connector"` and drawing nothing has no x to match.
- **V6c, NEW composition clause.** The one-click anchor stays as it is; added: the six `section
  data-view` slots appear in document order `V1 V2 V3 V4 V5 V6`, so **V1 leads and V6 is below the
  anchor** (`direction_ph5_html_v1.0.md`, Unit 5H-4). Why this is not redundant with H6: H6 rebuilds the
  page from the same `era_ph5_build_html.py`, so a reordering of that file's `VIEWS` constant reproduces
  itself exactly and H6 stays PASS. H6 sees page edits; it cannot see build-code edits. Same argument as
  for the five clauses above.
- **T2, normaliser hardened (§15.1 item 6).** Scope, not threshold: no tolerance changes, and the widened
  set of 289 credited elements from 5H-3 is unchanged. It asserts strictly more, because a shown value
  whose sign disagrees with its cell can no longer normalise to the cell's magnitude.
- **The style gate.** The ruling's 5H-4 sentence is "zero off-token colours with a declared-set assertion
  if the build emits a browser default that is not a token (never a loosened threshold)." **Declared: the
  condition does not arise on this page.** S1 measured 13 hex colours, all thirteen tokens, on 5H-3's
  page; every mark this unit adds is painted with a `var(--era-*)`, so no browser default reaches the
  file and no declared-set assertion is needed. **If S1 measures anything other than 13-of-13 after the
  build, the correction is a declared set of exact hex literals, never a raised count.**

### §15.3 — Steps 1 and 2, the build and the corrected gate. DECLARED TALLY

**`RESULT 75 PASS  0 FAIL  0 SKIP-BLIND  0 SKIP-OK`, `FAIL SET (empty)`, exit 0.** No gate id is added,
none is removed, the page stays ACCEPTED. Secondary declarations, weak ones marked:

| gate | declared |
| --- | --- |
| V4b | PASSES on the ORDINAL ramp; the eight classes are DFW 0, Columbus 1, Chicago 2, Austin 3, Northern Virginia 3, Phoenix 4, Atlanta 5, San Jose 6; V4 draws 0 `<line>`; V4 ink 24, strictly least of the five |
| V5b | PASSES with all five intervals' low/high labels and all three central labels at the ±8 px offsets |
| V3b | PASSES; the fixed channel is the ONLY row under one grid unit (1 px) and its label moves 1086 → 1074 |
| V2b | PASSES with 22 connectors over the eight states (2/3/4/3/2/3/2/3 in metro-name order) |
| V6c | PASSES; slot order V1 V2 V3 V4 V5 V6, unchanged by this unit |
| T1 | uncredited numeric count **0**; scanned **397**, numeric **122** — EXACT, not weak: this unit adds and removes only marks that carry no text |
| T2 | **289** credited text elements, all equal to their cells — EXACT, same reason |
| S1–S5 | unchanged and PASS: 13 hex all tokens, 5 sizes, one family, the three grid constants, 5 svgs on multiples of 8 |
| D / H / H13 / P / B | unchanged and PASS; **B4 in particular**, because the crossing guide and both endpoint marks keep their geometry |
| page size | ≈ 193 KB (**WEAK**) |
| V2 ink | 103 → 125; V2 `<line>` 4 → 26 (EXACT) |


### §15.2a — Amendment to §15.2, written after the build and BEFORE the corrected gate is written or run

**The least-ink clause's comparison set was declared ambiguously and is corrected here, beside itself,
not edited in place (F5H2-7).** §15.2 says V4's mark count is "STRICTLY LESS than every other view's";
§15.3 says "strictly least of the five". Those disagree, and the first is unsatisfiable: **V6 is a
`<table>` and draws no `rect`, `circle`, `line`, `path` or `text` at all — its mark count is 0**, so
"strictly less than every other view" can never hold for any view. The clause the gate is written to is
the second reading: **V4's mark count is strictly less than each of the other four SVG views (V1, V2, V3,
V5).** Measured on the built page, before the gate exists: V1 57, V2 125, V3 51, **V4 24**, V5 28.

Two further facts measured on the built page before the corrected gate was written, so the gate's
constants are taken from the artefact and not from prose:

- V4's eight ramp classes are `era-ramp-` 0, 1, 2, 3, 3, 4, 5, 6 for DFW, Columbus, Chicago, Austin,
  Northern Virginia, Phoenix, Atlanta, San Jose — **§15.1's declared ordinal steps, exactly**, and V4
  draws **zero** `<line>`.
- V2 draws **22** connectors, 2/3/4/3/2/3/2/3 over the eight states in metro-name order — **§15.3's
  declared counts, exactly**. V3's fixed channel is the only row under one grid unit (drawn extent 1 px)
  and its label moved 1086 → **1074**, `text-anchor="end"`, twelve pixels clear of the zero rule at 1086.
  V5's fifteen labels sit at exactly `rect_x − 8`, `rect_x + width + 8` and `tick_x + 8`. The crossing
  guide is at x 750 and Chicago's central label now begins at 758: **the overprint is gone**, and the
  guide's own geometry did not move, so B4 reads what it read before.


### §15.3a — Step 1 and 2 measured, and one guard added to the gate before the suite runs

**`RESULT 75 PASS  0 FAIL  0 SKIP-BLIND  0 SKIP-OK` / `FAIL SET (empty)` / exit 0 — §15.3 hit exactly**,
including both figures declared EXACT: `T1 uncredited numeric text count = 0 (122 numeric of 397 text
elements scanned)` and `T2 289 credited text elements`. Page 193,712 B (declared ≈193 KB, WEAK — hit).
The full run is recorded in §16.1. Every declared clause reads as written in the log:

- `V4b … ORDINAL ramp step from usd_per_it_mwh, no frame line, least ink 24 vs {'V1': 57, 'V2': 125, 'V3': 51, 'V5': 28}`
- `V2b … each joining its walk with one hairline connector per shared step (22 over the eight states)`
- `V3b … every row narrower than one grid unit carries its credited label clear of the zero rule`
- `V5b … every value label anchored to its own mark at 8 px`
- `V6c … slots in document order ['V1','V2','V3','V4','V5','V6'] (V1 leads, V6 below the anchor)`

**One guard is added to V2b's connector clause before the suite runs, and it is declared here rather
than discovered by a crash.** The clause indexes the DRAWN rows at `i` and `i+1` for pair indices it
derived from G2. W03 deletes a drawn row from a state; because the row it deletes is Columbus's LAST
(the excluded sibling), indices 0..3 still resolve and the case is unaffected — but a future case that
deletes a row from the MIDDLE of a walk would raise IndexError instead of failing the gate, and a gate
that crashes has measured nothing (F5B-9's shape). The guard records the missing row as a V2b failure.
No threshold moves and no id changes.

### §15.4 — Step 3, the tamper suite, declared before it runs

`BASELINE` is `set()` and stays `set()`: the clean page's FAIL set is EMPTY, so **every firing set below
is ABSOLUTE**, and the harness aborts NOT CONNECTED if the clean baseline is anything else. **W01 leads;
the control N01 runs last.** **A declared set is not inherited (F5H1-2): all twenty-three carried cases
are re-derived below against the page as it now stands, with the reason each set does or does not move.**
Six cases are added, one for each clause this unit introduced.

#### The six new positives

| case | kind | declared firing set | why, and can the mark chosen fire this clause at all (F5H3-2) |
| --- | --- | --- | --- |
| **W14** | page | **{V4b, H6}** | The four frame hairlines F5H3-9 removed are re-inserted at the head of the V4 svg. **This fires BOTH of V4b's new clauses and that is declared, not engineered around** (§15.2): the no-frame clause sees 4 `<line>` where it requires 0, and the least-ink clause sees V4 at 28 against V5's 28, which is not strictly less. CAN IT FIRE? Yes on both counts, measured: V4 is 24 marks with no line, and each restored line is +1. The lines carry a token class and no text, so S1 and T1 stay PASS. H6 by F5H0-3. |
| **W17** | page | **{V5b, H6}** | Dallas-Fort Worth's HIGH value label is moved from x 510 to x 550 — the row it belongs to and the text it shows are untouched. Fires the label-anchor clause only: the affine SPAN clause reads the rect, not the label, and the rect does not move; T2 reads the text, and the text does not change. CAN IT FIRE? Yes: the clause requires `x == rect_x + width + 8` = 288 + 214 + 8 = 510, and 550 is not 510. B4 stays PASS — the crossing is Columbus against Chicago and neither moves. |
| **W18** | page | **{V3b, H6}** | The fixed channel's credited label is moved from x 1074 back onto the zero rule at x 1086. Fires V3b's sub-grid-unit clause; the channel ORDER clause is untouched, so **W02 and W18 fire V3b through two different clauses**, which is the W07/W13 pattern. CAN IT FIRE? Yes, and it was checked against the artefact first (F5H3-2): the fixed channel is the ONLY row whose drawn extent is under one grid unit (1 px against rider 870, energy 457, demand 196, statutory 90), so it is the only row the clause quantifies over, and moving it to the rule's own x puts the distance at 0. Moving any other row's label would leave the clause silent. T2 stays PASS — the text is unchanged. |
| **W19** | page | **{V2b, H6}** | One `data-role="connector"` hairline is deleted from Columbus's state group. Fires V2b's connector clause on the count (3 drawn for 3 joined pairs becomes 2). The component rows, their order and their ids are untouched, so the order/count clause is silent and V2c stays PASS. CAN IT FIRE? Yes: Columbus draws exactly 3 and G2 yields exactly 3 joined pairs. |
| **W20** | page | **{T2, H6}** | **The positive for F5H1-3, and the one case in this suite that CANNOT fire against the gate as 5H-3 left it — which is the measurement.** San Jose's V1 value label is changed from `180.96` to `−180.96` (U+2212), against a cell of `180.9616556284141`. Under the OLD normaliser `re.sub(r"[,$%\s−]","",t)` the minus is STRIPPED and the shown value normalises to `180.96`, which equals the cell to the precision shown: **T2 passes on the negation of a positive cell.** Under the hardened normaliser the text translates to `-180.96` and the comparison fails by 361.92. T1 stays PASS: `NUMBER_RE` already accepts U+2212 and the element still carries its `data-src`, so the figure is credited, not uncredited. H6 by F5H0-3. |
| **W21** | page | **{V6c, H6}** | The V1 and V3 `<section>` slots are swapped WHOLE. Fires V6c's composition clause (document order becomes V3 V2 V1 V4 V5 V6, so V1 no longer leads). Every other gate finds its view by `data-view` and is order-blind, so V1a/V1b/V1c, V3a/V3b and all of P, B, S and T stay PASS. CAN IT FIRE? Yes. **And it is not redundant with H6 in the way it looks**: H6 fires here because the PAGE moved, but the clause exists for a change to `era_ph5_build_html.VIEWS`, which H6 would reproduce and pass (§15.2). |

#### The twenty-three carried cases, re-derived

| case | declared set now | moved? and why |
| --- | --- | --- |
| **W01** | {V1c, H6} | **NO.** V1's ramp is now ordinal (§15.1), but W01 rebinds `data-field` and no gate reads V1's ramp classes — checked: `era-ramp` appears in the gate only inside V4b. The geometry still does not move (F5B-4), so V1c alone sees it. |
| **W02** | {V3b, H6} | **NO.** V3b gained the sub-grid-unit clause; swapping two `data-channel` attributes leaves the fixed row and its label untouched, so the new clause is silent and the order clause fires exactly as before. |
| **W03** | {V2b, V2c, H6} | **NO.** V2b gained the connector clause; the row W03 deletes is an EXCLUDED sibling, which has no position in the walk and is never joined, so Columbus still draws 3 connectors for 3 joined pairs. V2b fires on the order/count clause as before. (This is the case the §15.3a guard was written for.) |
| **W04** | {V2c, H6} | **NO.** Attribute-only change on an excluded row; connectors untouched. |
| **W05** | {P6, H6} | **NO.** Which state is visible changes; every state carries its own connectors identically. |
| **W06** | {V2c, H6} | **NO.** The deleted CSS rule is `.era-excluded`; `.era-wf-connector` is a different rule and carries no hex, no size, no family and no grid constant, so S1–S4 still stay PASS. |
| **W07** | {V4b, H6} | **NO — but its needle was re-checked against the new page.** W07 keys on `class="era-ramp-1" … data-metro="Columbus"`, and under the ORDINAL rule Columbus is still step 1 (ascending index 1 of 8), so the needle still resolves. It fires the projection clause; the no-frame and least-ink clauses stay satisfied because a `cy` shift adds no mark. |
| **W08** | {V5b, H6} | **NO, and it now fires V5b through TWO clauses — declared.** Halving DFW's rect breaks the affine SPAN clause as before, and it also moves the drawn right edge out from under the high label, so the label-anchor clause fires too. Same gate, same set; recorded because a two-clause firing that is not declared is a MISS waiting to happen. B4 still PASS (DFW is not the crossing). |
| **W09** | {B4, H6} | **NO.** The crossing annotation is deleted; the guide, the intervals and every label keep their geometry, so V5b's new clause is silent. |
| **W10** | {V6b, H6} | **NO.** Two `<tr>` swapped inside V6; V6c reads `<section data-view>` order, not row order, so the composition clause is silent. |
| **W11** | {V6b, H6} | **NO.** |
| **W12** | {V6b, T2, H6} | **NO.** T2's normaliser changed but not its scope: the drawn text `unpriced` still does not equal the cell `limitation`, and that comparison never touched a minus sign. |
| **W13** | {V4b, H6} | **NO — and this is the case §14's conventions require to re-fire the RE-DERIVED ramp clause.** Columbus's class is swapped `era-ramp-1` → `era-ramp-6`. Under the ordinal rule Columbus wants step 1, so the clause fires exactly as it did under the linear rule — **re-derived to the new rule, never relaxed.** `era-ramp-6` is still a token class so S1 stays PASS, no coordinate moves so the projection clause stays PASS, and no mark is added so the least-ink clause stays PASS. |
| **W15** | {D2a, D2b, D2c, D3a} | **NO.** Grain-kind: runs the grain gate, not the page gate. |
| **W16** | {D5a, D6a} | **NO.** Grain-kind. |
| **W24** | {D11a, D11b, D11c} | **NO.** Grain-kind. |
| **W30** | {H13a, H6} | **NO.** |
| **W31** | {H13b, H13c, D11a, D11b, D11c, H6, T2, V4b, V5b} | **NO — the nine of 5H-3 hold, and each was re-checked, not carried.** Columbus `usd_per_it_mwh` + 200 on disk: H13b/H13c and the three D11 ties as before; H6 because the rebuild differs; T2 because V1 credits Columbus at 69.26 against that cell. **V4b still fires, for a different reason than in 5H-3**: under the linear rule the perturbation moved `hi` and re-scaled every step; under the ORDINAL rule it moves Columbus from ascending index 1 to index 7 and shifts six other metros down one, so six of the eight drawn classes disagree with the re-derived map. **V5b still fires** on Columbus's central mark against its own cell. **V3b, V2b and V6c do NOT join**: the first two read the drawing and G2, the third reads slot order. **B4 stays PASS** — `band_high_usd_per_it_mwh` did not move, so `band_crossings` still yields exactly one adjacency and the drawn crossing is unchanged. |
| **W32** | {T1, H6} | **NO.** |
| **W33** | {S1, H6} | **NO.** |
| **W34** | ∅ (two builds EQUAL) | **NO.** The md5 the harness prints becomes the new page's. |
| **W35** | {S1} | **NO.** |
| **N01** | ∅ | **NO.** Runs last. |

**Declared total: 29 of 29 AS DECLARED**, W01 first, N01 last.


## §16 — Results, in the order the runs happened, and the state after the unit

### §16.1 — Steps 1 and 2, the six drawing findings built and the seven gate scope corrections — DECLARATION HIT

Device VM scratch (Python 3.10.12), then copied to the mount and re-run from the project folder (4A).
Both runs identical; the page built in scratch and the page built on the mount are the SAME bytes.

**`RESULT 75 PASS  0 FAIL  0 SKIP-BLIND  0 SKIP-OK` / `FAIL SET (empty)` / exit 0.** §15.3 hit,
including both figures declared EXACT rather than weak:

| declared (§15.3) | measured | verdict |
| --- | --- | --- |
| 75 / 0 / 0 / 0, FAIL set empty, exit 0, no id added or removed | same | **HIT** |
| T1 uncredited **0**; scanned **397**; numeric **122** | 0 / 397 / 122 | **EXACT HIT** (5H-3's two WEAK misses on these counts do not recur — this unit adds and removes only marks that carry no text, so the counts were derivable, not guessed) |
| T2 **289** credited elements | 289 | **EXACT HIT** |
| V4 ramp DFW 0, Columbus 1, Chicago 2, Austin 3, NoVA 3, Phoenix 4, Atlanta 5, San Jose 6 | same | **HIT** — all seven steps used, the three banded metros three colours |
| V4 draws 0 `<line>`; ink 24, strictly least | `no frame line, least ink 24 vs {'V1': 57, 'V2': 125, 'V3': 51, 'V5': 28}` | **HIT** |
| V2 22 connectors, 2/3/4/3/2/3/2/3 | same | **HIT** |
| V3 fixed channel the only sub-grid-unit row; label 1086 → 1074 | same | **HIT** |
| V5 fifteen labels at `rect_x−8` / `rect_x+width+8` / `tick_x+8` | same | **HIT** |
| V6c slot order V1…V6 | same | **HIT** |
| S1–S5, D, H, H13, P, B unchanged and PASS; **B4 in particular** | all PASS | **HIT** |
| page ≈ 193 KB (WEAK) | 193,712 B | **HIT** (5H-3's page was 191,505 B) |

### §16.2 — Step 3, the tamper suite — 29 of 29 AS DECLARED, FIRST RUN, no MISS

`BASELINE  clean page FAIL set is EMPTY as declared (0 ids); the page is ACCEPTED and every firing set
below is ABSOLUTE.` W01 ran first, N01 last. **`RESULT 29 of 29 AS DECLARED (W01 ran first, V1 built)`**
on the VM scratch copy and again from the project folder on the mount. No UNDECLARED FIRING, nothing
DECLARED BUT SILENT, no ALSO-ASSERTED PASS NOT SEEN. Every one of the twenty-three carried sets held as
§15.4 re-derived it, including **W31's nine**, and every new clause fired the case written for it:
W14 {V4b,H6}, W17 {V5b,H6}, W18 {V3b,H6}, W19 {V2b,H6}, W20 {T2,H6}, W21 {V6c,H6}.
W34 printed `two builds: EQUAL (md5 2f7b7a75… / 2f7b7a75…)`.

**Two needle coordinates in the harness were corrected before the run, not after** (F5H3-2's discipline
applied to the mechanics rather than the logic). §15.4's W18 and W20 were written against coordinates
taken from the 5H-3 page; the new page moved them, because V3's label row and V1's value column are laid
out from row indices this unit's edits shifted by a few pixels. Read off the built artefact and corrected
in the harness before the suite ran: W18's y 212 → **216**, W20's x 1088 / y 65 → **1072 / 389**. Neither
correction touches a declared firing set, and both were found by asserting the needle's uniqueness rather
than by a crash — the `assert txt.count(head) == 1` in every mutation is what made this a pre-run check.

**W20's premise was measured, not argued, before the suite ran.** Against the normaliser as 5H-3 left it,
`−180.96` (U+2212) normalises to `180.96` and compares to the cell 180.9616556284141 with an error of
**0.0017** against a tolerance of **0.005000** — a SILENT PASS. Against the hardened normaliser it
translates to `-180.96` and the error is **361.9217**. **The case cannot fire the old gate. That is the
whole content of F5H1-3, and it is now a number rather than a note.**

### §16.3 — Step 4, H-3's chain end to end — THE DECLARATION DOES NOT HOLD, AND THE REASON IS A TIMESTAMP

The ruling's Unit 5H-4 line reads: *"Run H-3's chain end to end from Brad's shell: extract → build →
gate; declared: CSVs byte-identical to pins, page byte-identical to the committed page."* The session ran
the chain in a full copy of the project on the device VM — **never on the mount**, precisely because the
extract writes the manifest and the mount's manifest is a pin. Measured:

- `era_ph5_extract.py` md5 `5737ec29…`, which is the `script_md5` the manifest records: the same script.
- The extract's own gate: **57 of 57 PASS**. The four grains it wrote are **byte-identical to their pins**:
  `84fe4dbf…`, `3e8825ac…`, `f5b3638a…`, `fc1fa4b1…`. So is `era_ph5_dictionary_v1.0.md` (`41d01c84…`)
  and `era_ph5_style_v1.0.md` (`88704aa9…`). **First half of the declaration: HIT.**
- **`era_ph5_grains_manifest.json` is NOT byte-identical** — `fa8f7f8e…` against the pin `d28ed340…` —
  and the ONLY difference is five `written_utc` values, which the extract stamps from the wall clock:
  `2026-09-05T03:44:09Z` against `2026-09-04T22:18:28Z`. Every md5, row count, column count, byte count,
  `db_md5` and `user_version` in it is identical.
- **The page therefore is not byte-identical either.** Both are **193,712 B** and **848 lines**; they
  differ on **exactly one line** — line 813, the embedded manifest — in **exactly ten substrings**, all
  five timestamps. Normalise `written_utc` and the two files are **IDENTICAL**. `ffbb7a5e…` against
  `2f7b7a75…`. **Second half of the declaration: MISS, and it is a MISS the ruling could not avoid.**

**This is recorded as a MISS against the checkpoint, not repaired.** Repairing it means changing
`era_ph5_extract.py` so `written_utc` derives from content rather than from the clock, and that script is
the producer of the frozen contract: its md5 is recorded inside the manifest it writes, the manifest's md5
is a pin cited in project memory and in three results sections, and H13a compares the page's embedded copy
against it. Changing it moves all of those. **The test 4R set is "does the scoped work exist without it" —
it does: the page is built, gated, tamper-tested and rendered.** Routed to the strategy chat as a ruling
question (§16.6), with the honest restatement of the checkpoint offered: *the chain reproduces the
committed page to the byte outside the manifest's five write stamps*, which is what freshness by
construction actually requires and is exactly measurable.

### §16.4 — Step 5, the renders, and Step 6, the G4 re-check

**Renders — six committed, all six read (H-4; the ruling commits them from this unit on).** Cloud
container, Playwright Chromium 1194, `file://`, at `device_scale_factor=2`, rendered twice with
`java_script_enabled=True` and `False`. **Every probe is identical between the two runs**, which is what
measures "the page shows its saved state with script disabled": with script off the checked inputs read
`['Columbus', 'IT']` from the markup, V4 draws **0** `<line>`, V2 draws **22** connectors, a connector's
computed stroke is `rgb(204,215,227)` (`--era-rule`) on a 1 px box, Columbus's V4 dot is
`rgb(162,194,226)` (`--era-accent-200`, ramp step 1), and the V5 guide is a 1 × 89 px hairline at x 809.5
with Chicago's central label starting clear to its right. Committed as `renders/era_ph5_v1.png` …
`v6.png`, 2560 px wide (2× of the 1280 px page), read by the session:

- **V4** — the frame is gone and the eight dots carry eight readable weights; Dallas-Fort Worth palest,
  Columbus distinctly lighter than Chicago, San Jose and Atlanta darkest. The three metros the top of the
  ranking depends on are three different colours, which is what F5H3-7 asked for.
- **V5** — `37.46 ▉▉▉ 57.88` reads as an interval; the 14 px Chicago bracket and the 8 px Northern
  Virginia bracket now read as NARROW instead of spanning their rows; the crossing guide passes to the
  left of Chicago's `81.54` with no overprint, and Columbus's band visibly ends past it.
- **V2** — three hairlines join Columbus's walk from DCT-T's right edge down to the mitigated total. The
  two delta bars are still nearly invisible against a 546 M baseline — that is the data, not the drawing —
  but the walk now reads AS a walk, which it did not before.
- **V3** — the fixed channel's `226,130.88` sits clear to the left of the zero rule instead of on it.
- **V1** — the ramp now runs monotonically light to dark down the ranking; Austin and Northern Virginia
  share step 3, the one collision eight values into seven steps forces.
- **V6** — 21 rows, `C-FERC-H13` first with both dollar cells empty, the three `unpriced` above the
  eleven `limitation` rows.

**The committed renders are PIXEL-identical to the ones the session read, and NOT byte-identical.**
`device_commit_files` re-encodes the PNG stream: `era_ph5_v4.png` is 48,307 B in the container and 54,077 B
on the mount, magic bytes intact, 2560 × 988 both, and the decoded RGBA buffers hash the same
(`e6f9c0a7…`). Recorded so no later session reads the size or md5 difference as a content difference —
the same class of note as F5H0-6's CRLF.

**G4 reconciliation, re-checked.** V6 draws **21** rows for G4's **21**, order equals `sort_rank`, **zero**
cell mismatches, and no row borrows another row's credit. `era_ph5_grain_gate.py` standalone: **29 PASS /
0 FAIL**. **G4's `source_ref` files: FIVE, not four.** §14.4 listed `era_ph4_report_v1.1.md`,
`era_ph2_report_v1.2.md`, `era_ph5_dictionary_v1.0.md` and `direction_ph1_tariff_db_v1.0.md`; one
`source_ref` is a compound (`direction_ph1_tariff_db_v1.0.md; semester-plan.md`) and a split on the wrong
delimiter hides the second file. **All five are present on the mount.**

### §16.5 — State after the unit

**Unchanged, measured on the mount after every run:** `era_rates.db` `1c72e7a1b32c99a650d2e1fba17ae21e`,
`user_version` 14, its 0-byte journal of Aug 29 untouched; **the four grains at their E-1.4 pins**
(`84fe4dbf…`, `3e8825ac…`, `f5b3638a…`, `fc1fa4b1…`); **the manifest still `d28ed340…`** — the chain was
run in a VM copy and never on the mount, exactly so this pin would not move; style `88704aa9…`;
dictionary `41d01c84…`; `era_ph5_grain_gate.py` `7c1cf9a3…`; `era_ph5_extract.py` `5737ec29…`.
**Retired files untouched and unread:** `era_ph5_dashboard.twb` `20dcb01d…`, `era_ph5_workbook_gate.py`
`689b1354…`. No SQLite write. No `.tmp` on the mount. **No log written to the mount** — Brad's committed
5H-3 logs are byte-untouched and still carry their `Unit 5H-3` headers.

| file | md5 | what |
| --- | --- | --- |
| `era_ph5_views.py` | `642523c11cb345ddd380162416a11abf` | `ordinal_ramp` replaces `ramp_index` (V1 and V4); V4's frame dropped; V5's three label kinds anchored to their marks at `V5_LABEL_GAP`; V3's sub-grid-unit nudge; `_v2_connectors` and the connector marks |
| `era_ph5_build_html.py` | `1981d0bbeb80c1fe2cfb83b5d7f13fd1` | one CSS rule, `.era-wf-connector` |
| `era_ph5_page_gate.py` | `adfb41a9eacceff9cee1318c24ffa34a` | `gate_ordinal_ramp` replaces `gate_ramp_index`; `view_ink`, `gate_wf_pairs`, `_walks`, `_row_rect`; V4b + 2 clauses, V5b + 1, V3b + 1, V2b + 1, V6c + 1; T2's normaliser; the §15.3a guard; header declares §15.3 |
| `era_ph5_page_tamper.py` | `3924058d1293c10b0967b159df6f07de` | **W14, W17, W18, W19, W20, W21 added**; every carried set re-derived and unchanged; `BASELINE` still `set()` |
| `era_ph5_dashboard.html` | `2f7b7a750dd6b121841e5a68589cb1f0` | **193,712 B, six views, gate-accepted** |
| `README.md` | `484eb46fc48b0633b753dc05dd82fefd` | new section "The dashboard page": what it is, the three-command rebuild, and the manifest-timestamp caveat |
| `renders/era_ph5_v1…v6.png` | `65689b5b…`, `3f6a0ad0…`, `7d592c85…`, `4c6e1d03…`, `70bc80af…`, `392fb13a…` | 2× renders of the six views, committed |

**Checkpoint (`direction_ph5_html_v1.0.md`, Unit 5H-4), measured:**

1. the full gate passes with zero FAIL and zero SKIP-BLIND — **MEASURED HIT** (75/0/0/0, exit 0);
2. six renders committed and read — **MEASURED HIT**;
3. the page opens from disk with script disabled showing its saved states — **MEASURED HIT**
   (`['Columbus','IT']` from the markup, every probe identical with script on and off);
4. G4 reconciliation re-checked, README section added — **MEASURED HIT**;
5. **the chain reproduces the committed page to the byte from Brad's shell — MISS, and structurally so
   (§16.3): the four grains reproduce to the byte, the manifest's five wall-clock stamps do not, and the
   page embeds the manifest. Routed, not repaired.**
6. **OPEN: `era_ph5_5h_gate_run.log` and `era_ph5_5h_tamper_run.log` must be RE-WRITTEN from Brad's
   shell** (F5B-9). This session wrote no log to the mount; the closeout hands him the commands.
   **5H-5 checks for headers reading `Unit 5H-4` and does not take this paragraph as fact.**

### Findings

- **F5H4-1. H-3's chain cannot reproduce the committed page to the byte, and the obstacle is a wall-clock
  stamp rather than the data.** Measured end to end (§16.3): four grains byte-identical to their pins, the
  dictionary and the style file byte-identical, and one manifest field — `written_utc`, written five times
  — different, which propagates into the page because the page embeds the manifest verbatim so H13a can
  compare them. Both pages 193,712 B, 848 lines, one differing line, ten differing substrings, IDENTICAL
  after normalising that field. **The ruling declared an identity its own architecture forbids**, and
  neither the ruling nor any of the four preceding units caught it, because no unit before this one ran
  step 1. **A chain declared but never run is a prediction, and this is the fourth time in Phase 5 that
  running one found the gap (F5H1-1, F5H2-2, F5H3-1, now this).** Routed.
- **F5H4-2. Fixing the ramp was not the hard part; deciding which views it governs was.** F5H3-7 named V4,
  but V1's IT state ramps the SAME column with the SAME rule and carried the SAME collapse — Columbus and
  Chicago one colour, step 5 unused. Repairing V4 alone would have put two colour semantics for one column
  on one page, which is worse than the defect, and no gate anywhere would have noticed: `era-ramp` appears
  in the gate only inside V4b, so V1's ramp is ungated and always was. **The scope of a drawing finding is
  not the view it was observed in; it is the rule it names.** Both views moved.
- **F5H4-3. Eight values into seven steps forces exactly one collision, so the question is WHERE, and the
  linear rule put it in the worst place available.** Linear: steps 0,1,1,2,3,3,4,6 — two collisions, step 5
  unused, and one collision landing on Columbus/Chicago, the two banded metros whose adjacency C-BAND-25 is
  about and whose crossing B4 gates. Ordinal: 0,1,2,3,3,4,5,6 — one collision, all seven steps used, and it
  falls on Austin/Northern Virginia, ranks 4 and 5, neither banded and neither part of any ruled claim.
  **The improvement is not "more colours"; it is that the unavoidable ambiguity was moved off the metros the
  page's claims depend on.**
- **F5H4-4. The overprint was a symptom; anchoring was the defect.** F5H3-8 recorded two things — labels
  anchored to the row, and the crossing guide overprinting Chicago's `81.54` — and the obvious repair for
  the second is a special case (split the guide, or nudge that one label). One uniform rule fixes both:
  every V5 value label sits one grid unit from ITS OWN mark, so the central label no longer straddles the
  tick and the guide has nothing to cross. **The guide's geometry did not move, which is what let B4 —
  which gates that geometry — stay PASS without being touched.** Prefer the rule that removes the class of
  defect to the patch that removes the instance.
- **F5H4-5. A clause that cannot be fired alone is recorded as such, not engineered around.** V4b's
  least-ink clause and its no-frame clause both fire on W14, because restoring the four frame hairlines is
  the only way to make V4 not-least-inked and it necessarily restores the frame. Rather than invent a
  second case that adds five non-frame marks to V4 — a page nobody would ever build — the two-clause
  firing is DECLARED (§15.2) and recorded. **F5H3-2 asks whether a clause can be fired at all; it does not
  require that every clause be separable, and pretending otherwise produces fictional tampers.** The same
  question answered the other way for V3b, where the choice of row mattered: the fixed channel is the only
  row the sub-grid-unit clause quantifies over, so W18 had to be that row or it would have been silent.
- **F5H4-6. H5/H6 cannot see a view-code regression, which is why every drawing rule in this unit got a
  clause.** The reproduction gate rebuilds the page from the same `era_ph5_views.py` and
  `era_ph5_build_html.py` it is checking, so an edit to a view function, or to the build's `VIEWS`
  constant, reproduces itself exactly and H6 stays PASS. H6 catches a hand-edited PAGE; nothing caught a
  changed BUILD. **That is the precise reason the six drawing findings went unseen for four units, and the
  reason this unit's answer was seven gate clauses rather than seven prettier drawings.**
- **F5H4-7. The G4 `source_ref` set is five files, not four.** One cell is compound
  (`direction_ph1_tariff_db_v1.0.md; semester-plan.md`) and a split on the wrong delimiter drops
  `semester-plan.md`. All five are present. Cosmetic against §14.4's list; recorded because the same
  splitter would silently under-report if a source went missing.
- **F5H4-8. `device_commit_files` re-encodes a PNG.** The six committed renders are PIXEL-identical to the
  ones the session read (decoded RGBA md5 equal) and byte-different (48,307 B → 54,077 B on V4). Recorded
  so no later session reads the size or md5 difference as a content difference. Same class as F5H0-6.

### Routed

**ONE RULING QUESTION, to the strategy chat.** **F5H4-1: H-3's "the chain reproduces the committed page to
the byte" cannot hold while `era_ph5_extract.py` stamps `written_utc` from the wall clock and the page
embeds the manifest.** Three resolutions exist and the session ruled on none of them:

1. **Restate the checkpoint** — the chain reproduces the committed page byte for byte OUTSIDE the
   manifest's five write stamps. Costs nothing, changes no file, and is exactly measurable; the page gate
   could carry the normalised comparison as a clause so the claim is gated rather than asserted.
2. **Derive `written_utc` from content** (the DB's own stamp, or drop the field). Makes the literal
   identity true, but edits the producer of the frozen contract: its `script_md5` is recorded inside the
   manifest it writes, and the manifest md5 `d28ed340…` is a pin cited in memory and in three results
   sections. A Phase 5 file that has not been touched since 5A.
3. **Leave it and record it.** The weakest: a checkpoint that is known to be unmeetable and stays written
   is how a discipline erodes.

**The session's own reading, offered as a note and not a decision:** (1) is the smaller change and the more
honest claim, because the timestamp is metadata ABOUT the extract run and not data the page shows; a
freshness guarantee that requires the clock to stand still is not the guarantee H-3 was written to give.

**Notes to the strategy chat, no ruling requested.** F5H4-6 is the general form of what F5H2-1 and F5H3-4
found case by case: **the page's strongest gate, H6, is blind to exactly the layer the last two units spent
themselves on.** If one sentence goes into a standing rule from this unit, it is that one. Separately,
5H-3's suggestion that "a figure whose basis the contract cannot express is not typed" (F5B-2, F5H1-5,
F5H2-3, F5H3-3) has not been touched by this unit and still stands as a candidate standing rule.

### Conventions 5H-5 must follow (the Phase 5 report and the Phase 6 queue)

- **Check the log headers read `Unit 5H-4` before treating this unit as complete, and take no paragraph
  above as fact** (F5B-10). The page on disk should be `2f7b7a750dd6b121841e5a68589cb1f0`, 193,712 B, the
  gate 75 PASS / 0 FAIL / 0 SKIP-BLIND / 0 SKIP-OK with an EMPTY FAIL set and exit 0, the tamper suite
  **29 of 29**. **If the gate reports anything else, the unit is blocked: report, do not repair.**
- `BASELINE` is `set()`, every firing set is absolute, **W01 still leads** and N01 runs last.
- **The report's account of the chain must be §16.3's, not H-3's.** Do not write "the chain reproduces the
  page to the byte" into `era_ph5_report_v1.0.md` unless the strategy chat has ruled on F5H4-1 and the
  ruling has been executed. State what was measured: four grains to the byte, the page to the byte outside
  five timestamps.
- **The renders are committed and are portfolio artefacts (H-4).** They are pixel-stable, not byte-stable,
  across a device commit (F5H4-8) — do not gate them on md5.
- The report's figures are re-derived from the grains by a script, per the ruling. The grains are at their
  E-1.4 pins and the manifest at `d28ed340…`; **running `era_ph5_extract.py` on the mount would move the
  manifest pin and force a page rebuild for no gain.** Run it in a copy, as this unit did, or not at all.

---

# Unit 5H-5 — the Phase 5 report and the Phase 6 queue

`direction_ph5_html_v1.0.md` Unit 5H-5 (was 5E of `direction_ph5_tableau_v1.0.md`). One chat.
Everything below §17 was written BEFORE the run it predicts, in the order the protocol requires.

## §17 — What this session verified first, and what it declares before any run

### §17.1 — 5H-4's checkpoint item 6, checked rather than assumed — CLOSED

The handoff prompt carried the same conditional 5H-2's and 5H-3's did (*"if the logs do not read `Unit
5H-4`, record item 6 as still open"*). **They do.** Read off the mount before anything else:

- `era_ph5_5h_gate_run.log` header: `era_ph5_page_gate.py  Unit 5H-4  project=C:\Users\User\Claude\Projects\Electrical Rate Analysis  page=era_ph5_dashboard.html  python=3.13.5  platform=Windows-11-10.0.26200-SP0  page_md5=2f7b7a750dd6b121841e5a68589cb1f0`; last block `RESULT 75 PASS  0 FAIL  0 SKIP-BLIND  0 SKIP-OK` / `FAIL SET (empty)`.
- `era_ph5_5h_tamper_run.log` header: `era_ph5_page_tamper.py  Unit 5H-4  project=C:\Users\User\Claude\Projects\Electrical Rate Analysis  python=3.13.5`; `BASELINE  clean page FAIL set is EMPTY as declared (0 ids)`; last line `RESULT 29 of 29 AS DECLARED (W01 ran first, V1 built)`.
- `era_ph5_dashboard.html` on disk: **`2f7b7a750dd6b121841e5a68589cb1f0`**, 193,712 B, 848 lines, six `data-view` slots — the md5 in Brad's own gate header is the md5 of the file that is there.

**Item 6 is CLOSED. Unit 5H-4 is CLOSED on every item except item 5, which is the routed MISS
(F5H4-1) and is not a checkpoint this unit can close.** The session then re-ran both harnesses itself
in a VM copy (never on the mount, no `--log`): **gate exit 0, 75 PASS / 0 FAIL / 0 SKIP-BLIND / 0
SKIP-OK, FAIL SET (empty); tamper `RESULT 29 of 29 AS DECLARED (W01 ran first, V1 built)`.** Two
independent runs, Brad's shell and the VM, agree. The unit is not blocked.

**This is the third consecutive unit whose handoff premise about the logs was wrong in the same
direction, and it is now the second time the premise was wrong the same way twice running.** Recorded
as F5H5-1 rather than as a note, because a conditional that has been false three times in a row is a
convention that should be inverted.

### §17.2 — The ruling question F5H4-1, and this session's judgement on whether the report can be written

The prompt asks the session to decide one thing and route rather than decide the other. **Judgement:
`era_ph5_report_v1.0.md` CAN be written without a ruling on F5H4-1, and this session does not rule
on it.** The reason is that §16.3 produced an exactly measurable statement and a report publishes
measurements:

> the four grain CSVs, the dictionary and the style file reproduce byte-identically to their pins;
> the manifest differs in exactly five `written_utc` values and in nothing else; the rebuilt page is
> the same 193,712 bytes and 848 lines as the committed page, differs on exactly one line, and is
> identical after normalising that field.

That sentence is what goes into the report. **H-3's sentence — "the chain reproduces the committed
page to the byte" — is NOT written into the report**, and gate `X1` asserts its absence, so the
prohibition is gated rather than remembered. The choice between §16.6's three resolutions stays with
the strategy chat; the report carries F5H4-1 as an open ruling question in a section separate from
the ruled Phase 6 queue, so the queue this unit assembles is exactly the queue that was ruled.

### §17.3 — What the report is, and the one thing 5E asked for that does not exist

`era_ph5_report_v1.0.md`, per Unit 5E's scope as amended by H-1/H-4: what the page shows, what it
deliberately does not, the four grains and their bases, gate coverage, the Tableau record as the
reason for H-1, Phase 5's own findings, and the ordered Phase 6 pre-flight queue.

**5E's checkpoint also asks for "the public link", and there is none.** Under H-4 the deliverable is
one file that opens from disk; the public URL is the bradmachado.com subdomain deployment, which is
the SECOND item of the Phase 6 queue and has not happened. **The report says so and prints no URL;
gate `X4` asserts the report contains no `http` URL at all.** Recorded as F5H5-2: a checkpoint clause
written under the Tableau ruling survived into a unit list the HTML ruling rewrote, and the honest
discharge of it is a stated absence, not an invented link.

### §17.4 — The gate: `era_ph5_report_gate.py`, six groups, and the false-pass question asked of each

The ruling requires "a script that re-derives its figures from the grains". Two duties, taken from
the page gate's group T because the failure mode is identical:

- **every figure the report shows is credited to something that can be re-derived** (T1's duty: the
  count of UNCREDITED figures is ZERO), and
- **every credited figure equals what it cites** (T2's duty, at the precision shown).

Credit kinds, the markdown analogue of the page's `data-src`, written as HTML comments so they are
invisible when the file renders:

| kind | form | resolved against |
| --- | --- | --- |
| `G` | `<!--G:G1:Chicago:usd_per_it_mwh-->` | a grain cell, by row key and column |
| `D` | `<!--D:portfolio_baseline_usd-->` | a named derivation over the four grains, computed in the gate |
| `F` | `<!--F:era_ph5_dashboard.html:md5-->` | a fact about a file on disk: `md5`, `bytes`, `lines`, `rows` |

**Blocks carry the tables.** A region delimited by `<!--ERA-BLOCK:name-->` … `<!--/ERA-BLOCK:name-->`
is REGENERATED by the gate from the grains and must equal the file's content byte for byte. A block
is stronger than a credit, so every table in the report is a block and blocks are not scanned for
credits. Ten blocks: `ranking`, `channels`, `stack`, `bands`, `excluded`, `caveats`, `grains`,
`monthly`, `gatecoverage`, `tampercoverage`.

**The F5H2-1 question, asked of every group before it was written.** *Could this gate be satisfied by
a report that does not say what it claims?*

- **Group R (the blocks).** The generator reads only the four CSVs plus, for `gatecoverage` and
  `tampercoverage`, the live page gate and the tamper module's own `CASES` table. It shares no
  constant with the report text. **It is therefore NOT the F5H4-6 shape**, where H5/H6 rebuild the
  page from the code they are checking: here the reference is the data, and the artefact is prose a
  human wrote. Positive controls X01 (a CSV cell perturbed) and X02 (a digit changed in the report's
  table) must fire it from both sides — that is what proves it is connected to the data AND to the
  file.
- **Group C (the credits).** C1 could pass vacuously on a report with no figures, so it reports the
  scanned and figure counts and FAILS if nothing was scanned. C1 could also be evaded by hiding a
  figure inside an identifier, so identifier exclusions are WHOLE-TOKEN patterns, the count and the
  distinct forms of every exclusion are printed, and no exclusion pattern matches a bare decimal.
  Backtick spans are excluded from scanning and C1 separately asserts that no backtick span is a
  bare number.
- **Group Q (the queue).** A queue gate that reads its order from a constant in its own gate is
  self-satisfying. The constant therefore CITES the two direction files it was derived from and Q2
  pins both by md5, so the gate fails the moment a ruling text moves under it. This is the
  "measurement constant versus ruling constant" rule applied to a list.
- **Group X (the prohibitions).** Absence gates are the easiest to satisfy vacuously, so each one
  names the exact string it forbids and X01/X05 are positives that type the forbidden string in.
- **Group A (assembly).** Structure only; it can pass on a report with correct headings and wrong
  content, which is why it is five gates and not the acceptance.
- **Group D (the grains).** `era_ph5_grain_gate.group_d`, imported and run unchanged — the report's
  figures mean nothing if the grains are not the pinned ones.

### §17.5 — DECLARED before the run

**Gate tally — `era_ph5_report_gate.py` on `era_ph5_report_v1.0.md`:**

| group | ids | count |
| --- | --- | --- |
| D | `era_ph5_grain_gate.group_d`, unchanged | **29** |
| A | A1 A2 A3 A4 A5 | **5** |
| R | R1…R10, one per block | **10** |
| C | C1 C2 C3 C4 C5 | **5** |
| Q | Q1 Q2 Q3 Q4 Q5 | **5** |
| X | X1 X2 X3 X4 | **4** |
| | **TOTAL** | **58** |

**Declared: 58 PASS, 0 FAIL, 0 SKIP-BLIND, 0 SKIP-OK, FAIL SET empty, exit 0.**

Figures declared EXACT rather than weak, because each is derivable before the run rather than
guessed (the 5H-4 discipline, and the correction of 5H-3's four WEAK misses):

- **grains 8 × 73, 33 × 16, 384 × 24, 21 × 12**; portfolio baseline **$6,694,135,866.22**, mitigated
  **$6,419,218,640.05**, mitigation **4.106837 %**; spread ratio **3.795926**; excluded band
  **$-741,104,525.28**, **2.695737 ×** the whole mitigation; rider channel **$-167,099,502.51**
  against energy **$-87,551,080.84** and demand **$-37,732,405.75**; tightest adjacency **7.9209**
  $/IT-MWh; the C-BAND-25 crossing **0.80423602** $/MWh on the facility basis and **1.08102537** on
  the IT basis; Northern Virginia's ratchet **11** months.
- **`gatecoverage` re-derives to 75 gates** in the group counts the live run reports;
  **`tampercoverage` re-derives to 29 cases** from `era_ph5_page_tamper.CASES`.
- The report cites the page as **`2f7b7a750dd6b121841e5a68589cb1f0`, 193,712 B, 848 lines**, the four
  grains at `84fe4dbf…`, `3e8825ac…`, `f5b3638a…`, `fc1fa4b1…` and the manifest at `d28ed340…`.

**WEAK (a guess, marked as one):** the report is between 25 and 45 KB, and it carries between 120 and
220 credited figures outside the blocks.

**Tamper suite — `era_ph5_report_tamper.py`, six cases, firing sets ABSOLUTE against an EMPTY clean
baseline, X01 FIRST and N01 LAST (F5B-3):**

| case | kind | declared firing set | why |
| --- | --- | --- | --- |
| **X01** | data | **{R1, R2, R3, R4, R5, R8, C2, C3}** | Chicago's `usd_per_it_mwh` is perturbed by +1.00 in a COPY of `era_ph5_metro.csv`. Every block that draws that cell moves; the two credit gates that resolve against it move; group D is NOT in the set because D reads no absolute value of that column, and the blocks that do not draw Chicago (`caveats`, `grains`, `gatecoverage`, `tampercoverage`) do not move. **RUNS FIRST.** |
| **X02** | text | **{R1}** | one digit of Chicago's mitigated figure is changed inside the `ranking` block in a copy of the report. The block no longer equals its regeneration. Nothing else reads that block, and the credits outside it are untouched — this is the case that proves R is connected to the FILE and not only to the data. |
| **X03** | text | **{C1}** | a bare `47.67` is typed into a prose sentence with no credit comment. The uncredited count goes to one. C2/C3/C4 stay PASS because no existing credit moved, which is what scopes the firing. |
| **X04** | text | **{C2}** | one credited figure's digits are changed while its credit comment is left alone: the report now shows a number that is not the cell it cites. C1 stays PASS — the figure is still credited — and that is the whole point of having two gates rather than one. |
| **X05** | text | **{X1}** | H-3's forbidden sentence, verbatim, is typed into the report. The prohibition fires and nothing else does. |
| **N01** | control | **(nothing fires)** | an unmodified copy. Runs LAST. |

**Declared: `6 of 6 AS DECLARED`, X01 first, N01 last.**

**Predicted misses, written down so a hit is a measurement rather than luck.** The likeliest is
**X01's set**: `C2`'s and `C3`'s membership depends on whether any credited PROSE figure resolves to
Chicago's `usd_per_it_mwh` or to a derivation that reads it, and the report text is written before
the harness. If the prose happens to cite that cell only inside blocks, `C2` and `C3` will be silent
and the declaration will be a MISS. **It will be recorded as a MISS and the declaration amended in
writing beside itself, never edited in place (F5H2-7).**

### §17.6 — What this unit will not do

No file on `era_ph5_extract.py`'s side of the chain is touched, so the manifest stays `d28ed340…` and
the four grains stay at their E-1.4 pins; **the extract is not run on the mount, in this unit or any
other** (5H-4's note). No retired file is opened. No render is gated on md5 (F5H4-8). Nothing in
`era_rates.db` is read or written. `era_ph5_dashboard.html` is not rebuilt: the report describes it,
and if a figure in the report and a figure on the page disagreed, the gate would say so, because both
resolve to the same four CSVs.

### §17.5a — X01's declared set was INCOMPLETE. The MISS, and the amendment, written before the re-run.

**First run of `era_ph5_report_tamper.py`: `RESULT 5 of 6 AS DECLARED (X01 ran first, N01 last)`.**
`BASELINE  clean report FAIL set is EMPTY as declared (0 ids); 58 PASS / 0 FAIL, exit 0`. X02, X03,
X04, X05 and N01 fired exactly their declared sets on the first run. **X01 MISSED**, and the
declaration is amended here rather than edited in place, because the results file is the measurement
(F5H2-7) and a failing assertion is never rewritten to pass (4A).

| | ids |
| --- | --- |
| declared, §17.5 | `C2 C3 R1 R2 R3 R4 R5 R8` |
| actual | `C3 D11a D11c R1 R4 R7` |
| undeclared firing | `D11a D11c R7` |
| declared but silent | `C2 R2 R3 R5 R8` |

**Why each of the three undeclared firings is CORRECT and the declaration was wrong:**

- **`D11a`.** §17.5 said group D was out of the set "because D reads no absolute value of that
  column". False. `D11a` asserts `usd_per_it_mwh = annual_usd / it_annual_mwh` in every metro to
  1e-6; moving the numerator of an identity breaks the identity. **Group D is not a set of range
  checks; it holds derived identities, and a perturbed cell is exactly what they exist to catch.**
- **`D11c`.** The band on the siting metric is the metered band scaled by
  `usd_per_it_mwh / usd_per_mwh`. Move the ratio and the scaling no longer reproduces the stored
  band edges. The declaration missed it for the same reason it missed `D11a`.
- **`R7`, and this is the one worth carrying.** The `grains` block prints the **md5 of each CSV**, so
  the block that names the pins is precisely the block that must notice a perturbed CSV. **It is the
  report's own freshness clause — the analogue of the page's `H13` — and the declaration did not
  think of it at all.** A tamper declaration written by reasoning about which tables *draw a figure*
  will always miss the table that *names a hash*.

**Why each of the five silent gates is CORRECT to stay silent, which is what scopes the case:**

- **`R2`, `R3`, `R5`, `R8`.** `channels` draws the five mitigation channel columns; `stack` and
  `excluded` draw G2; `monthly` draws G3. **None of them draws G1's `usd_per_it_mwh`.** §17.5's
  phrase "every block that draws that cell" was right as a rule and wrong as a count: only two
  blocks draw it.
- **`C2`.** No prose G credit resolves to Chicago's `usd_per_it_mwh`. The report's five G credits are
  Austin's PUE level, Austin's alpha, Austin's IT energy, Austin's mitigation share and Phoenix's
  mitigation share. **§17.5's own predicted-miss note named this exact possibility before the run**,
  which is the only reason this MISS is a measurement rather than a surprise.
- **`C3` fires and is in both sets.** `band_crossing_it` is Columbus's IT-basis band high minus
  Chicago's `usd_per_it_mwh`, so the derivation moves and the prose figure no longer equals it.

**AMENDED DECLARATION for X01, in force from the re-run:**

> **X01 fires exactly `{D11a, D11c, R1, R4, R7, C3}`** — a derived identity, a band-scaling identity,
> the ranking block, the interval block, the block that carries the grain md5 pins, and the one
> derivation that reads the perturbed cell. Six ids across three groups. The other twenty-eight ids,
> including the four blocks that read other grains and the credit gate that resolves against other
> cells, stay PASS, and that is what scopes the case.

**No threshold moves, no gate id is added or removed, and no gate is edited.** Only the prediction
about which of them a data perturbation reaches. **The amended set asserts MORE of the gate than the
guess did** — it reaches group D and the pin block, neither of which the guess touched.

**Amended declaration for the suite: `6 of 6 AS DECLARED`, X01 first, N01 last, on the re-run.**

**One needle was corrected before the first run, not after.** X02's two-cell needle
`| 591,589,837.26 | 74.95 |` occurs TWICE in the report — once in the `ranking` row and once in the
`stack` block's mitigated-total row — and `replace_unique` refused to edit rather than editing the
wrong one. Widened to the four-cell form `| 81.54 | 591,589,837.26 | 74.95 | 8.08 |`. **Mechanics,
not a declared-set change** (the 5H-4 discipline, and the second consecutive unit in which the
uniqueness assertion caught a stale needle as a pre-run failure).

## §18 — Results, in the order the runs happened, and the state after the unit

### §18.1 — Step 1, the verification — the unit was NOT blocked

§17.1. Log headers read `Unit 5H-4`; `era_ph5_dashboard.html` on the mount is
`2f7b7a750dd6b121841e5a68589cb1f0`, the md5 in Brad's own gate header. Re-run by this session in a VM
copy with no `--log`: **page gate 75 PASS / 0 FAIL / 0 SKIP-BLIND / 0 SKIP-OK, FAIL SET (empty), exit
0; page tamper `RESULT 29 of 29 AS DECLARED (W01 ran first, V1 built)`.** Two independent runs on two
interpreters agree. **5H-4 checkpoint item 6 is CLOSED.**

### §18.2 — Step 2, the report, and Step 3, its gate — DECLARATION HIT EXACTLY

`era_ph5_report_v1.0.md`, `e1dbf60872785fd66325945bfd2a3b92`, 31,682 B. Built in VM scratch by
splicing the gate's own block generator into a prose template, copied onto the mount, and re-run from
the project folder (4A). **The tables in the report were never transcribed by hand: the same function
that regenerates a block for the gate is the function that wrote it.**

`era_ph5_report_gate.py`, `6952eedf64ee38773809322a95b7813f`.
**`RESULT 58 PASS  0 FAIL  0 SKIP-BLIND  0 SKIP-OK` / `FAIL SET (empty)` / exit 0.** §17.5 hit:

| declared (§17.5) | measured | verdict |
| --- | --- | --- |
| 58 / 0 / 0 / 0, FAIL set empty, exit 0 | same | **HIT** |
| D 29 + A 5 + R 10 + C 5 + Q 5 + X 4 | same | **HIT** |
| grains 8 x 73, 33 x 16, 384 x 24, 21 x 12 | same, drawn by the `grains` block | **HIT** |
| portfolio $6,694,135,866.22 / $6,419,218,640.05 / 4.106837 % | same | **HIT** |
| spread ratio 3.795926; excluded $-741,104,525.28 at 2.695737 x | same | **HIT** |
| rider $-167,099,502.51, energy $-87,551,080.84, demand $-37,732,405.75 | same | **HIT** |
| tightest adjacency 7.9209; crossing 0.80423602 and 1.08102537; NoVA 11 months | same | **HIT** |
| `gatecoverage` re-derives to 75 from the LIVE page-gate run | `{D 29, H 7, H13 3, P 7, V 15, B 4, S 8, T 2}` = 75 | **HIT** |
| `tampercoverage` re-derives to 29 from `era_ph5_page_tamper.CASES` | 29 | **HIT** |
| page cited as `2f7b7a75…`, 193,712 B, 848 lines; grains and manifest at their pins | same, and gate `C4` compares all ten file facts on disk | **HIT** |
| **WEAK:** report between 25 and 45 KB | 31,682 B | **HIT** |
| **WEAK:** 120 to 220 credited figures outside the blocks | **44** | **MISS, and by a factor of three** |

**The WEAK count was wrong in the informative direction and it is recorded as a MISS, not rounded
away.** The guess assumed the report would carry its figures in prose. It does not: every table is a
block, blocks are not scanned, and what is left in prose is 44 figures against 124 in the first draft
before the identifier masking was corrected. **The reason the number is small is the reason the gate
is strong** — a figure inside a block is not credited, it is regenerated.

### §18.3 — Step 4, the tamper suite — 5 of 6, THEN 6 of 6 AFTER A WRITTEN AMENDMENT

`era_ph5_report_tamper.py`, `37f3203c1780fddf61428cb1774da0d3`.

- **Pre-run, not post-run:** X02's needle occurred twice in the report and `replace_unique` refused
  to edit. Widened to the four-cell form before any case ran. Mechanics (§17.5a).
- **First run: `RESULT 5 of 6 AS DECLARED (X01 ran first, N01 last)`.** X02, X03, X04, X05 and N01
  fired their declared sets exactly. **X01 MISSED**: declared `C2 C3 R1 R2 R3 R4 R5 R8`, actual
  `C3 D11a D11c R1 R4 R7`. Recorded, reasoned through id by id, and amended in writing in §17.5a
  **before** the harness was touched.
- **Re-run with the amended declaration: `RESULT 6 of 6 AS DECLARED (X01 ran first, N01 last)`,
  exit 0.** `BASELINE  clean report FAIL set is EMPTY as declared (0 ids); 58 PASS / 0 FAIL, exit 0`.

**The MISS is the most useful thing this unit measured.** §17.5 predicted a miss on X01 and named
`C2` as the likely cause; `C2` did stay silent for exactly the predicted reason. But the three
UNDECLARED firings were not predicted at all, and one of them is structural: **`R7`, the `grains`
block, prints each CSV's md5, so it is the report's own freshness clause and it fires on any
perturbed grain.** A declaration reasoned from "which tables draw this figure" cannot reach a table
that names a hash.

### §18.4 — Step 5, the Phase 6 queue, and what was deliberately not added to it

The queue is Unit 5E's list as amended by H-4: licensing review first, subdomain deployment of the
page second, the ten carried items after, `X13c` struck. **Twelve items, gated four ways** — `Q1` on
the order, `Q2` pinning the constant to the three direction files it cites by md5, `Q3` requiring
every `open_ruling_ids` value carried in G1 to be named, `Q5` on the two promoted items and every
title verbatim, `Q4` on the struck item.

**F5H4-1 was NOT added to the queue.** It is an open ruling question for the strategy chat, not a
unit of work, and the queue this unit assembles is the queue that was ruled. It is published in the
report's own section for carried ruling questions instead, with §16.6's three resolutions named and
none of them chosen.

### §18.5 — State after the unit

**Unchanged, measured on the mount after every run:** `era_rates.db` `1c72e7a1b32c99a650d2e1fba17ae21e`,
`user_version` 14, its 0-byte journal untouched; **the four grains at their E-1.4 pins**
(`84fe4dbf…`, `3e8825ac…`, `f5b3638a…`, `fc1fa4b1…`); **the manifest still `d28ed340…`**;
`era_ph5_dashboard.html` still `2f7b7a75…`; style `88704aa9…`; dictionary `41d01c84…`;
`era_ph5_grain_gate.py` `7c1cf9a3…`; `era_ph5_extract.py` `5737ec29…`; `era_ph5_views.py`
`642523c1…`; `era_ph5_build_html.py` `1981d0bb…`; `era_ph5_page_gate.py` `adfb41a9…`;
`era_ph5_page_tamper.py` `3924058d…`. **The extract was NOT run, in any copy.** No SQLite write. No
`.tmp` on the mount. **No log written to the mount** — Brad's committed 5H-4 logs are byte-untouched.
**Retired files untouched and unread:** `era_ph5_dashboard.twb` `20dcb01d…`, `era_ph5_workbook_gate.py`
`689b1354…`. The six renders are untouched and no md5 is claimed for them (F5H4-8).

| file | md5 | what |
| --- | --- | --- |
| `era_ph5_report_v1.0.md` | `e1dbf60872785fd66325945bfd2a3b92` | **the Phase 5 report, 31,682 B, ten sections, ten regenerated blocks, gate-accepted** |
| `era_ph5_report_gate.py` | `6952eedf64ee38773809322a95b7813f` | six groups, 58 gates; block regeneration + the group-T duty applied to markdown |
| `era_ph5_report_tamper.py` | `37f3203c1780fddf61428cb1774da0d3` | six declared positives; `BASELINE` `set()`; X01 first, N01 last |
| `README.md` | `932822c0b744971571623674f0988f9a` | new section "The Phase 5 report" |

**Checkpoint (`direction_ph5_html_v1.0.md`, Unit 5H-5, with Unit 5E's clauses), measured:**

1. the report is published and gated by a script that re-derives its figures — **MEASURED HIT**
   (58/0/0/0, exit 0; ten blocks regenerated from the CSVs byte for byte; 44 prose figures credited
   and compared, zero uncredited, zero orphan credits);
2. the Phase 6 queue is written, ordered, and gated — **MEASURED HIT**;
3. project memory carries the Phase 5 status block — **DONE in this unit's closeout**;
4. **"the public URL in the report and in project memory" — DISCHARGED AS A STATED ABSENCE**, not as
   a link. There is no public URL: under H-4 the deliverable is a file that opens from disk and the
   deployment is the second Phase 6 item. Gate `X4` asserts the report contains no URL at all
   (F5H5-2);
5. the `ph5-closed` annotated tag is issued in the closeout — **in part 1 of the closeout block**;
6. **OPEN: `era_ph5_5h_report_gate_run.log` and `era_ph5_5h_report_tamper_run.log` must be WRITTEN
   from Brad's shell** (F5B-9), so the committed logs name his path and his interpreter. This session
   wrote no log to the mount; the closeout hands him the two commands. **They are NEW files, so
   nothing needs deleting first.** A later session checks for headers reading `Unit 5H-5` and takes
   no paragraph above as fact.

### Findings

- **F5H5-1. A handoff conditional that has been false three times running is a convention to
  invert.** 5H-2, 5H-3 and 5H-5 were each told to record the previous unit's log item as still open
  if the committed logs lacked the expected header; all three times the headers were there. The
  clause is not wrong — *check the artefact* is the rule that contained F5B-10's damage and it must
  stay — but its default should be stated the other way round: **"check the headers; they are
  expected to read `Unit <n>`; record what you find."** Written as a prediction of absence, it
  primes a session to expect a blocked unit and to read a hit as an exception.
- **F5H5-2. A checkpoint clause can outlive the ruling that wrote it, and the honest discharge of
  one is a stated absence.** Unit 5E's checkpoint asks for "the public link" in the report and in
  memory. Under H-4 there is no public link and will not be one until the second Phase 6 item.
  Inventing a plausible URL, or quietly dropping the clause, are the two failure modes; **the report
  says there is none and gate `X4` asserts it contains no URL at all**, which turns a dropped clause
  into a gated claim. Same shape as H-3's chain sentence: a ruling's words outliving the architecture
  they were written for.
- **F5H5-3. A declared firing set is a prediction about DATA DEPENDENCIES, and the id it missed was
  the one that names a hash.** X01's declaration reasoned about which tables *draw* the perturbed
  figure and therefore reached only blocks. It missed group D entirely — `D11a` and `D11c` are
  derived identities, and a perturbed cell is exactly what an identity catches — and it missed `R7`,
  the block that prints each CSV's md5 and is therefore the report's own freshness clause. **Ask of
  every data tamper: what else in the artefact names this file, rather than draws from it?** The
  general form of F5H1-2, one level up: not "re-derive the carried set" but "the set you are deriving
  is over dependencies you have not enumerated".
- **F5H5-4. Blocks are strictly stronger than credits, and the count proves it.** The first draft of
  the report carried 124 scanned figures in prose; the finished one carries 44, because every table
  moved into a regenerated block. A credit asserts *this figure equals that cell*; a block asserts
  *this entire table is what the data produces*, including its column set, its ordering, its
  formatting and its totals row. **Prefer regeneration to credit wherever a region can be
  regenerated** — the same instinct as "prefer removing a hazard by construction over gating it"
  (F5H4-4, H-3), applied to a document.
- **F5H5-5. The report gate is NOT the F5H4-6 shape, and it was designed against it on purpose.**
  The page's reproduction gate rebuilds the page from the same view code it is checking, so a
  view-code regression reproduces itself and passes. The report gate's reference is the four CSVs and
  the artefact is prose a human wrote; the two share no constant. X02 (edit the report, the data
  untouched) and X01 (edit the data, the report untouched) fire it from opposite sides, which is what
  proves it is connected to both. **The one place self-reference could have crept in — the Phase 6
  queue order, which lives as a constant in the gate — is pinned by `Q2` to the md5 of the three
  direction files it cites**, so a ruling that moves under the gate fails the gate.
- **F5H5-6. An orphan credit is a hole the size of the credit system, and it was found by writing
  the report rather than by reasoning about it.** Six figures were first drafted as spelled-out words
  wearing credit comments — `Three<!--D:market_priced_count-->`. The comment credits nothing, both
  comparison gates skip it silently, and the prose reads as gated while being gated by nothing.
  `C1` now asserts the orphan count is zero as well as the uncredited count. **Declared in writing
  (§17.5a) before the run, a SCOPE widening, no threshold moved.**
- **F5H5-7. The uniqueness assertion earned its place a second time.** X02's needle occurred twice —
  the ranking row and the stack block's mitigated-total row carry the same two cells — and the
  harness refused to edit rather than editing the wrong row and reporting a firing that meant
  something else. Second consecutive unit in which `replace_unique` converted a stale needle into a
  pre-run failure. **A tamper harness that does not assert its own needle is measuring an unknown
  edit.**

### Routed

**Nothing new is routed.** F5H4-1 remains the one open ruling question with the strategy chat and this
unit did not decide it: the report states §16.3's measurement and gate `X1` forbids H-3's sentence, so
the prohibition survives this session rather than depending on one. **The judgement this unit did
make, and states plainly: the report can be written without that ruling, because a measurement is
publishable and a checkpoint is not a figure.**

**Notes to the strategy chat, no ruling requested.** F5H5-1 (invert the log conditional in every
future handoff prompt) is a one-line change to the prompt template and would have saved three
sessions a paragraph each. F5H4-6 still stands as the sentence most worth promoting to a standing
rule, and F5H5-5 is its counter-example — a gate whose reference and artefact are genuinely
independent, which is what the page's H5/H6 cannot be by construction.
