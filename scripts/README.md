# Data refresh — International Student Demand

Source: data.gov.au dataset **student-visas** (Dept of Home Affairs, BP0015). CKAN API:
`https://data.gov.au/data/api/3/action/package_show?id=student-visas` → download the current
"Student visas granted" XLSX (a pivot-table workbook; the real multi-dimensional data is in the
embedded pivotCache, not the visible sheet).

1. `extract_visa.py` — streams the pivotCache records (~2.3M) from `visa_granted.xlsx`, filters
   to full financial years + the current partial and to **Primary** applicants (students, not
   dependants), aggregates to FY×sector, FY×country, FY×onshore/offshore, and country×sector
   (latest full year) → `visa_agg.json`. Runs in ~40s.
2. `build_visa.py` — cleans country names (formal → common) and writes `data.js`
   (window.VISADEMAND).

To refresh: download the newest granted XLSX as `visa_granted.xlsx`, update the `FULL`/`PARTIAL`
year lists in extract_visa.py if a new financial year has closed, run both, copy data.js here,
bump manifest lastBuild. (Grant-rate and lodged workbooks exist in the same dataset if a
grant-rate view is ever wanted — not currently used.)
