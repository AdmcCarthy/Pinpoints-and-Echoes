# Data licence

The licence in `LICENSE` (MIT License with Acknowledgement) covers the code, the story text and the figures made here. The extracts in `story/data/` are derived from the sources below and keep their terms.

## Sodir (Norwegian Offshore Directorate)

`story/data/wells.csv`, `geometry.csv`, `volve_reserves.csv` and `revisions.csv` derive from the Sodir FactPages (wellbore, field and reserves tables). Terms: Norwegian Licence for Open Government Data (NLOD 2.0), as recorded in the author's dataset register. Credit "Source: Sodir". Reuse, change and redistribution are permitted with that credit, a reference to the licence and a note that the data has been changed.

> Source: Sodir. Contains data under the Norwegian licence for Open Government data (NLOD 2.0) distributed by Sodir. Filtered, converted to wellhead positions and summarised by the author.

## Volve

`chain.csv`, `spread.csv`, `transect.csv`, `picks.csv`, `log.csv`, `section.json`, `horizons.csv`, `wedge.json`, `tie.csv`, `timedepth.csv`, `closure.csv`, `contact.csv`, `volumes.csv` and the Volve hole diameter in `geometry.csv` derive from the Volve data village. `header.json`, the band in the page's hero, is a synthetic section made by `scripts/make_header.py` (seismic_art) and derives from no dataset; the page says so. Terms: "Terms and conditions for license to data, Volve", published by Equinor ASA and the former Volve licence partners. The terms are based on CC BY 4.0 with two changes: the material may not be sold, and the licence covers all the data whether or not copyright applies. Commercial and non-commercial use, adapted material and sharing are permitted with credit, a link to the terms and a copyright notice; adapted material may not be shared under terms that stop recipients complying; the data must not be presented in a misleading or distorted way; no endorsement is implied. An earlier note in this repository and in related ones called the terms CC BY-NC-SA; that was wrong and is corrected here.

> Contains data from the Volve data village, © Equinor ASA and the former Volve licence partners (ExxonMobil E&P Norway, Bayerngas Norge). Used under the Volve Terms and Conditions. Generalised for display.

The raw Volve data (seismic, logs, interpretations, reports) is not in this repository and is never committed; the scripts read it from a local path. Everything here is a small, derived extract.

## Cited figures

GEBCO (2025), Hoek and Palmieri (1998) and ECMWF (2024) are cited for single figures in the text, with the source and date in the story's basis of analysis.

This project is not connected with, sponsored or endorsed by Sodir, Equinor or the former Volve licence partners.
