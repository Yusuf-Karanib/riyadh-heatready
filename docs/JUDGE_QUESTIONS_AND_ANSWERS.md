# Riyadh HeatReady: judge questions and answers

**Solo preparation for Yusuf Karanib. Based on the v6 presentation, its figures and notes, the recorded outputs and the processing code.**

These are simulated questions a reviewer could generate after reading your presentation. They are not the judges' actual questions. They deliberately challenge weak claims as well as ask ordinary questions.

## How to use this

Read the question, cover the answer and explain it aloud. Then check the answer. Learn the meaning rather than memorising every sentence. Give the short answer first. Use the follow-up only if asked. You have four minutes for the whole Q&A.

Start with questions **1, 3, 6, 7, 12, 22, 26, 27, 36 and 47**. Then practise the rest in random order. Yusuf answers all sections because Raed cannot attend.

## Numbers to know

| Fact | Remember |
| --- | --- |
| User and decision | Planning staff deciding where to inspect first |
| Case study | 168.3 km2 in southeast Riyadh |
| Candidate / retained growth | 13.82 / 3.74 km2 |
| Ranking | 67 eligible cells; 14 labelled High |
| First cell | R05C10, 78.7 points |
| Weights | Heat 40%, population 30%, growth 20%, low vegetation 10% |
| Built-up model test | F1 0.88; IoU 0.78; balanced accuracy 0.89 |
| Test reference and year | WorldCover 2021; 36,156 eastern test pixels |
| Heat observation | Landsat surface temperature, 10 May 2025 |
| What remains untested | Field accuracy and usefulness to real planners |

Evidence labels below refer to repository files. They let you trace an answer during study. You do not need to open code during the pitch.

---

## Problem and intended user

### 1. Explain your project in twenty seconds

**Answer:** HeatReady combines satellite evidence of growth, surface heat and vegetation with estimated population. It ranks one-kilometre areas in southeast Riyadh to help planning staff choose where to inspect first.

**If asked what happens next:** Staff compare the suggested areas with local plans and conditions, then decide whether an assessment or action is needed.

### 2. What is the actual problem?

**Answer:** Our proposed problem is the effort of comparing separate maps before deciding where to inspect. We bring those layers into one ranked view. We still need user interviews to confirm how well this matches real planning work.

**If asked for proof of demand:** We have not interviewed municipal users or measured demand. That is a gap the proposed pilot must address.

### 3. What is new if all these datasets and methods already exist?

**Answer:** The contribution is the screening workflow. Annual maps suggest growth, optical and radar evidence check it, and four visible drivers set the inspection order. The Tanager comparison examines a specific desert-confusion problem. We are using established methods.

**If asked for a new algorithm:** We do not claim one, or superiority over every existing planning tool.

### 4. Why Riyadh and why this small area?

**Answer:** The selected area has overlapping open-data coverage, including Tanager, and a mix of built and desert surfaces. It keeps the case study manageable. It covers 168.3 square kilometres in southeast Riyadh, rather than the whole city.

**If asked whether it generalises:** Another area needs fresh processing and validation. We have not established city-wide or cross-city performance.

### 5. Why not just give planners a temperature map?

**Answer:** A temperature map identifies hot surfaces. Our question also includes growth, estimated population and vegetation, so the hottest area alone may not rank first. We would compare HeatReady with a heat-only approach in a user pilot.

**If asked whether you beat that baseline:** We have not demonstrated better inspection outcomes than a heat-only map.

Evidence: slides 2, 3, 7 and 8; README.md; docs/METHODOLOGY.md.

---

## The result and its score

### 6. What is the strongest result you can show now?

**Answer:** A working ranked map and table of 67 eligible areas, with fourteen labelled High. R05C10 ranks first at about 78.7. We provide the score components and GIS outputs so the result can be examined.

**If asked about impact:** That is a completed analytical output. We have not measured improvements to planning decisions or heat outcomes.

### 7. What does 78.7 actually mean?

**Answer:** It is a weighted score comparing R05C10 with the other eligible areas. The four components are relative ranks for heat, population, growth and low vegetation. It indicates inspection priority under our chosen rules.

**If asked whether it means 78.7% danger or accuracy:** It does not. It is neither a health probability nor a model-accuracy percentage.

### 8. Can you calculate the score for that real area?

**Answer:** Its approximate component points are 35.22 for heat, 18.36 for population, 15.82 for growth and 9.25 for low vegetation. The unrounded calculation gives 78.6567, displayed as 78.7.

**If asked why the rounded parts add to 78.65:** We calculate with the original values before rounding the final score. Rounding each part separately changes the last decimal.

### 9. How do degrees Celsius and population become comparable?

**Answer:** Each driver becomes a percentile rank among the 67 eligible cells. Higher surface heat, more population, more retained growth and less vegetation increase the relevant component. We multiply those components by the weights, add them, and multiply by 100.

**If asked about ties:** Equal driver values receive their average rank. The population log step preserves order, so it does not change its percentile ranks.

### 10. Why are fourteen areas High? Is that a safety threshold?

**Answer:** High starts at the 80th percentile of eligible scores. That rule produces fourteen High cells in this dataset. It is a relative label chosen for the prototype.

**If asked whether High means unsafe:** The label has no validated medical or regulatory meaning. A cell can rank highly within one set without being comparable to another city's cells.

Evidence: slide 4; outputs/priority_zones.csv; src/run_analysis.py, percentile_component and priority calculation.

---

## Where the ranking can mislead

### 11. Why give heat 40% and population 30%?

**Answer:** They are our starting priorities for the prototype. Growth receives 20% and low vegetation 10%. The weights make the choices visible, but we have not established that these are the best values for real planning work.

**If asked about sensitivity testing:** We have not reported a full weight-sensitivity analysis. We would vary the weights and compare changes in the top areas.

### 12. Does your ranking leave out old but very hot neighbourhoods?

**Answer:** Yes. A cell needs retained growth to qualify. An established area without detected growth can therefore be excluded even if it is very hot. This version addresses growth areas within the case-study boundary.

**If asked whether excluded cells are safe:** Exclusion does not mean low heat or low need. A broader service would need to score those areas too.

### 13. Is first place meaningfully better than second?

**Answer:** The first scores are about 78.7 and 78.2. Such a small gap does not establish a meaningful real-world difference. I would treat them as close candidates for local review.

**If asked for confidence intervals:** We have not quantified score uncertainty or rank confidence intervals. We should examine input uncertainty and weight changes before treating the order as firm.

### 14. Are heat and vegetation being counted twice?

**Answer:** They can be related. We show them separately, but have not measured how their correlation affects the ranking. A pilot should compare alternatives, including reducing or removing the vegetation component.

**If asked whether the score is causal:** It does not show that growth caused heat, or predict how much a cooling measure would reduce it.

### 15. Why one-kilometre cells instead of individual buildings?

**Answer:** They suit early area screening and the approximately one-kilometre population layer. We process satellite evidence on a 30-metre grid before aggregation. The result is too coarse to choose an action for an individual building.

**If asked about grid boundaries:** Boundaries can affect rankings. We have not reported alternative-grid tests. Edge polygons are clipped, and estimated population is adjusted for the fraction inside the area.

Evidence: slides 3, 4 and 6; outputs/priority_zones.csv; eligibility and aggregation in src/run_analysis.py.

---

## Data and dates

### 16. What does each satellite source contribute?

**Answer:** Annual land-cover maps suggest growth. Sentinel-2 provides optical and vegetation measurements, while Sentinel-1 adds radar structure. Landsat supplies surface temperature. WorldPop adds estimated population. Tanager provides a separate descriptive spectral comparison.

**If asked about Satellite 813:** We did not use it. The baseline uses open data, including an open Tanager archive scene. Tanager and Satellite 813 are different sources.

### 17. Why mix 2018, 2021, 2023 and 2025?

**Answer:** The annual maps propose change from 2018 to 2023. The model learns from 2021 labels, then checks 2018 and 2025 images. The later image checks whether the candidate locations still look built-up. Heat and population add 2025 context.

**If asked for the construction date:** These comparisons cannot establish the exact construction year. This is a historical case study rather than live monitoring.

### 18. Have you measured the urban heat island or people's heat risk?

**Answer:** We measured a land-surface-temperature layer and combined it with population context. We have not measured an urban-versus-rural temperature difference or validated a personal health-risk model.

**If asked what is missing:** Repeated heat observations, weather and vulnerability data, worker locations and local evidence would be needed for those wider claims.

### 19. Is the temperature representative? What about population?

**Answer:** The heat layer comes from one Landsat observation on 10 May 2025. The area's mean surface temperature was about 49.0 degrees Celsius. WorldPop provides modelled residents, which can miss daytime workers in industrial areas.

**If asked whether this describes judging-day conditions:** It does not. More dates and local observations are needed to assess persistent heat and current exposure.

### 20. Does resizing everything to 30 metres create better detail?

**Answer:** Aligning layers makes their locations comparable. It does not create new detail in a coarser source. The code uses different resampling methods for categories, continuous values and population counts, then aggregates evidence for one-kilometre decisions.

**If asked for the map system:** The processing grid uses UTM zone 38N, EPSG:32638. The configured analysis resolution is 30 metres.

Evidence: slides 5, 6 and 9; config.json; docs/METHODOLOGY.md; outputs/results_summary.json.

---

## The model and the growth rule

### 21. What machine-learning model did you use, and why?

**Answer:** A random forest with 260 trees combines thirteen optical and radar features. It learns built/unbuilt labels from WorldCover. It is a manageable baseline for these numerical inputs. The final inspection score is a separate weighted calculation.

**If asked why not deep learning:** We have not benchmarked architectures. We do not claim that the random forest is the best possible model.

### 22. What does your slide mean by confirmed growth?

**Answer:** It means passing our processing rule. Annual maps must suggest non-built-to-built change, the 2025 model must exceed its built-up cut-off, and the estimated built-up probability must rise by at least 0.10 from 2018. Small isolated groups are removed.

**If asked whether someone visited those sites:** We have not field-confirmed them. The 3.74 square kilometres is retained growth signal under those rules.

### 23. How did you choose the model cut-off?

**Answer:** We chose it using F1 in the separate middle tuning strip. The selected cut-off was 0.42. The eastern test strip was kept apart from that threshold choice.

**If asked about the other rules:** The 0.10 probability-rise rule and minimum six connected 30-metre pixels are prototype choices. Their effect needs sensitivity testing. Model scores are not proven calibrated probabilities.

### 24. Did you throw away real growth when 13.82 became 3.74?

**Answer:** That is possible. Requiring agreement removes many candidate pixels, but stricter rules can also miss real development. We have not measured how much rejected candidate growth was actually real.

**If asked why not claim a false-positive reduction rate:** We lack independent labels for retained and rejected growth. Smaller output alone does not prove better real accuracy.

### 25. Have you proved that radar improves the model?

**Answer:** We tested the combined optical-and-radar model. We have not reported a controlled optical-only comparison. Radar supplies a different measurement, but its added performance needs an ablation test.

**If asked what that test means:** Train comparable models with and without radar, keep the same evaluation setup, then compare their results on the same held-out labels.

Evidence: slide 5; model fitting, choose_threshold and growth rules in src/run_analysis.py; outputs/validation_metrics.json.

---

## What the accuracy evidence means

### 26. Does F1 0.88 mean HeatReady is 88% accurate?

**Answer:** It measures built-up classification agreement with WorldCover in the eastern 2021 test area. F1 combines precision and recall. It does not measure final-ranking accuracy, health outcomes or performance everywhere.

**If asked for the ingredients:** Precision was about 0.884 and recall 0.873. Their harmonic mean is F1, about 0.878, displayed as 0.88.

### 27. Is WorldCover independent ground truth?

**Answer:** It is a satellite-derived reference, rather than surveyed truth. It also uses Sentinel-1 and Sentinel-2, so it can share errors with our inputs. Geographic separation helps test a different location, but does not remove shared source errors.

**If asked for a stronger test:** Use independent local labels or field observations, covering both built and unbuilt surfaces.

### 28. What do overlap 0.78 and balanced accuracy 0.89 mean?

**Answer:** Intersection over union divides correctly matched built pixels by all pixels labelled built by either source. Balanced accuracy averages the success rates for built and other pixels. Both describe agreement in this test.

**If asked why report several metrics:** A single number can hide different error types. These metrics show different aspects of the same comparison, rather than three independent experiments.

### 29. How did you separate training, tuning and testing?

**Answer:** The west, roughly the first 55% of image columns, supplies training. Columns from 60% to 75% tune the cut-off. The final 20% in the east tests it. Gaps separate those strips.

**If asked whether leakage is impossible:** Spatial separation reduces mixing of neighbouring examples. It does not eliminate spatial correlation or shared reference errors. This is one geographic split.

### 30. Can you explain the confusion matrix?

**Answer:** Of 36,156 test pixels, 13,994 matched the built reference and 18,281 matched the other class. There were 1,845 predictions of built where the reference said other, and 2,036 missed reference-built pixels.

**If asked whether those are 36,156 independent field checks:** They are neighbouring satellite pixels. They are not that many independent surveyed sites.

Evidence: slides 6 and 10; outputs/validation_metrics.json. Rows are reference classes; columns are predicted classes, both ordered Other, Built-up.

---

## Difficult checks on the evidence

### 31. Does the 2021 test validate predictions for 2018 and 2025?

**Answer:** It does not establish their accuracy. We apply the 2021 model to the other years, but changing imagery and surfaces can change performance. We have not separately validated those years against independent labels.

**If asked what reduces the problem:** We use May observations and apply documented image corrections. Those processing steps help comparability but do not replace temporal validation.

### 32. Why isn't candidate growth equal to 98.03 minus 85.39?

**Answer:** That subtraction gives about 12.64 square kilometres of net mapped built-area increase. The 13.82 candidate value counts particular non-built-to-built pixels after small-group filtering. Reverse classifications and filtering mean the two quantities differ.

**If asked about the 2022 dip:** Annual products can classify pixels differently between years. We do not treat the trend as an exact construction register.

### 33. How can R05C10 have growth but a lower total built fraction in 2025?

**Answer:** The retained growth layer is a subset of pixels passing our growth checks. Other pixels in the same cell can receive lower built-up predictions in 2025. A cell can therefore have retained growth pixels and lower total predicted built fraction.

**If asked whether this is a concern:** Yes. It highlights disagreement and uncertain temporal predictions. It is another reason to inspect locally rather than call this net construction.

### 34. Does feature importance prove the model understands buildings?

**Answer:** It describes how the fitted random forest used features in its splits. It does not prove a physical cause or quantify the performance lost if a feature were removed.

**If asked for better evidence:** Compare controlled model variants and independent labels. We have not reported that full comparison.

### 35. Are you mapping land use, or only land cover?

**Answer:** The classifier mainly identifies built surfaces and other cover. It does not establish whether a building is a home, warehouse or school. Those uses need local records or additional labels.

**If asked why that matters:** Different uses imply different people and exposure. Our inspection ranking is a starting point before that local information is added.

Evidence: outputs/results_summary.json; outputs/priority_zones.csv; outputs/validation_metrics.json; src/run_analysis.py.

---

## The Tanager comparison

### 36. What exactly did Tanager show?

**Answer:** In our selected scene and surface groups, likely-unbuilt ground had median narrow-band NDBI around 0.084, higher than established built land at about 0.049. That warns against treating a high built-up index as proof of buildings here.

**If asked what NDBI means:** It compares short-wave and near-infrared reflectance. In this scene the index can confuse bright unbuilt surfaces with built land.

### 37. Did Tanager validate the growth or prove your model was better?

**Answer:** It is one observation from 15 May 2025, so it cannot independently prove change over time. The surface groups come from other satellite products. This is a descriptive comparison, rather than independent validation.

**If asked whether you identified roof materials:** We did not establish specific materials using field spectra or independently labelled examples.

### 38. Your cloud mask flagged 54%. Why wasn't it your main mask?

**Answer:** The beta mask flagged much of this bright urban/desert scene. The main descriptive comparison used no-data and cirrus masks, and reported that concern. We repeated the index comparison excluding every beta-flagged pixel.

**If asked whether that proves the flagged pixels were clear:** It does not. The sensitivity check tests one comparison under stricter masking. It does not independently resolve every quality flag.

### 39. What happened when you used the stricter mask?

**Answer:** The median order stayed the same: likely-unbuilt about 0.083, growth about 0.072 and established built about 0.042. However, only 165 growth pixels remained, compared with 1,247 established-built and 17,251 likely-unbuilt pixels.

**If asked for the conclusion:** The narrow index warning survived that check. The small retained growth sample limits wider conclusions.

### 40. Is Tanager part of the final score, or just decoration?

**Answer:** Tanager does not set the four score components. It investigates a specific interpretation risk: bright-desert confusion in a built-up index. The core ranking can run without it.

**If asked whether it improves classification accuracy:** We have not measured a model-accuracy gain from adding Tanager. Its contribution here is the documented diagnostic comparison.

Evidence: slides 5 and 7; outputs/tanager_summary.json; src/analyze_tanager.py; config.json.

---

## Implementation and reproducibility

### 41. Is the demonstration live and interactive?

**Answer:** It is a self-contained static HTML report displaying generated maps and tables. It has no live filtering or automatic data feed. Updating the evidence means rerunning the processing. CSV, GeoJSON and GeoTIFF are separate outputs.

**If the browser fails:** The same result is visible on slide 4, and the separate output files remain available.

### 42. Can a judge reproduce the work?

**Answer:** The repository includes pinned requirements, exact source settings, example inputs and outputs, the processing scripts and a sample notebook. The notebook recalculates scores from committed driver values without credentials.

**If asked whether the notebook rebuilds every satellite image:** It does not. The full processing pipeline does that separately and needs downloads and source access.

### 43. What would a full rerun require?

**Answer:** The documented setup uses Python 3.12 and pinned dependencies. The full build checks sources, processes the scenes, runs the Tanager comparison, rebuilds outputs and checks them. Its first run includes an approximately 856 MB Tanager scene download.

**If asked for exact runtime or cost:** We have not established a general hardware/runtime or operating-cost benchmark. Open inputs still require processing resources.

### 44. How do we inspect the score rather than trust your chart?

**Answer:** Open priority_zones.csv to see each cell's driver components and final score. Recalculate 100 times the weighted sum. The summary and validation JSON files expose the reported areas and confusion matrix, while the code records the processing rules.

**If asked whether automated checks prove usefulness:** They can check calculations and output consistency. They do not replace independent reference data or user testing.

### 45. Did you use AI to make this?

**Answer:** Yes. AI tools assisted with code and documentation. The repository records the inputs, method and results for inspection. I can walk through how an input becomes a score and explain the limits.

**If asked who wrote the code:** AI assistance generated much of the code. Describe your own work and checks accurately. Do not claim manual authorship, fieldwork or experiments you did not perform. Practise the explanation before relying on it.

Evidence: README.md; requirements.txt; build_all.ps1; notebooks/02_main_analysis.ipynb; source and output folders. Dataset terms and attribution are recorded in docs/DATA_AND_LICENSES.md.

---

## Team, impact and next steps

### 46. Why are you presenting alone? What did each member do?

**Answer:** Raed is unable to attend, so I am presenting for our team. My pitch responsibility covers the problem, data, scoring and demonstration. Raed's assigned focus is validation interpretation and the proposed city test. I am covering those sections today.

**If asked about completed individual contributions:** Describe only actual work. Assigned roles do not establish that either member coded, interviewed users or performed field checks.

### 47. What is your biggest weakness?

**Answer:** The final ranking has not yet been tested with municipal users or independent field observations. We have a working output and a classifier reference-agreement test. We still need evidence that the list helps people choose useful inspections.

**If asked why continue:** The prototype is ready for that focused test. We can compare it with current practice and a simple baseline before expanding it.

### 48. How would you run that test properly?

**Answer:** Agree with planning staff on useful findings, false alarms and time taken. Compare their usual screening with HeatReady on the same task, check the top five and some lower-ranked areas, and review local evidence. Then adjust and repeat elsewhere.

**If asked whether it is already planned with a municipality:** It is proposed. No municipal partner or completed pilot is claimed.

### 49. Who pays, what does it cost, and how would it scale?

**Answer:** A municipal pilot would test workflow fit, update cost and procurement needs. A supported service or local deployment could follow if useful. We have no agreed customer, price, revenue or proven demand.

**If asked for the immediate development step:** Test the need first, then add repeated heat observations, local exposure information and evaluated weight choices. Another city needs its own validation.

### 50. What happens if your ranking is wrong?

**Answer:** Staff could waste inspection effort or miss a more important area. The output should guide review before any action. The pilot needs to measure both false alarms and missed priorities, including areas excluded by the growth rule.

**If asked what success would look like:** More useful findings for a given inspection effort, without unacceptable misses. Staff should agree the measures and targets before the trial. We have not measured that outcome yet.

Evidence: slide 8; README.md; docs/METHODOLOGY.md. Raed's supplied student background supports the introduction, not invented claims about completed tasks.

---

## Practise a four-minute judge session

Use a timer. Read each question aloud, then answer without reading the prepared response. The question itself uses time too. Stop at four minutes even if you have not finished the list.

Your pitch receives eight minutes, followed by four minutes of questions. The 15-minute booking includes organiser scoring and transition time.

| Round | Questions |
| --- | --- |
| First | 1. Explain it; 7. What does 78.7 mean; 26. What does F1 test; 48. How would you test usefulness |
| Tougher | 12. Excluded hot areas; 27. Shared reference errors; 31. Transfer across years; 45. AI use |
| Follow-up pressure | 11. Weight evidence; 13. Close scores; 38. Cloud mask; 47. Biggest weakness |

Aim for about 20-30 seconds per first answer. Do not recite every limitation after every question. Answer what was asked, then stop.

## If you freeze

If the question is unclear:

> Do you mean the built-up model, or the final inspection ranking?

If you have not done the requested test:

> We haven't tested that yet. The way I would check it is...

Then name a relevant test. Do not guess a result.

If you do not remember an exact number:

> I don't want to give you an incorrect exact figure. The recorded value is in our output file. The result it supports is...

Explain the result you do know. Offer to open the relevant appendix if useful.

## Six terms in plain words

- **Pixel:** one small area represented by a value in an image.
- **Built-up:** land classified as buildings or other built surfaces in the reference/model, rather than a verified building inventory.
- **Random forest:** many decision trees voting from the input measurements.
- **Holdout:** data kept apart from training and threshold selection for testing.
- **Percentile rank:** where a value sits compared with the other eligible values.
- **Proof of concept:** a working example used to test an idea before a full service.
