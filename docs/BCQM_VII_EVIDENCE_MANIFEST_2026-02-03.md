# BCQM VII Evidence Manifest (Stage-2 Pivot) — 2026-02-03

This manifest lists the **canonical run folders**, **analysis scripts**, **CSV artefacts**, and **command lines** used to regenerate the results referenced in the Stage-2 pivot record, the Stage-2 checkpoint notes, and the “Beyond Stability” plan.

## Canonical run folders (simulation outputs)

### Pivot baseline (N={4,8}, n={0.4,0.8})
- `outputs_cloth/ensemble_W100_N4N8_hits1_x10_bins20/`

### Gate-4 trace runs (N={4,8})
- `outputs_cloth/gate4_trace_hits1_x10_bins20_N4N8_n0p8/`
- `outputs_cloth/gate4_trace_hits1_x10_bins20_N4N8_n0p4/`

### A3 scale-ups (n=0.8)
- `outputs_cloth/gateA3_N16_hits1_x10_bins20_n0p8/`
- `outputs_cloth/gateA3_N32_hits1_x10_bins20_n0p8/`

## Analysis scripts (repo paths)
Baseline pivot scripts:
- `bcqm_vii_cloth/analysis/community_cloth_stability.py`
- `bcqm_vii_cloth/analysis/supergraph_edge_stability.py`
- `bcqm_vii_cloth/analysis/louvain_resolution_sweep.py`

Gate-4 localisation:
- `bcqm_vii_cloth/analysis/gate4_thread_localisation.py`  (tagged output filenames)

Effective dimensionality:
- `bcqm_vii_cloth/analysis/d_eff_ball_growth.py`

A2 sensitivity scripts (edge_source core|all):
- `bcqm_vii_cloth/analysis/community_cloth_stability_A2.py`
- `bcqm_vii_cloth/analysis/supergraph_edge_stability_A2.py`

Summaries:
- `bcqm_vii_cloth/analysis/summarise_runs.py`

## Canonical CSV artefacts (recommended locations)

### Pivot base (Gates 1–3)
Run these into `csv/pivot_base/`:
- `community_partition_stability.csv`
- `supergraph_ballgrowth_stability.csv`
- `supergraph_edge_stability.csv`
- `louvain_resolution_sweep_summary.csv`
- `community_supergraph_stability_summary.csv`
- `pivot_gates_1_2_3_summary.csv`

### A2 sensitivity (core/core vs all/all)
Run these into:
- `csv/A2_core_core/`
- `csv/A2_all_all/`

Each folder contains:
- `community_partition_stability.csv`
- `supergraph_edge_stability.csv`
- `supergraph_ballgrowth_stability.csv`

### Gate-4 (tagged)
Run these into `csv/gate4/`:
- `gate4_n0p8_all_all_stats_seedwise.csv`
- `gate4_n0p8_all_all_hopdist_seedwise.csv`
- `gate4_n0p4_all_all_stats_seedwise.csv`
- `gate4_n0p4_all_all_hopdist_seedwise.csv`

A3 N=32 tagged Gate-4 outputs (example tags):
- `gate4_gateA3_N32_n0p8_all_all_*`
- `gate4_gateA3_N32_n0p8_core_core_*`

### A3 scale-up summaries
- `csv/gateA3_N16/gateA3_N16_run_summary.csv`
- `csv/gateA3_N16/gateA3_N16_ballgrowth_pairwise.csv`
- `csv/gateA3_N32/gateA3_N32_run_summary.csv`
- `csv/gateA3_N32/gateA3_N32_ballgrowth_pairwise.csv`

### Test 2.4 d_eff outputs
- `csv/gateA3_N16/gateA3_N16_cloth_d_eff_runs.csv`
- `csv/gateA3_N16/gateA3_N16_cloth_d_eff_summary.csv`
- `csv/gateA3_N32/gateA3_N32_cloth_d_eff_runs.csv`
- `csv/gateA3_N32/gateA3_N32_cloth_d_eff_summary.csv`
- loose/ultra-loose cloth attempts (N=32): `gateA3_N32_cloth_loose_*`, `gateA3_N32_cloth_ultra_loose_*`
- super-graph d_eff: `pivot_supergraph_deff_d_eff_runs.csv`, `pivot_supergraph_deff_d_eff_summary.csv`

## Command lines (minimal regeneration set)

### Gates 1 & 3 baseline
```bash
python3 bcqm_vii_cloth/analysis/community_cloth_stability.py   --run_dir outputs_cloth/ensemble_W100_N4N8_hits1_x10_bins20   --out_dir csv/pivot_base --method louvain
```

### Gate 2 baseline
```bash
python3 bcqm_vii_cloth/analysis/supergraph_edge_stability.py   --run_dir outputs_cloth/ensemble_W100_N4N8_hits1_x10_bins20   --out_dir csv/pivot_base --method louvain
```

### Gate 3 tightening (resolution sweep)
```bash
python3 bcqm_vii_cloth/analysis/louvain_resolution_sweep.py   --run_dir outputs_cloth/ensemble_W100_N4N8_hits1_x10_bins20   --out_dir csv/pivot_base --resolutions 0.5,1.0,1.5,2.0
```

### A2 (edge_source sensitivity)
```bash
python3 bcqm_vii_cloth/analysis/community_cloth_stability_A2.py   --run_dir outputs_cloth/ensemble_W100_N4N8_hits1_x10_bins20   --out_dir csv/A2_core_core --edge_source core
python3 bcqm_vii_cloth/analysis/community_cloth_stability_A2.py   --run_dir outputs_cloth/ensemble_W100_N4N8_hits1_x10_bins20   --out_dir csv/A2_all_all --edge_source all
```
(and similarly for `supergraph_edge_stability_A2.py`).

### Test 2.4 d_eff (cloth)
```bash
python3 bcqm_vii_cloth/analysis/d_eff_ball_growth.py   --run_dir outputs_cloth/gateA3_N32_hits1_x10_bins20_n0p8   --object cloth --out_dir csv/gateA3_N32 --tag gateA3_N32_cloth
```

### Test 2.4 d_eff (super-graph)
```bash
python3 bcqm_vii_cloth/analysis/d_eff_ball_growth.py   --run_dir outputs_cloth/ensemble_W100_N4N8_hits1_x10_bins20   --object supergraph --partition_source all --supergraph_source all --resolution 1.0   --out_dir csv/pivot_base --tag pivot_supergraph_deff
```

### Gate-4 localisation (tagged)
```bash
python3 bcqm_vii_cloth/analysis/gate4_thread_localisation.py   --run_dir outputs_cloth/gate4_trace_hits1_x10_bins20_N4N8_n0p8   --out_dir csv/gate4 --partition_source all --supergraph_source all --tag n0p8_all_all
```

---

If this file is placed in the repo as `docs/EVIDENCE_MANIFEST.md`, it becomes the definitive index for reproduction and citation.
