# Current presentation: a modular photonic NPU

Updated 26 October 2026. The current objective is a processor that performs programmable computation in photonics, with electronic memory and control. The first proposed prototype is an 8×8 matrix–vector tile. A soliton microcomb supplies parallel carriers.

## Use these files

- [Pitch deck PDF](photonic_npu_preseed.pdf) and [editable LaTeX](photonic_npu_preseed.tex): 12 main slides plus technical appendix.
- [One-page PDF](photonic_npu_one_pager.pdf), [LaTeX](photonic_npu_one_pager.tex), and [plain-language overview](photonic_npu_one_pager.md).
- [Technical and commercial assumptions](photonic_npu_diligence.md).
- [Sources and claim boundaries](sources.md).
- [Draft follow-up to Andy](outreach_andy.md). No message has been sent.
- [Budget generator](preseed_budget.py), [allocation](preseed_budget.csv), [monthly cash plan](preseed_monthly_budget.csv), and [fabrication sensitivity](fabrication_sensitivity.csv).

The deck states proposed targets and the present development stage. The repository contains exploratory simulations and generic-PDK layout work; it does not establish measured performance of this NPU, customer commitments, or a fabrication-ready design.

## Scope and figures

The working ask is $750k for a 15-month feasibility program: $650k scheduled work and $100k reserve. The base scope includes one new compute-chip fabrication, an existing or shared microcomb/pump setup, external test electronics, and shared laboratory access. It does not include a second custom source chip, a custom CMOS controller, or a guaranteed full respin.

The proposed first precision targets are ≤5% normalized single-pass MVM error and ≤1 percentage-point inference-accuracy loss against the same digital model on a locked task. These are initial acceptance targets to review against the noise model and quotations before tapeout. No achieved speed, energy advantage, effective bit precision, or production margin is claimed.

There is no new NPU sales or exit forecast. Earlier source-module models do not apply to this product.

## Build

From the repository root:

    python3 misc/presentation/build.py

This regenerates the budget and compiles both PDFs twice using pdflatex. Intermediates stay in the ignored build/ directory. To regenerate only the financial tables:

    python3 misc/presentation/build.py --budget-only

The budget values and table included in both PDFs are generated from the same Python allocations.

## Earlier work

Previous source-module and retina presentations, original pitch files, reviews, and projections are preserved under [archive](archive/README.md). They are historical material. The movement manifest records old paths, new paths, and verified SHA-256 hashes.

The two Hopfion papers and AlGaAs paper formerly at the repository root are now in [references/papers](../../references/papers/). Old root-level images and animations are in results/legacy-root/. Simulation and layout entry points keep their original paths.
