# Detailed PoC Submission Process — verified orientation audit

**Reviewed:** 3 October 2026
**Source:** Yusuf's complete recording of the official 1 October orientation, the three official public orientation recordings, the live official submission guide, the displayed platform form, and every linked resource relevant to this entry.
**Official guide:** `https://spaceacademy-hackathons.space.gov.ae/guides/poc-submission-guide.html`

Public recordings:

- First orientation: `https://www.youtube.com/watch?v=942fmaGOHGk`
- Second orientation: `https://www.youtube.com/watch?v=LZtVr-1ER2c`
- Special technical orientation: `https://www.youtube.com/watch?v=w35Y_sM_e2Y`

The private recording and transcript remain in the ignored `work/` folder. They are not included in GitHub or the submission ZIP.

## What a valid PoC means

- It is a working, demonstrable slice that proves the idea can work with data, not a finished product.
- Satellite or other space data must be a core input. A complete project that does not rest on space data is not scored.
- The orientation recommends one focused problem, a simple baseline, repeatable execution, and iteration before complexity.
- This is not a Kaggle-style model leaderboard. The organizers said they prefer a holistic solution that can become an MVP or business over a complicated model built only to push technical performance.
- In the Q&A, the organizers confirmed that an executable notebook is the minimum. A written report alone is insufficient.

Relevant recording sections: first orientation 19:27–20:22 and 56:09–57:14; second orientation 58:35–1:00:12.

## Team and eligibility

- Team size: 1–5.
- Every member must be a national of one of the 22 Arab League states.
- At least 30% must be 35 or younger on 11 October 2026.
- A solo participant older than 35 must add a qualifying younger member.
- Team changes close 4 October. Open team cases are settled by 5 October.
- A team that is not confirmed by 5 October does not proceed.
- A person belongs to the most recent team they joined.

The portal shows two registered accounts for Milkaholics. Their eligibility remains a human check; this project does not invent ages, nationalities, skills, or contributions.

Relevant recording section: 20:24–21:20.

## Required submission

Both parts are mandatory:

1. the PoC form on the hackathon platform; and
2. the GitHub repository registered in that form.

Email does not count. A form without its repository, or a repository not registered in the form, is invalid.

### Form fields shown

| Field | Confirmed rule |
|---|---|
| Project title | Required |
| One-line summary | What the PoC does; maximum 2,000 characters |
| GitHub URL | Use a public repository. The written guide mentions private access, but the public orientations repeatedly instruct teams to make the repository public. |
| Presentation slides | PDF only; maximum 50 MB |
| Supporting archive | Optional ZIP; maximum 200 MB |
| Repository-content checkbox | Confirms README, end-to-end notebook, pinned requirements, example input/output, and no credentials or restricted imagery |
| Access checkbox | Confirms organizers can open the repository |

Relevant recording section: 41:13–43:44. Exact field limits were verified against the live guide and displayed form because automated speech recognition does not reliably capture small on-screen text.

## Repository validation

Blocking checks include:

- repository opens for an evaluator;
- root `README.md` exists;
- at least one functioning `.ipynb` runs end to end;
- `requirements.txt` uses pinned versions;
- example input and committed output exist;
- the business user and decision are stated;
- exact installation commands are present; and
- the PDF slides are supplied.

Notebook rules:

- restart the kernel and run all cells without errors;
- use relative paths;
- record exact scene IDs, dates, and parameters;
- set random seeds where randomness is used;
- keep visible outputs in the committed notebook; and
- include no credentials, restricted imagery, full scenes, model weights, or large intermediate rasters.

Recommended but not blocking: a Colab badge, `environment.yml` or Dockerfile, a code licence, and a 2–3 minute demo.

## Required README order

1. title and one-line summary, including project/team/theme;
2. business use case: user, decision, and what they use today;
3. problem, scale, and why satellite data are needed;
4. data: product, provider, dates, processing, and licence;
5. technical approach and execution order;
6. installation commands and Python version;
7. how to run the notebook, expected runtime, and outputs;
8. linked and embedded example input/output;
9. results, validation, assumptions, limitations, and failure cases; and
10. team, roles, code licence, data licence, and attribution.

## Required PDF slide order

1. title, project, team, theme, and country;
2. problem and affected group;
3. business use case and end user;
4. data and the role of hyperspectral data;
5. technical workflow diagram;
6. large, readable real outputs;
7. validation and limitations;
8. expected impact; and
9. next incubation steps.

The slides must show real PoC outputs rather than stock pictures of a system that was not built.

The first public orientation adds two useful clarifications:

- the submitted PDF may include extra appendix slides even though the spoken pitch must remain ten minutes; and
- answers in the five-minute question period count toward the score when the main slides do not cover a detail.

Riyadh HeatReady therefore keeps slides 1–9 as the timed pitch and uses slides 10–12 only as judge-reference appendices.

## Judging

Every complete entry first passes the space-data gate. Reviewers then score independently on:

1. **quality of space-data use** — stated as the heaviest criterion;
2. **team strength and expertise**;
3. **problem relevance and impact**, including a clear user group;
4. **innovation**; and
5. **feasibility** under real conditions.

Ties are decided by the technical score: feasibility plus quality of space-data use. Numeric weights were not published.

Bonus consideration is available for:

- progress beyond the basic PoC;
- hyperspectral data that improves the result; and
- evidence of contact with at least three real users or stakeholders.

No user-validation bonus is claimed for Riyadh HeatReady because no three-user contact has occurred.

Relevant recording section: 21:21–24:01.

## Dates and pitch process

| Stage | Confirmed date or rule |
|---|---|
| Team changes close | 4 October 2026 |
| Open team cases settled | 5 October 2026 |
| PoC deadline | 11 October 2026, 23:59 |
| Administrative validation | 12–13 October |
| Top 40 notification | 13 October, by email and platform alert |
| Online pitches | 14–16 October |
| Pitch format | 10 minutes presenting + 5 minutes questions |
| Incubation begins | 19 October |
| Final demonstrations/awards | 12–15 January 2027; ceremony date still to be confirmed |

The live guide describes the deadline as local time for the team creator, while the orientation slide says UAE time. Yusuf is the UAE-based team creator, so both produce the same deadline for this team.

Pitch slots are first come, first served. One member may present for the team. A no-show scores zero and cannot move forward. Shortlisted members must have valid identification for verification.

The special technical orientation also confirms that solo entries are judged on the merit of the submission and that the requirements were designed to be achievable by individuals. It does not remove the normal eligibility rules.

Relevant recording sections: 28:34–32:07.

## Link and resource verification

Forty-four official or directly linked pages were checked. Thirty-eight opened normally. Six provider or organization pages returned certificate or anti-bot errors in the automated check; this does not prove the pages are unavailable to a normal browser.

Working links included the official platform, onboarding/data pages, submission guide, official starter repository, Copernicus resources, Planet Tanager STAC collections, Microsoft Planetary Computer/STAC, public kickoff videos, Colab, pip requirements guidance, and licensing guidance.

The guide still contains an organizer placeholder about whether teams receive an automated validation report or a correction window. No correction window is assumed.

## Corrections made to Riyadh HeatReady

- Added a tested end-to-end notebook with visible outputs.
- Added a small sample input and committed example output under the requested folder pattern.
- Pinned JupyterLab in `requirements.txt`.
- Rebuilt the README in the exact ten-part order.
- Added the required nine-part PDF pitch deck.
- Added three appendix slides for data traceability, validation logic, and likely judge questions while keeping the timed pitch at nine slides.
- Updated the scoring strategy from older seven-part public language to the detailed five-criterion rubric and bonuses.
- Kept the raw orientation recording, transcript, credentials, and large satellite files out of GitHub.

## Remaining human actions

- Make the GitHub repository public and test it while signed out. This requires Yusuf's approval because it changes external visibility.
- Confirm both portal accounts meet nationality and age eligibility and confirm the second account's real role.
- Review every final claim and choose a code licence.
- Submit through the platform; this project does not submit automatically.
