# Phase 5 report — the siting answer, drawn once, in one file that gates itself

`era_ph5_report_v1.0.md` · Unit 5H-5 of `direction_ph5_html_v1.0.md` · gated by `era_ph5_report_gate.py`

**Phase 5 closes on this document.** It publishes no new figure. Every number below is re-derived from
the four extract grains Unit 5A froze and Unit 4R contracted, by a script that regenerates each table
in this file from those CSVs and compares byte for byte, and that requires every figure in the prose
to carry a credit resolving to a cell, a named derivation, or a fact about a file on disk. **The
report and its verifier fail together.**

Basis, stated once: the published facility basis `plant_derived_4a`, L = 1.150<!--G:G1:Austin:pue_level_L-->, alpha 2.8311<!--G:G1:Austin:pue_alpha-->, variant `lf090`. `era_rates.db` at 1c72e7a1b32c99a650d2e1fba17ae21e<!--F:era_rates.db:md5-->, `user_version` fourteen; nothing in Phase 5 wrote it.

---

## 1 — What the page is

`era_ph5_dashboard.html`: **one self-contained file**, 193,712<!--F:era_ph5_dashboard.html:bytes--> bytes across 848<!--F:era_ph5_dashboard.html:lines--> lines, md5 2f7b7a750dd6b121841e5a68589cb1f0<!--F:era_ph5_dashboard.html:md5-->. It opens from disk, from an
email attachment and from any static host, identically. It contains no script source, no stylesheet
link, no font import and no URL a browser would fetch. Python's standard library writes every mark as
inline SVG, so what a browser paints is what the build wrote — which is the whole reason an automated
gate can read the artefact instead of a specification that drives someone else's runtime.

Two controls: the metro selector, saved on Columbus, and the basis swap, saved on the siting metric.
Both are pre-rendered into the markup, so **the page shows its saved state with JavaScript disabled**;
the script toggles visibility and computes nothing.

Six views are drawn, and the page is built by `era_ph5_build_html.py` (1981d0bbeb80c1fe2cfb83b5d7f13fd1<!--F:era_ph5_build_html.py:md5-->) from `era_ph5_views.py` (642523c11cb345ddd380162416a11abf<!--F:era_ph5_views.py:md5-->). Six renders at twice scale are committed under `renders/` as portfolio artefacts. **They are pixel-stable and not byte-stable across a device commit, so no md5 is claimed for them.**

## 2 — What the page shows

**The ranking, and the answer to the question the tool exists to ask.** A giga-scale campus taking 7,892,912.46<!--G:G1:Austin:it_annual_mwh--> IT-MWh a year costs between 47.67<!--D:spread_low_it--> and 180.96<!--D:spread_high_it--> dollars per IT-MWh depending only on where it is put — **a factor of 3.80<!--D:spread_ratio_it-->**. Across all 8<!--D:metro_count--> metros, that is 63,143,299.69<!--D:portfolio_it_mwh--> IT-MWh, a baseline of $6.694<!--D:portfolio_baseline_usd_b--> B a year and a mitigated total of $6.419<!--D:portfolio_mitigated_usd_b--> B. **The entire mitigation stack — every tariff elective in the library, plus a battery, in every metro — is worth 4.11<!--D:portfolio_mitigation_pct--> % of the bill**, or -274,917,226.17<!--D:portfolio_mitigation_usd--> dollars a year. Siting beats mitigating, and it is not close.

<!--ERA-BLOCK:ranking-->
| # | metro | utility | schedule | baseline $/yr | baseline $/IT-MWh | mitigated $/yr | mitigated $/IT-MWh | mitigated % |
| --: | --- | --- | --- | --: | --: | --: | --: | --: |
| 1 | Dallas-Fort Worth | Oncor Electric Delivery Company LLC | TRANS-SVC | 376,275,667.62 | 47.67 | 373,816,438.34 | 47.36 | 0.65 |
| 2 | Columbus | AEP Ohio (Ohio Power Co) | DCT-T | 546,655,609.92 | 69.26 | 529,071,129.42 | 67.03 | 3.22 |
| 3 | Chicago | Commonwealth Edison Co | BESH-HV | 643,584,518.09 | 81.54 | 591,589,837.26 | 74.95 | 8.08 |
| 4 | Austin | Austin Energy | COMM-PRI-20MW | 748,606,614.06 | 94.85 | 655,353,403.13 | 83.03 | 12.46 |
| 5 | Northern Virginia | Virginia Electric & Power Co | GS-4 | 848,998,135.27 | 107.56 | 771,681,508.12 | 97.77 | 9.11 |
| 6 | Phoenix | Arizona Public Service Co | E-35 | 975,288,132.77 | 123.57 | 969,298,141.82 | 122.81 | 0.61 |
| 7 | Atlanta | Georgia Power Co | PLL-18 | 1,126,412,681.66 | 142.71 | 1,115,500,906.22 | 141.33 | 0.97 |
| 8 | San Jose / Bay Area | Pacific Gas & Electric Co | B-20-T | 1,428,314,506.82 | 180.96 | 1,412,907,275.74 | 179.01 | 1.08 |
| | **portfolio** | | | **6,694,135,866.22** | | **6,419,218,640.05** | | **4.11** |
<!--/ERA-BLOCK:ranking-->

**The order does not move between bases.** Ranking the same eight metros on dollars per metered-MWh —
comparing tariffs rather than sites — gives the identical order, which is why the basis swap is offered
and why the siting metric is the default. The tightest adjacency in the table is 7.9209<!--D:tightest_gap_it--> dollars per IT-MWh, and it sits between the second and third metros: the top of the ranking is its narrowest part, and Section 3 says why that matters more than it looks.

**Where the mitigation actually comes from.** The five channels are reported separately because a
load-factor change moves a demand charge as well as an energy charge.

<!--ERA-BLOCK:channels-->
| metro | rider $/yr | energy $/yr | demand $/yr | fixed $/yr | statutory $/yr |
| --- | --: | --: | --: | --: | --: |
| Dallas-Fort Worth | -2,592,245.12 | 133,015.84 | 0.00 | 0.00 | 0.00 |
| Columbus | -34,873,657.87 | 49,545.32 | 0.00 | 0.00 | 17,239,632.05 |
| Chicago | -49,166,618.19 | 35,149.89 | -2,863,212.54 | 0.00 | 0.00 |
| Austin | 0.00 | -80,153,228.35 | -13,326,113.46 | 226,130.88 | 0.00 |
| Northern Virginia | -73,932,777.42 | 1,108.05 | -3,384,957.79 | 0.00 | 0.00 |
| Phoenix | -112,161.59 | 45,913.41 | -5,923,742.78 | 0.00 | 0.00 |
| Atlanta | 0.00 | -6,782,668.44 | -4,129,106.99 | 0.00 | 0.00 |
| San Jose / Bay Area | -6,422,042.34 | -879,916.55 | -8,105,272.19 | 0.00 | 0.00 |
| **portfolio** | **-167,099,502.51** | **-87,551,080.84** | **-37,732,405.75** | **226,130.88** | **17,239,632.05** |
<!--/ERA-BLOCK:channels-->

**The rider channel carries it**: -167,099,502.51<!--D:channel_rider_usd--> dollars against -87,551,080.84<!--D:channel_energy_usd--> of energy and -37,732,405.75<!--D:channel_demand_usd--> of demand — more than the two other real channels combined. The portfolio prices 6<!--D:measure_row_count--> tariff electives, worth -229,931,560.09<!--D:measures_total_usd--> dollars, and the battery adds -44,985,666.07<!--D:storage_total_usd-->. Austin is the most mitigable metro at 12.46<!--G:G1:Austin:mitigation_pct_of_baseline--> % of its own baseline; Phoenix is the least at 0.61<!--G:G1:Phoenix:mitigation_pct_of_baseline--> %.

**The walk from baseline to mitigated, per metro**, which is what the waterfall draws:

<!--ERA-BLOCK:stack-->
| metro | step | kind | component | $/yr | $/IT-MWh |
| --- | --: | --- | --- | --: | --: |
| Dallas-Fort Worth | 0 | baseline | TRANS-SVC | 376,275,667.62 | 47.67 |
| Dallas-Fort Worth | 1 | storage | B100-4H battery, CP4 dispatch | -2,459,229.28 | -0.31 |
| Dallas-Fort Worth | 2 | mitigated | mitigated total | 373,816,438.34 | 47.36 |
| Columbus | 0 | baseline | DCT-T | 546,655,609.92 | 69.26 |
| Columbus | 1 | measure | Ohio kWh excise self-assessment | -16,187,651.92 | -2.05 |
| Columbus | 2 | storage | B100-4H battery, FLAT dispatch | -1,396,828.58 | -0.18 |
| Columbus | 3 | mitigated | mitigated total | 529,071,129.42 | 67.03 |
| Chicago | 0 | baseline | BESH-HV | 643,584,518.09 | 81.54 |
| Chicago | 1 | measure | ComEd Rider EEPP opt-out | -44,307,832.56 | -5.61 |
| Chicago | 2 | measure | Illinois self-direct RPS | -4,872,023.08 | -0.62 |
| Chicago | 3 | storage | B100-4H battery, FLAT dispatch | -2,814,825.19 | -0.36 |
| Chicago | 4 | mitigated | mitigated total | 591,589,837.26 | 74.95 |
| Austin | 0 | baseline | COMM-PRI-20MW | 748,606,614.06 | 94.85 |
| Austin | 1 | measure | Austin Energy high load factor election | -87,252,874.77 | -11.05 |
| Austin | 2 | storage | B100-4H battery, FLAT dispatch | -6,000,336.17 | -0.76 |
| Austin | 3 | mitigated | mitigated total | 655,353,403.13 | 83.03 |
| Northern Virginia | 0 | baseline | GS-4 | 848,998,135.27 | 107.56 |
| Northern Virginia | 1 | measure | Dominion Rider RPS exemption | -70,889,135.43 | -8.98 |
| Northern Virginia | 2 | storage | B100-4H battery, FLAT dispatch | -6,427,491.72 | -0.81 |
| Northern Virginia | 3 | mitigated | mitigated total | 771,681,508.12 | 97.77 |
| Phoenix | 0 | baseline | E-35 | 975,288,132.77 | 123.57 |
| Phoenix | 1 | storage | B100-4H battery, FLAT dispatch | -5,989,990.96 | -0.76 |
| Phoenix | 2 | mitigated | mitigated total | 969,298,141.82 | 122.81 |
| Atlanta | 0 | baseline | PLL-18 | 1,126,412,681.66 | 142.71 |
| Atlanta | 1 | storage | B100-4H battery, FLAT dispatch | -10,911,775.43 | -1.38 |
| Atlanta | 2 | mitigated | mitigated total | 1,115,500,906.22 | 141.33 |
| San Jose / Bay Area | 0 | baseline | B-20-T | 1,428,314,506.82 | 180.96 |
| San Jose / Bay Area | 1 | measure | PG&E B-20 power factor adjustment | -6,422,042.34 | -0.81 |
| San Jose / Bay Area | 2 | storage | B100-4H battery, WIN53 dispatch | -8,985,188.74 | -1.14 |
| San Jose / Bay Area | 3 | mitigated | mitigated total | 1,412,907,275.74 | 179.01 |
<!--/ERA-BLOCK:stack-->

**The uncertainty, drawn at the same size as the answer.** 3<!--D:market_priced_count--> of the metros are market-priced and carry a plus-or-minus twenty-five per cent band on the market component; 2<!--D:bracket_count--> publish as a pair because a determinant reading is unruled. Five intervals in all, and they are the same five the page draws.

<!--ERA-BLOCK:bands-->
| metro | kind | low $/IT-MWh | central $/IT-MWh | high $/IT-MWh | what the interval is |
| --- | --- | --: | --: | --: | --- |
| Dallas-Fort Worth | band | 37.46 | 47.67 | 57.88 | +/-25 % of the market component |
| Columbus | band | 55.90 | 69.26 | 82.62 | +/-25 % of the market component |
| Chicago | band | 70.87 | 81.54 | 92.21 | +/-25 % of the market component |
| Chicago | published pair | 73.65 | | 74.95 | chicago_tariff, unruled (F4C-7) |
| Northern Virginia | published pair | 97.77 | | 98.50 | tou_reaches, unruled (F4B-2) |
<!--/ERA-BLOCK:bands-->

**The three cheapest metros are exactly the three banded ones.** Columbus's upper edge crosses
Chicago's central value, and that is the only adjacency the bands touch anywhere in the table. **The
size of the crossing depends on the basis and the page prints neither figure**: it is 0.80423602<!--D:band_crossing_facility--> dollars per metered-MWh on the published facility basis and 1.08102537<!--D:band_crossing_it--> on the siting metric the view is drawn on. Two cells, in no cell. The page draws the geometry and names the caveat; the gate re-derives the adjacency from the grain and asserts there is exactly one.

**Shape through the year**, because an annual figure hides the interval that sets the demand charge:

<!--ERA-BLOCK:monthly-->
| metro | peak kWh month | peak baseline $ month | peak billed kW month | ratchet months |
| --- | --: | --: | --: | --: |
| Dallas-Fort Worth | 7 | 7 | 6 | 0 |
| Columbus | 7 | 7 | 8 | 0 |
| Chicago | 7 | 5 | 8 | 0 |
| Austin | 7 | 7 | 6 | 0 |
| Northern Virginia | 7 | 7 | 8 | 11 |
| Phoenix | 7 | 7 | 8 | 0 |
| Atlanta | 7 | 7 | 7 | 0 |
| San Jose / Bay Area | 7 | 7 | 6 | 0 |
<!--/ERA-BLOCK:monthly-->

Energy peaks in July everywhere. The billed-demand month does not, and the dollar peak does not
either — Chicago's most expensive month is May. Northern Virginia is the only metro whose ratchet
binds at all, and it binds in 11<!--D:nova_ratchet_months--> months of the year, August excepted.

## 3 — What the page deliberately does not show

**The largest numbers in this project are not in any total, and that is a decision, not an omission.**

**The 3<!--D:excluded_count--> voltage siblings are priced and excluded.** The published baseline is already billed on
the higher-voltage schedule, so counting the move again would be double-counting.

<!--ERA-BLOCK:excluded-->
| metro | component | $/yr | $/IT-MWh |
| --- | --- | --: | --: |
| Dallas-Fort Worth | voltage sibling PRI-GT10KW-SUB -> TRANS-SVC | -35,652,792.35 | -4.52 |
| Columbus | voltage sibling DCT -> DCT-T | -184,527,629.75 | -23.38 |
| San Jose / Bay Area | voltage sibling B-20 -> B-20-T | -520,924,103.18 | -66.00 |
| **total** | **excluded from every mitigated figure** | **-741,104,525.28** | |
<!--/ERA-BLOCK:excluded-->

That band is -741,104,525.28<!--D:excluded_total_usd--> dollars a year — **2.70<!--D:excluded_over_mitigation--> times the entire real mitigation stack**. It is drawn as a muted band beside the walk, never as an absence, and every sibling is priced against an unpriced transfer of substation and interconnection capex onto the customer.

**The FERC take-or-pay floor carries no figure at all.** ComEd's OATT Attachment H-13 Transmission
Security Agreement is the single largest unpriced item in the project. It sits first in the caveats
table with both dollar columns empty, which is the point: a number would be a guess and an absence
would be a lie.

**Three headline totals that exist in no cell are not typed.** The frozen contract carries no
portfolio-total cell for the mitigation channels, so the channel view makes its claim by bar length
and prints no total. The excluded siblings have no position in the walk, so the band is anchored at
zero rather than given an invented one. The band crossing is on two bases and the view prints the two
endpoint cells and the drawing instead. **A figure whose basis the contract cannot express is a figure
this project does not publish** — three measured instances, and none of them is a rounding decision.

**And no site has been chosen anywhere.** The map draws weather stations, because the station is what
the PUE overlay is driven by. The columns are named so they cannot be read as a site.

## 4 — The four grains and their bases

Every figure on the page and in this report comes from four CSVs, frozen at their Unit 5A pins and
embedded in the page verbatim beside their manifest, so there is no second copy of the data to go
stale.

<!--ERA-BLOCK:grains-->
| grain | file | rows | columns | md5 | what it is |
| --- | --- | --: | --: | --- | --- |
| G1 | era_ph5_metro.csv | 8 | 73 | 84fe4dbff836a169ec29d9f38281b683 | one row per metro: the ranking, the bases, the bands, the brackets |
| G2 | era_ph5_stack.csv | 33 | 16 | 3e8825ac3755a67fdcd882c32ba6da2d | the mitigation walk, one row per component, excluded siblings included |
| G3 | era_ph5_month.csv | 384 | 24 | f5b3638a2f9cc942b8d6835014043048 | twelve months x four stages per metro, levels and deltas |
| G4 | era_ph5_caveat.csv | 21 | 12 | fc1fa4b10c5f536faeb5850647317db7 | the honesty layer: every caveat, priced or not |
| | `era_ph5_grains_manifest.json` | | | d28ed3404fab100d8bb31d0e0bc95323 | the pins every row above is read against |
<!--/ERA-BLOCK:grains-->

The siting metric is dollars per IT-MWh: sites are compared at equal IT capacity, and IT energy is
identical across metros by construction. Dollars per metered-MWh compares tariffs rather than sites
and is available as a swap, never as a default. In the monthly grain, `baseline` and `mitigated` are
levels while `measures` and `storage` are deltas, so summing all four stages double-counts. **One
declared allocation exists in the four grains and it is named in the caveats**: Ohio's annual kWh
self-assessment has no monthly form, so the monthly grain spreads it on each month's share of metered
energy. The annual total is exact; the split is declared.

The honesty layer is a table, not prose, because typed caveats drift from the report and a table the
gate reconciles cannot. It holds 21<!--D:caveat_count--> rows: 3<!--D:caveat_unpriced_count--> unpriced, 11<!--D:caveat_limitation_count--> stated limitations, and the rest priced, unavailable, open or discharged.

<!--ERA-BLOCK:caveats-->
| # | id | category | scope | priced | $/yr | $/IT-MWh | ruling |
| --: | --- | --- | --- | --: | --: | --: | --- |
| 1 | C-FERC-H13 | unpriced | Chicago | 0 |  |  | Dockets 25-0677/25-0679 |
| 2 | C-CAPEX | unpriced | Columbus;Dallas-Fort Worth;San Jose / Bay Area | 0 |  |  | - |
| 3 | C-RETAIL-PROXY | unpriced | all | 0 |  |  | direction_ph1_tariff_db_v1.0.md |
| 4 | C-VOLT-EXCL | excluded | Columbus;Dallas-Fort Worth;San Jose / Bay Area | 1 | -741,104,525.28 | -93.894937 | - |
| 5 | C-PGE-OPT-R | unavailable | San Jose / Bay Area | 1 | 91,828,409.00 | 11.634300 | Ruling 10 |
| 6 | C-PGE-OPT-S | unavailable | San Jose / Bay Area | 1 | 103,339,369.00 | 13.092700 | Ruling 10 |
| 7 | C-F4C-7 | open_ruling | Chicago | 1 | -7,934,035.00 |  | Ruling 17 |
| 8 | C-F4B-2 | open_ruling | Northern Virginia | 1 | 7,901,881.12 |  | Ruling 16 |
| 9 | C-CHI-5CP | limitation | Chicago | 0 |  |  | Ruling 17 |
| 10 | C-PUE-BIAS | limitation | all | 0 |  |  | Ruling 14 |
| 11 | C-ALPHA-DOMAIN | limitation | all | 0 |  |  | Ruling 15 |
| 12 | C-BAND-25 | limitation | Chicago;Columbus;Dallas-Fort Worth | 0 |  |  | F2Fb-2 / F2Fb-4 |
| 13 | C-F4D-8 | limitation | Atlanta;Phoenix | 0 |  |  | Ruling 19 |
| 14 | C-F4M-13 | limitation | San Jose / Bay Area | 0 |  |  | Ruling 11 |
| 15 | C-F4M-3 | limitation | Dallas-Fort Worth | 1 |  | 0.885680 | Ruling 9 |
| 16 | C-SJ-PF | limitation | San Jose / Bay Area | 1 | -6,422,042.34 | -0.813647 | F4D-6 |
| 17 | C-OHIO-EXCISE | limitation | Columbus | 1 | -16,187,651.92 | -2.050910 | F4D-1 |
| 18 | C-EXCISE-ALLOC | limitation | Columbus | 1 | 17,239,632.05 |  | Unit 5A |
| 19 | C-STATION-POINT | limitation | all | 0 |  |  | Unit 5A |
| 20 | C-F4C-8 | discharged | San Jose / Bay Area | 1 |  |  | Ruling 10 |
| 21 | C-F4B-3 | discharged | Columbus | 1 | 0.00 | 0.000000 | Ruling 12 |
<!--/ERA-BLOCK:caveats-->

## 5 — Gate coverage

`era_ph5_page_gate.py` (adfb41a9eacceff9cee1318c24ffa34a<!--F:era_ph5_page_gate.py:md5-->) is the only acceptance for the page. It parses the file as XML and asserts, group by group, that the page is a faithful, fresh, self-contained, on-token rendering of the four grains with every figure credited to a cell. **A gate that has nothing to quantify over is a declared skip with its reason, never a pass; a gate that cannot run because its view is unbuilt fails.** The live run of that gate is what produced this table.

<!--ERA-BLOCK:gatecoverage-->
| group | gates | duty |
| --- | --: | --- |
| D | 29 | the four grains, imported unchanged by this gate too |
| H | 7 | page hygiene, determinism, and the scratch-rebuild reproduction |
| H13 | 3 | freshness by construction: embedded manifest == disk == the CSVs |
| P | 7 | the two controls, read from the markup with script disabled |
| V | 15 | the six views, asserted against the DRAWING |
| B | 4 | basis: the siting metric, the metered swap, the band crossing |
| S | 8 | the thirteen tokens, five sizes, one family, the 8 px grid |
| T | 2 | typed figures: uncredited count zero, credited equal their cells |
| **total** | **75** | **all PASS, empty FAIL set, exit 0** |
<!--/ERA-BLOCK:gatecoverage-->

**The count of uncredited numeric text on the page is zero, and every credited element is compared
against the cell it cites on every run.** That is not a style rule. Four of the five gates one unit
turned live could have passed on markup that described itself correctly while drawing something else,
which is why every drawing rule added since asserts drawn coordinates — a rect's edge against a
label's position, a tick against its label, two bars' shared edge against the connector between them.

Positive controls are the other half. `era_ph5_page_tamper.py` (3924058d1293c10b0967b159df6f07de<!--F:era_ph5_page_tamper.py:md5-->) runs 29<!--D:tamper_case_count--> declared cases against an empty clean baseline, each with an absolute firing set fixed before the run, the first case leading and the control last. **A harness that has never fired is not evidence.**

<!--ERA-BLOCK:tampercoverage-->
| case | kind | gates it must fire |
| --- | --- | --- |
| W01 | page | H6, V1c |
| W02 | page | H6, V3b |
| W03 | page | H6, V2b, V2c |
| W04 | page | H6, V2c |
| W05 | page | H6, P6 |
| W06 | page | H6, V2c |
| W07 | page | H6, V4b |
| W08 | page | H6, V5b |
| W09 | page | B4, H6 |
| W10 | page | H6, V6b |
| W11 | page | H6, V6b |
| W12 | page | H6, T2, V6b |
| W13 | page | H6, V4b |
| W14 | page | H6, V4b |
| W15 | grain | D2a, D2b, D2c, D3a |
| W16 | grain | D5a, D6a |
| W17 | page | H6, V5b |
| W18 | page | H6, V3b |
| W19 | page | H6, V2b |
| W20 | page | H6, T2 |
| W21 | page | H6, V6c |
| W24 | grain | D11a, D11b, D11c |
| W30 | page | H13a, H6 |
| W31 | input | D11a, D11b, D11c, H13b, H13c, H6, T2, V4b, V5b |
| W32 | page | H6, T1 |
| W33 | page | H6, S1 |
| W34 | build | (nothing fires) |
| W35 | build | S1 |
| N01 | control | (nothing fires) |
| **29 cases** | | **all AS DECLARED, W01 first, N01 last** |
<!--/ERA-BLOCK:tampercoverage-->

This report is gated the same way, by `era_ph5_report_gate.py`: six groups — the four grains imported
unchanged, assembly, block re-derivation, credits, the queue, and the prohibitions. Every table above
is regenerated from the CSVs and compared byte for byte; every figure in the prose carries a credit
that resolves and is compared to the precision shown; and the sentences this report is forbidden to
contain are named in the gate rather than remembered by a session.

## 6 — The chain, as measured

Freshness is by construction rather than by discipline: `era_ph5_extract.py` writes the four CSVs and
the manifest, `era_ph5_build_html.py` writes the page from them, `era_ph5_page_gate.py` accepts it, and
the page embeds the grains so the gate can prove the embedded copy equals the CSVs on disk. The chain
was run end to end, in a full copy of the project and never on the project folder itself, because the
extract rewrites the manifest and the manifest is a pin. **What was measured:**

- the four grain CSVs, the data dictionary and the style tokens came back **byte-identical to their
  pins**;
- `era_ph5_grains_manifest.json` did **not**: it differs in five `written_utc` values, stamped from the
  wall clock, and in nothing else — every md5, row count, column count, byte count and database hash in
  it is identical;
- the rebuilt page is the same 193,712<!--F:era_ph5_dashboard.html:bytes--> bytes and the same 848<!--F:era_ph5_dashboard.html:lines--> lines as the committed page, differs on exactly one line — the embedded manifest — in ten substrings, all of them those timestamps, and is **identical after normalising that field**.

**The ruling's own words for this checkpoint were an identity its architecture forbids, and this report
does not repeat them.** The honest statement is the measured one above. Whether the checkpoint is
restated, or the timestamp is derived from content at the cost of editing the producer of a frozen
contract, is an open ruling question and it is in Section 10. Re-running the extract is not a
maintenance step anyone should take casually: it moves the manifest pin and forces a page rebuild for
no gain unless the underlying figures have actually changed.

## 7 — Why the renderer is ours: the Tableau record

Phase 5 began as a Tableau layer and left it. The record, in one paragraph, because it is the reason
the renderer is Python and the reason the deliverable is one file.

A unit was spent measuring whether the free Tableau edition could hold a workbook that stayed
current. It could not: the Public edition re-attaches its own temporary extract on every reopen, so a
workbook that gated clean would show stale data the next time it was opened by anyone who was not
watching for it. That measurement closed on a fail and the fail is the finding. The alternative
branch — a paid licence — bought a fix for a problem the project did not need to have. **Brad's
ruling was to leave Tableau behind**, and the strategy chat's first replacement default, a JavaScript
charting library, was withdrawn on a second measurement: neither the container nor the device shell
can reach a package registry or a CDN, so the runtime would have been a vendored blob a human
downloads by hand and the gate could read only the specification driving it, never the numbers on the
screen. **An SVG written by Python is the artefact.** It is XML the gate already parses, it prints and
exports to PDF at any scale, which an architecture portfolio needs, and it requires nothing
downloaded by anyone. The retired Tableau set is kept whole in version control and is never edited
again.

## 8 — Phase 5's own findings

Building the views is a measurement of the data, and this project has never had a unit that found
nothing. Thirty-nine findings across the six units of the HTML build, twelve in the extract unit that
preceded them, nine in the Tableau measurement. The ones that changed how the work is done:

- **A gate written before its artefact exists is a prediction about markup, and the first built
  instance is what measures it (F5H1-1).** The prediction is usually false-pass-shaped rather than
  fail-shaped: a gate asserting attributes the build writes about itself will pass on a page that does
  not do what the ruling says (F5H2-1). Of five gates one unit turned live, four failed that question
  (F5H3-4). Every gate added since asserts the drawing and the page's own stylesheet.
- **The reproduction gate is blind to the build (F5H4-6).** The page gate rebuilds the page from the
  same view code it is checking, so an edit to a view function reproduces itself exactly and the
  reproduction gate still passes. It catches a hand-edited page; nothing catches a changed build. That
  is precisely why six drawing defects survived four units unseen, and why the answer was seven gate
  clauses rather than seven prettier drawings. **It is the single sentence from Phase 5 most worth
  promoting to a standing rule.**
- **A comparison is only as strong as the string it normalises (F5H1-3).** The credited-figure gate
  stripped the typographic minus instead of translating it, so a positive cell displayed as a negative
  number normalised back to the cell and compared equal. The error that produced was measured against the tolerance in force before the repair, not argued: a silent pass on the negation of a figure. It now translates, and a positive control proves it.
- **The scope of a drawing finding is the rule it names, not the view it was seen in (F5H4-2).** A
  colour ramp defect was observed on the map and the ranking view ramped the same column with the same
  rule, ungated. Repairing one would have put two colour semantics for one column on one page.
- **Prefer the rule that removes the class of defect to the patch that removes the instance
  (F5H4-4).** Two separate label defects were one anchoring rule.
- **A ruled prose claim can become a gate (F5H3-5).** The caveat that says its adjacency is the only
  one the bands touch is now re-derived from the grain and asserted as a count.
- **A declared tamper set is never inherited (F5H1-2).** Every carried case is re-derived against the
  page as it then stands, with a written reason for changing or not changing.
- **A chain that is declared but never run is a prediction (F5H4-1).** Four times in Phase 5, running
  a written prediction found the gap.
- **A handoff premise can be stale in the safe direction too (F5H5-1, this unit).** Three consecutive
  units were told to record a checkpoint item as still open if the committed logs lacked the expected
  header. Three times the headers were there. **A conditional that has been false three times running
  is a convention to invert:** check the artefact, then record what was found.
- **A checkpoint clause can outlive the ruling that wrote it (F5H5-2, this unit).** The unit list
  inherited from the Tableau ruling asks this report for "the public link". Under the HTML ruling the
  deliverable is a file that opens from disk and the public URL is the second Phase 6 item, so there is
  no link. **The honest discharge is a stated absence, and the gate asserts this report contains no URL
  at all** rather than letting a plausible one be invented later.

## 9 — The Phase 6 pre-flight queue

The order below is the Unit 5E list as amended: **the licensing review moves to the front**, because
the repository is private through Phase 5 and nothing else can be published until it is settled, and
**the subdomain deployment of the page follows immediately**, because the deliverable is one static
file and the deployment is the only thing standing between it and a public portfolio piece. The
freshness gate that was conditional in earlier planning is **struck**: X13c was made unconditional by
the page's own construction and is not a queue item.

| item | what | ruling | carried finding |
| --- | --- | --- | --- |
| Q6-01 | Licensing review before any visibility change | P5-5 / H-4 | - |
| Q6-02 | Subdomain deployment of era_ph5_dashboard.html on bradmachado.com | H-4 | - |
| Q6-03 | Chicago's 5CP derivation, then rule the bracket | Ruling 17 | F4C-7 |
| Q6-04 | Northern Virginia's third ratchet construction, priced then ruled | Ruling 16 | F4B-2 |
| Q6-05 | The two-segment PUE form; it moves all eight metros | Ruling 14 | - |
| Q6-06 | Schema v1.5 whole: node_class plus billing_determinant | Ruling 11 | F4M-14 |
| Q6-07 | Docket R | Ruling 11 | - |
| Q6-08 | The two false lines in era_tariff_read_log_v1.3.md, with Unit 4E's declared set | Ruling 18 | - |
| Q6-09 | The Atlanta and Phoenix library gap | Ruling 19 | F4D-8 |
| Q6-10 | PG&E Peak Day Pricing, the one elective that is a risk trade | Ruling 11 | F4M-13 |
| Q6-11 | F4M-12's latent seasonal flat-demand defect | Ruling 11 | F4M-12 |
| Q6-12 | Atlanta's missing voltage_level | - | - |

12<!--D:queue_length--> items. **Under the extract contract every one of them that moves a value is a value refresh into a frozen column shape followed by one command**, which is what makes carrying them free rather than expensive. Two of them collapse a published pair; one moves all eight metros in the same direction and cannot change the order.

## 10 — Open ruling questions carried out of Phase 5

Separate from the queue above, because these are decisions for the strategy chat rather than units of
work, and because the queue this report assembles is the queue that was ruled.

- **F5H4-1 — the chain identity.** The freshness ruling declared that the extract-build-gate chain
  reproduces the committed page exactly. It cannot, and the obstacle is a wall-clock stamp rather than
  the data: the extract writes `written_utc` five times into the manifest and the page embeds the
  manifest so the freshness gate can compare them. Three resolutions are set out in the unit's results
  record — restate the checkpoint and gate the normalised comparison; derive the field from content and
  accept editing the producer of a frozen contract; or leave it recorded. The executing session's
  non-binding reading is the first, because a freshness guarantee that requires the clock to stand still
  is not the guarantee the ruling was written to give. **Unruled. This report states the measurement and
  not the ruling.**
- **Two candidate standing rules, no ruling requested.** That the reproduction gate is blind to the
  build (F5H4-6), and that a figure whose basis the contract cannot express is not typed — the latter
  now measured three separate times in three separate views.

---

**Phase 5 is closed.** The deliverable is `era_ph5_dashboard.html` and the six renders beside it; the
acceptance is `era_ph5_page_gate.py` and `era_ph5_page_tamper.py`; the record is `era_ph5_5h_results.md`,
which is append-only because it is the measurement.
