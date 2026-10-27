# Photonic retina — revised product and funding brief

6 October 2026. The founder has clarified that the product intended for this raise is a compact photonic retina: sensing plus photonic processing. The microcomb is a possible component of that product. The existing interconnect-source presentation and module-sales model therefore do not represent the current product objective. No new PDF has been compiled after this clarification.

**Further clarification:** the intended first system is a simple detector plus an ML-designed, semi-tunable optical mask/chip, for preprocessing in doorbell or Flock-style cameras. See `photonic_retina_mask_assessment.md`. The detector–modulator–microcomb setup below is an earlier possibility, not the selected design; a passive scene-light optical front end may not require a microcomb.

The founder has now specified an **on-chip optical circuit with partly adjustable weights**. Its first architecture needs spatial optical inputs feeding the weighted circuit, followed by photodetection and readout. The circuit and input optics must be designed for the actual scene illumination; a coherent-laser processor is not assumed to handle natural camera light unchanged.

## Proposed opening

> We are building a compact photonic retina: a sensor connected to a photonic circuit that processes what it sees. Our first prototype will perform a small, clearly defined vision task. We are seeking $750k to design and fabricate the chip, build the sensing and control setup, and measure accuracy, response time, and total power against an electronic implementation of the same task.

The task, optical input, integration scope, fabrication estimate, and development schedule must be established before presenting this as a committed delivery plan. A visible-light sensor feeding a processor and a directly illuminated near-infrared chip are different first prototypes. Neither is assumed to be the founder's choice yet.

## Root-PDF findings

| Local paper | What the paper supplies | What it does not establish |
|---|---|---|
| `2406.06096v1.pdf`, *Space-Time Hopfion Crystals* | A theoretical method using bichromatic structured fields and proposed emitter arrangements to form space-time Hopfion structures | A fabricated retina, image-processing circuit, demonstrated classifier, or prototype price |
| `2504.03981v1.pdf`, *Construction of Hopfion Crystals* | A mathematical framework for periodic Hopfion configurations using helical waves and rational maps; a foundation for studying realizable material systems | An implemented photonic chip or working computation/sensing device |
| `PRXQuantum.6.010338_AlGaAs.pdf`, *Versatile Chip-Scale Platform for High-Rate Entanglement Generation Using an AlGaAs Microresonator Array* | Experimental AlGaAs-on-insulator resonator arrays with thermal tuning and entangled-photon generation | A classical vision processor, a bright soliton light-source power budget, or integrated retina |

The AlGaAs paper's device has 20 resonators and uses five in several demonstrations. It operates as an entangled-photon source, including pumping below the parametric-oscillation threshold, rather than demonstrating a bright soliton-comb source for classical signal processing. It reports 6.5dB chip-to-fiber loss per facet for the particular device, with improvements discussed, and substantial external equipment: electro-optic modulation, RF drive, amplification, filters, and single-photon detectors. Low on-chip optical pump power is not total system electrical consumption.

The two Hopfion papers belong in the long-term research references. The AlGaAs work can inform material/device selection but cannot independently support a claim that the proposed retina is a straightforward replication.

Local references: [space-time paper](../../2406.06096v1.pdf), [construction paper](../../2504.03981v1.pdf), [AlGaAs paper](../../PRXQuantum.6.010338_AlGaAs.pdf).

## Closer technical precedent

*An on-chip photonic deep neural network for image classification* reports direct processing of incident optical inputs for image classification. It is closer to the intended product than the three root papers, though its architecture need not be the appropriate implementation for this project. Published classification results do not establish the performance of a new detector/modulator/microcomb setup. [Nature (2022)](https://www.nature.com/articles/s41586-022-04714-0), [author preprint](https://arxiv.org/abs/2106.11747).

## What the first prototype should answer

1. Can the sensing-to-processing path perform a specified useful task with repeatable accuracy?
2. How much time elapses from optical input to a usable decision, including sensing, electronics, and readout?
3. What is total electrical power, including the laser, drivers, tuning, and control?
4. What advantage does photonic processing offer against the same electronic task and input?
5. Does a microcomb's wavelength parallelism improve that result enough to justify the source and integration cost?

A left/right bright-object task can test wiring and signal flow. It does not by itself establish a differentiated vision product. A later application benchmark needs real variation, noise, lighting, and a customer-relevant outcome—potentially a narrow industrial inspection task, if supported by customer discovery. Do not claim a competitive market position based only on a demonstration video.

Compactness must refer to the full proposed product: sensing optics, chip/package, laser if required, drivers, control, and readout. A small die connected to large laboratory instruments is a useful prototype but not yet a compact finished device.

## $750k funding sensitivity

The founder's $100–300k estimate is treated as an unverified chip-fabrication input, not independently sourced pricing. Batch size alone does not determine it; process, die area, MPW/dedicated-run access, available components, design work, and packaging scope matter.

Illustrative allocation assuming the quoted chip cost excludes packaging and system testing:

| Use | Midpoint planning amount |
|---|---:|
| Chip fabrication | $200k |
| Packaging, board, sensing/driver integration | $100k |
| Team and design support | $200k |
| Shared lab access and test equipment | $80k |
| Operations, software, IP, customer work | $50k |
| Reserve for rework and iteration | $120k |
| Total | $750k |

Holding the other allocations fixed, $100k fabrication gives a $650k program; $300k gives $850k. Thus $750k can support the midpoint scope but not the upper-bound fabrication cost with all other work unchanged. If the estimate already includes assembly or test, avoid adding those costs twice. The reserve does not guarantee that an entire additional $300k chip run can be funded.

No 15- or 18-month promise is assigned to this new scope until process availability, staffing, integration, and turnaround are clarified. The older source-module monthly budget is not a retina procurement plan.

## Commercial and investment implications

Commercializing published physics can support a company when the implementation solves a valuable problem and the team can manufacture, integrate, and sell it. Reproduction alone does not demonstrate that case. The retina should be the headline because it is the intended product, rather than an extra feature added to justify an otherwise unrelated funding ask.

The next deck should explain the vision task and buyer, the first sensing/processing architecture, its measured or modeled status, the full prototype cost, the technical team, and the experiments this round enables. It should not retain the light-source module's $3–5k selling-price assumption or unit-sales trajectory. Retina selling price, volumes, margins, and eventual outcomes require their own product/customer model.

Open inputs requested from the founder: visible-light versus controlled near-infrared input; whether $100–300k covers fabrication alone or also packaging/test; and any identified foundry/process. Hopfion computing remains a longer-term direction with no contribution to the initial product forecast.
