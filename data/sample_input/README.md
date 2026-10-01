# Sample input

`riyadh_priority_drivers.csv` is the small, public input used by
`notebooks/02_main_analysis.ipynb`.

It contains 67 eligible 1 km grid cells. The full satellite pipeline calculated
the heat, population, confirmed-growth, and lack-of-green components. The sample
intentionally leaves out the final priority score and class so the notebook can
recalculate them.

This is processed example data, not raw satellite imagery. The complete pipeline,
exact item IDs, dates, and download instructions are in `src/run_analysis.py` and
`config.json`. Large raw scenes are excluded from GitHub to keep the repository
small and to avoid redistributing provider files.

No credentials, signed URLs, or restricted imagery are included.
