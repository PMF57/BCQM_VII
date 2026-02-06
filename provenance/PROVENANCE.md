# Provenance (BCQM VII)

This repository (BCQM VII) is derived from the BCQM VI Stage-1 reference implementation.

## Upstream source (BCQM VI)
- GitHub: https://github.com/PMF57/BCQM_VI
- Archived release (code DOI): 10.5281/zenodo.18403109
- Release tag: v0.1.0

## Derivation method
BCQM VII was created by copying the BCQM VI codebase into a new package folder named `bcqm_vii_cloth`, and pruning/curating configuration files for Stage-2 “cloth” development. The intention is to keep Stage-2 development reproducible while maintaining an auditable lineage to the published Stage-1 code.

The following items were carried forward:
- `bcqm_vii_cloth/` (code package; copied from BCQM VI)
- `configs/` (curated set of runnable YAML configs for current sessions)
- `pyproject.toml` (dependencies pinned for the current development environment)
- `TRIM_MANIFEST.json` (record of what was kept/removed during trimming)

A `docs/` folder is maintained for internal notes and provenance artefacts.

## Cryptographic lineage proof (VI → VII)
A SHA256 comparison was performed between:
- the BCQM VI code extracted locally from the Zenodo archive, and
- the BCQM VII code folder in this repository,

using a fixed list of core runtime + pipeline files. The comparison result:

- MATCH: 14
- DIFF: 0
- MISS_VI: 0
- MISS_VII: 0

This demonstrates byte-identical identity for the tested files.

The script and the generated report are stored under:
- `docs/provenance/prove_vi_lineage.sh`
- (optional) `docs/provenance/vi_vs_vii_hash_report_20260129_122213.txt`

## Notes
- The pruning/curation of configs is recorded in `TRIM_MANIFEST.json`.
- Stage-2 development will introduce new modules and configs; these are tracked directly in this repository going forward.