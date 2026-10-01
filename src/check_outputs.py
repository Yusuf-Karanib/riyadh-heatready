"""Run final sanity checks and create a reproducibility manifest."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd
import rasterio
from shapely.geometry import shape


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "outputs"
NOTEBOOK = ROOT / "notebooks" / "02_main_analysis.ipynb"
SAMPLE_INPUT = ROOT / "data" / "sample_input" / "riyadh_priority_drivers.csv"
EXAMPLE_CSV = ROOT / "results" / "example_priority_zones.csv"
EXAMPLE_PNG = ROOT / "results" / "example_priority_output.png"
SLIDES_PDF = ROOT / "output" / "pdf" / "Riyadh_HeatReady_PoC_Pitch.pdf"
SLIDES_PPTX = ROOT / "slides" / "Riyadh_HeatReady_PoC_Pitch.pptx"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def check(condition: bool, message: str, checks: list[dict[str, str]]) -> None:
    if not condition:
        raise AssertionError(message)
    checks.append({"status": "PASS", "check": message})


def main() -> None:
    required = [
        "dashboard.html",
        "decision_map.png",
        "analysis_overview.png",
        "annual_built_area_timeseries.png",
        "annual_built_area_timeseries.csv",
        "validation.png",
        "tanager_material_analysis.png",
        "priority_zones.csv",
        "priority_zones.geojson",
        "results_summary.json",
        "validation_metrics.json",
        "tanager_summary.json",
        "data_feasibility.json",
        "built_probability_2018.tif",
        "built_probability_2025.tif",
        "annual_lulc_candidate_growth_2018_2023.tif",
        "confirmed_built_growth_2018_2023.tif",
        "land_surface_temperature_2025_c.tif",
        "priority_score_1km.tif",
    ]
    checks: list[dict[str, str]] = []
    for name in required:
        path = OUTPUT_DIR / name
        check(path.exists() and path.stat().st_size > 0, f"{name} exists and is not empty", checks)

    for path in [NOTEBOOK, SAMPLE_INPUT, EXAMPLE_CSV, EXAMPLE_PNG, SLIDES_PDF, SLIDES_PPTX]:
        check(
            path.exists() and path.stat().st_size > 0,
            f"{path.relative_to(ROOT).as_posix()} exists and is not empty",
            checks,
        )

    requirements = [
        line.strip()
        for line in (ROOT / "requirements.txt").read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]
    check(requirements and all("==" in line for line in requirements), "every Python requirement is pinned with ==", checks)

    notebook = json.loads(NOTEBOOK.read_text(encoding="utf-8"))
    code_cells = [cell for cell in notebook["cells"] if cell["cell_type"] == "code"]
    check(bool(code_cells), "submission notebook contains executable code cells", checks)
    check(all(cell.get("execution_count") is not None for cell in code_cells), "every submission notebook code cell has a committed execution count", checks)
    notebook_errors = [
        output
        for cell in code_cells
        for output in cell.get("outputs", [])
        if output.get("output_type") == "error"
    ]
    check(not notebook_errors, "submission notebook contains no saved error outputs", checks)

    sample = pd.read_csv(SAMPLE_INPUT)
    check(len(sample) == 67, "sample input contains all 67 eligible priority cells", checks)
    check("priority_score" not in sample and "priority_class" not in sample, "sample input leaves the score and class for the notebook to calculate", checks)
    example = pd.read_csv(EXAMPLE_CSV)
    check(example.iloc[0]["grid_id"] == "R05C10", "example notebook output preserves the verified top-ranked cell", checks)
    check(np.isclose(example.iloc[0]["priority_score"], 78.656723, atol=1e-5), "example notebook output reproduces the verified top score", checks)

    check(SLIDES_PDF.stat().st_size < 50 * 1024 * 1024, "presentation PDF is below the official 50 MB limit", checks)
    check(SLIDES_PDF.read_bytes()[:5] == b"%PDF-", "presentation file has a valid PDF header", checks)

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    required_readme_sections = [
        "## 1. Business use case",
        "## 2. Problem, scale, and why satellite data",
        "## 3. Data",
        "## 4. Technical approach",
        "## 5. Installation",
        "## 6. How to run",
        "## 7. Example input and output",
        "## 8. Results",
        "## 9. Validation, assumptions, and limitations",
        "## 10. Team, licence, and attribution",
    ]
    positions = [readme.find(heading) for heading in required_readme_sections]
    check(all(position >= 0 for position in positions), "README contains all ten required sections", checks)
    check(positions == sorted(positions), "README sections follow the official required order", checks)

    config = json.loads((ROOT / "config.json").read_text(encoding="utf-8"))
    feasibility = json.loads((OUTPUT_DIR / "data_feasibility.json").read_text(encoding="utf-8"))
    check(feasibility["result"] == "PASS", "data feasibility result is PASS", checks)
    check(len(feasibility["checks"]) == 38, "all 38 planned source assets were checked", checks)
    check(
        all(entry["status"] == "usable" for entry in feasibility["checks"]),
        "every source-asset check is usable",
        checks,
    )

    summary = json.loads((OUTPUT_DIR / "results_summary.json").read_text(encoding="utf-8"))
    validation = summary["validation"]
    check(0 < summary["new_built_area_km2"] <= summary["annual_lulc_candidate_growth_km2"], "confirmed growth is positive and no larger than the annual-map candidate growth", checks)
    check(20 <= summary["lst_mean_c"] <= 70, "mean land-surface temperature is physically plausible for the case study", checks)
    check(summary["population_estimate"] > 0, "population estimate is positive", checks)
    check(150 <= summary["analysis_area_km2"] <= 180, "exact AOI area is plausible", checks)
    check(summary["aoi_bbox_wgs84"] == config["aoi_bbox_wgs84"], "summary records the configured AOI", checks)
    check(0 <= validation["f1"] <= 1 and 0 <= validation["iou"] <= 1, "validation metrics are bounded between zero and one", checks)
    check(validation["test_pixels"] >= 10_000, "spatial holdout contains at least 10,000 reference pixels", checks)
    check("tanager" in summary, "Tanager analysis is linked into the final summary", checks)
    check(summary["tanager"]["role_in_project"].endswith("not Satellite 813 data."), "Tanager is not mislabelled as Satellite 813", checks)

    annual_table = pd.read_csv(OUTPUT_DIR / "annual_built_area_timeseries.csv")
    check(
        {"year", "built_area_km2", "year_to_year_change_km2"}.issubset(annual_table.columns),
        "annual time-series table contains the required fields",
        checks,
    )
    check(
        annual_table["year"].tolist() == list(range(2018, 2024)),
        "annual time series contains exactly 2018 through 2023 in order",
        checks,
    )
    check(
        np.isfinite(annual_table["built_area_km2"]).all()
        and (annual_table["built_area_km2"] > 0).all()
        and (annual_table["built_area_km2"] <= summary["analysis_area_km2"]).all(),
        "annual mapped built-up areas are finite and inside the AOI area",
        checks,
    )
    expected_changes = annual_table["built_area_km2"].diff()
    check(
        pd.isna(annual_table.loc[0, "year_to_year_change_km2"])
        and np.allclose(
            annual_table.loc[1:, "year_to_year_change_km2"],
            expected_changes.iloc[1:],
        ),
        "annual year-to-year changes match the mapped-area differences",
        checks,
    )
    summary_series = summary["annual_lulc_built_area_timeseries_km2"]
    csv_series = {
        str(int(row.year)): float(row.built_area_km2)
        for row in annual_table.itertuples(index=False)
    }
    check(
        summary_series.keys() == csv_series.keys()
        and all(np.isclose(summary_series[year], value) for year, value in csv_series.items()),
        "summary annual time series matches the CSV",
        checks,
    )
    check(
        np.isclose(summary["annual_lulc_built_area_2018_km2"], csv_series["2018"])
        and np.isclose(summary["annual_lulc_built_area_2023_km2"], csv_series["2023"]),
        "annual time-series endpoints match the reported 2018 and 2023 areas",
        checks,
    )

    table = pd.read_csv(OUTPUT_DIR / "priority_zones.csv")
    required_columns = {
        "grid_id",
        "priority_score",
        "lst_mean_c",
        "population_estimate",
        "new_built_fraction",
        "aoi_coverage_fraction",
    }
    check(required_columns.issubset(table.columns), "priority table contains the decision fields", checks)
    check(not table.empty, "priority table contains eligible growth cells", checks)
    check(table["priority_score"].between(0, 100).all(), "all priority scores are between 0 and 100", checks)
    check(table["priority_score"].is_monotonic_decreasing, "priority table is sorted from highest to lowest score", checks)
    check(table["grid_id"].is_unique, "each priority grid ID is unique", checks)
    numeric_columns = [
        "priority_score",
        "lst_mean_c",
        "population_estimate",
        "built_fraction_2018",
        "built_fraction_2025",
        "new_built_fraction",
        "aoi_coverage_fraction",
        "ndvi_mean_2025",
        "heat_component",
        "population_component",
        "growth_component",
        "lack_green_component",
    ]
    check(np.isfinite(table[numeric_columns].to_numpy()).all(), "priority table has no missing or infinite decision values", checks)
    check((table["new_built_fraction"] > 0).all(), "every ranked cell contains confirmed growth", checks)
    check(table["aoi_coverage_fraction"].between(0, 1).all(), "AOI coverage fractions are bounded", checks)
    west, south, east, north = config["aoi_bbox_wgs84"]
    check(table["longitude"].between(west, east).all(), "all ranked cell centres are inside the AOI longitude range", checks)
    check(table["latitude"].between(south, north).all(), "all ranked cell centres are inside the AOI latitude range", checks)
    check(len(table) == summary["eligible_grid_cells"], "priority row count matches the summary", checks)
    check((table["priority_class"] == "High").sum() == summary["high_priority_grid_cells"], "high-priority row count matches the summary", checks)

    geojson = json.loads((OUTPUT_DIR / "priority_zones.geojson").read_text(encoding="utf-8"))
    check(len(geojson["features"]) == len(table), "GeoJSON feature count matches the priority table", checks)
    bounds_inside = True
    for feature in geojson["features"]:
        left, bottom, right, top = shape(feature["geometry"]).bounds
        bounds_inside &= (
            left >= west - 1e-6
            and right <= east + 1e-6
            and bottom >= south - 1e-6
            and top <= north + 1e-6
        )
    check(bounds_inside, "all GeoJSON geometries are clipped to the AOI", checks)

    raster_expectations = {
        "built_probability_2018.tif": (0.0, 1.0),
        "built_probability_2025.tif": (0.0, 1.0),
        "priority_score_1km.tif": (0.0, 100.0),
        "land_surface_temperature_2025_c.tif": (10.0, 80.0),
    }
    for name, (minimum, maximum) in raster_expectations.items():
        with rasterio.open(OUTPUT_DIR / name) as src:
            data = src.read(1, masked=True).compressed()
            check(str(src.crs) == "EPSG:32638", f"{name} uses the expected Riyadh UTM coordinate system", checks)
            check(data.size > 0, f"{name} contains valid pixels", checks)
            check(float(np.nanmin(data)) >= minimum - 1e-4 and float(np.nanmax(data)) <= maximum + 1e-4, f"{name} values stay inside the expected range", checks)

    for name in [
        "annual_lulc_candidate_growth_2018_2023.tif",
        "confirmed_built_growth_2018_2023.tif",
    ]:
        with rasterio.open(OUTPUT_DIR / name) as src:
            raw = src.read(1, masked=True)
            values = set(np.unique(raw.compressed()).tolist())
            check(src.nodata == 255, f"{name} uses 255 rather than valid zero as nodata", checks)
            check(values.issubset({0, 1}), f"{name} contains only valid binary values", checks)
            check(0 in values and 1 in values, f"{name} contains both no-growth and growth pixels", checks)

    validation_file = json.loads((OUTPUT_DIR / "validation_metrics.json").read_text(encoding="utf-8"))
    check(validation_file["metrics"] == validation, "summary validation matches validation_metrics.json", checks)
    tanager_file = json.loads((OUTPUT_DIR / "tanager_summary.json").read_text(encoding="utf-8"))
    check(summary["tanager"] == tanager_file, "summary Tanager result matches tanager_summary.json", checks)
    strict_tanager = tanager_file["beta_cloud_mask_sensitivity"]
    strict_counts = [
        values["ndbi"]["count"]
        for values in strict_tanager["class_statistics"].values()
    ]
    strict_medians = [
        values["ndbi"]["median"]
        for values in strict_tanager["class_statistics"].values()
    ]
    check(min(strict_counts) >= 20, "strict Tanager cloud-mask sensitivity has enough pixels in every surface group", checks)
    check(np.isfinite(strict_medians).all(), "strict Tanager cloud-mask sensitivity has finite NDBI medians", checks)

    dashboard = (OUTPUT_DIR / "dashboard.html").read_text(encoding="utf-8")
    for phrase in [
        "Riyadh HeatReady",
        "Annual built-up trend",
        "Tanager adds material context, not change proof",
        "stricter sensitivity test",
        "Potential adopter, not a claimed customer",
        "Use this as a screening tool.",
        "Every priority zone needs local review and field checking.",
    ]:
        check(phrase in dashboard, f"dashboard contains: {phrase}", checks)

    manifest = []
    for path in sorted(OUTPUT_DIR.iterdir()):
        if path.is_file() and path.name not in {"verification_report.json", "verification_report.md", "manifest.json"}:
            manifest.append(
                {
                    "file": path.name,
                    "bytes": path.stat().st_size,
                    "sha256": sha256(path),
                }
            )
    (OUTPUT_DIR / "manifest.json").write_text(
        json.dumps(manifest, indent=2), encoding="utf-8"
    )
    report = {"result": "PASS", "checks_passed": len(checks), "checks": checks}
    (OUTPUT_DIR / "verification_report.json").write_text(
        json.dumps(report, indent=2), encoding="utf-8"
    )
    lines = [
        "# Verification report",
        "",
        f"**Result:** PASS — {len(checks)} checks passed.",
        "",
    ]
    lines.extend(f"- PASS: {entry['check']}" for entry in checks)
    lines.extend(
        [
            "",
            "The checks cover file presence, plausible numeric ranges, coordinate systems, table ordering, validation bounds, Tanager labelling, and required dashboard explanations. They do not replace independent field validation.",
        ]
    )
    (OUTPUT_DIR / "verification_report.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )
    print(json.dumps({"result": "PASS", "checks_passed": len(checks)}, indent=2))


if __name__ == "__main__":
    main()
