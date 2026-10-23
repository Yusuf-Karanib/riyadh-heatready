# Yusuf's solo finals backup guide

## Current situation

- Yusuf completed the pre-pitch onboarding on 22 October 2026.
- Final judging is scheduled for 28–29 October 2026. The exact team slot remains pending.
- The main final-pitch plan remains Yusuf on slides 1–5 and Raed on slides 6–8 once the exact time arrives.
- Use the solo material in this guide only if Raed later confirms that he cannot attend the actual final pitch.
- Use the final live deck for rehearsal and screen sharing. Its shorter wording and notes target a 6:15 finish.

## What to open before the final pitch

Open these before joining:

1. `slides/Riyadh_HeatReady_Final_Live_Pitch.pptx`
2. `output/pdf/Riyadh_HeatReady_Final_Live_Pitch.pdf`
3. `outputs/dashboard.html`
4. The public GitHub repository.

Use `docs/FINAL_LIVE_SCRIPT.md` as the main script. If Yusuf presents alone, he reads Raed's slides as well and removes only the spoken handoff at the end of slide 5.

Check the camera, microphone, speakers, internet connection and screen sharing. Close private tabs and notifications.

If they ask for a short project introduction, say:

> I am Yusuf Karanib, team leader of Milkaholics. Riyadh HeatReady uses satellite and population data to rank one-kilometre zones in southeastern Riyadh for municipal inspection. The ranking combines recent built-up growth, land-surface heat, modelled population and vegetation. It supports local inspection and does not make an automatic planning decision.

Continue monitoring email and the platform for the exact judging time and Teams link.

## The ten facts Yusuf must know

1. **User:** a municipal planning and heat-resilience team.
2. **Decision:** which 1 km zones in southeastern Riyadh should the team inspect first?
3. **Study area:** 168.30 km². It does not cover all of Riyadh.
4. **Growth method:** annual land-cover maps propose growth. Sentinel-2 and Sentinel-1 check whether it still looks built-up.
5. **Candidate versus confirmed growth:** 13.82 km² was proposed. The stricter confirmation retained 3.74 km².
6. **Score:** 40% heat, 30% modelled population, 20% confirmed growth and 10% lack of vegetation.
7. **Output:** 67 eligible cells, 14 High-priority cells and top cell R05C10 at about 78.7.
8. **Validation:** F1 0.88, IoU 0.78 and balanced accuracy 0.89 against WorldCover in a separate east-side test area.
9. **Main limit:** WorldCover agreement is not field accuracy. Land-surface temperature is not air temperature. WorldPop is not a census.
10. **Next step:** interview users, inspect the top five cells, record false alarms, adjust the method and repeat it in another Riyadh area.

## What the judges score

The latest official email gives six criteria totalling 100 points:

- **Problem relevance and potential impact, 20 points:** slides 1 and 2.
- **Scientific and technical validity, 25 points:** slides 4 and 6, with slides 9–10 available for questions.
- **Innovation and differentiation, 20 points:** slide 7.
- **Quality of implementation, 20 points:** slide 5, the dashboard and repository outputs.
- **Documentation and evidence, 10 points:** reproducible repository, source records, GIS files and appendix evidence.
- **Development potential, 5 points:** slide 8.

Presentation quality supports these criteria but does not receive a separate score.

## Older detailed solo study notes

The timed script below is kept only as extra study material. For the live pitch, Yusuf should use `docs/FINAL_LIVE_SCRIPT.md`, speak both members' sections, remove the handoff at the end of slide 5, and target 6:15. Slides 9-10 stay hidden unless a judge asks for evidence.

### Slide 1 — 0:00–0:20

> Good afternoon. I am Yusuf Karanib from Team Milkaholics. City planners may need to compare separate maps of urban growth, surface heat, population and vegetation. Riyadh HeatReady combines satellite and population evidence into one ranked map of one-kilometre cells in southeastern Riyadh. Our question is: where should a municipal planning team inspect first?

### Slide 2 — 0:20–1:10

> The study area covers 168.30 square kilometres on the southeastern edge of Riyadh. It is one part of the city, not all of Riyadh. Our intended user is a municipal planning and heat-resilience team. Growth, surface heat, population and vegetation can sit in separate layers. HeatReady combines them into a ranked list of one-kilometre cells. The list tells the team where to inspect first. It does not select trees, roofs or another intervention. We have not interviewed municipal users yet, so a pilot must test whether the ranking fits their work.

### Slide 3 — 1:10–1:35

> I am the team leader and today's presenter. My teammate Raed Mardoum cannot attend this session, so I will present the complete project. I will cover the satellite data, method, results, validation, limitations and proposed municipal pilot.

Do not say that Raed completed work that he did not complete. If asked, explain that validation and pilot preparation were his assigned finals topics, but he cannot attend.

### Slide 4 — 1:35–2:55

> Each source has one job. Sentinel-2 provides optical information about vegetation and built surfaces. Sentinel-1 adds radar structure, which helps because bright desert can look built-up in optical images. Six annual land-cover maps flag possible change from 2018 to 2023. Landsat provides land-surface temperature for 10 May 2025. WorldPop provides modelled population. Planet Tanager gives detailed spectral context for one date and helps test desert confusion. The annual maps first proposed 13.82 square kilometres of growth. We kept only pixels where the 2025 optical and radar evidence also looked built-up. This stricter check retained 3.74 square kilometres. We then ranked the eligible cells using 40 percent heat, 30 percent population, 20 percent confirmed growth and 10 percent lack of vegetation. These weights are PoC assumptions that users must review.

### Slide 5 — 2:55–4:20

> The result is a priority map and a chart showing every part of the score. Sixty-seven cells contain confirmed growth. Fourteen are labelled High priority. R05C10 ranks first at about 78.7. This is a relative score, not a 78.7 percent risk probability.
>
> [Show the Decision output section of `outputs/dashboard.html` if the demonstration has been rehearsed.] The dashboard is a static report. It shows the headline numbers, map and top-five table. The repository also includes CSV, GeoJSON and GeoTIFF files for spreadsheet or GIS review.
>
> Every result remains a screening priority. A planning team must compare it with local plans and field conditions before taking action. I will now explain what the validation shows and what it does not show.

If screen switching fails, stay on slide 5 and continue. Do not troubleshoot during the pitch.

### Slide 6 — 4:20–5:25

> We trained the built-up model in the western part of the study area, tuned it in a separate middle strip and tested it in the east against ESA WorldCover. The east-side test reached F1 0.88, intersection over union 0.78 and balanced accuracy 0.89. F1 balances false alarms and missed built-up pixels. Intersection over union measures overlap. Balanced accuracy gives equal weight to built and unbuilt classes. These numbers show agreement with another satellite product. They do not prove field accuracy. Landsat measures land-surface temperature rather than air temperature. WorldPop is modelled. Bright desert can still confuse the classifier. These limits are why the output supports inspection instead of automatic action.

### Slide 7 — 5:25–6:20

> The main difference is that HeatReady does not trust one change map or one index. Annual maps propose possible growth. Separate optical and radar evidence check whether it still looks built-up. We also tested the shortcut of treating high NDBI as proof of built land. In the Tanager scene, likely-unbuilt desert had a higher median narrow-band NDBI than established built land. One threshold can therefore fail in this setting. Tanager adds context for one date, but it cannot prove change or identify a material. The score remains visible so users can review each part.

### Slide 8 — 6:20–7:20

> The next step is a small municipal pilot. We would first interview planners, GIS staff or heat-resilience stakeholders and confirm their current workflow. They would inspect the top five cells and record useful findings and false alarms. We would then adjust the weights and add local information such as worker exposure and planning constraints. Finally, we would repeat the process in another Riyadh area and measure the time, cost and repeatability. We are asking for support to test whether HeatReady actually helps a municipal team. Thank you. I am ready for your questions.

## Demonstration practice

Use two browser or application windows:

1. PowerPoint in slideshow mode.
2. `outputs/dashboard.html`, already positioned at the Decision output section.

Practise this sequence five times:

1. Reach slide 5.
2. Switch to the dashboard.
3. Point to 3.74 km², the map and R05C10.
4. Return to slide 5.
5. Continue without pausing.

If this takes longer than 30 seconds or fails once during the final technical test, use slide 5 only.

## Most likely judge questions

Keep each answer under 25 seconds.

### What problem are you solving?

> Growth, surface heat, population and vegetation can sit in separate datasets. HeatReady combines them into a short list of zones for local inspection.

### Who is the user?

> A municipal planning and heat-resilience team deciding which one-kilometre zones to inspect first.

### Why southeastern Riyadh?

> The area has matching open satellite and population data and includes established development, recent construction and bright desert surfaces that test the method.

### Why use space data?

> The ranking needs repeatable area-wide information about built structure, land-cover change, surface heat and vegetation. Population data alone cannot produce it.

### Why use Sentinel-1 and Sentinel-2 together?

> Sentinel-2 provides optical information. Sentinel-1 provides radar structure. Using both reduces reliance on optical colour in bright desert areas.

### Why not use NDBI alone?

> Bright bare surfaces can also produce high NDBI. The Tanager comparison showed that one threshold can confuse desert and built surfaces.

### Did you use Satellite 813 imagery?

> No. Satellite 813 data were not available for this baseline. We used open Sentinel, Landsat, annual land-cover, WorldCover, WorldPop and Planet Tanager data.

### Why did 13.82 km² become 3.74 km²?

> The annual maps proposed 13.82 km². The stricter rule kept only places where separate 2025 optical and radar evidence also supported built-up land. This reduces false positives but can miss real growth.

### Why these score weights?

> They are transparent PoC assumptions. Heat receives the largest share because the challenge includes heat risk. A municipal pilot must test and change the weights with users.

### Is 78.7 a risk probability?

> No. It is a relative ranking score among eligible cells. It is not a health-risk percentage or an official municipal priority.

### Is 49 °C air temperature?

> No. It is satellite-derived land-surface temperature from one Landsat observation. It does not measure air temperature or personal exposure.

### Is F1 0.88 field accuracy?

> No. It measures agreement with ESA WorldCover in a separate east-side test area. WorldCover is also satellite-derived, so field checking is still required.

### What is innovative?

> The method uses annual change to propose growth, optical and radar evidence to confirm it, and transparent heat and population components to rank it. Tanager tests a known desert failure mode.

### What impact can you prove?

> We can prove that the workflow produces a reproducible ranked map and GIS files. We cannot yet prove time savings or municipal value because no user pilot has happened.

### What would you do next?

> Interview users, inspect the top five cells, record false alarms, adjust the weights, add local constraints and repeat the test in another Riyadh area.

### What did Raed contribute?

> Raed is a registered team member. Validation interpretation and pilot preparation were his assigned finals topics. He cannot attend this session, so I am presenting those sections today.

### Did you use AI tools?

> We used AI-assisted development tools. I reviewed the data, method, outputs and claims, and I take responsibility for the submission. The repository is documented and reproducible.

Use that answer only after completing this guide and reviewing the submitted materials.

## Statements to avoid

Do not say:

- the project measured human heat risk;
- land-surface temperature is air temperature;
- WorldPop is a live census;
- F1 0.88 is accuracy everywhere;
- every detected pixel is a new building;
- the team used Satellite 813 imagery;
- the score tells the municipality what to build;
- the project has municipal users, field validation, customers or revenue;
- Raed completed work that he did not complete.

## Study order if the final pitch becomes solo

1. Learn the ten facts at the start of this guide.
2. Read the complete solo script aloud once without timing.
3. Learn slides 1–4 and explain them without reading.
4. Learn the results and demonstration on slide 5.
5. Learn validation and limitations on slide 6.
6. Learn the NDBI finding on slide 7.
7. Learn the pilot on slide 8.
8. Run three timed presentations each day.
9. Practise every question above in random order.
10. Stop changing wording on the final day. Focus on clear delivery and short answers.

## Final technical checklist

- Laptop connected to power.
- Stable internet and backup mobile hotspot if available.
- Camera, microphone and screen sharing tested.
- Proper full name in Microsoft Teams.
- PowerPoint, PDF, dashboard and repository already open.
- Notifications and private tabs closed.
- Final deck downloaded locally.
- Water nearby.
- Join the final pitch lobby at least 15 minutes early.

