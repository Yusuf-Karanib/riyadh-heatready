# Riyadh HeatReady — project brief

## The project in one sentence

Riyadh HeatReady identifies 1 km zones along southeastern Riyadh's urban-industrial fringe where built-up growth from a separate annual land-cover product for 2018 to 2023, confirmed by 2025 optical and radar observations, overlaps high 2025 land-surface temperature and modelled population exposure.

## One user and one decision

**Intended user:** a municipal urban-planning and heat-resilience team.

**Decision:** which zones should be inspected first for locally suitable cooling measures such as shade, trees, cool roofs, or cool pavements?

The map does not choose an intervention automatically. It ranks places for professional review and field checking.

## Why southeastern Riyadh

1. The open Planet Tanager urban collection contains a Riyadh scene from 15 May 2025.
2. Low-cloud Sentinel-2, Sentinel-1 radar, and Landsat thermal observations exist within days of that scene.
3. Comparable Sentinel-2 and Sentinel-1 observations exist for May 2018.
4. Annual 10 m land-cover maps cover every year from 2018 through 2023.
5. The area mixes established neighbourhoods, industrial surfaces, new construction, roads, bare soil, and undeveloped land. That makes it a useful arid-city test.

## Why this problem was selected

| Candidate | Strength | Main problem | Decision |
|---|---|---|---|
| Riyadh growth + heat priority | Exact open Tanager scene; optical, radar, thermal, land-cover, and population data align | Requires careful separation of buildings from bright desert | **Selected** |
| UAE city heat priority | Strong regional relevance | No matching open Tanager urban scene was confirmed | Not selected |
| Riyadh green-space monitoring | Simple and explainable | Less direct match to the assigned growth, land-use, and heat-risk challenge | Not selected |

## Smallest credible MVP

The MVP is one self-contained dashboard with:

- a decision map of 1 km priority cells;
- an annual 2018–2023 mapped built-up trend;
- evidence maps for 2018/2025 built-up probability, confirmed growth, and 2025 surface temperature;
- a ranked table of zones;
- a spatial holdout validation result;
- a Planet Tanager spectral comparison;
- clear limitations and data provenance.

## Product delivery and viability hypothesis

This is a hypothesis for judging and future testing, not proof of a customer or business.

- **Potential adopter:** a municipal urban-planning or heat-resilience team.
- **Delivered product:** a regularly refreshed dashboard plus a ranked CSV, GeoJSON, and GeoTIFF layer that can enter an existing GIS workflow.
- **First pilot:** one planning team reviews the top five zones, compares them with local plans and field observations, and records whether the ranking saved useful screening time.
- **Scale path:** repeat the same open-data pipeline AOI by AOI, then add city-owned or sponsored higher-resolution data only when access and licence terms are confirmed.
- **Value hypothesis:** reduce the time spent manually comparing disconnected growth, heat, vegetation, and population layers.
- **Economic path to test:** a supported municipal analytics service or licensed deployment could be explored only after a real pilot proves demand, accuracy, operating cost, and procurement fit.

No municipality, paying customer, price, revenue, time saving, or deployment agreement is claimed.

## Current verified results

- Configured AOI: **168.30 km²** after exact boundary clipping.
- Annual land-cover built area: **85.39 km² in 2018** and **98.03 km² in 2023** inside the AOI.
- The intermediate annual estimates are **91.35, 92.01, 94.09, and 92.00 km²** for 2019–2022. The 2022 dip is a warning that these maps are not exact construction records.
- Annual-map candidate growth: **13.82 km²**.
- Conservative growth confirmed by the optical-radar rule: **3.74 km²**.
- Mean Landsat land-surface temperature on 10 May 2025: **49.02 °C**; 90th percentile: **51.71 °C**.
- WorldPop 2025 modelled population inside the AOI: approximately **594,902**.
- Built-up classifier agreement with the east-side WorldCover holdout: **F1 0.88**, **IoU 0.78**, **balanced accuracy 0.89**.

These are PoC results, not official city statistics. The growth value is intentionally conservative because a pixel must pass both the annual land-cover change test and the 2025 optical-radar confirmation rule.

## Correct claims

- Say **"land-surface temperature"**, not air temperature or human body exposure.
- Say **"modelled population estimate"**, not census count.
- Say **"agreement with WorldCover"**, not field-verified accuracy.
- Say **"confirmed growth signal"**, not every building constructed.
- Say **"open Planet Tanager archive scene"**, not Satellite 813 imagery.
- Say **"screening priority"**, not an official government priority or medical risk score.

## What the result enables

A planning team can start with the highest-ranked cells, inspect local conditions, compare planned development and infrastructure, and decide whether more detailed surveys or a cooling intervention assessment are justified.
