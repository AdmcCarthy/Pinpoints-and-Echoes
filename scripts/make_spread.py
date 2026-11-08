"""Extracts for the interpretation-spread beat: two published versions of the same Volve horizon.

Reads the Volve interpretation zip (not committed) and the ep_geoscience_analytics pick check; writes
story/data/spread.csv, transect.csv and picks.csv. Run with the ep interpreter:

    ..\\ep_geoscience_analytics\\.venv\\Scripts\\python.exe -I scripts\\make_spread.py ^
        --ep ..\\ep_geoscience_analytics --zip C:\\appl\\Volve\\Volve_Geophysical_Interpretations.zip

What the pairs are, and are not: each pair is the same surface from the base survey (ST0202R08, PSDM) and
the reprocessed survey (ST10010). They differ in processing and in picking, so they are two published
answers, not blind interpretations by different people. Time domain (two-way time, ms) only.
Differences are taken at nodes that coincide within 8 m. Distance is to the nearest well pick of any
interpreted surface (the control set of the horizon-to-pick check).
"""

import argparse
import sys
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.spatial import cKDTree

PAIRS = {
    "Ty Fm top": ("Ty_Fm_Top+ST0202R08_PS_PSDM_FULL_PP+STAT+TIME.dat", "Ty_Fm_Top+ST10010_Full+STAT+TIME.dat", "Ty Fm. Top"),
    "Shetland Gp top": ("SHETLAND_GP+ST0202R08_PS_PSDM_FULL_PP+STAT+TIME.dat", "SHETLAND_GP_Top+ST10010ZC11_Full+STAT+TIME.dat", "SHETLAND GP. Top"),
    "Base Cretaceous": ("BCU+ST0202R08_PS_PSDM_FULL_PP+STAT+TIME.dat", "BCU+ST10010ZC11_Full+STAT+TIME.dat", None),
    "Hod Fm top": ("Hod_Fm+ST0202R08_PS_PSDM_FULL_PP+STAT+TIME.dat", "Hod+ST10010_Pz-PSDM-Full+STAT+TIME.dat", "Hod Fm. Top"),
}
BINS = [0, 250, 500, 1000, 2000, np.inf]
LABELS = ["0-250 m", "250-500 m", "0.5-1 km", "1-2 km", "over 2 km"]
MIN_N = 1000  # nodes per bin, below which the bin is not drawn
MATCH_M = 8.0
STEP_M = 50.0


def load(z, names, fn, parse_horizons):
    return parse_horizons(z.read(names[fn]).decode("latin-1"))[0][0]


def paired(a, b):
    """B minus A at coinciding nodes; returns x, y, a_z, b_z."""
    d, i = cKDTree(a[["x", "y"]].to_numpy()).query(b[["x", "y"]].to_numpy())
    m = d < MATCH_M
    return b.x.to_numpy()[m], b.y.to_numpy()[m], a.z.to_numpy()[i[m]], b.z.to_numpy()[m]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ep", required=True, type=Path)
    ap.add_argument("--zip", required=True, type=Path)
    ap.add_argument("--out", type=Path, default=Path(__file__).resolve().parents[1] / "story" / "data")
    a = ap.parse_args()
    sys.path.insert(0, str(a.ep))
    from src.ingest.seismic_interp import parse_horizons  # noqa: E402

    z = zipfile.ZipFile(a.zip)
    names = {n.split("/")[-1]: n for n in z.namelist()}
    wc = pd.read_parquet(a.ep / "data/midlayer/marts/seis_horizon_well_check.parquet")
    ctrl = wc[["easting", "northing"]].dropna().drop_duplicates().to_numpy()
    tree = cKDTree(ctrl)

    rows, cache = [], {}
    for surf, (fa, fb, _) in PAIRS.items():
        A, B = load(z, names, fa, parse_horizons), load(z, names, fb, parse_horizons)
        x, y, za, zb = paired(A, B)
        cache[surf] = (A, B)
        diff = zb - za
        dist = tree.query(np.column_stack([x, y]))[0]
        band = pd.cut(dist, BINS, labels=LABELS, right=False)
        for lab in LABELS:
            s = np.asarray(band == lab)
            if s.sum() >= MIN_N:
                ad = np.abs(diff[s])
                rows.append((surf, lab, int(s.sum()), round(float(np.median(ad)), 2), round(float(np.percentile(ad, 90)), 2),
                             round(float(np.median(diff[s])), 2)))
    spread = pd.DataFrame(rows, columns=["surface", "band", "nodes", "abs_median_ms", "abs_p90_ms", "signed_median_ms"])
    a.out.mkdir(parents=True, exist_ok=True)
    spread.to_csv(a.out / "spread.csv", index=False)

    # transect for Ty Fm top: the longest straight line between two Ty picks that both versions cover
    A, B = cache["Ty Fm top"]
    picks = wc[wc.surface_name == "Ty Fm. Top"][["well", "easting", "northing", "pick_twt_ms"]].dropna()
    ta, tb = cKDTree(A[["x", "y"]].to_numpy()), cKDTree(B[["x", "y"]].to_numpy())
    best = None
    pts = picks[["easting", "northing"]].to_numpy()
    for i in range(len(pts)):
        for j in range(i + 1, len(pts)):
            L = float(np.hypot(*(pts[j] - pts[i])))
            if best is not None and L <= best[0]:
                continue
            n = int(L // STEP_M) + 1
            t = np.linspace(0, 1, n)[:, None]
            line = pts[i] + t * (pts[j] - pts[i])
            if (ta.query(line)[0] < MATCH_M * 2).all() and (tb.query(line)[0] < MATCH_M * 2).all():
                best = (L, i, j)
    L, i, j = best
    n = int(L // STEP_M) + 1
    t = np.linspace(0, 1, n)[:, None]
    line = pts[i] + t * (pts[j] - pts[i])
    za = A.z.to_numpy()[ta.query(line)[1]]
    zb = B.z.to_numpy()[tb.query(line)[1]]
    pd.DataFrame({"dist_m": np.round(np.linspace(0, L, n), 1), "twt_base_ms": np.round(za, 2), "twt_reprocessed_ms": np.round(zb, 2)}).to_csv(
        a.out / "transect.csv", index=False)
    # picks within 150 m of the line, projected onto it
    u = (pts[j] - pts[i]) / L
    rel = picks[["easting", "northing"]].to_numpy() - pts[i]
    along, across = rel @ u, rel @ np.array([-u[1], u[0]])
    near = (np.abs(across) <= 150) & (along >= -50) & (along <= L + 50)
    out = picks[near].assign(dist_m=np.round(along[near], 1), offset_m=np.round(across[near], 1))
    out[["well", "dist_m", "offset_m", "pick_twt_ms"]].round(2).to_csv(a.out / "picks.csv", index=False)
    print(spread.to_string(index=False))
    print(f"transect {L:.0f} m, {n} samples, {near.sum()} picks within 150 m")


if __name__ == "__main__":
    main()
