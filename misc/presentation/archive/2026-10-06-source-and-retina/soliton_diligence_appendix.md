# Soliton Microcombs — diligence and planning appendix

October 2026. All dollars USD; years run from financing close. This document accompanies the consolidated deck and one-pager. Quantitative targets are proposed acceptance criteria or operating assumptions unless explicitly attributed to a public source. It does not assert customer commitments or company measurements that were absent from the supplied materials.

## 1. Product and scope

The first commercial objective is a packaged multi-wavelength optical source for optical-engine designers and source integrators. A CW laser pumps a nonlinear microresonator to generate a comb. Conditioning/distribution and controls prepare the output for the customer interface. The deliverable is the source module, including pump and any required amplification/thermal management in its economics; it is not a complete data link or compute engine.

Gen 1 uses an external pump and a modular integration strategy. SiN is an initial candidate; the selected band, dispersion, coupling, and available process must be confirmed before tapeout. Later AlGaAs or heterogeneous integration are possible engineering options, not a guaranteed performance roadmap.

The initial feasibility gate is 16 usable carriers meeting the agreed specification. The current project's 50-carrier ambition is retained as a 32–50-carrier expansion objective. This change avoids funding a visible-line-count milestone without proving useful delivered power. More carriers are valuable only if the customer architecture can use them.

## 2. Technical acceptance and evidence

Complete the interface specification before finalizing layout:

| Parameter | Required decision/evidence |
|---|---|
| Band and grid | Prospect-selected operating band, spacing, absolute alignment, and tolerance |
| Output ports | Number of fibers/waveguides and power delivered on each |
| Usable lines | Minimum delivered power, flatness, noise, and stability for every counted line |
| Control | Automatic startup, stable operating window, recovery behavior, control-electronics burden |
| Temperature | Agreed operating range, warmup, drift, and recovery testing |
| Electrical draw | Complete pump, electronics, heating/cooling, amplification, and conditioning measurement |
| Reliability | Alpha acceptance distinct from later production qualification |
| Data test | Rate/channel, simultaneous channels, modulation, BER/FEC, receiver, losses, and duration |

Proposed feasibility tests are 24-hour operation and at least 95 successful cold starts in 100 attempts under defined conditions. These are not industry qualification standards or achieved results. Production requirements will be customer-specific and may be much stricter.

A later >1Tb/s gross demonstration could use 40 channels at 25Gb/s, but the lean raise does not guarantee this experiment. Feasibility work includes a partner-supported transmission test only if equipment, usable-channel count, and interface availability permit. Gross line rate must be distinguished from net payload throughput.

### Optical budget

Use `required optical pump = useful output / (usable pump-to-comb efficiency × output transmission)`. Then divide by the pump's wall-plug efficiency and add controls and thermal management to obtain total electrical power. The efficiency boundary must be consistent; do not count coupling loss twice or count residual pump as useful comb power.

Illustration: 64 channels at 1mW delivered per line require 64mW output. At 5% usable conversion and 50% transmission, pump input is 2.56W optical. At 20% wall-plug efficiency, pump electrical consumption is 12.8W before controls. If 16 ports each need identical line power, the aggregate output requirement rises sixteenfold. Amplifiers alter both optical noise and electrical cost; they must be modeled explicitly.

The 1mW/line and efficiency figures here are examples, not customer requirements. Some architectures achieve much higher conversion; the design must establish its own efficiency. [Kerr microcomb conversion-efficiency review](https://www.nature.com/articles/s44310-024-00030-9)

Automatic operation has been demonstrated in prior microcomb research. The company's prospective moat must lie in an owned implementation rather than the existence of turnkey microcombs. [Integrated turnkey soliton microcombs](https://arxiv.org/abs/1911.02636)

## 3. Competition and integration

Ayar SuperNova specifies up to 16 wavelengths per fiber across 16 fibers, serving 256 data channels. Lightmatter Guide specifies up to 16 wavelengths per fiber, 16 output fibers, and a 200GHz grid. Both are real alternatives and may be competing internal source strategies, rather than presumed buyers. Their appearance in this presentation implies no relationship. [Ayar product page](https://ayarlabs.com/supernova), [Lightmatter Hot Chips 2025, slide 17](https://lightmatter.co/wp-content/uploads/2025/08/57-lightmatter_hotchips_2025_final.pdf)

Guide's published spectrum is in the O-band around 1300–1320nm. The older appendix's 1520–1580nm design cannot be presented as a drop-in replacement for that interface. Select the customer and wavelength requirements together.

Compare the same delivered carrier count, port count, usable power, reliability requirement, and package boundary. Customer ASP, internal COGS, bare-die area, and module size must not be mixed. Full-module electrical consumption must not be compared with optical pump power or the passive die alone.

Foundry capabilities evolve. LIGENTEC describes SiN platforms and heterogeneous active-photonics integration, but the exact chosen MPW stack, design rules, turnarounds, and packaging requirements need quotations. Access to a generic SiN PDK does not establish a monolithic comb/modulator/detector product. [LIGENTEC technology](https://www.ligentec.com/technology/), [platform history](https://www.ligentec.com/about-our-story/)

## 4. Commercial path and market validation

Initial account types are optical-I/O developers, optical-engine suppliers, and source integrators. Hyperscalers can influence requirements and procurement but should not be categorically excluded as component buyers. Account-level make/buy decisions are what matter.

The selling sequence is requirements → evaluation → design-in → qualification → production orders. A paid sample, MOU, or pilot is not a production commitment. Define the work, acceptance criteria, integration responsibilities, and next purchasing decision in every evaluation agreement.

Planning assumes evaluation modules in Year 2, low-rate shipment in Year 3, and more meaningful ramps in Years 4–7. These dates are provisional and can move materially with customer schedules and reliability work.

Annual addressable source revenue is estimated as system shipments × modules per system × realizable ASP. Count unique source purchases, rather than summing full optical-engine, interconnect, AI-compute, and hyperscaler spending. One source serving many channels can reduce unit demand.

Build an opportunity register with: account/program, system volume, sources/system, selected band/grid, source alternatives, evaluation state, qualification work, intended procurement date, and evidence for the quantity. Do not probability-weight a pipeline until real opportunities exist.

Year 5 base volume is provisionally five programs at 500 modules/year. Year 5 upside is seven programs at 1,000/year. Programs need not represent distinct customers. Concentration risk, cancellation rights, exclusivity, and customer internal development must be assessed separately.

Licensing and NRE are optional commercial paths but contribute no assumed income to these scenarios. If actual development agreements appear, separate one-time NRE, recognized license fees, unit royalties, and product revenue; avoid counting mutually exclusive supply and licensing models twice.

## 5. Operating assumptions

| Year | Evaluation/production ASP | Delivered COGS/unit | Gross margin when selling | Base units | Base revenue |
|---|---:|---:|---:|---:|---:|
| 1 | $5,000 | $4,000 | — | 0 | $0 |
| 2 | $5,000 | $4,000 | 20% | 20 | $100k |
| 3 | $4,500 | $3,000 | 33.3% | 150 | $675k |
| 4 | $4,000 | $2,200 | 45% | 750 | $3.0M |
| 5 | $3,500 | $1,575 | 55% | 2,500 | $8.75M |
| 6 | $3,200 | $1,376 | 57% | 6,500 | $20.8M |
| 7 | $3,000 | $1,200 | 60% | 12,000 | $36.0M |

The original $30–50M Y5 model requires 10,000 modules at $3–5k. It is mathematically valid but is moved beyond the base scenario because no account-based quantity evidence was provided. The replacement Y5 upside is $24.5M; its Y7 $105M requires 35,000 modules at $3k, a substantial adoption hypothesis.

COGS includes pump, comb die, conditioning/amplification if required, electronics, package, assembly/test, yield loss, warranty allowances, and delivery costs. Actual accounting classification depends on the business. Routine customer engineering and research are budgeted separately in cash opex. Early prototype costs are not evidence of mature production COGS.

The revised base case uses cash opex of $0.35M, $0.85M, $1.6M, $2.8M, $4.5M, $7M, $10M, and capex of $0.10M, $0.15M, $0.25M, $0.40M, $0.60M, $0.80M, $1M across Y1–7. Cash gross profit less opex becomes positive in Y5; capex and working-capital growth keep cash flow before financing negative that year. The model first shows positive annual cash flow in Y6. It is not a GAAP profit forecast.

Working capital is simplified to 20% of product revenue. Cash before financing is gross profit − cash opex − capex − change in working capital. Model assumptions exclude taxes, debt service, financing fees, licensing, grants, acquisition proceeds, and unmodeled respins. Annual aggregation can hide temporary cash shortages.

The updated model's peak cumulative deficits are $5.55M delayed, $6.94M base, and $7.06M upside. These are mechanical financing minima before liquidity reserve and execution risk, not sufficient financing commitments. The base planning envelope remains $9–12M cumulative, including pre-seed; qualify it with an actual monthly manufacturing and customer schedule. The upside's strong later gross profit offsets growth spend in this model, but working-capital and supply-chain shocks could require considerably more funding.

The delayed case assumes eventual technical success and similar unit-cost learning. It does not capture complete failure, no design wins, adverse yield, or loss of a major customer. Zero revenue and zero investor recovery remain possible. A rise in Y5 COGS from $1,575 to $2,100, with base ASP and volume unchanged, reduces gross margin from 55% to 40% and gross profit from $4.8125M to $3.5M. Cash opex then exceeds gross profit by $1M before capex and working capital.

## 6. Pre-seed budget and financing gates

The current $750k ask is retained with revised deliverables and duration:

| Category | USD |
|---|---:|
| People and specialist support | $250k |
| Fabrication and packaging | $220k |
| Shared lab and test access | $100k |
| Operations and IP | $65k |
| Contingency | $115k |
| Total | $750k |

Core scheduled spend is $635k over 15 months: $450k in months 1–12 and $185k in months 13–15. The monthly CSV holds $115k reserve unspent. The reserve is not both an expenditure and available cash; if consumed, it must be released against an identified risk. No revenue or grant is assumed during this period.

The next annual operating scenario assumes follow-on financing. The base Y2 opex/capex allocation is $1M in total: $185k for the first three months, plus $815k for the remaining nine months. Consequently, the $750k raise is not claimed to finance all of Year 2. Monthly procurement categories are cash uses; expense/capital classifications in the annual model are provisional and require accounting reconciliation.

Compensation is lean. $250k over 15 months is $200k/year combined people/specialist expenditure. This does not support several full-market-rate specialists plus a founder. A written staffing plan must allocate payroll costs, founder compensation, contractors, and employer costs. Shared facilities and partner equipment are prerequisites for the lean scope.

Milestones from close:

- M0–3: technical owner; quoted fabrication/packaging/lab access; two prospect specifications; selected interface and test plan.
- M3–6: tapeout and process test structures as foundry timing permits.
- M6–9: comb characterization and complete source-power measurements.
- M9–12: automated lab prototype and defined repeatability tests.
- M12–15: external evaluation, integration requirements, and next design cycle; partner-supported transmission work if equipment access allows.

Begin follow-on discussions around M8–10. Size the next raise from qualification and pilot-production work packages rather than promising a $10M seed at a specific month. A $3–5M next round is a sensitivity to assess, not a committed financing plan or sufficient-capital conclusion.

### Fully costed expansion option

If the desired pre-seed scope includes two fully funded fabrication/packaging cycles, more independent instrumentation, a transmission demonstration, and 18 months of work, the review proposes a $1.2M planning budget: $450k people/specialists, $300k fabrication/packaging, $180k lab/test, $90k operations/IP, $180k reserve. This is a separate scope requiring supplier quotes, not an alternative promise under the same $750k ask. Revise the deck and monthly schedule together if this option is adopted.

## 7. Investor economics

The operating strategy builds an independent supplier. No acquisition date, named buyer interest, or likely valuation is assumed. A list of possible strategic buyers is not evidence of an exit market for this particular company.

For a simplified cap-binding post-money SAFE, initial ownership is investment/cap. Gross exit multiple is exit equity value × retained fraction of initial ownership / cap. This simplification excludes conversion complexities, pool changes beyond the retention assumption, liquidation preferences, debt, taxes, fees, and additional investment.

Example: $750k at an $8M cap starts at 9.375%; 60% retention results in 5.625% at exit. $50M/$100M/$200M equity exits yield 3.75x/7.5x/15x gross multiples. A 10x result requires approximately $133M equity value, and 20x approximately $267M. These are conditional sensitivities, not expected returns. Actual investor fit depends on fund size, entry terms, ownership, follow-on capacity, and portfolio strategy.

The companion CSV covers $6M/$8M/$10M caps, 40%/60%/80% retention, and $30M–1B hypothetical equity values. None is an offered financing term. Its seven-year annualized return column is a mathematical timing illustration, not an assumed exit year. A larger acquisition projection cannot substitute for demonstrated market adoption or proprietary value.

## 8. Long-term Hopfion research direction

The older deck contributes a useful separation between near-term photonic engineering and exploratory topology-inspired computing. Its dated roadmap is replaced by research gates, without promised years for a compute module or fibration computer.

The long-term question is whether linked three-dimensional optical-field configurations can support useful information encoding or processing in an implementable physical system. Capabilities developed for sources—optical control, measurement, packaging, and nonlinear-device design—could support future experiments. That is a capability relationship, not proof that a comb chip generates a computational Hopfion.

Differentiate:

- **Dissipative Kerr solitons:** nonlinear circulating pulse states used here for comb generation.
- **Optical Hopfions:** linked three-dimensional field/polarization configurations, with topology defined through an appropriate field mapping.
- **Magnetic Hopfions:** three-dimensional spin textures in magnetic materials, requiring a different physical platform.
- **Hopf-fibration-inspired layout:** geometric inspiration; a toroidal chip or linked routing alone does not establish a topological state, noise protection, or computational advantage.

Research sequence: define the physical degrees of freedom and topology; develop a model with measurable observables; show generation and readout experimentally; demonstrate control and realistic perturbation response; then benchmark a specific task including input encoding, calibration, power, and readout. A compute product follows only if these gates succeed and a useful task is demonstrated.

Optical Hopfion structures have been experimentally studied, but that evidence does not establish the proposed company's integrated memory or computation architecture. [Particle-like topologies in light](https://www.nature.com/articles/s41467-021-26171-5) Magnetic Hopfions are separately documented in magnetic systems. [Creation and observation in magnetic multilayers](https://www.nature.com/articles/s41467-021-21846-5)

The old one-pager's claims of entanglement-like linked-memory access, automatic topological protection, and guaranteed global-optimum Ising solutions are not retained. A driven nonlinear optical network requires an explicit mapping and convergence analysis; an optical loss minimum is not automatically the desired discrete Ising ground state. Analog optimizers can return suboptimal solutions, and their full time-to-solution must include repeated trials and system overhead. [Geometric landscape annealing and Ising mapping](https://doi.org/10.1103/PhysRevX.14.031054)

This research has no dedicated work package, product revenue, or valuation contribution in the current pre-seed model. Future experiments require separate resources and stage gates. Photonic-retina work is presented as a possible future application, with no assumed sales or dedicated work in the current budget.

## 9. Information to confirm

For presentation accuracy, confirm advisor engagement and permission for attribution, current technical work/results, laboratory arrangements, and any customer evaluation discussions. For underwriting, obtain vendor quotations, a committed technical lead, customer interface specifications, a delivered COGS/yield model, and design/control IP ownership. Replace assumptions with evidence as it becomes available; do not convert targets into historical results.

## 10. Consolidation record

`soliton_PD.tex` controls the current light-source scope, founder/contact details, and $750k ask. `PITCH_DECK.tex` contributes the broader research direction and team context, but its $2M seed ask, complete-link product, speculative compute dates, and historical market totals are superseded. `ONE_PAGER.txt` is historical research ideation; its toroidal/Ising architecture is not used as a current product specification. `soliton_PD_Appendix.txt` contributes design-in and qualification considerations, but its outdated pipeline, acquisition predictions, AI/camera performance claims, and categorical buyer statements are superseded.

The prior review remains an audit record. This package revises its annual financial model to align the first-year cash allocation with the narrower feasibility raise; it does not silently change the original documents.

## 11. Photonic retina: a possible future application

The idea is to combine sensing and photonic processing so useful features can be extracted near the sensor. This is a reasonable research direction, but it introduces a detector array, electrical drivers, modulators, a processing circuit, and readout in addition to the comb source. It is not simply a different use of the existing module without extra development.

The proposed first setup is detector array and electronics → modulators fed by the microcomb → small photonic processing circuit → output detectors and decision electronics. Start with a simple left/right bright-object task. Compare accuracy, full-system power, and sensing-to-result time with an electronic implementation using the same input and task. Include detector integration time, driver bandwidth, calibration, noise, and readout in the measurements.

Several comb wavelengths could help process inputs in parallel, but the experiment must show why a comb is better than a single source or electronic processing for the chosen task. A complete camera or general image classifier is a later step, conditional on useful results. No GHz full-frame rate, sub-nanosecond full-system response, zero standby power, or fixed accuracy is claimed.

Related optical image-classification systems have already been demonstrated, including direct on-chip processing of incident optical inputs. Those architectures differ from the proposed detector/modulator/comb setup. They support investigating the area, not a claim of being first or of inheriting their performance. [On-chip photonic image classification, Nature (2022)](https://www.nature.com/articles/s41586-022-04714-0)

The slide-level distinction among Kerr solitons, optical Hopfions, and magnetic Hopfions has been removed to keep the vision presentation focused. The physical distinction remains in these technical notes because it matters when selecting an experimental platform.
