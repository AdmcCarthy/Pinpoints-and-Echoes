"""The header band for the story's hero: a synthetic section with a geometry the eye reads, in
SubScout's header contract (docs/header-contract.md). No horizons, no surfaces: the texture alone.

Needs seismic_art (its interpreter):

    uv run --project ..\\seismic_art python scripts\\make_header.py

The band is a convolutional model from seismic_art.header.synthetic_hero: layers folded into a broad
anticline and thinning onto its crest, one normal fault whose throw dies upward, an angular unconformity
with flat layers above. It is not Volve and says so; the story's real seismic is in the echo beat.
Writes story/data/header.json (about 85 kB).
"""

from __future__ import annotations

import argparse
from pathlib import Path

from seismic_art import export_json
from seismic_art.header import synthetic_hero

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--out", type=Path, default=ROOT / "story" / "data" / "header.json")
    a = ap.parse_args()
    payload = synthetic_hero(
        seed=a.seed,
        label="synthetic section: folded layers under an unconformity, one fault; not Volve, no real survey",
    )
    payload["title"] = "Pinpoints and Echoes: the header band"
    path = export_json(a.out, payload)
    print(f"wrote {path} ({path.stat().st_size / 1e3:.0f} kB)")


if __name__ == "__main__":
    main()
