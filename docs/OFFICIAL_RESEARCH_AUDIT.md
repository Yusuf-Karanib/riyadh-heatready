# Official hackathon research audit

**Checked:** 1 October 2026  
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
- Private onboarding and data-resource text supplied by Yusuf.
- Both webinar PDFs supplied by Yusuf. They are byte-for-byte identical copies of the same 22-slide deck.
- Both briefing video pages linked by the official website. Their public metadata was available, but a usable Q&A transcript was not.
- Official starter repository, its links, and its notebooks: `https://github.com/Tnecniv-Teikram/813-hyperspectral-hackathon`
- The quickstart, land-use/change, and Week 2 time-series notebooks supplied by Yusuf.
- The complete live participant onboarding guide, every direct provider/tool link relevant to this project, and all ten files in the current starter repository at commit `55d310a0cd3dadbf0ffb39563eb466570e01b73c`. Detailed findings are in `ONBOARDING_REPOSITORY_AUDIT.md`.
- Primary documentation for Sentinel-1, Sentinel-2, Landsat, ESA WorldCover, the Impact Observatory/Esri annual land-cover product, WorldPop Global2, Planet Tanager, STAC, and the other providers linked by the official data page.

The remote starter-repository head was also checked against the local copy. Both pointed to commit `55d310a0cd3dadbf0ffb39563eb466570e01b73c`, so the local training copy was current at the time of this audit.

## Current official rules

- **Team size:** 1–5 members. Individuals are welcome and cross-country teams are allowed.
- **Portal reality:** Yusuf's accepted portal team currently contains two registered accounts. Do not describe the official portal team as a one-person team while that remains true.
- **Technical expectation:** at least one member should have a relevant technical background; basic Python ability is expected in the team.
- **Youth rule:** at least 30% of the team must be age 35 or younger. The supplied evidence does not prove the ages of both registered accounts, so this remains a human eligibility check.
- **Format:** the core program is remote and part-time.
- **Official track:** Sustainable Urban Planning and Smart Cities. Yusuf's Cockpit names the assigned challenge **Urban Expansion, Land Use Change & Heat Risk**.
- **Required product:** a technically credible digital Proof of Concept that converts Earth-observation data into an actionable insight, decision-support tool, or operational service.
- **Hyperspectral data:** useful use receives extra consideration, but it is not mandatory.

## Current dates

| Event | Current official date |
|---|---|
| Solution development | 7 September–10 October 2026 |
| Submission-preparation webinars | 29 September–1 October 2026 |
| PoC submission deadline | **11 October 2026, 11:59 PM in the team creator's timezone** |
| PoC presentations and selection | 12–16 October 2026 |
| Incubation | 19 October 2026–11 January 2027 |
| Final presentations | 12–15 January 2027 |
| Awards | January–February 2027; exact ceremony date not confirmed |

The project uses **10 October** as its internal readiness target. This is a safety target, not an organizer deadline. If a newer authenticated Cockpit notice later gives a different explicit deadline, the newer Cockpit notice wins.

## Eligibility before PoC judging

The live official page currently requires the team to:

1. have completed registration and received eligibility confirmation;
2. have every team member registered and identified on the team page;
3. complete every required project section;
4. address an official theme;
5. submit in English with professional content;
6. upload the requested files under the submission instructions;
7. accept the submission requirements; and
8. opt into judging rather than withdraw.

Yusuf's approval evidence satisfies item 1. The exact form sections, formats, file-size limits, pitch duration, and AI-disclosure wording are still unavailable because the submission form has not opened in the supplied portal evidence.

## Current PoC judging criteria

The live official website and the webinar deck agree on seven criteria:

1. **Problem definition** — a clear, real problem.
2. **Technical soundness** — a strong, scalable method.
3. **Use of hyperspectral / EO data** — purposeful data use; useful hyperspectral work receives extra consideration.
4. **Product and delivery model** — clear outputs and a realistic way to deploy them.
5. **Innovation** — a meaningful difference from existing approaches.
6. **Impact and strategic alignment** — social, environmental, or economic value and regional/SDG alignment.
7. **Business viability** — a short business plan showing plausible economic potential.

Judges score individually, and the technical score is the stated tie-breaker. No weights are published, so this project does not invent any.

## Data-access interpretation

- The official guidance consistently supports Sentinel-2, Sentinel-1, Landsat, open Planet examples, and other open datasets as the safe starting point.
- On 27 September, the National Space Academy team answered Yusuf in the authenticated mentor chat. They instructed teams to build the PoC baseline with open data such as Sentinel-2, Sentinel-1, and Landsat, using their own tools.
- The same answer says gIQ access and sponsored imagery are for shortlisted teams after PoC evaluation. Satellite 813 data will be shared when it becomes available.
- This authenticated answer resolves the earlier conflict between the public promotional language and the private onboarding warning.

**Project decision:** keep the complete PoC reproducible with open data. This is now confirmed by the organizer rather than merely being a cautious interpretation. Any later sponsored, gIQ, Satellite 813, or MBZ-SAT access may support a future shortlisted-stage improvement, but it is not a PoC dependency.

## Missing 29 September orientation material

- The authenticated Learning Track lists **Orientation session 29-9**, described as slides from the hackathon orientation session.
- Opening that row displays **“No PDF URL configured.”** This is a portal configuration problem, not a missing step on Yusuf's computer.
- A check of the public official website, indexed official pages, and the platform's publicly served application assets found the error component but no PDF address or publicly indexed copy of the orientation slides or recording.
- This does not prove that no recording exists. It means the material cannot currently be recovered from the accessible official sources and should be requested from the organizers.

## Important source conflicts

| Topic | Conflicting evidence | Decision used |
|---|---|---|
| PoC deadline | Live site, webinar, and GitHub Key Dates say 11 October; one old GitHub table says 26 October | Use **11 October 2026, 11:59 PM creator timezone** |
| Judging | Live site and webinar list 7 criteria; GitHub lists 5 older criteria | Use the live **7 criteria** |
| Team size | Live site says 1–5; older registration/GitHub language says 2–5 or 3–5 | Use live 1–5 generally; use the accepted two-account portal team for Yusuf's actual eligibility |
| Training dates | Older webinar slide begins in August; live site begins 7 September | Use the live site |
| GIQ/commercial data | Live site suggests access; onboarding says not guaranteed; the organizer later clarified the stage | Open Sentinel/Landsat data for the PoC; gIQ and sponsored imagery only for shortlisted teams after PoC evaluation |
| Exact submission files | Live site says required files and supporting documents; private form is still closed | Keep a flexible verified package and adapt when the form opens |

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

1. Exact portal fields and word limits.
2. Accepted upload types and maximum sizes.
3. Whether a repository must be public or private.
4. Required slide, video, demo, or report format and pitch duration.
5. Required AI-assistance wording.
6. Whether the missing 29 September orientation recording exists and when the broken PDF link will be fixed.
7. When Satellite 813 data will become available and what later-stage access will apply if the team is shortlisted.

These unknowns do not block the open-data PoC. They block only the final portal-specific packaging and submission.
