# Methodology — beginner version

## The basic idea

The project asks four simple questions for each 1 km grid cell:

1. Did built-up land appear between 2018 and 2023?
2. Does the 2025 satellite evidence still look built-up?
3. Was the surface hot in the May 2025 Landsat observation?
4. How many people are estimated to live in that cell, and how little vegetation is present?

The answers are combined into one transparent screening score.

## Step 1 — Keep the comparison fair

The optical and radar observations are from May in every comparison year. Using the same season reduces false change caused by seasonal vegetation or sunlight differences.

- Sentinel-2: 11 May 2018, 10 May 2021, 9 May 2025.
- Sentinel-1: 10 May 2018, 6 May 2021, 9 May 2025.
- Landsat temperature: 10 May 2025.
- Planet Tanager: 15 May 2025.

## Step 2 — Prepare the optical data

Sentinel-2 measures reflected light. Six bands are used: blue, green, red, near-infrared, and two short-wave infrared bands.

The workflow:

1. applies the Sentinel scene-classification mask;
2. removes cloud, shadow, snow, invalid, and saturated pixels;
3. applies the post-2022 Sentinel-2 radiometric offset so 2018 and 2025 are comparable;
4. calculates NDVI, NDBI, BSI, and MNDWI;
5. keeps the original reflectance bands too, because one index is not enough in a desert city.

## Step 3 — Add radar structure

Sentinel-1 radar measures how strongly the surface returns a microwave signal. Buildings often return radar differently from smooth bare ground, so radar helps reduce confusion between bright desert and built surfaces.

The model uses VV, VH, and the VV-minus-VH difference in decibels.

## Step 4 — Train and test the built-up model

A random-forest classifier combines the optical and radar features. ESA WorldCover 2021 class 50 supplies the built-up reference label.

To reduce spatial leakage:

- the western part of the AOI trains the model;
- a separate middle strip chooses the probability threshold;
- the eastern part tests the final model;
- gaps separate the three areas.

The final east-side holdout result is:

| Metric | Result | Plain meaning |
|---|---:|---|
| Precision | 0.88 | When the model says built-up, it agrees with the reference about 88% of the time. |
| Recall | 0.88 | It finds about 88% of the reference built-up pixels. |
| F1 | 0.88 | One balance between precision and recall. |
| IoU | 0.78 | The predicted and reference built-up areas overlap by about 78%. |
| Balanced accuracy | 0.89 | Average performance across built-up and other classes. |

This is agreement with another satellite-derived product. It is not field-verified accuracy.

## Step 5 — Show the annual trend and require two kinds of evidence for growth

Six Impact Observatory/Esri annual land-cover maps provide one mapped built-up estimate for each year from 2018 through 2023:

| Year | Mapped built-up area inside the AOI |
|---:|---:|
| 2018 | 85.39 km² |
| 2019 | 91.35 km² |
| 2020 | 92.01 km² |
| 2021 | 94.09 km² |
| 2022 | 92.00 km² |
| 2023 | 98.03 km² |

The overall direction is upward, but the 2022 dip shows why an annual map is not an exact construction record. Pixels can be classified differently from one year to the next.

For the final growth layer, the annual product proposes pixels that changed from non-built in the 2018 map to built in the 2023 map.

A proposed change is retained only when:

- the 2025 optical-radar model says the pixel is built-up; and
- its built-up probability increased by at least 0.10 from 2018 to 2025; and
- the connected group contains at least six 30 m pixels.

This conservative intersection removes many false changes. It can also miss real development, which is why the output is called a **confirmed growth signal** rather than total construction.

## Step 6 — Calculate surface temperature

Landsat Collection 2 Level-2 surface-temperature band values are converted from stored digital numbers to Kelvin using the product scale and offset, then converted to Celsius.

Cloud, cirrus, shadow, snow, fill, and dilated-cloud pixels are removed using the Landsat quality band. Plausibility limits of 10–80 °C catch broken values.

Land-surface temperature is the temperature of roofs, soil, roads, and vegetation seen from space. It is not the air temperature felt by a person.

## Step 7 — Add population and vegetation context

- WorldPop 2025 provides modelled people per approximately 1 km grid cell.
- Sentinel-2 NDVI provides vegetation context.
- All high-resolution evidence is averaged into 1 km decision cells.
- Cells and exported polygons are clipped to the configured AOI. Population in a
  partial edge cell is multiplied by the fraction of that cell inside the AOI.

## Step 8 — Calculate the priority score

An eligible cell must have its centre inside the AOI, contain some confirmed
2018–2023 growth, and have valid heat, vegetation, and built-up evidence. This
keeps the ranked output focused on the stated question: where recent growth,
heat, and population overlap.

Each component is ranked among those eligible growth cells. The PoC weights are:

| Component | Weight |
|---|---:|
| Hotter land surface | 40% |
| Modelled population | 30% |
| Confirmed recent growth | 20% |
| Lower vegetation | 10% |

These weights are transparent PoC assumptions. A real city user should review and change them.

## Step 9 — Use Tanager only where it helps

The open Planet Tanager scene contains 426 narrow bands. It is used to compare the 2025 spectra of confirmed-growth, established-built, and likely-unbuilt surface groups.

The comparison found:

- growth versus likely-unbuilt median spectral angle: **3.21°**;
- growth versus established-built median spectral angle: **0.61°**;
- likely-unbuilt median narrow-band NDBI: **0.084**;
- established-built median narrow-band NDBI: **0.049**.

The higher NDBI for likely-unbuilt land demonstrates why NDBI alone is unreliable in bright arid terrain. Tanager adds surface-material context, but one date cannot prove change and no specific material is named without field spectra.

The beta cloud mask flags many bright urban and desert pixels. A stricter sensitivity
test removes every flagged pixel. The median NDBI order remains the same:
likely-unbuilt **0.083**, confirmed-growth **0.072**, and established-built **0.042**.
The strict test retains 17,251, 165, and 1,247 pixels in those groups respectively.
This supports the narrow NDBI warning, but the small retained growth sample makes it
a sensitivity check rather than independent validation.

## Step 10 — Deliver a testable planning screen

The analysis is exported as a self-contained dashboard, a ranked CSV, GeoJSON polygons,
and GeoTIFF layers. A first real pilot should ask one planning team to review the top
five zones against local plans and field observations. The pilot should measure whether
the ranking is understandable, technically credible, and useful enough to reduce manual
screening work. No customer, time saving, price, or revenue is assumed before that test.

## Main limitations

1. Reference labels are satellite-derived, not surveyed on the ground.
2. WorldPop is modelled and may miss daytime industrial workers.
3. One Landsat temperature observation cannot describe every hot day.
4. Priority weights are assumptions, not official policy.
5. Mixed 30 m pixels may contain several surfaces.
6. The Tanager beta cloud mask flagged 54% of the scene. The main descriptive comparison uses no-data and cirrus masks; a separately reported strict sensitivity test excludes every beta-cloud pixel.
7. The annual land-cover series can contain year-to-year classification changes; it does not give exact construction dates.
8. Local field checks and city data are required before action.
