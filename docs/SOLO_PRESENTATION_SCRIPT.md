# Riyadh HeatReady: Yusuf's solo script

For the confirmed 29 October 2026 pitch. Use the **v6 live presentation**. Yusuf presents all eight main slides because Raed cannot attend. Slides 9 and 10 stay available for questions.

Read the indented speech paragraphs aloud. The smaller text gives instructions. The full spoken text includes the short demonstration. Aim to finish in **6:30 or less**, leaving room within the official eight minutes. Check your actual time aloud.

Before starting, open the slides and `outputs/dashboard.html`. In the report, find **Inspect these zones first** and leave the ranked map and table ready. Keep this script on another device or beside the slides. Share the slides or report window so your notes remain private.

## Slide 1: Our team

> Hello, I'm Yusuf Karanib from Team Milkaholics. I'm an early-career AI and cloud developer based in the UAE. My teammate, Raed Mardoum, studies Computer Engineering at AUS and specialises in AI and machine learning. Raed can't join today, so I'll present for our team.

Change to slide 2.

## Slide 2: Where should planners inspect first?

> Our project is Riyadh HeatReady. The question is simple: if a planning team can visit only a few areas, where should it start?

Change to slide 3.

## Slide 3: The problem and our answer

> We focused on 168 square kilometres in southeast Riyadh. Planners may need to compare separate maps of growth, surface heat, population and vegetation before choosing where to visit.

> HeatReady combines those layers and ranks one-kilometre areas. It gives staff a starting point for inspection. They can then check local conditions and decide what action is appropriate. We still need municipal users to test how well it fits their work.

---

## Slide 4: Where planners should inspect first

> Here is the result. Our stricter checks retained 3.74 square kilometres of possible built-up growth. Sixty-seven areas met the ranking rules, and fourteen received the High label.

> R05C10 came first at about 78.7 points. The chart shows how heat, population, growth and low vegetation contribute to each score. A high score is a reason to inspect an area early.

Switch to the report that you opened before the pitch. Spend **no more than 25 seconds** showing the ranked map and top-five table. You can point to them without clicking anything. Say:

> This is the working report. Here is the ranked map, and here is the table with R05C10 first. The same results are available as a CSV table and GIS files, so staff can review them in their own tools.

Return to the slides. Change to slide 5. The report is static: there are no live filters or zone-selection controls to demonstrate.

---

## Slide 5: The data behind the answer

> Each source had a job. Annual land-cover maps flagged possible growth between 2018 and 2023. Sentinel-2 optical data and Sentinel-1 radar checked whether those places looked built-up in 2025 and more built-like than in 2018. That reduced 13.82 square kilometres of candidate growth to 3.74. Passing these checks still needs confirmation on the ground.

> Landsat supplied surface temperature for one day in May 2025. WorldPop supplied estimated population, and Sentinel-2 supplied vegetation.

> We compared each area with the other eligible areas, then combined the results using 40 percent heat, 30 percent population, 20 percent growth and 10 percent low vegetation. Those weights are starting choices for the prototype. They need testing with planners. Tanager supplied an additional check on confusion between desert and built surfaces.

Change to slide 6. You continue presenting. There is no handover to Raed.

---

## Slide 6: How well the model matched the reference

> We trained the built-up model in the west, chose its cut-off in a separate middle strip, and tested it in the east. Against ESA WorldCover, it reached F1 of 0.88, overlap of 0.78 and balanced accuracy of 0.89.

> F1 balances false alarms and missed built-up pixels. The important boundary is what we tested: agreement with a satellite reference in 2021. These scores do not establish field accuracy or prove that the final inspection ranking is useful.

> Surface temperature also differs from air temperature, and population estimates can miss workers. Local checks remain necessary.

Change to slide 7.

## Slide 7: Why we used more than one signal

> Bright desert can resemble built land. In our Tanager comparison, likely-unbuilt ground had a higher median built-up index than established buildings. A simple threshold could therefore give the wrong impression here.

> That is why we check possible growth using more than one source. We also keep the four score components visible, so a planner can see why an area ranks highly. Our contribution is this screening workflow, using established methods.

Change to slide 8.

---

## Slide 8: How we would test it with planners

> The next step is to test the ranking with planning and GIS staff. We would ask how they choose inspection areas today, then compare our top five with local plans and site visits. We would include some lower-ranked areas to look for priorities we missed.

> We would record useful findings, false alarms and time taken, adjust the weights, and repeat in another part of Riyadh. We have not run that pilot yet.

> HeatReady gives planners a clear first list to investigate, with the evidence behind it. The next test is whether that list actually helps them. Thank you. I'm ready for your questions.

Stop speaking. Stay on slide 8. Open slide 9 only for source/date questions, or slide 10 for validation questions.

---

## If something goes wrong

These are replacements, not extra lines to add to the main script.

### If the report does not open

Stay on slide 4 and replace the demonstration paragraph with:

> The report contains the same map and ranked table shown here. The CSV and GIS files are also in our repository.

Continue to slide 5. Do not spend your presentation time fixing the report.

### If you reach slide 5 after four minutes

Replace the whole slide 5 speech with:

> Annual maps proposed the growth. Optical and radar checks reduced it to 3.74 square kilometres. We ranked the eligible areas using heat, population, growth and low vegetation, weighted 40, 30, 20 and 10 percent. The weights need testing with users.

### If time is nearly finished

Go to slide 8 and use this ending:

> Our next step is a pilot with planners, checking useful findings, false alarms and time taken. HeatReady provides a first inspection list. Local evidence determines the action. Thank you. I'm ready for your questions.

### If you lose your place

> The main point is that we turn several maps into one inspection list, and show the evidence behind each area.

Then move to the next slide. Follow the moderator if asked to stop.

Study this with the separate `JUDGE_QUESTIONS_AND_ANSWERS.pdf`. The speaking-time estimate is a planning guide, not evidence of a completed rehearsal.
