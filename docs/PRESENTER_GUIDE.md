# Final judging presenter guide

## Official format

- Online final judging, tentatively 21–23 October 2026.
- 8 minutes for the English pitch and demonstration.
- 4 minutes for English questions.
- Present slides 1–8. Slides 9–10 are appendices for questions only.

Aim to finish at **7:55**. The planned spoken time is split exactly 60/40:

- Yusuf: **4 minutes 45 seconds**.
- Raed: **3 minutes 10 seconds**.

## The simple answer

> Riyadh HeatReady ranks 1 km zones in southeastern Riyadh where recent built-up growth, hotter land surfaces, and modelled population overlap. It helps a municipal planning and heat-resilience team decide where to inspect first. It is a screening tool, not an automatic decision system.

The word-for-word script, beginner lessons, complete Q&A, and separate Yusuf/Raed study sections are in `docs/FINALS_COMPLETE_STUDY_BOOK.md`.

## Eight-minute speaking order

### Slide 1 — 0:00–0:20 — Yusuf

> Riyadh HeatReady uses satellite data to rank 1 km zones in southeastern Riyadh where recent growth, hotter land surfaces and modelled population overlap. The decision is simple: where should a municipal team inspect first?

### Slide 2 — 0:20–0:55 — Yusuf

Introduce both members by project responsibility, not unverified biography.

- Yusuf: project lead; problem, data, method, score, and demo.
- Raed: validation meaning, limitations, innovation, impact, and pilot plan.

### Slide 3 — 0:55–1:50 — Yusuf

> The study covers 168.30 square kilometres in southeastern Riyadh, not the whole city. Growth, heat, population and vegetation are normally separate layers. Our intended user is a municipal planning and heat-resilience team. The MVP gives that team a ranked list of 1 km zones to inspect. It does not automatically prescribe trees, roofs or pavements. We have not yet completed a municipal user interview, so the workflow and value still require testing.

### Slide 4 — 1:50–3:10 — Yusuf

Explain one job per source.

- Sentinel-2: optical features, vegetation and quality masking.
- Sentinel-1: radar structure that helps reduce bright-desert confusion.
- Annual LULC: six maps that propose 2018–2023 endpoint change.
- Landsat: 2025 land-surface temperature.
- WorldPop: modelled population exposure.
- Planet Tanager: material context and a desert failure-mode test.

Then state the chain: annual change proposes growth; separate 2025 optical and radar evidence confirms it; heat, population, growth and vegetation rank the eligible cells.

### Slide 5 — 3:10–4:45 — Yusuf

Show the dashboard or stay on the slide if live navigation is slow. The dashboard is a static report, not an interactive app.

- 3.74 km² conservative confirmed-growth signal.
- 14 High-priority cells from 67 eligible cells.
- R05C10 is first at about 78.7.
- Score: 40% heat, 30% population, 20% confirmed growth, 10% lack of vegetation.

On slide 5, show the component chart. In the dashboard, show the map and top-five table. Explain that the repository contains separate CSV, GeoJSON, and GeoTIFF files. Do not claim that the dashboard has filters, zone selection, or export buttons. End with: local checking is required before action.

Handoff line:

> Raed will now explain what the validation proves, what makes the approach different, and how we would test it with a municipality.

### Slide 6 — 4:45–5:55 — Raed

> The spatial east-side holdout reached F1 0.88, IoU 0.78 and balanced accuracy 0.89 against WorldCover. WorldCover is another satellite product, so this is agreement, not field accuracy. Land-surface temperature is not air temperature. WorldPop is modelled. Bright desert remains difficult. The score weights are transparent assumptions that a real user must review.

### Slide 7 — 5:55–6:55 — Raed

> The innovation is the conservative, explainable evidence chain. Annual change alone is not trusted; optical and radar evidence confirm it. Tanager showed why a simple high-NDBI-means-built rule can fail in bright desert. One Tanager date adds material context, but it does not prove change or identify a specific material. The possible impact is faster, repeatable screening, but this remains a hypothesis until users test it.

### Slide 8 — 6:55–7:55 — Raed

> The next stage is a measured pilot, not a deployment claim. First, we would interview real users and confirm the workflow. Second, we would inspect the top five zones and record useful results and false alarms. Third, we would adjust the weights and add local plans and worker-exposure information. Finally, we would test a repeatable update in another Riyadh area. Our ask is support for one municipal pilot that measures whether the ranking improves screening.

Close at or before 8:00.

## Demo fallback

If the dashboard fails or the connection is slow:

1. Stay on slide 5.
2. Point to the decision map, top-ten score chart, and three headline numbers.
3. Say that the repository contains the dashboard, CSV, GeoJSON, GeoTIFF, and a run-all sample notebook.
4. Do not spend pitch time troubleshooting.

## Questions ownership

- Yusuf answers the problem, data sources, method, NDBI details, score calculation, demo, and reproducibility.
- Raed answers validation meaning, limitations in use, innovation, user impact, false alarms, business path, and the pilot.
- Either member may start an answer; the owner should finish it.

## Statements to avoid

- “We measured human heat risk directly.”
- “WorldPop is a census.”
- “The model is 88% accurate everywhere.”
- “Every detected pixel is a new building.”
- “We used Satellite 813 imagery.”
- “The score tells the municipality what to build.”
- Any education, job, customer, interview, revenue, or deployment claim that is not true.
