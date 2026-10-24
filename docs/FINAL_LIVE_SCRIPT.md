# Final live pitch script

Use this with:

- `slides/Riyadh_HeatReady_Final_Live_Pitch_v3.pptx`
- `output/pdf/Riyadh_HeatReady_Final_Live_Pitch_v3.pdf`

Target finish: **6:15**. Do not go past **6:45** during practice. The official limit is 8:00.

Slides 1-5 are Yusuf. Slides 6-8 are Raed. This gives Yusuf about 60% and Raed about 40%. Slides 9-10 are only for questions.

Do not try to sound perfect. Learn the meaning, then speak normally.

## Slide 1 - Yusuf - 0:00 to 0:15

> Good afternoon. We are Team Milkaholics, and this is Riyadh HeatReady. We asked one practical question: if planners can inspect only a few areas, where should they start?

## Slide 2 - Yusuf - 0:15 to 0:35

> I am Yusuf, an early-career AI and cloud developer based in the UAE. I lead the project, explain the data and result, and run the demo. Raed focuses on validation and how this idea could be tested with planners.

## Slide 3 - Yusuf - 0:35 to 1:15

> The problem is that the information a planner needs sits in separate maps. One map shows growth, another heat, another population and another vegetation. Comparing them takes time. HeatReady brings these layers together and ranks one-kilometre areas. The ranking suggests where to inspect first. It does not make the final planning decision.

## Slide 4 - Yusuf - 1:15 to 2:45

> Here is our answer. Sixty-seven one-kilometre cells contained confirmed growth signals, and fourteen were labelled high priority. R05C10 ranked first with a score of about 78.7. The score combines heat, population, confirmed growth and low vegetation, so each result can be explained.

Open `outputs/dashboard.html` and show only the Decision output section.

> The dashboard shows the same ranked map and table. The files can also be opened in a spreadsheet or GIS.

Return to slide 4.

> A high score means inspect this area early. It does not mean a project should automatically start there.

## Slide 5 - Yusuf - 2:45 to 3:45

> We used open satellite data, and each source had one job. Annual land-cover maps showed where built-up land may have appeared between 2018 and 2023. Sentinel-2 and Sentinel-1 checked those places using optical and radar data. Landsat gave land surface temperature. WorldPop gave a population estimate, and Sentinel-2 also gave vegetation. The annual maps first flagged 13.82 square kilometres. After the optical and radar checks, 3.74 square kilometres remained. The final weights are 40 percent heat, 30 percent population, 20 percent confirmed growth and 10 percent low vegetation. These are starting assumptions that a real user should review.

## Slide 6 - Raed - 3:45 to 4:40

> We tested the built-up model on the eastern part of the study area, separate from the training area, using ESA WorldCover as a reference. It reached an F1 score of 0.88, an overlap score of 0.78 and balanced accuracy of 0.89. In simple terms, the model and the satellite reference agreed well. But this does not prove field accuracy. Landsat measures surface temperature, not air temperature or personal heat exposure. WorldPop is an estimate, not a live population count. Bright desert and roofs can still confuse the model. The weights in our final score are also our choices. HeatReady should guide inspection, not make an automatic decision.

## Slide 7 - Raed - 4:40 to 5:20

> The main difference is that we do not rely on one image or one index. Annual maps suggest where growth may have happened, then optical and radar data check that signal. In the Tanager scene, unbuilt desert scored higher than established built land on a common built-up index. This shows why one threshold can mislead us. Each final score also keeps its four parts visible, so a planner can see why an area ranked highly.

## Slide 8 - Raed - 5:20 to 6:15

> Our next step is small and practical. First, we would meet planners or GIS staff and learn how they choose areas today. Then we would check the top five HeatReady areas against local plans and field observations. We would record which results were useful and which were false alarms. Based on that, we would change the weights and add missing local information, such as worker exposure or planned projects. Finally, we would repeat the test in another part of Riyadh. The goal is to learn whether HeatReady saves time without sending staff to the wrong places. Thank you. We are ready for your questions.

## If something goes wrong

If the dashboard is slow, do not troubleshoot. Stay on slide 4 and say:

> The report contains the same map and the top-five table. The repository also includes CSV, GeoJSON and GeoTIFF files for further review.

If you reach 6:00 before slide 8 is finished, use this short ending:

> Our next step is to test the top five areas with city staff and measure useful results and false alarms. Thank you. We are ready for your questions.

Never open slides 9-10 during the main pitch. Use them only if a judge asks about sources or validation.
