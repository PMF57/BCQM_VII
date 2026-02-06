#!/usr/bin/env python3
"""
BCQM VII figure generation (schematics): Fig. 1 (bed-sheet) and Fig. 2 (Stage–2 pipeline).

Outputs:
  figures/fig01_bedsheet.pdf
  figures/fig02_stage2_pipeline.pdf
"""

from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
FIG_DIR = (ROOT / "figures").resolve()
FIG_DIR.mkdir(parents=True, exist_ok=True)

def finalize(fig, title: str, right: float = 1.0, top: float = 0.90):
    # Title above chart area (use suptitle) and reserve layout space
    fig.suptitle(title, y=0.98)
    fig.tight_layout(rect=[0, 0, right, top])

def save_fig(fig, name: str):
    out = FIG_DIR / name
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    print(f"[ok] wrote {out}")

def fig01_bedsheet():
    fig = plt.figure(figsize=(8.5, 5.5))
    ax = fig.add_subplot(111)
    ax.set_axis_off()

    left = FancyBboxPatch((0.04, 0.16), 0.43, 0.72, boxstyle="round,pad=0.02,rounding_size=0.02",
                          transform=ax.transAxes, linewidth=1.0, facecolor="none")
    right = FancyBboxPatch((0.53, 0.16), 0.43, 0.72, boxstyle="round,pad=0.02,rounding_size=0.02",
                           transform=ax.transAxes, linewidth=1.0, facecolor="none")
    ax.add_patch(left); ax.add_patch(right)

    ax.text(0.255, 0.86, "Molecular noise\n(edge-level fluctuations)", ha="center", va="center",
            transform=ax.transAxes, fontsize=12)
    ax.text(0.745, 0.86, "Fabric deformation\n(persistent mesoscopic geometry)", ha="center", va="center",
            transform=ax.transAxes, fontsize=12)

    rng = np.random.default_rng(0)
    for _ in range(26):
        x0, y0 = 0.07 + 0.37*rng.random(), 0.22 + 0.58*rng.random()
        x1, y1 = 0.07 + 0.37*rng.random(), 0.22 + 0.58*rng.random()
        ax.plot([x0, x1], [y0, y1], transform=ax.transAxes, linewidth=0.8)

    nodes = [(0.60, 0.30), (0.67, 0.55), (0.83, 0.35), (0.90, 0.62), (0.74, 0.75), (0.58, 0.72)]
    for (x,y) in nodes:
        ax.plot(x, y, marker="o", markersize=8, transform=ax.transAxes)

    edges = [(0,1),(1,2),(1,4),(4,3),(4,2),(5,4),(5,1),(2,3)]
    for i,j in edges:
        x0,y0 = nodes[i]; x1,y1 = nodes[j]
        ax.plot([x0,x1],[y0,y1], transform=ax.transAxes, linewidth=1.4)

    arr = FancyArrowPatch((0.47,0.52),(0.53,0.52), transform=ax.transAxes,
                          arrowstyle="-|>", mutation_scale=16, linewidth=1.2)
    ax.add_patch(arr)
    ax.text(0.50, 0.58, "coarse-grain\n(communities)", ha="center", va="center",
            transform=ax.transAxes, fontsize=11)
    finalize(fig, "Bed-sheet picture: microstructure varies; coarse geometry persists")
    return fig

def fig02_pipeline():
    fig = plt.figure(figsize=(8.5, 5.5))
    ax = fig.add_subplot(111)
    ax.set_axis_off()

    # Vertical pipeline to avoid horizontal squashing and give room for text
    boxes = [
        "Run outputs\n(outputs_cloth/...)",
        "Cloth extraction\n(hits1; core/halo)",
        "Community partition\n(Louvain; γ)",
        "Community super-graph\n(nodes=communities)",
        "Diagnostics\n(stability, d_eff, curvature,\noptional d_s, localisation)",
    ]

    x = 0.50
    w = 0.68
    h = 0.12
    y_centres = [0.80, 0.64, 0.48, 0.32, 0.16]

    for label, yc in zip(boxes, y_centres):
        y = yc - h/2
        patch = FancyBboxPatch(
            (x - w/2, y), w, h,
            boxstyle="round,pad=0.02,rounding_size=0.02",
            transform=ax.transAxes, linewidth=1.0, facecolor="none"
        )
        ax.add_patch(patch)
        ax.text(x, yc, label, ha="center", va="center", transform=ax.transAxes, fontsize=11)

    # Down arrows
    for y0, y1 in zip(y_centres[:-1], y_centres[1:]):
        arr = FancyArrowPatch(
            (x, y0 - h/2), (x, y1 + h/2),
            transform=ax.transAxes, arrowstyle="-|>", mutation_scale=16, linewidth=1.1
        )
        ax.add_patch(arr)

    finalize(fig, "Stage–2 pipeline: from runs to persistent cloth diagnostics")
    return fig

if __name__ == "__main__":
    save_fig(fig01_bedsheet(), "fig01_bedsheet.pdf")
    save_fig(fig02_pipeline(), "fig02_stage2_pipeline.pdf")
