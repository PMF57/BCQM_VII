# Figures

This folder contains the figure PDFs used by the BCQM VII paper and the scripts that (re)generate them.

## PDFs
- `fig01_bedsheet.pdf` … `fig09_scaling_core_fraction_qclock.pdf`

## Scripts
- `make_figs_01_02_schematics.py` — Fig. 1–2
- `make_figs_03_09_from_csv.py` — Fig. 3–9 (expects `csv/` at repo root)

## Regenerate
From repo root:
```bash
python3 figures/make_figs_01_02_schematics.py
python3 figures/make_figs_03_09_from_csv.py
```

These scripts write updated PDFs back into this folder.
