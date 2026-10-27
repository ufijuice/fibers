# Photonic NPU: development and funding assumptions

26 October 2026. USD throughout. This document supports the current pitch; it distinguishes the proposed first experiment from later products.

## Product and starting point

The objective is a computing processor. Gen 1 performs programmable matrix–vector multiplication in an optical core, with electronic buffering, conversion, calibration, nonlinear activations and scheduling. The first proposed scale is eight optical input channels and eight logical outputs. This is a development target, not a measured implementation or a foundry-ready layout.

The founder reports experience at Snowcap Compute and earlier topological-ML experiments. The repository contains nonlinear-wave simulations and generic-PDK layout experiments. These are preparation and research artifacts; neither their existence nor the published ML paper establishes performance of the proposed NPU. The new compute design, its loss/noise model and its numerical interface remain to be completed.

The base feasibility scope fabricates one compute chip and uses an existing or shared soliton microcomb with external pumping. That choice concentrates the new fabrication work on arithmetic. It does not make the source free, eliminate optical qualification, or establish a production supply agreement. Source access must be confirmed before committing to the compute design.

## Initial application and design hypothesis

The initial workload hypothesis is repeated dense projections in a small inference model, with weights fixed across a stream of input vectors. Prospective evaluators are teams developing real-time sensing and control hardware. No specific buyer, paid evaluation, letter of intent or production program has been established in this material.

The proposed engineering hypothesis is that readout and calibration improvements can deliver the task's required accuracy in a single pass, reducing repeated measurements. Candidate levers are receiver gain/bandwidth, optical coupling loss, source-to-detector power allocation, signed reference paths and calibration of weight transfer functions. These are investigations, not claims of owned inventions or demonstrated superiority.

The basic architecture is prior art. A [2026 reconfigurable tensor-processor paper](https://www.nature.com/articles/s41467-026-71599-2) reports 19.4% normalized MVM error in its single-measurement mode and 10.9% after four-measurement averaging. It identifies converter and receiver electronics as major energy costs. The test conditions are specific to that system; its figures are not a universal baseline or our projected result.

The first phase should select one representative task and a comparison boundary with an evaluator. It should determine how much of that task's latency and energy actually belongs to the recurring projection. An optical core is less useful if data loading, other layers or host interaction dominate.

## Acceptance protocol

The deck proposes two initial targets:

- Normalized MVM error at or below 5%, in a single pass.
- Inference accuracy within one percentage point of the same electronic model on a locked task.

These figures are planning judgments. They require a physical error budget and review with the technical lead and evaluator before fabrication. If the initial design cannot support them, revise the design or proposed scope before tapeout. Do not change the test protocol after inspecting reserved results.

For reference vectors x_i and ideal results y_i = W x_i, define:

    epsilon_MVM = sum_i ||measured_y_i - y_i||_2 / sum_i ||y_i||_2

Use a fixed, documented test population. Record input/weight ranges, signed encoding, calibration data, gain settings and excluded channels. Report absolute error for near-zero results, error distributions across channels, and behavior under cancellation. A mean error alone can hide unusable channels or poor dynamic range.

Weight resolution, ADC nominal bit depth, effective computational precision and classification accuracy are different quantities. A 5% vector error does not establish a particular number of effective bits. Task-level comparison should include the same trained weights and relevant electronic quantization baselines.

If repeated samples or repeated optical calculations are used, count them in energy and latency. Report source startup and recalibration separately, then include their duty-cycle effect for the intended application. Establish the initial laboratory temperature conditions and a sustained-run test protocol before testing.

## End-to-end comparison

The device boundary is digital input-vector buffer to digital output-result buffer. Include DACs, input drivers, optical computation, receivers, ADCs, memory accesses and necessary control. Report host transfer overhead separately and include it in the full application comparison.

Measure total electrical input power, including the pump and thermal control. Use component estimates only when a rail cannot be measured independently, label them, and reconcile them with total input power. Do not count optical output power as electrical consumption or count a subsystem twice.

Compare:

1. An optimized CPU implementation on the same task.
2. An appropriate FPGA or electronic NPU implementation or defensible hardware model.
3. A GPU where the workload size and deployment make it relevant.

Do not establish an advantage by comparing one resident optical calculation with unnecessary host overhead on the electronic side. Report batch-one latency, continuous-stream throughput, precision, weight-update frequency, amortized energy, setup cost and all offloaded operations.

Arithmetic throughput for N inputs, M outputs and r complete vectors/s is N*M*r MAC/s. If counting two operations per MAC, gross throughput is 2*N*M*r operations/s. For an 8×8 tile at a hypothetical 1 Gvector/s that is 0.128 TOPS. This arithmetic does not establish operating speed or performance at useful precision.

The small tile validates the loss/noise and electronics models. A later scaled design must include splitter loss, power per channel, crosstalk, tuning, receiver range, converters, routing, packaging, calibration and memory. Converter overhead may amortize with larger matrices; optical loss and required signal-to-noise can also grow. Neither a linear power extrapolation nor a guaranteed GPU advantage is assumed.

## Materials and layout

Initial candidates:

| Function | Candidate | Decision required |
|---|---|---|
| Multiwavelength source | Existing low-loss SiN soliton source and pump | Accessible source, comb state, band, spacing, useful line power and noise |
| Modulators and weights | Qualified silicon-on-insulator platform | Transfer curves, loss, bandwidth, tuning power and device availability |
| Detection | Foundry-supported Ge/SiGe photodiodes | Responsivity, saturation, bandwidth and receiver-noise budget |
| Control | FPGA/SRAM and external electronics initially | Converter precision, rates, interfaces and power |
| Later weight memory | Electrically programmed optical phase-change devices | Precision, drift, endurance, thermal interaction and foundry access |

Around 1550 nm is the starting band. The compute grid and optical power must match the actual source. A nominally CMOS-compatible material does not imply that the selected foundry supports all required devices in one process.

A tile can use wavelength input encoding, fan-out to output weight banks and balanced detection for signed weights. The input representation must explicitly support the chosen signed or nonnegative activation range. Keep monitor structures and electrical access for calibration. Control thermal coupling between tunable components and source operation. The detailed implementation and layout require a PDK, circuit simulation and design review.

Gen 1 does not require custom SiN fabrication, a custom CMOS controller, an integrated pump or a new memory material. These may become useful in a later product if measured results justify the added work. The older AlGaAs and Hopfion simulations do not qualify a foundry process for the NPU.

## Team, intellectual contribution and execution

A hands-on photonics technical lead or co-founder is an early requirement. The work also needs receiver/converter engineering, fabrication-aware design, packaging and test support. The $280k people allowance is combined expenditure across 15 months, equivalent to $224k/year across the team and specialists. It supports lean staffing, not a large group of fully paid specialists.

Scientific contacts and advisor affiliations are not listed as committed team members until their role and public attribution are confirmed.

Potential protectable work must be an actual implementation contribution, such as an improved readout or calibration architecture. Existing papers, the use of a microcomb, and generic layouts are not claimed as company-owned advantages. Confirm access and rights to the PDK, source, software and specialist work used by the project.

## Budget and gates

The [generator](preseed_budget.py) is the numerical source of truth for the [allocation](preseed_budget.csv), [monthly plan](preseed_monthly_budget.csv), [sensitivity](fabrication_sensitivity.csv) and generated LaTeX tables.

| Category | USD |
|---|---:|
| People and specialist support | $280k |
| Compute-chip fabrication | $120k |
| Packaging and assembly | $70k |
| Electronics and shared lab | $100k |
| Microcomb, pump and optics access | $50k |
| Operations and IP | $30k |
| Protected contingency reserve | $100k |
| **Total** | **$750k** |

The model schedules $650k of spending and leaves $100k cash reserve after month 15. No revenue, grant, free equipment or follow-on funding is counted as a cash receipt. Shared source/facility access is a scope assumption whose actual cost must fit the allocated allowances.

Fabrication-only sensitivity holds $530k of other core work and $100k reserve fixed:

| Fabrication | Total financing required | Extra above $750k |
|---|---:|---:|
| $100k | $730k | $0 |
| $120k base | $750k | $0 |
| $200k | $830k | $80k |
| $300k | $930k | $180k |

At the $300k fabrication case, the core work alone costs $830k, so consuming the entire reserve would still leave an $80k shortfall. The reserve is not both scheduled spending and available contingency.

These are planning sensitivities, not quotations. Packaging is separate from fabrication. Confirm whether vendor prices include NRE, dies, test structures, engineering runs, assembly, optical attachment and electrical test. Avoid charging shared equipment or source access to two categories.

Before fabrication: secure the technical lead; define the workload and acceptance protocol; obtain a loss/noise model and independent design review; confirm source and lab access; reconcile written quotes with the total program budget. If the scope cannot fit, revise the plan before placing orders.

The base scope does not promise a full respin, two custom photonic chips, an all-optical memory hierarchy, commercial qualification or a finished SoC. M8–10 follow-on discussions should use actual progress and revised procurement timing; future financing is not assumed.

## Commercial development

The possible product is a packaged compute module, followed by integration as a chiplet or licensed block when customers support it. Development agreements and paid evaluations may fund later work, but no income from them is forecast here.

Build a simple account record: application, recurring operation, task accuracy, interface, volume indication, alternative processor, evaluation owner, next test and next purchasing decision. A positive technical discussion is not a purchase commitment.

A later commercial model should derive pricing and units from a specified module, bill of materials, packaging/test yield, customer evaluation cycle and demand. The former light-source ASPs, margins, sales volumes, $9–12M financing envelope and investor-return illustrations are archived. They are not NPU assumptions.

## Long-term research

Hopfion-based information encoding remains the founder's long-term research direction. The NPU is a proposed first hardware project; its usefulness for that later work still needs to be established.

The larger goal is a functioning photonic processor. The staged path is compute tile, packaged NPU, chiplet and photonic–electronic SoC. Each generation requires new integration work and financing.

Topology can supply workloads and representation hypotheses. An exact algebra engine additionally needs a mapping from the actual algorithm to physical operations and a correctness argument. A trained E₂ surrogate would be an approximate predictor and should be evaluated as such.

Hopfion encoding requires defined writing, manipulation and readout operations before it becomes a computational proposal. A photonic retina is a possible application of a future NPU, with its own optical sensing and electronic-interface requirements. Neither direction is an assumed first-round deliverable or revenue source.
