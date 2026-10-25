# Yusuf's presentation guide

Riyadh HeatReady | Team Milkaholics | Live deck v5

## Your job on the day

Present slides 1-5. Explain the problem, show the answer, and explain how the data produced it. Raed presents slides 6-8. Keep slides 9-10 for questions.

Aim to hand over around 3:45 and finish together around 6:15. Those are practice targets. The limit is eight minutes including the demonstration. A real timed rehearsal decides whether your pace fits.

## Learn this first

> HeatReady helps planners choose where to inspect first. It ranks one-kilometre areas in southeast Riyadh using satellite evidence of growth, surface heat, vegetation and a population estimate.

A planner opens the map, reviews a high-ranked area, then checks local conditions. The working output is a shortlist of inspection areas.

## Study in this order

1. Read the exact words on pages 2-4 aloud with the slides open.
2. Study the method on page 5. Explain it back without reading.
3. Work through the real cell on page 6. Understand where 78.7 comes from.
4. Practise the Yusuf questions in the shared judge guide.
5. Rehearse with Raed and a timer. Practise once with the dashboard unavailable.

## Your memory card

| Item | Remember |
| --- | --- |
| User | Municipal planning and heat-resilience staff |
| Question | Which areas should they inspect first? |
| Study area | 168.3 square kilometres in southeast Riyadh |
| Growth | 13.82 km2 proposed; 3.74 km2 retained by the stricter rule |
| Output | 67 eligible cells; 14 labelled High |
| First cell | R05C10, about 78.7 points |
| Weights | Heat 40%, population 30%, growth 20%, low vegetation 10% |

Learn the story before memorising numbers. You should be able to explain each number when asked what it measures.

---

## Your exact words: slides 1-3

Only the quoted paragraphs are spoken. The cues are reminders for you.

### Slide 1: Where should planners inspect first?

Target: 0:00-0:15. Look at the camera for the opening.

> Hello, we're Team Milkaholics, and this is Riyadh HeatReady. We worked on one question: if a planning team can visit only a few areas, where should it start?

Cue: Say the question slowly. It gives the judges a reason to look at the map.

### Slide 2: Our team

Target: 0:15-0:40.

> I'm Yusuf Karanib. I lead the project, explain the data, and run the demonstration. Raed Mardoum will explain the validation results, their limits, and how planners could test the tool.

Cue: Introduce your actual presentation responsibilities. Personal background already appears on the slide.

### Slide 3: The problem and our answer

Target: 0:40-1:20.

> We focused on 168 square kilometres in southeast Riyadh. A planner may need to compare separate maps of growth, surface heat, population and vegetation before choosing where to visit. HeatReady brings these together and ranks one-kilometre areas. The result gives the team a starting point for inspection. Local staff still decide what the area needs after checking conditions on the ground.

Cue: Point first to the study area, then to the problem and answer. The proposed user need still needs testing with municipal staff.

### If you lose your place

> We combine those separate maps to help planners decide where to inspect first.

Then move to slide 4. You do not need to restart the explanation.

---

## Your exact words: slide 4 and the demo

### Slide 4: Where planners should inspect first

Target: 1:20-2:45, including screen switching.

> Here is the result. Our stricter checks retained 3.74 square kilometres of possible built-up growth. Sixty-seven cells met the ranking rules, and fourteen received the High label. R05C10 came first at about 78.7 points. The chart shows how heat, population, growth and vegetation each contribute to a score.

Point to the map and then the stacked bar chart. Say the cell name as "R zero five, C ten."

### Show the report

Before the call, open outputs/dashboard.html in your browser and scroll to "Decision output" and "Inspect these zones first." Keep that window ready. The report is a static page with a map and table.

Switch to the browser for about 25-30 seconds.

> This is the working report. Here is the ranked map, and here is the table with R05C10 at the top. The repository also contains the results as a spreadsheet table and GIS files.

Point to that row. Return to slide 4.

> A high score is a reason to inspect an area early. The inspection determines what action makes sense there.

### If the browser is slow

Stay on slide 4 and say:

> The report contains the same map and ranked table shown here. The separate CSV and map files are also in our repository.

Continue to slide 5. Leave troubleshooting until after the pitch.

### Understand the pictures

- The numbered areas are the first inspection suggestions from the ranking.
- The colours show the relative score, from lower to higher.
- Each coloured piece in the bar chart is one weighted score component.
- The output covers eligible growth areas within this study area. A blank or excluded area has not been shown to be safe.

---

## Your exact words: slide 5 and handoff

### Slide 5: The data behind the answer

Target: 2:45-3:45.

> Each dataset had a job. Annual land-cover maps flagged possible growth from 2018 to 2023. Sentinel-2 optical data and Sentinel-1 radar checked whether those places looked built-up in 2025 and had become more built-like since 2018. That narrowed 13.82 square kilometres to 3.74.

> Landsat supplied surface temperature. WorldPop supplied estimated population, and Sentinel-2 supplied vegetation. We ranked the cells using 40 percent heat, 30 percent population, 20 percent growth and 10 percent low vegetation. Those weights are starting choices for the proof of concept. Tanager added a separate check on desert confusion. Raed will explain what the tests tell us.

Change to slide 6. Stop talking and let Raed begin.

### Cues to remember

- Annual maps: suggest the change.
- Optical plus radar: check the candidate pixels.
- Heat plus population plus growth plus vegetation: rank the areas.
- Tanager: investigate a problem with one built-up index.

### If you are running late

Use this shorter slide 5 instead:

> Annual maps proposed the growth. Optical and radar checks reduced it to 3.74 square kilometres. We ranked the eligible cells using heat, population, growth and vegetation, weighted 40, 30, 20 and 10 percent. Raed will explain the validation and the next test.

### Three different numbers

| Number | What it measures |
| --- | --- |
| 0.42 | The classifier cut-off chosen on the tuning area |
| 0.88 | Built-up F1 agreement on the separate test area |
| 78.7 | The first cell's weighted screening score out of 100 |

These come from different parts of the workflow. The F1 value does not measure how useful the ranking is to a planner.

---

## Understand the method

### What goes in

| Source | Its job here |
| --- | --- |
| Annual IO/Esri land-cover maps | Compare 2018 and 2023 to flag possible built-up change |
| Sentinel-2 | Reflected-light bands, vegetation and other surface indices |
| Sentinel-1 | Radar features that add information about surface structure |
| ESA WorldCover 2021 | Built/unbuilt labels for training, tuning and the spatial test |
| Landsat 8 | Surface temperature on 10 May 2025 |
| WorldPop 2025 | Modelled population for exposure context |
| Open Planet Tanager | Detailed spectra for a desert-index check on 15 May 2025 |

Seven named data products are involved. WorldCover supplies the reference labels in addition to the six sources listed on slide 5.

### How the built-up model works

A random forest combines many decision trees. Here, each tree uses satellite measurements to estimate whether a pixel looks built-up. The model has 260 trees and 13 input features: six optical bands, four optical indices and three radar features.

The west of the 2021 image supplies training examples. A separate middle strip chooses the cut-off. The east measures final agreement. Gaps separate the strips. This reduces the problem of testing on pixels immediately beside training pixels.

The chosen cut-off is 0.42. That model output is a built-up estimate, rather than a guaranteed probability that a building exists.

### How a possible change survives the checks

1. The annual maps must show non-built in 2018 and built in 2023.
2. The 2025 optical-radar model must exceed the built-up cut-off.
3. The model output must rise by at least 0.10 from 2018 to 2025.
4. The rule removes small isolated groups, retaining groups of at least six 30 m pixels.

The code calls the retained area "confirmed growth." Explain that this means agreement with the project's checks. Ground surveys have not confirmed it.

### The two scales

The common analysis grid uses 30 m pixels. The result groups measurements into 1 km cells, matching the coarse population input. A 1 km cell covers about one square kilometre before clipping at the study boundary. Resampling inputs onto 30 m squares does not create finer original detail.

---

## Understand one real answer

R05C10 is the highest-ranked cell in the committed result. Its mean surface temperature is about 50.79 C, modelled population about 3,818, and retained-growth fraction about 7.11%.

The code compares each eligible cell with the other eligible cells. It turns each measurement into a percentile rank. Larger heat, population and growth values rank higher. Lower vegetation ranks higher for the lack-of-green component.

### Where 78.7 comes from

| Component | Rank, roughly | Weight | Points |
| --- | --- | --- | --- |
| Surface heat | 0.881 | 40% | 35.22 |
| Population | 0.612 | 30% | 18.36 |
| Growth | 0.791 | 20% | 15.82 |
| Low vegetation | 0.925 | 10% | 9.25 |
| Total | | 100% | 78.66 |

The arithmetic is 100 x (0.40 x heat rank + 0.30 x population rank + 0.20 x growth rank + 0.10 x low-vegetation rank). The total uses unrounded components. The rounded display is 78.7. It is a relative score, not a percentage chance of heat illness.

"High" starts at the 80th percentile of the 67 eligible scores. This gives 14 High cells. That label is chosen by the ranking rule, rather than an independently measured danger threshold.

### Details a judge might spot

The second cell scores about 78.2, so the first two differ by less than half a point. Small weight changes could swap their order. A pilot should treat them as close candidates and test ranking stability.

Population goes through log(1 + value) before ranking. Because that transformation preserves order, it does not change these percentile ranks. The ranking itself limits the influence of extreme magnitudes. An older guide overstated the effect of the log step.

### Check your knowledge without notes

1. Who will use the result, and what decision will they make?
2. Why does 13.82 become 3.74? What might the stricter rule miss?
3. What did the model learn in 2021, and where was it tested?
4. Why does 78.7 differ from F1 0.88?
5. Could a hot established neighbourhood be excluded by the growth rule?
6. What would you show if the dashboard failed?

Answers: planning staff, inspection order; extra checks, some real growth; built/unbuilt labels, east strip; ranking versus reference agreement; yes; slide 4 and its evidence.

Evidence: outputs/results_summary.json, outputs/validation_metrics.json, outputs/priority_zones.csv, config.json and src/run_analysis.py. Technical reference: https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html
