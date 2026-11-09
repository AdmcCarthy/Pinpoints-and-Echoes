"""The header band for the story's hero: the Volve inline through well 15/9-F-11 T2 with the
published surfaces that cross it, in SubScout's header contract (docs/header-contract.md).

Needs seismic_lib and seismic_art (the seismic_art interpreter has both):

    uv run --project ..\\seismic_art python scripts\\make_header.py ^
        --segy "C:\\appl\\Volve\\Seismic\\ST10010ZC11_PZ_PSDM_KIRCH_FULL_T.MIG_FIN.POST_STACK.3D.JS-017536.segy" ^
        --horizons C:\\appl\\Volve_work\\horizons_twt

The inline is the one `make_seismic.py` extracted for the echo beat (read from story/data/section.json),
so the hero and the section figure show the same line. Domain two-way time in ms (the file name says _T,
the text header says PSDM in time); amplitudes relative; polarity not stated in the headers. The surfaces
are the Volve interpreters' picks at the section's traces, nothing smoothed. Writes story/data/header.json
(about 230 kB). The SEG-Y and the horizon files are never copied.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from seismic_art import export_json, parse_surface_name
from seismic_art.header import header_payload, horizon_along
from seismic_art.horizons import read_horizon
from seismic_lib import make_domain, open_segy, section_inline

ROOT = Path(__file__).resolve().parents[1]
WINDOW = (2200.0, 3000.0)  # ms: Ty Fm top to below the Hugin Fm base
HORIZONS = (  # file name starts, shallow to deep
    "Ty_Fm_Top+ST10010",
    "SHETLAND_GP_Top+ST10010",
    "Hugin_Fm_Top+ST10010ZC11_Near",
    "Hugin_Fm_Base+ST10010ZC11_Near",
    "BCU+ST10010ZC11_Full",
)
ATTRIBUTION = (
    "Contains data from the Volve data village, \u00a9 Equinor ASA and the former Volve licence "
    "partners (ExxonMobil E&P Norway, Bayerngas Norge). Used under the Volve Terms and Conditions. "
    "Processed by seismic_art."
)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--segy", required=True)
    ap.add_argument("--horizons", type=Path, required=True, help="folder of the extracted *.dat horizon files")
    ap.add_argument("--cache", type=Path, default=Path(r"C:\appl\Volve_work\seismic_cache"))
    ap.add_argument("--out", type=Path, default=ROOT / "story" / "data" / "header.json")
    a = ap.parse_args()
    section_meta = json.loads((ROOT / "story" / "data" / "section.json").read_text(encoding="utf-8"))
    inline, well = int(section_meta["inline"]), section_meta["well"]
    with open_segy(a.segy, domain=make_domain("time", "amplitude"), cache_dir=a.cache) as src:
        sec = section_inline(src, src.index(), inline, window=WINDOW)
    surfaces, highlight = [], None
    for start in HORIZONS:
        (path,) = sorted(a.horizons.glob(start + "*"))
        hor = read_horizon(path)
        name = parse_surface_name(hor.meta["source_file"], hor.meta.get("header_name", ""))
        surfaces.append((name.label, horizon_along(sec, hor)))
        if start.startswith("Hugin_Fm_Top"):
            highlight = name.label
    payload = header_payload(
        sec,
        surfaces,
        attribution=ATTRIBUTION,
        polarity="unknown",
        title="Pinpoints and Echoes: the header band",
        label=f"Volve ST10010, inline {inline} through well {well}, {WINDOW[0]:.0f} to {WINDOW[1]:.0f} ms TWT; "
        f"{highlight} in the highlight colour",
        highlight=highlight,
        notes=(
            "ST10010ZC11 PZ PSDM Kirchhoff full stack converted to time, 4 ms, 2011 processing; domain TIME and "
            "quantity AMPLITUDE as stated by the author from the text header; polarity not stated in the headers",
            f"the same inline as the section figure (make_seismic.py), through well {well}",
        ),
    )
    path = export_json(a.out, payload)
    covers = ", ".join(f"{s['label']} {s['cover']:.0%}" for s in payload["surfaces"])
    print(f"wrote {path} ({path.stat().st_size / 1e3:.0f} kB): inline {inline}, {sec.n_traces} traces; cover {covers}")


if __name__ == "__main__":
    main()
