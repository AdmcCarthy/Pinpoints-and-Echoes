# Plan: Pinpoints and Echoes

*Drafted 2026-11-08. A plan for expanding the placeholder into a public SubScout story. Nothing here is built. Every number below is a thing to compute or verify, not a result.*

## Thesis

A decision worth hundreds of millions rests on almost nothing measured. A wellbore is a few tens of centimetres wide. A field is a few kilometres across. The North Sea is hundreds of thousands of square kilometres. Between the wells, the picture comes from echoes that return from kilometres down, and each of them carries an error. The story shows how a confident picture is built from that, how wrong it can be, and why it can still be trusted.

Keep the existing voice: confident about the mechanism, explicit about the uncertainty. Keep the three words Observed, Derived, Interpreted.

The title moved from "Pinpricks" to **Pinpoints and Echoes** (README.md, CLAUDE.md and `story/story.md` updated 2026-11-08).

## Revision 2026-11-08: field independent, Volve as the receipt

The story is about any field, not Volve. Volve is the backing: an open, real case that shows each claim holds with real numbers. Each step in `story/story.md` carries a **Receipt** line saying which Volve evidence (if any) backs it. Two beats need no receipt: the basin-wide hook (Sodir) and the volumes beat (a labelled simulation). Comparatives are researched in [`comparatives.md`](comparatives.md); the narrative was reworked first, as asked. A new beat, *error-stack*, covers "every measurement is uncertain, and they stack", and the ladder beat was split from the hook.

## What we already have

| Source | Holds | Used for |
|---|---|---|
| `ep_geoscience_analytics` | Sodir wellbores, fields, discoveries, seismic surveys (notebook 17); Volve logs (about 7 GB DLIS/LAS), check shots and time-depth tables, horizon-vs-well-pick checks (347 pairs), fault sticks and polygons, position uncertainty (`xy_sigma_m`, `z_sigma_m`), production | Scale hook, observation, tie, depth, test |
| `seismic_art` | Synthetic cube with known truth; windows along horizons, wiggle features; rings, growth, flow and cities sketches; Volve exports | Echo beat, the art-led opening and closing visual |
| `volve-surfaces` | Smoothed Volve horizons in time and depth, fault throw, 132 well picks checked, scale bar and attribution pattern | Map and "cut the map" figures, and the reusable attribution wording |
| `SubScout` | Story format, arcs (`pre-post-drill`, `zoom`), P90/P50/P10 forms, well symbols, readability gate | The build |

## The scale ladder (the spine)

One idea per step, each zoomed out one rung further than the last:

1. A **wellbore**: diameter in centimetres, sampling a thin cylinder.
2. A **field** (Volve): all its wells together, as a share of the field's area.
3. The **North Sea** (Sodir): every wellbore as a dot at true size. They vanish.
4. The **echo**: the sound path, travel time, wavelength and resolution. Features thinner than about a quarter wavelength blur together.
5. **Measurement error stacked on it**: position sigma, depth reference, velocity, pick.

Every ratio is a `story.py` metric, computed from data and sourced, so no figure is typed into the prose.

## Comparatives from other fields

Each is a *scale comparator* figure: the same ratio, drawn in a familiar setting beside the subsurface one. All outside figures use the `cite:` filter and must be verified before use. I have not checked any of them.

| Analogy | What it conveys |
|---|---|
| Opinion polling: a thousand people stand for millions | Sampling, margin of error, and how the sample can be biased |
| Medical biopsy and ultrasound | A needle sample against an echo image; the same observation/interpretation split |
| Bat or sonar echolocation | Time is measured, not distance; velocity is assumed |
| Weather forecast ensembles | A range of outcomes carried through to the number people quote |
| Mapping the seabed or other planets | We often know remote surfaces better than the one under our own sea |
| Geotechnical boreholes for a bridge or tunnel | Another trade that infers between holes |

Choose three at most, one per section, so they clarify and do not decorate. Each carries its own source and confidence tag.

## Beats, data and figures

Builds on the existing outline, with the data mapped.

| Beat | Figure | Data | Confidence |
|---|---|---|---|
| hook (Outcrop) | Wells at true scale: North Sea, then field, then one well | Sodir wellbores, fields; bit sizes | Derived |
| observation | Composite log of one Volve well | Volve LAS/DLIS | Observed |
| echo | Wiggle section, time not depth; resolution limit | Volve SEG-Y extract; synthetic wedge from `seismic_art` for the resolution point, labelled synthetic | Observed / Derived |
| tie | Well tie: log, synthetic, traces | Volve check shots and logs | Interpreted |
| interpretation | Alternative pictures of one surface | Volve "Official" vs "Other" horizons; base survey vs reprocessed (ST0202 vs ST10010); real pick-to-horizon misfit | Interpreted |
| measurement error | Position ellipse and depth reference per well | `position_uncertainty`, rotary-table elevation | Derived |
| depth | Time-to-depth fan; "cut the map" | Check-shot disagreement (one table is tens of ms off at the reservoir); `volve-surfaces` | Interpreted |
| volumes | P90/P50/P10 bar and exceedance curve | To build; pick inputs with ranges, state them | Interpreted (simulated, labelled so) |
| test | Prognosis against outcome | See open question 3 | Observed vs Interpreted |
| therefore | How to read a subsurface claim | none | n/a |

`seismic_art` also gives a candidate opening or closing image: a seismic section wrapped into rings, to make the echo something the reader feels before they are told what it is. It must follow that repo's honest-art rules: attribution, domain, polarity, and synthetic labelled as synthetic.

## Licences and acknowledgements

- **Volve.** `volve-surfaces/DATA-LICENCE.md` sets the working terms: credit Equinor and the former licence partners, link the Terms and Conditions, no sale, nothing misleading, no endorsement, as-is. `seismic_art/docs/concepts.md` says CC BY-NC-SA. These two statements must be reconciled against Equinor's current terms before publishing. If it is NC-SA, derived data in this repo carries that licence too.
- Use the attribution line from `volve-surfaces` on the story and in the appendix, and add a plain-language acknowledgement of Volve as a rare open data release.
- **Sodir.** Check the FactPages licence and record the terms in `data/README.md`.
- Raw data stays out of git (`data/raw/`, ignored); only story-sized extracts are committed.
- Code is MIT; the narrative text and figures need their own licence, consistent with the data terms.

## Phases

1. **Housekeeping.** Rename text to Pinpoints. Add `docs/` links to CLAUDE.md. Settle licences (above) and write `data/README.md`.
2. **Audit.** Confirm what exists locally: the Volve SEG-Y, logs and interpretation files; whether the Volve seismic cube is available (`seismic_art` notes it is not local); and the Sodir marts. Decide the Volve well and the extraction window. Output: a short availability table.
3. **Extracts and metrics.** Small, committed files in `data/`; `story.py` with the scale and uncertainty metrics, each with source and confidence.
4. **Figures.** Check which devices SubScout's `charts.js` already covers (map, dots, range bars) and which are new custom figures (wiggle section, well tie, composite log, depth fan, exceedance curve). Reuse `seismic_art` and `volve-surfaces` D3 code where it fits.
5. **Write and build.** Replace the outline with prose. `uv run subscout build`, then the readability gate on phone and desktop.
6. **Review and publish.** Check every number appears in the ledger; check attribution; publish to GitHub Pages. Publishing is public, so confirm first.

## Risks

- SubScout's `story.md` format is v0.1 and may change; the outline's own header says so.
- Several figures are new custom components, which is the largest build cost.
- The Volve seismic cube may not be on this machine. The echo and tie beats need the SEG-Y extract (121 files, 0.54 GB in the inventory); without it they fall back to the synthetic cube, clearly labelled.
- "Several interpreters" has no ready set of independent interpretations. The Volve alternatives are different surveys and folders, not blind picks by different people, so the text must say what they are.
- Outside analogies add claims that must be sourced.

## Open questions

1. ~~Is Volve the whole story?~~ Settled: no. Field independent, Volve as the receipt.
2. Do we make our own alternative horizon picks (labelled Interpreted, method stated), or use only what the Volve release contains?
3. The pre/post-drill beat needs a prognosis. Does the Volve release include one (the plan for development against production, or well prognoses against actual tops)? I have not checked.
4. Which comparatives to keep? Researched; recommendation in `comparatives.md` (seafloor mapping, tunnel ground investigation, weather ensembles, plus the industry's look-back studies for the test beat).
5. Should this repo's CLAUDE.md also import Idiom's `CORE.md`, as `seismic_art` and `ep_geoscience_analytics` do, for voice and structure?
