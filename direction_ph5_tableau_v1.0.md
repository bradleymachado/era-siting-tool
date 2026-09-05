# Direction — Phase 5: the Tableau layer

`direction_ph5_tableau_v1.0.md` · 2026-08-28 · strategy ruling → Phase 5
**Blocked by Unit 4R** (`direction_ph4_close_v1.0.md`). Phase 5 opens when 4R closes and the two
extracts are frozen under Ruling 13.
Layer 5 of the architecture in [[siting-tool-architecture]]. Semester slot Nov 9–20; **the dates are
advisory and the project is running roughly ten weeks ahead of them. The unit sequence is binding.**

---

## 0 — What Phase 5 is actually for, stated once so the views can be judged against it

The siting tool answers one question: **what does a giga-scale campus cost per IT-MWh, where, and
how much of that is avoidable.** Phases 1–4 answered it to the cent. Phase 5's only job is to make
the answer *legible without a reader* — and to make the uncertainty legible at the same time, which
is the harder half and the half most dashboards skip.

Two failure modes to design against, both of them specific to this project:

1. **The order is robust and the absolute figures are not.** The three cheapest metros are the three
   market-priced ones (F2Fb-4), so the top of the ranking is the least certain part of it. A
   dashboard that shows eight bars and no bands publishes false precision.
2. **The biggest numbers in this project are the ones that are NOT in the totals** — the voltage
   siblings at $741 M/yr (2.7× the entire real stack), the unpriced FERC take-or-pay floor, the
   unpriced capex transfer. A view that shows only what was priced misrepresents the work.

---

## Ruling P5-1 — Sessions do NOT drive Tableau. Sessions write the build spec; Brad builds; sessions GATE the result.

Tableau Desktop is Brad's to operate. Every Phase 5 unit that touches the workbook delivers a
**build spec** — literal, numbered, sequential UI instructions per Brad's standing format
preference, with a calculated-field appendix — and Brad executes it.

**The workbook is then gated the way everything else in this project is gated: by a script that
parses it.** A `.twb` is XML. A session can read it, diff it, and assert against it without opening
Tableau. `era_ph5_workbook_gate.py` asserts field bindings, aggregation types, filter scope, the
colour tokens actually in use, and that no sheet is bound to a column outside the frozen contract.
**A view that looks right and is bound to the wrong field is the exact failure this project has
caught four times in SQL and once in a PDF parse.** It gets a gate here too.

## Ruling P5-2 — `.twb`, not `.twbx`. The extracts stay CSVs beside it.

`.twbx` is a zip; it is opaque to diff, opaque to the gate, and it duplicates the data. **The repo
holds `era_ph5_dashboard.twb` plus the committed extract CSVs.** A `.twbx` is produced only at
publication, in Unit 5D, and is not committed. Live text connections, not `.hyper` — at four
extracts of eight to a few thousand rows the performance argument does not exist, and diffability
does.

## Ruling P5-3 — No dashboard publishes without the caveats reachable from the front dashboard

Not a footnote, not a tooltip, not a second workbook. **A caveats sheet, reachable in one click from
the primary dashboard, driven by a DATA table (grain G4 below) rather than by typed text.** Typed
caveats drift from the report; a table that the gate reconciles against `era_ph4_report_v1.1.md`
cannot. This is the same rule as "a document that cites figures needs a script that re-derives
them", applied to the honesty layer.

## Ruling P5-4 — The aesthetic spec is written ONCE, in Unit 5A, as tokens, and the gate enforces it

Austere architectural presentation, per Brad's standing preference: maximum negative space,
structural alignment, one simple sans-serif, **strict monochromatic — one accent colour, distinction
by tint/tone/shade only, on stark white**, and text kept to labels. **Unit 5A writes the tokens** —
hex values, type sizes, grid, margins — into `era_ph5_style_v1.0.md`, and `era_ph5_workbook_gate.py`
asserts that the colours in the `.twb` are drawn from that list and nothing else. Diverging measures
(savings vs cost) use two ends of one ramp, never two hues.

## Ruling P5-5 — Publication scope

The repo stays **Private through Phase 5**; the licensing review is Phase 6. **Tableau Public
publication is in scope for Unit 5D**: every figure in the extracts derives from public tariff
filings and public market reports, so there is nothing confidential to expose, and the semester
plan's portfolio milestone requires the public link. **Deployment beyond Tableau Public — the
bradmachado.com subdomain in [[deployment-staging]] — is Phase 6 and is not touched here.**

---

# The units. One chat each. In order.

---

## Unit 5A — the extract contract: four grains, a dictionary, a style spec, and a gate. NO TABLEAU.

The unit that decides whether Phase 5 is cheap or expensive. It builds no views.

**Grains.** Four files, each with a stated key, each re-derived rather than copied where it can be:

| | file | grain | feeds |
| --- | --- | --- | --- |
| **G1** | `era_ph5_metro.csv` | metro (8 rows) | ranking, map, bands |
| **G2** | `era_ph5_stack.csv` | metro x component | waterfall, channel decomposition |
| **G3** | `era_ph5_month.csv` | metro x month x stage | seasonality, ratchet and dispatch views |
| **G4** | `era_ph5_caveat.csv` | one row per named caveat / unpriced item / open ruling, with metro scope, a `priced` flag and a `usd_per_year` where one exists | the caveats sheet (Ruling P5-3) |

**G1 is `era_ph4e_published_v1.1.csv` plus derived presentation fields and nothing removed.** The
frozen contract from Ruling 13 is the floor, not the ceiling.

**G3 is the unit's real problem and it is not to be assumed away.** `era_engine_v1.2_monthly.csv` is
on the Phase 2 metered basis; `era_ph4a_engine_monthly.csv` is on the facility basis. **Determine
which is on the published basis, state it, and re-derive the monthly series on that basis if
neither is.** A monthly view built on the wrong basis is a view whose totals do not tie to the
headline — assert the tie explicitly: G3 summed to the year must equal G1 to the cent, per metro,
per stage.

**G4 is not a text file with a header.** Minimum membership, each with its scope and its dollars
where they exist: the three voltage siblings and their $741,104,525/yr exclusion; the unpriced
capex transfer; the ComEd FERC Attachment H-13 take-or-pay floor (the largest unpriced item);
Ruling 14's signed and bounded PUE bias; Ruling 15's alpha domain; the ±25 % market bands and which
adjacency they touch; Chicago's declared-and-unratified 5CP window; the two open rulings
(`F4C-7`, `F4B-2`) and which metro each is on; F4D-8's and F4M-13's library gaps; Ruling 10's PG&E
unavailability; F4M-3's ERCOT construction residual; the retail-schedule proxy caveat.

**Also delivered:** `era_ph5_dictionary_v1.0.md` — every field in all four grains, its units, its
basis, its provenance, and whether it is re-derived or declared; and `era_ph5_style_v1.0.md`
(Ruling P5-4).

**Checkpoint — 5A is complete when** all four extracts exist and are written by one gated script;
G3 ties to G1 to the cent per metro per stage; G2 ties to G1 to the cent; every G4 dollar figure
reconciles against `era_ph4_report_v1.1.md`; the dictionary covers every column with no orphans in
either direction; a tamper suite exists with at least one injection per grain, each naming its
expected check and its blast radius.

> **Handoff prompt — Unit 5A**
> Read project memory, then `direction_ph5_tableau_v1.0.md`, `direction_ph4_close_v1.0.md` and
> `direction_session_protocol_v1.2.md`. Execute **Unit 5A** only — the four Phase 5 extract grains,
> the data dictionary, the style token spec and their gate. **No Tableau work in this unit.** G1 is
> Unit 4R's frozen contract plus derived fields, nothing removed. G3's basis question is real: work
> out which monthly series is on the published facility basis and re-derive if neither is, then
> assert that G3 sums to G1 to the cent per metro per stage. G4 carries the caveats as DATA, per
> Ruling P5-3. End with the closeout block per the session protocol, both halves.

---

## Unit 5B — the workbook skeleton and the three quantitative views

Brad builds; the session specs and gates. Deliverables: `era_ph5_build_5b_v1.0.md` (literal
sequential UI steps + calculated-field appendix), `era_ph5_workbook_gate.py`, and Brad's saved
`era_ph5_dashboard.twb`.

**V1 — the ranking.** Eight metros, horizontal bars, sorted, **$ per IT-MWh**, baseline and
mitigated shown together so the mitigation is a visible remainder rather than a second chart. The
metered $/MWh basis is available as a swap, never as the default — 2F established that $ per IT-MWh
is the correct siting metric because sites are compared at equal IT capacity.

**V2 — the waterfall**, from G2: baseline, each measure, storage, mitigated total, for the selected
metro. **The three voltage siblings appear as an explicitly excluded band, not as absent.**

**V3 — the channel decomposition**, five channels not two (F4E-3: the rider channel carries the
mitigation at −$167.1 M against −$87.6 M energy and −$37.7 M demand, which is the single most
counter-intuitive result in the project and should be visible without a click).

**Checkpoint — 5B is complete when** the three sheets exist in a saved `.twb`, the gate parses it
and passes, every mark is bound to a contract column, the sheet totals reconcile to
`era_ph4_report_v1.1.md`, and one deliberate mis-binding is shown to make the gate fail.

> **Handoff prompt — Unit 5B**
> Read project memory, then `direction_ph5_tableau_v1.0.md` and `direction_session_protocol_v1.2.md`.
> Execute **Unit 5B** only — the workbook skeleton and the three quantitative views (ranking,
> waterfall, channel decomposition) on Unit 5A's grains. You do not drive Tableau: write
> `era_ph5_build_5b_v1.0.md` as literal numbered UI steps for Brad, with a calculated-field
> appendix, then write `era_ph5_workbook_gate.py` to parse the saved `era_ph5_dashboard.twb` XML and
> assert field bindings, aggregations, filter scope and style tokens. `.twb`, never `.twbx`
> (Ruling P5-2). Prove the gate fails on a deliberate mis-binding. End with the closeout block per
> the session protocol, both halves.

---

## Unit 5C — the honesty layer: map, bands, brackets, caveats

**V4 — the map.** Eight points, colour by $ per IT-MWh on one ramp. It is orientation, not analysis;
it gets the least ink on the page and does not lead the dashboard.

**V5 — bands and brackets.** The ±25 % market bands on the three market-priced metros, and the two
published pairs (Chicago and Northern Virginia) drawn as intervals, not as two bars. **The one
adjacency the bands touch is annotated by name and by number**, from G4 rather than typed.

**V6 — the caveats sheet**, driven entirely by G4, sorted so unpriced items outrank stated
limitations. **Every row shows its scope, its dollars where they exist, and `priced` / `unpriced`.**
The FERC take-or-pay floor sits at the top with no dollar figure, which is the point.

**Checkpoint — 5C is complete when** V4–V6 exist in the saved `.twb`, the gate passes, V5's
annotation and every V6 row derive from G4 with **zero typed figures anywhere in the workbook**, and
the gate asserts that count is zero.

> **Handoff prompt — Unit 5C**
> Read project memory, then `direction_ph5_tableau_v1.0.md` and `direction_session_protocol_v1.2.md`.
> Execute **Unit 5C** only — the honesty layer: map, the ±25 % bands and the two published pairs as
> intervals, and the G4-driven caveats sheet. Same method as 5B: a literal build spec for Brad plus
> an extension to `era_ph5_workbook_gate.py`. The hard requirement is **zero typed figures anywhere
> in the workbook** — every number on screen resolves to a field — and the gate asserts it. End with
> the closeout block per the session protocol, both halves.

---

## Unit 5D — dashboard assembly, aesthetic conformance, publication

Assemble the six sheets into a primary dashboard plus the one-click caveats sheet (Ruling P5-3).
Filter and highlight actions defined once and gated. **Aesthetic conformance is checked by the gate
against `era_ph5_style_v1.0.md`, not by eye** — colours drawn only from the token list, one accent,
tints and shades only.

Publish to Tableau Public (Ruling P5-5). **The published `.twbx` is not committed; the `.twb` and
the extracts are.** Record the public URL in project memory and in the Phase 5 report.

**Checkpoint — 5D is complete when** the dashboard is assembled, the style gate passes with zero
off-token colours, the caveats sheet is reachable in one click, the Tableau Public link resolves and
has been opened and read, and the published figures have been spot-checked against
`era_ph4_report_v1.1.md`.

> **Handoff prompt — Unit 5D**
> Read project memory, then `direction_ph5_tableau_v1.0.md` and `direction_session_protocol_v1.2.md`.
> Execute **Unit 5D** only — dashboard assembly, aesthetic conformance and Tableau Public
> publication. The style gate must pass with zero off-token colours against `era_ph5_style_v1.0.md`;
> the caveats sheet must be one click from the primary dashboard (Ruling P5-3). Verify the published
> URL by fetching it — do not hand Brad an unverified link. End with the closeout block per the
> session protocol, both halves.

---

## Unit 5E — the Phase 5 report and the Phase 6 handoff

`era_ph5_report_v1.0.md`: what the dashboard shows, what it deliberately does not, the four grains
and their bases, the gate coverage, the public link, and the findings Phase 5 itself produced —
because building the views is a measurement of the data and this project has never had a unit that
found nothing.

**It also assembles the Phase 6 pre-flight queue**, which by then holds, in order:
Chicago's 5CP derivation (Ruling 17, first — the only carried ruling whose adoption is expected);
Northern Virginia's third ratchet construction (Ruling 16); the two-segment PUE form (Ruling 14, the
one that moves all eight metros); schema v1.5 whole — `node_class` plus `billing_determinant`
against F4M-14 (Ruling 11); Docket R; the read-log lines (Ruling 18); the library gaps F4D-8 and
F4M-13 (Rulings 19, 11); F4M-12; Atlanta's missing `voltage_level`; and the licensing review.

**Checkpoint — 5E is complete when** the report is published and gated by a script that re-derives
its figures, the Phase 6 queue is written, project memory carries the Phase 5 status block and the
public URL, and the `ph5-closed` tag is issued in the closeout.

> **Handoff prompt — Unit 5E**
> Read project memory, then `direction_ph5_tableau_v1.0.md`, `direction_ph4_close_v1.0.md` and
> `direction_session_protocol_v1.2.md`. Execute **Unit 5E** only — the Phase 5 report, gated by a
> script that re-derives its figures, plus the ordered Phase 6 pre-flight queue. Record the Tableau
> Public URL in the report and in project memory. End with the closeout block per the session
> protocol, both halves; part 1 includes the `ph5-closed` annotated tag.

---

## What Phase 5 does NOT do

- It does not reopen any figure. Every number it displays comes from Unit 4R's frozen extracts.
- It does not execute any carried ruling. Those are Phase 6, and Ruling 13 makes each of them an
  extract refresh rather than a workbook rebuild.
- It does not build the iOS thin client, the methodology one-pager, or the subdomain deployment.
  Those are spring, Phase 6 and Phase 6 respectively.
