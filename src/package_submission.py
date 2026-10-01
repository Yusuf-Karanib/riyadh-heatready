"""Create a small internal submission candidate without raw or cached data."""

from __future__ import annotations

import json
import hashlib
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_DIR = ROOT / "submission_candidate"
ZIP_PATH = PACKAGE_DIR / "riyadh-heatready-submission-candidate.zip"
PACKAGE_MANIFEST_NAME = "PACKAGE-MANIFEST.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def files_to_include() -> list[Path]:
    fixed = [
        ROOT / "README.md",
        ROOT / "config.json",
        ROOT / "requirements.txt",
        ROOT / "build_all.ps1",
    ]
    sources = sorted((ROOT / "src").glob("*.py"))
    docs = sorted((ROOT / "docs").glob("*.md"))
    output_names = [
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
        "data_feasibility.md",
        "verification_report.md",
        "manifest.json",
    ]
    outputs = [ROOT / "outputs" / name for name in output_names]
    return fixed + sources + docs + outputs


def main() -> None:
    PACKAGE_DIR.mkdir(parents=True, exist_ok=True)
    files = files_to_include()
    missing = [str(path) for path in files if not path.exists()]
    if missing:
        raise RuntimeError(f"Cannot package; missing files: {missing}")
    manifest = {
        "scope": "Every archive file except PACKAGE-MANIFEST.json itself",
        "files": [
            {
                "file": path.relative_to(ROOT).as_posix(),
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
            }
            for path in files
        ],
    }
    with zipfile.ZipFile(ZIP_PATH, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in files:
            archive.write(path, path.relative_to(ROOT).as_posix())
        archive.writestr(PACKAGE_MANIFEST_NAME, json.dumps(manifest, indent=2))
    with zipfile.ZipFile(ZIP_PATH, "r") as archive:
        broken = archive.testzip()
        if broken is not None:
            raise RuntimeError(f"Submission archive failed integrity check: {broken}")
        for entry in manifest["files"]:
            archived_bytes = archive.read(entry["file"])
            archived_hash = hashlib.sha256(archived_bytes).hexdigest()
            if len(archived_bytes) != entry["bytes"] or archived_hash != entry["sha256"]:
                raise RuntimeError(
                    f"Submission archive does not match its manifest: {entry['file']}"
                )
    report = {
        "status": "created",
        "path": str(ZIP_PATH),
        "bytes": ZIP_PATH.stat().st_size,
        "files": len(files) + 1,
        "sha256": sha256(ZIP_PATH),
        "integrity": "PASS",
        "manifest_verification": "PASS",
        "warning": "Internal candidate only. Adapt to the official portal requirements before submission.",
    }
    (PACKAGE_DIR / "package_report.json").write_text(
        json.dumps(report, indent=2), encoding="utf-8"
    )
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
