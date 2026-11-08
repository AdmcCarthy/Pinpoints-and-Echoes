---
# DRAFT OUTLINE v2 (2026-11-08). The SubScout story.md format is not final; front matter and blocks
# below follow the planned syntax and will be updated when the spec lands. No numbers are real yet:
# every {{ ... }} expression is a placeholder to be computed from data at build time.
#
# Field-independent by design. The argument is about any field; Volve is the "receipt": a real,
# open case that shows each claim holds with real numbers. Each step has a Receipt line.
title: Pinpoints and Echoes
dek: >
  Every map of the subsurface is mostly inference. A handful of boreholes and the echoes of sound
  waves become a confident picture of rocks no one has seen.
arc: pre-drill-post-drill
register: section
palette: tide
type: ledger
units: sm3
status: placeholder
---

::: step {beat=hook register=outcrop}
## Every well ever drilled into the shelf
The basin at true scale, every wellbore a dot sized to its real diameter. At that scale the wells
all but vanish. Together they have sampled {{ wells.sampled_area_share | pct | about }} of the area.
*Device: wellbores at true scale, North Sea wide (Sodir). Confidence: Derived.*
*Receipt: none needed; this beat is the whole basin.*
:::

::: step {beat=ladder}
## A well, a field, a basin
Zoom in one rung at a time. A well is {{ well.diameter_cm | round:0 }} cm across; a field is
kilometres; the basin is hundreds of them. Decisions worth {{ decision.cost | about }} are made on
what sits between the dots.
*Device: three-rung scale ladder, each rung to the same ratio. Confidence: Derived.*
*Receipt: Volve, one field with {{ volve.n_wells | int }} wellbores, as a share of its own area.*
:::

::: step {beat=observation}
## What a well actually sees
A composite log: gamma ray, resistivity, density and porosity against depth. Rich detail, but only
along one line, and only centimetres either side of it. Every curve is also a measurement with its
own error.
*Device: composite log. Language: these are Observed.*
*Receipt: a Volve log, with the stated tool and depth reference.*
:::

::: step {beat=echo}
## Seismic is an echo, not a photograph
Reflections recorded in two-way travel time, not depth. Features thinner than roughly a quarter
wavelength blur together; the echo cannot see them, however good the processing.
*Device: wiggle-trace section; thin-bed wedge on a synthetic. Language: the data is Observed; what
it means is Interpreted.*
*Receipt: a Volve section at the reservoir; the synthetic wedge is labelled synthetic.*
:::

::: step {beat=tie}
## Tying the pinpoint to the echo
The log is converted to a synthetic seismogram and matched to the real traces. This is where
observation and interpretation meet, and where the first judgement calls are made.
*Device: well tie, log and seismic side by side.*
*Receipt: a Volve well tie from its check-shot table.*
:::

::: step {beat=error-stack}
## Every measurement is uncertain, and they stack
Where the well is (horizontal and vertical position), what depth means (which reference), how fast
sound travels, where the pick sits on the wavelet. Each is small alone.
*Device: a stack of error bars, one per link in the chain, then their combined spread at the target.
Confidence: Derived for each stated error; Interpreted for the combination.*
*Receipt: Volve's stated position uncertainty per well, the rotary-table reference, and the
disagreement between check-shot tables at the reservoir.*
:::

::: step {beat=interpretation}
## Same data, different answers
Several valid picks of one horizon. Surfaces agree near the wells and diverge away from them.
*Device: overlaid picks; spread grows with distance from the wells. Language: Interpreted.*
*Receipt: Volve's alternative horizons and its two processing vintages, with the real misfit to
well picks. States plainly that these are different surveys and folders, not blind interpreters.*
:::

::: step {beat=depth}
## From time to depth, the uncertainty compounds
Velocities convert time to depth and are themselves uncertain. One horizon becomes a fan of depths,
and the trap's size changes with it.
*Device: depth-conversion fan; "cut the map" cross-section.*
*Receipt: Volve horizons in time and depth against well picks.*
:::

::: step {beat=volumes}
## The number people quote
Uncertainty in area, thickness, porosity and fluid content carried through to recoverable volume:
P90 {{ prospect.p90 | volume }}, P50 {{ prospect.p50 | volume }}, P10 {{ prospect.p10 | volume }}.
In this convention P90 is the low case. The simulation is labelled as one.
*Device: P90/P50/P10 range bar and exceedance curve. Confidence: Interpreted.*
*Receipt: none; a worked, simulated example, not a Volve claim.*
:::

::: step {beat=test}
## The test: drilling
Predictions against outcomes, for one well and then for many. How often were they right, and how far
off were the misses?
*Device: claim, test, reveal. Confidence: Observed outcomes vs Interpreted predictions.*
*Receipt: only if a Volve prognosis is public (open question). Otherwise Sodir discovery
estimates against later reserves, or this beat is told from published industry studies.*
:::

::: step {beat=therefore}
## How to read a subsurface claim
Three words: Observed, Derived, Interpreted. Ask which one you are looking at, what it was compared
with, and how wide the range is. Confident about the mechanism, explicit about the uncertainty.
:::

::: appendix
How we know: sources, methods, the numbers ledger, declared exceptions. Acknowledgement of the
Volve data release and its terms.
:::
