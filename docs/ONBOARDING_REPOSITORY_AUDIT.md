# Onboarding guide and GitHub audit

**Checked:** 1 October 2026  
**Purpose:** determine whether the participant onboarding guide, its links, and the full starter repository require changes to Riyadh HeatReady.

## Bottom line

The guide confirms the project's current direction. No analysis or project-scope change is required.

Riyadh HeatReady already follows every important instruction in the guide:

- one official theme;
- one precise problem, user, and decision;
- one manageable area of interest;
- an open Sentinel/Landsat baseline;
- multi-date evidence for a change question;
- documented quality masks, sources, dates, processing, and licences;
- a spatially separated model test;
- strategic rather than decorative hyperspectral use;
- no dependency on restricted data; and
- no credentials or raw restricted imagery in the package.

The deeper audit did find weaknesses in the starter repository. They strengthen the decision to use it as teaching material rather than as the final authority or as submission-ready code.

## Guide-to-project comparison

| Onboarding instruction | Riyadh HeatReady evidence | Result |
|---|---|---|
| Choose one official theme | Sustainable Urban Planning and Smart Cities; assigned challenge is Urban Expansion, Land Use Change & Heat Risk | Met |
| Start with a user and decision | One municipal planning/heat-resilience user and one inspection-priority decision | Met |
| Use a small AOI | 168.30 km² southeastern Riyadh test area, not a whole city or country | Met |
| Start with Sentinel-2 or Landsat | Sentinel-2 is the optical baseline; Landsat supplies surface temperature | Met |
| Use a time series for change | Six annual maps for 2018–2023 plus separate 2018/2025 optical-radar evidence | Met |
| Screen clouds and quality flags | Sentinel-2 SCL, Landsat QA, Tanager no-data/cirrus, and a strict beta-cloud sensitivity test | Met |
| Do not treat an index as truth | NDBI is treated as one feature; the project explicitly demonstrates its arid-city failure | Met |
| Avoid random neighbouring-pixel train/test leakage | West training area, separated middle threshold strip, and east holdout area | Met |
| Establish an explainable baseline before deep learning | Transparent random forest and explicit scoring formula; no deep-learning dependency | Met |
| Record provenance and licences | Exact item IDs, dates, assets, provider links, processing notes, and licences are recorded | Met |
| Use hyperspectral data only for a real limitation | Tanager is used to test surface-spectral separation and the NDBI limitation, not to decorate the entry | Met |
| Do not rely on premium data | The complete PoC uses open data and remains reproducible without gIQ, commercial imagery, Satellite 813, or MBZ-SAT | Met |

## Access phases

The guide says the PoC should be built from open multispectral and open hyperspectral data. It places commercial Planet data, gIQ, Satellite 813, and MBZ-SAT in later or availability-dependent stages.

This matches the 27 September authenticated organizer answer: use open Sentinel-2, Sentinel-1, and Landsat with the team's own tools for the PoC; gIQ and sponsored imagery are for shortlisted teams after PoC evaluation; Satellite 813 will be shared when available.

**Decision:** do not add a restricted-data dependency. A later dataset can improve a shortlisted version, but it must not replace the reproducible open baseline.

## Full starter-repository audit

Repository: `https://github.com/Tnecniv-Teikram/813-hyperspectral-hackathon`

### Current state

- Default branch: `main`.
- Current head: `55d310a0cd3dadbf0ffb39563eb466570e01b73c`.
- Head commit date: 24 August 2026.
- The head is unchanged from the earlier project audit.
- Contents: README, requirements, `.gitignore`, and seven notebooks; ten files total.
- Branches: `main` and `develop`.
- No tags or releases.
- No open issues.
- GitHub reports no repository licence, and the repository contains no `LICENSE` file.

### Documentation problems

The README is useful background, but several parts cannot be trusted as current instructions:

1. It contains older team-size, schedule, data-access, and judging information. The live official site and authenticated portal take priority.
2. It describes a `notebooks/`, `docs/`, and `assets/` directory structure that is not present in the repository.
3. Several README notebook links point into the missing `notebooks/` directory and are broken.
4. The Colab badge uses the placeholder `YOUR-ORG/arab-813-hackathon` and a nonexistent notebook path.
5. The README says the code is MIT licensed, but there is no licence file and GitHub detects no licence. Do not copy or redistribute its code based only on that sentence.
6. The quick-start notebook contains a saved `NameError: h5py is not defined` output. The current source does import `h5py`, so this appears to be stale or out-of-order notebook output rather than proof that the current cell sequence always fails. It still means the notebook is not a clean, fully executed reference artifact.

### Notebook findings

- The repository notebooks are tutorials. Their outputs show example scenes and thresholds, not validated hackathon results.
- `00_EO_data_quickstart_notebook.ipynb` teaches STAC, COGs, Sentinel-2, Tanager HDF5, wavelength metadata, and quality masks. These concepts are already used in the project.
- `02_land_use_land_cover_change.ipynb` lists four urban items but selects `items[0]`. That first item covers approximately 106.57–106.78°E and 10.59–10.78°N, around Ho Chi Minh City, not Riyadh.
- The Riyadh item is the second listed item: `20250515_080954_16_4001`, covering approximately 46.74–46.97°E and 24.49–24.67°N. Riyadh HeatReady explicitly uses this exact item rather than inheriting the notebook's first-item choice.
- The land-use notebook uses simple NDBI/BUI thresholds. Bright bare desert can exceed built surfaces on NDBI, so that method is not safe by itself for Riyadh. The project instead combines optical bands, radar, reference land cover, annual maps, and a separate Tanager sensitivity check.
- The other five theme notebooks contain no hidden rule that changes the urban challenge. They demonstrate agriculture, greenhouse-gas, disaster, blue-carbon, and water workflows.

## Linked-source findings

The guide's direct links and the relevant deeper documentation were checked.

| Source | What the deeper link established | Project decision |
|---|---|---|
| Copernicus Data Space | Free/open Sentinel access, browsers, APIs, STAC, and cloud processing are available | Sentinel-2 remains appropriate |
| Microsoft Planetary Computer | STAC access supports the exact Sentinel-1, Sentinel-2, Landsat, WorldCover, and annual land-cover items used by the project | Keep the recorded item IDs |
| NASA/USGS Landsat | Landsat supports historical multispectral analysis and Level-2 surface-temperature work | Keep the Landsat LST layer and its air-temperature warning |
| Planet Tanager STAC | The urban collection and exact Riyadh item remain reachable and the collection is CC BY 4.0 | Keep the selected open scene and attribution |
| HyperCoast documentation and repository | HyperCoast is an optional interactive hyperspectral viewer and analysis library with Tanager examples | Do not add it merely for complexity; the direct `h5py` workflow is smaller and reproducible |
| EnMAP and DLR | EnMAP is a valid alternative hyperspectral source, but current download workflows require registration; an institutional/company email or exemption may be needed. A temporary planning-portal maintenance period runs through 9 October 2026 | Do not add EnMAP unless it solves a demonstrated gap |
| STAC specification | STAC is a catalogue standard for searching and describing geospatial assets | Continue recording exact collection and item metadata |

## Exact Tanager facts checked

For `20250515_080954_16_4001`:

- the STAC item and HDF5 asset are reachable;
- the collection licence is `CC-BY-4.0`;
- the surface-reflectance asset contains 426 wavelength records;
- the recorded centres span 376.44–2499.0 nm;
- the STAC item reports a nominal `gsd` of 32.7 m;
- the orthorectified HDF5 grid itself is 760 × 654 with exact 30 m × 30 m grid spacing; and
- the current project's “30 m pixels” wording refers to this grid spacing and is correct.

GSD and output-grid spacing describe related but different things. They should not be silently substituted for each other.

## Current link and data verification

The project's live source verification was rerun on 1 October 2026 and passed all **38 checks**. This confirms that the exact planned Sentinel-2, Sentinel-1, Landsat, WorldCover, annual land-cover, WorldPop, and Tanager sources remain reachable and cover the configured AOI.

## What was actually missing

No required analysis step was missing. The earlier project had already used the guide's important technical lessons.

The items that were not previously documented in one place were:

- the repository's broken paths and placeholder Colab link;
- the absence of a repository licence file;
- the stale error output in the quick-start notebook;
- the exact distinction between the Tanager STAC GSD and the HDF5 grid spacing; and
- why HyperCoast and EnMAP are optional rather than necessary additions.

These findings improve documentation and presentation readiness. They do not justify changing the problem, city, user, model, or MVP.

## Still unknown

The onboarding guide does not reveal the closed submission form's exact fields, word limits, upload sizes, pitch duration, video or slide requirement, repository visibility rule, or required AI-disclosure wording. Those still require the portal, the repaired orientation material, or a direct organizer answer.
