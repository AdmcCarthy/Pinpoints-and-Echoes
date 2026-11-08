# Pinpoints and Echoes

> **Status: draft, first slice built.** The hook, scale ladder and error-stack beats build from real
> Sodir and Volve extracts; the remaining beats are outlined in [`docs/outline-v2.md`](docs/outline-v2.md).
> Plan: [`docs/plan.md`](docs/plan.md). Comparatives research: [`docs/comparatives.md`](docs/comparatives.md).

## Build

```powershell
# extracts (reads ../ep_geoscience_analytics, writes story/data/)
..\ep_geoscience_analytics\.venv\Scripts\python.exe -I scripts\make_extracts.py --ep ..\ep_geoscience_analytics
# page (SubScout is a sibling checkout)
cd ..\SubScout; uv run subscout build ..\Pinpoints-and-Echoes\story --out ..\Pinpoints-and-Echoes\_site
```

## The thesis

Interpreting the subsurface is honest persuasion. Geoscientists build confident cases from sparse,
indirect evidence (wells are pinpoints, seismic is an echo) while keeping observation separate
from interpretation.

The voice is the interpreter's voice: **confident about the mechanism, explicit about the
uncertainty.**

## The story

A data narrative about how uncertain geoscience interpretation is, and why it can still be trusted.
The reader should leave able to tell an observation from an interpretation in any subsurface claim,
and know which questions to ask about the uncertainty behind it.

- **Working title:** Pinpoints and Echoes
- **Standfirst (draft):** Every map of the subsurface is mostly inference. A handful of
  boreholes and the echoes of sound waves become a confident picture of rocks no one has seen. Here
  is how that picture is built, how wrong it can be, and why it is still worth trusting.
- **Arc:** *pre-drill / post-drill* (prediction → result → what we learned), framed by the
  observation → interpretation ladder.
- **Register:** *Section* (feature) by default, with an *Outcrop* (showpiece) opening hook.
- **Confidence language:** every claim is tagged **Observed**, **Derived** or **Interpreted**, and the
  story teaches the reader to use the same three words.

The beat-by-beat outline is in [`story/story.md`](story/story.md).

## Signature devices to try

| Device | Purpose |
|---|---|
| Wellbores at true scale on a basin map | The opening hook: how little of the subsurface is ever sampled |
| Composite log | What a well actually observes: one dimension, centimetres around the hole |
| Seismic wiggle traces | The echo: reflections in two-way time, not depth; limited resolution |
| Several interpreters, one dataset | Different valid horizon picks from the same seismic |
| Depth-conversion fan | How velocity uncertainty becomes a range of possible depths |
| P90 / P50 / P10 volumes | Uncertainty carried through to the number people quote |
| Pre-drill vs post-drill | The honest test: predictions against outcomes |
| "Cut the map" | A line across the map opens a cross-section beneath it |

## Candidate open datasets

Not yet chosen. Licences and terms must be checked before use.

- Norwegian Offshore Directorate (Sodir) FactPages / FactMaps: wellbores, discoveries, fields.
- Equinor's Volve field data release: seismic, well logs and production for one field.
- Netherlands NLOG (TNO): wells and seismic for the Dutch sector.
- UK North Sea Transition Authority National Data Repository: wells and seismic.
- The F3 Netherlands seismic block (dGB Earth Sciences), widely used for interpretation teaching.

See [`data/README.md`](data/README.md).

## Licence

Code: MIT (see [LICENSE](LICENSE)). Licence for the narrative text and figures: to be decided.
