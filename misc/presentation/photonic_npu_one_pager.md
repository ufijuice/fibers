# A modular photonic NPU

Pavel Chekmaryov · p@occurai.com · October 2026

We are developing a photonic neural processing unit: a programmable optical compute core supported by electronic memory and control. A soliton microcomb supplies parallel optical carriers. The first chip we will fabricate is an 8×8 matrix–vector tile using an existing or shared source and external test electronics.

The first workload to validate is repeated dense projection in a small inference model, with weights reused over a continuous input stream. Prospective users are teams building real-time sensing and control hardware. The initial phase selects one task, evaluator and electronic baseline.

Our design hypothesis is that better readout and calibration can provide useful accuracy in one pass, reducing repeated measurements. The architecture has research precedent. Our implementation must establish its own advantage in complete-system latency or energy at matched task accuracy.

The proposed initial targets are ≤5% normalized single-pass MVM error and ≤1 percentage-point accuracy loss against the same digital model on a locked task. These are working acceptance targets for review against the loss/noise model and quotations before fabrication. The prototype also measures power, latency, stability and weight-update costs.

The working ask is **$750k for 15 months**:

| Allocation | USD |
|---|---:|
| People / specialist support | $280k |
| Compute-chip fabrication | $120k |
| Packaging / assembly | $70k |
| Electronics / shared lab | $100k |
| Microcomb / pump / optics access | $50k |
| Operations / IP | $30k |
| Contingency reserve | $100k |
| **Total** | **$750k** |

The base scope includes one compute-chip fabrication, shared facilities and lean staffing. A second custom source chip, custom CMOS controller, dedicated laboratory or guaranteed full respin is outside that allocation. Fabrication-only costs of $200k and $300k raise total funding needs to $830k and $930k respectively if the other allowances and reserve are maintained.

Pavel's background includes Snowcap Compute and exploratory work on topological features for learning, nonlinear optics and photonic layouts. A technical co-founder or photonics engineer with hands-on design, packaging and test experience is an early execution priority.

The development path is compute tile → packaged NPU → chiplet integration → a larger photonic–electronic SoC. Each generation requires its own performance evidence and funding.

The project is at an early design stage. No measured NPU performance, customer commitment, quoted manufacturing cost or processor advantage is claimed. Earlier light-source sales and exit models are archived; they do not forecast this product.

Research context: [microcomb tensor core](https://www.nature.com/articles/s41586-020-03070-1), [reconfigurable tensor processor](https://www.nature.com/articles/s41467-026-71599-2), [photonic–electronic accelerator](https://www.nature.com/articles/s41586-025-08786-6).
