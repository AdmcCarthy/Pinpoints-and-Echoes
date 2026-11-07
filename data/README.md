# Data

Nothing here yet. Raw downloads go in `data/raw/` (git-ignored). Processed, story-sized outputs go
in `data/` and are committed. Heavy ingestion belongs in the separate Parquet pipeline; this repo
only keeps the small extracts the story needs.

## Candidates (licences to be checked before use)

| Source | What it could provide | Story beats |
|---|---|---|
| Norwegian Offshore Directorate (Sodir) FactPages / FactMaps | Wellbore positions, depths, results; discoveries; fields | hook, test |
| Equinor Volve data release | Seismic, well logs, interpretations and production for one field | observation, echo, tie, depth |
| NLOG (TNO, Netherlands) | Wells and seismic, Dutch sector | alternative for most beats |
| UK NSTA National Data Repository | Wells and seismic, UK sector | alternative for most beats |
| F3 Netherlands seismic block (dGB Earth Sciences) | Public 3D seismic used for teaching interpretation | echo, interpretation |

## To decide

- One basin and one field, so the story moves from the shelf down to a single well.
- Whether the "several interpreters" beat uses published interpretations or ones we make ourselves
  (if our own, they are labelled Interpreted and the method is stated).
- Pre-drill vs post-drill comparisons need prognosed vs actual values. Check what's public.
