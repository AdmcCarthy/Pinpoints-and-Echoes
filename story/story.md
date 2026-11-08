---
title: Pinpoints and Echoes
short_title: Pinpoints and Echoes
dek: Every map of the subsurface is mostly inference. A handful of boreholes and the echoes of sound waves become a confident picture of rocks no one has seen.
kicker: DRAFT · NORTH SEA · SODIR WELLBORES, VOLVE AS THE WORKED CASE
byline: Adam McCarthy
date: 2026-11-08
register: section
palette: tide
surface: nordic-cool
units: sm3
horizon: true
kpis:
  - { metric: n_wellbores, label: petroleum wellbores in the Norwegian North Sea }
  - { metric: hole_cm, label: "cm across at reservoir depth", filter: round:0 }
  - { metric: nn_km, label: "km to the nearest other exploration well (typical)", filter: round:1 }
sources:
  sodir:
    name: Sodir FactPages, wellbore table (Norwegian Offshore Directorate)
    note: Contains data under the Norwegian licence for Open Government data (NLOD) distributed by Sodir. Filtered, converted to wellhead positions and summarised by the author.
  volve:
    name: Volve data village, Equinor ASA and the former Volve licence partners
    note: Contains data from the Volve data village, © Equinor ASA and the former Volve licence partners (ExxonMobil E&P Norway, Bayerngas Norge). Used under the Volve Terms and Conditions. Generalised for display.
data:
  wells: data/wells.csv
  geometry: data/geometry.csv
  chain: data/chain.csv
  spread: data/spread.csv
  transect: data/transect.csv
  picks: data/picks.csv
---

This is a draft. The argument is about any field; the Volve data, which is open, is the worked case that
shows each claim holding with real numbers. Every number is computed from the data when the page is built
and listed in [Basis of analysis](#basis-of-analysis).

::: step {beat=hook register=outcrop}
### Every well ever drilled in the Norwegian North Sea

Here are {{ n_wellbores | int }} petroleum wellbores, drawn at true size on the area they span. You cannot
see them. At this scale each one is far smaller than a pixel, and together they have ever been a hole in
one part in {{ one_in | about }} of the area. Everything we know of what lies between them is inferred.

```chart
id: shelf
type: custom
module: figures/scale.js
data: [wells, geometry]
state: { mag: 1 }
title: At true size, the wells vanish
subtitle: Wellhead positions of petroleum wellbores, Norwegian North Sea, true size
source: sodir
confidence: derived
unit: km (area), cm (hole)
notes: Wellhead positions, not bottom-hole. The dashed outline is the convex hull of the wellheads, not the sea. Every wellbore counts, sidetracks included. Hole diameter is the Volve reservoir-depth median.
```
:::

::: step {beat=hook}
### Enlarge them and the gaps show

Each dot here is enlarged thousands of times so that you can see where the wells are. Between them is
rock sampled only by inference.

```chart
use: shelf
mag: 12000
title: Enlarged to be seen, the wells still leave the area empty
subtitle: Wellhead positions of petroleum wellbores, Norwegian North Sea, each enlarged by the factor stated below
```
:::

::: step {beat=ladder}
### A well is about {{ hole_cm | round:0 }} cm across, and the next is kilometres away

At reservoir depth a wellbore is about {{ hole_cm | round:0 }} cm across. The typical exploration well is
{{ nn_km | round:1 }} km from its nearest neighbour, in a range from {{ nn_p10 | round:1 }} km
to {{ nn_p90 | round:1 }} km. Divide one by the other and the gap is {{ spacing_ratio | about }} wellbore
widths.

```chart
id: ruler
type: custom
module: figures/ruler.js
data: geometry
state: { coin: false }
title: From a hole you could put a hand in to an area hundreds of kilometres wide
subtitle: Lengths on a logarithmic scale, metres to kilometres
source: sodir
confidence: derived
unit: m, km
notes: Distances use wellhead positions of exploration wellbores (initial bores, 100 m cells). Logarithmic axis, which departs from the linear-axis default; it is the only way to show both ends. Hole diameter is the Volve reservoir-depth median.
exception: { rule: linear axes, reason: the lengths span seven orders of magnitude }
```
:::

::: step {beat=ladder}
### Shrink the area until the wellbore is a coin

Redraw the same picture with the wellbore as a coin one centimetre across. The nearest well is then {{ coin_m | about }} m
away, and the area they span is a square {{ coin_span_km | about }} km across. A decision worth a great
deal of money is made on what lies in all that space.

```chart
use: ruler
coin: true
title: As a coin, the next well is a long walk away
```
:::

::: step {beat=error-stack}
### And every one of those measurements is uncertain

Where the well is. What depth means. How fast sound travels. Where a pick lands on the echo. Each link in the
chain has an error, and they stack. In Volve the horizontal position of a well is known to a median
{{ pos_h | round:0 }} m at the end of its survey, and up to {{ pos_h_max | round:0 }} m in the worst case. The
figure below follows the {{ n_links | int }} vertical links, one at a time.

```chart
id: stack
type: custom
module: figures/errstack.js
data: stack
state: { upto: 0 }
title: Small errors in each link add up at the target
subtitle: Vertical error at the reservoir, Volve. Solid bar typical, lighter bar largest on file.
source: volve
confidence: interpreted
unit: m
notes: Links are combined in quadrature, which assumes they are independent. The depth reference is a systematic offset, so the largest combined value is a bound, not a forecast. Time errors are converted to depth at the Volve average velocity. The Volve horizons shown are already adjusted to the wells.
exception: { rule: one hue per entity, reason: the combined row takes the highlight colour to set it apart }
```
:::

::: step {beat=error-stack}
### Where the bottom of the well is

The vertical position of a well is tied to a survey; its stated uncertainty is a few metres.

```chart
use: stack
upto: 2
title: A well's depth is known to a few metres
```
:::

::: step {beat=error-stack}
### What depth is measured from

A depth reference mixed up between the rotary table and sea level shifts every depth by the height of the
rig floor. It is a known trap, and it appears in the Volve record.

```chart
use: stack
upto: 3
title: The depth reference can shift every depth at once
```
:::

::: step {beat=error-stack}
### Time becomes depth through a velocity

Seismic arrives as two-way time. Converting it to depth uses velocities from check shots, and those ties
disagree with the picks by tens of metres in the worst case.

```chart
use: stack
upto: 4
title: Time to depth adds tens of metres of doubt
```
:::

::: step {beat=error-stack}
### The seismic surface against the well picks

Even after the horizons were adjusted to the wells, the surface at the reservoir misses the well picks by
metres typically and by about a hundred in the worst case.

```chart
use: stack
upto: 5
title: Even adjusted to the wells, the reservoir surface misses by metres
```
:::

::: step {beat=error-stack}
### The sum at the target

Typical errors combine to about {{ stack_typical | round:0 }} m at the target. The largest on file combine to
about {{ stack_worst | round:0 }} m. That spread is the honest width of the answer to "how deep is it?",
before a single interpretive judgement is made.

```chart
use: stack
upto: 6
title: Together, a range of metres to hundreds of metres
```
:::

::: step {beat=interpretation}
### Same data, different answers

Take one surface, the top of the Ty Formation, along a {{ line_km | round:1 }} km line between wells. At the
{{ n_picks_line | int }} well picks near the line (circles) the depth was observed; its time comes from a check-shot
table. Everywhere between them the surface is drawn by an interpreter, by software, or by both.

```chart
id: transect
type: custom
module: figures/transect.js
data: [transect, picks]
state: { stage: 1 }
title: Between the wells, the surface is drawn, not measured
subtitle: Ty Fm top along a line between two well picks, Volve, two-way time in ms (time increases downward)
source: volve
confidence: interpreted
unit: ms TWT, km
notes: Pick depths are Observed and their times Derived through the check-shot table; both surfaces are Interpreted. The two versions are the base survey (ST0202R08, PSDM) and the reprocessed survey (ST10010) as published in the Volve release; they differ in processing and in picking, so they are two published answers, not blind picks by different interpreters. Values are read at the nearest node, 50 m apart. Picks within 150 m of the line are shown at their along-line position.
```
:::

::: step {beat=interpretation}
### Two defensible answers

The base survey gives one surface and the reprocessed survey another. They agree on the broad shape and differ in the detail. Along this line they
differ by a median {{ gap_med_ms | round:0 }} ms and by up to {{ gap_max_ms | round:0 }} ms, which is up to about
{{ gap_max_m | round:0 }} m of depth at the Volve average velocity. Neither is wrong; each is a defensible answer. Neither passes through the picks: on average they miss them by
{{ miss_base | round:0 }} and {{ miss_repro | round:0 }} ms.

```chart
use: transect
stage: 3
title: Two defensible surfaces, and the gap between them
```
:::

::: step {beat=interpretation}
### Wells do not remove the disagreement

The textbook picture is that interpretations agree near the wells and part away from them. The Volve versions show
a weaker version of it. Within a quarter of a kilometre of a well pick the median difference is already
{{ near_lo | round:0 }} to {{ near_hi | round:0 }} ms, depending on the surface. Beyond two kilometres, where
{{ n_far | int }} of the {{ n_versions | int }} surfaces have enough nodes to compare, it is {{ far_lo | round:0 }}
to {{ far_hi | round:0 }} ms. The wells help; they do not settle it.

```chart
id: spread
type: custom
module: figures/spread.js
data: spread
title: The versions differ at the wells, and more away from them
subtitle: Difference between the base and reprocessed versions of four Volve horizons, by distance to the nearest well pick
source: volve
confidence: derived
unit: ms TWT
notes: Solid line is the median absolute difference at nodes 12.5 m apart, dashed line the 90th percentile. Bands with fewer than a thousand nodes are not drawn. Distance is to the nearest well pick of any interpreted surface. The Ty Fm top is a special case near wells because the official version was updated with the later F-11 wells. A systematic offset between versions is included, not removed. Two published versions are not two independent interpreters.
exception: { rule: one hue per entity, reason: four surfaces take the categorical colours in a fixed order }
```
:::

## What comes next

Still to build: the log a well actually records, the seismic echo and its resolution limit, the well tie,
the depth-conversion fan, the P90/P50/P10 volumes and the
test of drilling against prediction. The outline is in `docs/outline-v2.md`.
