---
# DRAFT OUTLINE. The SubScout story.md format is not final; front matter and blocks below follow
# the planned syntax and will be updated when the spec lands. No numbers are real yet:
# every {{ ... }} expression is a placeholder to be computed from data at build time.
title: Pinpricks and Echoes
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
## The whole shelf, and every well ever drilled into it
Show the basin at true scale with every wellbore as a dot sized to its real diameter. At that scale
the wells all but vanish. They have sampled {{ wells.sampled_area_share | pct | about }} of the area.
*Device: wellbores at true scale; zoom from basin to a single well.*
*Confidence: Derived (geometry from public well positions and bit sizes).*
:::

::: step {beat=observation}
## What a well actually sees
A composite log: gamma ray, resistivity, density and porosity tracks against depth. Rich detail, but
only along one line, and only centimetres either side of it.
*Device: composite log. Language: these are Observed.*
:::

::: step {beat=echo}
## Seismic is an echo, not a photograph
Wiggle traces: reflections recorded in two-way travel time, not depth. Show vertical resolution
(features thinner than roughly a quarter wavelength blur together) and what that hides.
*Device: wiggle-trace section. Language: the data is Observed; what it means is Interpreted.*
:::

::: step {beat=tie}
## Tying the pinprick to the echo
A well tie: the log converted to a synthetic seismogram and matched to the real traces. This is
where observation and interpretation meet, and where the first judgement calls are made.
*Device: well tie, with the log and seismic side by side.*
:::

::: step {beat=interpretation}
## Same data, different answers
Several interpreters pick the same horizon on the same seismic. Their surfaces agree near the wells
and diverge away from them.
*Device: overlaid picks; spread grows with distance from wells. Language: Interpreted.*
:::

::: step {beat=depth}
## From time to depth, the uncertainty compounds
Converting time to depth needs velocities, which are themselves uncertain. One horizon becomes a
fan of possible depths, and the trap's size changes with it.
*Device: depth-conversion fan; map with a "cut the map" cross-section.*
:::

::: step {beat=volumes}
## The number people quote
Uncertainty in area, thickness, porosity and fluid content carried through to recoverable volume:
P90 {{ prospect.p90 | volume }}, P50 {{ prospect.p50 | volume }}, P10 {{ prospect.p10 | volume }}.
In this convention P90 is the low case.
*Device: P90/P50/P10 range bar and exceedance curve. Confidence: Interpreted.*
:::

::: step {beat=test}
## The test: drilling
Pre-drill prediction against the post-drill result, for one well and then for many. How often were
the predictions right, and how far off were the misses?
*Device: claim → test → reveal. Confidence: Observed outcomes vs Interpreted predictions.*
:::

::: step {beat=therefore}
## How to read a subsurface claim
Three words: Observed, Derived, Interpreted. Ask which one you are looking at, what it was compared
with, and how wide the range is. Confident about the mechanism, explicit about the uncertainty.
:::

::: appendix
How we know: sources, methods, the numbers ledger, declared exceptions.
:::
