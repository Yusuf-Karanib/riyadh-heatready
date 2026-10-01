# Presenter guide for Yusuf

This guide is for studying after the technical package is finished. Do not memorize words you do not understand.

## The 20-second answer

> Riyadh HeatReady finds 1 km zones where recent built-up growth, hotter land surfaces, and modelled population overlap. It helps a city planning team decide where to inspect first for suitable cooling measures. It is a screening tool, not an automatic decision system.

## The 60-second answer

> I focused on southeastern Riyadh because one open Planet Tanager scene and matching optical, radar, thermal, land-cover, and population data cover the area. I used six annual land-cover maps to show the 2018–2023 built-up trend. I kept an endpoint growth pixel only when a separate Sentinel-2 and Sentinel-1 model confirmed that it still looked built-up in 2025. Then I added Landsat land-surface temperature, WorldPop population, and vegetation context. The result is a transparent 1 km priority score. The built-up model reached an F1 agreement of 0.88 against a spatially separate WorldCover reference area, but that is not field accuracy. The final map tells planners where to inspect first, and every result still needs local checking.

## Official 10-minute pitch order

### 1. Problem — 0:00 to 0:45

Rapid development and hot surfaces can overlap, but planners need a short list of places to inspect rather than several disconnected satellite layers. State the 168.30 km² southeastern Riyadh study area and do not claim the whole city was analysed.

### 2. User and decision — 0:45 to 1:30

The intended user is a municipal urban-planning and heat-resilience team. The decision is which 1 km zones should receive field review first. Say clearly that no real municipal user interview has happened yet.

### 3. Data — 1:30 to 2:40

- Sentinel-2: reflected light, quality mask, vegetation, and built-surface features.
- Sentinel-1: radar structure that helps separate buildings from bright desert.
- Annual land cover: six maps showing the 2018–2023 trend and proposing endpoint change.
- Landsat: 2025 land-surface temperature.
- WorldPop: modelled 2025 population.
- Planet Tanager: detailed 2025 surface spectra used for material context and a desert-confusion test.

Explain that Earth-observation data are core: without them, the result cannot exist.

### 4. Method — 2:40 to 4:30

Train the optical-radar model in the west, tune it in a separate middle strip, and test it in the east. Plot the six annual built-up estimates, then keep 2018–2023 endpoint growth only when the separate 2025 optical-radar model confirms it. Rank only cells containing confirmed growth with a transparent score: 40% heat, 30% population, 20% growth, and 10% lack of vegetation.

### 5. Working outputs and results — 4:30 to 6:45

Show the actual decision map, annual trend, priority table, and dashboard.

- 3.74 km² conservative confirmed-growth signal.
- Annual mapped built-up area rose overall from 85.39 km² to 98.03 km², with a 2022 dip that warns against treating each year as exact construction truth.
- Mean May 2025 land-surface temperature: 49.02 °C.
- F1 agreement: 0.88; IoU: 0.78.
- 14 High-priority cells from 67 eligible cells.
- R05C10 is the highest-ranked example at about 78.7.

### 6. Validation and limitations — 6:45 to 7:45

Explain the spatial holdout and then limit the claim: WorldCover is also satellite-derived, so the score is agreement, not field accuracy. Temperature is the land surface, population is modelled, and bright desert remains difficult.

### 7. Hyperspectral contribution and innovation — 7:45 to 8:30

Tanager showed likely-unbuilt bright desert with higher median narrow-band NDBI than established-built surfaces. This supports the decision not to use a simple "high NDBI means built" rule. Do not claim specific material identification or change from one Tanager date.

### 8. Impact and product path — 8:30 to 9:15

The PoC delivers a dashboard and GIS-ready ranked layer. A sensible first pilot is for one municipal team to inspect the top five zones and record whether the ranking improves its screening process. This is a value hypothesis, not a claimed customer or sale.

### 9. Incubation next steps — 9:15 to 10:00

Interview at least three real users, agree on the score weights, add city plans and worker-exposure data, field-check the top zones, measure false alarms, and test a repeatable update for another Riyadh area. Stop at 10 minutes.

## How the project fits the five official criteria

- **Quality of space-data use:** each EO source has a defined purpose; quality masks, exact scenes, two-source confirmation, and Tanager sensitivity analysis are documented.
- **Team strength and expertise:** do not invent qualifications. Demonstrate strength through the working notebook, clear explanation, tested outputs, and honest ownership of the method.
- **Problem relevance and impact:** one regional urban-heat problem, one municipal user, and one inspection decision.
- **Innovation:** the workflow joins growth, heat, people, and vegetation while measuring why NDBI alone fails in bright desert.
- **Feasibility:** a focused area, traditional baseline, spatial holdout, reproducible sample, dashboard, and GIS-ready outputs.

The technical tie-breaker is feasibility plus quality of space-data use. The project can claim working features and meaningful hyperspectral analysis as bonuses. It cannot claim the three-user validation bonus.

## What the Tanager result means

The Tanager spectra separate likely-unbuilt surfaces from built and growth surfaces. More importantly, the likely-unbuilt desert group had a higher median narrow-band NDBI than the established-built group. The same order remains after excluding every pixel flagged by the beta cloud mask. This shows why a simple "high NDBI equals buildings" rule is unsafe in Riyadh. It does not identify a specific surface material.

Do not say the project used Satellite 813 imagery. It used an **open Planet Tanager archive scene** because Satellite 813 data were not guaranteed during the PoC phase.

## Questions judges may ask

### Why not use only NDBI?

Bright bare soil can have a high NDBI. In this case, Tanager showed likely-unbuilt land with higher median NDBI than established built land. Radar and reference land cover reduce this confusion.

### Is 49 °C the air temperature?

No. It is satellite-derived land-surface temperature for one Landsat observation. Roofs, roads, and soil can be much hotter than the air.

### Is the F1 score true field accuracy?

No. It is agreement with ESA WorldCover in a spatially separate test area. Independent field or city data are still needed.

### Why is confirmed growth only 3.74 km² when the annual map proposed 13.82 km²?

The final layer is conservative. A change must pass the annual-map test and the separate 2025 optical-radar confirmation. This reduces false positives but can miss real growth.

### Why did mapped built-up area dip in 2022?

The annual product can classify some pixels differently between years because of imagery and model uncertainty. The six-year line is supporting evidence, not an exact building-construction calendar.

### Why use a 1 km decision grid?

It is simple enough for a first planning screen and matches the population layer. It does not pretend the data can select an individual building intervention.

### Why these score weights?

They are transparent PoC assumptions: 40% heat, 30% population, 20% recent growth, and 10% lack of vegetation. A real user should review them.

### What is the product, not just the analysis?

The product is the decision dashboard and its GIS-ready ranked zones. A planning team can use them as a repeatable first screen before detailed local assessment.

### Who is the customer and what is the business model?

The potential adopter is a municipality or urban-planning authority. The honest next step is a small pilot that measures usefulness, accuracy, operating cost, and procurement fit. No customer, price, revenue, or contract is currently claimed.

### What is innovative here?

It is not a new satellite index. The useful difference is the narrow decision workflow: annual change proposes growth, separate optical-radar evidence confirms it, heat and population set inspection priority, and hyperspectral data tests a known desert failure mode.

## Six terms to understand

- **Pixel:** one measured square on Earth.
- **Band:** one wavelength range measured by a satellite.
- **Index:** a band formula that highlights a pattern; it is not ground truth.
- **F1:** one number balancing missed built pixels and false built pixels.
- **IoU:** the overlap between predicted and reference built-up areas.
- **Time series:** repeated observations of the same place across several dates.

## Statements to avoid

- "We measured human heat risk directly."
- "The population number is a census."
- "The model is 88% accurate everywhere."
- "Every red pixel is a new building."
- "Tanager is Satellite 813."
- "The score tells the municipality exactly what to build."
