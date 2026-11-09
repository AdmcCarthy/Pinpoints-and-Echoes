---
title: Pinpoints and Echoes
short_title: Pinpoints and Echoes
dek: Every map of the subsurface is mostly inference. A handful of boreholes and the echoes of sound waves become a confident picture of rocks no one has seen. Here is how that picture is built, how far it can be wrong, and why it is still worth trusting.
kicker: NORTH SEA · SODIR WELLBORES · VOLVE AS THE WORKED CASE
byline: Adam McCarthy
date: 2026-11-09
register: section
palette: tide
surface: nordic-cool
units: sm3
horizon: true
kpis:
  - { metric: n_wellbores, label: petroleum wellbores in the Norwegian North Sea }
  - { metric: hole_cm, label: "cm across at reservoir depth", filter: round:0 }
  - { metric: nn_km, label: "km to the nearest other exploration well (typical)", filter: round:1 }
  - { metric: volve_swing, label: "× between the highest and lowest estimate of one field", filter: round:1 }
sources:
  sodir:
    name: Sodir FactPages, wellbore, field and reserves tables (Norwegian Offshore Directorate)
    url: "https://factpages.sodir.no"
    accessed: 2026-11-06
    note: "Source: Sodir. Contains data under the Norwegian licence for Open Government data (NLOD 2.0) distributed by Sodir. Filtered, converted to wellhead positions and summarised by the author."
  volve:
    name: Volve data village, Equinor ASA and the former Volve licence partners
    url: "https://www.equinor.com/energy/volve-data-sharing"
    note: "Contains data from the Volve data village, © Equinor ASA and the former Volve licence partners (ExxonMobil E&P Norway, Bayerngas Norge). Used under the Volve Terms and Conditions. Generalised for display. Horizons, closure curve and contact distribution via volve-surfaces; surveys, check shots and picks via the author's data engine."
  gebco:
    name: GEBCO, release of the GEBCO_2025 Grid
    url: "https://gebco.net/news/release-gebco2025-grid"
    accessed: 2026-11-08
    note: "Share of the world's ocean floor mapped to modern standards, as announced by the Seabed 2030 project on 21 June 2025."
  hoek:
    name: Hoek and Palmieri (1998), Geotechnical risks on large civil engineering projects, IAEG Congress keynote
    url: "https://www.rocscience.com/assets/resources/learning/hoek/Geotechnical-Risks-on-Large-Civil-Engineering-Projects-1998.pdf"
    accessed: 2026-11-08
    note: "Citing the World Bank (1985) on hydropower costs and the US National Committee on Tunnel Technology (1984) on 84 tunnels."
  ecmwf:
    name: ECMWF, Enter the ensembles (2024)
    url: "https://www.ecmwf.int/en/about/media-centre/aifs-blog/2024/enter-ensembles"
    accessed: 2026-11-08
data:
  wells: data/wells.csv
  geometry: data/geometry.csv
  chain: data/chain.csv
  spread: data/spread.csv
  transect: data/transect.csv
  picks: data/picks.csv
  log: data/log.csv
  section: data/section.json
  horizons: data/horizons.csv
  wedge: data/wedge.json
  tie: data/tie.csv
  timedepth: data/timedepth.csv
  closure: data/closure.csv
  contact: data/contact.csv
  volumes: data/volumes.csv
  volve_reserves: data/volve_reserves.csv
  revisions: data/revisions.csv
  notes: data/beats_notes.json
---

A field development is sanctioned on a picture of rock that nobody has seen. The picture is assembled from
two kinds of evidence: a few holes a hand's width across, and sound that went down several kilometres and
came back. This story follows one such picture from the first hole to the number in the board paper, and keeps
a tally of what is observed, what is derived and what is interpreted along the way. The argument holds for any
field. The receipts come from Volve, a small North Sea oil field whose owners released its data when it was
done, and from Sodir, the Norwegian regulator, whose records cover every well on the shelf.

## Pinpoints

::: step {beat=hook register=outcrop}
### Every well ever drilled in the Norwegian North Sea

The map shows {{ n_wellbores | int }} petroleum wellbores drawn at their true size on the area they span. None
of them is visible. At this scale each one is a small fraction of a pixel, and together they have ever been a
hole in one part in {{ one_in | about }} of the area inside the dashed line. Everything known about the rock
between them is inferred.

```chart
id: shelf
type: custom
module: figures/scale.js
data: [wells, geometry]
state: { mag: 1 }
title: At true size, the wells vanish
subtitle: Wellhead positions of petroleum wellbores, Norwegian North Sea, drawn at true diameter
source: sodir
confidence: derived
unit: km (area), cm (hole)
notes: Wellhead positions, not bottom-hole. The dashed outline is the convex hull of the wellheads, not the sea. Every wellbore counts, sidetracks included. Hole diameter is the Volve reservoir-depth median.
```
:::

::: step {beat=hook}
Enlarged thousands of times, the same wells show where the drilling has been: strings of platforms along the
field axes, and wide areas between them that no bit has touched.

```chart
use: shelf
mag: 12000
title: Enlarged to be seen, the wells still leave the area empty
subtitle: The same wellheads, each enlarged by the factor stated below
```
:::

::: step {beat=ladder}
### A hole a hand's width across, and the next one kilometres away

At reservoir depth a wellbore is about {{ hole_cm | round:0 }} cm across. The typical exploration well is
{{ nn_km | round:1 }} km from its nearest neighbour, in a range from {{ nn_p10 | round:1 }} km to
{{ nn_p90 | round:1 }} km. Divide one by the other and the gap is {{ spacing_ratio | about }} hole widths.
The rock in between is never touched, only argued about.

```chart
id: ruler
type: custom
module: figures/ruler.js
data: geometry
state: { coin: false }
title: From a hole a hand fits in to an area hundreds of kilometres wide
subtitle: Lengths on a logarithmic scale, metres to kilometres
source: sodir
confidence: derived
unit: m, km
notes: Distances use wellhead positions of exploration wellbores (initial bores, 100 m cells). Logarithmic axis, which departs from the linear-axis default; it is the only way to show both ends. Hole diameter is the Volve reservoir-depth median.
exception: { rule: linear axes, reason: the lengths span seven orders of magnitude }
```
:::

::: step {beat=ladder}
Redrawn with the wellbore as a coin one centimetre across, the nearest well sits {{ coin_m | about }} m away
and the area the wells span becomes a square {{ coin_span_km | about }} km on a side. Decisions costing
billions of kroner rest on what lies in that space.

```chart
use: ruler
coin: true
title: As a coin, the next well is a long walk away
```
:::

::: step {beat=observation}
### What one well records

Along its own path a well is generous. The composite log of Volve well F-11 T2 samples the rock every
{{ log_sample_cm | int }} cm over {{ log_span_m | round:0 }} m of hole: natural radioactivity, bulk density,
electrical resistivity and the speed of sound. Each curve is a measurement with a tool, a calibration and an
error of its own. The Hugin Formation, the reservoir, is {{ hugin_thickness | round:0 }} m thick here and
stands out on every track. A metre to the side of the hole, nothing is measured at all.

```chart
id: log
type: custom
module: figures/log.js
data: log
state: { zoom: false, reservoir: [3181.5, 3282.8] }
title: Rich along one line, blind a metre away
subtitle: Composite log of 15/9-F-11 T2 against depth below mean sea level; the Hugin Fm shaded
source: volve
confidence: observed
unit: API, g/cm³, ohm·m, µs/ft
notes: Four of the composite's 21 curves. Depth is converted from measured depth with the well's near-offset check-shot table. Resistivity is on a logarithmic axis, as is conventional. The reservoir band is the interpreters' top and base picks.
```
:::

::: step {beat=observation}
Within the reservoir the log resolves layers a few tens of centimetres thick: cemented bands, shale breaks,
the fine structure that decides how oil moves. This is the detail the echo cannot see.

```chart
use: log
zoom: true
title: In the reservoir, the log sees layers the echo cannot
```
:::

## Echoes

::: step {beat=echo}
### The same ground as an echo

Sound left the sea surface, travelled down through the water and {{ hugin_top_tvdss | round:0 }} m of rock,
and part of it returned from the top of the Hugin Formation after {{ hugin_twt_s | round:2 }} seconds. The
panel is inline {{ inline | int }} of the Volve survey, {{ n_traces | int }} traces across, with the well
as a dashed line. The vertical axis is time, not depth. What looks like a cross-section is a record of
arrivals, and turning it into depth is a separate step with its own uncertainty.

```chart
id: section
type: custom
module: figures/section.js
data: [section, horizons]
state: { horizons: false }
title: A cross-section made of sound, in time
subtitle: Inline {{ inline | int }} of the ST10010 full stack through 15/9-F-11 T2, two-way time, relative amplitude
source: volve
confidence: observed
unit: ms two-way time; km from the well
notes: Pre-stack depth migrated and delivered in time (2011 processing). Every second crossline is drawn. Amplitudes are relative and polarity is not stated in the headers. Greyscale, positive dark, departs from the data palette because seismic is read as texture; one highlight marks the well.
exception: { rule: data palette, reason: greyscale variable density is how a seismic section is read }
```
:::

::: step {beat=echo}
On the same panel, the surfaces the Volve interpreters published. Each line is a judgement about which
arrival belongs to which rock boundary, carried across the survey from where the wells pin it. Away from the
well the lines are interpretation; at the well they are tied.

```chart
use: section
horizons: true
title: What an interpreter adds to the echo
```
:::

::: step {beat=echo}
### Thinner than a quarter of a wavelength, and it disappears

Around the reservoir the data's dominant frequency is about {{ dom_hz | round:0 }} Hz and the sound travels at
{{ v_res | int }} m/s, so a quarter of a wavelength is {{ quarter_m | round:0 }} m. A synthetic bed thinned
from eighty metres to nothing shows what that means: below about {{ tuning_m | round:0 }} m the echoes from its top and
base merge, and the thickness the seismic reports stops following the truth. The layers the log resolved in
the previous panel are far below this limit.

```chart
id: wedge
type: custom
module: figures/wedge.js
data: wedge
title: Below the tuning thickness, two echoes become one
subtitle: Synthetic wedge at the data's wavelet; left, the response; right, the thickness the echo reports against the truth
source: volve
confidence: derived
unit: m, ms
notes: Synthetic, and labelled so. A zero-phase Ricker wavelet at the centroid frequency of the real data, two interfaces of equal and opposite reflectivity, the velocity from the well's sonic log in the Hugin Fm. Real wavelets are not zero phase, so real tuning differs in detail.
```
:::

::: step {beat=echo}
The limit is set by wavelength, in water as in rock. The same physics maps the sea floor by sonar, and by 2025
only {{ 27.3 | cite:gebco }} per cent of the world's ocean floor had been mapped to modern standards. The rock
beneath it is mapped from kilometres further away, through the sea floor, with a longer wave.

```chart
use: wedge
title: The same limit applies to every echo, including the sea floor's
```
:::

::: step {beat=tie}
### Where the pinpoint meets the echo

The two kinds of evidence meet in the well tie. The log's sonic and density give a reflectivity series over {{ ai_cover | pct }} of the window; the
data's wavelet turns it into a synthetic trace; the check-shot table places it in time. Beside it is the real
trace at the well. Without adjustment the two correlate at {{ tie_zero | round:2 }}. A single bulk shift of
{{ tie_shift | int }} ms raises that to {{ tie_corr | round:2 }}.

```chart
id: tie
type: custom
module: figures/tie.js
data: tie
state: { shifted: false }
title: The log, turned into sound, beside the sound itself
subtitle: Synthetic seismogram from the 15/9-F-11 T2 log and the real trace at the well, 2,300 to 3,100 ms
source: volve
confidence: derived
unit: ms two-way time; relative amplitude
notes: Reflectivity from sonic and density where both exist (a share stated in the ledger), convolved with a zero-phase Ricker wavelet at the data's centroid frequency, placed in time with the near-offset check-shot table. Scaled to the real trace's RMS. The data's polarity is not stated; the synthetic is drawn with the sign that matches better. No stretch applied.
```
:::

::: step {beat=tie}
After the shift the main reflectors line up and the detail between them does not. The log is sampled every
{{ log_sample_cm | int }} cm; the echo averages tens of metres. Two instruments measuring the same rock agree on the outline and
disagree on the detail, which is the whole relationship between a well and a seismic survey in one panel. A
working tie would go further: a wavelet extracted from the data rather than assumed, and stretch applied to the
synthetic. Each of those steps is a judgement, and this is where the judgements begin.

```chart
use: tie
shifted: true
title: After one shift, the outline agrees and the detail does not
```
:::

## Measurements

::: step {beat=error-stack}
### Every measurement is uncertain, and they stack

Where the well is. What depth is measured from. How fast sound travels. Where a pick sits on the wavelet. Each
link in the chain carries an error, and the errors stack. In Volve the horizontal position of a well is known
to a median {{ pos_h | round:0 }} m at the end of its survey, and to {{ pos_h_max | round:0 }} m in the worst
case. The figure follows the {{ n_links | int }} vertical links one at a time, starting with the well's own
depth.

```chart
id: stack
type: custom
module: figures/errstack.js
data: stack
state: { upto: 2 }
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
A depth reference mixed up between the rotary table and sea level shifts every depth in a well by the height
of the rig floor, {{ rt_m | round:0 }} m for the Volve platform wells. It is a known trap, and one Volve
check-shot table turned out to be referenced that way.

```chart
use: stack
upto: 3
title: The depth reference can shift every depth at once
```
:::

::: step {beat=error-stack}
Seismic arrives as two-way time, and velocities from check shots convert it to depth. Where the picks and the
check shots were made independently they disagree by tens of metres in the worst case. Even after the Volve
horizons were adjusted to the wells, the reservoir surface misses the picks by metres typically and by about a
hundred in the worst case.

```chart
use: stack
upto: 5
title: Time to depth, and the surface against the picks, add the most
```
:::

::: step {beat=error-stack}
Typical errors combine to about {{ stack_typical | round:0 }} m at the reservoir. The largest on file combine
to about {{ stack_worst | round:0 }} m. That is the honest width of the answer to the question "how deep is
it?", before any interpretive judgement has been made.

```chart
use: stack
upto: 6
title: Together, metres in the typical case and hundreds in the worst
```
:::

## Interpretations

::: step {beat=interpretation}
### Between the wells the surface is drawn, not measured

Take one surface, the top of the Ty Formation, along a {{ line_km | round:1 }} km line between wells. At the
{{ n_picks_line | int }} well picks near the line (circles) the depth was observed and its time comes from a
check-shot table. Everywhere between them the surface is drawn, by an interpreter, by software, or by both.

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
The base survey gives one surface and the reprocessed survey another. They agree on the broad shape and differ
in the detail. Along this line they differ by a median {{ gap_med_ms | round:0 }} ms and by up to
{{ gap_max_ms | round:0 }} ms, which is up to about {{ gap_max_m | round:0 }} m of depth at the Volve average
velocity. Neither is wrong. Neither passes through the picks either: on average they miss them by
{{ miss_base | round:0 }} and {{ miss_repro | round:0 }} ms.

```chart
use: transect
stage: 3
title: Two defensible surfaces, and the gap between them
```
:::

::: step {beat=interpretation}
### Wells narrow the disagreement without ending it

The textbook picture is that interpretations agree near the wells and part away from them. The Volve versions
show a weaker form of it. Within a quarter of a kilometre of a well pick the median difference is already
{{ near_lo | round:0 }} to {{ near_hi | round:0 }} ms, depending on the surface. Beyond two kilometres, where
{{ n_far | int }} of the {{ n_versions | int }} surfaces have enough nodes to compare, it is
{{ far_lo | round:0 }} to {{ far_hi | round:0 }} ms.

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
notes: Solid line is the median absolute difference at nodes 12.5 m apart, dashed line the 90th percentile. Bands with fewer than a thousand nodes are not drawn. Distance is to the nearest well pick of any interpreted surface. The Ty Fm top is a special case near wells because its official version was updated with later wells. A systematic offset between versions is included, not removed.
exception: { rule: one hue per entity, reason: four surfaces take the categorical colours in a fixed order }
```
:::

::: step {beat=depth}
### One time, six depths

Converting time to depth needs a velocity, and the velocity comes from check shots in a few wells. Volve has
{{ fan_n | int }} check-shot tables from {{ fan_wells | int }} wellbore folders. Read every one at
{{ fan_twt_s | round:2 }} seconds of two-way time and the depth comes back between {{ fan_min | round:0 }} and
{{ fan_max | round:0 }} m below sea level, a spread of {{ fan_range | round:0 }} m.

```chart
id: fan
type: custom
module: figures/fan.js
data: timedepth
state: { at: 2650, zoom: false }
title: Six tables, one time, a 68 m spread in depth
subtitle: Two-way time against depth for every Volve check-shot table; the fan is read at 2.65 s
source: volve
confidence: observed
unit: ms, m below MSL
notes: Tables as delivered, including one whose depth reference was found to be the rotary table rather than sea level (corrected here by the stated 54.9 m). Two tables belong to one wellbore folder with two bores. The reading time is chosen because every table covers it.
```
:::

::: step {beat=depth}
Close in, the curves fan out. Some of the spread is real, because the wells are kilometres apart and the rock
between them changes. Some of it is measurement. A horizon mapped in time can be placed in depth anywhere
inside that band, and the trap's size changes with it. Between the wells there is no way to say which table
applies, which is the point.

```chart
use: fan
zoom: true
title: Close in, one time opens into a band of depth
```
:::

## The number

::: step {beat=volumes}
### Fifteen metres of contact, more than twice the area

The depth of the oil-water contact decides how much of a structure holds oil. On the smoothed Hugin top
surface the area inside the closing contour does not grow smoothly with depth. Where the contact drops below
a saddle that joins two highs, the trap takes in the second high at once, and the curve steps.

```chart
id: closure
type: custom
module: figures/closure.js
data: [closure, contact]
state: { cases: false }
title: Area inside the closing contour grows in steps, not smoothly
subtitle: Area inside the closing contour of the Volve high on the Hugin top, against depth
source: volve
confidence: interpreted
unit: m below MSL, km²
notes: The curve is the merge-tree closure analysis of volve-surfaces on a smoothed, interpreted depth surface; it is a reading of the structure, not the plan's own map. The contact distribution is digitised from the 2005 plan for development, table 3.5. Depth increases downward.
```
:::

::: step {beat=volumes}
Volve's 2005 plan for development gave the contact as a distribution: P90 {{ owc_p90 | int }} m, P50
{{ owc_p50 | int }} m, P10 {{ owc_p10 | int }} m below sea level, with P90 the shallow, low case. The area is
{{ area_p90 | round:1 }} km² at the P90 contact and {{ area_p50 | round:1 }} km² at the P50,
{{ area_ratio | round:1 }} times as much for {{ owc_step | int }} m more depth, because the P50 contact lies
just below the saddle. The P10 contact lies deeper than the mapped surface can hold.

```chart
use: closure
cases: true
title: A few metres of contact depth can double the trap
subtitle: The same curve with the plan's three contact cases
```
:::

::: step {beat=volumes}
### The number people quote

Carry the contact through to recoverable oil and the width of the answer becomes visible. With the closure
curve above, the plan's contact distribution and illustrative ranges for pay, porosity, saturation, shrinkage
and recovery ({{ sim_n | int }} draws, parameters in the ledger), the simulation gives a P90 of
{{ vol_p90 | round:0 }}, a P50 of {{ vol_p50 | round:0 }} and a P10 of {{ vol_p10 | round:0 }} million Sm³.
The high case is {{ vol_ratio | round:1 }} times the low.

```chart
id: exceed
type: custom
module: figures/exceed.js
data: volumes
title: One number is really a curve
subtitle: Simulated recoverable oil, chance of at least each volume, with P90, P50 and P10 (oilfield convention)
source: volve
confidence: interpreted
unit: Mn Sm³ (toggle for boe)
notes: A simulation, labelled as one. Area from the closure curve at a contact drawn from the plan's distribution (draws deeper than the mapped surface take its deepest area, a share stated in the ledger); average net pay 15 to 50 m, porosity 0.16 to 0.24, water saturation 0.25 to 0.50, formation volume factor 1.15 to 1.35, recovery factor 0.30 to 0.50, all triangular and chosen for the story. Seed 7.
```
:::

::: step {beat=volumes}
The exercise is illustrative and is not an estimate of Volve: every range was chosen for the story, and
{{ capped | pct }} of the draws fall deeper than the mapped surface and take its deepest area. Its shape is
the shape every such number has. Weather forecasters publish the same thing when they run
{{ 51 | cite:ecmwf }} versions of tomorrow and show how far they spread.

```chart
use: exceed
title: A P50 is one point on the curve, not a prediction
```
:::

## The test

::: step {beat=test}
### Twenty years of one field's number

Drilling and production are the test of every estimate. Sodir has published its own recoverable estimate for
Volve each year since {{ volve_first_yr | int }}: {{ volve_first | round:1 }} million Sm³ of oil equivalent
at first, {{ volve_peak | round:1 }} at the peak in {{ volve_peak_yr | int }}, {{ volve_low | round:1 }} at
the low in {{ volve_low_yr | int }}, and {{ volve_latest | round:1 }} in {{ volve_latest_yr | int }}, with
the field produced out. The highest estimate was {{ volve_swing | round:1 }} times the lowest, for the same
rock, as the wells and the production history arrived.

```chart
id: volve_hist
type: line
data: volve_hist
x: snapshot_year
y: recoverable_mn_sm3
series: series
volume: true
unit_label: "Mn {unit} o.e."
title: Sodir's estimate of Volve moved by half as the field was drilled and produced
subtitle: Recoverable resources of the Volve field by snapshot year, million Sm³ oil equivalent
source: sodir
confidence: observed
unit: Mn Sm³ o.e.; 1 Sm³ o.e. = 6.29 boe
notes: Sodir's annual resource accounts as held in the FactPages. Oil equivalent follows Sodir's convention.
```
:::

::: step {beat=test}
### Half the fields grew, half shrank

Volve is not unusual. For the {{ rev_n | int }} Norwegian fields with a development plan approved since 2003
and at least five years of Sodir snapshots, the latest estimate divided by the first is {{ rev_median | round:2 }}
at the median, but {{ rev_p10 | round:2 }} at the 10th percentile and {{ rev_p90 | round:2 }} at the 90th.

```chart
id: revisions
type: dots
data: revisions_dec
row: decade
value: ratio_pct
label: field_label
scale: linear
unit: "% of first estimate"
value_label: one dot per field
title: The median field held its estimate; most individual fields did not
subtitle: Latest Sodir recoverable estimate divided by the first, by decade of plan approval
source: sodir
confidence: derived
notes: Fields whose first Sodir snapshot falls within a year of plan approval, so the first number is close to the sanction estimate. A value of 100 means no change. When highlighted, Volve is the dark dot.
```
:::

::: step {beat=test}
{{ rev_down | pct }} fell by more than five per cent and {{ rev_up | pct }} grew by more than that;
{{ rev_halved | pct }} at least halved and {{ rev_doubled | pct }} at least doubled. The median estimate was
about right. Almost no single field was, and Volve, highlighted, is one dot among them.

```chart
use: revisions
highlight: [Volve]
title: Volve, highlighted, is one field among many that moved
subtitle: The same ratios with Volve picked out
```
:::

## Reading a claim

::: step {beat=therefore}
### Three words for any subsurface claim

Every number above carries one of three words. Observed means measured or published, with a source: the log,
the trace, Sodir's estimate. Derived means calculated from observed data by a stated method: the distance
between wells, the tuning thickness, the fan. Interpreted means dependent on a model or a judgement, and given
with its range: the horizons, the closure area, the simulated volume.

```chart
id: shelf_again
type: custom
module: figures/scale.js
data: [wells, geometry]
state: { mag: 1 }
title: "Back to the start: the wells, at true size"
subtitle: Wellhead positions of petroleum wellbores, Norwegian North Sea, drawn at true diameter
source: sodir
confidence: derived
unit: km (area), cm (hole)
notes: The opening figure again. Wellhead positions, convex hull of the wellheads, every wellbore counted, Volve reservoir-depth hole diameter.
```
:::

::: step {beat=therefore}
Other trades infer between boreholes and live with the consequences. A review of {{ 84 | cite:hoek }} tunnels
found contract costs rising as the length of exploration drilling fell relative to the tunnel, and hydropower
projects that had spent on average under {{ 1 | cite:hoek }} per cent of their cost on investigation before
design overran by {{ 27 | cite:hoek }} per cent. The subsurface case is the same case with deeper holes.

```chart
use: shelf_again
mag: 12000
title: Enlarged again, the holes and the ground between them
subtitle: The same wellheads, each enlarged by the factor stated below
```
:::

::: step {beat=therefore}
The questions to ask of any claim about the subsurface are the same three: which word applies, what it was
compared with, and how wide the range is. The wells remain the only points where the rock has been touched.
Everything between them is echo and inference.

```chart
use: shelf_again
mag: 12000
title: Pinpoints and echoes
subtitle: The same wellheads, each enlarged by the factor stated below
```
:::

## Acknowledgement

The Volve data were released by Equinor ASA and the former Volve licence partners (ExxonMobil E&P Norway,
Bayerngas Norge) under the Volve Terms and Conditions, a rare open release of a complete field, and this story
could not be told without it. Wellbore, field and reserves data are from Sodir (Source: Sodir, under the Norwegian Licence for Open Government Data).
Closure and contact analysis comes from the author's volve-surfaces project; surveys, check shots and picks
from the author's data engine. Built with SubScout by Adam McCarthy (github.com/AdmcCarthy/SubScout). No
endorsement by Equinor, the former partners or Sodir is implied. Numbers, methods and sources follow in the
basis of analysis.
