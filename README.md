# Riyadh HeatReady

Riyadh HeatReady is a small, testable Proof of Concept for the **Urban Expansion, Land Use Change & Heat Risk** challenge.

## One-sentence problem

Identify 1 km zones along southeastern Riyadh's urban-industrial fringe where built-up growth from a separate annual land-cover product for 2018 to 2023, confirmed by 2025 optical and radar observations, overlaps high 2025 land-surface temperature and population exposure, so municipal planning and heat-resilience teams can prioritize cooling measures and field checks.

## Why this city and area

- The official open Tanager urban collection contains a Riyadh scene from 15 May 2025.
- Matching low-cloud Sentinel-2, Sentinel-1, and Landsat observations exist within days of that scene.
- Comparable Sentinel-2 and Sentinel-1 observations exist for May 2018.
- The area contains a mix of built-up land, industrial surfaces, roads, bare soil, and undeveloped land. That makes it useful for testing urban-growth methods in an arid environment.

## Intended user and decision

The intended user is a municipal urban-planning and heat-resilience team. The product ranks zones for **closer inspection**, not automatic construction decisions. A high-priority zone is a place where heat, people, and recent growth overlap and where locally suitable cooling measures should be assessed.

## Current state

The end-to-end PoC is working. It produces a decision dashboard, a six-year annual built-up trend, evidence maps, a spatial holdout check, priority-zone tables, GeoTIFF outputs, and a descriptive Planet Tanager spectral comparison.

## Set up a clean copy

Use Python 3.12 from this `project` folder:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

The complete first run downloads the open inputs, including one Planet Tanager
HDF5 scene of about 856 MB.

## Reproduce the outputs

Run the complete sequence:

```powershell
.\build_all.ps1
```

The script uses a local `.venv` when present, the workspace environment as a
fallback, or the active `python` command. It stops immediately if any step fails.
Raw and cached data are excluded from the submission package. The second analysis
run embeds the completed Tanager result in the self-contained dashboard.

The same sequence can be run manually:

```powershell
.\.venv\Scripts\python.exe src\verify_sources.py
.\.venv\Scripts\python.exe src\run_analysis.py
.\.venv\Scripts\python.exe src\analyze_tanager.py
.\.venv\Scripts\python.exe src\run_analysis.py
.\.venv\Scripts\python.exe src\check_outputs.py
.\.venv\Scripts\python.exe src\package_submission.py
```

Main result: open `outputs/dashboard.html`.

The Week 2 training review is in `docs/WEEK2_TRAINING_REVIEW.md`. The annual chart is `outputs/annual_built_area_timeseries.png`, and its exact values are in `outputs/annual_built_area_timeseries.csv`.

The current rules, deadlines, judging criteria, link audit, and source conflicts are in `docs/OFFICIAL_RESEARCH_AUDIT.md`.

The detailed onboarding-guide, linked-source, and full starter-repository review is in `docs/ONBOARDING_REPOSITORY_AUDIT.md`.

## Folder guide

- `src/` — data checks, analysis, Tanager comparison, and final verification.
- `docs/` — official research audit, project brief, beginner explanation, data licences, presenter guide, AI log, and submission checklist.
- `outputs/` — dashboard, maps, tables, rasters, summaries, manifest, and verification report.
- `data/raw/` and `data/cache/` — downloaded working data; excluded from the submission package.

## Important limits

- Land-surface temperature is not the same as air temperature or personal heat exposure.
- Satellite-built-up classification can confuse bright roofs, compacted soil, and bare desert.
- WorldPop values are modelled estimates, not a live census.
- The Tanager scene is one date, so it can characterise 2025 surface materials but cannot independently prove 2018–2025 change.
- Any high-priority result requires local review and field checking.
