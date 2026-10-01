# Yusuf's study plan — learn from the finished answer

Start this only after the submission package is stable. Each lesson uses the completed project, not an empty notebook.

## Lesson 0 — What are the actual rules?

Open:

- `project/docs/OFFICIAL_RESEARCH_AUDIT.md`

Learn:

- the 11 October deadline;
- the seven judging criteria;
- what is confirmed and what still waits for the submission form;
- why the live official platform overrides older GitHub text when they conflict.

Finish when you can name the seven criteria and the deadline without guessing.

## Lesson 1 — What did we build?

Open:

- `project/outputs/dashboard.html`
- `project/docs/PROJECT_BRIEF.md`

Learn:

- the problem;
- the intended user;
- the decision;
- why Riyadh was selected;
- why the output is a screening map.

Finish when you can give the 20-second answer without reading.

## Lesson 2 — What does each dataset do?

Open:

- `project/docs/DATA_AND_LICENSES.md`
- `project/outputs/analysis_overview.png`

Learn one sentence for each source:

- Sentinel-2 sees reflected light.
- Sentinel-1 adds radar structure.
- Annual land cover proposes change.
- Landsat measures land-surface temperature.
- WorldPop estimates population.
- Tanager provides many narrow spectral bands.

Finish when you can explain why no single source is enough.

## Lesson 3 — How does the method work?

Open:

- `project/docs/METHODOLOGY.md`
- `project/docs/WEEK2_TRAINING_REVIEW.md`
- `project/outputs/validation.png`

Learn:

- training, tuning, and spatial testing;
- why two sources must confirm growth;
- what F1 and IoU mean;
- why this is not field accuracy.

Finish when you can explain the full method in six simple steps.

## Lesson 4 — What did we find?

Open:

- `project/outputs/decision_map.png`
- `project/outputs/annual_built_area_timeseries.png`
- `project/outputs/tanager_material_analysis.png`
- `project/outputs/results_summary.json`

Learn the four main numbers:

- 3.74 km² conservative confirmed-growth signal;
- 49.02 °C mean land-surface temperature for the observation;
- F1 0.88;
- IoU 0.78.

Learn the time-series result: mapped built-up area rose overall from 85.39 km² in 2018 to 98.03 km² in 2023, but it dipped in 2022. That dip is why the chart is supporting evidence rather than an exact construction record.

Learn the main surprise: likely-unbuilt desert had higher median narrow-band NDBI than established built land, so NDBI alone is unsafe.

Finish when you can state every number with its limitation.

## Lesson 5 — Present and answer questions

Open:

- `project/docs/PRESENTER_GUIDE.md`
- `project/docs/AI_ASSISTANCE_LOG.md`

Practice:

1. 20-second answer.
2. 60-second answer.
3. Three-minute pitch.
4. Judge questions.
5. Honest AI disclosure.

Finish when you can answer without pretending that surface temperature is air temperature, WorldPop is a census, Tanager is Satellite 813, or WorldCover agreement is field truth.

## Lesson 6 — Explain the product path honestly

Open:

- `project/docs/PROJECT_BRIEF.md`
- `project/docs/PRESENTER_GUIDE.md`

Learn:

- the potential adopter;
- what files and dashboard are delivered;
- what the first municipal pilot would test;
- why there is no claimed customer, price, revenue, or proven time saving yet.

Finish when you can explain a plausible pilot without inventing business results.
