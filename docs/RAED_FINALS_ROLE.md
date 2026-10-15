# Raed Mardoum — finals role and study guide

## Assigned role

**Decision Workflow and Impact Lead; Co-presenter**

Raed owns one clear part of Riyadh HeatReady: explaining how the satellite analysis becomes a practical municipal decision, how the priority score should be interpreted, what impact the tool could have, and how the team would validate and develop it during incubation.

## Contribution statement

> Raed focused on turning the analytical results into a usable municipal decision workflow. He reviewed how planners would interpret the ranked 1 km zones, the score's assumptions and limitations, and the field-validation steps needed before action. He also helped shape the impact and incubation plan and co-presents these parts of the solution.

## Team-slide wording

**Raed Mardoum**

Decision Workflow and Impact Lead; Co-presenter

- Translated the ranked-zone output into a municipal inspection workflow.
- Reviewed the priority-score interpretation, assumptions, and limitations.
- Shaped and presents the impact, user-validation, and incubation plan.

**Project expertise:** municipal decision workflow, dashboard interpretation, impact framing, and incubation planning.

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

### 5. Why the result could help

The ranking can reduce the time spent comparing separate datasets. It gives the planning team a consistent starting point for local review and makes every score component visible.

No real municipal user interview has happened yet, so this benefit remains a hypothesis that the team must test.

### 6. Important limitations

- Landsat measures land-surface temperature, not air temperature or personal heat exposure.
- WorldPop is a modelled population estimate, not a live census.
- The validation score measures agreement with another satellite product, not field accuracy.
- Bright desert surfaces can resemble built-up land.
- The selected score weights have not been approved by a municipality.

### 7. Incubation plan

1. Interview at least three planners, GIS staff, or heat-resilience stakeholders.
2. Confirm the real decision workflow and agree on score weights and thresholds.
3. Inspect the highest-ranked zones and record useful results and false alarms.
4. Add local plans, worker-exposure information, and higher-resolution imagery where available.
5. Test the workflow in another Riyadh area and measure update time and cost.

## Raed's speaking section

Target length: 45 seconds.

> The next stage is a measured pilot, not a deployment claim. First, we would interview real users and confirm the workflow. Second, we would inspect the top five zones and record useful results and false alarms. Third, we would adjust the weights and add local plans and worker-exposure information. Finally, we would test a repeatable update in another Riyadh area. Our ask is support for one municipal pilot that measures whether the ranking improves screening.

## Questions Raed should be ready to answer

### What did you contribute?

I focused on how the analytical result becomes a usable municipal decision. I reviewed the ranked-zone workflow, score interpretation, limitations, expected impact, and the plan for user and field validation.

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

1. Learn the user, decision, and action.
2. Memorize the four score components and their weights.
3. Understand the result and its limitations.
4. Learn the five incubation steps.
5. Rehearse the speaking section until it fits within 45 seconds.
6. Practise every question above with Yusuf.

Raed does not need to claim that he wrote the code or processed the satellite data. Yusuf presents the technical workflow, validation metrics, and data sources.
