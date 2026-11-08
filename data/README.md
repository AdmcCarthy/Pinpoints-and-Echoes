# Data

Raw downloads go in `data/raw/` (git-ignored). Story-sized extracts are committed in `story/data/`, written by `scripts/make_extracts.py` from the `ep_geoscience_analytics` mid-layer. Heavy ingestion stays there.

## In use

| File | From | Used for |
|---|---|---|
| `story/data/wells.csv` | Sodir wellbore table: North Sea petroleum wellbores, wellhead positions | hook, ladder |
| `story/data/geometry.csv` | the same, plus the Volve reservoir hole diameter | hook, ladder |
| `story/data/chain.csv` | Volve survey, check-shot and horizon-to-pick checks | error stack |
| `story/data/spread.csv`, `transect.csv`, `picks.csv` | Volve base (ST0202R08) and reprocessed (ST10010) versions of four horizons, and the well picks, in two-way time | interpretation spread |

Licences and attribution lines: [`../DATA-LICENCE.md`](../DATA-LICENCE.md). Open items there: the Sodir NLOD version and the Volve licence wording.

## Candidates for later beats

Volve logs, SEG-Y and interpretations (composite log, echo, tie, interpretation spread, depth); Sodir discoveries and reserves (test beat); NLOG and NSTA as alternates; F3 for teaching seismic.

## To decide

- The spread beat uses published Volve versions only (two surveys, not blind interpreters; the story says so). Whether to add picks we make ourselves is open.
- What public prognosis exists for the pre-drill and post-drill beat (see `docs/comparatives.md`).
