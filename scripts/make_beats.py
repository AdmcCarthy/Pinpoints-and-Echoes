"""Extracts for the observation, tie, echo (wedge), depth, volumes and test beats.

Run with the ep_geoscience_analytics interpreter (pandas, scipy, pyarrow):

    ..\\ep_geoscience_analytics\\.venv\\Scripts\\python.exe -I scripts\\make_beats.py ^
        --ep ..\\ep_geoscience_analytics --volve C:\\appl\\Volve --surfaces ..\\volve-surfaces

Inputs (none committed): the Volve well-log zip (one LAS file of 15/9-F-11 T2), the ep mid-layer
(check-shot tables, reserves snapshots, field master), volve-surfaces closures.json and contacts.json, and
story/data/section.json written by make_seismic.py (for the dominant frequency).

Assumptions are stated next to the code and repeated in data/README.md:
- The well is 15/9-F-11 T2 throughout. Its time-depth table is check shot 1 (the near-offset survey).
- Sonic DT (us/ft) and bulk density give acoustic impedance; where either is missing the reflectivity is zero
  and the gap is recorded. The wavelet is a zero-phase Ricker at the centroid frequency of the real data
  around the reservoir. No stretch or squeeze is applied to the synthetic; a single bulk shift is reported.
- The wedge is synthetic: two interfaces of equal and opposite reflectivity at the log's reservoir velocity.
- The depth fan reads every Volve check-shot table at one two-way time that all of them cover.
- Closure area against depth is the Volve high on the Hugin top depth surface from volve-surfaces, which is an
  interpreted and smoothed surface; the contact distribution is the 2005 plan for development (PUD) as
  digitised there.
- The volume simulation is illustrative: its parameters are chosen for the story and listed; it is not a
  Volve estimate.
"""

import argparse
import io
import json
import re
from pathlib import Path

import numpy as np
import pandas as pd

WELL = "15/9-F-11 T2"
LAS_MEMBER = "Well_logs_pr_WELL/15_9-F-11 T2/05.PETROPHYSICAL INTERPRETATION/WLC_PETRO_COMPUTED_INPUT_1.LAS"
CHECKSHOT = "TZV_TIME_CHECKSHOT_1"
HUGIN_TVDSS = (3181.5, 3282.84)  # pick depths of the Hugin top and base in this well (ep pick table)
LOG_TVDSS = (2300.0, 3320.0)  # window kept for the composite log
FAN_TWT = 2650.0  # ms, covered by every table
SEED = 7
N_SIM = 20000


def read_las(text: str) -> pd.DataFrame:
    head, _, body = text.partition("~A")
    cur = head.split("~C")[1].split("~")[0]
    names = [re.match(r"\s*([A-Za-z0-9_\-]+)\s*\.", l).group(1) for l in cur.splitlines() if re.match(r"\s*[A-Za-z0-9_\-]+\s*\.", l)]
    body = body.split("\n", 1)[1]
    d = pd.read_csv(io.StringIO(body), sep=r"\s+", header=None, names=names, na_values=[-999.25, "-999.25"], engine="c")
    return d


def ricker(f_hz: float, dt_ms: float, half_ms: float = 100.0) -> np.ndarray:
    t = np.arange(-half_ms, half_ms + dt_ms, dt_ms) / 1000.0
    a = (np.pi * f_hz * t) ** 2
    return (1 - 2 * a) * np.exp(-a)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ep", required=True, type=Path)
    ap.add_argument("--volve", required=True, type=Path)
    ap.add_argument("--surfaces", required=True, type=Path)
    ap.add_argument("--out", type=Path, default=Path(__file__).resolve().parents[1] / "story" / "data")
    a = ap.parse_args()
    out = a.out
    marts = a.ep / "data/midlayer/marts"
    notes = {}

    # ---- time-depth of the well (check shot 1) and the composite log
    td_all = pd.read_parquet(marts / "well_timedepth.parquet")
    td = td_all[td_all.member.str.contains(WELL.replace("/", "_").replace(" ", " ")) & td_all.member.str.contains(CHECKSHOT)]
    td = td.sort_values("md_m")
    md2tvd = lambda md: np.interp(md, td.md_m, td.tvdss_m)
    md2twt = lambda md: np.interp(md, td.md_m, td.twt_ms)

    import zipfile

    z = zipfile.ZipFile(a.volve / "Volve_Well_logs_pr_WELL.zip")
    las = read_las(z.read(LAS_MEMBER).decode("latin-1"))
    las["tvdss_m"] = md2tvd(las.DEPTH)
    las["twt_ms"] = md2twt(las.DEPTH)
    inwin = (las.tvdss_m >= LOG_TVDSS[0]) & (las.tvdss_m <= LOG_TVDSS[1]) & (las.DEPTH >= td.md_m.min()) & (las.DEPTH <= td.md_m.max())
    L = las[inwin].copy()
    log = L.iloc[::5][["DEPTH", "tvdss_m", "twt_ms", "GR", "RHOB", "NPHI", "RT", "DT"]].rename(columns={"DEPTH": "md_m", "GR": "gr_api", "RHOB": "rhob_g_cm3", "NPHI": "nphi_v_v", "RT": "rt_ohm_m", "DT": "dt_us_ft"})
    log.round({"md_m": 2, "tvdss_m": 2, "twt_ms": 2, "gr_api": 1, "rhob_g_cm3": 3, "nphi_v_v": 3, "rt_ohm_m": 2, "dt_us_ft": 1}).to_csv(out / "log.csv", index=False)
    step_m = float(np.median(np.diff(las.DEPTH)))
    notes["log"] = {"well": WELL, "hugin_tvdss": list(HUGIN_TVDSS), "hugin_thickness_m": round(HUGIN_TVDSS[1] - HUGIN_TVDSS[0], 1), "las": LAS_MEMBER.split("/")[-1], "sample_m": step_m, "rows_kept": int(len(log)),
                    "md_range": [float(L.DEPTH.min()), float(L.DEPTH.max())], "coverage": {c: float(L[c].notna().mean()) for c in ["GR", "RHOB", "NPHI", "RT", "DT"]}}

    # ---- synthetic seismogram from the log, against the real trace at the well
    sec = json.loads((out / "section.json").read_text())
    f_hz = float(sec["centroid_hz"])
    v = 304800.0 / L.DT  # us/ft -> m/s
    ai = (v * L.RHOB).to_numpy()
    rc = np.zeros(len(L))
    ok = np.isfinite(ai[1:]) & np.isfinite(ai[:-1])
    rc[1:][ok] = (ai[1:][ok] - ai[:-1][ok]) / (ai[1:][ok] + ai[:-1][ok])
    twt = L.twt_ms.to_numpy()
    dt = 1.0
    grid = np.arange(np.floor(twt.min()), np.ceil(twt.max()) + dt, dt)
    rc_t = np.zeros(len(grid))
    np.add.at(rc_t, np.clip(np.round((twt - grid[0]) / dt).astype(int), 0, len(grid) - 1), rc)
    w = ricker(f_hz, dt)
    syn = np.convolve(rc_t, w, mode="same")
    tr = pd.read_csv(out / "trace.csv")
    syn4 = np.interp(tr.t_ms, grid, syn, left=0.0, right=0.0)
    win = (tr.t_ms >= 2300) & (tr.t_ms <= 3100)
    s_rms = np.sqrt(np.mean(syn4[win] ** 2)) or 1.0
    r_rms = np.sqrt(np.mean(tr.amp[win] ** 2))
    syn4 = syn4 / s_rms * r_rms
    # correlation at zero lag and the best bulk shift within +-40 ms (no stretch)
    def corr(lag):
        s = np.roll(syn4, lag)
        return float(np.corrcoef(s[win], tr.amp[win])[0, 1])
    lags = range(-10, 11)  # 4 ms samples
    cc = {lag * 4: corr(lag) for lag in lags}
    best_lag = max(cc, key=cc.get)
    worst_lag = min(cc, key=cc.get)
    sign = 1
    if -cc[worst_lag] > cc[best_lag]:  # the opposite polarity matches better
        sign, best_lag = -1, worst_lag
    syn4 = sign * syn4
    tie = pd.DataFrame({"t_ms": tr.t_ms, "real": tr.amp.round(4), "synthetic": np.round(syn4, 4), "synthetic_shifted": np.round(np.roll(syn4, best_lag // 4), 4)})
    tie.to_csv(out / "tie.csv", index=False)
    rc_cov = float(np.mean(np.isfinite(ai)))
    notes["tie"] = {"wavelet_hz": f_hz, "corr_zero_lag": round(sign * cc[0], 3), "best_shift_ms": best_lag, "corr_best": round(abs(cc[best_lag]), 3), "sign": sign,
                    "impedance_coverage": rc_cov, "window_ms": [2300, 3100],
                    "polarity": "the data's polarity is not stated; the synthetic is drawn with whichever sign matches better, and that sign is reported"}

    # ---- the published horizons along the extracted inline (for the section figure)
    import sys
    sys.path.insert(0, str(a.ep))
    from src.ingest.seismic_interp import parse_horizons  # noqa: E402
    zi = zipfile.ZipFile(a.volve / "Volve_Geophysical_Interpretations.zip")
    names = {n.split("/")[-1]: n for n in zi.namelist()}
    hz_files = {"Ty Fm top": "Ty_Fm_Top+ST10010_Full+STAT+TIME.dat", "Shetland Gp top": "SHETLAND_GP_Top+ST10010ZC11_Full+STAT+TIME.dat",
                "Base Cretaceous": "BCU+ST10010ZC11_Full+STAT+TIME.dat", "Hugin Fm top": "Hugin_Fm_Top+ST10010ZC11_Near_190314+STAT+TIME.dat",
                "Hugin Fm base": "Hugin_Fm_Base+ST10010ZC11_Near_190314+STAT+TIME.dat"}
    hrows = []
    xls = np.array(sec["crosslines"])
    for label, fn in hz_files.items():
        d = parse_horizons(zi.read(names[fn]).decode("latin-1"))[0][0]
        d = d[d.inline == sec["inline"]].set_index("crossline").z
        for xl in xls:
            if xl in d.index:
                hrows.append((label, int(xl), round(float(d.loc[xl]), 1)))
    pd.DataFrame(hrows, columns=["horizon", "crossline", "twt_ms"]).to_csv(out / "horizons.csv", index=False)
    notes["horizons"] = {k: int(sum(1 for r in hrows if r[0] == k)) for k in hz_files}

    # ---- the wedge (synthetic)
    hug = L[(L.tvdss_m >= HUGIN_TVDSS[0]) & (L.tvdss_m <= HUGIN_TVDSS[1])]
    v_res = float(np.nanmedian(304800.0 / hug.DT))
    thick = np.arange(0, 81, 1.0)
    tgrid = np.arange(0, 200.0, 1.0)
    wav = ricker(f_hz, 1.0, half_ms=99.0)  # odd length, so "same" convolution keeps the grid length
    amp = np.zeros((len(thick), len(tgrid)))
    appar = np.zeros(len(thick))
    for i, h in enumerate(thick):
        r = np.zeros(len(tgrid))
        t_top = 60.0
        t_base = t_top + 2 * h / v_res * 1000
        r[int(round(t_top))] += 1.0
        if int(round(t_base)) < len(tgrid):
            r[int(round(t_base))] -= 1.0
        s = np.convolve(r, wav, mode="same")
        amp[i] = s
        i_top = int(np.argmax(s[: int(t_top) + 40]))
        i_base = int(np.argmin(s[i_top:])) + i_top

        def refine(k):  # parabolic peak position between samples
            if 0 < k < len(s) - 1 and (s[k - 1] - 2 * s[k] + s[k + 1]) != 0:
                return k + 0.5 * (s[k - 1] - s[k + 1]) / (s[k - 1] - 2 * s[k] + s[k + 1])
            return float(k)

        appar[i] = (refine(i_base) - refine(i_top)) / 1000 * v_res / 2
    peak = amp.max(axis=1)
    tuning = float(thick[np.argmax(peak)])
    quarter = v_res / (4 * f_hz)
    sc = float(np.abs(amp).max())
    wedge = {"f_hz": f_hz, "v_m_s": round(v_res), "thickness_m": thick.tolist(), "t_ms": tgrid.tolist(), "top_ms": 60.0,
             "amp": np.round(amp / sc, 3).tolist(), "peak_amp": np.round(peak / sc, 3).tolist(), "apparent_m": np.round(appar, 1).tolist(),
             "tuning_m": tuning, "quarter_wavelength_m": round(quarter, 1), "note": "synthetic: two interfaces of equal and opposite reflectivity"}
    (out / "wedge.json").write_text(json.dumps(wedge, separators=(",", ":")))
    notes["wedge"] = {"v_m_s": round(v_res), "tuning_m": tuning, "quarter_wavelength_m": round(quarter, 1), "f_hz": f_hz}

    # ---- the depth fan from every check-shot table
    rows = []
    labels = {}
    for mem, g in td_all.groupby("member"):
        well = g.wellbore_name.iloc[0] or mem.split("/")[1].replace("_", "/", 1)
        short = mem.split("/")[-1].replace(".ASC", "").replace(".LIST", "").replace("TZV_TIME_", "").replace("STATOIL_", "")
        labels[mem] = f"{well} {short}"
        g = g.sort_values("twt_ms")
        for _, r in g.iloc[:: max(1, len(g) // 60)].iterrows():
            rows.append((labels[mem], round(r.twt_ms, 1), round(r.tvdss_m, 1)))
        if g.twt_ms.min() <= FAN_TWT <= g.twt_ms.max():
            rows.append((labels[mem], FAN_TWT, round(float(np.interp(FAN_TWT, g.twt_ms, g.tvdss_m)), 1)))
    tdf = pd.DataFrame(rows, columns=["table", "twt_ms", "tvdss_m"]).drop_duplicates().sort_values(["table", "twt_ms"])
    tdf.to_csv(out / "timedepth.csv", index=False)
    at = tdf[tdf.twt_ms == FAN_TWT]
    notes["fan"] = {"twt_ms": FAN_TWT, "n_tables": int(len(at)), "depth_min": float(at.tvdss_m.min()), "depth_max": float(at.tvdss_m.max()),
                    "wells": sorted(set(t.split(" ")[0] + " " + t.split(" ")[1] for t in at.table))}

    # ---- closure area against depth, and the published contact distribution
    cl = json.loads((a.surfaces / "data/out/closures.json").read_text())["horizons"]["hugin_top_depth"]["highs"]
    main_high = max((h for h in cl if h.get("curve")), key=lambda h: h["relief"])
    curve = pd.DataFrame({"depth_m": main_high["curve"]["depth"], "area_km2": main_high["curve"]["area_km2"]})
    curve.to_csv(out / "closure.csv", index=False)
    ct = json.loads((a.surfaces / "data/out/contacts.json").read_text())
    txt = json.dumps(ct)
    m = re.search(r'"quantiles":\s*(\{[^}]*"exceedance":\s*\{[^}]*\}[^}]*\})', txt)
    q = json.loads(m.group(1))
    exc = {float(k): v for k, v in q["exceedance"].items()}
    depths = sorted(exc)
    probs = [exc[d] - (exc[depths[i + 1]] if i + 1 < len(depths) else 0) for i, d in enumerate(depths)]
    contact = pd.DataFrame({"depth_m": depths, "exceedance_pct": [exc[d] for d in depths], "probability_pct": probs})
    contact.to_csv(out / "contact.csv", index=False)
    area_at = lambda d: float(np.interp(d, curve.depth_m, curve.area_km2, right=np.nan))
    notes["closure"] = {"high": main_high["id"], "crest_m": main_high["z"], "spill_m": main_high["spill"]["z"], "spill_kind": main_high["spill"]["kind"],
                        "curve_max_depth": float(curve.depth_m.max()), "P90": q["P90"], "P50": q["P50"], "P10": q["P10"],
                        "area_P90": area_at(q["P90"]), "area_P50": area_at(q["P50"]), "area_base_3120": area_at(3120)}

    # ---- the volume simulation (illustrative; parameters chosen for the story)
    rng = np.random.default_rng(SEED)
    pc = rng.choice(depths, size=N_SIM, p=np.array(probs) / 100)
    pc = np.minimum(pc, curve.depth_m.max())  # the surface is not mapped deeper; capped and declared
    area = np.interp(pc, curve.depth_m, curve.area_km2) * 1e6  # m2
    pay = rng.triangular(15, 30, 50, N_SIM)  # m, average net pay (parameter)
    phi = rng.triangular(0.16, 0.20, 0.24, N_SIM)  # porosity (parameter)
    sw = rng.triangular(0.25, 0.35, 0.50, N_SIM)  # water saturation (parameter)
    bo = rng.triangular(1.15, 1.25, 1.35, N_SIM)  # formation volume factor (parameter)
    rf = rng.triangular(0.30, 0.40, 0.50, N_SIM)  # recovery factor (parameter)
    rec = area * pay * phi * (1 - sw) / bo * rf / 1e6  # Mn Sm3
    pcts = np.arange(1, 100)
    exceed = pd.DataFrame({"exceedance_pct": pcts, "recoverable_mn_sm3": np.round(np.percentile(rec, 100 - pcts), 3)})
    exceed.to_csv(out / "volumes.csv", index=False)
    notes["volumes"] = {"n": N_SIM, "seed": SEED, "P90": float(np.percentile(rec, 10)), "P50": float(np.percentile(rec, 50)), "P10": float(np.percentile(rec, 90)),
                        "area_share_capped": float(np.mean(pc >= curve.depth_m.max())),
                        "params": {"pay_m": [15, 30, 50], "phi": [0.16, 0.20, 0.24], "sw": [0.25, 0.35, 0.50], "bo": [1.15, 1.25, 1.35], "rf": [0.30, 0.40, 0.50]}}

    # ---- the test: Sodir's own estimate of Volve over time, and every field's first-to-latest revision
    rs = pd.read_parquet(a.ep / "data/midlayer/canonical/reserves_snapshot.parquet")
    rs = rs[(rs.entity_type == "field") & (rs.rc_group == "RC_ALL")]
    volve = rs[rs.entity_name.str.upper() == "VOLVE"].sort_values("snapshot_year")
    volve[["snapshot_year", "recoverable_oe_sm3", "remaining_oe_sm3"]].to_csv(out / "volve_reserves.csv", index=False)
    fm = pd.read_parquet(a.ep / "data/midlayer/canonical/field_master.parquet")
    pdo = fm.dropna(subset=["pdo_approved_date"]).assign(pdo_year=lambda d: pd.to_datetime(d.pdo_approved_date).dt.year)
    pdo = pdo.assign(key=pdo.field_name.str.upper())[["key", "pdo_year"]].drop_duplicates("key")
    r = rs.assign(key=rs.entity_name.str.upper()).merge(pdo, on="key", how="inner")
    r = r[r.snapshot_year >= r.pdo_year - 1]
    g = r.sort_values("snapshot_year").groupby("key")
    rev = pd.DataFrame({"first_year": g.snapshot_year.first(), "first_oe": g.recoverable_oe_sm3.first(), "latest_year": g.snapshot_year.last(),
                        "latest_oe": g.recoverable_oe_sm3.last(), "n_years": g.size(), "pdo_year": g.pdo_year.first()})
    rev = rev[(rev.first_year <= rev.pdo_year + 1) & (rev.n_years >= 5) & (rev.first_oe > 0)]
    rev["ratio"] = rev.latest_oe / rev.first_oe
    rev = rev.reset_index().rename(columns={"key": "field"}).sort_values("ratio")
    rev.round({"ratio": 3}).to_csv(out / "revisions.csv", index=False)
    notes["revisions"] = {"n_fields": int(len(rev)), "median_ratio": float(rev.ratio.median()), "p10": float(rev.ratio.quantile(0.1)), "p90": float(rev.ratio.quantile(0.9)),
                          "share_up": float((rev.ratio > 1.05).mean()), "share_down": float((rev.ratio < 0.95).mean()),
                          "volve_first": float(volve.recoverable_oe_sm3.iloc[0]), "volve_max": float(volve.recoverable_oe_sm3.max()), "volve_latest": float(volve.recoverable_oe_sm3.iloc[-1])}

    (out / "beats_notes.json").write_text(json.dumps(notes, indent=1))
    print(json.dumps(notes, indent=1))


if __name__ == "__main__":
    main()
