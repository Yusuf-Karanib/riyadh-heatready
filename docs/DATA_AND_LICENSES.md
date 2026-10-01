# Data sources, exact items, and licences

All analysis inputs are open-access. Raw data are not included in the submission folder; the scripts record and retrieve the exact items.

## Organizer-confirmed PoC access

On 27 September 2026, the National Space Academy team confirmed in the authenticated mentor chat that the PoC baseline should use open Sentinel-2, Sentinel-1, and Landsat data with the team's own tools. They stated that gIQ access and sponsored imagery are for shortlisted teams after PoC evaluation, and Satellite 813 data will be shared when available. The current project therefore does not depend on any of those later or unavailable sources.

## Exact satellite items

| Purpose | Collection and item | Date | Main assets |
|---|---|---|---|
| Optical baseline | Sentinel-2 L2A `S2A_MSIL2A_20180511T072621_R049_T38RPN_20201012T082634` | 2018-05-11 | B02, B03, B04, B08, B11, B12, SCL |
| Radar baseline | Sentinel-1 RTC `S1A_IW_GRDH_1SDV_20180510T145710_20180510T145735_021844_025B78_rtc` | 2018-05-10 | VV, VH |
| Model reference epoch | Sentinel-2 L2A `S2B_MSIL2A_20210510T072619_R049_T38RPN_20210511T101721` | 2021-05-10 | B02, B03, B04, B08, B11, B12, SCL |
| Model reference radar | Sentinel-1 RTC `S1A_IW_GRDH_1SDV_20210506T145728_20210506T145753_037769_047525_rtc` | 2021-05-06 | VV, VH |
| Current optical | Sentinel-2 L2A `S2B_MSIL2A_20250509T072619_R049_T38RPN_20250509T094732` | 2025-05-09 | B02, B03, B04, B08, B11, B12, SCL |
| Current radar | Sentinel-1 RTC `S1A_IW_GRDH_1SDV_20250509T145740_20250509T145805_059119_rtc` | 2025-05-09 | VV, VH |
| Surface temperature | Landsat C2 L2 `LC08_L2SP_166043_20250510_02_T1` | 2025-05-10 | lwir11, qa_pixel |
| Built reference | ESA WorldCover `ESA_WorldCover_10m_2021_v200_N24E045` | 2021 | map |
| Annual trend | IO/Esri annual LULC `38R-2018` | 2018 | data |
| Annual trend | IO/Esri annual LULC `38R-2019` | 2019 | data |
| Annual trend | IO/Esri annual LULC `38R-2020` | 2020 | data |
| Annual trend | IO/Esri annual LULC `38R-2021` | 2021 | data |
| Annual trend | IO/Esri annual LULC `38R-2022` | 2022 | data |
| Annual trend | IO/Esri annual LULC `38R-2023` | 2023 | data |
| Hyperspectral context | Planet Tanager urban `20250515_080954_16_4001` | 2025-05-15 | ortho_sr_hdf5 |

The Microsoft Planetary Computer STAC endpoint is `https://planetarycomputer.microsoft.com/api/stac/v1`.

The Planet Tanager item is at `https://www.planet.com/data/stac/tanager-core-imagery/urban/20250515_080954_16_4001/20250515_080954_16_4001.json`.

## Population source

- Product: WorldPop Global2, constrained 2025 population, 1 km, Saudi Arabia.
- DOI: `10.5258/SOTON/WP00840`.
- File: `sau_pop_2025_CN_1km_R2025A_UA_v1.tif`.
- Unit: modelled people per grid cell.
- Licence: Creative Commons Attribution 4.0.
- Product status: WorldPop labels R2025A as an alpha release that may change as it is improved.
- Saudi Arabia 1 km record: `https://hub.worldpop.org/geodata/summary?id=79157`.

## Licence record

| Dataset | Licence or terms | Reference |
|---|---|---|
| Sentinel-2 L2A | Copernicus Sentinel data legal notice; free, full, and open access | `https://dataspace.copernicus.eu/terms-and-conditions` |
| Sentinel-1 RTC hosted by Microsoft | CC BY 4.0 | `https://planetarycomputer.microsoft.com/api/stac/v1/collections/sentinel-1-rtc` |
| Landsat Collection 2 Level-2 | United States public domain | `https://www.usgs.gov/faqs/are-landsat-data-cloud-still-considered-be-within-public-domain` |
| ESA WorldCover 2021 | CC BY 4.0 | `https://esa-worldcover.org/en/data-access` |
| Impact Observatory/Esri annual LULC | CC BY 4.0 | `https://planetarycomputer.microsoft.com/api/stac/v1/collections/io-lulc-annual-v02` |
| WorldPop 2025 | CC BY 4.0 | `https://hub.worldpop.org/geodata/summary?id=79157` |
| Planet Tanager open archive | CC BY 4.0 | `https://www.planet.com/pulse/unleash-the-power-of-hyperspectral-over-50-tanager-radiance-datasets-now-available-on-planet-s/` |

## Provider documentation checks

- Planetary Computer describes Sentinel-2 L2A as bottom-of-atmosphere reflectance with 10 m, 20 m, and 60 m bands. The project uses the 20 m scene-classification layer for pixel-level quality masking.
- The Sentinel-1 RTC collection is radiometrically terrain corrected, 10 m C-band SAR under CC BY 4.0. Its current collection metadata says a Planetary Computer account is required to obtain new RTC asset tokens; the project's source test confirmed the recorded items were readable in the build environment.
- Landsat Collection 2 Level-2 supplies atmospherically corrected surface reflectance and surface-temperature products. This project uses the thermal product only as land-surface temperature.
- ESA WorldCover 2021 is a 10 m classification derived from Sentinel-1 and Sentinel-2. It is a satellite reference rather than field truth.
- The Impact Observatory/Esri V2 annual product covers 2017–2023 at 10 m and reports average assessed accuracy over 75%. That does not make every year or pixel correct, so the project treats the annual line as supporting evidence.
- The selected Tanager item contains 426 wavelength records spanning 376.44–2499.0 nm. Its STAC metadata reports nominal GSD 32.7 m, while the orthorectified HDF5 grid spacing is exactly 30 m. It is one open 2025 surface-reflectance scene and cannot establish change alone.

## Attribution text for outputs

> Contains modified Copernicus Sentinel data (2018, 2021, 2025), Sentinel-1 RTC data hosted by Microsoft, USGS Landsat Collection 2 Level-2 data, Impact Observatory/Esri annual land-cover data, and WorldPop 2025 data. © ESA WorldCover project 2021 / Contains modified Copernicus Sentinel data (2021) processed by ESA WorldCover consortium. Adapted from Tanager STAC Data, available at www.planet.com/data/stac © 2025 Planet Labs PBC. All Rights Reserved.

## Distribution rules used by this project

- Publish code, item IDs, methods, small derived tables, and permitted figures.
- Do not include passwords, access tokens, signed temporary URLs, or portal account data.
- Do not include the 856 MB Tanager HDF5 file, cloud caches, or virtual environment in the submission archive.
- Recheck every licence if the project later adds commercial, sponsored, Satellite 813, MBZ-SAT, or gIQ data.
