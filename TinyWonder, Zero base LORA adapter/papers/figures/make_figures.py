#!/usr/bin/env python3
"""Publication-grade, receipt-backed vector figures for the isolated revision."""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

HERE = Path(__file__).resolve().parent
DATA = json.loads((HERE / "data.json").read_text(encoding="utf-8"))

NAVY = "#17324D"
BLUE = "#2A6FBB"
TEAL = "#148A8A"
GREEN = "#2E8B57"
RED = "#B23A48"
GOLD = "#C58B1D"
INK = "#1F2933"
MUTED = "#52606D"
PALETTE = {"full": RED, "gamma_0_1": BLUE, "inverse_depth": GREEN}
LABELS = {"full": r"$\gamma=1$", "gamma_0_1": r"$\gamma=0.1$", "inverse_depth": r"$\gamma(k)=1/k$"}

rcParams.update({
    "font.family": "serif",
    "font.serif": ["DejaVu Serif"],
    "font.size": 9,
    "axes.titlesize": 11,
    "axes.labelsize": 9,
    "legend.fontsize": 8,
    "figure.dpi": 150,
    "savefig.dpi": 300,
    "axes.edgecolor": "#52606D",
    "axes.linewidth": 0.7,
    "xtick.color": INK,
    "ytick.color": INK,
    "text.color": INK,
})


def save(fig, name: str):
    fig.savefig(HERE / f"{name}.svg", bbox_inches="tight", metadata={"Creator": "Tiny Wonder publication revision"})
    fig.savefig(HERE / f"{name}.pdf", bbox_inches="tight", metadata={"Creator": "Tiny Wonder publication revision"})
    plt.close(fig)


def paper1_lanes():
    fig, ax = plt.subplots(figsize=(7.0, 3.7), constrained_layout=True)
    ax.set_xlim(0, 10); ax.set_ylim(0, 5.2); ax.axis("off")
    ax.text(5, 4.85, "Explicit execution-lane boundary", ha="center", va="center", fontsize=14, weight="bold", color=NAVY)
    def box(x, y, w, h, text, fill, edge=NAVY):
        p = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.025,rounding_size=0.08", linewidth=1.2, edgecolor=edge, facecolor=fill)
        ax.add_patch(p); ax.text(x+w/2, y+h/2, text, ha="center", va="center", fontsize=9, wrap=True)
    def arrow(x1, y1, x2, y2, color=MUTED, style="-|>"):
        ax.add_patch(FancyArrowPatch((x1,y1),(x2,y2), arrowstyle=style, mutation_scale=12, linewidth=1.1, color=color))
    box(.45, 2.55, 2.25, .9, "Self-describing\nbundle", "#E7F0F8")
    box(3.35, 3.2, 2.4, 1.0, "Zero-base lane\nbase = None", "#E8F5E9", GREEN)
    box(3.35, 1.45, 2.4, 1.0, "Attached lane\nexplicit base ABI", "#FFF4CC", GOLD)
    box(6.6, 3.2, 2.7, 1.0, "Standalone specialist\nvalidated and routed", "#E8F5E9", GREEN)
    box(6.6, 1.45, 2.7, 1.0, "Base-dependent execution\nonly under declared ABI", "#FFF4CC", GOLD)
    box(3.05, .12, 3.0, .7, "Declared base in zero-base input → typed refusal", "#FDE8E7", RED)
    arrow(2.7, 3.0, 3.35, 3.7); arrow(2.7, 3.0, 3.35, 1.95)
    arrow(5.75, 3.7, 6.6, 3.7, GREEN); arrow(5.75, 1.95, 6.6, 1.95, GOLD)
    arrow(4.55, 3.2, 4.55, .82, RED, "-[")
    ax.text(5, .0, "Receipt-backed scope: lane validation, refusal semantics, and release provenance", ha="center", va="bottom", fontsize=8, color=MUTED)
    save(fig, "paper1_figure2_lane_boundary")


def paper1_architecture_fallback():
    fig, ax = plt.subplots(figsize=(10.5, 5.8), constrained_layout=True)
    ax.set_xlim(0, 12); ax.set_ylim(0, 7); ax.axis("off")
    ax.text(6, 6.72, "Independent adapter host: validation, coordination, and reversible release", ha="center", fontsize=14, weight="bold", color=NAVY)
    def box(x,y,w,h,text,fill="#E7F0F8",edge=NAVY,fs=8.7):
        p=FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0.025,rounding_size=0.06",linewidth=1.0,edgecolor=edge,facecolor=fill)
        ax.add_patch(p); ax.text(x+w/2,y+h/2,text,ha="center",va="center",fontsize=fs,wrap=True)
    def ar(x1,y1,x2,y2,c=MUTED):
        ax.add_patch(FancyArrowPatch((x1,y1),(x2,y2),arrowstyle="-|>",mutation_scale=11,linewidth=1.0,color=c))
    xs=[.25,2.65,5.05,7.45,9.85]
    labels=["Bundle\nABI · vocab · digest","Contract\nvalidation","Versioned\nfront door","Capability\nregistry","Outcome\nsuccess/abstain"]
    for x,t in zip(xs,labels): box(x,5.35,1.75,.85,t)
    for x in [2.0,4.4,6.8,9.2]: ar(x,5.78,x+.65,5.78)
    box(.55,3.45,2.7,.95,"Zero-base lane\nstandalone specialist","#E8F5E9",GREEN)
    box(4.55,3.45,2.7,.95,"Attached lane\nexplicit base ABI","#FFF4CC",GOLD)
    box(8.55,3.45,2.7,.95,"Refusal path\ninvalid/unsafe input","#FDE8E7",RED)
    ar(5.9,5.35,1.9,4.4,GREEN); ar(5.9,5.35,5.9,4.4,GOLD); ar(7.0,3.92,8.55,3.92,RED)
    box(.55,1.5,2.35,.95,"Individual routing","#F2F4F7")
    box(3.15,1.5,2.35,.95,"Decision-space\ncoordination","#F2F4F7")
    box(5.75,1.5,2.35,.95,"Tool gate\nschema + postcondition","#F2F4F7")
    box(8.35,1.5,2.9,.95,"Lifecycle\ncanary · approval · rollback","#F2F4F7")
    for x in [1.72,4.32,6.92]: ar(x,3.45,x,2.45)
    ar(9.92,3.45,9.8,2.45)
    ax.text(6,.48,"Measured evidence families: contract · no-data execution · semantic behavior · release integrity · portability",ha="center",fontsize=8.5,color=MUTED)
    save(fig,"paper1_figure1_architecture")


def plot_series(ax, series, title):
    depth=series["depth"]
    for key in ("full","gamma_0_1","inverse_depth"):
        ax.plot(depth,series[key],marker="o",markersize=3.5,linewidth=1.8,color=PALETTE[key],label=LABELS[key])
    ax.set_yscale("log"); ax.set_xlabel("Cumulative stack depth"); ax.set_ylabel("Perplexity")
    ax.set_title(title,weight="bold"); ax.grid(True,which="both",alpha=.22,linewidth=.6)
    ax.legend(frameon=False,loc="upper left")


def paper2_curves():
    fig,axes=plt.subplots(1,2,figsize=(11.2,4.2),constrained_layout=True)
    plot_series(axes[0],DATA["paper2"]["local_additive"],"(a) Additive runtime path")
    plot_series(axes[1],DATA["paper2"]["remote_additive"],"(b) Second CPU host")
    fig.suptitle("Cumulative LoRA composition under gain control",fontsize=14,weight="bold",color=NAVY)
    fig.text(.5,.0,"Panels use different hosts/builds; absolute perplexities are not compared across panels.",ha="center",fontsize=8.5,color=MUTED)
    save(fig,"paper2_figure1_stability_curves")


def paper2_intervals():
    d=DATA["paper2"]["shard_deltas"]; fig,ax=plt.subplots(figsize=(7.2,4.2),constrained_layout=True)
    x=list(range(len(d["labels"]))); means=d["means"]
    ax.errorbar(x,means,yerr=[[m-l for m,l in zip(means,d["low"])],[h-m for m,h in zip(means,d["high"])]],fmt="o",capsize=5,color=NAVY,linewidth=1.5,markersize=6)
    ax.set_xticks(x,d["labels"]); ax.set_ylabel("Paired perplexity difference vs. base\n(shard means)")
    ax.set_title("Gain schedules: five disjoint corpus shards",weight="bold",color=NAVY)
    ax.axhline(0,color="#7B8794",linewidth=.8); ax.grid(axis="y",alpha=.25)
    ax.text(.02,.03,"n=5; paired t interval; df=4; depth rows are not replicates",transform=ax.transAxes,fontsize=8,color=MUTED)
    save(fig,"paper2_figure2_gain_intervals")


def paper2_payload_remote():
    fig,axes=plt.subplots(1,2,figsize=(11.2,4.2),gridspec_kw={"width_ratios":[.9,1.25]},constrained_layout=True)
    slots=DATA["paper2"]["payload_slots"]; cls={"A":BLUE,"B":GOLD,"C":TEAL}
    for i,s in enumerate(slots):
        axes[0].add_patch(Rectangle((i,.05),.9,.9,facecolor=cls[s["class"]],edgecolor="white",linewidth=1))
        axes[0].text(i+.45,.5,s["class"],ha="center",va="center",color="white",weight="bold",fontsize=10)
    axes[0].set_xlim(0,9); axes[0].set_ylim(0,1); axes[0].set_xticks([i+.45 for i in range(9)],[str(i+1) for i in range(9)]); axes[0].set_yticks([])
    axes[0].set_xlabel("Nominal stack slot"); axes[0].set_title("(a) Nine slots, three payload classes",weight="bold")
    axes[0].text(4.5,-.23,"A/B/C are byte-level equivalence classes",ha="center",fontsize=8,color=MUTED)
    plot_series(axes[1],DATA["paper2"]["remote_additive"],"(b) Qualitative second-host replication")
    fig.suptitle("Payload identity and cross-host behavior",fontsize=14,weight="bold",color=NAVY)
    fig.text(.5,.0,"Only within-host deltas are interpreted; absolute scales remain host/build specific.",ha="center",fontsize=8.5,color=MUTED)
    save(fig,"paper2_figure3_payload_replication")


def paper2_trajectory_3d():
    fig=plt.figure(figsize=(8.2,6.0),constrained_layout=True)
    ax=fig.add_subplot(111,projection="3d")
    series=DATA["paper2"]["local_additive"]
    depth=series["depth"]
    for idx,key in enumerate(("gamma_0_1","inverse_depth","full")):
        y=[idx]*len(depth)
        ax.plot(depth,y,series[key],marker="o",linewidth=2.0,color=PALETTE[key],label=LABELS[key])
    ax.set_xlabel("Stack depth",labelpad=8); ax.set_ylabel("Schedule",labelpad=8); ax.set_zlabel("Perplexity",labelpad=8)
    ax.set_yticks([0,1,2],[r"$\gamma=0.1$",r"$1/k$",r"$\gamma=1$"])
    ax.set_zscale("log"); ax.view_init(elev=25,azim=-58)
    ax.set_title("Measured trajectory surface: depth × gain schedule × perplexity",pad=16,weight="bold",color=NAVY)
    ax.legend(frameon=False,loc="upper left",bbox_to_anchor=(0.0,1.0))
    fig.text(.5,.01,"All points are measured values from Paper 2 controls C2/C3/C9; no interpolation is used.",ha="center",fontsize=8.5,color=MUTED)
    save(fig,"paper2_figure4_trajectory_3d")


if __name__ == "__main__":
    paper1_architecture_fallback(); paper1_lanes(); paper2_curves(); paper2_intervals(); paper2_payload_remote(); paper2_trajectory_3d()
    print("generated 6 publication figures")
