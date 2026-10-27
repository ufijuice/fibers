# Soliton pitch review and replacement financial assumptions

Reviewed 5 October 2026. Sources: `soliton_PD.tex` and `soliton_PD_Appendix.txt` in this directory. Original files have been preserved. Dollar figures below assume USD; neither original establishes the currency. Years in the replacement model start at financing close, not a calendar date. This review checks arithmetic and public technical evidence; it cannot establish demand, supplier pricing, IP ownership, or actual experimental results from these documents.

## Judgment

The interconnect light-source concept can support a credible pre-seed pitch, but the documents do not yet establish a fundable company. Their central weakness is the jump from published microcomb physics to a cheap, reliable, customer-compatible product with substantial sales. The exit projections expose that gap rather than cause it.

Do not replace a $50–200M acquisition promise with a $500M–1B promise. Replace the acquisition-led story with a business that can stand independently: a customer-defined light-source module, measured advantages at the same interface, a defensible implementation, staged qualification, and enough capital to prove those claims. Large outcomes belong in a conditional return sensitivity, not in the operating forecast.

My recommendation is to keep optical interconnect sources as the first product, move neural-network accelerators and photonic retinas into a separate research document, and remove Hopf-fibration computing from this raise. The appendix is partly useful sales planning and partly speculative conversation; it should not be circulated in its current form.

## 1. Exit economics: what needs to change

The deck promises $50–200M in years 3–5 (lines 303–304 and 437–438). The appendix alternatively says $30–100M after years 2–3, $50–100M in years 3–5, and calls acquisition the likely outcome (lines 87–127). There is no evidence for the likelihood, price, or buyer interest.

Illustration: $750k invested on an $8M post-money SAFE cap initially represents 9.375% under simplified cap-binding conversion assumptions. After retaining 60% of that ownership through future rounds and pool increases, it represents 5.625%. No pro-rata investment is included.

| Exit equity value | Gross investor proceeds | Gross multiple | Illustrative seven-year annualized return |
|---|---:|---:|---:|
| $30M | $1.688M | 2.25x | 12.3% |
| $50M | $2.813M | 3.75x | 20.8% |
| $100M | $5.625M | 7.50x | 33.4% |
| $200M | $11.250M | 15.00x | 47.2% |
| $300M | $16.875M | 22.50x | 56.0% |
| $500M | $28.125M | 37.50x | 67.8% |

These are conditional successful-exit returns, not expected returns. They omit failures, preferences, debt, taxes, fees, earn-outs, and additional invested capital. Equity proceeds must be distinguished from acquisition enterprise value. At small exits, the preference waterfall could materially change these results.

The simple gross multiple is `exit equity value × retained ownership fraction / post-money cap`. At an $8M cap and 60% retention, a 10x result requires about $133M; 20x requires about $267M. At a $10M cap the thresholds rise to $167M and $333M. If only 40% of initial ownership remains, the $8M-cap thresholds become $200M and $400M.

This means the existing exit range is not inherently unsuitable for all pre-seed funding. Its low end, particularly after a capital-intensive development program, is unattractive for investors whose portfolios need large winners. For example, a $500k check at the same $8M cap and 60% retention owns 3.75% at exit: a $100M exit returns $3.75M and a $500M exit $18.75M. Those outcomes have very different significance to a $20M fund versus a $100M fund.

The $10M seed target also needs scrutiny. A simplified $10M raise at $20M pre-money issues 33.3% to new investors before pool changes. Two subsequent 20% dilutive events leave initial investors with only 42.7% of their starting ownership. A $10M seed can be appropriate if supported by a funded qualification/manufacturing plan; it is not an automatically positive milestone.

Carta reports median 2025 post-money SAFE caps around $10M for $250k–$1M raises. This is broad US data, not a photonics valuation benchmark or a recommendation for this company. The $6M/$8M/$10M caps in the companion return CSV are sensitivities, not proposed legal terms. [Carta, 2025 pre-seed report](https://carta.com/data/state-of-pre-seed-2025/)

**Replacement deck wording:**

> We intend to build an independent supplier of qualified multi-wavelength light sources. Strategic acquisition is a possible outcome after technical validation and commercial adoption; our operating plan does not depend on a buyer or exit date. At a $3,000 mature module ASP, a $100M annual product business requires roughly 33,300 modules per year, supported by multiple production programs.

Do not put the $100M ambition in the deck unless you can explain how customer system volumes translate into this many modules. A $300–500M equity outcome can be shown internally as a venture-return sensitivity; it remains unsupported as a forecast.

## 2. Replacement operating scenarios

The original year-five arithmetic is correct: 10,000 modules × $3–5k = $30–50M. The adoption assumption is unsubstantiated. A module serving many fibers or optical engines could produce substantial system bandwidth with comparatively few module sales. More channels per module can also reduce required unit volumes.

The companion Python model and CSV separate units, price, delivered COGS, gross profit, cash operating expense, capex, and simplified working capital. They exclude licensing/NRE income and do not assume grants. Early sales are evaluation modules, not qualified production shipments. The base case assumes initial paid evaluations in year two, low-rate shipments in year three, and meaningful production ramp in years four through seven.

| Input or result | Y1 | Y2 | Y3 | Y4 | Y5 | Y6 | Y7 |
|---|---:|---:|---:|---:|---:|---:|---:|
| ASP, all scenarios | $5,000 | $5,000 | $4,500 | $4,000 | $3,500 | $3,200 | $3,000 |
| COGS/module, all scenarios | $4,000 | $4,000 | $3,000 | $2,200 | $1,575 | $1,376 | $1,200 |
| Delayed-case units | 0 | 0 | 30 | 150 | 500 | 1,500 | 3,500 |
| Delayed revenue, $M | 0 | 0 | .135 | .600 | 1.750 | 4.800 | 10.500 |
| Base units | 0 | 20 | 150 | 750 | 2,500 | 6,500 | 12,000 |
| Base revenue, $M | 0 | .100 | .675 | 3.000 | 8.750 | 20.800 | 36.000 |
| Upside units | 0 | 40 | 300 | 1,800 | 7,000 | 18,000 | 35,000 |
| Upside revenue, $M | 0 | .200 | 1.350 | 7.200 | 24.500 | 57.600 | 105.000 |
| Gross margin when selling | — | 20% | 33.3% | 45% | 55% | 57% | 60% |
| Base cash opex, $M | .50 | .90 | 1.60 | 2.80 | 4.50 | 7.00 | 10.00 |
| Base gross profit less cash opex, $M | -.50 | -.88 | -1.375 | -1.45 | .3125 | 4.856 | 11.60 |

These are more restrained planning cases than the original, not empirically validated predictions. Even the base case depends on obtaining design wins and qualifying the product. A plausible decomposition of Y5 base volume is five shipping programs averaging 500 modules/year; the upside requires roughly seven programs averaging 1,000. Programs can share customers, so this is not a claim of five or seven customers. Each program needs a named opportunity, system volume estimate, modules/system, procurement probability, and qualification date.

The upside uses the same unit-cost learning curve as the base for comparability. Real downside includes weaker yields, price pressure, cancelled programs, and complete technical failure; the delayed case alone does not capture it. Gross margin should be lower if pump, amplifier, packaging, or yield costs cannot reach the proposed COGS.

The modeled peak cumulative external capital needed is $5.80M delayed, $7.24M base, and $7.31M upside, before reserve, financing costs, tax, or debt service. This is a mechanical result of annual cash flows, not a fundraising estimate. Annual aggregation hides intra-year cash troughs. Working capital is provisionally 20% of revenue; replace it with inventory, supplier deposits, receivables, and payables. The upside demands much more operating scale even though modeled gross profit funds later growth.

For the base case, use a provisional cumulative financing envelope of **$9–12M through sustained positive cash flow**, subject to vendor quotes and a monthly plan. This adds liquidity and execution headroom to the modeled $7.24M deficit. It is not evidence that $9M will suffice: packaging failures, custom integration, slower qualification, or large production deposits could require substantially more. A $10M seed on top of pre-seed would consume much of this envelope and needs an explicit explanation of scope.

In the upside, $105M Y7 revenue at $3k ASP requires 35,000 modules/year. On a hypothetical $2B annual source market that would be 5.25% share; on $500M it would be 21%. That is why the market boundary and the module count must be established before calling the upside realistic. Do not obtain a $1B valuation by mechanically assigning a software-style revenue multiple to a component supplier. Strategic differentiation, growth, concentration, profitability, and comparable transactions all matter.

## 3. Raise, runway, and milestones

The original $250k + $250k + $150k + $100k totals $750k correctly. Rounded allocations total 99%; exact shares are 33.3%, 33.3%, 20%, 13.3%. Eighteen months implies average spend of $41,667/month. The team allocation supports only $166,667/year combined fully loaded compensation, or $83,333/year each for two people, with no extra specialists. That is a lean staffing assumption, not a validated hiring plan.

The deck funds fabrication, packaging, instrumentation, people, customer work, and a data demo with no explicit contingency. The milestone schedule has first soliton at M6 in one list and M7–9 in another. Closing funding at M3 while calling the plan an 18-month runway also leaves the starting cash assumption unclear.

**Recommended full-scope planning ask: $1.2M for 18 months**, conditional on actual compensation and supplier quotes:

| Use | USD | Purpose |
|---|---:|---|
| Team and specialist support | $450k | Explicit founder/technical lead compensation, employer costs, and contracted expertise |
| Fabrication and packaging | $300k | Two design/fabrication cycles with specified packaging scope |
| Lab, test access, and equipment | $180k | Shared facilities/rentals plus necessary instrumentation |
| Operations, IP, software, customer work | $90k | Distinguish legal/IP from basic operating overhead |
| Contingency | $180k | 15% reserve for respin, schedule slippage, or packaging rework |
| Total | $1.2M | $66,667/month average including reserve |

This is a budget proposal, not supplier-price evidence. Instrumentation access and data-transmission partner support must be confirmed. The seven-year model annualizes spending differently and is a scenario tool, not a reconciliation of this 18-month budget; replace its first two years with a monthly cash schedule before using it for fundraising.

If $750k is the practical fundraising limit, narrow the deliverable to a **12–15 month technical feasibility program** using shared lab access, lean founder compensation, and external partner transmission equipment. A possible allocation is $250k people, $220k fab/packaging, $100k lab/test, $65k operations/IP, $115k reserve. Do not retain all full-scope milestones merely by lowering salaries. If confirmed costs make this scope impossible, increase the raise or reduce the experiment.

Use milestones from financing close, with a fallback if the first fabrication does not work:

1. M0–3: committed technical owner; foundry process and packaging quotes; written interface requirements from at least two prospects. Select wavelength band/grid and quantify required per-line power at the delivered interface.
2. M3–6: tapeout/test plan and initial process characterization. Do not promise first soliton before confirmed fabrication turnaround.
3. M6–9: characterized comb generation and usable-channel spectrum; compare measured optical and electrical power with the complete baseline.
4. M9–12: packaged alpha with automated acquisition and recovery; proposed acceptance targets of 24-hour operation and at least 95 successful cold starts in 100 attempts under defined conditions. These are new targets, not current results.
5. M12–18: independent evaluation against a written specification; transmission on the required grid; second design cycle if necessary; paid evaluation or a design agreement specifying what must be achieved before production procurement.

An aggregate 1 Tbps demonstration can mean, for example, 40 usable channels × 25 Gb/s/channel. Specify BER, modulation, receiver, FEC overhead, temperature, run duration, and whether all channels transmit simultaneously. A spectrum containing 50 visible lines does not prove 50 useful communication channels.

Start the next raise sufficiently before cash depletion, provisionally M10–12 for an 18-month plan. Replace “raise $10M at M18” with “finance qualification and pilot production after measured alpha performance and customer evaluation.” Determine the next round from its work packages; $3–5M is a planning sensitivity, not a promised funding outcome.

## 4. Main-deck numerical and technical corrections

| Location | Finding | Necessary correction |
|---|---|---|
| Lines 38–50, problem | 50% data-movement power is architecture-specific; 64 lasers costing $3.2–6.4k, 1,000 mm², and 10–20W have no matched source | Name the actual incumbent product and system boundary. Do not generalize chip-wide power to source power |
| Lines 47, 66–75 | 64 wavelengths need not mean 64 separately packaged lasers or fibers | Compare arrays/modules and per-fiber wavelengths; acknowledge multiplexing and multi-port distribution |
| Lines 78, 111, 150, 226, 246 | “Cost” varies across $500–2k, $1–3k, and $3–5k | Separate customer ASP, delivered COGS, prototype expense, die cost, and production volume |
| Lines 112, 151 | mW microcomb power and 1W module power are not interchangeable | Show optical pump input, usable output, and total electrical wall-plug draw including stabilization/amplification |
| Lines 150–155 | Improvement arithmetic cherry-picks bounds | $2–5k/$1–3k permits 0.67–5x, not a demonstrated 2–3x. 100/16–32 is 3.1–6.25x. Bandwidth ranges permit 2.5–10x, not a fixed 5x |
| Lines 162–166, 256 | $10/line uses a $1k figure; actual $3–5k ASP/100 lines is $30–50/line | At a $125 baseline, that is 2.5–4.17x, not >10x. At 50 useful lines it is $60–100/line |
| Lines 152, 246–248 | Bare chip size is compared with packaged incumbent size | Compare packaged source modules including pump, control, filtering, amplification, and connectors |
| Lines 172–198 | Drop-in integration and unchanged packaging are unproven | Reframe as designed for integration pending band/grid, power, noise, coupling, recovery, and qualification validation |
| Lines 209–229, 431–432 | $10B × 20% = $2B is correct arithmetic; segment and market figures are unsupported and TAM varies | Build annual source SAM from system shipments × sources/system × realizable source ASP; separate it from full interconnect TAM |
| Lines 233–235 | Gen 3 requiring 50–100 wavelengths is unsupported | Obtain an actual roadmap requirement rather than extrapolating from the technology's maximum line count |
| Lines 271–285 | A single PID, tuning, and foundry access are described as solved challenges | Identify experimental status, failure modes, and the technical team accountable for resolving them |
| Lines 390–410 | Advisor expertise does not establish execution capacity | State advisor commitment accurately; recruit or commit a technical lead experienced in combs, packaging, and testing |

Ayar's current SuperNova page specifies up to 16 wavelengths per fiber across 16 fibers, supporting 256 data channels; the incumbent is already a compact multi-wavelength module. It advertises reliability qualification as well. Therefore “64 fibers/waveguides for 64 lasers” is not a generally valid comparison. [Ayar SuperNova](https://ayarlabs.com/supernova)

Lightmatter's Guide source is specified at up to 16 wavelengths/fiber, 16 fiber outputs, and a 200 GHz grid. Its Hot Chips 2025 spectrum is in the roughly 1,300–1,320 nm O-band, whereas the appendix proposes 1,520–1,580 nm. That prototype is not automatically compatible with Guide's architecture. Ayar and Lightmatter have source solutions; treat them as possible collaborators, competitors, or buyers only according to actual discussions. [Lightmatter, Hot Chips 2025, slide 17](https://lightmatter.co/wp-content/uploads/2025/08/57-lightmatter_hotchips_2025_final.pdf)

The most important technical diligence is delivered power per usable line and port. Illustrative calculation, not a specification: 64 channels × 1mW delivered requires 64mW usable comb power. At 5% usable pump-to-comb conversion and 50% output transmission, that requires 2.56W optical pump power. At 20% pump wall-plug efficiency it consumes 12.8W electrically before controls. Supplying the same power on 16 output fibers multiplies the optical demand by 16 unless another architecture changes the budget. A 1W total-module claim therefore needs explicit efficiency, per-port power, loss, and amplification evidence. High conversion efficiencies exist in some architectures; ordinary bright-soliton behavior cannot simply inherit their results. [Kerr-comb efficiency review](https://www.nature.com/articles/s44310-024-00030-9)

Published turnkey soliton operation predates this company. The foundational mechanism and the existence of automatic startup are not proprietary differentiation. Explain what is novel and owned: a particular efficiency/stability architecture, process-tolerant design, packaging, controls, or customer integration supported by actual know-how and IP rights. [Integrated turnkey microcombs](https://arxiv.org/abs/1911.02636)

## 5. Appendix audit

The first sales-planning section is useful after removing categorical buyer claims. “Hyperscalers don't buy components,” “minimum orders in millions,” “Ayar/Lightmatter WILL buy,” and “no alternative above 32 wavelengths” are not established facts. Evaluate each named account's make/buy strategy. Licensing fees of $2–10M and royalties of $50–500 are unvalidated deal ideas; omit them from the base forecast. License/NRE fees are not recurring product revenue, and hypothetical license, supply, and acquisition paths must not be added together as concurrent revenue.

The appendix's manufacturing margin range is wrong at its upper bound: $500–1,000 COGS and $2–4k ASP allow 50–87.5% gross margin, not 50–75%. That still does not validate either cost range. Specify yield, packaging/test scrap, pump, amplifier, electronics, warranty, and shipping. General customer support belongs in operating expenses unless properly attributable to delivery.

The dated Ayar example in lines 155–161 must be labeled hypothetical and converted into relative dates. It currently reads like an actual 2025–2027 pipeline and conflicts with the deck's fabrication schedule. No partnership should be implied from a target-company logo or name.

The AI/retina sections contain errors sufficiently material to damage confidence in the interconnect pitch:

| Appendix location | Correction |
|---|---|
| 204–236, ring timing | With group index 2, a 100µm-diameter ring has ~2.1ps round-trip time and ~477GHz FSR; a 500µm-diameter ring has ~10.5ps and ~95.4GHz. Approximately 100GHz spacing needs ~477µm diameter, not a 100µm ring. Use FSR = c/(n_g π D) |
| 249–282, accelerator | 450W/1W is a power ratio, not energy-efficiency improvement at different throughput. Using its own numbers, 100 Gpixels/s at 450W is 4.5nJ/pixel, versus 10 Gpixels/s at 1W = 0.1nJ/pixel: 45x. Against 1 Gpixel/s at 5W = 5nJ/pixel, it is 50x. None is a measured application comparison |
| 255–275, throughput | 10Gb/s serial input provides only 1.25Gpixels/s at 8 bits/pixel, before overhead. Eight 8-bit 10GS/s outputs require 640Gb/s raw readout, before interface overhead; a complete system <1W has no supporting power budget |
| 269–275, network | An 8×8 MZI matrix is not by itself a 784-input, multilayer MNIST classifier. Specify tiling, data loading, weighted accumulation, nonlinearities, retraining/calibration, and movement between layers. An MZI mesh transformation is not automatically an arbitrary unconstrained real-valued neural weight matrix |
| 325–335, demo | 96.3% accuracy, 100ns, and 0.8W appear as displayed results without experiments. Mark them as hypothetical, or remove them. 450/0.8 = 562.5x power ratio; 10ms/100ns = 100,000x latency ratio is arithmetically correct but unsupported as a matched benchmark |
| 365–408, architecture | Photodetection creates an electrical signal. Detector-to-modulator encoding includes electronics and electrical latency/power; the claimed absence of an electrical bottleneck does not follow |
| 390–394, 4K bitrate | 3840×2160×120×12-bit monochrome = 11.94Gb/s, so ~12Gb/s is possible with that explicit assumption. At 24-bit RGB it is 23.89Gb/s, excluding transport overhead |
| 472–496, frame rate | Detector GHz bandwidth does not establish GHz full-frame sensing. Exposure/photon budget, noise, driver/readout bandwidth, and classifier timing matter. A 1GHz/pixel later specification also does not establish 10Gframes/s |
| 485–486, ADC | A bandwidth mismatch does not prove a literal 90% loss of useful information; it depends on signal spectrum and sampling/aliasing. ADCs above 1GS/s exist |
| 500–510, idle power | No scene change does not turn off CW pumping, thermal tuning, or control electronics. Quantify standby power, wake-up energy, recovery time, and duty cycle |
| 588–617, 840–843, fabrication | SiN combs, fast modulators, and Ge detectors are not an automatically available single MPW stack. Confirm exact PDK/process options; quote cost and turnaround for that stack, including packaging |
| 623–632, coupling | A detector electrical output cannot connect to an optical input via a fiber connector alone; the electrical driver/E–O modulator path is required |
| 664–667, vehicle benefit | 384W saving cannot establish +20 miles range without trip time, battery, and Wh/mile. Replacing 50ms latency with 1µs saves ~49.999ms, inconsistent with “0.1ms faster.” Sensing-to-decision latency also excludes vehicle actuation |
| 670–695, markets | 10M×8×$100 = $8B and 100k×$50k = $5B are correct products of assumed inputs. The latter is installed-base equipment value, not annual revenue; vehicle volumes/adoption and inspection savings are unsupported |
| 689–691, defect performance | 99.99% detection and $1M/line savings require a dataset, test methodology, false-positive cost, and operating economics |
| 759–760, 854, novelty | “Nobody doing this” and “world's first” require prior-art and competitor research. They cannot be concluded from this appendix |

Analog Devices offers a 10.25GS/s ADC, directly contradicting the asserted general 1GHz ADC ceiling; this is an example, not the power estimate for your proposed electronics. [AD9213 specifications](https://www.analog.com/en/products/ad9213.html)

Foundry integration capability is evolving: LIGENTEC publicly describes SiN, TFLN modulators, and InGaAs detector integration. That is not confirmation of the appendix's Ge-on-SiN stack, availability in a selected MPW, or simultaneous suitability for combs and the proposed accelerator. Obtain a written foundry scope and quote. [LIGENTEC technology](https://www.ligentec.com/technology/), [LIGENTEC platform history](https://www.ligentec.com/about-our-story/)

## 6. Cleaner story and replacement slide text

Use roughly 11–12 core slides: customer problem; first product and interface; current proof; matched baseline economics; differentiation and IP; beachhead customer/use case; bottom-up market; design-in and qualification path; business model/scenarios; technical milestones; execution team; raise/use of funds. Move frequency-comb tutorials, the CW explanation, and detailed stability physics into a technical appendix.

Suggested opening:

> We are developing a packaged multi-wavelength source for optical interconnect designers. A single pump-driven microcomb could reduce the cost and complexity of supplying many wavelengths, if we can meet required per-channel power, stability, reliability, and integration specifications. This round funds a customer-specified alpha and independent evaluation.

Suggested economics slide:

> Target evaluation-module ASP: $5,000. Illustrative production ASP: $3,500 at 2,500 annual units, declining toward $3,000 at scale. Target delivered COGS: $1,575 at 2,500 annual units, or 55% gross margin; subject to supplier quotes, yield, and measured optical architecture. Base planning case: $8.75M year-five revenue; upside: $24.5M. These are conditional operating scenarios, not contracted demand.

Suggested funding slide:

> Seeking $1.2M to finance 18 months of design, two fabrication/packaging cycles, automated alpha operation, and independent customer evaluation, including a 15% contingency. Next financing funds qualification and pilot production after measured technical and customer milestones.

For the $750k version, replace both the duration and deliverables using the narrower feasibility scope above. Do not present both asks as one interchangeable plan.

Before a serious investor discussion, the highest-value evidence is: a committed technical execution lead; process/packaging/lab quotations; an honest measured-versus-simulated results page; two prospect specifications and their actual evaluation status; a line/port power budget; a delivered-Cost BOM with yield sensitivity; ownership of design/control IP; and a monthly cash plan showing what happens after a failed first fabrication. Without these, increasing the sales or acquisition numbers makes the pitch less credible.

## Companion files and limitations

- `soliton_PD_financial_model.py`: editable operating assumptions and dilution sensitivities; regenerate with Python 3.
- `soliton_PD_projection_scenarios.csv`: seven-year operating scenarios and simplified capital requirements.
- `soliton_PD_investor_returns.csv`: $6M/$8M/$10M post-money cap sensitivities, 40%/60%/80% ownership retention, and $30M–1B exit equity values.

No probability weights are assigned because the documents do not support them. No discounted expected exit valuation, legal SAFE conversion model, preference waterfall, or verified company valuation is provided. The delayed case assumes the product eventually works; a technical-failure or no-design-win case can return zero. Cash opex is a planning input, not GAAP EBITDA, and taxes are omitted. The originals remain unchanged so the review can be assessed before rewriting the pitch.
