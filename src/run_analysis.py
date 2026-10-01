"""Build the Riyadh HeatReady proof-of-concept from open satellite data.

The workflow intentionally stays small and explainable:

1. Read matching May observations for 2018, 2021, and 2025.
2. Train an optical + radar built-up classifier against ESA WorldCover 2021.
3. Measure the 2018–2023 annual land-cover trend and confirm endpoint change
   with the 2018/2025 fusion model.
4. Derive Landsat surface temperature for 10 May 2025.
5. Aggregate growth, heat, vegetation, and WorldPop exposure to 1 km cells.
6. Rank cells for field inspection and cooling-planning review.

The output is a screening tool, not an automatic policy decision or a health-risk
model. Every important limitation is carried into the generated dashboard.
"""

from __future__ import annotations

import base64
import hashlib
import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import planetary_computer
import rasterio
from matplotlib.colors import ListedColormap
from matplotlib.patches import Rectangle
from pystac_client import Client
from rasterio.enums import Resampling
from rasterio.features import geometry_mask
from rasterio.transform import from_origin, xy
from rasterio.vrt import WarpedVRT
from rasterio.warp import reproject, transform, transform_bounds, transform_geom
from scipy import ndimage
from shapely.geometry import box as shapely_box
from shapely.geometry import mapping, shape
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)


ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "config.json"
CACHE_DIR = ROOT / "data" / "cache"
RAW_DIR = ROOT / "data" / "raw"
OUTPUT_DIR = ROOT / "outputs"


@dataclass(frozen=True)
class Grid:
    crs: str
    transform: rasterio.Affine
    width: int
    height: int
    resolution: float

    @property
    def bounds(self) -> tuple[float, float, float, float]:
        left = self.transform.c
        top = self.transform.f
        right = left + self.width * self.resolution
        bottom = top - self.height * self.resolution
        return left, bottom, right, top


def load_config() -> dict[str, Any]:
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


def make_grid(config: dict[str, Any], resolution: float) -> Grid:
    bbox = config["aoi_bbox_wgs84"]
    crs = config["target_crs"]
    left, bottom, right, top = transform_bounds(
        "EPSG:4326", crs, *bbox, densify_pts=21
    )
    left = math.floor(left / resolution) * resolution
    bottom = math.floor(bottom / resolution) * resolution
    right = math.ceil(right / resolution) * resolution
    top = math.ceil(top / resolution) * resolution
    width = int(round((right - left) / resolution))
    height = int(round((top - bottom) / resolution))
    return Grid(crs, from_origin(left, top, resolution, resolution), width, height, resolution)


def make_aoi_polygon(config: dict[str, Any]):
    west, south, east, north = config["aoi_bbox_wgs84"]
    edge_steps = 64
    bottom_edge = [[float(x), south] for x in np.linspace(west, east, edge_steps)]
    right_edge = [[east, float(y)] for y in np.linspace(south, north, edge_steps)[1:]]
    top_edge = [[float(x), north] for x in np.linspace(east, west, edge_steps)[1:]]
    left_edge = [[west, float(y)] for y in np.linspace(north, south, edge_steps)[1:]]
    geometry = {
        "type": "Polygon",
        "coordinates": [[*bottom_edge, *right_edge, *top_edge, *left_edge]],
    }
    return shape(transform_geom("EPSG:4326", config["target_crs"], geometry))


def grid_center_mask(polygon, grid: Grid) -> np.ndarray:
    return geometry_mask(
        [mapping(polygon)],
        out_shape=(grid.height, grid.width),
        transform=grid.transform,
        invert=True,
        all_touched=False,
    )


def grid_coverage_fraction(polygon, grid: Grid) -> np.ndarray:
    coverage = np.zeros((grid.height, grid.width), dtype="float32")
    cell_area = grid.resolution * grid.resolution
    for row in range(grid.height):
        top = grid.transform.f - row * grid.resolution
        bottom = top - grid.resolution
        for col in range(grid.width):
            left = grid.transform.c + col * grid.resolution
            right = left + grid.resolution
            cell = shapely_box(left, bottom, right, top)
            coverage[row, col] = float(cell.intersection(polygon).area / cell_area)
    return coverage


def open_item(catalog: Client, spec: dict[str, str]):
    collection = catalog.get_collection(spec["collection"])
    item = collection.get_item(spec["id"])
    if item is None:
        raise RuntimeError(f"Missing STAC item: {spec['collection']} / {spec['id']}")
    return planetary_computer.sign(item)


def _cache_path(label: str, grid: Grid, href: str) -> Path:
    left, _, _, top = grid.bounds
    token = f"{grid.width}x{grid.height}_{int(left)}_{int(top)}_{int(grid.resolution)}m"
    parsed = urlsplit(href)
    stable_source = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
    source_hash = hashlib.sha256(stable_source.encode("utf-8")).hexdigest()[:12]
    return CACHE_DIR / token / f"{label}_{source_hash}.tif"


def write_raster(
    path: Path,
    array: np.ndarray,
    grid: Grid,
    *,
    nodata: float | int,
    dtype: str,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    out = np.asarray(array)
    if np.issubdtype(np.dtype(dtype), np.floating):
        out = np.where(np.isfinite(out), out, nodata).astype(dtype)
    else:
        out = out.astype(dtype)
    with rasterio.open(
        path,
        "w",
        driver="GTiff",
        height=grid.height,
        width=grid.width,
        count=1,
        dtype=dtype,
        crs=grid.crs,
        transform=grid.transform,
        nodata=nodata,
        compress="deflate",
        predictor=2 if np.issubdtype(np.dtype(dtype), np.floating) else 1,
        tiled=True,
    ) as dst:
        dst.write(out, 1)


def read_cached_raster(path: Path, categorical: bool, grid: Grid) -> np.ndarray:
    with rasterio.open(path) as src:
        if (
            src.width != grid.width
            or src.height != grid.height
            or str(src.crs) != grid.crs
            or not src.transform.almost_equals(grid.transform)
        ):
            raise RuntimeError(f"Cached raster grid does not match: {path}")
        data = src.read(1)
        if categorical:
            return data
        data = data.astype("float32")
        if src.nodata is not None:
            data[data == src.nodata] = np.nan
        return data


def read_asset_to_grid(
    href: str,
    label: str,
    grid: Grid,
    *,
    resampling: Resampling,
    categorical: bool = False,
) -> np.ndarray:
    cache = _cache_path(label, grid, href)
    if cache.exists():
        try:
            return read_cached_raster(cache, categorical, grid)
        except Exception as error:
            print(f"Ignoring invalid cache {cache.name}: {error}", flush=True)

    print(f"Reading cloud asset: {label}", flush=True)

    env_options = {
        "GDAL_DISABLE_READDIR_ON_OPEN": "EMPTY_DIR",
        "CPL_VSIL_CURL_ALLOWED_EXTENSIONS": ".tif,.TIF,.tiff,.TIFF",
        "GDAL_HTTP_TIMEOUT": "45",
        "GDAL_HTTP_MAX_RETRY": "3",
        "GDAL_HTTP_RETRY_DELAY": "2",
    }
    with rasterio.Env(**env_options), rasterio.open(href) as src:
        src_nodata = src.nodata
        vrt_nodata = 0 if categorical else -9999.0
        with WarpedVRT(
            src,
            crs=grid.crs,
            transform=grid.transform,
            width=grid.width,
            height=grid.height,
            resampling=resampling,
            src_nodata=src_nodata,
            nodata=vrt_nodata,
        ) as vrt:
            data = vrt.read(1)

    if categorical:
        data = data.astype("uint16")
        write_raster(cache, data, grid, nodata=0, dtype="uint16")
        return data

    data = data.astype("float32")
    data[data == -9999.0] = np.nan
    write_raster(cache, data, grid, nodata=-9999.0, dtype="float32")
    return data


def safe_index(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    denominator = a + b
    out = np.full(a.shape, np.nan, dtype="float32")
    valid = np.isfinite(a) & np.isfinite(b) & (np.abs(denominator) > 1e-6)
    out[valid] = (a[valid] - b[valid]) / denominator[valid]
    return out


FEATURE_NAMES = [
    "blue",
    "green",
    "red",
    "nir",
    "swir1",
    "swir2",
    "NDVI",
    "NDBI",
    "BSI",
    "MNDWI",
    "VV_dB",
    "VH_dB",
    "VV_minus_VH_dB",
]


def sentinel2_epoch(item, label: str, grid: Grid) -> dict[str, np.ndarray]:
    arrays: dict[str, np.ndarray] = {}
    for band in ["B02", "B03", "B04", "B08", "B11", "B12"]:
        arrays[band] = read_asset_to_grid(
            item.assets[band].href,
            f"{label}_{band}",
            grid,
            resampling=Resampling.bilinear,
        )
    scl = read_asset_to_grid(
        item.assets["SCL"].href,
        f"{label}_SCL",
        grid,
        resampling=Resampling.nearest,
        categorical=True,
    )

    # Sentinel-2 processing baseline 04.00 introduced a -1000 radiometric
    # offset. Applying it keeps pre-2022 and post-2022 reflectance comparable.
    baseline = float(item.properties.get("s2:processing_baseline", "0"))
    offset = -1000.0 if baseline >= 4.0 else 0.0
    bad_scl = np.isin(scl, [0, 1, 3, 7, 8, 9, 10, 11])

    reflectance: dict[str, np.ndarray] = {}
    for band, raw in arrays.items():
        value = (raw + offset) / 10000.0
        valid = (
            np.isfinite(raw)
            & (raw > 0)
            & ~bad_scl
            & (value >= -0.1)
            & (value <= 1.2)
        )
        reflectance[band] = np.where(valid, value, np.nan).astype("float32")

    blue = reflectance["B02"]
    green = reflectance["B03"]
    red = reflectance["B04"]
    nir = reflectance["B08"]
    swir1 = reflectance["B11"]
    swir2 = reflectance["B12"]
    ndvi = safe_index(nir, red)
    ndbi = safe_index(swir1, nir)
    mndwi = safe_index(green, swir1)
    bsi_num = (swir1 + red) - (nir + blue)
    bsi_den = (swir1 + red) + (nir + blue)
    bsi = np.full(red.shape, np.nan, dtype="float32")
    valid_bsi = np.isfinite(bsi_num) & np.isfinite(bsi_den) & (np.abs(bsi_den) > 1e-6)
    bsi[valid_bsi] = bsi_num[valid_bsi] / bsi_den[valid_bsi]
    return {
        "blue": blue,
        "green": green,
        "red": red,
        "nir": nir,
        "swir1": swir1,
        "swir2": swir2,
        "ndvi": ndvi,
        "ndbi": ndbi,
        "bsi": bsi,
        "mndwi": mndwi,
    }


def sentinel1_epoch(item, label: str, grid: Grid) -> dict[str, np.ndarray]:
    values: dict[str, np.ndarray] = {}
    for polarization in ["vv", "vh"]:
        linear = read_asset_to_grid(
            item.assets[polarization].href,
            f"{label}_{polarization}",
            grid,
            resampling=Resampling.bilinear,
        )
        valid = np.isfinite(linear) & (linear > 0)
        db = np.full(linear.shape, np.nan, dtype="float32")
        db[valid] = 10.0 * np.log10(linear[valid])
        db[(db < -40) | (db > 10)] = np.nan
        values[polarization] = db
    values["ratio"] = values["vv"] - values["vh"]
    return values


def build_epoch_features(s2: dict[str, np.ndarray], s1: dict[str, np.ndarray]) -> np.ndarray:
    return np.stack(
        [
            s2["blue"],
            s2["green"],
            s2["red"],
            s2["nir"],
            s2["swir1"],
            s2["swir2"],
            s2["ndvi"],
            s2["ndbi"],
            s2["bsi"],
            s2["mndwi"],
            s1["vv"],
            s1["vh"],
            s1["ratio"],
        ],
        axis=-1,
    ).astype("float32")


def sample_balanced(
    features: np.ndarray,
    labels: np.ndarray,
    mask: np.ndarray,
    random_state: int = 42,
    max_per_class: int = 40_000,
) -> tuple[np.ndarray, np.ndarray]:
    rng = np.random.default_rng(random_state)
    flat_x = features.reshape(-1, features.shape[-1])
    flat_y = labels.ravel()
    flat_mask = mask.ravel()
    selected: list[np.ndarray] = []
    for value in [0, 1]:
        indices = np.flatnonzero(flat_mask & (flat_y == value))
        if indices.size == 0:
            raise RuntimeError(f"No training pixels for class {value}")
        if indices.size > max_per_class:
            indices = rng.choice(indices, size=max_per_class, replace=False)
        selected.append(indices)
    chosen = np.concatenate(selected)
    rng.shuffle(chosen)
    return flat_x[chosen], flat_y[chosen]


def choose_threshold(y_true: np.ndarray, probability: np.ndarray) -> float:
    best_threshold = 0.5
    best_score = -1.0
    for threshold in np.linspace(0.2, 0.8, 31):
        score = f1_score(y_true, probability >= threshold, zero_division=0)
        if score > best_score:
            best_score = score
            best_threshold = float(threshold)
    return best_threshold


def clean_binary(mask: np.ndarray, minimum_pixels: int) -> np.ndarray:
    labels, count = ndimage.label(mask)
    if count == 0:
        return mask.astype(bool)
    sizes = np.bincount(labels.ravel())
    keep = sizes >= minimum_pixels
    keep[0] = False
    return keep[labels]


def predict_probability(model, features: np.ndarray) -> np.ndarray:
    flat = features.reshape(-1, features.shape[-1])
    valid = np.all(np.isfinite(flat), axis=1)
    result = np.full(flat.shape[0], np.nan, dtype="float32")
    batch = 100_000
    valid_indices = np.flatnonzero(valid)
    for start in range(0, valid_indices.size, batch):
        indices = valid_indices[start : start + batch]
        result[indices] = model.predict_proba(flat[indices])[:, 1].astype("float32")
    return result.reshape(features.shape[:2])


def landsat_temperature(item, grid: Grid) -> np.ndarray:
    raw = read_asset_to_grid(
        item.assets["lwir11"].href,
        "landsat_2025_lwir11",
        grid,
        resampling=Resampling.bilinear,
    )
    qa = read_asset_to_grid(
        item.assets["qa_pixel"].href,
        "landsat_2025_qa_pixel",
        grid,
        resampling=Resampling.nearest,
        categorical=True,
    )
    band_meta = item.assets["lwir11"].extra_fields["raster:bands"][0]
    scale = float(band_meta["scale"])
    offset = float(band_meta["offset"])
    celsius = raw * scale + offset - 273.15
    bad_bits = sum(1 << bit for bit in [0, 1, 2, 3, 4, 5])
    clear = (qa & bad_bits) == 0
    plausible = np.isfinite(celsius) & (celsius >= 10) & (celsius <= 80)
    return np.where(clear & plausible, celsius, np.nan).astype("float32")


def aggregate_average(array: np.ndarray, source: Grid, destination: Grid) -> np.ndarray:
    out = np.full((destination.height, destination.width), np.nan, dtype="float32")
    reproject(
        source=array.astype("float32"),
        destination=out,
        src_transform=source.transform,
        src_crs=source.crs,
        src_nodata=np.nan,
        dst_transform=destination.transform,
        dst_crs=destination.crs,
        dst_nodata=np.nan,
        resampling=Resampling.average,
    )
    return out


def population_to_grid(path: Path, destination: Grid) -> np.ndarray:
    out = np.zeros((destination.height, destination.width), dtype="float32")
    with rasterio.open(path) as src:
        reproject(
            source=rasterio.band(src, 1),
            destination=out,
            src_transform=src.transform,
            src_crs=src.crs,
            src_nodata=src.nodata,
            dst_transform=destination.transform,
            dst_crs=destination.crs,
            dst_nodata=0,
            resampling=Resampling.sum,
        )
    out[~np.isfinite(out) | (out < 0)] = 0
    return out


def percentile_component(values: np.ndarray, eligible: np.ndarray, *, positive_only: bool = False) -> np.ndarray:
    out = np.zeros(values.shape, dtype="float32")
    valid = eligible & np.isfinite(values)
    if positive_only:
        valid &= values > 0
    if not np.any(valid):
        return out
    series = pd.Series(values[valid])
    out[valid] = series.rank(method="average", pct=True).to_numpy(dtype="float32")
    return out


def build_geojson(table: pd.DataFrame, grid: Grid, aoi_polygon) -> dict[str, Any]:
    features = []
    for _, row in table.iterrows():
        r = int(row["row"])
        c = int(row["col"])
        left = grid.transform.c + c * grid.resolution
        right = left + grid.resolution
        top = grid.transform.f - r * grid.resolution
        bottom = top - grid.resolution
        clipped = shapely_box(left, bottom, right, top).intersection(aoi_polygon)
        if clipped.is_empty:
            continue
        geometry = transform_geom(
            grid.crs,
            "EPSG:4326",
            mapping(clipped),
            precision=7,
        )
        properties = {
            key: (None if pd.isna(value) else value)
            for key, value in row.drop(labels=["row", "col"]).to_dict().items()
        }
        features.append(
            {
                "type": "Feature",
                "properties": properties,
                "geometry": geometry,
            }
        )
    return {"type": "FeatureCollection", "features": features}


def stretch_rgb(red: np.ndarray, green: np.ndarray, blue: np.ndarray) -> np.ndarray:
    channels = []
    for channel in [red, green, blue]:
        finite = channel[np.isfinite(channel)]
        low, high = np.nanpercentile(finite, [2, 98])
        scaled = np.clip((channel - low) / max(high - low, 1e-6), 0, 1)
        channels.append(np.nan_to_num(scaled, nan=0.0))
    rgb = np.stack(channels, axis=-1)
    return np.power(rgb, 0.85)


def draw_scalebar(ax, grid: Grid, length_km: int = 5) -> None:
    left, bottom, right, _ = grid.bounds
    x0 = left + 0.05 * (right - left)
    y0 = bottom + 0.06 * (grid.bounds[3] - bottom)
    length = length_km * 1000
    ax.plot([x0, x0 + length], [y0, y0], color="white", linewidth=5, solid_capstyle="butt")
    ax.plot([x0, x0 + length], [y0, y0], color="black", linewidth=1)
    ax.text(x0 + length / 2, y0 + 250, f"{length_km} km", ha="center", va="bottom", fontsize=8, color="black", bbox={"facecolor": "white", "alpha": 0.75, "edgecolor": "none"})


def save_visuals(
    grid: Grid,
    score_grid: Grid,
    s2_2025: dict[str, np.ndarray],
    probability_2018: np.ndarray,
    probability_2025: np.ndarray,
    new_built: np.ndarray,
    lst: np.ndarray,
    score: np.ndarray,
    table: pd.DataFrame,
    metrics: dict[str, Any],
    feature_importance: dict[str, float],
) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    extent = [grid.bounds[0], grid.bounds[2], grid.bounds[1], grid.bounds[3]]
    score_extent = [score_grid.bounds[0], score_grid.bounds[2], score_grid.bounds[1], score_grid.bounds[3]]

    fig, axes = plt.subplots(2, 2, figsize=(13, 10), constrained_layout=True)
    panels = [
        (probability_2018, "Built-up probability — May 2018", "magma", 0, 1),
        (probability_2025, "Built-up probability — May 2025", "magma", 0, 1),
        (new_built.astype(float), "Confirmed new built-up signal — 2018 to 2023", "Reds", 0, 1),
        (lst, "Landsat land-surface temperature — 10 May 2025 (°C)", "inferno", float(np.nanpercentile(lst, 2)), float(np.nanpercentile(lst, 98))),
    ]
    for ax, (data, title, cmap, vmin, vmax) in zip(axes.ravel(), panels):
        image = ax.imshow(data, extent=extent, origin="upper", cmap=cmap, vmin=vmin, vmax=vmax)
        ax.set_title(title, fontsize=11, weight="bold")
        ax.set_xlabel("UTM Easting (m)")
        ax.set_ylabel("UTM Northing (m)")
        fig.colorbar(image, ax=ax, shrink=0.78)
    fig.suptitle("Riyadh HeatReady — analysis evidence", fontsize=16, weight="bold")
    fig.savefig(OUTPUT_DIR / "analysis_overview.png", dpi=180, bbox_inches="tight")
    plt.close(fig)

    rgb = stretch_rgb(s2_2025["red"], s2_2025["green"], s2_2025["blue"])
    fig, ax = plt.subplots(figsize=(11, 9))
    ax.imshow(rgb, extent=extent, origin="upper")
    masked_score = np.ma.masked_invalid(score)
    overlay = ax.imshow(
        masked_score,
        extent=score_extent,
        origin="upper",
        cmap="turbo",
        vmin=0,
        vmax=100,
        alpha=0.58,
        interpolation="nearest",
    )
    ax.set_xlim(grid.bounds[0], grid.bounds[2])
    ax.set_ylim(grid.bounds[1], grid.bounds[3])
    top = table.nlargest(5, "priority_score")
    for rank, (_, row) in enumerate(top.iterrows(), start=1):
        r = int(row["row"])
        c = int(row["col"])
        left = score_grid.transform.c + c * score_grid.resolution
        top_y = score_grid.transform.f - r * score_grid.resolution
        ax.add_patch(
            Rectangle(
                (left, top_y - score_grid.resolution),
                score_grid.resolution,
                score_grid.resolution,
                fill=False,
                edgecolor="white",
                linewidth=2.5,
            )
        )
        ax.text(
            left + score_grid.resolution / 2,
            top_y - score_grid.resolution / 2,
            str(rank),
            ha="center",
            va="center",
            color="white",
            fontsize=11,
            weight="bold",
            bbox={"boxstyle": "circle,pad=0.25", "facecolor": "#111827", "alpha": 0.9, "edgecolor": "white"},
        )
    colorbar = fig.colorbar(overlay, ax=ax, shrink=0.72, pad=0.02)
    colorbar.set_label("Screening priority score (0–100)")
    ax.set_title("Riyadh HeatReady decision map\nTop zones where heat, population and recent growth overlap", fontsize=15, weight="bold")
    ax.set_xlabel("UTM Easting (m)")
    ax.set_ylabel("UTM Northing (m)")
    draw_scalebar(ax, grid)
    ax.annotate("N", xy=(0.96, 0.94), xytext=(0.96, 0.84), xycoords="axes fraction", textcoords="axes fraction", ha="center", va="center", fontsize=13, weight="bold", arrowprops={"facecolor": "black", "width": 2.5, "headwidth": 8})
    ax.text(0.01, 0.01, "Screening result — verify locally before action", transform=ax.transAxes, fontsize=8, bbox={"facecolor": "white", "alpha": 0.85, "edgecolor": "none"})
    fig.savefig(OUTPUT_DIR / "decision_map.png", dpi=200, bbox_inches="tight")
    plt.close(fig)

    importance = pd.Series(feature_importance).sort_values(ascending=True)
    fig, axes = plt.subplots(1, 2, figsize=(12, 5), constrained_layout=True)
    matrix = np.array(metrics["confusion_matrix"])
    axes[0].imshow(matrix, cmap="Blues")
    for i in range(2):
        for j in range(2):
            axes[0].text(j, i, f"{matrix[i, j]:,}", ha="center", va="center", fontsize=12, weight="bold")
    axes[0].set_xticks([0, 1], ["Other", "Built-up"])
    axes[0].set_yticks([0, 1], ["Other", "Built-up"])
    axes[0].set_xlabel("Predicted")
    axes[0].set_ylabel("WorldCover reference")
    axes[0].set_title("Spatial holdout check (east AOI)")
    axes[1].barh(importance.index, importance.values, color="#7c3aed")
    axes[1].set_xlabel("Random-forest feature importance")
    axes[1].set_title("What the classifier used")
    fig.suptitle(
        f"Validation evidence — F1 {metrics['f1']:.2f}, IoU {metrics['iou']:.2f}, balanced accuracy {metrics['balanced_accuracy']:.2f}",
        fontsize=13,
        weight="bold",
    )
    fig.savefig(OUTPUT_DIR / "validation.png", dpi=180, bbox_inches="tight")
    plt.close(fig)


def image_data_uri(path: Path) -> str:
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:image/png;base64,{encoded}"


def save_annual_timeseries(table: pd.DataFrame) -> None:
    """Plot the six annual land-cover estimates used as trend context."""
    fig, ax = plt.subplots(figsize=(10, 5.5), constrained_layout=True)
    years = table["year"].to_numpy()
    areas = table["built_area_km2"].to_numpy()
    ax.plot(years, areas, color="#7134ff", linewidth=3, marker="o", markersize=7)
    ax.fill_between(years, areas, color="#7134ff", alpha=0.10)
    for year, area in zip(years, areas):
        ax.annotate(
            f"{area:.1f}",
            (year, area),
            xytext=(0, 10),
            textcoords="offset points",
            ha="center",
            fontsize=9,
            weight="bold",
        )
    ax.set_xticks(years)
    ax.set_ylabel("Mapped built-up area inside AOI (km²)")
    ax.set_xlabel("Annual land-cover map year")
    ax.set_title("Annual mapped built-up trend — 2018 to 2023", fontsize=14, weight="bold")
    ax.grid(axis="y", alpha=0.25)
    ax.text(
        0.01,
        0.02,
        "Trend support from one annual land-cover product; not exact construction dates or field truth.",
        transform=ax.transAxes,
        fontsize=9,
        color="#5f6f69",
    )
    fig.savefig(OUTPUT_DIR / "annual_built_area_timeseries.png", dpi=180, bbox_inches="tight")
    plt.close(fig)


def build_dashboard(summary: dict[str, Any], table: pd.DataFrame) -> None:
    top_rows = table.nlargest(5, "priority_score")
    table_html = "".join(
        f"<tr><td>{rank}</td><td>{row.grid_id}</td><td>{row.priority_score:.1f}</td>"
        f"<td>{row.lst_mean_c:.1f} °C</td><td>{row.population_estimate:,.0f}</td>"
        f"<td>{row.new_built_fraction * 100:.1f}%</td></tr>"
        for rank, (_, row) in enumerate(top_rows.iterrows(), start=1)
    )
    decision_uri = image_data_uri(OUTPUT_DIR / "decision_map.png")
    overview_uri = image_data_uri(OUTPUT_DIR / "analysis_overview.png")
    validation_uri = image_data_uri(OUTPUT_DIR / "validation.png")
    annual_timeseries_uri = image_data_uri(OUTPUT_DIR / "annual_built_area_timeseries.png")
    tanager_section = ""
    tanager_path = OUTPUT_DIR / "tanager_material_analysis.png"
    tanager_summary_path = OUTPUT_DIR / "tanager_summary.json"
    if tanager_path.exists() and tanager_summary_path.exists():
        tanager = json.loads(tanager_summary_path.read_text(encoding="utf-8"))
        tanager_uri = image_data_uri(tanager_path)
        stats = tanager["class_statistics"]
        angle = tanager["spectral_angle_separation"]["growth_vs_likely_unbuilt_degrees"]
        strict = tanager.get("beta_cloud_mask_sensitivity", {})
        strict_note = ""
        if strict:
            strict_stats = strict["class_statistics"]
            strict_note = (
                " A stricter sensitivity test that excludes every beta-cloud-flagged "
                f"pixel keeps the same order ({strict_stats['Likely unbuilt']['ndbi']['median']:.3f} "
                f"versus {strict_stats['Established built']['ndbi']['median']:.3f})."
            )
        tanager_section = f"""
<section><div class=\"eyebrow\" style=\"color:var(--violet)\">Hyperspectral check</div><h2>Tanager adds material context, not change proof</h2><p class=\"sub\">The open Planet Tanager scene from 15 May 2025 separates the median spectrum of confirmed-growth surfaces from likely-unbuilt surfaces by {angle:.2f}°. It also exposes an important arid-city trap: median narrow-band NDBI was {stats['Likely unbuilt']['ndbi']['median']:.3f} for likely-unbuilt land, higher than {stats['Established built']['ndbi']['median']:.3f} for established built land.{strict_note} That is why the PoC does not call NDBI alone a building detector.</p><img src=\"{tanager_uri}\" alt=\"Planet Tanager spectral comparison\"><div class=\"warning\"><b>Correct data claim:</b> this is open Planet Tanager archive data. It is not Satellite 813 imagery. One Tanager date describes 2025 surface spectra but cannot prove 2018–2023 change.</div></section>
"""
    html = f"""<!doctype html>
<html lang=\"en\">
<head>
<meta charset=\"utf-8\">
<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
<title>Riyadh HeatReady</title>
<style>
:root{{--ink:#10231f;--muted:#5f6f69;--paper:#f6f4ed;--card:#ffffff;--lime:#c5ff54;--violet:#7134ff;--line:#d8ded8}}
*{{box-sizing:border-box}} body{{margin:0;background:var(--paper);color:var(--ink);font-family:Inter,Segoe UI,Arial,sans-serif;line-height:1.45}}
header{{padding:48px max(24px,7vw) 34px;background:linear-gradient(125deg,#082c27 0%,#13443a 72%,#266b58 100%);color:white}}
.eyebrow{{font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--lime);font-weight:800}}
h1{{font-size:clamp(36px,6vw,72px);line-height:.95;margin:14px 0 18px;max-width:850px}} .lead{{max-width:850px;font-size:18px;color:#d9eee7}}
main{{max-width:1280px;margin:auto;padding:30px 24px 70px}} .cards{{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-top:-52px}}
.card{{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:20px;box-shadow:0 9px 30px rgba(10,35,31,.08)}} .metric{{font-size:30px;font-weight:850;margin-top:6px}} .label{{font-size:12px;text-transform:uppercase;letter-spacing:.08em;color:var(--muted);font-weight:700}}
section{{margin-top:34px;background:var(--card);border:1px solid var(--line);border-radius:18px;padding:clamp(18px,3vw,34px)}} h2{{font-size:28px;margin:0 0 12px}} .sub{{color:var(--muted);max-width:850px}}
img{{width:100%;height:auto;border-radius:12px;border:1px solid var(--line);margin-top:18px}} table{{width:100%;border-collapse:collapse;margin-top:16px;font-size:14px}} th,td{{padding:11px 9px;border-bottom:1px solid var(--line);text-align:left}} th{{background:#edf5f0;font-size:12px;text-transform:uppercase;letter-spacing:.05em}}
.method{{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-top:18px}} .step{{background:#eef5f1;border-radius:12px;padding:15px}} .step b{{display:block;color:var(--violet);margin-bottom:5px}}
.warning{{border-left:5px solid #f4b740;background:#fff7df;padding:16px 18px;margin-top:18px;border-radius:8px}} footer{{max-width:1280px;margin:auto;padding:0 24px 50px;color:var(--muted);font-size:13px}}
@media(max-width:900px){{.cards,.method{{grid-template-columns:1fr 1fr}}}} @media(max-width:560px){{.cards,.method{{grid-template-columns:1fr}} main{{padding:20px 14px 50px}}}}
</style>
</head>
<body>
<header><div class=\"eyebrow\">Arab Youth Space Hackathon · Urban track · Proof of Concept</div><h1>Riyadh HeatReady</h1><p class=\"lead\">A transparent screening map that shows where separately mapped recent built-up growth, hotter surfaces and population exposure overlap along southeastern Riyadh's urban-industrial fringe.</p></header>
<main>
<div class=\"cards\">
<div class=\"card\"><div class=\"label\">Growth comparison</div><div class=\"metric\">2018–2023</div></div>
<div class=\"card\"><div class=\"label\">Confirmed growth signal</div><div class=\"metric\">{summary['new_built_area_km2']:.1f} km²</div></div>
<div class=\"card\"><div class=\"label\">Mean May surface temperature</div><div class=\"metric\">{summary['lst_mean_c']:.1f} °C</div></div>
<div class=\"card\"><div class=\"label\">Population estimate in AOI</div><div class=\"metric\">{summary['population_estimate']:,.0f}</div></div>
</div>
<section><div class=\"eyebrow\" style=\"color:var(--violet)\">Decision output</div><h2>Inspect these zones first</h2><p class=\"sub\">The score is a transparent ranking: 40% heat, 30% population, 20% recent built-up growth, and 10% lack of vegetation. It helps a planning team decide where to check conditions and assess locally suitable cooling actions.</p><img src=\"{decision_uri}\" alt=\"Riyadh HeatReady decision map\">
<table><thead><tr><th>Rank</th><th>Grid cell</th><th>Score</th><th>Mean LST</th><th>Modelled population</th><th>New built signal</th></tr></thead><tbody>{table_html}</tbody></table></section>
<section><div class=\"eyebrow\" style=\"color:var(--violet)\">Time-series check</div><h2>Annual built-up trend</h2><p class=\"sub\">Six annual land-cover maps show how mapped built-up area changed from 2018 through 2023. This supports the endpoint comparison, but it does not prove the exact year when each building appeared.</p><img src=\"{annual_timeseries_uri}\" alt=\"Annual mapped built-up area from 2018 through 2023\"></section>
<section><div class=\"eyebrow\" style=\"color:var(--violet)\">How it works</div><h2>One explainable chain of evidence</h2><div class=\"method\"><div class=\"step\"><b>1 · Map surfaces</b>Sentinel-2 optical bands separate vegetation, bare land and built-like spectra.</div><div class=\"step\"><b>2 · Reduce desert confusion</b>Sentinel-1 radar adds surface-structure evidence.</div><div class=\"step\"><b>3 · Add heat</b>Landsat thermal data provides same-season land-surface temperature.</div><div class=\"step\"><b>4 · Add exposure</b>WorldPop supplies a modelled 2025 population layer.</div></div><img src=\"{overview_uri}\" alt=\"Analysis evidence maps\"></section>
<section><div class=\"eyebrow\" style=\"color:var(--violet)\">Delivery and pilot</div><h2>From a working PoC to a municipal test</h2><p class=\"sub\">Potential adopter, not a claimed customer: a municipal urban-planning or heat-resilience team. The value hypothesis is that one ranked view can reduce the effort of manually comparing separate growth, heat, vegetation, and population layers.</p><div class=\"method\"><div class=\"step\"><b>Deliver</b>Refreshable dashboard plus CSV, GeoJSON, and GeoTIFF outputs for an existing GIS workflow.</div><div class=\"step\"><b>Pilot</b>Review the top five zones against local plans and field observations.</div><div class=\"step\"><b>Measure</b>Record usefulness, errors, analyst time, operating cost, and missing local data.</div><div class=\"step\"><b>Scale carefully</b>Repeat AOI by AOI; add commercial or city data only after access and licences are confirmed.</div></div><div class=\"warning\"><b>Business claim boundary:</b> no municipality, paying customer, price, revenue, saved time, or deployment agreement is claimed.</div></section>
{tanager_section}
<section><div class=\"eyebrow\" style=\"color:var(--violet)\">Validation</div><h2>Tested against a spatially separate reference area</h2><p class=\"sub\">The 2021 fusion model was trained on the western part of the AOI, tuned in a separate middle strip, and checked in the eastern part against ESA WorldCover built-up labels. This is a reference-agreement test, not field-verified accuracy.</p><img src=\"{validation_uri}\" alt=\"Validation and feature importance\">
<div class=\"warning\"><b>Use this as a screening tool.</b> Land-surface temperature is not air temperature or personal heat exposure. WorldPop is modelled, industrial worker exposure may be missed, and bright roofs or compacted soil can confuse satellite classification. Every priority zone needs local review and field checking.</div></section>
</main><footer>Open-data PoC. Sources: Sentinel-1 RTC, Sentinel-2 L2A, Landsat Collection 2 Level-2, ESA WorldCover 2021, WorldPop 2025, and Planet Tanager open-archive metadata/imagery. Exact item IDs and licences are recorded with the project.</footer>
</body></html>"""
    (OUTPUT_DIR / "dashboard.html").write_text(html, encoding="utf-8")


def main() -> None:
    config = load_config()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    grid = make_grid(config, float(config["analysis_resolution_m"]))
    score_grid = make_grid(config, float(config["priority_grid_m"]))
    aoi_polygon = make_aoi_polygon(config)
    analysis_aoi_mask = grid_center_mask(aoi_polygon, grid)
    score_aoi_mask = grid_center_mask(aoi_polygon, score_grid)
    score_aoi_coverage = grid_coverage_fraction(aoi_polygon, score_grid)
    catalog = Client.open(config["stac_api"])

    epochs: dict[str, dict[str, Any]] = {}
    for year in ["2018", "2021", "2025"]:
        s2_item = open_item(catalog, config["items"][f"sentinel2_{year}"])
        s1_item = open_item(catalog, config["items"][f"sentinel1_{year}"])
        s2 = sentinel2_epoch(s2_item, f"sentinel2_{year}", grid)
        s1 = sentinel1_epoch(s1_item, f"sentinel1_{year}", grid)
        epochs[year] = {"s2": s2, "s1": s1, "features": build_epoch_features(s2, s1)}
        print(f"Prepared {year} optical + radar features")

    worldcover_item = open_item(catalog, config["items"]["worldcover_2021"])
    worldcover = read_asset_to_grid(
        worldcover_item.assets["map"].href,
        "worldcover_2021_map",
        grid,
        resampling=Resampling.nearest,
        categorical=True,
    )
    labels = (worldcover == 50).astype("uint8")
    features_2021 = epochs["2021"]["features"]
    finite_2021 = (
        np.all(np.isfinite(features_2021), axis=-1)
        & (worldcover > 0)
        & analysis_aoi_mask
    )
    columns = np.indices((grid.height, grid.width))[1]
    train_mask = finite_2021 & (columns < int(grid.width * 0.55))
    tune_mask = finite_2021 & (columns >= int(grid.width * 0.60)) & (columns < int(grid.width * 0.75))
    test_mask = finite_2021 & (columns >= int(grid.width * 0.80))
    if min(train_mask.sum(), tune_mask.sum(), test_mask.sum()) < 1_000:
        raise RuntimeError("Spatial validation strips do not contain enough valid pixels")

    train_x, train_y = sample_balanced(features_2021, labels, train_mask)
    model = RandomForestClassifier(
        n_estimators=260,
        max_depth=14,
        min_samples_leaf=6,
        max_features="sqrt",
        class_weight="balanced_subsample",
        n_jobs=-1,
        random_state=42,
    )
    model.fit(train_x, train_y)
    probability_2021 = predict_probability(model, features_2021)
    threshold = choose_threshold(labels[tune_mask], probability_2021[tune_mask])
    predicted_test = probability_2021[test_mask] >= threshold
    truth_test = labels[test_mask]
    matrix = confusion_matrix(truth_test, predicted_test, labels=[0, 1])
    intersection = int(np.logical_and(truth_test == 1, predicted_test).sum())
    union = int(np.logical_or(truth_test == 1, predicted_test).sum())
    metrics = {
        "reference": "ESA WorldCover 2021 built-up class (50)",
        "split": "west train / middle tune / east test with gaps",
        "threshold": threshold,
        "test_pixels": int(test_mask.sum()),
        "accuracy": float(accuracy_score(truth_test, predicted_test)),
        "balanced_accuracy": float(balanced_accuracy_score(truth_test, predicted_test)),
        "precision": float(precision_score(truth_test, predicted_test, zero_division=0)),
        "recall": float(recall_score(truth_test, predicted_test, zero_division=0)),
        "f1": float(f1_score(truth_test, predicted_test, zero_division=0)),
        "iou": float(intersection / union) if union else 0.0,
        "confusion_matrix": matrix.tolist(),
        "important_caveat": "Reference agreement is not independent field-verified accuracy; WorldCover is also satellite-derived.",
    }
    feature_importance = {
        name: float(value) for name, value in zip(FEATURE_NAMES, model.feature_importances_)
    }
    (OUTPUT_DIR / "validation_metrics.json").write_text(
        json.dumps({"metrics": metrics, "feature_importance": feature_importance}, indent=2),
        encoding="utf-8",
    )
    print(f"Spatial holdout F1={metrics['f1']:.3f}, IoU={metrics['iou']:.3f}, threshold={threshold:.2f}")

    probability_2018 = predict_probability(model, epochs["2018"]["features"])
    probability_2025 = predict_probability(model, epochs["2025"]["features"])
    probability_2018[~analysis_aoi_mask] = np.nan
    probability_2021[~analysis_aoi_mask] = np.nan
    probability_2025[~analysis_aoi_mask] = np.nan
    built_2018 = clean_binary(probability_2018 >= threshold, minimum_pixels=9)
    built_2025 = clean_binary(probability_2025 >= threshold, minimum_pixels=9)
    probability_delta = probability_2025 - probability_2018

    # Six annual land-cover maps show the trend. The endpoint change remains the
    # conservative proposal: the fusion model must also confirm that it looks
    # built-up in 2025 and became more built-like since 2018.
    annual_lulc: dict[int, np.ndarray] = {}
    annual_built: dict[int, np.ndarray] = {}
    for year in range(2018, 2024):
        label = f"annual_lulc_{year}"
        item = open_item(catalog, config["items"][label])
        annual_lulc[year] = read_asset_to_grid(
            item.assets["data"].href,
            label,
            grid,
            resampling=Resampling.nearest,
            categorical=True,
        )
        annual_built[year] = analysis_aoi_mask & (annual_lulc[year] == 7)
    annual_lulc_2018 = annual_lulc[2018]
    annual_lulc_2023 = annual_lulc[2023]
    annual_built_2018 = annual_built[2018]
    annual_built_2023 = annual_built[2023]
    annual_growth = clean_binary(
        analysis_aoi_mask
        & (annual_lulc_2018 > 0)
        & (annual_lulc_2023 > 0)
        & ~annual_built_2018
        & annual_built_2023,
        minimum_pixels=6,
    )
    new_built = clean_binary(
        annual_growth
        & (probability_2025 >= threshold)
        & (probability_delta >= 0.10),
        minimum_pixels=6,
    )

    landsat_item = open_item(catalog, config["items"]["landsat_2025"])
    lst = landsat_temperature(landsat_item, grid)
    lst[~analysis_aoi_mask] = np.nan
    ndvi_2025 = epochs["2025"]["s2"]["ndvi"].copy()
    ndvi_2025[~analysis_aoi_mask] = np.nan

    built_fraction_2018 = aggregate_average(
        np.where(np.isfinite(probability_2018), built_2018.astype("float32"), np.nan), grid, score_grid
    )
    built_fraction_2025 = aggregate_average(
        np.where(np.isfinite(probability_2025), built_2025.astype("float32"), np.nan), grid, score_grid
    )
    new_built_fraction = aggregate_average(
        np.where(np.isfinite(probability_delta), new_built.astype("float32"), np.nan), grid, score_grid
    )
    lst_mean = aggregate_average(lst, grid, score_grid)
    ndvi_mean = aggregate_average(ndvi_2025, grid, score_grid)
    population_path = RAW_DIR / "worldpop_sau_2025_1km.tif"
    if not population_path.exists():
        raise RuntimeError("WorldPop file missing. Run verify_sources.py first.")
    population = population_to_grid(population_path, score_grid) * score_aoi_coverage

    eligible = (
        score_aoi_mask
        & np.isfinite(lst_mean)
        & np.isfinite(built_fraction_2018)
        & np.isfinite(built_fraction_2025)
        & np.isfinite(ndvi_mean)
        & (new_built_fraction > 0)
    )
    heat_component = percentile_component(lst_mean, eligible)
    population_component = percentile_component(np.log1p(population), eligible)
    growth_component = percentile_component(new_built_fraction, eligible, positive_only=True)
    lack_green_component = percentile_component(-ndvi_mean, eligible)
    priority = np.full(lst_mean.shape, np.nan, dtype="float32")
    priority[eligible] = 100.0 * (
        0.40 * heat_component[eligible]
        + 0.30 * population_component[eligible]
        + 0.20 * growth_component[eligible]
        + 0.10 * lack_green_component[eligible]
    )
    high_cut = float(np.nanpercentile(priority[eligible], 80))
    medium_cut = float(np.nanpercentile(priority[eligible], 50))

    rows: list[dict[str, Any]] = []
    for r in range(score_grid.height):
        for c in range(score_grid.width):
            if not eligible[r, c]:
                continue
            east, north = xy(score_grid.transform, r, c, offset="center")
            lon, lat = transform(score_grid.crs, "EPSG:4326", [east], [north])
            score = float(priority[r, c])
            category = "High" if score >= high_cut else "Medium" if score >= medium_cut else "Watch"
            rows.append(
                {
                    "grid_id": f"R{r + 1:02d}C{c + 1:02d}",
                    "row": r,
                    "col": c,
                    "longitude": float(lon[0]),
                    "latitude": float(lat[0]),
                    "priority_score": score,
                    "priority_class": category,
                    "lst_mean_c": float(lst_mean[r, c]),
                    "population_estimate": float(population[r, c]),
                    "built_fraction_2018": float(built_fraction_2018[r, c]),
                    "built_fraction_2025": float(built_fraction_2025[r, c]),
                    "new_built_fraction": float(new_built_fraction[r, c]),
                    "aoi_coverage_fraction": float(score_aoi_coverage[r, c]),
                    "ndvi_mean_2025": float(ndvi_mean[r, c]),
                    "heat_component": float(heat_component[r, c]),
                    "population_component": float(population_component[r, c]),
                    "growth_component": float(growth_component[r, c]),
                    "lack_green_component": float(lack_green_component[r, c]),
                }
            )
    table = pd.DataFrame(rows).sort_values("priority_score", ascending=False).reset_index(drop=True)
    table.to_csv(OUTPUT_DIR / "priority_zones.csv", index=False)
    geojson = build_geojson(table, score_grid, aoi_polygon)
    (OUTPUT_DIR / "priority_zones.geojson").write_text(
        json.dumps(geojson, indent=2), encoding="utf-8"
    )

    pixel_area_km2 = (grid.resolution ** 2) / 1_000_000.0
    annual_timeseries = pd.DataFrame(
        {
            "year": list(range(2018, 2024)),
            "built_area_km2": [
                float(annual_built[year].sum() * pixel_area_km2)
                for year in range(2018, 2024)
            ],
        }
    )
    annual_timeseries["year_to_year_change_km2"] = annual_timeseries[
        "built_area_km2"
    ].diff()
    annual_timeseries.to_csv(
        OUTPUT_DIR / "annual_built_area_timeseries.csv", index=False
    )
    valid_lst = lst[np.isfinite(lst)]
    summary = {
        "project_name": config["project_name"],
        "problem_statement": config["problem_statement"],
        "aoi": config["aoi_name"],
        "analysis_period": "Built-up change: 2018 to 2023; heat and exposure context: 2025",
        "aoi_bbox_wgs84": config["aoi_bbox_wgs84"],
        "analysis_area_km2": float(aoi_polygon.area / 1_000_000.0),
        "annual_lulc_built_area_2018_km2": float(annual_built_2018.sum() * pixel_area_km2),
        "annual_lulc_built_area_2023_km2": float(annual_built_2023.sum() * pixel_area_km2),
        "annual_lulc_built_area_timeseries_km2": {
            str(int(row.year)): float(row.built_area_km2)
            for row in annual_timeseries.itertuples(index=False)
        },
        "annual_lulc_candidate_growth_km2": float(annual_growth.sum() * pixel_area_km2),
        "new_built_area_km2": float(new_built.sum() * pixel_area_km2),
        "lst_mean_c": float(np.mean(valid_lst)),
        "lst_p90_c": float(np.percentile(valid_lst, 90)),
        "population_estimate": float(population.sum()),
        "eligible_grid_cells": int(eligible.sum()),
        "high_priority_grid_cells": int((priority >= high_cut).sum()),
        "priority_weights": {
            "heat": 0.40,
            "population": 0.30,
            "recent_growth": 0.20,
            "lack_of_vegetation": 0.10,
        },
        "validation": metrics,
        "top_priority_zones": table.head(5)[
            [
                "grid_id",
                "longitude",
                "latitude",
                "priority_score",
                "lst_mean_c",
                "population_estimate",
                "new_built_fraction",
            ]
        ].to_dict(orient="records"),
        "limitations": [
            "This is a screening model, not an automatic policy decision.",
            "Land-surface temperature is not air temperature or personal heat exposure.",
            "WorldPop is a modelled population estimate and may miss industrial worker exposure.",
            "Bright roofs, compacted soil, and bare desert can confuse built-up classification.",
            "The growth layer is an intersection of an annual land-cover change product and an optical-radar confirmation rule; it can miss real change that either source fails to detect.",
            "WorldCover agreement is not independent field-verified accuracy.",
            "The open Tanager scene is one date, so it cannot independently prove change.",
        ],
    }
    tanager_summary_path = OUTPUT_DIR / "tanager_summary.json"
    if tanager_summary_path.exists():
        summary["tanager"] = json.loads(tanager_summary_path.read_text(encoding="utf-8"))
    (OUTPUT_DIR / "results_summary.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )

    write_raster(OUTPUT_DIR / "built_probability_2018.tif", probability_2018, grid, nodata=-9999.0, dtype="float32")
    write_raster(OUTPUT_DIR / "built_probability_2025.tif", probability_2025, grid, nodata=-9999.0, dtype="float32")
    annual_growth_output = np.where(analysis_aoi_mask, annual_growth, 255).astype("uint8")
    new_built_output = np.where(analysis_aoi_mask, new_built, 255).astype("uint8")
    write_raster(OUTPUT_DIR / "annual_lulc_candidate_growth_2018_2023.tif", annual_growth_output, grid, nodata=255, dtype="uint8")
    write_raster(OUTPUT_DIR / "confirmed_built_growth_2018_2023.tif", new_built_output, grid, nodata=255, dtype="uint8")
    write_raster(OUTPUT_DIR / "land_surface_temperature_2025_c.tif", lst, grid, nodata=-9999.0, dtype="float32")
    write_raster(OUTPUT_DIR / "priority_score_1km.tif", priority, score_grid, nodata=-9999.0, dtype="float32")

    save_visuals(
        grid,
        score_grid,
        epochs["2025"]["s2"],
        probability_2018,
        probability_2025,
        new_built,
        lst,
        priority,
        table,
        metrics,
        feature_importance,
    )
    save_annual_timeseries(annual_timeseries)
    build_dashboard(summary, table)
    print(json.dumps({"status": "complete", "summary": summary}, indent=2))


if __name__ == "__main__":
    main()
