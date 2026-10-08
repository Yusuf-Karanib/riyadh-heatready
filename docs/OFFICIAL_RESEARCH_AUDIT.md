# Official hackathon research audit

**Checked:** 8 October 2026
**Purpose:** separate current official rules from older guidance and technical training material.

## Source order used when information conflicts

1. The newest authenticated Dashboard or Cockpit notice.
2. The live official hackathon website.
3. The official webinar slides and organizer announcements.
4. The private onboarding and learning-track material supplied by Yusuf.
5. The official starter GitHub repository.
6. Primary documentation from the actual data provider.

The starter repository is useful for code and learning, but it contains older dates, team rules, and judging criteria. It is not used as the final authority for those points.

## Material checked

- Live official program page: `https://spaceacademy-hackathons.space.gov.ae/`
- Live official data page and every relevant provider link: `https://spaceacademy-hackathons.space.gov.ae/data`
- Registration page: `https://spaceacademy-hackathons.space.gov.ae/register`
- Authenticated portal screenshots supplied by Yusuf: approval, Cockpit, team, Tasks, learning track, FAQ, notifications, submission area, and mentor chat.
- The 27 September organizer reply in the authenticated mentor chat and the 29 September orientation-resource error supplied by Yusuf.
- Yusuf's complete 1 October recording of the official **Detailed PoC Submission Process** orientation, including the displayed form, slides, live questions, and answers.
- Live official PoC submission guide and every direct link it contains: `https://spaceacademy-hackathons.space.gov.ae/guides/poc-submission-guide.html`
- Private onboarding and data-resource text supplied by Yusuf.
- Both webinar PDFs supplied by Yusuf. They are byte-for-byte identical copies of the same 22-slide deck.
- All three official public orientation recordings, including their slides, platform demonstrations, captions, and Q&A:
  - **1st Orientation Session:** `https://www.youtube.com/watch?v=942fmaGOHGk`
  - **2nd Orientation Session:** `https://www.youtube.com/watch?v=LZtVr-1ER2c`
  - **Special Technical Orientation Session:** `https://www.youtube.com/watch?v=w35Y_sM_e2Y`
- Official starter repository, its links, and its notebooks: `https://github.com/Tnecniv-Teikram/813-hyperspectral-hackathon`
- The quickstart, land-use/change, and Week 2 time-series notebooks supplied by Yusuf.
- The complete current preparatory-training set supplied on 8 October: kickoff, remote-sensing, machine-learning, GDAL, hyperspectral, and deep-learning decks; the two example CSV files; the GDAL and time-series notebook text; and both copies of the deep-learning notebook. Detailed findings are in `PREP_TRAINING_AUDIT_2026-10-08.md`.
- The complete live participant onboarding guide, every direct provider/tool link relevant to this project, and all ten files in the current starter repository at commit `55d310a0cd3dadbf0ffb39563eb466570e01b73c`. Detailed findings are in `ONBOARDING_REPOSITORY_AUDIT.md`.
- Primary documentation for Sentinel-1, Sentinel-2, Landsat, ESA WorldCover, the Impact Observatory/Esri annual land-cover product, WorldPop Global2, Planet Tanager, STAC, and the other providers linked by the official data page.

The remote starter-repository head was also checked against the local copy. Both pointed to commit `55d310a0cd3dadbf0ffb39563eb466570e01b73c`, so the local training copy was current at the time of this audit.

## Current official rules

- **Team size:** 1–5 members. Individuals are welcome and cross-country teams are allowed.
- **Portal reality:** Yusuf's accepted portal team currently contains two registered accounts. Do not describe the official portal team as a one-person team while that remains true.
- **Nationality:** every team member must be a national of one of the 22 Arab League states.
- **Youth rule:** at least 30% of the team must be age 35 or younger on 11 October 2026. A solo participant older than 35 must add an eligible member aged 35 or younger. The supplied evidence does not prove the ages or nationalities of both registered accounts, so these remain human checks.
- **Team lock:** team changes close on 4 October; open cases are settled by 5 October. A team not confirmed by 5 October does not proceed. A person belongs to the most recent team they joined.
- **Format:** the core program is remote and part-time.
- **Official track:** Sustainable Urban Planning and Smart Cities. Yusuf's Cockpit names the assigned challenge **Urban Expansion, Land Use Change & Heat Risk**.
- **Required product:** a working, demonstrable slice that proves the idea is feasible with data. A written report alone is not a PoC.
- **Evaluation intent:** this is not a Kaggle-style model leaderboard. The organizers prefer a complete, usable solution with a path to an MVP or business over a technically complex model presented without an end-user workflow.
- **Space-data gate:** Earth-observation or other space data must be core to the result. A complete entry that does not rest on space data is not scored. Drone, field, or other data may support but not replace it.
- **Hyperspectral data:** meaningful use that improves the result can earn bonus consideration, but it is not mandatory.
- **Submission:** both the platform form and the linked GitHub repository are required. A form without its registered repository, or a repository not registered in the form, is invalid.
- **Repository access:** the public orientations repeatedly instruct teams to make the GitHub repository public. This is the operational rule used by the checklist even though the written guide still mentions a private-repository access route.
- **Submission page:** the organizers confirmed during the second orientation that the PoC submission tab had been activated. Yusuf should now see it in the Cockpit.

## Current dates

| Event | Current official date |
|---|---|
| Solution development | 7 September–10 October 2026 |
| Submission-preparation webinars | 29 September–1 October 2026 |
| Team changes close | **4 October 2026** |
| Open team cases settled | **5 October 2026** |
| PoC submission deadline | **11 October 2026, 11:59 PM**; the guide says creator-local time and the orientation slide says UAE time. Both are the same for Yusuf. |
| Administrative validation | 12–13 October 2026 |
| Top 40 announcement and pitch-slot link | 13 October 2026, by email and platform alert |
| Top 40 pitches | 14–16 October 2026; 10-minute presentation plus 5-minute questions |
| Incubation | 19 October 2026–11 January 2027 |
| Final demonstrations and awards | 12–15 January 2027; exact award-ceremony date not confirmed |

The project uses **10 October** as its internal readiness target. This is a safety target, not an organizer deadline. If a newer authenticated Cockpit notice later gives a different explicit deadline, the newer Cockpit notice wins.

## Required submission contents

The form displayed in the official orientation contains:

1. project title;
2. one-line summary of what the PoC does, with a 2,000-character maximum;
3. GitHub URL, public or private with access granted to the evaluation account;
4. presentation slides as PDF only, maximum 50 MB;
5. optional supporting ZIP, maximum 200 MB;
6. confirmation that the repository contains a README, an end-to-end Jupyter notebook, pinned `requirements.txt`, example input and output, and no credentials or restricted imagery; and
7. confirmation that organizers can access the repository.

Email submissions do not count. Every link must work for someone outside the team.

The repository validation checks for an accessible repository, root README, executable `.ipynb`, pinned requirements, sample input, committed output, business use case, installation commands, and PDF slides. The notebook must restart and run all cells without errors, use relative paths, set random seeds where relevant, and keep visible outputs.

The README must present, in order: title/summary; business use case; problem and satellite need; data and licences; technical approach; installation; how to run; example input/output; results and limitations; team/licence/attribution.

The PDF slides must cover, in order: title; problem; business user; data and hyperspectral role; workflow; large readable example outputs; validation and limitations; impact; and next incubation steps.

The submitted PDF may contain extra appendix slides. Only the live pitch must fit ten minutes. Judges can score answers given during the five-minute question period, so the appendix should hold traceability and validation details rather than extend the spoken pitch.

## Current PoC judging criteria

Two official descriptions are still visible and both are treated as relevant.

The current public site and the September kickoff deck list seven detailed PoC criteria:

1. **Problem definition** — clarity and real-world relevance.
2. **Technical soundness** — methodology quality, robustness, and scalability.
3. **Hyperspectral or other EO data use** — meaningful use, with bonus credit for effective hyperspectral use and Satellite 813 when available.
4. **Product and delivery model** — clear decision output, insight, API, or analytics service with a plausible deployment path.
5. **Innovation** — distinction from existing approaches.
6. **Impact and strategic alignment** — societal, environmental, or economic value plus regional and SDG alignment.
7. **Business viability** — a short, credible path showing possible economic value.

The detailed 1 October submission orientation groups review into five broader operational headings: **quality of space-data use, team strength and expertise, problem relevance and impact, innovation, and feasibility**. It also states that technical evidence decides ties.

These formulations overlap. The project covers their union instead of assuming that one silently cancels the other. The organizers did not publish numeric weights, so this project does not invent any. Clear communication is explicit judging advice, not an additional numbered criterion.

Three optional bonuses were stated:

- progress beyond a basic PoC, such as working features, a pilot, or deployment;
- hyperspectral data used in a way that improves the result; and
- evidence of contact with at least three real users or stakeholders.

Riyadh HeatReady can claim working features and a useful open Tanager analysis. It does **not** claim the user-validation bonus because no three-user contact has occurred.

## Data-access interpretation

- The official guidance consistently supports Sentinel-2, Sentinel-1, Landsat, open Planet examples, and other open datasets as the safe starting point.
- On 27 September, the National Space Academy team answered Yusuf in the authenticated mentor chat. They instructed teams to build the PoC baseline with open data such as Sentinel-2, Sentinel-1, and Landsat, using their own tools.
- The same answer says gIQ access and sponsored imagery are for shortlisted teams after PoC evaluation. Satellite 813 data will be shared when it becomes available.
- This authenticated answer resolves the earlier conflict between the public promotional language and the private onboarding warning.

**Project decision:** keep the complete PoC reproducible with open data. This is now confirmed by the organizer rather than merely being a cautious interpretation. Any later sponsored, gIQ, Satellite 813, or MBZ-SAT access may support a future shortlisted-stage improvement, but it is not a PoC dependency.

## Recovered orientation material

- The authenticated Learning Track PDF row still displays **“No PDF URL configured.”** This is a portal configuration problem, not a missing step on Yusuf's computer.
- The organizers have now published the first, second, and special technical orientation recordings on YouTube. These recordings recover the important spoken guidance, slide content, platform demonstration, and Q&A even though the PDF row remains broken.
- The first and second orientations confirm the PoC rules and submission process. The special technical session mainly concerns the biosecurity track; its problem-first design advice is useful across themes, but its biosecurity examples are not rules for Yusuf's urban track.

## Important source conflicts

| Topic | Conflicting evidence | Decision used |
|---|---|---|
| PoC deadline | Current guide says 11:59 PM in the team creator's local time; orientation slide says UAE time; one old GitHub table says 26 October | Use **11 October 2026, 11:59 PM UAE time** for Yusuf because he is the UAE-based creator |
| Judging | The current public site and kickoff deck list seven detailed criteria; the detailed 1 October orientation groups review into five broader headings and bonuses | Cover the **union of both official descriptions**, keep the space-data gate and technical tie-breaker, and invent no weights |
| Team size | Live site says 1–5; older registration/GitHub language says 2–5 or 3–5 | Use live 1–5 generally; use the accepted two-account portal team for Yusuf's actual eligibility |
| Training dates | Older webinar slide begins in August; live site begins 7 September | Use the live site |
| GIQ/commercial data | Live site suggests access; onboarding says not guaranteed; the organizer later clarified the stage | Open Sentinel/Landsat data for the PoC; gIQ and sponsored imagery only for shortlisted teams after PoC evaluation |
| Repository visibility | The written guide mentions public or private with evaluator access; the public orientations repeatedly say the repository must be public | Use a **public repository** unless organizers give Yusuf a written exception. Test the URL while signed out. |
| Validation correction window | The guide contains an organizer placeholder rather than a final rule | Do not assume a correction window exists |

## Technical findings that affect this project

- Sentinel-2 L2A is bottom-of-atmosphere reflectance with 10–60 m bands and a scene-classification layer. The project uses that quality layer rather than relying only on scene-level cloud percentage.
- Sentinel-1 RTC is terrain-corrected C-band radar and is licensed CC BY 4.0 on Microsoft Planetary Computer. The project uses it as structural evidence, not as a direct building label.
- Landsat Collection 2 Level-2 contains atmospherically corrected surface reflectance and surface temperature. The project correctly labels the thermal result as land-surface temperature, not air temperature.
- ESA WorldCover 2021 is a 10 m Sentinel-1/Sentinel-2 product under CC BY 4.0. It is used only as a satellite-derived reference; its agreement score is not field accuracy.
- The annual Impact Observatory/Esri 9-class product covers 2017–2023 at 10 m, reports average assessed accuracy over 75%, and is CC BY 4.0. It is supporting trend evidence, not an exact construction register.
- WorldPop Global2 R2025A is a modelled, alpha-release population product. Its values are people per grid cell, not census counts, and may change as the product is improved.
- Planet Tanager records 426 narrow bands for the selected item, spanning wavelength centres of 376.44–2499.0 nm. Its STAC metadata reports nominal GSD 32.7 m, while its orthorectified HDF5 grid spacing is exactly 30 m. The open Riyadh collection is CC BY 4.0. One scene can add surface-spectral context but cannot prove change by itself.

## Training-notebook findings

The official notebooks are teaching examples, not submission rules or validated city products.

- The quickstart correctly teaches small AOIs, STAC, cloud-aware analysis, and strategic hyperspectral use.
- The land-use notebook's narrative says Riyadh, but its first selected item is a Ho Chi Minh City scene. The Riyadh item is a later item in the collection. This project uses the exact Riyadh scene ID instead of blindly using the first item.
- The teaching classification relies heavily on NDBI/BUI thresholds. That is unsafe in bright desert because bare soil can look built-like. Riyadh HeatReady uses optical, radar, reference land cover, and a separate hyperspectral sensitivity check.
- The Week 2 time-series idea was useful, so the project added six actual annual maps. Its interpolation, resizing, and six-point change-break examples were not copied as proof.

## What remains genuinely unknown

1. Whether teams receive an automated validation report or any correction window; the live guide leaves this as an organizer placeholder.
2. When the broken orientation PDF link will be fixed.
3. When Satellite 813 data will become available and what later-stage access will apply if the team is shortlisted.

These unknowns do not block the open-data PoC. The GitHub repository was confirmed public and anonymously accessible on 3 October 2026.
