# Direction — Phase 4 close: thirteen rulings, one re-issue, and the extract contract

`direction_ph4_close_v1.0.md` · 2026-08-28 · strategy ruling → Phase 4 close, Phase 5 open
Answers `brief_ph4_unit4m_open_v1.0.md` §7 (Q1–Q4) and disposes of **every** older open ruling:
`brief_ph4_unit4a_open_v1.0.md` §6 Q1/Q2, `brief_ph4_unit4b_open_v1.0.md` §6 Q1/Q2,
`brief_ph4_unit4c_open_v1.0.md` §7 Q1/Q2, `brief_ph4_unit4e_open_v1.0.md` §7 Q1/Q2/Q3.
**Ruling numbers continue the Phase 4 sequence in `direction_ph4_scenario_layer_v1.0.md` (1–7).**
Rulings 1–7 stand unchanged except where Ruling 14 amends Ruling 1's form.

**Phase 4 does not close on this file. It closes on Unit 4R** (§Unit 4R below), which is the single
re-issue that carries every ruled figure change at once. Phase 5 opens when 4R closes.

---

## 0 — The organising principle, stated before the rulings so they can be read against it

Eleven rulings were open. Ruling them all before Phase 5 is not the goal; **paying the re-issue once
is**, and those are different targets. The distinction that separates them is Ruling 13's:

- A **value** change moves numbers inside a fixed set of columns. Downstream it is an extract
  refresh. Cheap, and it stays cheap forever.
- A **shape** change adds, removes or re-grains a column. Downstream it is a workbook rebuild.
  Expensive, and it gets more expensive the later it lands.

So the test applied to each open ruling was not "is it ripe?" but **"can it still be executed as a
value change after Phase 5 is built?"** Everything that can is carried without cost. Everything
that cannot is either ruled now or given a column now so that it can be. That is why four rulings
execute in Unit 4R, three are carried on purpose, and one — Ruling 13 — exists only to make the
carrying safe.

---

## Ruling 8 — Columbus moves to the AEP ZONE. The construction is ratified project-wide. **AND IT REOPENS PHASE 2.**

**Unit 4M's Q1: YES.** Adopt **day-ahead / load ZONE / SIMPLE average** as the ratified construction
for all three market-priced metros. Unit 4M's §5 reasoning is accepted in full and not restated: a
load zone is where a retail load settles, a simple average is the right statistic for a flat 0.87-LF
load, day-ahead is what a full-requirements supplier hedges in, and PJM's day-ahead and real-time
simple averages sit within 1 % on both zones anyway.

**The change is one parameter on two rows.** AEP Ohio `DCT` and `DCT-T` together, per F2G-1:

```
0.04513  ->  0.04581  $/kWh        (AEP-DAYTON HUB DA PLMP 45.13  ->  AEP ZONE DA avg 45.81 $/MWh)
```

Priced by Unit 4M and **not to be re-derived**: **+$6,261,839.41/yr = +0.793350 $ per IT-MWh**,
metered pass-through exactly 1.000000, drift on the other seven metros exactly $0.00, order
unchanged.

**F4M-4 is the reason this is not a preference.** The AEP zone's real-time average and the
AEP-Dayton hub's day-ahead average are both $45.13 to the cent. A parameter that cannot be
distinguished by value from a different statistic at a different node is not a sourced parameter;
it is a sentence in a `source_note`. This ruling makes the sentence the same on all three metros.

### 8a — the consequence Unit 4M did not flag: this moves a PHASE 2 published figure too

Unit 4M's brief traces the change through `era_ph4_report_v1.0.md` only. It also lands on
`era_ph2_report_v1.1.md`, by exactly the mechanism Unit 2G's +7.21 landed there, and the pass-through
Unit 4M measured at 1.000000 is what makes it certain:

- **Columbus metered 58.54 -> 59.22 $/MWh** (+0.68, the market delta passed through unchanged).
- **The ±25 % band moves and widens**: it is 25 % of the market parameter, so 11.2825 -> 11.4525.
- **The published band-crossing caveat changes size.** 2F-b published "Columbus's upper band edge
  crosses Chicago's central by 0.12 $/MWh". Under this ruling that crossing is roughly **eight times
  larger**. The unit derives the figure; the strategy chat is ruling only that the sentence cannot
  stand as written.
- **The k = 2.31 common-multiplier crossing moves** and must be re-derived.
- Chicago's band is unchanged (its parameter is ComEd's 36.64), so 2F-b's "Columbus/Chicago is the
  ONLY adjacency the bands touch" **must be re-checked and is expected to hold** — Chicago's upper
  edge 78.85 against Austin's 79.21 does not move.

**Phase 2 is therefore REOPENED by numbered ruling, for this figure and no other**, exactly as its
closure terms provide. `era_ph2_report_v1.2.md` and `era_ph2fb_published_v1.1.csv` are issued **in
the same commit** as the Phase 4 re-issue. A Phase 4 report whose Columbus figure disagrees with the
Phase 2 report's Columbus figure is worse than either error alone.

### 8b — what the re-issue must also correct

**F4E-2 is wrong under this reading and the correction is larger than the brief asked for.** Unit 4M
established that Columbus/Chicago at 7.9209 displaces Chicago/Austin's 8.0786 as the tightest
mitigated adjacency. Deriving the other two stages from Unit 4M's own anchors shows more than that:
**Columbus/Chicago becomes the tightest adjacency at ALL THREE stages**, displacing a different pair
at each one — Austin/Northern Virginia on the baseline, Chicago/Austin after measures, Chicago/Austin
again after storage. The re-issue asserts this, it does not assume it; §7's whole adjacency table is
re-derived and gated.

---

## Ruling 9 — Dallas-Fort Worth's 34.59 STANDS, and its flagged substitution is RATIFIED, not carried

**Unit 4M's Q2: YES, unchanged.** Do **not** re-target to 35.34. Re-targeting costs +0.885680 $ per
IT-MWh and breaks the parity Ruling 8 creates, which is the wrong trade in both directions at once.

Ruling 8's construction is a **load zone**, so Ruling 1's specification of the ERCOT North *hub*
is superseded and Unit 1C's substitution becomes the ruled rule. **DFW's `SUBSTITUTION FLAGGED`
residual is DISCHARGED** — closed, not carried. That is the second flag this ruling closes and it
was not free: it is the reason Ruling 8's construction is worth adopting even though it costs
Columbus $6.3 M.

**The `source_note` on both Oncor rows is corrected** to cite the 2025 ERCOT SOM Table 1 as the
corroborating annual source, to record 35.34 with its construction (annual, load-weighted,
real-time, North load zone), and to record **F4M-3's residual as a named limitation**: ERCOT North's
implied load-weighting premium is +0.198 % against a PJM minimum of +5.72 %, so either the monthly
report's annual figure is itself load-weighted — in which case parity with PJM's simple averages is
already broken inside DFW's own source — or ERCOT North's 2025 duration curve really was that flat.
**That residual is the reason DFW's number deserves less confidence than Columbus's or Chicago's,
and it belongs in the Phase 6 one-pager verbatim, not only in a `source_note`.**

---

## Ruling 10 — Phase 4 prices NEITHER PG&E instrument, and the unavailability is PUBLISHED as a result

**Unit 4M's Q3: DISCHARGED, and the discharge is ratified.** F4M-8 settles it on the tariff's own
arithmetic before value ever enters: the battery is 8.32 % of a 1,201,595.60 kW facility peak
against thresholds of 20 % (Option R) and 10 % (Option S), and Option S's smallest qualifying system
is 2.403× the entire 50 MW B-20 programme cap — unreachable by construction, and barred on day 1 at
a new location by sheet 21's own words.

**No figure in `era_ph4_report_v1.0.md` moves. Two SENTENCES in it are now false and must.** §4's
"PG&E's Option R and Option S rate cells are NOT in `era_rates.db` and remain a Brad-browser task
under Unit 4M" is stale on both clauses. It is replaced by the finding, with its numbers:

> The two PG&E storage electives are **unavailable to a load of this shape** — the modelled battery
> is 8.32 % of the facility peak against eligibility floors of 20 % and 10 %, and Option S's
> smallest qualifying system exceeds the whole programme cap. Priced anyway, both are large net
> losses: **Option R +$91,828,409/yr (+11.6343 $ per IT-MWh), Option S +$103,339,369 (+13.0927)**,
> and for both the dominant term is the shared energy uplift, not the demand structure.

**That is a stronger result than a saving and it is to be published as one, in the report body, not
in a caveat list.** The siting tool's job is to say what a site costs and why; "the advertised
storage tariff does not reach a load this size" is a siting finding.

**F4M-11 rides with it**: `direction_ph4_scenario_layer_v1.0.md`'s "Option R is solar-specific — do
not use" was true of an older tariff book (AL 6676-E applicability against AL 7846-E rates) and is
**withdrawn**. The measures list in [[siting-tool-architecture]] carries the correction.

---

## Ruling 11 — F4M-12, F4M-13 and F4M-14 into the Phase 6 pre-flight with Docket R. Schema v1.5 stays WHOLE.

**Unit 4M's Q4: as defaulted, with one part overruled.**

- **F4M-12** (B-20-T's Jun–Sep TOU summer against May–Oct/Nov–Apr `flat_demand`, $0.00 today) —
  Phase 6 pre-flight, as a **latent** defect with its waking condition recorded: a seasonal flat
  demand rate.
- **F4M-13** (Peak Day Pricing absent from the library, $32.48/kW-yr of credit against event
  exposure) — Phase 6 pre-flight, and it joins F4D-8's family with a distinguishing note: **it is
  the only elective in the library that is a RISK TRADE and could go the wrong way.** An
  uncurtailable load takes $0.90/kWh on every event hour.
- **F4M-14** (schema v1.4 cannot express a per-DAY maximum or a monthly maximum over an EXCLUDED
  window) — Phase 6 pre-flight, **explicitly as v1.5 design scope**, and it is now the senior of the
  two v1.5 candidates.

**OVERRULED: `node_class` does NOT ship in Unit 4R.** Unit 4M's §6 recommends it land in the same
commit as the node ruling. Declining that, for three reasons and against the project's own
precedent:

1. **2C-c's rule cuts the other way here.** A half-migrated schema is worse than an untouched one,
   and shipping one of two ratified-together v1.5 candidates *is* a half migration — it forces a
   v1.6 for the second, three weeks later, inside the same docket.
2. **F4M-14 reorders the candidates.** A v1.5 built around `node_class` alone is a v1.5 that still
   cannot hold the tariff Unit 4M just read. The columns should be designed together against both
   problems, and the second problem is the harder one.
3. **Unit 4R's job is to move a value, and a migration doubles its blast radius** immediately before
   the Phase 5 extract is frozen. The coupling this project has avoided everywhere else should not
   be introduced in the one unit that touches two published reports at once.

**What replaces it costs nothing, because Unit 4M already built it.** The node class is recorded in
the `source_note` — as it is today — and **M1f and M1h are the gate**: M1f proves the node asymmetry
from the database, M1h derives the market-priced rate-id set from the database exhaustively. Unit 4M
proved the column "would make the check cheaper, not possible" and then wrote the cheap check
anyway. Ruling 13 adds the extract column that carries the class downstream. **The migration lands
in Phase 6, populated with Ruling 8's value, with `billing_determinant` designed in the same pass.**

---

## Ruling 12 — F4B-3 is CLOSED as a declared determinant, not carried as a defect

**Unit 4B's Q2, measured at exactly $0.00 four times now** (F4C-6, F4D-4, 4E's E6g, and again in
Unit 4M's run). DCT-T's 85 % capacity floor is 1,040,584 kW against a lowest monthly 30-minute peak
of 1,140,126 kW — **99,542 kW of headroom**, and the floor is anchored on a contract, so shaving the
peak does not move it.

**Ruled: DCT-T's absence of a non-rider demand row is a DECLARED DETERMINANT of that schedule, not
an engine defect.** The question is closed. The narrow fix Unit 4B described — falling back to the
determinant the schedule's kW riders bill on — is **contingent scope**: it enters Phase 6 only if a
second schedule with no non-rider demand row enters the library, or if the headroom gate ever fails.
**Unit 4R adds that gate**: an assertion that the floor is non-binding, with the headroom as its
stated quantity, so the closure is enforced in code rather than remembered. Four measurements of
$0.00 earn a closure; they do not earn silence.

---

## Ruling 13 — THE EXTRACT IS A CONTRACT. Unit 4R freezes its shape and adds the columns the open rulings will need.

**This is the ruling that makes Rulings 14, 16 and 17 safe to carry, and it is the direct answer to
the question that opened this session.** Rebuilding a Tableau workbook after the numbers move is
expensive only when the numbers move *shape*. A value refresh into a fixed column contract is a
file swap.

**Ruled:**

1. **`era_ph4e_published_v1.1.csv` is the frozen Phase 5 metro-grain contract.** Its column set does
   not change again inside Phase 5. Unit 5A may add GRAINS (§Phase 5) but may not re-shape this one.
2. **Every open ruling must be expressible as a VALUE inside that contract.** Unit 4R adds the
   columns that make this true, and they are the whole list:
   - `market_node_class` — `zone` or `hub`, per Ruling 8; carries F4M-4's distinction downstream
     without waiting for the schema migration.
   - `market_construction` — e.g. `da_zone_simple`; the sentence, as a field.
   - `pue_form` — `linear_4a` today, `two_segment_ph6` after Ruling 14 executes. **A refresh, not a
     rebuild.**
   - `pue_alpha_domain_max` — 4.7405, per Ruling 15.
   - `open_ruling_ids` — a delimited list of the rulings still capable of moving that metro's row.
     Empty on five metros, populated on Chicago and Northern Virginia.
3. **Any future unit that needs a column this contract does not have raises it as a ruling before
   Phase 5 builds, not after.** After 5D publishes, a shape change costs a workbook.

The cost of this ruling is five literal columns in one unit. The cost of not making it is discovering
in Phase 6 that ruling F4C-7 means rebuilding a published dashboard.

---

## Ruling 14 — 4A's Q1 is ADOPTED IN PRINCIPLE and EXECUTED IN PHASE 6. The bias is published now, with its sign and its bound.

**Unit 4A's §6 Q1: the two-segment form is correct and Ruling 1's single chord is not.** Above the
25.556 °C design wet bulb the economiser is fully out, so the only remaining channel is the
chiller's own 1.5 %/°F — a marginal slope of 0.00198 PUE/°C against the chord's 0.00471. Continuing
the chord past the design point extrapolates a mechanism that has stopped operating. **Ruling 1 is
amended in principle: the overlay above the knee is a chord to the design point and the marginal
slope beyond it.**

**It does NOT execute before Phase 5, and the reason is not squeamishness — it is that this is the
only open ruling that moves all eight metros.** Executing it rebuilds the facility profiles and
re-runs the entire 4A–4E chain, which is a phase-scale unit and not a pre-flight. Under Ruling 13 it
is a value refresh into a frozen contract, and `pue_form` is the column that records which form
produced any given row.

**What is published in the meantime is the bias itself, with a sign and a bound**, in
`era_ph4_report_v1.1.md` §8 and in the Phase 6 one-pager:

> The PUE overlay's single linear segment above the knee **overstates** PUE at the hottest
> intervals — by up to **0.0184 at Phoenix's maximum wet bulb, 0.0171 at Austin, 0.0122 at
> Dallas-Fort Worth**. That interval sets the demand charge in five of the eight metros. Every
> figure in this report is therefore an **upper** bound in that channel. The corrected two-segment
> form is ruled and scheduled (Ruling 14); it moves all eight metros in the same direction and
> cannot change the order.

**A bounded, signed, published bias is a stronger position than an open ruling**, and it is the same
move the project made on alpha in Ruling 1 and on every bracket since.

---

## Ruling 15 — 4A's Q2: the tighter alpha bound is STATED in the Phase 4 record, not left in code

**Unit 4A's §6 Q2: yes.** Unit 2F published its elasticity domain as alpha ≤ 4.947 at its own
reporting level of 1.20; at the ruled L = 1.150 the same construction gives **4.7405**, and Unit 4A
already enforces the tighter bound. A published number that has been silently narrowed is a defect
of the record, not of the code. **`era_ph4_report_v1.1.md` states both values, says which is
operative and why, and carries the re-derivation assertion (4A's G2a, which reproduces 2F's 4.947 at
2F's own level).** The extract carries it as `pue_alpha_domain_max` per Ruling 13.

---

## Ruling 16 — 4B's Q1 is CARRIED, and it is carried SHARPER: both ends of the bracket may be wrong

**Unit 4B's §6 Q1 (F4B-2, Dominion GS-4's ratchet, Northern Virginia's pair 97.7689 / 98.5005).
Not ruled. The pair stands as published.** The reason is not that it is hard to decide; it is that
**the strategy chat does not believe either priced end is the tariff's answer.**

The tariff puts one 100 % twelve-month ratchet on one Distribution Demand charge billed under II.A.2.
The database folds that single charge into **two** TOU demand rows. The two priced ends are therefore
"the floor reaches both folded rows" (+$7,901,881, which applies one ratchet twice and which Unit 4B
itself called an upper bound) and "the floor reaches neither" (the current reading). **The tariff's
own reading is a third construction nobody has priced: the ratchet applied ONCE to the combined
distribution demand.** It is expected to sit between the two ends, and until it is measured, ruling
between the existing two is choosing between two known misreadings.

**Routed to the Phase 6 pre-flight as a priced question, not a decision**: price the third
construction, then rule. Bounded at 1.0011 $ per IT-MWh, cannot move the order (Northern Virginia's
neighbours are 12.7 and 16.0 away), and under Ruling 13 it is a value refresh whenever it lands.
`open_ruling_ids` carries `F4B-2` on the Northern Virginia row.

---

## Ruling 17 — 4C's Q1 is CARRIED. Chicago publishes as a pair. Adopting the tariff determinants is a UNIT, not an edit.

**Unit 4C's §7 Q1 (F4C-7, ComEd Rate BESH's determinants, Chicago's pair 74.9520 / 73.6457). Not
ruled, and the reason is precise: the tariff reading is probably right and cannot be adopted
cheaply.** The three rate rows carry `determinant_is_assumption = 1`, which is a debt flag, and
F4D's rule is that a flagged estimate comes due. But adopting the reading means **ratifying a
five-hour coincident-peak expected value**, on exactly the footing Unit 4B ratified the ERCOT 4CP
one — an expected determinant with a p05–p95 band derived from a real calendar, not a declared
window carried forward. Standing caveat 2 of the Phase 4 report says so in the report's own words:
Chicago's PJM coincident-peak window is **DECLARED and UNRATIFIED**.

**A parameter derivation is a work unit.** Folding one into the re-issue would put an underived
parameter inside a gated publication, which is the one thing this project's gate discipline exists
to prevent.

**Scheduled as the first Phase 6 pre-flight unit, ahead of Docket R**, because it is the only carried
ruling whose adoption is *expected* rather than merely possible. Under Ruling 13 it is a value
refresh; the extract already carries both ends in `bracket_reading`, `mitigated_alt_usd_per_it_mwh`
and `mitigated_alt_annual_usd`, so **Phase 5 can display the bracket honestly today and collapse it
to a single number later without touching the workbook.** `open_ruling_ids` carries `F4C-7` on the
Chicago row.

**One consequence Unit 4R must gate now**, because it is cheap now and expensive later: under
Ruling 8 *and* Chicago's alternative end together, Columbus/Chicago closes to roughly **6.61 $ per
IT-MWh**. C13's margin (largest single storage saving 1.3825) still holds at both ends of both
brackets, but **the re-issue asserts it at the ends, not only at the schema reading** — that is
F4E-5's lesson applied one level up.

---

## Ruling 18 — 4E's Q1: the two read-log lines are corrected in the Phase 6 pre-flight, as defaulted

`era_tariff_read_log_v1.3.md` lines **512 and 1018** carry the false claim F4E-6 corrected in
`era_ph4b_scenario.py`'s `MEASURES` literal. No figure moves. A Phase 6 pre-flight unit corrects both
lines and **updates 4E's E9b declared set in the same commit**. Editing a Phase 2 read record is
a records change and gets its own unit, which is the call Unit 4E made when it routed rather than
edited, and it was right.

## Ruling 19 — 4E's Q3: F4D-8's Atlanta/Phoenix library gap is CARRIED as a stated limitation

It cannot move the order — Phoenix's neighbours are 24.94 and 18.52 $ per IT-MWh away, Atlanta's
18.52 and 37.68 — and closing it means reading two more tariff books with the thoroughness ComEd's
and Dominion's got. **Phase 6 scope, stated in the report and in the one-pager as a statement about
this project's reading and not about those tariffs.** F4M-13 joins the same family with its own
distinguishing note (Ruling 11).

## Ruling 20 — PHASE 4 CLOSES ON UNIT 4R, with two pairs published and one collapsed

**Unit 4E's Q2, answered.** Phase 4 closes when `era_ph4_report_v1.1.md`, `era_ph2_report_v1.2.md`
and their two extracts are published and gated. At close:

| metro | disposition | why |
| --- | --- | --- |
| **Columbus** | **single number, moved** | Ruling 8 |
| **Chicago** | **pair** | Ruling 17 — the ratification is a unit |
| **Northern Virginia** | **pair** | Ruling 16 — both priced ends may be wrong |
| the other five | single number | nothing open on them |

Tag `ph4-closed` is issued in Unit 4R's closeout.

---

# Unit 4R — the single re-issue. ONE CHAT. It is the last Phase 4 unit and it blocks Phase 5.

**Read first:** project memory (especially [[phase4-unit4e]], [[phase4-unit4m]], [[session-tiers]]),
this file, `direction_ph4_scenario_layer_v1.0.md`, `direction_session_protocol_v1.2.md`.
**Do not re-derive anything in [[phase4-unit4m]].** 4M is read-only on six objects and every figure
it measured is an input here, not a question.

## Scope — six things, in this order

1. **The database edit.** `era_rates.db`: AEP Ohio `DCT` and `DCT-T` market price
   `0.04513 -> 0.04581 $/kWh`, **both rows, one migration**, per F2G-1 and Ruling 8. Corrected
   `source_note` on both, naming the AEP zone, the table, the construction and the SOM page.
   Corrected `source_note` on both Oncor rows per Ruling 9. **NEVER run SQLite writes against the
   mounted folder** — see [[env-sqlite-on-mount]]: write on local disk, copy back, truncate the
   stale journal first. Record the database md5 before and after and `pragma integrity_check` after.
   **No schema change. `user_version` stays 14** (Ruling 11).
2. **Re-run the chain, unmodified.** `era_ph4e_publish.py`'s 67 gates plus the F1 gate first with no
   override; 4B's 80 gates; 4M's 46. `era_ph4b_scenario.py` is PINNED BY CONTENT HASH at E9c — if
   nothing in 4B changes, the hash does not change, and if it does the hash moves in the same
   commit.
3. **Re-issue `era_ph4_report_v1.1.md`**, superseding v1.0 (reports are superseded, not amended;
   v1.0 is left untouched). Required corrections, each gated:
   - Columbus's row and every total, portfolio figure and percentage it feeds.
   - **§1 and §7: the tightest-adjacency claim, at all three stages** (Ruling 8b). The whole
     adjacency table is re-derived.
   - **§7: C13's margin asserted at the ENDS of both brackets, not only at the schema reading**
     (Ruling 17).
   - **§4: the PG&E paragraph replaced by Ruling 10's finding, with both figures.**
   - **§5: unchanged in structure** — Chicago and Northern Virginia still publish as pairs
     (Rulings 16, 17); Columbus's "needs no pair" paragraph gains Ruling 12's gate.
   - **§8: caveat 3 rewritten.** "Four rulings are open and two of them move figures published
     here" is false after this file. It becomes: **two** rulings are open on published figures
     (F4C-7 Chicago, F4B-2 Northern Virginia), one is adopted and scheduled (Ruling 14), and two
     are discharged (F4C-8 on eligibility, F4B-3 on measurement).
   - **§8: two new caveats** — Ruling 14's signed and bounded PUE bias, and Ruling 15's 4.7405.
4. **Issue `era_ph2_report_v1.2.md`** (Ruling 8a), superseding v1.1: Columbus 58.54 -> 59.22, the
   band, the band-crossing sentence, the k-crossing figure, and a re-check that Columbus/Chicago is
   still the only adjacency the bands touch. **Gated by a script that re-derives them**, per 2F-b.
5. **Write the two extracts**: `era_ph4e_published_v1.1.csv` and `era_ph2fb_published_v1.1.csv`.
   `era_ph4e_stack.csv` is regenerated. **Add exactly the five columns in Ruling 13 §2 and no
   others.** This freezes the Phase 5 contract.
6. **Add the two gates this file creates**: Ruling 12's DCT-T headroom assertion, and an assertion
   that the two reports' Columbus figures are consistent with each other through the measured
   pass-through of 1.000000.

## Out of scope — say so in the brief rather than doing it

Schema v1.5 in any form. The two-segment PUE form. Chicago's 5CP derivation. Northern Virginia's
third ratchet construction. The read-log lines. Atlanta's and Phoenix's library gap. PDP. Any
Tableau work.

## Required reconciliations — write these down BEFORE the run, and mark the weak ones weak

Unit 4M measured the first four. They are inputs. If the chain does not reproduce them the chain is
wrong, not Unit 4M.

| | expected | basis |
| --- | --- | --- |
| Columbus baseline $ per IT-MWh | 68.4657 -> **69.2590** | 4M, measured |
| Columbus mitigated $ per IT-MWh | 66.2377 -> **67.0311** | 4M, measured |
| Columbus annual delta | **+$6,261,839.41** on baseline AND on mitigated | 4M, measured |
| drift, other seven metros | exactly **$0.00** | 4M, measured |
| Columbus/Chicago, + measures and storage | **7.9209** | 4M M5g, measured |
| Columbus/Chicago, baseline | ~12.28, and the tightest baseline adjacency | derived here — **verify, do not assume** |
| Columbus/Chicago, + measures | ~8.10, and the tightest at that stage | derived here — **verify, do not assume** |
| Columbus metered | 58.54 -> **59.22** $/MWh | derived here — **verify** |
| band-crossing against Chicago's central | ~0.12 -> **~0.98** $/MWh | derived here — **weak, verify** |
| order, at every stage and both bracket ends | **unchanged** | 4M, measured |

## Checkpoint — Unit 4R is complete when

- Both reports published and gated, both extracts written, `era_rates.db` edited by migration with
  md5 recorded before and after and `integrity_check` = `ok`.
- **Every gate in 4B, 4E and 4M passes unchanged**, plus the two new ones.
- A tamper case exists for the node change itself: bend one of the two AEP rows and require the
  gate that catches a half-applied F2G-1 correction to fire, **and nothing else**. Unit 4M's W15 is
  the template and M1h is the gate.
- The two reports agree on Columbus.
- `open_ruling_ids` is empty on six metros and carries `F4C-7` and `F4B-2` on Chicago and Northern
  Virginia respectively.

## Pre-written handoff prompt for Unit 4R

> Read project memory, then `direction_ph4_close_v1.0.md`, `direction_ph4_scenario_layer_v1.0.md`
> and `direction_session_protocol_v1.2.md`. Execute **Unit 4R** only — the single Phase 4 re-issue.
> Ruling 8 moves AEP Ohio's market price 0.04513 -> 0.04581 $/kWh on BOTH the DCT and DCT-T rows;
> everything else follows from it. Do not re-derive anything in [[phase4-unit4m]] — its measured
> figures are inputs, and the required reconciliations are tabulated in §Unit 4R. Two reports are
> re-issued in one commit (`era_ph4_report_v1.1.md` and `era_ph2_report_v1.2.md`, Phase 2 reopened
> by Ruling 8a) plus two extracts, and Ruling 13's five new extract columns FREEZE the Phase 5
> contract — add exactly those five. No schema change: `user_version` stays 14. Never run SQLite
> writes against the mounted folder. End with the closeout block per the session protocol, both
> halves; part 1 includes the `ph4-closed` annotated tag.

---

## Disposition of all eleven open rulings — the whole board, in one table

| ruling | source | disposition | moves a published figure? | when |
| --- | --- | --- | --- | --- |
| Columbus HUB -> ZONE | 4M Q1 | **RULED YES** (R8) | **yes, in BOTH reports** | Unit 4R |
| DFW's 34.59 | 4M Q2 | **RULED: STANDS**, flag discharged (R9) | no; `source_note` only | Unit 4R |
| PG&E instrument | 4M Q3 | **DISCHARGED**, published as a result (R10) | no; two sentences | Unit 4R |
| F4M-12/13/14 | 4M Q4 | **ROUTED** to Phase 6 pre-flight (R11) | no | Phase 6 |
| schema v1.5 `node_class` | 4M §6 | **OVERRULED — ships whole, in Phase 6** (R11) | no | Phase 6 |
| DCT-T's inert ratchet | 4B Q2 | **CLOSED** as a declared determinant + gate (R12) | no | Unit 4R |
| PUE form above design wet bulb | 4A Q1 | **ADOPTED IN PRINCIPLE**, bias published (R14) | later, all eight | Phase 6 |
| alpha domain 4.947 -> 4.7405 | 4A Q2 | **RULED: state it** (R15) | narrows a published bound | Unit 4R |
| GS-4's ratchet, NoVA's pair | 4B Q1 | **CARRIED, sharpened — a THIRD reading** (R16) | pair stands | Phase 6 |
| BESH determinants, Chicago's pair | 4C Q1 | **CARRIED — 5CP is a unit** (R17) | pair stands | Phase 6, first |
| read-log lines 512 / 1018 | 4E Q1 | **RULED: Phase 6 pre-flight** (R18) | no | Phase 6 |
| Atlanta/Phoenix library gap | 4E Q3 | **CARRIED** as a stated limitation (R19) | no | Phase 6 |
| does Phase 4 close on the pairs | 4E Q2 | **RULED: closes on 4R** (R20) | — | Unit 4R |

**Four execute in Unit 4R. Three are carried on purpose. Ruling 13 is why carrying them is free.**

## What this file deliberately does NOT do

- It does not rule F4C-7 or F4B-2 on the evidence available. Ruling between two constructions when
  a third is unpriced is not a ruling, it is a coin toss with a citation.
- It does not execute anything. The strategy chat issues direction files, not code.
- It does not reopen Phase 2 for anything but Columbus's market parameter.
