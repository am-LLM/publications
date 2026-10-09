# ⚡ Tiny Wonder: Zero-Base LoRA Adapter Host & Stacking Attenuation

**Scientific Manuscripts, Reproducible Artifacts, and Vector Figures for Zero-Base LoRA Host Architectures and Multi-Adapter Stacking Dynamics.**

---

## 📄 Scientific Manuscripts & Submission Packages

| Document | Format | Description | Artifact Link |
|---|---|---|---|
| **Paper 1: Zero-Base LoRA Host** | PDF / DOCX / Markdown | *Zero-Base LoRA Host Architecture: Decoupled Multi-Tenant Adapter Execution and Strict Lane Isolation* | [`paper1_zero_base_host.pdf`](./paper1_zero_base_host.pdf) • [`Draft`](./papers/paper1_zero_base_host_draft.md) |
| **Paper 2: Stacking Attenuation** | PDF / DOCX / Markdown | *Dynamic Stacking Attenuation and Interference Dynamics in Multi-LoRA Composite Ensembles* | [`paper2_stacking_attenuation.pdf`](./paper2_stacking_attenuation.pdf) • [`Draft`](./papers/paper2_stacking_attenuation_draft.md) |

---

## 🏛️ Directory Layout

```
TinyWonder, Zero base LORA adapter/
├── paper1_zero_base_host.pdf          # Latest submission PDF (Paper 1)
├── paper2_stacking_attenuation.pdf    # Latest submission PDF (Paper 2)
├── README.md                          # Repository overview & navigation
├── make_docx.py                       # Manuscript DOCX build script
├── papers/
│   ├── README.md                      # Publication notes & overview
│   ├── paper1_zero_base_host_draft.md # Complete Markdown text of Paper 1
│   ├── paper2_stacking_attenuation_draft.md # Complete Markdown text of Paper 2
│   ├── publication_artifact_manifest.md     # Public release provenance manifest
│   ├── submission/
│   │   ├── paper1_zero_base_host.pdf
│   │   ├── paper1_zero_base_host.docx
│   │   ├── paper2_stacking_attenuation.pdf
│   │   ├── paper2_stacking_attenuation.docx
│   │   ├── make_pdfs.py               # Reproducible ReportLab PDF compiler
│   │   └── README.md
│   └── figures/
│       ├── paper1_figure1_architecture.svg / .pdf / .png
│       ├── paper1_figure2_lane_boundary.svg / .pdf / .png
│       ├── paper2_figure1_stability_curves.svg / .pdf / .png
│       ├── paper2_figure2_gain_intervals.svg / .pdf / .png
│       ├── paper2_figure3_payload_replication.svg / .pdf / .png
│       ├── paper2_figure4_trajectory_3d.svg / .pdf / .png
│       ├── data.json                  # Sanitized vector figure telemetry
│       └── make_figures.py            # Reproducible figure rendering engine
└── tools/
    └── publication_hygiene.py         # Zero-leak release audit verification tool
```

---

## 🔬 Core Contributions

### 1. Zero-Base Host Architecture (Paper 1)
* **Decoupled Adapter Execution**: Eliminates monolithic weight merging by maintaining isolated runtime lanes for base foundation weights and modular rank-$r$ adapters.
* **Page-Permission Transport**: High-throughput memory-mapped weight paging with sub-millisecond switching overhead.
* **Deterministic Boundary Isolation**: Prevents cross-tenant state pollution and interference across concurrent inference pipelines.

### 2. Multi-Adapter Stacking Attenuation (Paper 2)
* **Harmonic Interference Mitigation**: Analyzes destructive interference when stacking $K \ge 3$ heterogeneous LoRA adapters.
* **Dynamic Attenuation Schedules**: Formulates optimal gain decay profiles ($1/N$, exponential, and learned per-layer weighting) to maintain low perplexity across composite tasks.
* **Empirical Replication**: Verified across multi-shard evaluation benchmarks with paired confidence intervals.

---

## 🛡️ Release Verification & Publication Hygiene

This distribution has been audited using [`tools/publication_hygiene.py`](./tools/publication_hygiene.py) to guarantee:
- Zero internal hostnames, machine IP addresses, or private cluster topology leaks.
- Zero API keys, private tokens, or credential patterns.
- Fully sanitized and reproducible vector figure data.

To verify the tree:
```bash
python3 tools/publication_hygiene.py .
```
