# Final live pitch script

Use this with:

- `slides/Riyadh_HeatReady_Final_Live_Pitch_v5.pptx`
- `output/pdf/Riyadh_HeatReady_Final_Live_Pitch_v5.pdf`

Target finish: about **6:15** including the demonstration. Practise under **6:45**. The official limit is 8:00. These are practice targets, not measured speaking times.

Personal scripts and lessons: `docs/YUSUF_PRESENTATION_PREP.md` and `docs/RAED_PRESENTATION_PREP.md`. Joint questions and practice: `docs/JUDGES_QA_AND_REHEARSAL.md`.

Slides 1-5 are Yusuf. Slides 6-8 are Raed. This gives Yusuf about 60% and Raed about 40%. Slides 9-10 are only for questions.

Do not try to sound perfect. Learn the meaning, then speak normally.

## Slide 1 - Yusuf - 0:00 to 0:15

> Hello, we're Team Milkaholics, and this is Riyadh HeatReady. We worked on one question: if a planning team can visit only a few areas, where should it start?

## Slide 2 - Yusuf - 0:15 to 0:40

> I'm Yusuf Karanib. I lead the project, explain the data, and run the demonstration. Raed Mardoum will explain the validation results, their limits, and how planners could test the tool.

## Slide 3 - Yusuf - 0:40 to 1:20

> We focused on 168 square kilometres in southeast Riyadh. A planner may need to compare separate maps of growth, surface heat, population and vegetation before choosing where to visit. HeatReady brings these together and ranks one-kilometre areas. The result gives the team a starting point for inspection. Local staff still decide what the area needs after checking conditions on the ground.

## Slide 4 - Yusuf - 1:20 to 2:45

> Here is the result. Our stricter checks retained 3.74 square kilometres of possible built-up growth. Sixty-seven cells met the ranking rules, and fourteen received the High label. R05C10 came first at about 78.7 points. The chart shows how heat, population, growth and vegetation each contribute to a score.

Open `outputs/dashboard.html`, already at Decision output. Keep the demonstration to about 25-30 seconds.

> This is the working report. Here is the ranked map, and here is the table with R05C10 at the top. The repository also contains the results as a spreadsheet table and GIS files.

Return to slide 4.

> A high score is a reason to inspect an area early. The inspection determines what action makes sense there.

## Slide 5 - Yusuf - 2:45 to 3:45

> Each dataset had a job. Annual land-cover maps flagged possible growth from 2018 to 2023. Sentinel-2 optical data and Sentinel-1 radar checked whether those places looked built-up in 2025 and had become more built-like since 2018. That narrowed 13.82 square kilometres to 3.74.

> Landsat supplied surface temperature. WorldPop supplied estimated population, and Sentinel-2 supplied vegetation. We ranked the cells using 40 percent heat, 30 percent population, 20 percent growth and 10 percent low vegetation. Those weights are starting choices for the proof of concept. Tanager added a separate check on desert confusion. Raed will explain what the tests tell us.

Change to slide 6 and let Raed begin.

## Slide 6 - Raed - 3:45 to 4:45

> Thank you, Yusuf. I'm Raed Mardoum. We tested the built-up model on the eastern part of the area, away from its training data. Against ESA WorldCover, it reached F1 of 0.88, overlap of 0.78 and balanced accuracy of 0.89.

> Those numbers show agreement with a satellite reference. Field checks are still needed. They also test the built-up model, rather than the usefulness of the final ranking. Surface temperature differs from air temperature, and WorldPop is an estimate. Desert surfaces can still confuse the model. These are reasons to check the suggested areas locally.

## Slide 7 - Raed - 4:45 to 5:30

> We used more than one source because bright desert can resemble built land. Annual maps flag possible change, and optical and radar measurements check those places. In our Tanager comparison, likely-unbuilt ground had a higher median built-up index than established buildings. That shows why one threshold can mislead us here. The final score also shows its four parts, so a planner can see why an area ranks highly.

## Slide 8 - Raed - 5:30 to 6:15

> Next, we would ask planners and GIS staff how they choose inspection areas today. They would check our top five against local plans and visits to the area. We would record useful findings, false alarms and the time taken. Then we would adjust the weights and add missing local information, such as worker exposure. Finally, we would repeat the test in another part of Riyadh. That would tell us whether HeatReady saves staff time and gives them useful places to inspect. Thank you. We're ready for your questions.

## If something goes wrong

If the dashboard is slow, do not troubleshoot. Stay on slide 4 and say:

> The report contains the same map and ranked table shown here. The separate CSV and map files are also in our repository.

Short slide 5 if behind schedule:

> Annual maps proposed the growth. Optical and radar checks reduced it to 3.74 square kilometres. We ranked the eligible cells using heat, population, growth and vegetation, weighted 40, 30, 20 and 10 percent. Raed will explain the validation and the next test.

If running late on slide 8, use this short ending:

> We would test the top five areas with planning staff, measure useful findings and false alarms, and improve the score from their feedback. Thank you. We're ready for your questions.

Never open slides 9-10 during the main pitch. Use them only if a judge asks about sources or validation.

If Raed cannot attend the assigned final slot, Yusuf can use the same slides 6-8 content and omit Raed's personal introduction.
