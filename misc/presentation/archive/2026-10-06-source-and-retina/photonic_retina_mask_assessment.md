# Compact photonic retina: trained optical mask and detector

6 October 2026. The founder describes a simple photodetector, an ML-designed semi-tunable mask on the chip, and optical preprocessing for doorbell or Flock-style cameras. The founder has confirmed that the intended mask is an on-chip optical circuit with partly adjustable weights. A fabricated free-space mask is therefore a related alternative, not the chosen concept. Input coupling, detector placement, circuit topology, and output task remain to be specified.

## Product framing

> We are developing a compact optical preprocessor for battery-powered cameras. A trained optical mask transforms incoming light before detection, producing a small number of signals that can help the camera decide when to wake or which image features to process. The first prototype will test whether this reduces total camera energy without missing useful events.

This describes optical preprocessing with detector/electronic readout. The optical computation can be passive or partly tunable; sensing, tuning, threshold decisions, video recording, and communications may still use electronics. A useful product does not require all of these functions to be photonic.

## First architecture hypothesis

For the confirmed adjustable-weight circuit, the current working architecture is:

`Scene → collection optics → several spatial optical inputs → weighted optical circuit → one or a few photodetectors → small readout circuit → camera wake/feature signal`

Spatial information must be preserved up to the weighted circuit. A single detector before it measures an electrical scalar; a single waveguide collecting all scene light also does not preserve an arbitrary image vector without an explicit encoding method. The input optics/couplers are part of the product, not incidental packaging.

Partly adjustable weights can mean most weights are fixed after training, with a small number of adjustable settings for calibration or installation. Specify which weights can change, their physical mechanism, tuning power, range, update rate, and drift. A coherent interferometer mesh cannot simply inherit its usual coherent-vector behavior under unrelated incoherent scene inputs. For mutually incoherent inputs, a passive linear optical circuit maps input intensities through power-transfer coefficients; reproducing a desired signed or nonlinear ML computation may need additional architecture, balanced readout, or electronic processing. The initial model must reflect the illumination actually used.

The mask/metasurface version discussed below is retained only for comparison:

`Scene → collection optics → trained optical mask/chip → one or a few detector outputs → small readout circuit → camera wake/feature signal`

Preserve an ordinary imaging path if the product must record recognizable video or read license plates. A low-dimensional feature output is not equivalent to an image. The ordinary path could be separate or share optics, but splitting light reduces the photons available to each branch and must be measured.

If a photodetector is placed before the optical processor, it converts the scene into electrical signals and requires modulation to feed another optical stage. If the aim is to process scene light directly, put the trained optical transformation before the final detector.

The previous microcomb architecture is not assumed necessary. Passive processing of natural scene light can be investigated without a soliton source. A comb is justified only if the chosen encoding and processing method actually needs it and the complete power/cost comparison favors it.

## What “ML mask” can mean

Training software optimizes an optical element for a specific task. The fabricated element performs a physical transformation; software training alone does not make it a full multilayer nonlinear neural network. Define whether the mask modifies amplitude, phase, polarization, spectrum, or several of these.

Outdoor scene light is broad-spectrum and largely spatially incoherent. A design simulated with a coherent laser cannot automatically be transferred to a doorbell. Model spectral response, illumination, angular range, photon loss, detector noise, and realistic object variation. Static optical transformations are often limited in the functions they realize without nonlinearities or later processing; optical-intensity readout adds its own measurement behavior.

A single photodetector generally produces one scalar measurement at a time. This can support a learned score or trigger, but rich multi-feature output needs multiple detector channels, temporal measurements, or another encoding mechanism. A single fixed weighted score should not be presented as complete person recognition or license-plate decoding.

Specify limited tuning concretely: calibration for temperature/installation, a few switchable task masks, or adjustable optical weights. These have different fabrication and control requirements. A passive fixed mask consumes no electrical power for its transformation, but tuners, detectors, readout, illumination, and the rest of the camera can consume power. Avoid a zero-power-system claim.

## Relevant prior work

- [Optical machine learning with incoherent light and a single-pixel detector](https://arxiv.org/abs/1904.10851) investigates a programmable single-pixel framework for linear pattern recognition under incoherent light. Its specific measurement scheme must not be assumed to be a single static mask performing unrestricted classification.
- [Image sensing with multilayer, nonlinear optical neural networks](https://arxiv.org/abs/2207.14293) demonstrates optical image preprocessing and compressed outputs under incoherent light, using a commercial image intensifier for nonlinear activation. The nonlinear component is additional hardware, not a property automatically supplied by a mask.
- [Optical metasurfaces for general vision processing on the edge](https://www.nature.com/articles/s41586-026-10635-z) describes a metasurface optical front end with a digital back end for real-scene tasks. This is related evidence, not proof of the proposed compact device's cost or power.

These establish that the broad direction is technically serious and already researched. Differentiation must come from the chosen task, manufacturable implementation, robustness, integration, and measured camera-level benefit.

## Camera economics: plausible reasons to buy, not validated demand

| Application | Potential benefit | Necessary comparison |
|---|---|---|
| Battery doorbell | Fewer unnecessary camera/processor/radio wakeups, longer battery life | Existing camera plus its current motion/person detection, including standby power and missed events |
| Solar-powered roadside camera | Lower average power, smaller power system, fewer irrelevant captures | Current trigger/capture pipeline at the same required capture rate and nighttime conditions |
| Camera feature preprocessing | Fewer sensor outputs or less electronic work for a narrow task | Complete optical/readout path versus an electronic preprocessor, while preserving useful image information |

Ring already offers motion detection and video at comparatively low consumer prices; its current product page includes advertised offers as low as $39.99. Those are retail promotions, not OEM component budgets. A component cannot assume a large selling price merely because the end camera has valuable features. [Ring lineup](https://ring.com/video-doorbell-cameras)

Flock describes solar-powered, motion-activated cameras that identify vehicle details and capture plate images. That suggests a power-limited use case, but not an established gap in the existing triggering system or a buyer commitment. A lossy optical transformation that destroys plate detail would be unsuitable as the only imaging path. [Flock system description](https://resources.flocksafety.com/meetflock/)

For either customer type, speed is valuable only if current latency causes a real problem. Nanosecond optical propagation is not by itself a purchasing reason for a video camera. Photon collection, detector integration, wakeup, and image capture can dominate the useful response time.

### Illustrative economic checks

System saving must be calculated as avoided sensing/processing/communications energy minus added optical-readout/tuning energy, including any changes in illumination or exposure. If a preprocessor prevents wakeups, measure their rate and energy under realistic traffic, rather than assuming that the main camera was continuously active.

At an assumed electricity cost of $0.20/kWh, saving 1W continuously saves only $1.75/year. Battery life, maintenance, false alarms, or a smaller solar system may therefore be more valuable than electricity cost alone. This is arithmetic using hypothetical inputs, not a measured product saving or an electricity-price benchmark.

Illustrative supplier sensitivity: at a $10 component selling price and $5 delivered cost, each unit contributes $5 gross profit. Producing $750k of gross profit requires 150,000 units, before ongoing operating expenses. At $30 price and $15 cost, it requires 50,000. Neither price is an established customer willingness to pay; these examples show why low-priced camera components need meaningful volume and OEM access.

## What should precede a $100–300k chip commitment

Train and simulate the mask using real target scenes and lighting variation. Build an optical bench prototype with available mask/display and detector hardware when practical. Compare it against an existing inexpensive electronic trigger or classifier. Show a path from the bench optics to the intended compact stack and quantify transmission/alignment tolerances.

This can establish whether expensive custom fabrication is justified. The founder's fabrication estimate remains an input to quote, not a validated cost for every architecture. A trained diffractive mask/metasurface and a programmable waveguide circuit need different suppliers and process options. Do not select a microcomb foundry solely because it was suitable for the previous interconnect concept.

## Fundraising implications

The $750k proposal can be framed as funding a trained optical preprocessor, compact integration, and camera-level testing if the full work plan and supplier quotes support that amount. Its first milestone should establish a useful task and realistic system-level advantage; later milestones can fund custom fabrication and OEM evaluation.

Keep the financial model tied to this product. The old multi-wavelength-source ASP, 2,500-module Y5 plan, $9–12M funding envelope, and acquisition sensitivities are not validated retina economics and should not be reused as such.

PDF rebuilding remains on hold. This assessment and `photonic_retina_product_brief.md` are working inputs for the replacement presentation; no coherent-laser, microcomb, rich-classification, or OEM-sales assumption is treated as confirmed.
