# Raed Mardoum — finals role and study guide

For the live pitch, study slides 6-8 in `docs/FINAL_LIVE_SCRIPT.md`. That shorter script replaces any older timing in this guide.

## Assigned role

**Validation and pilot presenter**

Raed presents slides 6–8. He explains what the validation proves, the main limitations, what makes the solution different, its possible impact, and how the team would test it through a municipal pilot.

## Contribution statement

> My finals responsibility is to explain the validation evidence and its limits, why the evidence chain is different, how planners should interpret the ranking, and how we would test the solution through a municipal pilot.

## Team-slide wording

**Raed Mardoum**

Validation and pilot presenter

- Explains what the validation results mean and what they do not prove.
- Explains the main limits and how planners should use the ranking safely.
- Presents how the team would test the ranking through a municipal pilot.

**Project responsibility:** validation interpretation, municipal decision workflow, impact framing, and pilot planning.

## What Raed must understand

### 1. The problem

Urban growth, heat, population, and vegetation information often sit in separate maps or datasets. A planning team may need to compare them manually before deciding where to inspect.

Riyadh HeatReady combines these signals into one screening map for southeastern Riyadh.

### 2. The user and decision

- **User:** a municipal urban-planning and heat-resilience team.
- **Decision:** which 1 km zones should the team inspect first?
- **Action after the ranking:** compare the highest-ranked zones with local plans and field conditions before selecting any measure.

The tool does not automatically prescribe trees, shade, cool roofs, or cool pavements. Local inspection decides what is suitable.

### 3. The priority score

Only cells containing confirmed built-up growth are ranked.

- 40% land-surface heat
- 30% modelled population
- 20% confirmed built-up growth
- 10% lack of vegetation

The weights are transparent PoC assumptions. Municipal users must review and adjust them during a pilot.

### 4. The result

- 67 eligible 1 km cells were ranked.
- 14 cells were labelled High priority.
- The highest-ranked example is **R05C10**, with a score of about **78.7**.
- The result tells planners where to inspect first. It does not prove personal heat exposure or select a final intervention.

### 5. Validation numbers

- **F1: 0.88**
- **Intersection over Union: 0.78**
- **Balanced accuracy: 0.89**

These numbers compare the model with ESA WorldCover in a separate east-side test area. WorldCover is another satellite product. The numbers show satellite-product agreement, not field accuracy.

### 6. What makes the approach different

The project does not trust one change map or one index by itself.

- Annual land-cover maps propose possible growth.
- Separate optical and radar evidence confirm pixels that still look built-up in 2025.
- The score shows every component instead of hiding the decision inside a black box.
- Planet Tanager showed why a simple NDBI threshold can fail in bright desert.

One Tanager date adds material context. It does not prove change or identify a specific material.

### 7. Why the result could help

The ranking can reduce the time spent comparing separate datasets. It gives the planning team a consistent starting point for local review and makes every score component visible.

No real municipal user interview has happened yet, so this benefit remains a hypothesis that the team must test.

### 8. Important limitations

- Landsat measures land-surface temperature, not air temperature or personal heat exposure.
- WorldPop is a modelled population estimate, not a live census.
- The validation score measures agreement with another satellite product, not field accuracy.
- Bright desert surfaces can resemble built-up land.
- The selected score weights have not been approved by a municipality.

### 9. Incubation plan

1. Interview at least three planners, GIS staff, or heat-resilience stakeholders.
2. Confirm the real decision workflow and agree on score weights and thresholds.
3. Inspect the highest-ranked zones and record useful results and false alarms.
4. Add local plans, worker-exposure information, and higher-resolution imagery where available.
5. Test the workflow in another Riyadh area and measure update time and cost.

## Raed's speaking section

Target length: **3 minutes 10 seconds** across slides 6–8.

### Slide 6 — 4:45–5:55

> The east-side spatial test reached an F1 score of 0.88, an Intersection over Union of 0.78, and balanced accuracy of 0.89 against WorldCover. These numbers show agreement with another satellite product, not field accuracy. Land-surface temperature is not air temperature, WorldPop is modelled, and bright desert can still confuse classification. The score weights are also assumptions that municipal users must review. These limits are why HeatReady supports local inspection instead of automatic action.

### Slide 7 — 5:55–6:55

> What makes the project different is the conservative and explainable evidence chain. Annual land-cover change proposes possible growth, while separate optical and radar evidence confirm it. Tanager also showed why one NDBI threshold can fail in bright desert. Every priority zone keeps visible score components and GIS evidence. The possible impact is faster and more repeatable screening, but we cannot claim that benefit until real users test it.

### Slide 8 — 6:55–7:55

> The next stage is a measured pilot, not a deployment claim. First, we would interview real users and confirm the workflow. Second, we would inspect the top five zones and record useful results and false alarms. Third, we would adjust the weights and add local plans and worker-exposure information. Finally, we would test a repeatable update in another Riyadh area. Our ask is support for one municipal pilot that measures whether the ranking improves screening.

## Questions Raed should be ready to answer

### What did you contribute?

My finals responsibility is validation interpretation, the ranked-zone workflow, impact, and the municipal pilot plan. I prepared these sections so I can explain what the evidence proves and what still requires real-user and field testing.

### Is the F1 score field accuracy?

No. It is agreement with ESA WorldCover in a separate east-side test area. Independent field or municipal reference data are still required.

### Why not use NDBI alone?

Bright bare surfaces can also produce a high NDBI. The Tanager comparison showed that a single threshold is unsafe in this desert setting, so the project uses multiple evidence sources.

### Is the reported temperature air temperature?

No. It is satellite-derived land-surface temperature from one Landsat observation. It does not measure personal heat exposure.

### Who is the user?

A municipal urban-planning and heat-resilience team. The tool helps them choose which 1 km zones to inspect first.

### Why use a ranking instead of prescribing an intervention?

Satellite and population data cannot show every local condition. The ranking narrows the search area, while planners and field teams decide whether shade, vegetation, cool materials, or another response fits the location.

### Why these four score components?

They represent the PoC's decision logic: heat shows hotter surfaces, population represents possible exposure, confirmed growth shows recently urbanized areas, and vegetation provides cooling context. The exact weights still require user review.

### Why is heat weighted at 40%?

The selected challenge includes heat risk, so the PoC gives surface heat the largest share. The 40% value is an assumption, not an official municipal weight. A pilot must test alternatives with users.

### What is the expected impact?

The tool could reduce the time planners spend comparing separate datasets and give them a repeatable way to select field-inspection priorities. This remains a hypothesis until real users test it.

### How would you validate the product during incubation?

We would interview users, agree on the decision and weights, inspect the top-ranked zones, label useful results and false alarms, and compare the ranking with local plans and field evidence.

### What happens if the ranking is wrong?

No automatic action follows from the score. A wrong ranking wastes inspection time, so the pilot must measure false alarms and adjust the model before operational use.

### Why use 1 km cells?

They keep the PoC simple, match the population layer, and support early area-level screening. They are not detailed enough to select an individual building intervention.

### What would you build next?

We would add user-approved weights, local plans, worker-exposure information, field labels, and higher-resolution imagery, then test a repeatable update in another Riyadh area.

## Study order

1. Learn the three validation metrics and their limits.
2. Learn the bright-desert/NDBI finding and the evidence-chain explanation.
3. Learn the user, decision, and action.
4. Memorize the four score components and their weights.
5. Learn the result, limitations, and five pilot steps.
6. Rehearse slides 6–8 until the full section fits within 3 minutes 10 seconds.
7. Practise every question above with Yusuf.

Raed does not claim that he wrote the code or processed the imagery. Yusuf presents the data and technical method. Raed presents what the validation means, the limits, innovation, impact, and pilot plan.
