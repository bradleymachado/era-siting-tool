#!/usr/bin/env python3
"""era_ph5_views.py — Unit 5H-1 of direction_ph5_html_v1.0.md (Ruling H-1)

This section is intended to DRAW THE VIEWS as inline SVG written by the Python
standard library, one function per view, called by era_ph5_build_html.py. No
library, no download, no runtime: the marks the browser shows are the marks
this file wrote, which is why the page gate can read them (H-1, gate reads the
artefact).

5H-1 delivers V1 (the ranking) and V3 (the channel decomposition), both from
G1 (era_ph5_metro.csv). 5H-2 adds V2 (the waterfall) from G2
(era_ph5_stack.csv), eight pre-rendered metro states and the excluded band.
V4, V5, V6 stay build-incomplete slots.

Conventions this file honours (era_ph5_5h_results.md section 6, written by 5H-0):
  - a built view is <svg data-view="Vn" width height>, and its slot drops
    data-status="build-incomplete";
  - V1 bars carry data-role="bar" data-metro data-field; the two basis states
    are sibling <g data-state-basis="IT"|"Metered"> with data-axis-field, the
    Metered one hidden="hidden" data-remainder="0" and the text
    "baseline tariff rate only" (F5B-2);
  - V3 carries data-channel on exactly the five channel rows, in V3_ORDER;
  - every numeric <text> carries data-src="<grain-stem>:<row-key>:<column>"
    and shows the cell to the precision printed (row key for G1 is metro);
  - no hex colour and no font-size is written here: marks carry CSS classes
    defined in the build's <style> from the thirteen tokens (S1/S2/S3);
  - every <svg> width and height is a multiple of 8 (S5).

Sign convention: figures are printed with the ASCII hyphen-minus, never the
typographic minus. The gate strips U+2212 rather than translating it, so a
typographic minus would silently drop the sign (recorded, 5H-1).
"""

# V3's declared row order (F4E-3, most negative first). Kept here as the
# drawing order; era_ph5_grain_gate.V3_ORDER is the gate's copy and D8b is
# what proves the order is a fact about the data, not a preference.
V3_ORDER = ["mitigation_rider_usd", "mitigation_energy_channel_usd",
            "mitigation_demand_channel_usd", "mitigation_fixed_usd",
            "mitigation_statutory_usd"]
V3_LABELS = {
    "mitigation_rider_usd": "Rider",
    "mitigation_energy_channel_usd": "Energy",
    "mitigation_demand_channel_usd": "Demand",
    "mitigation_fixed_usd": "Fixed",
    "mitigation_statutory_usd": "Statutory",
}

RAMP_STEPS = 7          # accent-100 .. accent-700; style rule 2 caps a ramp at seven


def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            .replace('"', "&quot;"))


def num(x):
    return float(x)


def fmt2(v):
    """Two decimals, ASCII minus, comma groups. Correct rounding keeps
    |shown - cell| <= 0.005, which is exactly the page gate's T2 tolerance."""
    return "{:,.2f}".format(v)


def ordinal_ramp(values, n=RAMP_STEPS):
    """Unit 5H-4, F5H3-7. This section is intended to ASSIGN A RAMP STEP BY
    ORDINAL POSITION rather than by linear magnitude, and to return the whole
    value -> step map so a view assigns every mark from one derivation.

    The linear rule it replaces (int((v-lo)/(hi-lo)*n)) collapsed exactly where
    the ranking is least certain: over the eight measured usd_per_it_mwh values
    it used steps 0,1,1,2,3,3,4,6 - step 5 never appeared, Columbus and Chicago
    took one colour and Northern Virginia and Phoenix took another, so the map
    could not separate the three banded metros at the top of the ranking.

    The step is still a function of the value alone, and a monotone one: equal
    values take equal steps and a larger value never takes a smaller step.
    int(x + 0.5), NOT round(): round() is banker's rounding and this must give
    the same page on 3.10, 3.11 and 3.13 (F5H0-5).
    """
    order = sorted(set(values))
    N = len(order)
    if N == 0:
        return {}
    if N == 1:
        return {order[0]: 0}
    return {v: int(i * (n - 1) / (N - 1) + 0.5) for i, v in enumerate(order)}


def by_rank(G1):
    return sorted(G1, key=lambda r: int(r["rank"]))


# --------------------------------------------------------------------------
# V1 — the ranking
# --------------------------------------------------------------------------
V1_W = 1184
V1_TOP = 24
V1_ROW = 48
V1_BAR_H = 24
V1_BAR_X = 288
V1_BAR_MAX = 768
V1_VALUE_X = V1_BAR_X + V1_BAR_MAX + 16


def _v1_state(rows, field, basis, axis_field, hidden, parts):
    """One pre-rendered basis state. parts=True draws the stacked split
    (mitigated remainder + the mitigation drawn hollow); parts=False draws the
    single baseline bar the metered basis can express (F5B-2: there is no
    mitigated metered column, so the remainder is 0 and the label says so)."""
    vals = [num(r[field]) for r in rows]
    lo, hi = min(vals), max(vals)
    # 5H-4: the SAME ordinal ramp V4 uses. V1's IT state ramps the same column
    # with the same rule, so it carried the same collapse (F5H3-7); two colour
    # semantics for one column on one page is what this unit exists to remove.
    steps = ordinal_ramp(vals)
    scale = V1_BAR_MAX / hi
    out = ['<g data-state-basis="%s" data-axis-field="%s"%s%s>'
           % (basis, axis_field,
              ' data-remainder="0"' if not parts else "",
              ' hidden="hidden"' if hidden else "")]
    for i, r in enumerate(rows):
        metro = r["metro"]
        total = num(r[field])
        y = V1_TOP + i * V1_ROW + (V1_ROW - V1_BAR_H) // 2
        base = y + 17
        step = steps[total]
        out.append('<g data-role="bar" data-metro="%s" data-field="%s">' % (esc(metro), field))
        out.append('<title>%s</title>' % esc(metro))
        if parts:
            rem = num(r["mitigated_usd_per_it_mwh"])
            w_rem = int(round(rem * scale))
            w_tot = int(round(total * scale))
            out.append('<rect class="era-ramp-%d" data-part="mitigated" data-field="mitigated_usd_per_it_mwh" '
                       'x="%d" y="%d" width="%d" height="%d"/>'
                       % (step, V1_BAR_X, y, w_rem, V1_BAR_H))
            out.append('<rect class="era-mitigation" data-part="mitigation" '
                       'data-field="mitigation_usd_per_it_mwh" '
                       'x="%d" y="%d" width="%d" height="%d"/>'
                       % (V1_BAR_X + w_rem, y, max(w_tot - w_rem, 1), V1_BAR_H))
        else:
            out.append('<rect class="era-ramp-%d" x="%d" y="%d" width="%d" height="%d"/>'
                       % (step, V1_BAR_X, y, int(round(total * scale)), V1_BAR_H))
        out.append('<text class="era-metro" x="0" y="%d">%s</text>' % (base, esc(metro)))
        out.append('<text class="era-value" x="%d" y="%d" data-src="era_ph5_metro:%s:%s">%s</text>'
                   % (V1_VALUE_X, base, esc(metro), field, esc(fmt2(total))))
        out.append("</g>")
    if not parts:
        out.append('<text class="era-note" x="0" y="%d">baseline tariff rate only</text>'
                   % (V1_TOP + len(rows) * V1_ROW + 8))
    out.append("</g>")
    return out


def view_v1(G1):
    """V1: eight metros sorted by rank, the bar is usd_per_it_mwh split into the
    mitigated remainder (solid, ramped by magnitude) and the mitigation (hollow,
    hairline) so the avoidable part is a remainder and not a second chart.
    Both p. Basis states are pre-rendered; IT is the saved state."""
    rows = by_rank(G1)
    h = V1_TOP + len(rows) * V1_ROW + 24
    out = ['<svg data-view="V1" width="%d" height="%d" viewBox="0 0 %d %d" role="img" '
           'aria-label="Cost per IT-MWh by metro, ranked">' % (V1_W, h, V1_W, h)]
    out += _v1_state(rows, "usd_per_it_mwh", "IT", "usd_per_it_mwh", False, True)
    out += _v1_state(rows, "usd_per_mwh", "Metered", "usd_per_mwh", True, False)
    out.append("</svg>")
    return "\n".join(out)


# --------------------------------------------------------------------------
# V3 — the channel decomposition
# --------------------------------------------------------------------------
V3_W = 1184
V3_TOP = 24
V3_ROW = 48
V3_BAR_H = 24
V3_PLOT_X = 216
V3_PLOT_W = 960
# 5H-4, F5H1-4: a channel whose whole walk is narrower than one grid unit puts
# its credited label on top of the zero rule - measured, the fixed channel's
# drawn extent is ONE pixel and its label landed at x 1086, the zero rule's own
# x, to the pixel. A row that narrow is nudged one and a half grid units clear,
# to the LEFT, which keeps the label inside the plot instead of pushing it at
# the 1184 px edge.
V3_GRID = 8
V3_NUDGE = 12


def _v3_extent(rows):
    lo, hi = 0.0, 0.0
    for ch in V3_ORDER:
        cum = 0.0
        for r in rows:
            cum += num(r[ch])
            lo, hi = min(lo, cum), max(hi, cum)
    return lo, hi


def view_v3(G1):
    """V3: the five mitigation channels, portfolio-wide, no metro filter, one
    colour (F4E-3 is a comparison of lengths, not of hues). Each row is the
    eight metros walked from zero, so every mark resolves to a cell and the
    row's end point IS the channel total without a typed figure. The largest
    single contribution in each row carries its own cell as a label."""
    rows = by_rank(G1)
    lo, hi = _v3_extent(rows)
    span = hi - lo

    def x_of(v):
        return int(round(V3_PLOT_X + (v - lo) / span * V3_PLOT_W))

    h = V3_TOP + len(V3_ORDER) * V3_ROW + 24
    out = ['<svg data-view="V3" width="%d" height="%d" viewBox="0 0 %d %d" role="img" '
           'aria-label="Mitigation by channel, portfolio">' % (V3_W, h, V3_W, h)]
    out.append('<line class="era-axis" x1="%d" y1="%d" x2="%d" y2="%d"/>'
               % (x_of(0.0), V3_TOP - 8, x_of(0.0), V3_TOP + len(V3_ORDER) * V3_ROW))
    for i, ch in enumerate(V3_ORDER):
        y = V3_TOP + i * V3_ROW + (V3_ROW - V3_BAR_H) // 2
        base = y + 17
        out.append('<g data-channel="%s">' % ch)
        out.append('<text class="era-metro" x="0" y="%d">%s</text>' % (base, esc(V3_LABELS[ch])))
        cum = 0.0
        big = max(rows, key=lambda r: abs(num(r[ch])))
        big_mid = None
        row_lo = row_hi = x_of(0.0)
        for r in rows:
            v = num(r[ch])
            a, b = x_of(cum), x_of(cum + v)
            cum += v
            row_lo, row_hi = min(row_lo, a, b), max(row_hi, a, b)
            is_big = r is big and v != 0.0
            if is_big:
                big_mid = (min(a, b) + max(a, b)) // 2
            out.append('<rect class="%s" data-metro="%s" data-field="%s"%s '
                       'x="%d" y="%d" width="%d" height="%d"><title>%s</title></rect>'
                       % ("era-seg-big" if is_big else "era-seg", esc(r["metro"]), ch,
                          ' data-role="largest"' if is_big else "",
                          min(a, b), y, abs(b - a), V3_BAR_H, esc(r["metro"])))
        if big_mid is not None:
            if row_hi - row_lo < V3_GRID:
                lx, anchor = row_lo - V3_NUDGE, "end"
            else:
                lx, anchor = min(max(big_mid, V3_PLOT_X + 72), V3_W - 72), "middle"
            out.append('<text class="era-value" x="%d" y="%d" text-anchor="%s" '
                       'data-src="era_ph5_metro:%s:%s">%s</text>'
                       % (lx, y + 36, anchor, esc(big["metro"]), ch,
                          esc(fmt2(num(big[ch])))))
        out.append("</g>")
    out.append("</svg>")
    return "\n".join(out)


# --------------------------------------------------------------------------
# V2 — the waterfall (Unit 5H-2)
# --------------------------------------------------------------------------
# Geometry, and why it is what it is (era_ph5_5h_results.md section 10.1):
#   - ONE scale for all eight pre-rendered states. A per-metro scale would
#     rescale the bars when p. Metro is switched, which is the one thing a
#     pre-rendered state control must not do.
#   - baseline and mitigated-total rows run zero -> waterfall_end_usd; measure
#     and storage rows are floating bars waterfall_start_usd -> waterfall_end_usd.
#   - THE EXCLUDED SIBLINGS HAVE NO POSITION IN THE WALK: G2 leaves their
#     waterfall_start_usd and waterfall_end_usd EMPTY. They are drawn as a
#     magnitude anchored at ZERO, below a hairline separator, in --era-muted
#     with an --era-rule outline (style rule 3). Anchoring them at the mitigated
#     total and extending leftward would draw "what the total would have been",
#     which asserts an additivity the frozen contract does not carry.
#   - a bar whose true width rounds below one pixel is drawn one pixel wide, as
#     V1 already does for its mitigation segment. Disclosed, not hidden.
#   - no axis figures: a tick label is not a cell. Each row carries its own
#     credited figure instead, and there is one zero line.
V2_W = 1184
V2_TOP = 24
V2_ROW = 48
V2_BAR_H = 24
V2_PLOT_X = 304
V2_PLOT_W = 688
V2_VALUE_X = V2_PLOT_X + V2_PLOT_W + 16
V2_MAX_ROWS = 5
V2_H = V2_TOP + V2_MAX_ROWS * V2_ROW + 24       # 288, a multiple of 8 (S5)

V2_LEVEL_KINDS = ("baseline", "mitigated")


def _v2_order(r):
    return int(r["waterfall_order"] or 0)


def _v2_rows(G2, metro):
    return sorted((r for r in G2 if r["metro"] == metro), key=_v2_order)


def _v2_walks(r):
    """True when the row has a position in the walk. The excluded siblings do
    not: G2 leaves both endpoints empty on exactly those rows."""
    return bool(r["waterfall_start_usd"]) and bool(r["waterfall_end_usd"])


def _v2_scale(G2):
    """The largest quantity any state must draw, so one scale serves all eight."""
    hi = 0.0
    for r in G2:
        if _v2_walks(r):
            hi = max(hi, abs(num(r["waterfall_start_usd"])), abs(num(r["waterfall_end_usd"])))
        else:
            hi = max(hi, abs(num(r["usd_per_year"])))
    return hi


def _v2_connectors(rows, x_of):
    """5H-4, F5H2-4. This section is intended to FIND THE STEPS A WATERFALL WALK
    JOINS, from the grain and not from the drawing order.

    Consecutive rows are joined at the x-value they SHARE. Row i+1 shares row
    i's end if EITHER its waterfall_start_usd or its waterfall_end_usd lands on
    the same pixel: the first half joins a delta to the level or delta before
    it, the second half lets the mitigated TOTAL row - which starts at zero,
    not at the previous end - be joined at the value the walk actually landed
    on. A row that shares nothing is not joined at all, and an excluded sibling
    has no position in the walk (both endpoints empty in G2), so it is never
    joined - the same refusal 5H-2 made when it anchored those rows at zero.

    The share is tested on the VALUES, not on their pixels: two steps that
    round to one pixel are not the same step. Measured on G2, the two tests
    agree everywhere (22 connectors either way), and the value test is the one
    that means what the sentence says.

    Returns [(index_of_upper_row, x)].
    """
    out = []
    for i in range(len(rows) - 1):
        a, b = rows[i], rows[i + 1]
        if not (_v2_walks(a) and _v2_walks(b)):
            continue
        e = num(a["waterfall_end_usd"])
        if e == num(b["waterfall_start_usd"]) or e == num(b["waterfall_end_usd"]):
            out.append((i, x_of(e)))
    return out


def view_v2(G2, metros, saved_metro):
    """V2: the mitigation waterfall from G2, per metro. All eight metros are
    pre-rendered as sibling <g data-state-metro> groups drawn from the same top,
    so p. Metro toggles visibility and nothing reflows; the saved state
    (Columbus, F5B-7) is the only one without hidden, IN THE MARKUP, so the page
    shows it with script disabled. The three voltage siblings are present as an
    EXCLUDED band, never omitted."""
    hi = _v2_scale(G2)

    def x_of(v):
        return int(round(V2_PLOT_X + (v / hi) * V2_PLOT_W))

    out = ['<svg data-view="V2" width="%d" height="%d" viewBox="0 0 %d %d" role="img" '
           'aria-label="Mitigation waterfall for the selected metro">' % (V2_W, V2_H, V2_W, V2_H)]
    out.append('<line class="era-axis" x1="%d" y1="%d" x2="%d" y2="%d"/>'
               % (V2_PLOT_X, V2_TOP - 8, V2_PLOT_X, V2_TOP + V2_MAX_ROWS * V2_ROW))
    for m in metros:
        rows = _v2_rows(G2, m)
        out.append('<g data-state-metro="%s"%s>'
                   % (esc(m), "" if m == saved_metro else ' hidden="hidden"'))
        for i, r in enumerate(rows):
            walks = _v2_walks(r)
            excluded = r["included_in_mitigated_total"] == "0"
            y = V2_TOP + i * V2_ROW + (V2_ROW - V2_BAR_H) // 2
            base = y + 17
            if walks:
                a, b = x_of(num(r["waterfall_start_usd"])), x_of(num(r["waterfall_end_usd"]))
                cls = "era-wf-level" if r["kind"] in V2_LEVEL_KINDS else "era-wf-delta"
            else:
                # no position in the walk: a magnitude anchored at zero, under a rule
                out.append('<line class="era-axis" x1="0" y1="%d" x2="%d" y2="%d"/>'
                           % (y - 12, V2_W, y - 12))
                a, b = x_of(0.0), x_of(abs(num(r["usd_per_year"])))
                cls = "era-excluded"
            key = "%s|%s" % (r["metro"], r["component_id"])
            out.append('<g data-component="%s"%s>'
                       % (esc(r["component_id"]),
                          ' data-excluded="1" data-muted="1"' if excluded else ""))
            out.append('<title data-src="era_ph5_stack:%s:component_name">%s</title>'
                       % (esc(key), esc(r["component_name"])))
            out.append('<rect class="%s" x="%d" y="%d" width="%d" height="%d"/>'
                       % (cls, min(a, b), y, max(abs(b - a), 1), V2_BAR_H))
            out.append('<text class="era-metro" x="0" y="%d" '
                       'data-src="era_ph5_stack:%s:component_name">%s</text>'
                       % (base, esc(key), esc(r["component_name"])))
            out.append('<text class="era-value" x="%d" y="%d" '
                       'data-src="era_ph5_stack:%s:usd_per_year">%s</text>'
                       % (V2_VALUE_X, base, esc(key), esc(fmt2(num(r["usd_per_year"])))))
            out.append("</g>")
        for i, cx in _v2_connectors(rows, x_of):
            y_top = V2_TOP + i * V2_ROW + (V2_ROW - V2_BAR_H) // 2 + V2_BAR_H
            y_bot = V2_TOP + (i + 1) * V2_ROW + (V2_ROW - V2_BAR_H) // 2
            out.append('<line class="era-wf-connector" data-role="connector" '
                       'x1="%d" y1="%d" x2="%d" y2="%d"/>' % (cx, y_top, cx, y_bot))
        out.append("</g>")
    out.append("</svg>")
    return "\n".join(out)


# --------------------------------------------------------------------------
# V4 — the map (Unit 5H-3)
# --------------------------------------------------------------------------
# Geometry, and why it is what it is (era_ph5_5h_results.md section 13.1):
#   - PLATE CARREE (plain equirectangular): x is linear in station_longitude,
#     y is linear in station_latitude with north up, and ONE degrees-to-pixels
#     scale serves both axes. That single shared scale is what makes it a
#     projection rather than an arbitrary stretch, and it is what the page
#     gate re-derives from the grain (V4b clauses 2 and 3).
#   - NO BASEMAP. The ruling's default is none, and no public-domain outline
#     file is vendored, so there is no provenance to record. The frame is four
#     hairlines; the eight points are the whole drawing.
#   - Least ink on the page: eight dots, four rules, sixteen labels. No
#     graticule, no axis figures, no tick labels - a degree is not a cell.
#   - THE POINT IS A WEATHER STATION, NOT A SITE (C-STATION-POINT, which V6
#     prints). The columns are named so they cannot be read as a site.
V4_W = 1184
V4_H = 432
V4_PAD = 48
V4_PLOT_X = V4_PAD
V4_PLOT_Y = V4_PAD
V4_PLOT_W = V4_W - 2 * V4_PAD          # 1088
V4_PLOT_H = V4_H - 2 * V4_PAD          # 336
V4_INSET = 40                          # room for the labels hanging off the outermost points
V4_R = 7
V4_FLIP_X = 0.62                       # right of this fraction of the width, labels anchor end


def view_v4(G1):
    """V4: eight weather stations on a plate-carree frame, coloured by
    usd_per_it_mwh on the same seven-step ramp V1 uses. Orientation, not
    analysis (5C): it gets the least ink and it does not lead the page."""
    rows = by_rank(G1)
    lats = [num(r["station_latitude"]) for r in rows]
    lons = [num(r["station_longitude"]) for r in rows]
    lat_lo, lat_hi = min(lats), max(lats)
    lon_lo, lon_hi = min(lons), max(lons)
    s = min((V4_PLOT_W - 2 * V4_INSET) / (lon_hi - lon_lo),
            (V4_PLOT_H - 2 * V4_INSET) / (lat_hi - lat_lo))
    ox = V4_PLOT_X + (V4_PLOT_W - (lon_hi - lon_lo) * s) / 2.0
    oy = V4_PLOT_Y + (V4_PLOT_H - (lat_hi - lat_lo) * s) / 2.0
    it = [num(r["usd_per_it_mwh"]) for r in rows]
    steps = ordinal_ramp(it)

    def px(lon):
        return int(round(ox + (lon - lon_lo) * s))

    def py(lat):
        return int(round(oy + (lat_hi - lat) * s))

    out = ['<svg data-view="V4" width="%d" height="%d" viewBox="0 0 %d %d" role="img" '
           'aria-label="Metro weather stations, coloured by cost per IT-MWh">'
           % (V4_W, V4_H, V4_W, V4_H)]
    # 5H-4, F5H3-9: THE FRAME IS GONE. It bounded the 1088 x 336 plot box while
    # the projected extent is 966 x 256, so it read as an arbitrary rectangle
    # around the points rather than the edge of anything. Hugging the extent
    # instead would put the four extreme stations' r=7 circles half outside
    # their own frame - an arbitrary rectangle traded for a broken one. The
    # ruling's word for this view is LEAST INK; eight dots and their labels are
    # the whole drawing, and the page gate now asserts V4 draws no line at all
    # and is strictly the least-inked view.
    for r in rows:
        m = r["metro"]
        cx, cy = px(num(r["station_longitude"])), py(num(r["station_latitude"]))
        step = steps[num(r["usd_per_it_mwh"])]
        end = cx > V4_W * V4_FLIP_X
        tx = cx - (V4_R + 5) if end else cx + (V4_R + 5)
        anchor = ' text-anchor="end"' if end else ""
        out.append('<circle class="era-ramp-%d" data-role="point" data-metro="%s" '
                   'data-field="usd_per_it_mwh" cx="%d" cy="%d" r="%d">'
                   '<title data-src="era_ph5_metro:%s:metro">%s</title></circle>'
                   % (step, esc(m), cx, cy, V4_R, esc(m), esc(m)))
        out.append('<text class="era-metro" x="%d" y="%d"%s data-src="era_ph5_metro:%s:metro">%s</text>'
                   % (tx, cy + 4, anchor, esc(m), esc(m)))
        out.append('<text class="era-value" x="%d" y="%d"%s data-src="era_ph5_metro:%s:state">%s</text>'
                   % (tx, cy + 20, anchor, esc(m), esc(r["state"])))
    out.append("</svg>")
    return "\n".join(out)


# --------------------------------------------------------------------------
# V5 — the bands and the two published pairs, as intervals (Unit 5H-3)
# --------------------------------------------------------------------------
# THE BASIS PROBLEM AND ITS RESOLUTION (era_ph5_5h_results.md section 13.1):
# C-BAND-25's crossing figure is 0.8042 $/MWh on the PUBLISHED FACILITY basis
# (measured off G1: Columbus band_high_usd_per_mwh 70.81617743 - Chicago
# usd_per_mwh 70.01194141 = 0.80423602). V5 is ruled onto the $/IT-MWh axis,
# where the SAME adjacency crosses by 1.08102537 - a difference of two cells,
# which exists in no cell of any grain.
#   Printing 0.8042 beside an IT-basis drawing is the basis mismatch F5A-4
#   exists to prevent. Printing 1.0810 is a typed derived figure (F5H1-5).
#   SO V5 PRINTS NEITHER. The crossing is carried by the two endpoint cells,
#   each printed and credited to its own G1 column, and by the drawing:
#   Columbus's band extends strictly past Chicago's central mark, under a
#   guide hairline. The annotation names the adjacency from G4, verbatim.
# DO NOT "improve" this into 0.8042.
V5_W = 1184
V5_TOP = 24
V5_ROW = 48
V5_BAR_H = 16
V5_PLOT_X = 288
V5_PLOT_W = 640
# 5H-4, F5H3-8: THE VALUE LABELS ANCHOR TO THE MARK, NOT TO THE ROW. The fixed
# row positions this replaces (V5_LOW_X / V5_HIGH_X) made a 14 px bracket read
# as though it spanned the whole row, and the narrower the interval the more
# the labels overstated it - the opposite of what an interval view is for.
# One offset, one grid unit, all three label kinds: the low label sits a grid
# unit left of the drawn left edge, the high label a grid unit right of the
# drawn right edge, the central label a grid unit right of its own tick.
# THE CROSSING GUIDE'S OVERPRINT IS SOLVED BY THIS RULE AND NOT BY A SPECIAL
# CASE: the guide is a hairline at the crossed metro's central tick x, and that
# metro's label no longer straddles the tick. The guide's geometry does not
# move, which matters because B4 gates it.
V5_LABEL_GAP = 8
V5_NOTE_DY = 32
V5_H = V5_TOP + 5 * V5_ROW + 72        # 336, a multiple of 8 (S5)

V5_BAND = ("band", "band_low_usd_per_it_mwh", "band_high_usd_per_it_mwh", "era-band")
V5_BRACKET = ("bracket", "bracket_low_usd_per_it_mwh", "bracket_high_usd_per_it_mwh", "era-bracket")


def _v5_rows(G1):
    """The five intervals, bands first then brackets, each in rank order.
    Membership is READ OFF THE GRAIN (is_market_priced / has_bracket), never
    listed here - the same discipline F5B-7 imposed on V2's eligible set."""
    rank = sorted(G1, key=lambda r: int(r["rank"]))
    out = [(r, V5_BAND) for r in rank if r["is_market_priced"] == "1"]
    out += [(r, V5_BRACKET) for r in rank if r["has_bracket"] == "1"]
    return out


def _v5_crossing(G1):
    """The adjacency the bands touch, DERIVED from G1: a banded metro whose
    upper edge reaches past the central figure of a metro ranked below it.
    C-BAND-25 says there is exactly one anywhere in the table; this returns
    every one it finds so the page gate can assert that count."""
    rank = sorted(G1, key=lambda r: int(r["rank"]))
    hits = []
    for a in rank:
        if a["is_market_priced"] != "1":
            continue
        for b in rank:
            if int(b["rank"]) > int(a["rank"]) and \
                    num(a["band_high_usd_per_it_mwh"]) > num(b["usd_per_it_mwh"]):
                hits.append((a["metro"], b["metro"]))
    return hits


def view_v5(G1, G4):
    rows = _v5_rows(G1)
    vals = []
    for r, (kind, lof, hif, cls) in rows:
        vals += [num(r[lof]), num(r[hif])]
        if kind == "band":
            vals.append(num(r["usd_per_it_mwh"]))
    lo, hi = min(vals), max(vals)

    def x_of(v):
        return int(round(V5_PLOT_X + (v - lo) / (hi - lo) * V5_PLOT_W))

    out = ['<svg data-view="V5" width="%d" height="%d" viewBox="0 0 %d %d" role="img" '
           'aria-label="Market bands and published pairs, as intervals">'
           % (V5_W, V5_H, V5_W, V5_H)]
    y_of_row = {}
    for i, (r, (kind, lof, hif, cls)) in enumerate(rows):
        m = r["metro"]
        bar_y = V5_TOP + i * V5_ROW + 20
        base = bar_y + 12
        y_of_row[(m, kind)] = bar_y
        a, b = x_of(num(r[lof])), x_of(num(r[hif]))
        rw = max(b - a, 1)
        out.append('<g data-role="interval" data-metro="%s" data-kind="%s" '
                   'data-low-field="%s" data-high-field="%s">'
                   % (esc(m), kind, lof, hif))
        out.append('<title data-src="era_ph5_metro:%s:metro">%s</title>' % (esc(m), esc(m)))
        out.append('<rect class="%s" data-edge="span" x="%d" y="%d" width="%d" height="%d"/>'
                   % (cls, a, bar_y, rw, V5_BAR_H))
        out.append('<text class="era-metro" x="0" y="%d" data-src="era_ph5_metro:%s:metro">%s</text>'
                   % (base, esc(m), esc(m)))
        out.append('<text class="era-value" x="%d" y="%d" text-anchor="end" '
                   'data-role="label-low" data-src="era_ph5_metro:%s:%s">%s</text>'
                   % (a - V5_LABEL_GAP, base, esc(m), lof, esc(fmt2(num(r[lof])))))
        out.append('<text class="era-value" x="%d" y="%d" text-anchor="start" '
                   'data-role="label-high" data-src="era_ph5_metro:%s:%s">%s</text>'
                   % (a + rw + V5_LABEL_GAP, base, esc(m), hif, esc(fmt2(num(r[hif])))))
        if kind == "band":
            cx = x_of(num(r["usd_per_it_mwh"]))
            out.append('<line class="era-axis" data-role="central" data-metro="%s" '
                       'data-src="era_ph5_metro:%s:usd_per_it_mwh" '
                       'x1="%d" y1="%d" x2="%d" y2="%d"/>'
                       % (esc(m), esc(m), cx, bar_y - 4, cx, bar_y + V5_BAR_H + 4))
            out.append('<text class="era-value" x="%d" y="%d" text-anchor="start" '
                       'data-role="label-central" '
                       'data-src="era_ph5_metro:%s:usd_per_it_mwh">%s</text>'
                       % (cx + V5_LABEL_GAP, bar_y - 8, esc(m),
                          esc(fmt2(num(r["usd_per_it_mwh"])))))
        out.append("</g>")

    # the crossing: a guide hairline at the crossed central mark, spanning the
    # two rows it joins, plus the adjacency's name from G4, rendered verbatim.
    hits = _v5_crossing(G1)
    idx = {r["metro"]: r for r in G1}
    for hi_m, lo_m in hits:
        if (hi_m, "band") not in y_of_row or (lo_m, "band") not in y_of_row:
            continue
        gx = x_of(num(idx[lo_m]["usd_per_it_mwh"]))
        ya = min(y_of_row[(hi_m, "band")], y_of_row[(lo_m, "band")]) - 12
        yb = max(y_of_row[(hi_m, "band")], y_of_row[(lo_m, "band")]) + V5_BAR_H + 12
        out.append('<line class="era-axis" data-role="guide" x1="%d" y1="%d" x2="%d" y2="%d"/>'
                   % (gx, ya, gx, yb))
    band = next((r for r in G4 if r["caveat_id"] == "C-BAND-25"), None)
    if band is not None:
        out.append('<text class="era-note" data-role="crossing" x="0" y="%d" '
                   'data-src="era_ph5_caveat:C-BAND-25:title">%s</text>'
                   % (V5_TOP + len(rows) * V5_ROW + V5_NOTE_DY, esc(band["title"])))
    out.append("</svg>")
    return "\n".join(out)


# --------------------------------------------------------------------------
# V6 — the caveats table (Unit 5H-3)
# --------------------------------------------------------------------------
# Driven ENTIRELY by G4, in sort_rank order, unpriced above limitations, the
# FERC take-or-pay floor first with no dollar - which is the point (5C).
# Every cell is that row's own cell, credited era_ph5_caveat:<id>:<column>;
# a row may not borrow another row's credit (page gate V6b clause 4).
#
# `statement` IS DELIBERATELY NOT A COLUMN. C-BAND-25's statement cell holds
# the literal 0.9742, which B3 forbids as page text (F5A-4) - rendering it
# would fire B3 on the honesty table itself. The statements are on the page in
# full, in the embedded G4 JSON that H13 proves fresh. Nothing is hidden.
#
# usd_per_it_mwh prints at SIX decimals, the grain's own precision. Four would
# put C-SJ-PF (-0.813647 -> -0.8136, error 0.000047) at 94 % of T2's 0.00005
# tolerance, and a gate that passes by 6 % of a margin is not a gate.
V6_COLUMNS = [
    ("caveat_id", "ID", False),
    ("category", "Class", False),
    ("title", "Caveat", False),
    ("metro_scope", "Scope", False),
    ("priced", "Priced (1/0)", True),
    ("usd_per_year", "USD / yr", True),
    ("usd_per_it_mwh", "USD / IT-MWh", True),
]


def fmt6(v):
    return "{:,.6f}".format(v)


def view_v6(G4):
    rows = sorted(G4, key=lambda r: int(r["sort_rank"]))
    out = ['<table class="era-table" data-view="V6">', "<thead>", "<tr>"]
    for col, head, numeric in V6_COLUMNS:
        out.append('<th%s>%s</th>' % (' class="era-num"' if numeric else "", esc(head)))
    out += ["</tr>", "</thead>", "<tbody>"]
    for r in rows:
        cid = r["caveat_id"]
        out.append('<tr data-caveat="%s">' % esc(cid))
        for col, head, numeric in V6_COLUMNS:
            raw = r[col]
            if col == "usd_per_year":
                txt = fmt2(num(raw)) if raw else ""
            elif col == "usd_per_it_mwh":
                txt = fmt6(num(raw)) if raw else ""
            else:
                txt = raw
            out.append('<td%s data-src="era_ph5_caveat:%s:%s">%s</td>'
                       % (' class="era-num"' if numeric else "", esc(cid), col, esc(txt)))
        out.append("</tr>")
    out += ["</tbody>", "</table>"]
    return "\n".join(out)


# A BUILT view is registered here; the build's unbuilt branch is driven by
# VIEWS.get(v) is None, so V4/V5/V6 stay build-incomplete slots.
VIEWS = {"V1": view_v1, "V2": view_v2, "V3": view_v3,
         "V4": view_v4, "V5": view_v5, "V6": view_v6}


def render(view_id, grains, metros, saved_metro):
    """Dispatch: each view is handed the grain it reads and nothing else. V2 is
    the first view that does not read G1, which is why this exists — the 5H-1
    build called every view with grains['G1']. The metro order and the saved
    metro are PASSED IN from the build so there is exactly one definition of
    them on the page (the same list P4 gates the control against)."""
    if view_id == "V1":
        return view_v1(grains["G1"])
    if view_id == "V2":
        return view_v2(grains["G2"], metros, saved_metro)
    if view_id == "V3":
        return view_v3(grains["G1"])
    if view_id == "V4":
        return view_v4(grains["G1"])
    if view_id == "V5":
        return view_v5(grains["G1"], grains["G4"])
    if view_id == "V6":
        return view_v6(grains["G4"])
    return None
