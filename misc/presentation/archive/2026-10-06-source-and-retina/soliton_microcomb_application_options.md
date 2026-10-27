# Soliton microcomb: application options for a first product

6 October 2026. The founder wants the soliton microcomb to remain central to the product. The recent passive camera-preprocessor discussion does not satisfy that aim. This document compares applications before another presentation rewrite. Existing source-module and retina forecasts remain unvalidated alternatives, not approved projections for the selected business.

## What is useful in the original soliton_PD.tex

The title and solution slides supply the clearest technical premise: one CW pump drives a microresonator that generates many regularly spaced optical lines. The first architecture uses an external pump; later pump integration is optional. The technical challenges—startup/stability, packaging, and manufacturing variation—remain relevant across applications.

The most useful development sequence is chip fabrication → measured comb → automated operation → application test → customer evaluation. The initial customer should help define the requirements before fabrication, since line spacing, band, output power, noise, and tuning differ among applications.

The interconnect idea remains technically legitimate. The overstatements about discrete lasers, universal drop-in replacement, module power, cost, and guaranteed acquisitions should not be restored. The original deck is a source-module proposal, not evidence that it supplies an entire optical link or processor motherboard.

The optical motherboard is a longer-term direction: the source might eventually feed a photonic interconnect demonstrator between two devices. Building a CPU/GPU/memory fabric entails electronics, modulation, receiving, protocol and packaging responsibilities well beyond a first source chip. It should not be a $750k delivery promise.

## Shortlist

| First application | Why the comb is useful | First demonstration | Main unresolved burden |
|---|---|---|---|
| Programmable RF filter | Each comb wavelength provides a weighted, delayed copy of the input; many taps from one source | A small multi-tap filter with measured frequency response and tuning | RF modulator, delays, usable optical power, fast detection, linearity/noise, and comparison with existing RF filters |
| Parallel coherent ranging | Several coherent wavelengths provide parallel ranging channels | Several simultaneous distance measurements on a controlled target | Chirp control, optics/return power, receiver, calibration, and full-system cost |
| Multi-wavelength interconnect source | Each useful line is a data carrier | Transmission on customer-required wavelengths | Output power/ports, noise, band/grid compatibility, qualification, and incumbent alternatives |
| Narrow photonic convolution processor | Wavelengths provide parallel weighted operations | One defined filter/convolution on high-rate inputs | Data encoding, weight control, delays/readout, precision, and practical advantage over electronics |

These are engineering options. No verified sales price, customer commitment, market size, or successful financing probability is assigned to any of them.

## A. Programmable RF filter — closest to the adjustable-weight idea

Working arrangement:

`CW pump → soliton microcomb → RF input modulator → wavelength weights and delays → fast photodetector → filtered RF output`

Different wavelengths carry copies of the RF input. Applying different weights and delays lets their detected combination form a filter response. Weights without delays would generally not establish the desired frequency-selective filter. Signed taps require the appropriate modulation/detection architecture; positive optical powers alone do not implement arbitrary signed coefficients.

Published soliton-microcomb RF filters demonstrate the mechanism. Some laboratory implementations use fiber delay and amplification, so the paper does not imply a compact finished product. [Reconfigurable radiofrequency filters based on versatile soliton microcombs](https://www.nature.com/articles/s41467-020-18215-z)

Proposed starting scope: an 8–16-tap laboratory prototype using a custom comb chip and available external modulator/detector hardware, then a plan to reduce delay and control hardware. Those counts are proposed scope, not a performance guarantee or a vendor quote.

Measure passband shape, tuning range, rejection, linearity/dynamic range, noise, drift, and electrical power. Select a specific RF band and buyer problem before layout. This approach is most interesting when wide bandwidth or filter flexibility is difficult for the current electronics; it is unlikely to beat inexpensive electronics for low-rate camera triggers merely because the optical operation is fast.

My assessment: a good candidate if the founder wants a microcomb plus trained/adjustable optical weights with a manageable input-output demonstration. Its commercial case depends on finding a buyer with an actual RF-processing gap. It is not automatically the most fundable option.

## B. Parallel coherent ranging — closest to a comb-based sensing product

Working arrangement:

`Chirped pump / comb source → several wavelength measurement channels → target → coherent receiver → distance and possibly velocity results`

Published work demonstrates soliton-microcomb parallel coherent ranging. The key benefit is several measurements in parallel, rather than an ordinary camera image being classified by a passive mask. [Massively parallel coherent laser ranging using a soliton microcomb](https://www.nature.com/articles/s41586-020-2239-3)

Start with a few simultaneous measurement points on a controlled target, not a full automotive scanner or integrated optical phased array. Receiver architecture determines whether multiple detector channels or a dual-comb arrangement are appropriate. Chirp behavior, channel calibration, return-light collection, and electronics are substantial work beyond comb generation.

An industrial dimensional/speed measurement use case is worth investigating because the task can be narrow and accuracy/sampling requirements explicit. This is a customer-discovery suggestion, not proven willingness to pay. A doorbell normally has no need for high-rate parallel ranging; the application must justify the extra source and optics.

My assessment: the strongest conceptual alternative if the founder wants the microcomb to enable sensing directly. It is more complex than the first RF-filter bench setup and should be scoped with a ranging specialist and equipment access.

## C. Interconnect source — retain if there is a real integration opportunity

The original product scope makes sense when a customer can specify required wavelengths and output power. Comb lines act as optical communication carriers; the circulating soliton is not itself the data packet. This is established in published microcomb communication work. [Microresonator-based solitons for massively parallel coherent optical communications](https://www.nature.com/articles/nature22387)

The first module should demonstrate a useful number of simultaneous channels under a realistic link budget. That is a narrower contribution toward an optical motherboard. It need not develop processors or a complete board.

My assessment: this offers the most continuity with the original deck and a relatively clear component-selling model. Choose it if there is credible access to an optical-engine customer and a requirement the incumbent sources do not meet economically. Do not call it differentiated solely because it generates many wavelengths.

## D. Photonic convolution — keep the comb, but narrow the compute task

Microcombs have been used for parallel photonic convolution with stored weights. The optical source supplies multiple channels used for computation, giving a genuine role for the comb and a connection to partly adjustable weights. [Parallel convolutional processing using an integrated photonic tensor core](https://www.nature.com/articles/s41586-020-03070-1)

A prototype could implement one filter or feature operation rather than a full camera classifier or multilayer neural accelerator. For ordinary scene images, sensing and electro-optic encoding may add enough cost/power to erase the processing benefit. High-rate signal inputs are a more promising hypothesis, subject to benchmarks.

My assessment: appropriate if the founder's main goal is photonic processing, but a generic AI accelerator pitch is too broad. The initial scope must specify task, input rate, accuracy, precision, and the complete electronic baseline. A visually impressive demo does not establish favorable energy per inference or customer value.

## Other legitimate uses that are not my initial recommendation

Dual-comb spectroscopy and low-noise microwave generation also use properties of microcombs. They impose specialized requirements: spectroscopy needs an appropriate absorption band, line sampling, calibration, and sometimes frequency conversion; microwave generation needs competitive phase noise and stability. They are not simple applications to add to a general-purpose prototype without domain expertise. [Microcomb mid-infrared dual-comb spectroscopy](https://www.nature.com/articles/s41467-021-26958-6), [high-speed tunable microwave-rate soliton microcomb](https://www.nature.com/articles/s41467-023-39229-3)

## Choosing a product and budgeting the raise

The closest fit to the founder's adjustable-weight idea is a programmable RF filter; the closest fit to comb-based sensing is parallel coherent ranging; the closest fit to the original deck is an interconnect source. Select one for the first funded application, rather than financing all three.

For each candidate, identify: the buyer's present implementation and deficiency; the measured outcome needed; the proposed chip and external hardware; fabrication/packaging/test quotations; and the team capable of doing that work. The founder's $100–300k fabrication estimate remains unverified and does not alone determine the full application prototype cost.

An application does not create an investment case merely by being attached to a published source. The company-specific work should produce a useful implementation advantage, manufacturing/control know-how, customer evaluation, and a credible sales route. The $750k raise should purchase those milestones as well as the chip.

If the first objective is definitely a dissipative Kerr soliton, choose the design and acceptance tests accordingly. Different applications can also use dark-pulse, soliton-crystal, electro-optic, or other comb architectures; do not import their efficiency or other reported performance into a bright single-soliton design. The final product must beat alternatives on the buyer's requirements.

No presentation PDF has been rebuilt while the first application is being selected.
