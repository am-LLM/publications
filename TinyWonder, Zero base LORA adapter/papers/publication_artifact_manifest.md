# Publication Artifact Manifest

Project: Tiny Wonder / LoRA Lens Lab

This manifest is public-release oriented. It intentionally omits local workspace paths, agent traces, session identifiers, private prompts, and machine-specific control metadata.

## Paper 1 artifacts

- independent Tiny Wonder host release artifact;
- release manifest with content hashes;
- zero-base adapter manifests and weights;
- attached-lane compatibility fixture;
- closed tool schemas and evaluation fixtures;
- cancellation, replay, cache, and release receipts;
- clean-bundle reproduction script;
- page-permission transport microbenchmark receipt with repeated p50/p99 measurements;
- `tools/publication_hygiene.py`, a standard-library, read-only scanner for private paths, credential patterns, symlink escapes, VCS metadata, and staged-release residue. Exit codes: 0 clean/warnings-only, 1 release-blocking findings, 2 usage, 3 scan error.

## Submission PDFs

The current manuscripts are compiled into anonymous, figure-backed PDFs:

- `submission/paper1_zero_base_host.pdf` — 12 pages — SHA-256 `efbe77c517f045ad15b75fd5429788c2a896aaf4e0cd05db76a8ed0443665365`;
- `submission/paper2_stacking_attenuation.pdf` — 10 pages — SHA-256 `e3e2925862957f94a698242f6e9b2499629f66ed6d5d7f8d06aa37c332da9c02`;
- `submission/make_pdfs.py` — reproducible ReportLab build source;
- `submission/README.md` — build and package notes.

The PDFs are seven pages each, with IMRaD headings, tables, references, limitations, artifact availability, and embedded vector figures.

## Figures

The publication bundle includes receipt-backed vector figures:

- `figures/paper1_figure1_architecture.svg` / `.pdf` — zero-base host architecture and lane separation;
- `figures/paper1_figure2_lane_boundary.svg` / `.pdf` — zero-base versus attached execution contract;
- `figures/paper2_figure1_stability_curves.svg` / `.pdf` — local additive and tensor-merge trajectories on separate axes;
- `figures/paper2_figure2_gain_intervals.svg` / `.pdf` — five-shard paired confidence intervals;
- `figures/paper2_figure3_payload_replication.svg` / `.pdf` — payload identity and second-host qualitative replication;
- `figures/data.json` — sanitized figure data with logical receipt sources;
- `figures/make_figures.py` — reproducible standard-library/matplotlib generator.

Figures must retain their captions, evaluator/host boundaries, and source metadata. Absolute PPL values from different hosts or evaluator scales must not be overlaid.

## Primary citation additions

- Punica: https://arxiv.org/abs/2310.18547 and https://github.com/punica-ai/punica;
- vLLM LoRA documentation: https://docs.vllm.ai/en/latest/features/lora;
- READ: https://arxiv.org/abs/2609.31600;
- PRM: https://arxiv.org/abs/2609.32332;
- LILAC: https://arxiv.org/abs/2607.04801.

## Paper 2 artifacts

- additive GGUF stacking raw results;
- tensor-merge raw results;
- attenuation schedules and configuration;
- per-adapter probe results;
- adapter-order control results;
- exhaustive permutation receipt over the six distinct payload-class orders;
- colon-style compatibility receipt for legacy `path:scale` semantics;
- constant-gain and 1/N baselines;
- corpus-level perplexity inputs and summary tables;
- evaluator version and hardware tags;
- corrected reference bibliography.

## Provenance contract

Every published result should carry:

- stable artifact identifier;
- content hash;
- experiment configuration digest;
- host/architecture tag;
- software/backend version;
- dataset or prompt-set identity;
- raw result path inside the release bundle;
- derived-table generator version.

## Public exclusions

Do not package credentials, private state databases, internal agent transcripts, session IDs, absolute home-directory paths, or unreviewed generated data.

## Publication status

Paper 1 and Paper 2 are evidence-integrated scientific drafts. Paper 1 includes the folded orchestration lane and current collision-boundary citations. Paper 2 includes local controls and the parent-verified second-host qualitative replication. Remaining submission boundaries are exact reference-protocol reproduction, independent adapter-training repetitions, exhaustive order permutations, and no cross-host absolute-PPL comparison.
