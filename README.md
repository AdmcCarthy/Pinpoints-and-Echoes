# Pinpoints and Echoes

A data story about how uncertain subsurface interpretation is, and why it can still be trusted. Live page:
<https://admccarthy.github.io/Pinpoints-and-Echoes/>. Built with [SubScout](https://github.com/AdmcCarthy/SubScout);
the argument is field-independent and the worked case is Volve. Plan: [`docs/plan.md`](docs/plan.md); comparatives
research: [`docs/comparatives.md`](docs/comparatives.md); the original outline: [`docs/outline-v2.md`](docs/outline-v2.md).

## Build

Data extracts are written by the scripts in `scripts/` from local copies of the Volve data (`C:\appl\Volve`, never committed), the
`ep_geoscience_analytics` mid-layer and `volve-surfaces`; the small results are committed in `story/data/`. The page is built by
SubScout from `story/`.

```powershell
# extracts (the ep and seismic_lib interpreters hold the dependencies)
..\ep_geoscience_analytics\.venv\Scripts\python.exe -I scripts\make_extracts.py --ep ..\ep_geoscience_analytics
..\ep_geoscience_analytics\.venv\Scripts\python.exe -I scripts\make_spread.py --ep ..\ep_geoscience_analytics --zip C:\appl\Volve\Volve_Geophysical_Interpretations.zip
..\seismic_lib\.venv\Scripts\python.exe -I scripts\make_seismic.py --segy "C:\appl\Volve\Seismic\ST10010ZC11_PZ_PSDM_KIRCH_FULL_T.MIG_FIN.POST_STACK.3D.JS-017536.segy" --x 436123.2 --y 6479126.0 --well "15/9-F-11 T2"
..\ep_geoscience_analytics\.venv\Scripts\python.exe -I scripts\make_beats.py --ep ..\ep_geoscience_analytics --volve C:\appl\Volve --surfaces ..\volve-surfaces
# page (SubScout is a sibling checkout; GitHub Pages builds the same way from SubScout main)
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

## Data in use

Sodir FactPages (wellbores, fields, reserves) and the Volve data village (logs, seismic, interpretations, check shots, surveys, the 2005 plan's contact distribution via volve-surfaces). Terms in `DATA-LICENCE.md`. Candidates considered and not used:

- Norwegian Offshore Directorate (Sodir) FactPages / FactMaps: wellbores, discoveries, fields.
- Equinor's Volve field data release: seismic, well logs and production for one field.
- Netherlands NLOG (TNO): wells and seismic for the Dutch sector.
- UK North Sea Transition Authority National Data Repository: wells and seismic.
- The F3 Netherlands seismic block (dGB Earth Sciences), widely used for interpretation teaching.

See [`data/README.md`](data/README.md).

## Licence and acknowledgement

MIT License with Acknowledgement (see [LICENSE](LICENSE)): the MIT licence plus one condition, that anything built with this
work says so visibly and does not imply endorsement. It is custom wording and not OSI-approved. Use the line:
"Built with Pinpoints and Echoes by Adam McCarthy (https://github.com/AdmcCarthy/Pinpoints-and-Echoes)".

The data extracts keep their own terms: Sodir (NLOD 2.0, "Source: Sodir") and the Volve data village (Volve Terms and
Conditions, CC BY 4.0 based with a no-sale condition). Details and attribution lines: [DATA-LICENCE.md](DATA-LICENCE.md).
Built with SubScout by Adam McCarthy (https://github.com/AdmcCarthy/SubScout).
