# Data

Raw downloads go in `data/raw/` (git-ignored). Story-sized extracts are committed in `story/data/`, written by `scripts/make_extracts.py` from the `ep_geoscience_analytics` mid-layer. Heavy ingestion stays there.

## In use

| File | From | Used for |
|---|---|---|
| `story/data/wells.csv` | Sodir wellbore table: North Sea petroleum wellbores, wellhead positions | hook, ladder |
| `story/data/geometry.csv` | the same, plus the Volve reservoir hole diameter | hook, ladder |
| `story/data/chain.csv` | Volve survey, check-shot and horizon-to-pick checks | error stack |
| `story/data/spread.csv`, `transect.csv`, `picks.csv` | Volve base (ST0202R08) and reprocessed (ST10010) versions of four horizons, and the well picks, in two-way time | interpretation spread |
| `story/data/log.csv` | Volve 15/9-F-11 T2 composite log (four curves, 0.5 m) with depth and time from check shot 1 | observation |
| `story/data/section.json`, `horizons.csv` | ST10010 full-stack inline 10215 (int8, every second crossline, 1,800 to 3,300 ms) and the published horizons along it | echo |
| `story/data/wedge.json` | Synthetic wedge at the data's centroid frequency and the log's reservoir velocity | echo (resolution) |
| `story/data/tie.csv`, `trace.csv` | Synthetic seismogram from the log and the real trace at the well | tie |
| `story/data/timedepth.csv` | Every Volve check-shot table, decimated, plus the reading at 2,650 ms | depth fan |
| `story/data/closure.csv`, `contact.csv` | Area against depth of the Volve high on the Hugin top (volve-surfaces) and the 2005 plan's contact distribution | volumes |
| `story/data/volumes.csv` | Exceedance curve of the illustrative simulation (seed 7, 20,000 draws) | volumes |
| `story/data/volve_reserves.csv`, `revisions.csv` | Sodir recoverable estimates of Volve by year, and first-to-latest ratios of 59 fields | test |
| `story/data/beats_notes.json` | Method notes and summary numbers written by `make_beats.py`, read as metrics | several |

Licences and attribution lines: [`../DATA-LICENCE.md`](../DATA-LICENCE.md). Open items there: the Sodir NLOD version and the Volve licence wording.

## Assumptions worth knowing

- Positions are wellhead positions; the study area is the convex hull of them, not the sea.
- The well throughout the Volve beats is 15/9-F-11 T2; its time comes from check shot 1 (near offset).
- The seismic polarity is not stated by the data; the synthetic is drawn with the better-matching sign and says so.
- The closure curve is from a smoothed, interpreted surface; the volume simulation uses parameters chosen for the story and is not a Volve estimate.
- Raw Volve files stay outside the repository (`C:ppl\Volve`); the scripts read them from there.

## Open

- The spread beat uses published Volve versions only (two surveys, not blind interpreters; the story says so). Independent picks could be added later.
- The test beat uses Sodir's annual estimates rather than a pre-drill prognosis; the published look-back studies in `docs/comparatives.md` remain unverified.
