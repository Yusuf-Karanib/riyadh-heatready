"""Build the small, offline notebook and its public sample input.

The full Earth-observation workflow lives in ``src/run_analysis.py`` and uses
large satellite files that are intentionally not committed.  This builder
creates a compact notebook that lets a reviewer reproduce the final priority
ranking without network access or hidden files.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "outputs" / "priority_zones.csv"
SAMPLE_DIR = ROOT / "data" / "sample_input"
SAMPLE = SAMPLE_DIR / "riyadh_priority_drivers.csv"
NOTEBOOK_DIR = ROOT / "notebooks"
NOTEBOOK = NOTEBOOK_DIR / "02_main_analysis.ipynb"
CELL_NUMBER = 0


def cell_id() -> str:
    global CELL_NUMBER
    CELL_NUMBER += 1
    return f"heatready-{CELL_NUMBER:02d}"


def write_sample_input() -> None:
    """Copy only the inputs to the transparent priority formula."""
    excluded = {"priority_score", "priority_class"}
    with SOURCE.open(newline="", encoding="utf-8") as source:
        reader = csv.DictReader(source)
        fieldnames = [name for name in (reader.fieldnames or []) if name not in excluded]
        rows = [{name: row[name] for name in fieldnames} for row in reader]

    SAMPLE_DIR.mkdir(parents=True, exist_ok=True)
    with SAMPLE.open("w", newline="", encoding="utf-8") as destination:
        writer = csv.DictWriter(destination, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def markdown(source: str) -> dict:
    return {
        "cell_type": "markdown",
        "id": cell_id(),
        "metadata": {},
        "source": source.splitlines(True),
    }


def code(source: str) -> dict:
    return {
        "cell_type": "code",
        "id": cell_id(),
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": source.splitlines(True),
    }


def write_notebook() -> None:
    NOTEBOOK_DIR.mkdir(parents=True, exist_ok=True)
    cells = [
        markdown(
            """# Riyadh HeatReady — reproducible priority ranking\n
**Question:** Which 1 km zones in southeastern Riyadh should a municipal planning and heat-resilience team inspect first?\n
This notebook reproduces the final decision score from a small committed sample. The input columns were derived by the full Earth-observation pipeline from open Sentinel-1, Sentinel-2, Landsat, annual land cover, and WorldPop data. The full download and processing code is in `src/run_analysis.py`; the exact scene IDs and dates are in `config.json`.\n
The sample does **not** replace the raw-satellite workflow. It makes the final ranking easy for judges to run without downloading several gigabytes.\n"""
        ),
        markdown(
            """## Method in plain language\n
Each eligible grid cell already contains four normalized values from 0 to 1:\n
- **heat** — hotter land surfaces score higher;\n
- **population** — more modelled residents score higher;\n
- **growth** — a larger confirmed new-built fraction scores higher;\n
- **lack of green** — less vegetation scores higher.\n
The PoC score is `100 × (40% heat + 30% population + 20% growth + 10% lack of green)`. The top 20% are labelled **High**, the next 30% **Medium**, and the rest **Watch**. These weights are transparent PoC assumptions, not official municipal policy.\n"""
        ),
        code(
            """from pathlib import Path\n
import numpy as np\n
import pandas as pd\n
import matplotlib.pyplot as plt\n
\n
# This works from the repository root or from inside notebooks/.\n
cwd = Path.cwd().resolve()\n
ROOT = cwd if (cwd / \"config.json\").exists() else cwd.parent\n
INPUT = ROOT / \"data\" / \"sample_input\" / \"riyadh_priority_drivers.csv\"\n
RESULTS = ROOT / \"results\"\n
RESULTS.mkdir(exist_ok=True)\n
print(f\"Repository root: {ROOT}\")\n
print(f\"Input: {INPUT.relative_to(ROOT)}\")\n"""
        ),
        code(
            """zones = pd.read_csv(INPUT)\n
required = [\n
    \"grid_id\", \"longitude\", \"latitude\", \"lst_mean_c\",\n
    \"population_estimate\", \"new_built_fraction\", \"ndvi_mean_2025\",\n
    \"heat_component\", \"population_component\", \"growth_component\",\n
    \"lack_green_component\",\n
]\n
missing = sorted(set(required) - set(zones.columns))\n
assert not missing, f\"Missing columns: {missing}\"\n
assert len(zones) == 67, f\"Expected 67 eligible zones, found {len(zones)}\"\n
assert zones[required].notna().all().all(), \"Input contains missing values\"\n
print(f\"Loaded {len(zones)} eligible 1 km zones with no missing required values.\")\n
zones.head(3)\n"""
        ),
        markdown(
            """## Recalculate the score\n
Keeping the formula visible makes the result auditable. A real user should review the weights before operational use.\n"""
        ),
        code(
            """weights = {\n
    \"heat_component\": 0.40,\n
    \"population_component\": 0.30,\n
    \"growth_component\": 0.20,\n
    \"lack_green_component\": 0.10,\n
}\n
zones[\"priority_score\"] = 100 * sum(\n
    zones[column] * weight for column, weight in weights.items()\n
)\n
high_cut = zones[\"priority_score\"].quantile(0.80)\n
medium_cut = zones[\"priority_score\"].quantile(0.50)\n
zones[\"priority_class\"] = np.select(\n
    [zones[\"priority_score\"] >= high_cut, zones[\"priority_score\"] >= medium_cut],\n
    [\"High\", \"Medium\"],\n
    default=\"Watch\",\n
)\n
zones = zones.sort_values([\"priority_score\", \"grid_id\"], ascending=[False, True])\n
assert zones.iloc[0][\"grid_id\"] == \"R05C10\"\n
assert np.isclose(zones.iloc[0][\"priority_score\"], 78.656723, atol=1e-5)\n
print(f\"High threshold: {high_cut:.2f}; medium threshold: {medium_cut:.2f}\")\n
zones[[\"grid_id\", \"priority_score\", \"priority_class\", \"lst_mean_c\", \"population_estimate\", \"new_built_fraction\"]].head(10)\n"""
        ),
        markdown(
            """## Save a judge-readable output\n
The chart shows the ten highest-ranked zones and how the four parts add to each score. A score is a screening priority, not a claim that a specific intervention is already suitable.\n"""
        ),
        code(
            """output_columns = [\n
    \"grid_id\", \"longitude\", \"latitude\", \"priority_score\", \"priority_class\",\n
    \"lst_mean_c\", \"population_estimate\", \"new_built_fraction\", \"ndvi_mean_2025\",\n
]\n
zones[output_columns].to_csv(RESULTS / \"example_priority_zones.csv\", index=False)\n
\n
top = zones.head(10).sort_values(\"priority_score\")\n
parts = [\n
    (\"Heat (40%)\", \"heat_component\", 40, \"#E85D3F\"),\n
    (\"Population (30%)\", \"population_component\", 30, \"#6B5DD3\"),\n
    (\"Growth (20%)\", \"growth_component\", 20, \"#14A38B\"),\n
    (\"Lack of green (10%)\", \"lack_green_component\", 10, \"#D7A72E\"),\n
]\n
fig, ax = plt.subplots(figsize=(11, 6.2))\n
left = np.zeros(len(top))\n
for label, column, maximum, color in parts:\n
    value = top[column].to_numpy() * maximum\n
    ax.barh(top[\"grid_id\"], value, left=left, label=label, color=color)\n
    left += value\n
for y, score in enumerate(top[\"priority_score\"]):\n
    ax.text(score + 0.7, y, f\"{score:.1f}\", va=\"center\", fontsize=9)\n
ax.set_xlim(0, 100)\n
ax.set_xlabel(\"Priority score (0–100)\")\n
ax.set_title(\"Riyadh HeatReady: ten highest screening priorities\", loc=\"left\", weight=\"bold\")\n
ax.legend(ncol=4, loc=\"upper center\", bbox_to_anchor=(0.5, -0.12), frameon=False)\n
ax.grid(axis=\"x\", alpha=0.2)\n
ax.spines[[\"top\", \"right\", \"left\"]].set_visible(False)\n
fig.tight_layout()\n
fig.subplots_adjust(bottom=0.20)\n
figure_path = RESULTS / \"example_priority_output.png\"\n
fig.savefig(figure_path, dpi=180, bbox_inches=\"tight\", facecolor=\"white\")\n
plt.show()\n
print(f\"Saved: {figure_path.relative_to(ROOT)}\")\n"""
        ),
        markdown(
            """## What the result means\n
The highest-ranked cell is **R05C10** with a score of about **78.7**. It combines high land-surface heat, modelled population, confirmed growth, and little vegetation. A planning team would inspect this zone first, compare it with local plans and field conditions, and only then consider an intervention.\n
## Main limitations\n
- Land-surface temperature is not air temperature or personal heat exposure.\n
- WorldPop is a modelled estimate, not a live census or worker count.\n
- Satellite change can confuse bright roofs, compacted soil, and bare desert.\n
- The validation reference is also satellite-derived, so it is agreement rather than field accuracy.\n
- The score weights and thresholds must be reviewed with a real municipal user.\n"""
        ),
    ]
    notebook = {
        "cells": cells,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "version": "3.12"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    NOTEBOOK.write_text(json.dumps(notebook, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> None:
    if not SOURCE.exists():
        raise FileNotFoundError(f"Run the full analysis first; missing {SOURCE}")
    write_sample_input()
    write_notebook()
    print(f"Created {SAMPLE.relative_to(ROOT)}")
    print(f"Created {NOTEBOOK.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
