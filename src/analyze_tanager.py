"""Use the open Planet Tanager scene for narrow-band surface context.

This does not call the Tanager scene "Satellite 813" and does not use one date to
claim change. It asks a narrower question: do the surfaces inside independently
mapped growth areas have measurably different 2025 spectra from established built
and likely-unbuilt areas?
"""

from __future__ import annotations

import json
import math
import re
from pathlib import Path
from typing import Any

import h5py
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import rasterio
import requests
from rasterio.enums import Resampling
from rasterio.transform import from_bounds
from rasterio.warp import reproject


ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "tanager_riyadh_20250515_ortho_sr.h5"
OUTPUT_DIR = ROOT / "outputs"
HDF_ROOT = "HDFEOS/GRIDS/HYP/Data Fields"


def valid_tanager_file(path: Path) -> bool:
    try:
        with h5py.File(path, "r") as h5:
            surface = h5[f"{HDF_ROOT}/surface_reflectance"]
            return (
                surface.ndim == 3
                and surface.shape[0] > 100
                and "wavelengths" in surface.attrs
            )
    except Exception:
        return False


def ensure_tanager_file() -> None:
    if RAW.exists() and RAW.stat().st_size > 0 and valid_tanager_file(RAW):
        return
    config = json.loads((ROOT / "config.json").read_text(encoding="utf-8"))
    spec = config["items"]["tanager_2025"]
    item_url = f"{spec['collection_url']}/{spec['id']}/{spec['id']}.json"
    item_response = requests.get(item_url, timeout=60)
    item_response.raise_for_status()
    item = item_response.json()
    asset_url = item["assets"]["ortho_sr_hdf5"]["href"]
    RAW.parent.mkdir(parents=True, exist_ok=True)
    part = RAW.with_suffix(".h5.part")
    print("Downloading the one open Tanager HDF5 scene (about 856 MB)...", flush=True)
    with requests.get(asset_url, stream=True, timeout=180) as response:
        response.raise_for_status()
        with part.open("wb") as handle:
            for chunk in response.iter_content(chunk_size=4 * 1024 * 1024):
                if chunk:
                    handle.write(chunk)
    if not valid_tanager_file(part):
        raise RuntimeError("Downloaded Tanager HDF5 file is invalid")
    part.replace(RAW)


def parse_grid(h5: h5py.File) -> tuple[str, rasterio.Affine, int, int]:
    text = h5["HDFEOS INFORMATION/StructMetadata.0"][()].decode("utf-8")
    xdim = int(re.search(r"XDim=(\d+)", text).group(1))
    ydim = int(re.search(r"YDim=(\d+)", text).group(1))
    ul_match = re.search(r"UpperLeftPointMtrs=\(([-\d.]+),([-\d.]+)\)", text)
    lr_match = re.search(r"LowerRightMtrs=\(([-\d.]+),([-\d.]+)\)", text)
    zone = int(re.search(r"ZoneCode=(\d+)", text).group(1))
    left, top = map(float, ul_match.groups())
    right, bottom = map(float, lr_match.groups())
    crs = f"EPSG:{32600 + zone}"
    return crs, from_bounds(left, bottom, right, top, xdim, ydim), xdim, ydim


def reproject_raster(path: Path, crs: str, transform, width: int, height: int, resampling: Resampling) -> np.ndarray:
    out = np.full((height, width), np.nan, dtype="float32")
    with rasterio.open(path) as src:
        reproject(
            source=rasterio.band(src, 1),
            destination=out,
            src_transform=src.transform,
            src_crs=src.crs,
            src_nodata=src.nodata,
            dst_transform=transform,
            dst_crs=crs,
            dst_nodata=np.nan,
            resampling=resampling,
        )
    return out


def pick_band(wavelengths: np.ndarray, target_nm: float) -> int:
    return int(np.argmin(np.abs(wavelengths - target_nm)))


def safe_index(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    denominator = a + b
    out = np.full(a.shape, np.nan, dtype="float32")
    valid = np.isfinite(a) & np.isfinite(b) & (np.abs(denominator) > 1e-6)
    out[valid] = (a[valid] - b[valid]) / denominator[valid]
    return out


def spectral_angle_degrees(a: np.ndarray, b: np.ndarray) -> float:
    valid = np.isfinite(a) & np.isfinite(b)
    av = a[valid]
    bv = b[valid]
    cosine = float(np.dot(av, bv) / (np.linalg.norm(av) * np.linalg.norm(bv)))
    return math.degrees(math.acos(float(np.clip(cosine, -1, 1))))


def summarize(values: np.ndarray) -> dict[str, float]:
    finite = values[np.isfinite(values)]
    return {
        "count": int(finite.size),
        "median": float(np.median(finite)),
        "p25": float(np.percentile(finite, 25)),
        "p75": float(np.percentile(finite, 75)),
    }


def main() -> None:
    ensure_tanager_file()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    with h5py.File(RAW, "r") as h5:
        crs, transform, width, height = parse_grid(h5)
        fields = h5[HDF_ROOT]
        surface = fields["surface_reflectance"]
        wavelengths = np.asarray(surface.attrs["wavelengths"], dtype="float32")
        sensor_good = np.asarray(surface.attrs["good_wavelengths"], dtype=bool)
        nodata = fields["nodata_pixels"][:] == 0
        cloud_flag = fields["beta_cloud_mask"][:] != 0
        cirrus_flag = fields["beta_cirrus_mask"][:] != 0

        # The thumbnail is visually cloud-free, while the beta cloud mask flags
        # much of the bright desert/urban scene. We therefore use the nodata mask
        # for this descriptive analysis and report the cloud-mask disagreement.
        valid = nodata & ~cirrus_flag

        probability_2018 = reproject_raster(
            OUTPUT_DIR / "built_probability_2018.tif", crs, transform, width, height, Resampling.bilinear
        )
        probability_2025 = reproject_raster(
            OUTPUT_DIR / "built_probability_2025.tif", crs, transform, width, height, Resampling.bilinear
        )
        growth = reproject_raster(
            OUTPUT_DIR / "confirmed_built_growth_2018_2023.tif", crs, transform, width, height, Resampling.nearest
        ) >= 0.5

        classes = {
            "Confirmed growth": valid & growth,
            "Established built": valid & ~growth & (probability_2018 >= 0.80) & (probability_2025 >= 0.80),
            "Likely unbuilt": valid & (probability_2018 <= 0.20) & (probability_2025 <= 0.20),
        }

        target_bands = {
            "red": pick_band(wavelengths, 665),
            "red_edge": pick_band(wavelengths, 705),
            "nir": pick_band(wavelengths, 830),
            "swir1": pick_band(wavelengths, 1610),
        }
        band_arrays = {
            name: np.asarray(surface[index, :, :], dtype="float32")
            for name, index in target_bands.items()
        }
        for array in band_arrays.values():
            array[(array <= -1) | (array > 1.5) | ~valid] = np.nan
        ndvi = safe_index(band_arrays["nir"], band_arrays["red"])
        ndbi = safe_index(band_arrays["swir1"], band_arrays["nir"])
        red_edge_slope = band_arrays["nir"] - band_arrays["red_edge"]

        # Keep instrument-approved bands, remove atmospheric absorption windows,
        # and remove the noisy detector edge above 2450 nm.
        good = (
            sensor_good
            & ~((wavelengths >= 1350) & (wavelengths <= 1450))
            & ~((wavelengths >= 1800) & (wavelengths <= 1950))
            & (wavelengths <= 2450)
        )
        good_indices = np.flatnonzero(good)
        stride = 3
        cube = np.asarray(surface[good_indices, ::stride, ::stride], dtype="float32")
        cube[(cube <= -1) | (cube > 1.5)] = np.nan
        wavelengths_good = wavelengths[good_indices]

    class_stats: dict[str, Any] = {}
    strict_cloud_mask_stats: dict[str, Any] = {}
    spectra: dict[str, dict[str, np.ndarray]] = {}
    rng = np.random.default_rng(42)
    for name, full_mask in classes.items():
        sampled_mask = full_mask[::stride, ::stride]
        coordinates = np.flatnonzero(sampled_mask.ravel())
        if coordinates.size < 20:
            raise RuntimeError(f"Not enough Tanager samples for {name}: {coordinates.size}")
        if coordinates.size > 5000:
            coordinates = rng.choice(coordinates, size=5000, replace=False)
        flat_cube = cube.reshape(cube.shape[0], -1)[:, coordinates]
        median = np.nanmedian(flat_cube, axis=1)
        p25 = np.nanpercentile(flat_cube, 25, axis=1)
        p75 = np.nanpercentile(flat_cube, 75, axis=1)
        spectra[name] = {"median": median, "p25": p25, "p75": p75}
        class_stats[name] = {
            "sampled_spectral_pixels": int(coordinates.size),
            "full_resolution_pixels": int(full_mask.sum()),
            "ndvi": summarize(ndvi[full_mask]),
            "ndbi": summarize(ndbi[full_mask]),
            "red_edge_slope": summarize(red_edge_slope[full_mask]),
        }
        strict_mask = full_mask & ~cloud_flag
        strict_cloud_mask_stats[name] = {
            "full_resolution_pixels": int(strict_mask.sum()),
            "ndbi": summarize(ndbi[strict_mask]),
        }

    strict_ndbi_medians = {
        name: values["ndbi"]["median"]
        for name, values in strict_cloud_mask_stats.items()
    }
    strict_ndbi_order = sorted(
        strict_ndbi_medians,
        key=strict_ndbi_medians.get,
        reverse=True,
    )

    angles = {
        "growth_vs_established_degrees": spectral_angle_degrees(
            spectra["Confirmed growth"]["median"], spectra["Established built"]["median"]
        ),
        "growth_vs_likely_unbuilt_degrees": spectral_angle_degrees(
            spectra["Confirmed growth"]["median"], spectra["Likely unbuilt"]["median"]
        ),
        "established_vs_likely_unbuilt_degrees": spectral_angle_degrees(
            spectra["Established built"]["median"], spectra["Likely unbuilt"]["median"]
        ),
    }

    colors = {
        "Confirmed growth": "#d9485f",
        "Established built": "#6d3ce8",
        "Likely unbuilt": "#2b9a72",
    }
    fig, axes = plt.subplots(1, 2, figsize=(14, 5.5), constrained_layout=True)
    for name, values in spectra.items():
        color = colors[name]
        axes[0].plot(wavelengths_good, values["median"], label=name, color=color, linewidth=1.8)
        axes[0].fill_between(wavelengths_good, values["p25"], values["p75"], color=color, alpha=0.14)
    axes[0].axvspan(1350, 1450, color="#d1d5db", alpha=0.5)
    axes[0].axvspan(1800, 1950, color="#d1d5db", alpha=0.5)
    axes[0].set_xlabel("Wavelength (nm)")
    axes[0].set_ylabel("Surface reflectance")
    axes[0].set_title("Tanager median spectra (shading = middle 50%)")
    axes[0].grid(alpha=0.2)
    axes[0].legend(frameon=False)

    labels = list(classes)
    box_data = [ndbi[classes[name] & np.isfinite(ndbi)] for name in labels]
    boxes = axes[1].boxplot(box_data, tick_labels=labels, patch_artist=True, showfliers=False)
    for patch, name in zip(boxes["boxes"], labels):
        patch.set_facecolor(colors[name])
        patch.set_alpha(0.75)
    axes[1].axhline(0, color="#374151", linewidth=0.8)
    axes[1].set_ylabel("Narrow-band NDBI")
    axes[1].set_title("One narrow-band material indicator")
    axes[1].tick_params(axis="x", rotation=12)
    fig.suptitle("Open Planet Tanager scene — 15 May 2025 material context", fontsize=15, weight="bold")
    fig.savefig(OUTPUT_DIR / "tanager_material_analysis.png", dpi=190, bbox_inches="tight")
    plt.close(fig)

    result = {
        "source": "Planet Tanager open archive",
        "item_id": "20250515_080954_16_4001",
        "date": "2025-05-15",
        "role_in_project": "Descriptive 2025 surface-material context; not change proof and not Satellite 813 data.",
        "grid": {"crs": crs, "width": width, "height": height, "resolution_m": 30},
        "valid_pixel_fraction": float(valid.mean()),
        "beta_cloud_flag_fraction": float(cloud_flag.mean()),
        "cloud_mask_note": "The beta cloud mask flagged much of a visually cloud-free bright desert/urban scene, so it was reported but not used as the primary validity mask.",
        "selected_band_indices": target_bands,
        "selected_band_wavelengths_nm": {
            name: float(wavelengths[index]) for name, index in target_bands.items()
        },
        "class_statistics": class_stats,
        "beta_cloud_mask_sensitivity": {
            "purpose": "Checks whether the narrow-band NDBI pattern remains when every pixel flagged by the beta cloud mask is excluded.",
            "class_statistics": strict_cloud_mask_stats,
            "ndbi_order_high_to_low": strict_ndbi_order,
        },
        "spectral_angle_separation": angles,
        "conclusion": "Tanager shows measurable spectral differences among independently defined surface groups. It adds material context, but the single scene is not used to claim growth or heat exposure.",
        "limitations": [
            "The classes were defined using other satellite products, so this is descriptive comparison rather than independent validation.",
            "Mixed 30 m pixels can contain several materials.",
            "Spectral separation does not by itself identify a specific roofing or pavement material.",
            "Field spectra or labelled local materials would be required for material classification.",
        ],
    }
    (OUTPUT_DIR / "tanager_summary.json").write_text(
        json.dumps(result, indent=2), encoding="utf-8"
    )
    rows = []
    for name, stats in class_stats.items():
        rows.append(
            {
                "surface_group": name,
                "sampled_pixels": stats["sampled_spectral_pixels"],
                "median_ndvi": stats["ndvi"]["median"],
                "median_ndbi": stats["ndbi"]["median"],
                "median_red_edge_slope": stats["red_edge_slope"]["median"],
            }
        )
    import csv

    with (OUTPUT_DIR / "tanager_surface_groups.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
