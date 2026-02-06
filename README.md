# BCQM VII — Code + artefacts (Stage–2 “cloth”)

This repository accompanies **BCQM VII** (Stage–2 cloth programme: persistent coarse spatial cloth via communities and a community super-graph), and contains:

- the simulation/analysis package (`bcqm_vii_cloth/`)
- Stage–2 run configs (`configs_stage2/`)
- consolidated analysis outputs (`csv/`)
- figure PDFs and figure-generation scripts (`figures/`)
- documentation and validation plans (`docs/`)
- provenance notes (`provenance/`)
- output_cloths.zip

Zenodo DOIs (paper):
```text
Concept DOI : 10.5281/zenodo.18497216
Version 1 DOI: 10.5281/zenodo.18497217
```

> Note: The paper is reproducible from the shipped CSV artefacts and scripts, and runs can be regenerated using the configs in `configs_stage2/`.

---

## Quickstart

### Requirements
- Python **>= 3.13** (as specified in `pyproject.toml`)
- Recommended: create a virtual environment.

### Install
From repo root:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -e .
```

---

## Reproducing the paper figures

Two figure generator scripts are provided in `figures/`:

- `make_figs_01_02_schematics.py` — schematic figures (Fig. 1–2)
- `make_figs_03_09_from_csv.py` — data-driven figures (Fig. 3–9) from `csv/`

From repo root:
```bash
python3 figures/make_figs_01_02_schematics.py
python3 figures/make_figs_03_09_from_csv.py
```

Outputs are written to `figures/*.pdf`.

---

## Re-running simulations (optional; raw outputs not bundled)

Stage–2 run configs live in `configs_stage2/`. To re-run a scan:
```bash
python3 -m bcqm_vii_cloth.cli scan --config configs_stage2/<CONFIG>.yml
```

This will generate a new run folder under `outputs_cloth/` (not included in this repo ZIP). You can then re-run analysis scripts under `bcqm_vii_cloth/analysis/` to regenerate CSV tables under `csv/`.

---

## Repository map

- `bcqm_vii_cloth/` — simulation + analysis code
- `configs_stage2/` — configs used for Stage–2 validation (baseline + A3 scale-ups)
- `configs/` — shared / auxiliary configs
- `csv/` — consolidated artefacts used by the paper and figures
- `docs/` — evidence manifest, validation plan, lab notes
- `figures/` — final PDFs + figure generator scripts
- `provenance/` — provenance notes, trimming notes
- output_cloths.zip

See `docs/EVIDENCE_MANIFEST.md` for the authoritative artefact index and rebuild recipes.

---
