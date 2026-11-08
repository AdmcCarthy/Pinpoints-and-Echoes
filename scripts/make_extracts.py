"""Write the small, story-sized extracts from the ep_geoscience_analytics mid-layer.

Reads parquet only; writes CSV under story/data/. Run with the ep_geoscience_analytics
interpreter (it has pandas, scipy and pyarrow):

    ..\\ep_geoscience_analytics\\.venv\\Scripts\\python.exe -I scripts\\make_extracts.py ^
        --ep ..\\ep_geoscience_analytics

Assumptions (also stated in data/README.md):
- Positions are wellhead (surface) positions, not bottom-hole. Deviated wells reach other places.
- "Petroleum wellbores" = Sodir well type DEVELOPMENT or EXPLORATION, minus soil drilling,
  shallow gas and scientific purposes. Every wellbore counts, sidetracks included.
- The "study area" is the convex hull of those North Sea wellbore positions, not the sea.
- 1 ms two-way time is converted to depth with the Volve average velocity (a stated parameter).
"""

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.spatial import ConvexHull, cKDTree

R_EARTH_KM = 6371.0088
EXCLUDE_PURPOSE = {"SOIL DRILLING", "SHALLOW GAS", "SCIENTIFIC"}
V_AVG_M_S = 2345.0  # Volve upper average velocity in the check-shot summary (rounded)


def xy_km(lat, lon, lat0):
    """Equirectangular kilometres about lat0; fine at this extent for an area to ~1 %."""
    y = np.radians(lat) * R_EARTH_KM
    x = np.radians(lon) * R_EARTH_KM * np.cos(np.radians(lat0))
    return np.column_stack([x, y])


def wells(ep: Path) -> pd.DataFrame:
    w = pd.read_parquet(ep / "data/midlayer/canonical/well_header.parquet")
    w = w[(w.main_area == "NORTH SEA") & w.lat_etrs89.notna()]
    w = w[w.well_type.isin(["DEVELOPMENT", "EXPLORATION"]) & ~w.purpose.isin(EXCLUDE_PURPOSE)]
    out = pd.DataFrame(
        {
            "wellbore": w.well_name.astype(str),
            "lat": w.lat_etrs89.astype(float).round(5),
            "lon": w.lon_etrs89.astype(float).round(5),
            "year": pd.to_datetime(w.entry_date).dt.year.astype("Int64"),
            "type": w.well_type.astype(str).str.lower(),
            "kind": w.wellbore_kind.astype(str),
        }
    )
    return out.reset_index(drop=True)


def geometry(w: pd.DataFrame, ep: Path) -> pd.DataFrame:
    p = xy_km(w.lat.to_numpy(), w.lon.to_numpy(), w.lat.mean())
    hull = ConvexHull(p)
    first = w[(w.type == "exploration") & (w.kind == "initial")]
    pe = xy_km(first.lat.to_numpy(), first.lon.to_numpy(), w.lat.mean())
    pe = np.unique(np.round(pe, 1), axis=0)  # one point per site (100 m)
    d, _ = cKDTree(pe).query(pe, k=2)
    nn = d[:, 1]
    bits = pd.read_parquet(ep / "data/midlayer/marts/bit_size_interval.parquet")
    open_hole = bits[(bits.hole_state == "open_hole") & (bits.bottom_md_m >= 3000)].bit_size_mm  # reservoir depth, Volve (assumption)
    rows = [
        ("reservoir_hole_mm", float(open_hole.median()), "mm", f"Volve open-hole runs reaching 3,000 m MD or deeper, {len(open_hole)} runs"),
        ("n_wellbores", len(w), "count", "wells.csv"),
        ("n_exploration_sites", len(pe), "count", "exploration wellbores (initial), 100 m cells"),
        ("hull_area_km2", hull.volume, "km2", "convex hull of wellhead positions"),
        ("nn_median_km", float(np.median(nn)), "km", "exploration sites, nearest neighbour"),
        ("nn_p10_km", float(np.percentile(nn, 10)), "km", "exploration sites, nearest neighbour"),
        ("nn_p90_km", float(np.percentile(nn, 90)), "km", "exploration sites, nearest neighbour"),
    ]
    return pd.DataFrame(rows, columns=["key", "value", "unit", "basis"])


def chain(ep: Path) -> pd.DataFrame:
    """Volve error links, each in metres at the target (depth), plus the horizontal one."""
    m = ep / "data/midlayer/marts"
    s = pd.read_parquet(m / "well_survey_check.parquet")
    h = pd.read_parquet(m / "seis_horizon_well_summary.parquet")
    k = pd.read_parquet(m / "well_timedepth_pick_summary.parquet")
    ms_to_m = V_AVG_M_S / 2 / 1000  # metres of depth per ms of two-way time
    rows = []

    def add(link, axis, typical, worst, unit, basis, confidence):
        rows.append((link, axis, round(float(typical), 2), round(float(worst), 2), unit, basis, confidence))

    add("Well position (horizontal)", "horizontal", s.sigma_lateral_end_m.median(),
        s.sigma_lateral_end_m.max(), "m", "Volve survey covariance at end of survey, 26 surveys; "
        "unit and confidence level not stated in the export", "Observed")
    add("Well depth (vertical position)", "vertical", s.sigma_vertical_end_m.median(),
        s.sigma_vertical_end_m.max(), "m", "same surveys, vertical", "Observed")
    ref = s.rt_used_m.dropna()
    add("Depth reference (rotary table to sea level)", "vertical", 0.0, ref.median(), "m",
        "a mixed-up reference shifts every depth by the rotary-table elevation", "Observed")
    kk = k.dropna(subset=["residual_abs_max_ms"])
    add("Time-depth tie (check-shot residual)", "vertical",
        (kk.residual_median_ms.abs() * ms_to_m).median(), kk.residual_abs_max_ms.max() * ms_to_m,
        "m", f"pick residuals against check shots, ms converted at {V_AVG_M_S:.0f} m/s", "Derived")
    d = h[(h.domain == "DEPTH") & h.surface_name.str.contains("Hugin")]
    add("Horizon against well picks (reservoir)", "vertical", d.mistie_median.abs().median(),
        d.mistie_abs_max.max(), "m", "Volve Hugin top and base, depth horizons already adjusted to wells",
        "Derived")
    return pd.DataFrame(rows, columns=["link", "axis", "typical", "worst", "unit", "basis", "confidence"])


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ep", required=True, type=Path)
    ap.add_argument("--out", type=Path, default=Path(__file__).resolve().parents[1] / "story" / "data")
    a = ap.parse_args()
    a.out.mkdir(parents=True, exist_ok=True)
    w = wells(a.ep)
    w.to_csv(a.out / "wells.csv", index=False)
    g = geometry(w, a.ep)
    g.to_csv(a.out / "geometry.csv", index=False)
    chain(a.ep).to_csv(a.out / "chain.csv", index=False)
    print(g.to_string(index=False))
    print(chain(a.ep).drop(columns="basis").to_string(index=False))


if __name__ == "__main__":
    main()
