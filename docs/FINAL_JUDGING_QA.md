# Final judging Q&A

Keep answers short. Answer the question first, then add evidence.

## Team capability

### What did Yusuf contribute?

**Owner: Yusuf**

I am the project lead and data/method presenter. My responsibility is to explain the problem, Earth-observation workflow, scoring method, demonstration, and reproducibility.

### What did Raed contribute?

**Owner: Raed**

My finals responsibility is to explain the validation evidence and its limits, the ranked-zone workflow, the solution's innovation and expected impact, and the municipal pilot plan.

## Space data and analytics

### Why is space data essential?

**Owner: Yusuf**

The result depends on repeatable, city-scale evidence of built structure, land-cover change, surface temperature, vegetation and population context. Without the satellite layers, the ranked zones cannot be produced.

### Why use both Sentinel-2 and Sentinel-1?

**Owner: Yusuf**

Sentinel-2 provides optical and vegetation features. Sentinel-1 provides radar structure. Combining them reduces dependence on a single optical index in bright desert conditions.

### Why not use NDBI alone?

**Owner: Yusuf**

Bright bare surfaces can have a high NDBI. In this case, the open Tanager scene showed likely-unbuilt surfaces with higher median narrow-band NDBI than established-built surfaces. Multiple evidence sources are safer.

### Did you use Satellite 813?

**Owner: Yusuf**

No. The PoC uses open Sentinel, Landsat, WorldCover, WorldPop, annual land-cover and Planet Tanager data. Satellite 813 data were not available for the PoC baseline.

## Scientific validity

### Is the F1 score field accuracy?

**Owner: Raed**

No. It is agreement with ESA WorldCover in a spatially separate east-side holdout. Independent field or municipal reference data are still required.

### Why did the annual built-up line dip in 2022?

**Owner: Yusuf**

Annual satellite products can classify some pixels differently between years. That dip is why the time series is supporting trend evidence, not an exact construction calendar.

### Why is confirmed growth smaller than candidate growth?

**Owner: Yusuf**

The annual product proposed 13.82 km². The stricter rule retained 3.74 km² only where separate 2025 optical and radar evidence also looked built-up. This is conservative and can miss real growth, but it reduces false positives.

### Is 49 °C the air temperature?

**Owner: Yusuf**

No. It is satellite-derived land-surface temperature for one Landsat observation. Surface temperature is not air temperature or personal heat exposure.

## User need and impact

### Who is the user?

**Owner: Raed**

A municipal urban-planning and heat-resilience team. The tool helps the team decide which 1 km zones to inspect first.

### Why use 1 km cells?

**Owner: Yusuf**

They match the population layer and support early area screening. They are not detailed enough to choose an intervention for one building.

### Why these score weights?

**Owner: Yusuf**

They are transparent PoC assumptions: 40% heat, 30% population, 20% confirmed growth and 10% lack of vegetation. A real user must review and test them.

### What happens if the ranking is wrong?

**Owner: Raed**

No automatic action follows. The cost is wasted inspection time, so the pilot must measure useful results and false alarms before operational use.

### What impact can you prove now?

**Owner: Raed**

We can prove that the workflow produces a reproducible ranked map and exportable evidence. We cannot yet prove time savings or municipal value because no real user pilot has happened.

## Innovation and development

### What is innovative?

**Owner: Raed**

The innovation is not a new index. It is the conservative decision chain: annual change proposes growth, optical and radar evidence confirm it, heat and exposure rank it, and hyperspectral evidence tests a known desert failure mode.

### What would you build next?

**Owner: Raed**

We would interview users, agree on weights, inspect the top five zones, record false alarms, add local plans and worker-exposure data, and test a repeatable update in another Riyadh area.

### What is the business model?

**Owner: Raed**

The honest next step is a municipal pilot that measures usefulness, update cost and procurement fit. A supported analytics service or local deployment could be tested later. No customer, price, revenue or contract is claimed.

## Reproducibility

### Can the judges run it?

**Owner: Yusuf**

Yes. The public repository contains pinned requirements, a run-all sample notebook, example input and output, exact source configuration, the full pipeline and documented limitations. The sample requires no credential.
