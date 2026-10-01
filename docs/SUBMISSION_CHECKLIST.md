# Submission checklist

The current official deadline is **11 October 2026 at 11:59 PM in the team creator's timezone**. The official submission form is not yet open in the supplied portal evidence, so this checklist separates completed internal work from portal-dependent items. Internal readiness target: **10 October**.

## Official eligibility checks

- [x] Registration approved by the organizers.
- [x] Official challenge assigned in the Cockpit.
- [x] Portal team members are registered and identified.
- [ ] Yusuf confirms that the registered team still meets the rule that at least 30% of members are age 35 or younger.
- [ ] Every required project section is completed after the submission form opens.
- [ ] Submission is in English and professional.
- [ ] Every required file is uploaded under the final instructions.
- [ ] Submission requirements are accepted and the team opts into judging.

## Technical package — completed

- [x] One clear problem, user, decision, and AOI.
- [x] Exact item IDs and dates recorded.
- [x] Open-data PoC approach confirmed by the organizer on 27 September.
- [x] Data feasibility check passed: 38 checks.
- [x] Reproducible optical-radar built-up model.
- [x] Separate annual land-cover change proposal.
- [x] Six-year annual mapped built-up trend for 2018–2023.
- [x] Landsat land-surface temperature layer.
- [x] WorldPop exposure layer.
- [x] Conservative confirmed-growth layer.
- [x] Transparent 1 km priority score.
- [x] Spatial holdout validation.
- [x] Open Planet Tanager spectral analysis.
- [x] Decision map, evidence figures, CSV, GeoJSON, and GeoTIFF outputs.
- [x] Self-contained HTML dashboard.
- [x] Automated verification report: 80 checks passed.
- [x] ZIP integrity and every packaged-file hash verified against the package manifest.

## Explanation package — completed

- [x] Project brief.
- [x] Beginner methodology.
- [x] Data and licence record.
- [x] Presenter guide and judge questions.
- [x] Limitations stated next to results.
- [x] AI-assistance log started.

## Official judging alignment — completed internally

- [x] Problem definition.
- [x] Technical soundness.
- [x] Purposeful EO and hyperspectral use.
- [x] Clear product and delivery model.
- [x] Innovation explained without claiming a new satellite index.
- [x] Impact and regional/SDG alignment.
- [x] Short business-viability hypothesis with no invented customer, price, or revenue.

## Yusuf must complete before submission

- [ ] Read the project brief and explain the user and decision in his own words.
- [ ] Open the dashboard and understand each card and map.
- [ ] Explain why NDBI alone fails in bright desert.
- [ ] Explain why land-surface temperature is not air temperature.
- [ ] Explain the validation caveat.
- [ ] Review the AI-assistance disclosure and correct anything incomplete.
- [ ] Decide whether the project name will remain "Riyadh HeatReady."
- [ ] Decide whether the code will be published and under which licence.

## Portal-dependent items — waiting for official release

- [ ] Confirm required form fields and word limits.
- [ ] Confirm allowed upload types and maximum file sizes.
- [ ] Confirm whether a repository link must be public or private.
- [ ] Confirm whether a video, live demo, report, or slide deck is required.
- [ ] Confirm pitch length and question time.
- [ ] Confirm the required AI disclosure wording.
- [ ] Recheck that the Cockpit still shows the same deadline and team details immediately before submission.
- [ ] Enter every field and upload every required file.
- [ ] Test every link in a signed-out/private window when appropriate.
- [ ] Save submission screenshots and confirmation.

## Suggested small submission archive

Include:

- `README.md`
- `config.json`
- `requirements.txt`
- `src/`
- `docs/`
- `outputs/dashboard.html`
- `outputs/decision_map.png`
- `outputs/analysis_overview.png`
- `outputs/annual_built_area_timeseries.png`
- `outputs/annual_built_area_timeseries.csv`
- `outputs/validation.png`
- `outputs/tanager_material_analysis.png`
- `outputs/priority_zones.csv`
- `outputs/results_summary.json`
- `outputs/verification_report.md`
- `outputs/manifest.json`

Exclude:

- `.venv/`
- `data/raw/`
- `data/cache/`
- the 856 MB Tanager HDF5 file
- downloaded starter repository files
- signed URLs, credentials, or portal screenshots containing private contact details
- archived experiments
