# Final live pitch script

Use this with:

- `slides/Riyadh_HeatReady_Final_Live_Pitch.pptx`
- `output/pdf/Riyadh_HeatReady_Final_Live_Pitch.pdf`

Target finish: **6:15**. Do not go past **6:45** during practice. The official limit is 8:00.

Slides 1-5 are Yusuf. Slides 6-8 are Raed. This gives Yusuf about 60% and Raed about 40%. Slides 9-10 are only for questions.

Do not try to sound perfect. Learn the meaning, then speak normally.

## Slide 1 - Yusuf - 0:00 to 0:15

> Good afternoon. We are Team Milkaholics, and this is Riyadh HeatReady. We used satellite and population data to answer a simple question: when a planning team has limited time, which parts of southeast Riyadh should they inspect first?

## Slide 2 - Yusuf - 0:15 to 0:55

> In our study area, the information a planner needs is spread across separate maps. One map shows growth, another heat, another population and another vegetation. Comparing them takes time. HeatReady combines them and ranks one-kilometre areas. The highest-ranked areas are the places we suggest checking first. It does not choose an intervention or make a planning decision. A local team would still compare the result with city plans and visit the area. We have not interviewed municipal users yet, so that is an important next step.

## Slide 3 - Yusuf - 0:55 to 1:10

> I am Yusuf, and I will explain the data, method and demo. Raed will cover the validation, the limits and how we would test HeatReady with a municipal team.

## Slide 4 - Yusuf - 1:10 to 2:15

> We used open satellite data, and each source had one job. Annual land-cover maps showed where built-up land may have appeared between 2018 and 2023. We checked those areas with Sentinel-2 optical images and Sentinel-1 radar, because bright desert can sometimes look like buildings. Landsat gave us land surface temperature, WorldPop gave a population estimate, and Sentinel-2 also gave vegetation. The annual maps first flagged 13.82 square kilometres. After the optical and radar checks, 3.74 square kilometres remained. We then scored each eligible one-kilometre area: 40 percent heat, 30 percent population, 20 percent confirmed growth and 10 percent low vegetation. These weights are starting assumptions for this proof of concept. A real user should review them.

## Slide 5 - Yusuf - 2:15 to 3:45

> Here is the result. Sixty-seven cells contained confirmed growth, and fourteen were labelled high priority. R05C10 ranked first with a score of about 78.7. The chart shows why: its score combines heat, population, growth and vegetation. It is not a hidden prediction.

Open `outputs/dashboard.html` and show only the Decision output section.

> The report shows the same map and a short table. Here is R05C10 at the top. A planner can also use the result as a CSV, GeoJSON or GeoTIFF file in a spreadsheet or GIS.

Return to slide 5.

> A high score means inspect this area early. It does not mean a specific project should start there. Raed will now explain the validation, the limits and what makes this method different.

## Slide 6 - Raed - 3:45 to 4:40

> We tested the built-up model on the eastern part of the study area, separate from the training area, using ESA WorldCover as a reference. It reached an F1 score of 0.88, an overlap score of 0.78 and balanced accuracy of 0.89. In simple terms, the model and the satellite reference agreed well. But this does not prove field accuracy. Landsat measures surface temperature, not air temperature or personal heat exposure. WorldPop is an estimate, not a live population count. Bright desert and roofs can still confuse the model. The weights in our final score are also our choices. HeatReady should guide inspection, not make an automatic decision.

## Slide 7 - Raed - 4:40 to 5:20

> The main difference is that we do not rely on one image or one index. Annual maps suggest where growth may have happened, then optical and radar data check that signal. In the Tanager scene, unbuilt desert scored higher than established built land on a common built-up index. This shows why one threshold can mislead us. Each final score also keeps its four parts visible, so a planner can see why an area ranked highly.

## Slide 8 - Raed - 5:20 to 6:15

> Our next step is small and practical. First, we would meet planners or GIS staff and learn how they choose areas today. Then we would check the top five HeatReady areas against local plans and field observations. We would record which results were useful and which were false alarms. Based on that, we would change the weights and add missing local information, such as worker exposure or planned projects. Finally, we would repeat the test in another part of Riyadh. The goal is to learn whether HeatReady saves time without sending staff to the wrong places. Thank you. We are ready for your questions.

## If something goes wrong

If the dashboard is slow, do not troubleshoot. Stay on slide 5 and say:

> The report contains the same map and the top-five table. The repository also includes CSV, GeoJSON and GeoTIFF files for further review.

If you reach 6:00 before slide 8 is finished, use this short ending:

> Our next step is to test the top five areas with city staff and measure useful results and false alarms. Thank you. We are ready for your questions.

Never open slides 9-10 during the main pitch. Use them only if a judge asks about sources or validation.
