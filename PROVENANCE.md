# Provenance (BCQM VII)

This repository (BCQM VII) begins from a proven, byte-identical baseline derived from the published BCQM VI Stage-1 reference implementation.

## Upstream source (BCQM VI)
- GitHub: https://github.com/PMF57/BCQM_VI  
- Code archive (Zenodo, release DOI): 10.5281/zenodo.18403109  
- Release tag: v0.1.0

## Downstream baseline (BCQM VII)
- GitHub: https://github.com/PMF57/BCQM_VII  
- Baseline commit: the first commit in this repo contains the proven baseline described below.

## Derivation method
BCQM VII was created by copying the BCQM VI codebase into a new package folder named `bcqm_vii_cloth`, and trimming/curating configuration files for Stage-2 “cloth” development. The repo contains:

- `bcqm_vii_cloth/` — code package copied from BCQM VI (v0.1.0)
- `configs/` — curated runnable YAML configs for current sessions
- `pyproject.toml` — dependencies for the development environment
- `TRIM_MANIFEST.json` — record of what was kept/removed during trimming
- `docs/` — internal notes and provenance artefacts

## Cryptographic lineage proof (VI → VII)
A SHA256 comparison was performed between:
- a local extraction of the BCQM VI Zenodo archive, and
- the BCQM VII code folder in this repository,

using a fixed list of core runtime and pipeline files. Result:

- MATCH: 14  
- DIFF: 0  
- MISS_VI: 0  
- MISS_VII: 0  

This demonstrates byte-identical identity for the tested files and constitutes the provenance proof for the Stage-2 starting point.

The proof artefacts are stored under:
- `docs/provenance/prove_vi_lineage.sh`
- `docs/provenance/vi_vs_vii_hash_report_20260129_122213.txt` (timestamped)

## Going forward
All Stage-2 development (new cloth construction, metrics, configs, pipelines) is tracked directly in this BCQM VII repository from the proven baseline.