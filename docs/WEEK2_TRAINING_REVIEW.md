# Week 2 training review — time series and change detection

## What this update is

This is learning material, not a new submission rule. Its main lesson is useful: do not rely only on a start image and an end image when several dates are available.

## What was added to Riyadh HeatReady

The project now checks six annual land-cover maps: 2018, 2019, 2020, 2021, 2022, and 2023. It exports a chart and CSV showing mapped built-up area for every year.

The result rises overall from **85.39 km²** in 2018 to **98.03 km²** in 2023. It dips from **94.09 km²** in 2021 to **92.00 km²** in 2022. That dip is important: annual classifications can change because of imagery and model uncertainty, so the line is not an exact construction calendar.

The final decision layer still uses a conservative endpoint rule. A 2018–2023 annual-map change must also look built-up in the separate 2025 optical-radar model.

## What was not copied from the lesson

- **NDBI alone:** bright desert can look more built-up than buildings. Our Tanager check measured this problem in the actual Riyadh area.
- **Simple array resizing:** all project rasters are aligned to one exact UTM grid, not merely resized to the same number of rows and columns.
- **Missing dates filled by interpolation:** that can invent a transition that the satellite never observed.
- **Automatic BFAST or Ruptures use:** six annual values are too small for a credible disturbance model without stronger assumptions and a longer history.
- **The lesson's calibration formula:** the project uses the official Sentinel-2 Level-2A offset and quantification formula.

## Safe lessons we kept

1. Compare the same place across several dates.
2. Align every image to one shared map grid.
3. Mask invalid, cloudy, and shadowed pixels.
4. Separate the measured value from the amount of change.
5. Show uncertainty and validate with another source.

## Official technical references checked

- Copernicus Browser documentation: `https://documentation.dataspace.copernicus.eu/Applications/Browser.html`
- Sentinel-2 product and radiometric-offset documentation: `https://sentiwiki.copernicus.eu/web/s2-products`
- Sentinel-2 cloud detector: `https://github.com/sentinel-hub/sentinel2-cloud-detector`
- BFAST documentation: `https://bfast.readthedocs.io/en/latest/`
- Ruptures documentation: `https://centre-borelli.github.io/ruptures-docs/`
- Rasterio documentation: `https://rasterio.readthedocs.io/`

The private portal lesson was supplied as pasted text. Where the paste did not preserve a link address, the named tool was checked on its official website.
