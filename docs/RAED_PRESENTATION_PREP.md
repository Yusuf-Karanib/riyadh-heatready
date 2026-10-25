# Raed's presentation guide

Riyadh HeatReady | Team Milkaholics | Live deck v5

## Your job on the day

Present slides 6-8. Explain what the evidence shows, what makes this approach useful to test, and how a city team could evaluate it. Your subject is validation and the proposed city test.

Yusuf presents slides 1-5 and hands over around 3:45. Aim to finish around 6:15. Your part is about two minutes thirty seconds, roughly 40% of the planned presentation time.

## The project in plain words

> HeatReady combines separate satellite and population layers into a ranked map of one-kilometre areas in southeast Riyadh. It helps planning staff choose where to inspect first.

The study covers 168.3 square kilometres. The stricter growth rule retained 3.74 square kilometres. There are 67 eligible cells and 14 High cells. R05C10 ranks first at about 78.7.

The score weights are 40% surface heat, 30% estimated population, 20% retained growth and 10% low vegetation. These are assumptions chosen for the prototype.

## Study in this order

1. Read your exact words on pages 2-3 with slides 6-8 open.
2. Learn the three validation numbers on page 4.
3. Practise the city test and knowledge questions on page 5.
4. Answer the Raed questions in the shared judge guide aloud.
5. Rehearse the handoff and closing with Yusuf and a timer.

## Your role introduction

> I'm Raed Mardoum. My presentation covers the validation results and how planners could test the ranking.

This describes your responsibility. If asked about past work, describe only the review or preparation you have actually completed.

---

## Your exact words: slide 6

### Slide 6: How well the model matched the reference

Target: 3:45-4:45. Begin after Yusuf's handoff.

> Thank you, Yusuf. I'm Raed Mardoum. We tested the built-up model on the eastern part of the area, away from its training data. Against ESA WorldCover, it reached F1 of 0.88, overlap of 0.78 and balanced accuracy of 0.89.

> Those numbers show agreement with a satellite reference. Field checks are still needed. They also test the built-up model, rather than the usefulness of the final ranking. Surface temperature differs from air temperature, and WorldPop is an estimate. Desert surfaces can still confuse the model. These are reasons to check the suggested areas locally.

### Understand what you just said

- Built-up model: the part that predicts built versus unbuilt ground.
- Eastern test area: a geographic area kept out of training and threshold selection.
- WorldCover: the land-cover product used as reference labels.
- F1: balances finding built-up pixels with avoiding false alarms.
- Overlap: intersection over union, also called IoU.
- Balanced accuracy: gives the built and unbuilt classes equal importance.

These are 2021 classifier results. Applying that classifier to 2018 and 2025 adds uncertainty that this test does not measure.

### Where to point

Point to the three large numbers. Then point to the limitation text. If asked for details during Q&A, slide 10 contains the confusion matrix and the test sample size.

### If you lose your place

> The model agrees well with the satellite reference. The next check is whether the ranked areas are useful to real planners.

Continue to slide 7.

---

## Your exact words: slides 7-8

### Slide 7: Why we used more than one signal

Target: 4:45-5:30.

> We used more than one source because bright desert can resemble built land. Annual maps flag possible change, and optical and radar measurements check those places. In our Tanager comparison, likely-unbuilt ground had a higher median built-up index than established buildings. That shows why one threshold can mislead us here. The final score also shows its four parts, so a planner can see why an area ranks highly.

Point to the box plot, then the "WHY IT HELPS" sentence. Say "Tanager" as "TAN-uh-jer." Say NDBI as separate letters if a judge uses that term.

### Slide 8: How we would test it with planners

Target: 5:30-6:15.

> Next, we would ask planners and GIS staff how they choose inspection areas today. They would check our top five against local plans and visits to the area. We would record useful findings, false alarms and the time taken. Then we would adjust the weights and add missing local information, such as worker exposure. Finally, we would repeat the test in another part of Riyadh. That would tell us whether HeatReady saves staff time and gives them useful places to inspect. Thank you. We're ready for your questions.

Stop on slide 8. Slides 9-10 are for questions.

### If time is nearly finished

Use this shorter ending:

> We would test the top five areas with planning staff, measure useful findings and false alarms, and improve the score from their feedback. Thank you. We're ready for your questions.

### What makes it different, in one sentence

> We check possible growth with optical and radar evidence, then show the reasons behind each inspection priority.

The individual tools are established methods. The case for this entry is their application to this decision and the evidence provided, rather than a claim to have invented a new algorithm.

---

## Understand the validation

Imagine comparing our built/unbuilt prediction with the WorldCover labels, one pixel at a time. The test contains 36,156 pixels.

| Reference label | Predicted unbuilt | Predicted built |
| --- | --- | --- |
| Unbuilt | 18,281 | 1,845 |
| Built | 2,036 | 13,994 |

The diagonal entries are agreements. The other two are disagreements with WorldCover. They are not independently verified field mistakes.

### Precision: about 88.4%

Of the pixels our model calls built, about 88 out of 100 also have the built label in WorldCover. The formula is 13,994 / (13,994 + 1,845).

### Recall: about 87.3%

Of the pixels WorldCover labels built, our model finds about 87 out of 100. The formula is 13,994 / (13,994 + 2,036).

### F1: about 0.88

F1 combines precision and recall. Both must be strong for F1 to be strong. It does not mean that the final risk ranking is 88% correct.

### Intersection over union: about 0.78

Think of two sets of built-up pixels: ours and WorldCover's. Their shared pixels divided by all pixels labelled built by either gives the overlap score. Here that is 13,994 / (13,994 + 1,845 + 2,036).

### Balanced accuracy: about 0.89

It averages how well the model finds the built class and how well it finds the unbuilt class. This keeps the larger class from dominating the summary.

### The important boundary

WorldCover also uses Sentinel-1 and Sentinel-2. Its agreement with our model therefore does not supply independent ground truth. The geographic split reduces nearby training/test overlap, but it does not remove shared errors in the source and reference products.

Technical references: https://scikit-learn.org/stable/modules/model_evaluation.html and https://esa-worldcover.org/en

---

## What is proven, and what comes next

| Evidence available | What still needs testing |
| --- | --- |
| Working map, ranked table and GIS files | Whether staff choose better inspection areas |
| Spatial agreement with WorldCover | Independent field accuracy and transfer to other years |
| Visible score components | Whether users agree with the weights |
| One Tanager comparison | Wider performance across dates and sites |
| Code, settings and example notebook | Practical update cost and operational reliability |

### Explain Tanager without overclaiming

It measures many narrow bands of reflected light. Here it compares groups already defined by other satellite layers. Likely-unbuilt ground had median narrow-band NDBI about 0.084, compared with 0.049 for established built land. That is an example of desert confusion in this scene.

One image date cannot show when a building appeared. The comparison does not identify specific roofing materials or prove that radar improved accuracy over an optical-only model.

### A useful city test

Ask staff to review the same area using their current method and HeatReady. Record time, useful findings, false alarms and missing local information. Check some lower-ranked areas too, so a good finding missed by the ranking can be discovered. Test weight alternatives and repeat in another area. These are proposed activities, not completed results.

### Answering questions together

You lead on validation meaning, limitations, differences and the proposed pilot. Yusuf leads on source dates, code, scoring and the demonstration. Answer directly, then use one piece of evidence. If needed, say: "Yusuf can explain that processing step."

### Check your knowledge without notes

1. Does F1 0.88 validate the final ranking?
2. Why does a geographic test still need field checking?
3. What did the Tanager comparison show?
4. What happens after a planner sees a high score?
5. How would you measure useful impact?
6. Why check some lower-ranked cells during the pilot?

Answers: no, it tests classifier agreement; the reference is satellite-derived too; a built-up index can rank desert higher here; local review; compare time and useful findings with current practice; to look for missed priorities.

Evidence: outputs/validation_metrics.json, outputs/tanager_summary.json, outputs/results_summary.json and src/run_analysis.py. Describe your own preparation as completed only after doing it.
