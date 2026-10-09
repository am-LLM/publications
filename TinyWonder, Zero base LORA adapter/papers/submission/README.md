# Submission package

The submission PDFs are generated from the isolated Markdown manuscripts with the reproducible ReportLab builder. Figures are generated from `papers/figures/data.json`; editable Mermaid source is retained in `papers/figures/paper1_architecture.mmd`, while Graphviz/Matplotlib-compatible vector sources and high-resolution derivatives are preserved alongside the PDFs.

```text
python3 papers/figures/make_figures.py
python3 papers/submission/make_pdfs.py
```

Artifacts:

- `paper1_zero_base_host.pdf` — 12 pages
- `paper2_stacking_attenuation.pdf` — 10 pages
- `make_pdfs.py`
- `../figures/*.svg` and `../figures/*.pdf`
- `../figures/paper1_architecture.mmd`
- `../figures/rendered/*.png` — high-resolution composition derivatives

Absolute PPL values from different evaluators remain separated in Paper 2 figures and text. The measured 3D trajectory view uses only C2/C3/C9 values and is not treated as an additional replicate.
