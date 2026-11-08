# Data

Raw downloads go in `data/raw/` (git-ignored). Story-sized extracts are committed in `story/data/`, written by `scripts/make_extracts.py` from the `ep_geoscience_analytics` mid-layer. Heavy ingestion stays there.

## In use

| File | From | Used for |
|---|---|---|
| `story/data/wells.csv` | Sodir wellbore table: North Sea petroleum wellbores, wellhead positions | hook, ladder |
| `story/data/geometry.csv` | the same, plus the Volve reservoir hole diameter | hook, ladder |
| `story/data/chain.csv` | Volve survey, check-shot and horizon-to-pick checks | error stack |

Licences and attribution lines: [`../DATA-LICENCE.md`](../DATA-LICENCE.md). Open items there: the Sodir NLOD version and the Volve licence wording.

## Candidates for later beats

Volve logs, SEG-Y and interpretations (composite log, echo, tie, interpretation spread, depth); Sodir discoveries and reserves (test beat); NLOG and NSTA as alternates; F3 for teaching seismic.

## To decide

- Whether the interpretation-spread beat uses published alternatives only (Volve horizon folders and processing vintages) or ones we make.
- What public prognosis exists for the pre-drill and post-drill beat (see `docs/comparatives.md`).
