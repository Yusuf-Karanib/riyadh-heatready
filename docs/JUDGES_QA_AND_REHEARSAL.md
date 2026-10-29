# Judge questions and rehearsal guide

**29 October update:** Yusuf presents alone. The current solo question pack is `docs/JUDGE_QUESTIONS_AND_ANSWERS.md`, with a matching PDF in `output/pdf/`. The owner assignments below describe the earlier two-person plan.

Riyadh HeatReady | Yusuf Karanib and Raed Mardoum | Live deck v6

## How to answer

Let the judge finish. Give the direct answer, then one reason or number. Stop after about 20-30 seconds and let them ask for more. The four-minute Q&A belongs to the whole team.

Yusuf leads questions about data, code, scoring, output and the demonstration. Raed leads questions about validation, limitations, differences and the proposed city test. Both must understand the user, result and main limitations.

If the question is unclear, say: "Do you mean the built-up model or the final ranking?" If you do not know: "We haven't tested that yet. The way we would check it is..." Describe a proposed test rather than a guessed result.

## Facts both presenters need

| Question | Answer to remember |
| --- | --- |
| Who is it for? | Municipal planning and heat-resilience staff |
| What does it help decide? | Which areas to inspect first |
| Where? | 168.3 km2 in southeast Riyadh |
| What result? | 67 eligible cells, 14 High, R05C10 first at 78.7 |
| What growth? | 13.82 km2 proposed, 3.74 km2 retained by extra checks |
| What score? | 40% heat, 30% population, 20% growth, 10% low vegetation |
| What model evidence? | 2021 WorldCover agreement: F1 0.88, IoU 0.78, balanced accuracy 0.89 |
| What comes next? | A comparison with real planning work and local evidence |

## Example of a short answer

Judge: "What does 78.7 mean?"

> It is a weighted score comparing that cell with the other eligible cells. Heat, population, growth and low vegetation contribute to it. It helps order inspections. It isn't a probability of illness.

The correction is relevant because the judge asked about the score. Avoid reading a long list of limitations in every answer.

---

## The first questions to practise

### 1. Explain the project briefly. Both

> HeatReady combines satellite evidence of growth, surface heat and vegetation with estimated population. It ranks one-kilometre areas in southeast Riyadh to help planning staff decide where to inspect first.

### 2. What problem are you solving? Yusuf

> The proposed problem is the effort of comparing separate maps before choosing inspection areas. We bring the layers together in one ranked view. Municipal interviews are still needed to confirm how well that fits their workflow.

### 3. What makes your entry different? Raed

> We check possible growth with optical and radar evidence and show the components behind each inspection priority. Our Tanager comparison also shows a desert case where one built-up index gives a misleading result. The methods are established. Our contribution is their use in this screening workflow.

### 4. What is your strongest result? Yusuf

> The working output is a ranked map and table of 67 eligible areas. Fourteen are High under our chosen rule. R05C10 ranks first at about 78.7. We also provide GIS files and a notebook that reproduces the scoring.

### 5. What would the user actually do? Raed

> Review the first areas on the list, compare them with local plans, and visit the places that need checking. Staff then decide whether an area needs a more detailed assessment or a suitable response.

### 6. What impact have you measured? Raed

> We have a working, documented analysis and a ranked output. We have not measured staff time savings or improvements in heat outcomes. A pilot would compare the ranking with the team's current process and record time, useful findings and errors.

Evidence to show: slide 3 for problem and answer, slide 4 for the result, slide 7 for the comparison, slide 8 for the proposed test.

---

## Data and dates

### 7. Why Riyadh, and why this part? Yusuf

> This part of Riyadh has overlapping open Sentinel, Landsat, annual land-cover, population and Tanager coverage. It offers a mix of built and desert surfaces for the case study. The study is one defined area, rather than evidence for the whole city.

### 8. Why do you need satellite data? Yusuf

> The growth, built-surface, vegetation and surface-temperature layers come from Earth observation. Population data alone cannot provide those measurements. Each source contributes a different part of the inspection ranking.

### 9. Did you use Satellite 813 or paid imagery? Yusuf

> This proof of concept uses open data. It includes an open Planet Tanager archive scene, which is different from Satellite 813 imagery. We did not use Satellite 813 or sponsored commercial imagery in the baseline.

### 10. Why mix 2018, 2021, 2023 and 2025? Yusuf

> Annual maps propose change from 2018 to 2023. The model is trained and tested using 2021 labels, then applied to 2018 and 2025 images. The 2025 image checks whether candidate change still looks built-up. Heat and population are 2025 context. These dates cannot establish an exact construction year.

### 11. Does the temperature represent the current city climate? Raed

> The heat layer is one Landsat surface-temperature observation from 10 May 2025. It gives a snapshot for this case study. More dates and weather context are needed to assess persistent heat patterns or conditions on the judging day.

### 12. Why is 13.82 different from 98.03 minus 85.39? Yusuf

> The subtraction gives net mapped built-area change, about 12.64 square kilometres. Candidate growth counts particular pixels that changed from non-built to built, after removing small groups. Other pixels can change in the opposite direction, so gross candidate growth and net change measure different things.

Evidence: slide 9 and config.json for dates, outputs/results_summary.json for areas.

### Extra question: How can the top cell have growth while its total built fraction falls? Yusuf

> The growth layer keeps a subset of pixels that pass our checks. Other pixels in the same cell can receive lower built-up predictions in 2025. Growth signals and whole-cell net change therefore differ. That disagreement is another reason for local review.

---

## The model and the growth checks

### 13. What model did you use? Yusuf

> A random forest with 260 trees. Its 13 inputs combine optical bands and indices with radar features. It learns built/unbuilt labels from WorldCover. The inspection score is a separate weighted calculation after that model.

### 14. How did you keep training and testing separate? Yusuf

> The west supplies training examples. A middle strip chooses the classifier cut-off. The east is held back for testing, with geographic gaps between strips. That reduces mixing of neighbouring training and test pixels. It does not remove shared errors in satellite-derived reference labels.

### 15. Why is 3.74 called confirmed growth? Yusuf

> It passed our confirmation rule. Annual maps must suggest growth, the 2025 model must classify it as built, and the built-up estimate must rise at least 0.10 from 2018. We remove tiny isolated groups too. Here "confirmed" means passing those checks, rather than survey confirmation.

### 16. Have you proved radar improves the result? Yusuf

> We tested the combined model. We have not reported a controlled optical-only versus optical-plus-radar comparison. Radar adds a different measurement, but an ablation test would be needed to quantify its contribution.

### 17. Why not use the built-up index alone? Raed

> In our Tanager comparison, likely-unbuilt ground had median narrow-band NDBI around 0.084, compared with 0.049 for established built land. A simple high-value threshold can confuse those surfaces here. This is a finding from the selected scene, rather than a universal threshold rule.

### 18. Why wasn't Tanager's cloud flag the main mask? Yusuf

> The beta flag marked about 54% of this bright scene. The analysis reports that issue and repeats the index comparison with flagged pixels removed. The unbuilt-versus-built median ordering remains, about 0.083 versus 0.042. That sensitivity check helps describe the limitation. Independent quality checking is still needed.

Evidence: src/run_analysis.py and outputs/tanager_summary.json. Slide 7 shows the comparison. The Tanager groups come from other satellite layers, so they do not supply independent material labels.

---

## The score and its boundaries

### 19. Why these weights? Yusuf

> They express our initial priorities: 40% surface heat, 30% population, 20% growth and 10% low vegetation. They are prototype assumptions. We would ask planning staff to review them and check how alternative weights change the top areas.

### 20. Why 1 km cells? Yusuf

> They match the coarse population layer and keep the output at an area-screening scale. The satellite analysis uses a 30 m grid, then aggregates to the cells. The result does not resolve individual buildings or people's exposure.

### 21. Why does R05C10 rank first? Yusuf

> It scores relatively highly across the four drivers. Its points are about 35.22 from heat, 18.36 from population, 15.82 from growth and 9.25 from low vegetation. Using unrounded values gives about 78.66, displayed as 78.7.

### 22. Why are exactly 14 areas High? Yusuf

> High starts at the 80th percentile of eligible scores. Applying that relative cut-off to these 67 cells gives 14 High cells. The label depends on the chosen rule and the comparison set, rather than an absolute danger measurement.

### 23. What if an established neighbourhood is very hot? Raed

> A cell needs some retained growth to enter this ranking, so an established neighbourhood with no detected growth can be excluded. This prototype screens growth areas. A broader heat-priority service would need to include established neighbourhoods and test that wider scope.

### 24. Are heat and vegetation being counted twice? Yusuf

> They can be related. We keep them visible as separate drivers, but have not quantified how that correlation affects the ranking. We would test alternatives, including reducing or removing the vegetation component, before setting operational weights.

### 25. Is the first area definitely more important than the second? Raed

> The first two scores are about 78.7 and 78.2. That small gap does not establish a meaningful real-world difference. We would review them as close candidates and test how changes in weights and input uncertainty affect their order.

Evidence: outputs/priority_zones.csv. Population's log step preserves order, so percentile ranking is unchanged by it. Do not credit the log transform with changing these ranks.

---

## Validation and difficult scientific questions

### 26. Does F1 0.88 mean the whole project is 88% accurate? Raed

> It measures built-up classification agreement with WorldCover in the eastern 2021 test area. It balances precision and recall. It does not measure final ranking accuracy, health outcomes, or performance everywhere.

### 27. Why isn't WorldCover independent ground truth? Raed

> WorldCover is itself a satellite-derived product using Sentinel-1 and Sentinel-2. Our model uses those sensors too, so the products can share errors. The separate test area helps with geographic separation. Local reference labels are still needed to test real accuracy.

### 28. What do the other two metrics mean? Raed

> IoU 0.78 describes overlap between our predicted built pixels and the reference built pixels. Balanced accuracy 0.89 averages performance for built and unbuilt classes. The test has 36,156 reference pixels.

### 29. Did you validate the 2018-to-2025 model transfer? Yusuf

> The reported spatial test is for 2021. We apply that model to the other years, but have not separately established their accuracy with field labels. Changes in imagery or surface conditions could affect those predictions. A labelled test in each year would address that uncertainty.

### 30. Have you measured heat-island intensity or health risk? Raed

> We have a surface-temperature layer and population context. We have not calculated an urban-versus-rural temperature difference or built a validated health-risk model. Weather, vulnerability, worker locations and repeated observations would be needed for those wider questions.

### 31. What is your biggest limitation? Raed

> The final inspection ranking has not yet been tested with municipal users or field observations. The classifier test shows agreement with a satellite reference, while the value of the ranking remains a question for the pilot.

Evidence: slides 6 and 10, outputs/validation_metrics.json. Feature importance describes how the forest used a feature in its splits. It does not show what causes construction or prove that removing a feature would preserve performance.

---

## Implementation, team and future work

### 32. Can we reproduce it? Yusuf

> The repository includes pinned requirements, source settings, example inputs and outputs, and full processing code. The sample notebook recalculates scores from committed driver values. It does not reprocess every satellite image. The full pipeline does that separately and needs data access and downloads.

### 33. Is the dashboard live and interactive? Yusuf

> It is a self-contained static report. It displays the generated evidence and ranking. Updating observations requires rerunning the processing. CSV, GeoJSON and GeoTIFF files are separate outputs in the repository.

### 34. What has each team member done? Both

> Yusuf leads the project and presents the data, scoring and demonstration. Raed presents validation interpretation and the proposed city test.

Then describe actual completed work if asked. Studying and reviewing are real activities once completed. Do not assign invented coding, interviews or fieldwork to either person.

### 35. How did you use AI? Yusuf

> We used AI tools for coding and documentation. The inputs, processing and recorded outputs are available for inspection. I can explain the workflow and its limitations.

Use the final sentence once you can do so. If asked who wrote the code, answer directly: "AI assistance generated much of the code. My responsibility is to understand it, check the evidence and explain the result." State checks you actually performed.

### 36. How would you prove it helps? Raed

> Have staff review the same area with their current process and with HeatReady. Compare time, useful findings and errors, including some lower-ranked cells. Agree on weights, adjust the method, and repeat in another area. We have not run that pilot yet.

### 37. Who will buy it, and what will it cost? Raed

> A municipal pilot would test workflow fit, update cost and procurement requirements. We do not yet have a customer, agreed price or operating-cost benchmark. Those need evidence before a commercial offer.

Evidence: README.md, notebooks/02_main_analysis.ipynb, build_all.ps1 and source/output folders. Dataset licences are separate. Public GitHub access does not itself give the code an open-source licence.

---

## Rehearse in your own words

Allow about two hours for the first preparation session. Repeat weak parts afterward. Reading the material is different from being ready to present.

1. First 15 minutes: both explain the user, question, result and limitations without notes.
2. Next 30 minutes: Yusuf learns slides 1-5. Raed learns slides 6-8 and the metrics.
3. Next 15 minutes: Yusuf practices the demonstration and fallback. Raed explains the confusion matrix and pilot in plain words.
4. Next 20 minutes: rehearse together with a timer. Mark where a term or transition causes hesitation, then correct that section.
5. Next 25 minutes: take turns as a judge. Ask questions 1-6 first, then choose difficult ones at random.
6. Last 15 minutes: give one complete pitch and a four-minute Q&A. Record it if possible. Listen for vague claims or rushed explanations.

### Readiness check

- Both can give the short project answer without reading.
- Yusuf can explain the source-to-output steps and the 78.7 score.
- Raed can explain the three metrics and why the ranking needs testing.
- Both can answer the first six questions in under 30 seconds each.
- The full pitch, including demo and handoff, finishes within 6:45 at your normal pace.
- Repeat a successful timed run so one lucky fast reading is not the only evidence.

### Recover from a delay

Use the short slide 5 and slide 8 paragraphs in your own guides. If the report window fails, use slide 4. If interrupted by a question, answer briefly and return to the next point. Follow the moderator's timing instructions.

### Before the call

Open the v6 deck, matching PDF and report. Put the browser at Decision output. Check camera, microphone and screen sharing. Close private tabs and notifications. Agree who changes slides and keep one person in control. The team introduction is now slide 1 and the project question is slide 2.

Your confirmed pitch is Thursday, 29 October 2026 at 09:45 UAE time. Opening remarks are Wednesday, 28 October, 09:30-10:15 UAE time. Upload the final presentation through the platform before 22:00 UAE time on Monday, 26 October. The email requires this upload even if a previous version was emailed. Save its confirmation.

Join shortly before your pitch and wait in the lobby. A 15-minute schedule slot contains eight minutes of presentation, four minutes of questions, and three minutes for scoring and transition. Follow the moderator when asked to leave. Keep the invitation links in your email or local work/finals-oct26/ACCESS.md. Upload completion has not yet been confirmed.

---

## Evidence to open during preparation

These are study references. You do not need to display code during the eight-minute pitch.

| Evidence | Where it is in the repository |
| --- | --- |
| Latest live slides | slides/Riyadh_HeatReady_Final_Live_Pitch_v6.pptx |
| Matching backup | output/pdf/Riyadh_HeatReady_Final_Live_Pitch_v6.pdf |
| Static report | outputs/dashboard.html |
| Areas and summary numbers | outputs/results_summary.json |
| Ranked cells and score parts | outputs/priority_zones.csv |
| Validation and confusion matrix | outputs/validation_metrics.json |
| Tanager comparison and mask check | outputs/tanager_summary.json |
| Dates, area and source item IDs | config.json |
| Full method | src/run_analysis.py |
| Quick scoring example | notebooks/02_main_analysis.ipynb |
| Dataset attribution | docs/DATA_AND_LICENSES.md |

### Official technical references checked

- Metrics: https://scikit-learn.org/stable/modules/model_evaluation.html
- Random forest: https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html
- WorldCover's Sentinel-based reference: https://esa-worldcover.org/en
- Surface temperature: https://www.usgs.gov/landsat-missions/landsat-collection-2-surface-temperature

Project numbers come from the committed outputs. External references explain the products and methods, rather than independently validating the project.

### What confidence means

You can explain how an input becomes an output, point to the evidence, and describe a limitation without guessing. If asked for an experiment you have not done, say so and explain how you would test it.
