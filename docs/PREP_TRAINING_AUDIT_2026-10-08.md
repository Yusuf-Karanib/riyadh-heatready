# Preparatory training audit — 8 October 2026

## Bottom line

The new material strengthens the existing Riyadh HeatReady approach. It does not justify changing the problem, city, user, scoring formula, or MVP.

The project already follows the main technical lessons:

- start with a small, explainable baseline;
- use a small area of interest and exact source records;
- quality-mask and align satellite inputs before comparing them;
- use a projected coordinate system for local measurement;
- keep categorical and continuous resampling separate;
- use explicit NoData values;
- separate model development and spatial testing;
- treat simple indices and one-date imagery as evidence, not truth; and
- deliver visible results with limitations and reproducible code.

The training files are optional learning material. They are not extra submission deliverables. Their contents are summarized here, but the files themselves are not copied into this public repository because the supplied decks prohibit redistribution.

## Rule hierarchy used

When sources differ, this project uses the newest authenticated portal instruction first, followed by the current official website, the detailed submission orientation, earlier official decks, and then optional training examples.

Two official judging descriptions remain visible:

1. The current public site and the September kickoff deck list seven PoC criteria: problem definition, technical soundness, meaningful EO or hyperspectral use, product and delivery model, innovation, impact and strategic alignment, and business viability.
2. The detailed 1 October submission orientation groups evaluation into five operational headings: space-data quality, team strength, problem relevance and impact, innovation, and feasibility, with stated bonus considerations.

These formulations overlap rather than requiring two different projects. Riyadh HeatReady is checked against their union. No unpublished weights are assumed. Clear communication is important judging advice, but it is not treated as an additional numbered criterion.

The deadline remains **11 October 2026 at 23:59 in the team creator's local time**. For Yusuf, that is 23:59 UAE time.

## Material reviewed

| Material | What it is | Effect on Riyadh HeatReady |
|---|---|---|
| Preparatory kickoff deck | Official program, themes, data phases, technical bar, criteria, timeline, and early submission framing | Confirms the selected urban theme, open-data baseline, small explainable PoC, deadline, and public seven-criterion rubric |
| Introduction to remote sensing | Optional technical foundation | Confirms that resolution must follow the question, clouds and atmosphere matter, and local measurements should use a projected CRS |
| Two hyperspectral-imaging decks | Optional technical foundation at two levels of detail | Confirms that spectra depend on surface condition and processing; supports the project's cautious one-date Tanager use |
| Introduction to machine learning | Optional general ML training | Confirms train/validation/test separation, suitable metrics, and the warning against random splitting for spatial data |
| California housing and breast-cancer CSV files | Generic regression and classification examples | Useful for learning only; they are unrelated to the hackathon problem and are not project inputs |
| GDAL end-to-end slides and pasted lab | Optional geospatial processing training | Confirms inspect-first processing, float arithmetic for indices, correct resampling, explicit NoData, projected measurement, tiled compressed outputs, and spatial splitting by area |
| Time-series and change-detection notebook text | Optional teaching workflow using Sentinel-1 and Sentinel-2 | Confirms alignment, quality masking, common grids, and multi-date evidence; its conflict example and simple NDBI workflow are not copied into this project |
| Deep-learning slides and two notebooks | Optional pixel-classification lesson | Confirms baseline-first experimentation, validation before final testing, spatial separation, and honest transfer limits; deep learning is not required for this PoC |

## Technical comparison with the project

| Training lesson | Project evidence | Result |
|---|---|---|
| Inspect metadata, grid, and CRS | Exact collection, item, asset, date, CRS, and grid records are stored in `config.json` and the data audit | Met |
| Use metres for local area and distance | Analysis rasters use Riyadh UTM, EPSG:32638 | Met |
| Use float arithmetic for band calculations | Continuous bands are converted to floating point before indices and model features are calculated | Met |
| Preserve class labels during resampling | Land-cover and mask layers use nearest-neighbour resampling | Met |
| Use suitable resampling for measurements | Continuous layers use bilinear or average resampling according to their purpose | Met |
| Declare NoData explicitly | Continuous outputs use `-9999`; binary categorical outputs use `255`, leaving valid zero untouched | Met |
| Make shared rasters efficient | Outputs are tiled GeoTIFFs with DEFLATE compression; they are small local judge artifacts, so adding overviews would not materially improve review | Met |
| Avoid neighbouring-pixel leakage | West is used for training, a separate middle strip for tuning, and the east side for the final spatial holdout | Met |
| Establish an explainable baseline before complexity | The model and four-part priority score are transparent; there is no deep-learning dependency | Met |
| Do not treat one index as truth | Growth must pass annual land-cover, optical, and radar checks; Tanager specifically tests the bright-desert NDBI failure mode | Met |
| Show useful output, not only model metrics | Dashboard, ranked zones, maps, GIS layers, notebook, and pilot workflow are included | Met |
| State transfer limits | The project distinguishes WorldCover agreement from field accuracy and identifies date, sensor, population, surface-temperature, and desert-confusion limits | Met |

## Files that add no new project evidence

- The two `geoai_lab_colab` notebooks have identical markdown and code. They differ only in notebook metadata; neither contains saved execution results.
- The two CSV datasets are standard classroom examples. They do not describe Riyadh, Earth observation, or the submitted model.
- The deeper-learning exercise uses an airborne 1992 Indiana scene. It teaches evaluation discipline but cannot be presented as evidence for this project.

## Optional training items not supplied

The current portal list also names:

- `ML Fundamentals - Notebook`;
- `Ghaf root - student project` slides; and
- `optical_data.zip`, which is needed only to reproduce the optional GDAL lab locally.

None of these is a submission requirement or a blocker. If Yusuf wants a completely archived training library, these are the remaining items to download. The project should not wait for them.

## Changes justified by this audit

- Make the seven public criteria and the five detailed-orientation headings visible as two overlapping official formulations.
- Make innovation, SDG alignment, and the cautious business path easier to find in the README.
- Add English-language, professional-content, and judging-opt-in checks to the submission checklist.
- Keep all supplied organizer training files outside the public repository.

No algorithm, result, city, user, or project claim was changed.
