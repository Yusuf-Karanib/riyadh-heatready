"""Verify that every planned data source is reachable and intersects the AOI.

This script reads only a tiny window from each cloud raster. It does not download
whole Sentinel, Landsat, WorldCover, or Tanager hyperspectral scenes.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import numpy as np
import planetary_computer
import rasterio
import requests
from pystac_client import Client
from rasterio.warp import transform_bounds
from rasterio.windows import from_bounds


ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "config.json"
RAW_DIR = ROOT / "data" / "raw"
OUTPUT_DIR = ROOT / "outputs"


def load_config() -> dict[str, Any]:
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


def open_pc_item(catalog: Client, spec: dict[str, str]):
    item = catalog.get_collection(spec["collection"]).get_item(spec["id"])
    if item is None:
        raise RuntimeError(f"STAC item not found: {spec['collection']} / {spec['id']}")
    return planetary_computer.sign(item)


def read_small_sample(href: str, bbox_wgs84: list[float]) -> dict[str, Any]:
    env_options = {
        "GDAL_DISABLE_READDIR_ON_OPEN": "EMPTY_DIR",
        "CPL_VSIL_CURL_ALLOWED_EXTENSIONS": ".tif,.TIF,.tiff,.TIFF",
    }
    with rasterio.Env(**env_options), rasterio.open(href) as src:
        bounds = transform_bounds("EPSG:4326", src.crs, *bbox_wgs84, densify_pts=21)
        window = from_bounds(*bounds, transform=src.transform).round_offsets().round_lengths()
        sample = src.read(1, window=window, out_shape=(64, 64), masked=True)
        values = np.asarray(sample.compressed(), dtype="float64")
        if values.size == 0:
            raise RuntimeError("AOI sample contained no valid pixels")
        return {
            "crs": str(src.crs),
            "source_width": src.width,
            "source_height": src.height,
            "sample_valid_pixels": int(values.size),
            "sample_min": float(np.nanmin(values)),
            "sample_max": float(np.nanmax(values)),
        }


def download_worldpop(config: dict[str, Any]) -> Path:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    target = RAW_DIR / "worldpop_sau_2025_1km.tif"
    if target.exists() and target.stat().st_size > 0:
        try:
            with rasterio.open(target) as src:
                if src.crs is not None and src.width > 0 and src.height > 0:
                    src.read(1, window=((0, 1), (0, 1)))
                    return target
        except Exception:
            pass
    part = target.with_suffix(".tif.part")
    with requests.get(config["worldpop"]["url"], stream=True, timeout=120) as response:
        response.raise_for_status()
        with part.open("wb") as handle:
            for chunk in response.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    handle.write(chunk)
    with rasterio.open(part) as src:
        if src.crs is None or src.width <= 0 or src.height <= 0:
            raise RuntimeError("Downloaded WorldPop raster is invalid")
        src.read(1, window=((0, 1), (0, 1)))
    part.replace(target)
    return target


def bbox_intersects(first: list[float], second: list[float]) -> bool:
    return not (
        first[2] < second[0]
        or first[0] > second[2]
        or first[3] < second[1]
        or first[1] > second[3]
    )


def read_remote_prefix(url: str, size: int = 8) -> bytes:
    with requests.get(
        url,
        headers={"Range": f"bytes=0-{size - 1}"},
        stream=True,
        timeout=60,
    ) as response:
        response.raise_for_status()
        return response.raw.read(size)


def main() -> None:
    config = load_config()
    bbox = config["aoi_bbox_wgs84"]
    catalog = Client.open(config["stac_api"])
    checks: list[dict[str, Any]] = []

    planned_assets = {
        "sentinel2_2018": ["B02", "B03", "B04", "B08", "B11", "B12", "SCL"],
        "sentinel1_2018": ["vv", "vh"],
        "sentinel2_2021": ["B02", "B03", "B04", "B08", "B11", "B12", "SCL"],
        "sentinel1_2021": ["vv", "vh"],
        "sentinel2_2025": ["B02", "B03", "B04", "B08", "B11", "B12", "SCL"],
        "sentinel1_2025": ["vv", "vh"],
        "landsat_2025": ["lwir11", "qa_pixel"],
        "worldcover_2021": ["map"],
        "annual_lulc_2018": ["data"],
        "annual_lulc_2019": ["data"],
        "annual_lulc_2020": ["data"],
        "annual_lulc_2021": ["data"],
        "annual_lulc_2022": ["data"],
        "annual_lulc_2023": ["data"],
    }

    for label, asset_keys in planned_assets.items():
        item = open_pc_item(catalog, config["items"][label])
        for asset_key in asset_keys:
            if asset_key not in item.assets:
                raise RuntimeError(f"Missing asset {asset_key} in {label}")
            sample = read_small_sample(item.assets[asset_key].href, bbox)
            checks.append(
                {
                    "source": label,
                    "item_id": item.id,
                    "asset": asset_key,
                    "status": "usable",
                    **sample,
                }
            )

    worldpop_path = download_worldpop(config)
    checks.append(
        {
            "source": "worldpop_2025",
            "asset": worldpop_path.name,
            "status": "usable",
            "download_bytes": worldpop_path.stat().st_size,
            **read_small_sample(str(worldpop_path), bbox),
        }
    )

    tanager = config["items"]["tanager_2025"]
    tanager_item_url = (
        f"{tanager['collection_url']}/{tanager['id']}/{tanager['id']}.json"
    )
    response = requests.get(tanager_item_url, timeout=60)
    response.raise_for_status()
    tanager_item = response.json()
    required_tanager_assets = ["ortho_visual", "ortho_sr_hdf5", "thumbnail"]
    for asset_key in required_tanager_assets:
        if asset_key not in tanager_item.get("assets", {}):
            raise RuntimeError(f"Missing Tanager asset {asset_key}")
    if not bbox_intersects(bbox, tanager_item["bbox"]):
        raise RuntimeError("The selected Tanager scene does not intersect the AOI")
    hdf5_prefix = read_remote_prefix(
        tanager_item["assets"]["ortho_sr_hdf5"]["href"]
    )
    if hdf5_prefix != b"\x89HDF\r\n\x1a\n":
        raise RuntimeError("The selected Tanager HDF5 asset is not readable")
    checks.append(
        {
            "source": "tanager_2025",
            "item_id": tanager_item["id"],
            "asset": "metadata_and_planned_assets",
            "status": "usable",
            "bbox": tanager_item["bbox"],
            "datetime": tanager_item["properties"]["datetime"],
            "assets": required_tanager_assets,
            "hdf5_header": "valid",
        }
    )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    report = {
        "project": config["project_name"],
        "aoi": config["aoi_name"],
        "bbox_wgs84": bbox,
        "result": "PASS",
        "checks": checks,
    }
    (OUTPUT_DIR / "data_feasibility.json").write_text(
        json.dumps(report, indent=2), encoding="utf-8"
    )

    lines = [
        "# Data feasibility check",
        "",
        f"**Result:** PASS ({len(checks)} checks)",
        "",
        f"**AOI:** {config['aoi_name']} — `{bbox}`",
        "",
        "The exact planned Sentinel-2, Sentinel-1, Landsat, WorldCover, WorldPop, and Tanager items are reachable and intersect the AOI.",
        "",
        "| Source | Asset | Status |",
        "|---|---|---|",
    ]
    for check in checks:
        lines.append(f"| {check['source']} | {check['asset']} | {check['status']} |")
    lines.extend(
        [
            "",
            "This check proves access and coverage only. It does not prove model accuracy or suitability; those are tested by the analysis and validation steps.",
        ]
    )
    (OUTPUT_DIR / "data_feasibility.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )
    print(json.dumps({"result": "PASS", "checks": len(checks)}, indent=2))


if __name__ == "__main__":
    main()
