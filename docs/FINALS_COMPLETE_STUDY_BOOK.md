# Riyadh HeatReady finals study book

This records the original two-presenter preparation for Yusuf Karanib and Raed Mardoum. Raed is now unavailable for the final pitch. Yusuf must use `docs/SOLO_FINALS_CRASH_GUIDE.md` as the active speaking and study guide.

Use it with the corrected final deck:

- `slides/Riyadh_HeatReady_Final_Judging_Pitch_SUBMIT.pptx`
- `output/pdf/Riyadh_HeatReady_Final_Judging_Pitch_SUBMIT.pdf`

Submit the `SUBMIT` files above, not the older `READY` files. Slides 1–8 are the spoken pitch. Slides 9–10 are backup evidence for questions.

## 1. Official final format

- Final judging is online. The latest 22 October onboarding email refers to pitches during the following week, but the exact date and time are still pending.
- The team receives about 12 minutes.
- The English pitch and demonstration receive 8 minutes.
- English questions receive 4 minutes.
- The updated English presentation deadline was 19 October 2026 at 11:59 PM UAE time, with submission by email.
- The exact judging slot and meeting link are still waiting for organizer confirmation.
- A pre-pitch onboarding session is scheduled for 22 October 2026 at 11:04–11:11 AM UAE time.

Current speaking plan:

- Yusuf presents slides 1–8 alone, subject to organizer confirmation during onboarding.
- The solo script targets 7:20, leaving time for normal pauses.
- Slides 9–10 remain available for questions only.

## 2. The project in very simple words

### The problem

A city planner may have one map for urban growth, another for surface heat, another for population, and another for vegetation. Comparing them takes time.

### The user

A municipal urban-planning and heat-resilience team.

### The decision

Which 1 km zones in southeastern Riyadh should the team inspect first?

### The solution

Riyadh HeatReady combines satellite and population evidence into one ranked list and map.

### The action

The planner starts with the highest-ranked zones, checks local plans and field conditions, and then decides whether a detailed assessment is needed.

### What the project does not do

- It does not automatically order trees, shade, cool roofs, or cool pavements.
- It does not measure a person's heat exposure.
- It does not produce official city statistics.
- It does not replace municipal experts or field checks.

### The 20-second answer

> Riyadh HeatReady ranks 1 km zones in southeastern Riyadh where recent built-up growth, hotter land surfaces, and modelled population overlap. It helps a municipal planning and heat-resilience team decide where to inspect first. It is a screening tool, not an automatic decision system.

## 3. Why this fits the challenge

The assigned track is Urban Expansion, Land Use Change and Heat Risk.

The project addresses all three parts:

- Urban expansion: it looks for a conservative built-up growth signal.
- Land-use change: it compares annual land-cover maps from 2018 to 2023.
- Heat risk context: it adds 2025 land-surface temperature, modelled population, and vegetation.

Space data are essential. Without satellite observations, the growth, built structure, vegetation, and surface temperature layers could not be produced at this scale.

## 4. The study area and main results

Study area:

- Southeastern Riyadh urban-industrial fringe.
- Exact clipped area: 168.30 km².
- This is not the whole city.

Main results:

- Annual mapped built-up area: 85.39 km² in 2018 and 98.03 km² in 2023.
- Annual-map candidate growth: 13.82 km².
- Conservative confirmed-growth signal: 3.74 km².
- Mean land-surface temperature on 10 May 2025: 49.02 °C.
- 90th-percentile land-surface temperature: 51.71 °C.
- Modelled population inside the area: about 594,902.
- Eligible 1 km cells: 67.
- High-priority cells: 14.
- Highest-ranked cell: R05C10, score about 78.7.
- Spatial holdout F1: 0.88.
- Spatial holdout intersection over union: 0.78.
- Spatial holdout balanced accuracy: 0.89.

Every result above is a PoC output, not an official government statistic.

## 5. What each dataset does

### Sentinel-2

Sentinel-2 is an optical satellite. It measures reflected sunlight in several bands.

Its job here:

- provide colour and infrared information;
- calculate vegetation and built-surface features;
- help identify surfaces that look built-up.

Simple sentence:

> Sentinel-2 shows how surfaces reflect light.

### Sentinel-1

Sentinel-1 is a radar satellite. Radar responds to surface structure and roughness and works differently from optical imagery.

Its job here:

- add structural evidence;
- reduce dependence on optical colour alone;
- help with bright-desert confusion.

Simple sentence:

> Sentinel-1 adds radar structure, so the model does not rely on optical colour alone.

### Annual land-use and land-cover maps

Six annual maps cover 2018 through 2023.

Their job here:

- show the overall mapped built-up trend;
- propose pixels that changed from non-built in 2018 to built in 2023.

They do not prove the exact construction year of each building. The mapped built-up area falls in 2022 and rises again in 2023, which shows classification uncertainty.

### Landsat 8

Landsat thermal data estimate land-surface temperature.

Its job here:

- show which surfaces were hotter on the selected clear observation;
- provide the heat component of the ranking.

It does not measure air temperature, body temperature, or personal heat exposure.

### WorldPop

WorldPop is a modelled population grid.

Its job here:

- add a possible exposure context;
- help prioritize areas where more people may be present.

It is not a live census and may miss industrial workers or daily population movement.

### ESA WorldCover

WorldCover is a satellite-derived land-cover product.

Its job here:

- provide built and unbuilt labels for the 2021 classifier test.

Agreement with WorldCover is not independent field accuracy because both the model and reference use satellite evidence.

### Planet Tanager

Tanager is a hyperspectral satellite source with many narrow spectral bands.

Its job here:

- add material context for one 2025 date;
- test a known desert failure mode;
- show why high NDBI alone cannot safely mean built-up.

It does not prove change and does not identify a specific roof or pavement material without labelled field data.

The project uses an open Planet Tanager archive scene. It does not use Satellite 813 imagery.

## 6. The method from start to finish

### Step 1: Put the sources on the same map

Every source is clipped to the same study area and aligned to a common grid. Invalid or low-quality pixels are masked.

### Step 2: Build the optical-radar classifier

The model uses:

- Sentinel-2 bands and indices;
- Sentinel-1 VV and VH radar features;
- ESA WorldCover 2021 built-up labels.

The classifier is a random forest. It combines many decision trees.

### Step 3: Separate training, tuning, and testing by location

- Western strip: train the model.
- Middle strip: choose the probability threshold.
- Eastern strip: test the model.
- Gaps separate the strips.

This is safer than randomly mixing nearby pixels because neighbouring pixels can look very similar.

### Step 4: Propose growth

The annual land-cover maps propose pixels that were not built in 2018 and were built in 2023. This produces 13.82 km² of candidate growth.

### Step 5: Confirm growth conservatively

A candidate pixel is retained only when the 2025 optical-radar model also calls it built-up and its built probability increased enough from 2018. Small isolated groups are removed.

This leaves 3.74 km². It reduces false positives, but it can also miss real growth.

### Step 6: Build 1 km decision cells

Only cells with valid evidence and some confirmed growth are eligible. There are 67 eligible cells.

For each eligible cell, four values are ranked from 0 to 1 compared with the other eligible cells:

- hotter surface receives a higher heat component;
- larger modelled population receives a higher population component;
- more confirmed growth receives a higher growth component;
- less vegetation receives a higher lack-of-green component.

Population is log-transformed before ranking so a few very large values do not dominate everything.

### Step 7: Calculate the score

The score is:

> 100 × (0.40 heat + 0.30 population + 0.20 confirmed growth + 0.10 lack of vegetation)

The weights are transparent PoC assumptions.

They are not:

- probabilities;
- government-approved weights;
- proof that one intervention is correct.

High priority means the top 20% of eligible scores. Medium begins at the median. The remaining eligible cells are Watch.

### Step 8: Deliver the result

The project provides:

- a self-contained static HTML dashboard;
- a CSV ranked table;
- GeoJSON polygons;
- GeoTIFF map layers;
- a run-all sample notebook;
- the complete source pipeline and documented limitations.

## 7. Important terms in beginner language

- AOI: area of interest, meaning the exact study area.
- Earth observation or EO: observing Earth using satellites or other remote sensors.
- Optical data: reflected-light measurements, similar to a camera but with more bands.
- Radar data: measurements made using radio waves that respond to structure and roughness.
- Thermal data: measurements used to estimate surface temperature.
- Hyperspectral data: many narrow colour-like bands that show detailed spectral differences.
- Pixel: one small square measurement in an image.
- Land cover: what covers the ground, such as buildings, vegetation, water, or bare soil.
- NDVI: a vegetation index. Higher values usually indicate more green vegetation.
- NDBI: a built-up index. It can also be high over bright bare ground, so it is unsafe alone.
- LST: land-surface temperature, not air temperature.
- Classifier: a model that assigns a class, such as built or unbuilt.
- Random forest: many decision trees voting together.
- Training data: examples used to teach the model.
- Tuning data: separate examples used to select a setting such as the threshold.
- Test data: separate examples used only to measure final performance.
- Spatial holdout: testing in a different geographic area from training.
- Threshold: the cut-off that changes a probability into built or unbuilt.
- False positive: the model says built when the reference says unbuilt.
- False negative: the model misses a built pixel.
- Precision: of the pixels called built, how many match the reference.
- Recall: of the reference built pixels, how many the model finds.
- F1: one number balancing precision and recall.
- Intersection over union or IoU: how much the predicted built area overlaps the reference built area.
- Balanced accuracy: accuracy that gives built and unbuilt classes equal importance.
- Percentile rank: a value's position compared with the other eligible cells.
- Proof of concept or PoC: a small working test, not a finished operational system.
- Screening tool: a tool that narrows where to look first.
- CSV: a table that opens in spreadsheet software.
- GeoJSON: map features that GIS and web-mapping software can read.
- GeoTIFF: a raster image that contains geographic location information.
- Reproducible: another person can follow the documented process and obtain the same example result.

Pronunciation:

- EO: “E-O”.
- PoC: “proof of concept”.
- NDVI: “N-D-V-I”.
- NDBI: “N-D-B-I”.
- IoU: “eye-oh-you”.
- GeoTIFF: “geo-tiff”.

## 8. Original two-presenter script, now superseded

Use the solo script in `docs/SOLO_FINALS_CRASH_GUIDE.md`. The script below remains only as a record of the original split.

Do not read the words inside square brackets aloud.

### Slide 1, Yusuf, 0:00–0:20

> Good afternoon. We are Team Milkaholics, and our project is Riyadh HeatReady. We used satellite data to find places in southeast Riyadh where recent growth, hot land surfaces and population overlap. Our question is: where should a municipal planning team inspect first?

### Slide 2, Yusuf, 0:20–0:55

> I am Yusuf Karanib, the project lead. I will explain how the satellite data becomes a priority map and run the demonstration. Raed Mardoum will explain what the validation results mean, where the method is limited and how we would test the ranking with a municipal team.

### Slide 3, Yusuf, 0:55–1:50

> The study area covers 168.30 square kilometres on the southeastern edge of Riyadh. It is one part of the city, not all of Riyadh. Our intended user is a municipal planning and heat-resilience team. Growth, surface heat, population and vegetation can sit in separate layers, so staff still have to compare them before deciding where to inspect. HeatReady puts those layers into one ranked list of one-kilometre cells. It does not tell the user to plant trees or install a cool roof. It only suggests where to check first and compare with local plans and field conditions. We have not yet interviewed municipal users, so the first pilot must test whether this workflow is useful to them.

### Slide 4, Yusuf, 1:50–3:10

> We used six open data sources, and each one has a specific job. Sentinel-2 provides optical information about vegetation and built surfaces. Sentinel-1 adds radar structure, which helps because bright desert can look built-up in optical images. Six annual land-cover maps flag possible built-up change from 2018 to 2023. Landsat 8 provides land-surface temperature for 10 May 2025. WorldPop provides modelled population for 2025. Planet Tanager gives us a detailed spectrum for one date, which we use to test a known desert problem. We did not trust the annual change map by itself. It first flagged 13.82 square kilometres. We then kept only pixels where the 2025 optical and radar evidence also looked built-up. This left 3.74 square kilometres. We ranked the eligible one-kilometre cells using 40 percent heat, 30 percent population, 20 percent confirmed growth and 10 percent lack of vegetation. These weights are our PoC assumptions, not municipal policy.

### Slide 5, Yusuf, 3:10–4:45

> [On slide 5.] The result is a decision map and a component chart. Sixty-seven cells contain confirmed growth, and fourteen are labelled High priority. R05C10 ranks first with a score of about 78.7. Its score does not come from one hidden prediction; the chart shows the heat, population, growth and vegetation components.
>
> [Open `outputs/dashboard.html` and stay at the Decision output section.] This dashboard is a self-contained static report, not an interactive application. Here are the headline metrics, the decision map and the top-five table. The stricter rule retained 3.74 square kilometres of confirmed growth, and the top row is R05C10. The repository also contains separate CSV, GeoJSON and GeoTIFF files so a planner can review the same result in a spreadsheet or GIS.
>
> [Return to slide 5.] This output is a screening result. It cannot choose an intervention by itself; every high-ranked zone still needs local inspection. Raed will now explain what our validation proves, what the method adds, and how we would test it with a municipality.

### Slide 6, Raed, 4:45–5:55

> To test the built-up model, we trained in the western part of the study area, tuned in a separate middle strip and tested in the east against ESA WorldCover. The east-side holdout reached an F1 score of 0.88, an intersection over union of 0.78 and balanced accuracy of 0.89. F1 balances missed built-up pixels and false alarms. Intersection over union measures overlap. Balanced accuracy gives equal weight to built and unbuilt classes. These numbers show agreement with another satellite product; they are not field accuracy. Landsat measures land-surface temperature, not air temperature or personal heat exposure. WorldPop is modelled and may miss worker exposure. Bright desert and roofs can still confuse classification. The score weights are assumptions that a real user must review. Because of these limits, HeatReady supports inspection rather than making an automatic decision.

### Slide 7, Raed, 5:55–6:55

> HeatReady does not depend on one index. The annual maps flag possible change, and separate optical and radar evidence check whether the area still looks built-up. We also tested a common shortcut: using a high NDBI value as proof of built land. In the Tanager scene, likely-unbuilt desert had a higher median narrow-band NDBI than established built land, so one threshold can fail here. The Tanager image gives extra spectral context for one date. It cannot prove change or identify a material. Each ranked cell keeps its score parts and GIS evidence. This could make screening faster, but we need real users to test that before we claim a benefit.

### Slide 8, Raed, 6:55–7:55

> Our next step is a small municipal pilot. First, we would speak with at least three planners, GIS staff or heat-resilience stakeholders and confirm how they currently choose areas to inspect. Second, they would review the top five cells against local plans and field observations, and record useful findings and false alarms. Third, we would adjust the weights and add missing local information such as worker exposure and city-plan constraints. Finally, we would repeat the test in another Riyadh area and measure the time, cost and repeatability. We are asking for support to run that pilot and find out whether HeatReady actually helps a municipal team. Thank you. We are ready for your questions.

## 9. Yusuf's exact study section

Yusuf owns:

- slides 1–5;
- the problem and user;
- every data source;
- the classifier and change method;
- the score and results;
- the dashboard demonstration;
- reproducibility questions.

Yusuf must be able to explain these seven points without notes:

1. The user is a municipal planning and heat-resilience team.
2. The decision is which 1 km zones to inspect first.
3. Annual land cover proposes growth; optical and radar evidence confirm it.
4. Landsat adds surface heat, WorldPop adds modelled population, and Sentinel-2 adds vegetation.
5. The score weights are 40, 30, 20, and 10 percent.
6. The top cell is R05C10 at about 78.7; 14 of 67 cells are High.
7. The result supports inspection and never automatically chooses an intervention.

Yusuf's learning order:

1. Say the 20-second answer ten times.
2. Learn the role of each dataset.
3. Draw the eight method steps on paper from memory.
4. Memorize the score and the main results.
5. Practise the static-dashboard demonstration.
6. Rehearse slides 1–5 until the handoff happens at 4:45.
7. Practise every Yusuf-owned question in section 12.

## 10. Raed's exact study section

Raed's finals role is:

> Validation and pilot presenter.

Raed owns:

- slides 6–8;
- what the validation numbers mean;
- what the validation does not prove;
- limitations and safe interpretation;
- innovation and differentiation;
- expected impact;
- false-alarm handling;
- the municipal pilot plan.

Raed must be able to explain these six points without notes:

1. The user and decision.
2. F1 0.88, IoU 0.78, and balanced accuracy 0.89.
3. These are WorldCover agreement metrics, not field accuracy.
4. The innovation is the conservative, visible evidence chain.
5. The value is only a hypothesis until a real user pilot.
6. The next step is interviews, top-five checks, weight adjustment, and a repeatable second-area test.

Raed's contribution wording, after he has actually studied and reviewed these sections:

> For the final stage, I own validation interpretation, the ranked-zone workflow, impact framing, and the municipal pilot plan. I reviewed these parts so I can explain what the evidence proves, how a planner should use the result, and what still needs real-user and field testing.

Raed must not say he wrote the code, processed the imagery, completed field validation, or interviewed municipal users unless that becomes true.

Raed's learning order:

1. Learn the user, decision, result, and score.
2. Learn F1, IoU, and balanced accuracy in simple language.
3. Learn every limitation and why it matters.
4. Learn the Tanager and NDBI finding.
5. Memorize the four pilot steps.
6. Rehearse slides 6–8 until they take 3 minutes 10 seconds.
7. Practise every Raed-owned question in section 12.

## 11. Exact demonstration plan

The dashboard is a static report. It has no buttons, filters, zone selector, or download button.

Before joining the call:

1. Open the PowerPoint or PDF.
2. Open `outputs/dashboard.html` in a browser.
3. Scroll the dashboard to the Decision output section.
4. Keep the GitHub repository open only as a backup.
5. Close private tabs and notifications.

During slide 5:

1. Point to the map and component chart already visible on slide 5.
2. Share the browser window.
3. Show the dashboard's headline figures.
4. Show the decision map and top-five table.
5. Point to R05C10 at 78.7.
6. Say that the CSV, GeoJSON, and GeoTIFF are separate repository files.
7. Return to slide 5.
8. Hand over to Raed.

Do not try to click a zone. Do not say the dashboard exports files. The repository contains the separate output files.

Fallback if the browser fails:

1. Stay on slide 5.
2. Point to the map, component chart, and three headline numbers.
3. Say: “The repository contains the static dashboard, ranked CSV, GeoJSON polygons, GeoTIFF layers, and a run-all sample notebook.”
4. Continue to Raed. Do not troubleshoot during the pitch.

## 12. Judge questions and exact answers

Answer the question first. Keep most answers under 25 seconds.

### Team capability

#### What did Yusuf contribute?

Owner: Yusuf

> I am the project lead and data and method presenter. I own the problem definition, Earth-observation workflow, scoring logic, working-output demonstration, and reproducibility explanation for the final stage.

#### What did Raed contribute?

Owner: Raed

> For the final stage, I own validation interpretation, the ranked-zone workflow, impact framing, and the municipal pilot plan. I reviewed these sections so I can explain what the evidence proves and what still needs user and field testing.

Use this answer only after Raed completes that review.

#### Why are you presenting alone?

Owner: Yusuf

> Raed Mardoum is unavailable for the final session. I am the registered team leader and prepared to present the complete project. I asked the organizers to confirm this arrangement during the pre-pitch onboarding.

### Problem and user

#### Who is the user?

Owner: Raed

> A municipal urban-planning and heat-resilience team. The tool helps that team decide which 1 km zones to inspect first.

#### What exact problem do you solve?

Owner: Yusuf

> Growth, surface heat, population and vegetation can sit in separate layers. We combine them into a short, explainable inspection priority list.

#### Why southeastern Riyadh?

Owner: Yusuf

> The area has open Tanager coverage, matching Sentinel, Landsat, annual land-cover and population data, and a useful mix of established development, new construction and bright desert surfaces.

#### Does this cover all of Riyadh?

Owner: Yusuf

> No. The PoC covers a 168.30 km² area in southeastern Riyadh. A later test would repeat the workflow in another area before any citywide claim.

### Space data and method

#### Why is space data essential?

Owner: Yusuf

> The result needs repeatable area-wide evidence of built structure, land-cover change, surface temperature and vegetation. The priority map cannot be produced from population data alone.

#### Why use Sentinel-2 and Sentinel-1 together?

Owner: Yusuf

> Sentinel-2 provides optical and vegetation information. Sentinel-1 provides radar structure. Combining them reduces dependence on one optical index in bright desert conditions.

#### What model did you use?

Owner: Yusuf

> A random-forest classifier combines six Sentinel-2 bands, four optical indices, and three Sentinel-1 radar features. It was trained, tuned, and tested in separate geographic strips.

#### How did you prevent train-test leakage?

Owner: Yusuf

> We trained in the west, tuned in a separate middle strip, and tested in the east, with geographic gaps between them. Nearby test pixels were not mixed randomly into training.

#### Why not use NDBI alone?

Owner: Yusuf

> Bright bare surfaces can also have high NDBI. In the Tanager check, likely-unbuilt desert had a higher median narrow-band NDBI than established built land, so multiple evidence sources are safer.

#### Why use Tanager?

Owner: Yusuf

> It adds detailed spectral context and tests the desert-confusion failure mode. One Tanager date cannot prove change or identify a material by itself.

#### Did you use Satellite 813?

Owner: Yusuf

> No. The PoC uses open Sentinel, Landsat, annual land-cover, WorldCover, WorldPop and Planet Tanager data. Satellite 813 data were not available for the baseline.

#### Why is 2023 growth confirmed with 2025 data?

Owner: Yusuf

> The annual product proposes an endpoint change from 2018 to 2023. The 2025 optical-radar observation checks whether those pixels still look built-up. It is confirmation of persistence, not an exact construction-date claim.

#### Why did mapped built-up area fall in 2022?

Owner: Yusuf

> Annual satellite products can classify some pixels differently between years. The dip is a warning that the series supports an overall trend but is not an exact construction register.

#### Why is confirmed growth smaller than candidate growth?

Owner: Yusuf

> The annual map proposed 13.82 km². The stricter rule retained 3.74 km² only where separate 2025 optical-radar evidence also supported built-up land. This reduces false positives but can miss real growth.

### Score and output

#### Why 1 km cells?

Owner: Yusuf

> They match the population layer and are suitable for early area screening. They are not detailed enough to select an intervention for one building.

#### How is the priority score calculated?

Owner: Yusuf

> Eligible cells receive percentile-ranked heat, population, confirmed-growth and lack-of-vegetation components. The score is 40% heat, 30% population, 20% growth and 10% lack of vegetation, multiplied by 100.

#### Why is heat weighted at 40%?

Owner: Yusuf

> The challenge includes heat risk, so the PoC gives surface heat the largest share. Forty percent is a transparent assumption, not an official weight. A pilot must test it with users.

#### Is a score of 78.7 a 78.7% risk probability?

Owner: Yusuf

> No. It is a weighted relative ranking among eligible cells. It is not a probability, health-risk percentage, or official priority.

#### Why are 14 cells High?

Owner: Yusuf

> High begins at the 80th percentile of scores among 67 eligible cells. Fourteen cells meet that threshold because of the data distribution and ties.

#### Is 49 °C air temperature?

Owner: Yusuf

> No. It is satellite-derived land-surface temperature from one Landsat observation. It is not air temperature or personal heat exposure.

#### Is 594,902 an official census count?

Owner: Yusuf

> No. It is a modelled WorldPop estimate inside the study area. It may not represent industrial workers or daily movement.

#### How would a planner use the result?

Owner: Raed

> Start with the highest-ranked zones, compare them with local plans and field conditions, record useful results and false alarms, and only then assess a suitable intervention.

#### What happens if the ranking is wrong?

Owner: Raed

> No automatic action follows from the score. The main immediate cost is wasted inspection time, so a pilot must measure false alarms and adjust the method before operational use.

### Validation

#### What does F1 0.88 mean?

Owner: Raed

> It combines precision and recall for the built-up class. A higher value means a better balance between false alarms and missed built pixels against the WorldCover reference.

#### What does IoU 0.78 mean?

Owner: Raed

> It measures how much the predicted built-up area overlaps the reference built-up area. The intersection is divided by the union.

#### What does balanced accuracy 0.89 mean?

Owner: Raed

> It averages performance on built and unbuilt classes so the larger class does not dominate the result.

#### Is this field accuracy?

Owner: Raed

> No. It is agreement with ESA WorldCover in a separate east-side test area. WorldCover is also satellite-derived. Independent field or municipal reference data are still needed.

#### What is the biggest scientific limitation?

Owner: Raed

> The reference is another satellite product rather than field truth. Bright desert also remains difficult, so high-ranked areas require local checking.

### Innovation, impact, and future work

#### What is innovative?

Owner: Raed

> The innovation is the conservative and explainable evidence chain. Annual change proposes growth, optical and radar evidence confirm it, heat and exposure rank it, and hyperspectral evidence tests a known desert failure mode.

#### What impact can you prove now?

Owner: Raed

> We can prove that the workflow produces a reproducible ranked map and GIS-ready evidence. We cannot yet prove time savings or municipal value because no real-user pilot has happened.

#### What would you build next?

Owner: Raed

> We would interview users, agree on weights, inspect the top five zones, record false alarms, add local plans and worker-exposure data, and test a repeatable update in another Riyadh area.

#### What is the business model?

Owner: Raed

> The honest next step is a municipal pilot that measures usefulness, update cost and procurement fit. A supported analytics service or local deployment could be explored later. We do not claim a customer, price, revenue or contract.

#### Can this scale to another city?

Owner: Raed

> The open-data workflow can be repeated, but each city needs local calibration, user-approved weights, field checking and a review of data availability and licence terms.

### Reproducibility and tools

#### Can judges run it?

Owner: Yusuf

> Yes. The public repository contains pinned requirements, a run-all sample notebook, example input and output, exact source configuration, the full pipeline and documented limitations. The sample needs no credential.

#### Why is there a small notebook and a larger pipeline?

Owner: Yusuf

> The small notebook lets judges reproduce the scoring quickly from committed example inputs. The full pipeline downloads and processes the open satellite sources and takes longer.

#### Did you use AI tools?

Owner: Yusuf

> We used AI-assisted development tools during the work. We reviewed the data, method, outputs and claims, and we take responsibility for the submission. The repository is documented and reproducible, and we will not claim a step we cannot explain.

Do not add this topic unless a judge asks or an official rule requires it.

## 13. Claims neither person may make

Do not say:

- “We measured human heat risk directly.”
- “The 49 °C value is air temperature.”
- “WorldPop is a census.”
- “The model is 88% accurate everywhere.”
- “Every detected pixel is a new building.”
- “We used Satellite 813 imagery.”
- “Tanager proves land-use change.”
- “Tanager identified a specific material.”
- “The score tells the municipality what to build.”
- “A municipality is our customer.”
- “We proved time savings.”
- “We completed field validation.”
- “We interviewed users.”
- Any education, job, customer, revenue, or project contribution that is not true.

Use these corrections:

- land-surface temperature;
- modelled population estimate;
- WorldCover agreement;
- conservative confirmed-growth signal;
- screening priority;
- potential adopter;
- value hypothesis;
- proposed municipal pilot.

## 14. How the pitch covers the judging criteria

### Problem relevance and potential impact, 20 points

Slides 1 and 3 define the user, decision and intended value. Slide 8 explains how a pilot would test that value.

### Scientific and technical validity, 25 points

Slides 4 and 6 explain the data, method, spatial test, metrics and limits. Slides 9–10 provide supporting evidence.

### Innovation and differentiation, 20 points

Slide 7 explains the conservative evidence chain and the bright-desert NDBI failure test.

### Quality of implementation, 20 points

Slide 5 shows the working priority map, component chart and GIS-ready outputs. The dashboard and public repository provide the working evidence.

### Documentation and evidence, 10 points

The public repository contains a README, pinned requirements, a run-all sample notebook, exact source configuration, example inputs and outputs, GIS files and documented limitations.

### Development potential, 5 points

Slide 8 gives a measurable municipal pilot without claiming that deployment has happened.

### Presentation quality

Presentation quality supports the six criteria but does not receive separate points. Yusuf should use the solo script, finish before eight minutes and answer questions directly.

## 15. Rehearsal plan

### 16 October

- Both: read sections 2–7.
- Yusuf: learn slides 1–3.
- Raed: learn the validation terms and slide 6.
- Both: confirm that the role wording is honest.

### 17 October

- Yusuf: learn slides 4–5 and practise the static-dashboard demonstration.
- Raed: learn slides 7–8.
- Run one slow rehearsal with notes.
- Run one timed rehearsal.

### 18 October

- Run three full timed rehearsals.
- Practise the fallback without opening the dashboard.
- Ask each other every question in section 12.
- Fix any sentence either person cannot explain.

### 19 October

- Submit the corrected final PDF before 11:59 PM UAE time using the organizer's instructions.
- Aim to submit several hours early.
- Save the confirmation.
- Run one calm rehearsal after submission.

### 20 October

- Test camera, microphone, screen share, browser, PowerPoint, PDF, and internet.
- Prepare a charger and backup hotspot if available.
- Run one pitch and one Q&A session.

### Judging day

- Join 15 minutes early.
- Open the deck, dashboard, and repository before joining.
- Yusuf watches the timer.
- Yusuf follows the solo script and finishes before 8:00.
- Answer briefly and honestly.

## 16. What is still missing

These are the only known external items still pending:

- confirmed judging date and exact time;
- meeting link;
- confirmation that the final PDF was received.
- organizer confirmation that Yusuf may present alone;

Yusuf must also complete these actions if they are not already complete:

- attend the 22 October pre-pitch onboarding;
- confirm the solo-presenter arrangement;
- ask for the final date, time and Teams link;
- confirm that the emailed final PDF was received;
- save organizer confirmations;
- monitor email, spam, and the platform at least twice each day.

No new feature is required before judging. The work now is final submission, understanding, rehearsal, demonstration practice, and Q&A.

## 17. Final readiness test

The team is ready only when all answers are yes:

- Can Yusuf give the 20-second answer without notes?
- Can Yusuf explain every dataset in one sentence?
- Can Yusuf explain candidate growth versus confirmed growth?
- Can Yusuf state the score and its limitation?
- Can Yusuf demonstrate the static dashboard without clicking nonexistent controls?
- Can Raed explain all three validation metrics simply?
- Can Raed say why they are not field accuracy?
- Can Raed explain the innovation without calling NDBI a building detector?
- Can Raed explain the four pilot steps?
- Can both members explain the user and decision?
- Can both members state what the project does not prove?
- Can the team finish by 7:55 three times in a row?
- Can the team answer questions without inventing experience, users, customers, or results?

If any answer is no, rehearse that exact section again.
