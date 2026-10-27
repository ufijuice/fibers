# Soliton microcombs for interconnects: application and product assessment

Research date: 6 October 2026. This is a product recommendation, not a validated sales forecast. Original soliton_PD.tex remains the reference for the founder's intent; the current presentation PDFs have not been rebuilt.

## Recommendation

Investigate a packaged external multiwavelength source for short-reach wavelength-division-multiplexed optical interconnects. Demonstrate it with a compatible transmitter and receiver rather than building an entire optical motherboard. Sell initially to optical-engine developers and module integrators; a processor company need not be the first customer.

The original deck's external CW pump, microcomb and automatic control are useful foundations. Its claims of a universal drop-in replacement, unchanged packaging, 100 useful wavelengths, 1 W total consumption and large cost savings are not established. A source is an important subsystem, but it does not itself supply modulators, receiver electronics, protocol handling or the full link.

## Applications and entry routes

| Application | What could be sold | Possible first buyer | Assessment |
|---|---|---|---|
| External source for on-board or near-package optical engines | Packaged pump, comb, wavelength conditioning, control and optical outputs | Optical-engine developer or module integrator | Best initial product boundary. Define one engine's wavelength and power requirements first. |
| External source for co-packaged switch optics | A serviceable source module outside the switch package | CPO subsystem supplier | Real industry architecture, but high power, qualification and incumbent competition make this a demanding first design-in. |
| Board-to-board links within an accelerator chassis | Initially a source plus evaluation link; later a complete link with a partner | Board/system developer through an optics partner | Useful demonstration of customer value. Full-link development adds electronics and protocol work beyond the source. |
| Accelerator-to-accelerator or accelerator-to-switch links across a rack | Source embedded in an optical-engine supplier's offering | Engine/module supplier | Strong application fit where many closely spaced wavelengths are actually used. Do not equate AI infrastructure spending with obtainable source revenue. |
| Shared source feeding several optical engines | Source and distribution subsystem | System or engine integrator | Potential packaging benefit; splitting reduces per-engine optical power and creates a shared failure point. Investigate after a single-engine link. |
| PCIe/CXL optical expansion and memory pooling | Source inside a protocol-capable link | Specialist bridge/link vendor | Longer-term application. Optical bandwidth alone does not solve latency, ordering, protocol compliance or memory coherency. |
| Complete optical motherboard or CPU/GPU optical chiplet | Full interconnect platform | Compute platform vendor | Too broad for the proposed first round. Requires much more than microcomb fabrication. |
| Conventional single-wavelength or four widely spaced wavelength links | Laser-source replacement | Transceiver supplier | Weak default comb case: many comb lines may go unused. Assess only against a concrete customer's requirements. |

These rankings are judgments about an early company's scope, not measurements of market size.

## Evidence that the external-source boundary is real

The OCI specification describes on-board, package and interposer implementations, with an external laser source feeding wavelength groups. Its basic 200G optical unit uses four wavelengths; channel counts must be tied to the selected engine rather than assumed from a broad comb spectrum. [OCI specification, March 2026](https://oci-msa.org/assets/files/200G-OCI-Optical-Phy-Specification-v1.0.pdf).

External light sources can be serviced separately from compute/switch packages. Lumentum announced an eight-wavelength DWDM ELSFP demonstration in September 2026, targeting initial availability in the first half of 2027. [Lumentum announcement](https://investor.lumentum.com/financial-news-releases/news-details/2026/Lumentum-to-Demonstrate-DWDM-ELSFP-Laser-Module-for-OCI-MSA-Applications-at-ECOC-2026/default.aspx).

This makes a module business plausible; it does not establish that a new comb is electrically, optically or commercially compatible. A standardized enclosure is only part of qualification. Wavelengths, output power, noise, polarization, reflections, startup, recovery, thermal behavior and management must match the buyer's requirements.

## Competition and differentiation

Enlightra advertises an ATLAS comb-based ELSFP for CPO: 8–32 lines per output, 100/200 GHz spacing, center wavelength 1290–1310 nm. Its existence is direct evidence of competing commercial intent; the page alone does not establish shipment volumes or customer qualification. [Enlightra products](https://enlightra.com/products).

Ayar Labs also markets an external source as part of its optical I/O offering. [Ayar Labs products](https://ayarlabs.com/products/). Lumentum provides a conventional-laser alternative. Neither should be represented as an assumed customer or partner.

Consequently, “microcomb for interconnects” is not sufficient differentiation. Candidate advantages to test are lower total electrical power at the same delivered power per usable wavelength, lower packaged cost at equivalent specifications, simpler assembly, or reliable autonomous operation with a useful customer-specific wavelength set. Select an advantage only after measuring it and comparing with a relevant alternative. A published physics result does not by itself establish proprietary product technology; rights, know-how and freedom to operate need separate investigation.

## Numerical corrections that matter

1. **Useful lines, not visible peaks.** Count channels that simultaneously meet power, grid, noise and temperature requirements at the output connector. Broad spectral coverage alone is not a product specification.
2. **Total module power.** Include pump wall-plug consumption, temperature control, controllers and any amplification. A millimetre-scale resonator or low optical pump threshold does not imply a milliwatt electrical module.
3. **Compare equal functionality.** Match wavelength count, delivered optical power, output ports, temperature range and reliability. Do not compare a bare comb die with a packaged laser subsystem.
4. **No automatic power saving.** Lumentum reports up to 24 dBm, roughly 250 mW, per wavelength across eight simultaneous channels with approximately 12 W module consumption. That is a demanding high-power comparator, not a universal requirement. Eight outputs at that stated per-channel level would total about 2 W of optical power, so a 1 W electrical source cannot supply equivalent outputs. [Lumentum announcement](https://investor.lumentum.com/financial-news-releases/news-details/2026/Lumentum-to-Demonstrate-DWDM-ELSFP-Laser-Module-for-OCI-MSA-Applications-at-ECOC-2026/default.aspx).
5. **Sharing has a power cost.** An ideal equal splitter feeding eight engines costs 9.0 dB per branch; sixteen costs 12.0 dB, before excess loss. More wavelengths do not remove this loss.
6. **Source savings are only part of link savings.** Illustratively, if the source accounts for 20% of link electrical power and its consumption is halved, total link power falls 10%. This is arithmetic, not a measured source share.
7. **Bandwidth belongs to the link.** Wavelength count times measured data rate per channel gives gross capacity; payload rate depends on coding and overhead. The source alone does not establish a Tbps product.

## A concrete pre-seed milestone

Choose one optical engine, supported spectral band and wavelength group. An 8–16-line goal could be an engineering starting point, not a claim that this count is the right commercial specification. O-band versus C-band is a consequential design decision; an available fabrication process must actually support the selected band, dispersion and loss.

Build a packaged source with an external pump and automatic startup/recovery, then demonstrate a simultaneous multiwavelength data link with a partner's engine. Compare against an appropriate laser source at equal transmitted data rate and delivered optical power. Report source and whole-link electrical power, bit-error performance, usable channels, stability and assembly cost separately.

Obtain an engine developer's written source specification and a credible evaluation route before committing to the first expensive fabrication run. Later commercial milestones are an accepted evaluation module, a design-in and qualification; lab delivery is not equivalent to production revenue.

The proposed $750k should be assessed as funding source fabrication, packaging, control and a partner-assisted link demonstration. The founder's $100k–$300k chip estimate remains unquoted and does not cover all packaging, pump, test equipment, staffing or redesign costs. No evidence currently validates $750k as sufficient for a production-qualified ELSFP, a complete optical motherboard or a new processor-integrated optical chiplet. Rebuild the budget from the chosen engine's requirements and partner access before changing revenue or exit projections.

## Proposed plain-language positioning

“We are developing a compact multiwavelength light source for optical links between computing chips and boards. A soliton microcomb generates the wavelengths from one pump laser. Our first aim is to test whether a packaged source can reduce the cost or power of supplying light to a compatible optical engine. The first prototype will demonstrate a working data link, with automatic source control.”

Once evidence exists, replace “test whether” with the measured benefit. Keep optical motherboards and broader computing architectures as later directions.
