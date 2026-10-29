# Riyadh HeatReady: short solo script

Use the **v6 live slides**. You present slides 1-8. Keep slides 9-10 for questions.

Read the indented paragraphs aloud. The smaller text gives instructions. Aim for **about 5:30**, including the brief demonstration and slide changes. The official limit is eight minutes. Check your pace once with a timer.

Before you start, open the report at **Inspect these zones first**. Keep this script outside the window you share.

## Slide 1: Our team

> Hello, I'm Yusuf Karanib, an early-career AI and cloud developer based in the UAE. I'm presenting for Team Milkaholics. My teammate, Raed Mardoum, studies Computer Engineering at AUS and focuses on AI and machine learning. Raed can't join today, so I'll present for both of us.

## Slide 2: Where should planners inspect first?

> Our project is Riyadh HeatReady. It gives planners a map and a ranked list to help them choose where to inspect first.

## Slide 3: The problem and our answer

> We looked at 168 square kilometres in southeast Riyadh. The problem we're tackling is choosing inspection areas when the evidence is spread across separate maps.
>
> We bring growth, surface heat, population and vegetation together, then rank one-kilometre areas with detected growth. Planners can review that list before deciding where to visit.

Change to slide 4. Try to reach this point by about **1:20**.

---

## Slide 4: Where planners should inspect first

> Our checks kept 3.74 square kilometres of possible growth. Sixty-seven areas qualified for ranking, and fourteen received the High label. R05C10 came first at 78.7 points. These scores give us an inspection order.

Switch to the report. Point to the map and the first table row. Keep the whole demonstration within **20 seconds**. Say:

> Here's the report. The map and table show the same ranking. Staff can also use the exported data in their own GIS.

Return to the slides and change to slide 5.

## Slide 5: The data behind the answer

> We started with annual land-cover maps. They suggested 13.82 square kilometres of growth between 2018 and 2023. We checked those places with Sentinel-2 optical images and Sentinel-1 radar, comparing 2018 and 2025. Only 3.74 passed our checks.
>
> For the ranking, Landsat provided surface heat for one day in May 2025. WorldPop provided estimated population, and Sentinel-2 provided vegetation.
>
> We rank the values among eligible areas, then combine them using 40 percent heat, 30 percent population, 20 percent growth and 10 percent low vegetation. Those weights are our starting choices. They need testing with planners.

Change to slide 6. Try to reach it by about **3:30**.

---

## Slide 6: How well the model matched the reference

> We tested the built-up model in the east, away from its training and tuning areas. Its F1 score was 0.88 against WorldCover 2021. F1 balances false alarms and missed built-up pixels.
>
> WorldCover comes from satellites, so ground checks are still needed. We also haven't tested whether the final ranking helps planners yet. Surface heat differs from air temperature, and population estimates can miss workers.

## Slide 7: Why we used more than one signal

> In our Tanager image, likely-unbuilt ground had a higher median built-up index than established buildings. That shows why relying on one index can mislead us in bright desert.
>
> Our approach checks more than one source. It also lets a planner see what contributed to each score.

## Slide 8: How we would test it with planners

> Next, we'd test this with planners. They'd review the top five areas and some lower-ranked ones, using local plans and site visits.
>
> We'd measure useful findings, false alarms and time taken, then adjust the score and repeat elsewhere. That test hasn't happened yet. For now, we have a working map and list ready for that review.
>
> Thank you. I'm happy to take your questions.

Stop. Aim to finish around **5:30**, leaving time for pauses or interruptions. The timing is a rehearsal target, not a measured speaking time.

---

## If something goes wrong

Use these only as replacements. Do not add them to the main speech.

### If the report will not open

Stay on slide 4, point to its map and chart, and say:

> The same map and table are in our saved report. I'll continue with how we made them.

Go straight to slide 5. Leave troubleshooting until after the pitch.

### If you reach slide 5 after four minutes

Replace its speech with:

> Annual maps suggested growth. Optical and radar checks narrowed it to 3.74 square kilometres. We then ranked the areas using heat, population, growth and low vegetation. The score weights still need testing with planners.

### If the moderator says time is almost finished

Move to slide 8 and say:

> The next step is to check these areas with planners and measure whether the list helps them. Thank you. I'm happy to take your questions.

### If you lose your place

> The main point is helping planners choose where to inspect first.

Then continue with the next slide.

The separate `JUDGE_QUESTIONS_AND_ANSWERS.pdf` has the detailed answers. You do not need to read those details during the pitch.
