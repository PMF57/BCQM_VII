#!/usr/bin/env python3
"""
BCQM VII figure generation from CSV artefacts (Fig. 3--9).

This script expects the CSV folder produced by the Stage--2 analysis, with paths like:
  csv/louvain_resolution_sweep_summary.csv
  csv/pivot_gates_1_2_3_summary.csv
  csv/pivot_base/pivot_supergraph_deff_d_eff_runs.csv
  csv/curvature/curvature_pivot_*_supergraph_curvature_runs.csv
  csv/spectral_dim/pivot_core_exact_spectral_dim_curves.csv
  csv/gate4/gate4_n0p4_all_all_hopdist_seedwise.csv
  csv/gate4/gate4_n0p8_all_all_hopdist_seedwise.csv
  csv/gateA3_N16/gateA3_N16_run_summary.csv
  csv/gateA3_N32/gateA3_N32_run_summary.csv

Outputs (PDF):
  figures/fig03_partition_stability.pdf
  figures/fig04_supergraph_summary_stability.pdf
  figures/fig05_ballgrowth_deff.pdf
  figures/fig06_forman_curvature_summary.pdf
  figures/fig07_spectral_dimension_curves.pdf
  figures/fig08_localisation_hopdist_stacked.pdf
  figures/fig09_scaling_core_fraction_qclock.pdf
"""

from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
CSV_DIR = (ROOT / "csv").resolve()
FIG_DIR = (ROOT / "figures").resolve()
FIG_DIR.mkdir(parents=True, exist_ok=True)

def finalize(fig, title: str, right: float = 1.0, top: float = 0.90):
    # Title above chart area (use suptitle) and reserve layout space; adjust right margin for legends if needed
    fig.suptitle(title, y=0.98)
    fig.tight_layout(rect=[0, 0, right, top])

def apply_bcqm_axes_style(ax):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.minorticks_on()
    ax.grid(True, which="major", linestyle="--", linewidth=0.8)

def save_pdf(fig, filename):
    out = FIG_DIR / filename
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    print(f"[ok] wrote {out}")

def quad_label(N, n):
    return f"N={int(N)}, n={float(n):.1f}"

quad_order = [(4,0.4),(4,0.8),(8,0.4),(8,0.8)]
markers = ["o","s","^","D"]

def fig03_partition_stability():
    sweep = pd.read_csv(CSV_DIR / "louvain_resolution_sweep_summary.csv")
    fig = plt.figure(figsize=(8.5,5.5))
    ax = fig.add_subplot(111)
    for (N,n), m in zip(quad_order, markers):
        sub = sweep[(sweep["N"]==N) & (np.isclose(sweep["n"], n))].sort_values("resolution")
        ax.errorbar(sub["resolution"], sub["NMI_mean"], yerr=sub["NMI_std"],
                    marker=m, linewidth=1.5, capsize=3, label=quad_label(N,n))
    ax.set_xlabel("Louvain resolution γ")
    ax.set_ylabel("Partition similarity (NMI)")
    ax.set_ylim(0.0, 1.0)
    apply_bcqm_axes_style(ax)
    ax.legend(frameon=False, ncol=2, fontsize=10)
    finalize(fig, "Partition stability across seeds vs Louvain resolution", right=1.0, top=0.9)

    save_pdf(fig, "fig03_partition_stability.pdf")

def fig04_supergraph_summary_stability():
    pivot = pd.read_csv(CSV_DIR / "pivot_gates_1_2_3_summary.csv")
    pivot["order"] = pivot.apply(lambda r: quad_order.index((int(r["N"]), float(r["n"]))), axis=1)
    pivot = pivot.sort_values("order")
    x = np.arange(len(pivot))
    labels = [quad_label(r.N, r.n) for r in pivot.itertuples(index=False)]
    fig = plt.figure(figsize=(8.5,5.5))
    ax1 = fig.add_subplot(111)
    ax2 = ax1.twinx()
    ax1.errorbar(x, pivot["K_mean"], yerr=pivot["K_std"], marker="o", linewidth=1.5, capsize=3, label="K (communities)")
    ax2.errorbar(x, pivot["super_J_mean"], yerr=pivot["super_J_std"], marker="s", linewidth=1.5, capsize=3, label="Edge Jaccard (super)")
    ax2.errorbar(x, pivot["super_corr_mean"], yerr=pivot["super_corr_std"], marker="^", linewidth=1.5, capsize=3, label="Weight corr (super)")
    ax1.set_xticks(x)
    ax1.set_xticklabels(labels, rotation=20, ha="right")
    ax1.set_ylabel("K (mean ± sd)")
    ax2.set_ylabel("Stability (mean ± sd)")
    apply_bcqm_axes_style(ax1)
    ax2.spines["top"].set_visible(False)
    h1,l1 = ax1.get_legend_handles_labels()
    h2,l2 = ax2.get_legend_handles_labels()
    ax1.legend(h1+h2, l1+l2, frameon=False, fontsize=10, loc="upper right")
    finalize(fig, "Super-graph summary and stability across seeds", right=1.0, top=0.9)

    save_pdf(fig, "fig04_supergraph_summary_stability.pdf")

def fig05_ballgrowth_deff():
    deff = pd.read_csv(CSV_DIR / "pivot_base" / "pivot_supergraph_deff_d_eff_runs.csv")
    fig = plt.figure(figsize=(8.5,5.5))
    ax = fig.add_subplot(111)
    rng = np.random.default_rng(0)
    for i,(N,n) in enumerate(quad_order):
        sub = deff[(deff["N"]==N) & (np.isclose(deff["n"], n))]
        xi = np.full(len(sub), i) + rng.uniform(-0.10,0.10,size=len(sub))
        ax.plot(xi, sub["d_eff"].values, marker="o", linestyle="None")
    means = []; sds = []
    for (N,n) in quad_order:
        sub = deff[(deff["N"]==N) & (np.isclose(deff["n"], n))]
        means.append(sub["d_eff"].mean())
        sds.append(sub["d_eff"].std(ddof=1))
    ax.errorbar(np.arange(4), means, yerr=sds, marker="s", linewidth=1.5, capsize=3, label="mean ± sd")
    ax.set_xticks(np.arange(4))
    ax.set_xticklabels([quad_label(N,n) for N,n in quad_order], rotation=20, ha="right")
    ax.set_ylabel("d_eff (ball-growth fit exponent)")
    apply_bcqm_axes_style(ax)
    ax.legend(frameon=False, fontsize=10, loc="upper right")
    finalize(fig, "Ball-growth effective exponent on the community super-graph", right=1.0, top=0.9)

    save_pdf(fig, "fig05_ballgrowth_deff.pdf")

def fig06_forman_curvature_summary():
    all_df = pd.read_csv(CSV_DIR / "curvature" / "curvature_pivot_all_supergraph_curvature_runs.csv")
    core_df = pd.read_csv(CSV_DIR / "curvature" / "curvature_pivot_core_supergraph_curvature_runs.csv")
    fig = plt.figure(figsize=(8.5,5.5))
    ax = fig.add_subplot(111)
    rng = np.random.default_rng(0)
    offset = 0.14
    for i,(N,n) in enumerate(quad_order):
        a = all_df[(all_df["N"]==N) & (np.isclose(all_df["n"], n))]
        c = core_df[(core_df["N"]==N) & (np.isclose(core_df["n"], n))]
        xa = np.full(len(a), i - offset) + rng.uniform(-0.03,0.03,size=len(a))
        xc = np.full(len(c), i + offset) + rng.uniform(-0.03,0.03,size=len(c))
        ax.plot(xa, a["F_mean"].values, marker="o", linestyle="None", label="all edges" if i==0 else None)
        ax.plot(xc, c["F_mean"].values, marker="^", linestyle="None", label="core edges" if i==0 else None)
        ax.errorbar(i - offset, a["F_mean"].mean(), yerr=a["F_mean"].std(ddof=1), marker="s", capsize=3, linewidth=1.2)
        ax.errorbar(i + offset, c["F_mean"].mean(), yerr=c["F_mean"].std(ddof=1), marker="s", capsize=3, linewidth=1.2)
    ax.set_xticks(np.arange(4))
    ax.set_xticklabels([quad_label(N,n) for N,n in quad_order], rotation=20, ha="right")
    ax.set_ylabel("Edge-mean Forman curvature (F_mean)")
    apply_bcqm_axes_style(ax)
    ax.legend(frameon=False, fontsize=10, loc="lower left")
    finalize(fig, "Curvature proxy on the community super-graph (all vs core)", right=1.0, top=0.9)

    save_pdf(fig, "fig06_forman_curvature_summary.pdf")

def fig07_spectral_dimension_curves():
    sd = pd.read_csv(CSV_DIR / "spectral_dim" / "pivot_core_exact_spectral_dim_curves.csv")
    sd = sd[(sd["mode"]=="exact") & (sd["t"]>=3) & (sd["t"]<=100)].copy()
    sd = sd[np.isfinite(sd["d_s"])].copy()
    sd = sd[(sd["d_s"]>-5) & (sd["d_s"]<5)]
    fig = plt.figure(figsize=(8.5,5.5))
    ax = fig.add_subplot(111)
    for (N,n) in quad_order:
        sub = sd[(sd["N"]==N) & (np.isclose(sd["n"], n))]
        if sub.empty:
            continue
        grp = sub.groupby("t")["d_s"]
        t = grp.mean().index.values
        mean = grp.mean().values
        std = grp.std(ddof=1).values
        ax.plot(t, mean, linewidth=1.6, label=quad_label(N,n))
        ax.fill_between(t, mean-std, mean+std, alpha=0.20)
    ax.axhline(0.0, linewidth=1.0)
    ax.set_xlabel("t (walk steps)")
    ax.set_ylabel("d_s(t)")
    apply_bcqm_axes_style(ax)
    ax.legend(frameon=False, fontsize=10, ncol=2)
    finalize(fig, "Spectral-dimension curves on the community super-graph (exact mode)", right=1.0, top=0.9)

    save_pdf(fig, "fig07_spectral_dimension_curves.pdf")

def fig08_localisation_hopdist():
    hop04 = pd.read_csv(CSV_DIR / "gate4" / "gate4_n0p4_all_all_hopdist_seedwise.csv")
    hop08 = pd.read_csv(CSV_DIR / "gate4" / "gate4_n0p8_all_all_hopdist_seedwise.csv")
    hop = pd.concat([hop04, hop08], ignore_index=True)
    cols = ["frac_d0","frac_d1","frac_d2","frac_dge3"]
    agg = hop.groupby(["N","n"])[cols].mean().reset_index()
    agg["order"] = agg.apply(lambda r: quad_order.index((int(r["N"]), float(r["n"]))), axis=1)
    agg = agg.sort_values("order")
    x = np.arange(len(agg))
    labels = [quad_label(r.N, r.n) for r in agg.itertuples(index=False)]
    fig = plt.figure(figsize=(8.5,5.5))
    ax = fig.add_subplot(111)
    bottom = np.zeros(len(agg))
    stack_labels = ["d=0", "d=1", "d=2", "d≥3"]
    for c,lab in zip(cols, stack_labels):
        ax.bar(x, agg[c].values, bottom=bottom, label=lab)
        bottom = bottom + agg[c].values
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=20, ha="right")
    ax.set_ylabel("Fraction of mapped transitions")
    ax.set_ylim(0, 1.0)
    apply_bcqm_axes_style(ax)
    ax.legend(frameon=False, fontsize=10, loc="center left", bbox_to_anchor=(1.02, 0.5))
    finalize(fig, "Thread localisation proxy: hop-distance distribution on the super-graph", right=0.82, top=0.9)

    save_pdf(fig, "fig08_localisation_hopdist_stacked.pdf")

def fig09_scaling_core_fraction_qclock():
    rs16 = pd.read_csv(CSV_DIR / "gateA3_N16" / "gateA3_N16_run_summary.csv")
    rs32 = pd.read_csv(CSV_DIR / "gateA3_N32" / "gateA3_N32_run_summary.csv")
    rs = pd.concat([rs16, rs32], ignore_index=True)
    rs["N_total_events"] = rs["core_events_count"] + rs["halo_events_count"]
    rs["phi_core"] = rs["core_events_count"] / rs["N_total_events"]
    summary = rs.groupby("N").agg(
        phi_mean=("phi_core","mean"),
        phi_std=("phi_core", lambda s: s.std(ddof=1)),
        Q_mean=("Q_clock","mean"),
        Q_std=("Q_clock", lambda s: s.std(ddof=1)),
    ).reset_index().sort_values("N")
    fig = plt.figure(figsize=(8.5,5.5))
    ax1 = fig.add_subplot(111)
    ax2 = ax1.twinx()
    ax1.errorbar(summary["N"], summary["phi_mean"], yerr=summary["phi_std"], marker="o", linewidth=1.5, capsize=3, label="Core fraction Φ")
    ax2.errorbar(summary["N"], summary["Q_mean"], yerr=summary["Q_std"], marker="s", linewidth=1.5, capsize=3, label="Q_clock")
    ax1.set_xlabel("Ensemble size N")
    ax1.set_ylabel("Core fraction Φ (mean ± sd)")
    ax1.set_ylim(0.0, 1.02)
    ax2.set_ylabel("Clock quality Q_clock (mean ± sd)")
    apply_bcqm_axes_style(ax1)
    ax2.spines["top"].set_visible(False)
    h1,l1 = ax1.get_legend_handles_labels()
    h2,l2 = ax2.get_legend_handles_labels()
    ax1.legend(h1+h2, l1+l2, frameon=False, fontsize=10, loc="upper center", bbox_to_anchor=(0.5, 0.98), ncol=2)
    finalize(fig, "Scaling with N: core/halo separation and clock stability (n=0.8)", right=1.0, top=0.9)

    save_pdf(fig, "fig09_scaling_core_fraction_qclock.pdf")

if __name__ == "__main__":
    fig03_partition_stability()
    fig04_supergraph_summary_stability()
    fig05_ballgrowth_deff()
    fig06_forman_curvature_summary()
    fig07_spectral_dimension_curves()
    fig08_localisation_hopdist()
    fig09_scaling_core_fraction_qclock()
