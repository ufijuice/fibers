# Consolidated Soliton pre-seed presentation

Prepared October 2026. `../soliton_PD.tex` is the source of current product scope. The older deck and one-pager supply founder/advisor context and the long-term research direction; their earlier commercial scope, market totals, and funding asks are superseded. All original files are preserved.

**Product clarification, 6 October 2026:** the founder intends to fund a compact photonic retina, rather than an interconnect light-source supplier. The existing PDFs and financial scenarios below reflect the earlier source-module scope and must not be presented as retina projections. See `photonic_retina_product_brief.md` for the root-paper review, revised product framing, and provisional fabrication-cost sensitivity. PDF rebuilding is on hold while the initial sensing architecture and fabrication scope are clarified. The slide-16 paragraph-spacing fix is in the TeX source but has not yet been compiled into a replacement PDF.

## Presentation files

- `soliton_preseed.pdf` / `soliton_preseed.tex`: 12 core slides plus seven diligence/research slides. Core presentation ends with the ask; appendix slides are for questions.
- `soliton_one_pager.pdf` / `soliton_one_pager.tex` / `soliton_one_pager.txt`: concise investor overview.
- `soliton_diligence_appendix.md`: evidence, specifications, financial assumptions, commercial risks, and research boundaries.
- `financial_model.py`: editable, dependency-free model; regenerates the three CSVs.
- `projection_scenarios.csv`: seven-year operating scenarios.
- `investor_returns.csv`: dilution and hypothetical exit sensitivities, for diligence rather than a promised exit slide.
- `preseed_monthly_budget.csv`: 15-month cash allocation, retaining $115k contingency.

## Decisions applied consistently

1. **Product:** packaged microcomb light source, rather than a complete interconnect, neural accelerator, or camera.
2. **Raise:** retain the current $750k pre-seed amount; narrow its duration and scope to 15-month feasibility. A fully costed 18-month expansion option remains in the diligence appendix, not as a competing headline ask.
3. **Technical gate:** 16 usable carriers at a customer-defined interface; 32–50 remains an expansion objective. Reaching 50 spectrum lines without useful delivered power is not acceptance.
4. **Commercial case:** independent source supplier; staged design-in and qualification; scenario-based unit revenue; no assumed acquisition price, date, or customer partnership.
5. **Research:** Photonic retina sensing/processing is included as a possible future application, and Hopfion computing as a longer-term direction. Both require separate experiments. It is excluded from the operating revenue and pre-seed work packages.
6. **Evidence:** public benchmarks establish context. Company-specific performance is not asserted where the provided documents contain no measured results.

## Before external circulation

Confirm USD as the intended currency, advisor engagement/public attribution, current technical-lead and laboratory arrangements, and any actual measured results or customer discussions that should replace conservative evidence-status wording. The presentation is complete as a development-stage pitch, but procurement quotations and customer evidence remain business inputs to obtain; they are not invented here.

The budget schedules $635k of core work and holds $115k reserve. Its category allocations and timing are planning assumptions, not procurement contracts. If quotations invalidate that scope, revise the work or financing amount before committing to the milestones.

## Build

From this directory:

```sh
python3 financial_model.py
pdflatex -interaction=nonstopmode -halt-on-error soliton_preseed.tex
pdflatex -interaction=nonstopmode -halt-on-error soliton_preseed.tex
pdflatex -interaction=nonstopmode -halt-on-error soliton_one_pager.tex
pdflatex -interaction=nonstopmode -halt-on-error soliton_one_pager.tex
```

The updated model is distinct from the earlier review model: first-year cash spending is now $450k to match the narrower feasibility budget. Its base-case second-year cash opex plus capex totals $1M, covering the final three pre-seed months and the following nine months financed by the next round. The first three months consume $185k of planned core spend; later activity depends on follow-on funding.

Annual projections are illustrative; the monthly schedule is authoritative for the initial 15-month raise. No cap table, legal financing offer, or probability-weighted valuation is implied.
