# BUILD SPEC — International Student Demand (dashboard #9 in Phil's suite)

Build a single-file `index.html` in THIS directory. New dashboard: Department of Home Affairs
student-visa **grants** by source country and education sector — the international-**demand**
counterpart to the CRICOS course-**supply** dashboard. Audience: a PVC (Research) / Dean of an
education-product unit; tone executive, numbers-first, honest about what the data is.

## What this data is (state it, don't blur it)

- Counts are **visa GRANTS** (subclass 500) — a demand-*realised* signal (who was granted a visa
  to come), NOT applications, NOT enrolments, NOT commencements. Never call them any of those.
- **Primary applicants only** — the students. Dependants (secondary) are excluded.
- **National / sector / source-country.** Home Affairs publishes provider *state* but NOT
  individual providers, so **there is no institution-level or ACU view** — do not invent one or
  force an ACU default. This is macro demand intelligence.
- It **complements CRICOS** (which is course supply with no nationality) — say so, but they are
  separate datasets, not a join (the demand×supply join is a separate future dashboard).

## Suite conventions (match the sibling dashboards; read grant-outcomes/index.html for patterns — do NOT read its data blob)

- Single self-contained `index.html`; data via `<script src="data.js"></script>` (present —
  `window.VISADEMAND`; schema below is authoritative, don't parse the file wholesale).
- `<head>`, non-deferred: `<script src="https://pdparker.github.io/dashboard-commons/commons.js" data-dash="intl-demand"></script>`
  (suite nav; the "intl-demand" entry is being registered separately — an unhighlighted strip in
  local dev is fine).
- ACU brand identical to the grant-outcomes pages: purple `#3C1053` masthead, red `#F2120C`
  accents, sand `#FBF6F0`/white surfaces, Manrope headings, Arial body. Reuse the same
  `.masthead`/`.kpi`/`.card`/`.bar-row`/`.chip` CSS idioms.
- Chart.js 4.5.1 (same pinned CDN + SRI as the siblings) for the temporal LINE charts only.
  Ranked country/sector bars = pure CSS/HTML divs (print-friendly).
- URL state via `DashCommons.state`; CSV export button; print stylesheet (hide controls, cards
  break-inside:avoid). Registry not needed (no institutions in this data).

## Data schema (`window.VISADEMAND`)

```
{
  generated, source, measure,
  full_years: ["2005-06", ... "2024-25"],       // 20 clean financial years
  partial_label: "2025-26 to 31 May 2026",       // current partial FY — never compare to full years
  latest_full: "2024-25",
  sectors: ["Higher Education","VET","ELICOS","Postgraduate Research","Schools","Non-Award","Foreign Affairs/Defence"],
  fyTotal:  { "2024-25": 322773, ... },           // primary grants per FY (incl the partial key)
  byFYsec:  { "2024-25": { "Higher Education":206300, "VET":53671, ... }, ... },
  byFYcty:  { "2024-25": { "China":86160, "India":41700, ... }, ... },   // ~195 countries/yr, cleaned names
  ctySec_latest: { "Nepal": { "Higher Education":20456, "VET":3210, ... }, ... },  // 2024-25 only
  byFYloc:  { "2024-25": { onshore:112350, offshore:210423 }, ... },     // In/Outside Australia
  meta: { note, partial, policy }
}
```

## Views (top to bottom)

1. **Masthead** (purple). Title "International Student Demand". Subtitle: Home Affairs student-
   visa grants (subclass 500, primary applicants) by source country and sector; the demand
   complement to CRICOS supply. Controls: **Year** selector (financial years, `latest_full`
   default; the partial year labelled "(to 31 May 2026, partial)"); CSV export. (No metric
   toggle — single measure. No institution control.)
2. **KPI row (4)**: total grants (selected year); change vs the 2022-23 peak (▼ from ~500k —
   the tightening story); Higher Education share; offshore share (grants made outside Australia).
3. **National trend** (centrepiece) — Chart.js line, grants by FY 2005-06 → 2024-25, with the
   `partial_label` point dashed/hollow and labelled partial (reuse the dashed-final-segment
   technique from the staff dashboard). Brief annotation of the shape: COVID collapse (2020-21),
   post-COVID peak (2022-23 ~500k), tightening since. A caption references MD107/111 + caps.
4. **By sector** — sector mix. Either a stacked-area over time or, for the selected year, ranked
   CSS bars per sector with share (Higher Ed ~64%, VET next). Include a small "sector share over
   time" element if clean — the VET share swing is the interesting bit.
5. **Top source countries** — ranked CSS bars, top ~15 for the selected year, grants + share of
   that year. China / India / Nepal lead. This is the "nationality" view.
6. **Country explorer** — select a source country (default China) → its grant trend across years
   as a line (surge-and-tighten is visible per country) + its sector mix from `ctySec_latest`
   (e.g. Nepal is far more VET-weighted than China). Country selection persists in the URL.
7. **Onshore / offshore** — share of grants made In vs Outside Australia (selected year, and/or
   over time). Offshore ≈ genuinely new arrivals; onshore ≈ transitions/further study of people
   already here — a meaningful demand-composition signal.
8. **Caveats card** (always visible): grants not applications/enrolments; primary only
   (dependants excluded); national/sector only, no provider or institution detail; 2025-26
   partial; policy context (MD107 then 111, financial/English requirements, NOSC caps from 2025);
   complements but does not join CRICOS.
9. **CSV export** — long format, e.g. `dimension,year,key,grants` covering fyTotal, byFYsec,
   byFYcty (selected year), byFYloc; or a sensible tidy layout. Respect the selected year for the
   country/sector rows.
10. **Sources footer** — Home Affairs BP0015 via data.gov.au; part of Phil's dashboard suite.

## URL state keys

`year` (default `latest_full`), `country` (country explorer, default "China"). Read ALL params
before applying any; sync on change; restore on load.

## Verification (before finishing)

Serve `python3 -m http.server 8954`; browser tools:
- zero console errors.
- Hand-checks (year 2024-25): total grants **322,773**; 2022-23 peak **499,696** (KPI shows the
  ▼ vs peak); Higher Education **206,300 (63.9%)**; VET **53,671**; offshore **210,423** of
  322,773 (**65.2%**); top country **China 86,160**; national-trend line peaks at 2022-23 and the
  final point is the dashed partial (**268,429**).
- Country explorer: default China renders a multi-year line; switching to Nepal shows its sector
  mix is much more VET-weighted (HE 20,456 vs VET 3,210) than China's.
- `?year=2022-23&country=India` cold-load restores both.
- CSV intercept (URL.createObjectURL) has plausible long-format rows.
Kill the server. Do NOT git commit / push / create repos — the parent session deploys. Only
create index.html; do not edit data.js, manifest.json, or this spec.
