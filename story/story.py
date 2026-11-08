"""Metrics and derived datasets for Pinpoints and Echoes.

Inputs are the small extracts written by scripts/make_extracts.py, make_spread.py, make_seismic.py and
make_beats.py. Every number in the prose comes from here, with its method, source and confidence.
"""

import math

from subscout import metric

SODIR = "sodir"
VOLVE = "volve"
V_AVG = 2345.0  # m/s, Volve upper average velocity in the check-shot summary (rounded); stated on the page
MS_TO_M = V_AVG / 2 / 1000  # metres of depth per ms of two-way time


def _g(d, key):
    return float(d["geometry"].set_index("key").value[key])


def datasets(d):
    c = d["chain"]
    v = c[c.axis == "vertical"].copy()
    v["cum_typical"] = (v.typical**2).cumsum() ** 0.5  # independent errors add in quadrature
    v["cum_worst"] = (v.worst**2).cumsum() ** 0.5
    vr = d["volve_reserves"].assign(series="Volve", recoverable_mn_sm3=lambda x: x.recoverable_oe_sm3 / 1e6)
    rev = d["revisions"].assign(
        decade=lambda x: (x.pdo_year // 10 * 10).astype(int).astype(str) + "s", field_label=lambda x: x.field.str.title(), ratio_pct=lambda x: x.ratio * 100
    )
    return {"stack": v.reset_index(drop=True), "volve_hist": vr, "revisions_dec": rev}


def scale_metrics(d):
    n = _g(d, "n_wellbores")
    area = _g(d, "hull_area_km2")
    hole_m = _g(d, "reservoir_hole_mm") / 1000
    nn_m = _g(d, "nn_median_km") * 1000
    cross_km2 = n * math.pi * (hole_m / 2) ** 2 / 1e6
    return {
        "n_wellbores": metric(int(n), "Petroleum wellbores (development and exploration, sidetracks included) with a wellhead position in the Norwegian North Sea", SODIR, "observed"),
        "hole_cm": metric(hole_m * 100, "Median open-hole diameter of Volve runs reaching 3,000 m MD or deeper, cm", VOLVE, "derived", "cm"),
        "one_in": metric(area / cross_km2, "Area spanned by the wellheads (convex hull) divided by the summed cross-sections of the wellbores at that diameter", SODIR, "derived"),
        "nn_km": metric(nn_m / 1000, "Median distance from an exploration well to the nearest other exploration site (wellhead positions, 100 m cells), km", SODIR, "derived", "km"),
        "nn_p10": metric(_g(d, "nn_p10_km"), "10th percentile of the same distance, km", SODIR, "derived", "km"),
        "nn_p90": metric(_g(d, "nn_p90_km"), "90th percentile of the same distance, km", SODIR, "derived", "km"),
        "spacing_ratio": metric(nn_m / hole_m, "Median distance to the nearest exploration site divided by the hole diameter", SODIR, "derived"),
        "coin_m": metric(nn_m / hole_m * 0.01, "If the wellbore were a 1 cm coin, the median distance to the nearest exploration site, m", SODIR, "derived", "m"),
        "coin_span_km": metric(math.sqrt(area) * 1000 / hole_m * 0.01 / 1000, "If the wellbore were a 1 cm coin, the side of a square of the area spanned, km", SODIR, "derived", "km"),
    }


def log_metrics(d):
    n = d["notes"]
    L, T, W, S = n["log"], n["tie"], n["wedge"], d["section"]
    hz = d["horizons"]
    i_well = min(range(len(S["dist_m"])), key=lambda i: abs(S["dist_m"][i] - S["well_dist_m"]))
    xl = S["crosslines"][i_well]
    row = hz[(hz.horizon == "Hugin Fm top") & (hz.crossline == xl)]
    t_hugin = float(row.twt_ms.iloc[0]) if len(row) else float("nan")
    return {
        "log_sample_cm": metric(round(L["sample_m"] * 100), "Depth sampling of the composite log, cm", VOLVE, "observed", "cm"),
        "log_span_m": metric(L["md_range"][1] - L["md_range"][0], "Measured depth covered by the log window shown, m", VOLVE, "observed", "m"),
        "hugin_thickness": metric(L["hugin_thickness_m"], "Vertical thickness of the Hugin Fm at the well, from the interpreters' top and base picks, m", VOLVE, "observed", "m"),
        "hugin_top_tvdss": metric(L["hugin_tvdss"][0], "Hugin Fm top pick at the well, m below MSL", VOLVE, "observed", "m"),
        "hugin_twt_s": metric(t_hugin / 1000, "Two-way time of the published Hugin top horizon at the well, s", VOLVE, "observed", "s"),
        "inline": metric(S["inline"], "ST10010 inline through the well", VOLVE, "observed"),
        "n_traces": metric(len(S["crosslines"]) * 2, "Traces on the inline (every second one drawn)", VOLVE, "observed"),
        "dom_hz": metric(S["centroid_hz"], "Centroid frequency of the amplitude spectrum, 41 traces about the well, 2,300 to 3,100 ms", VOLVE, "derived", "Hz"),
        "v_res": metric(W["v_m_s"], "Median sonic velocity of the Hugin Fm at the well, m/s", VOLVE, "derived", "m/s"),
        "quarter_m": metric(W["quarter_wavelength_m"], "A quarter of the dominant wavelength at that velocity and frequency, m", VOLVE, "derived", "m"),
        "tuning_m": metric(W["tuning_m"], "Bed thickness at which the synthetic wedge's top and base echoes merge (peak amplitude), m", VOLVE, "derived", "m"),
        "tie_corr": metric(T["corr_best"], "Correlation of the synthetic and the real trace, 2,300 to 3,100 ms, after one bulk shift", VOLVE, "derived"),
        "tie_shift": metric(abs(T["best_shift_ms"]), "Bulk shift applied to the synthetic, ms", VOLVE, "derived", "ms"),
        "tie_zero": metric(T["corr_zero_lag"], "The same correlation with no shift", VOLVE, "derived"),
        "ai_cover": metric(T["impedance_coverage"], "Share of the log window with both sonic and density, so with a reflectivity", VOLVE, "observed"),
    }


def spread_metrics(d):
    t, sp, pk = d["transect"], d["spread"], d["picks"]
    gap = (t.twt_reprocessed_ms - t.twt_base_ms).abs()
    near = sp[sp.band == "0-250 m"].abs_median_ms
    far = sp[sp.band == "over 2 km"].abs_median_ms
    idx = [(t.dist_m - p).abs().idxmin() for p in pk.dist_m]
    miss_a = t.twt_base_ms.loc[idx].to_numpy() - pk.pick_twt_ms.to_numpy()
    miss_b = t.twt_reprocessed_ms.loc[idx].to_numpy() - pk.pick_twt_ms.to_numpy()
    return {
        "miss_base": metric(float(abs(miss_a).mean()), "Mean absolute miss of the base version against the well picks near the line, ms TWT; pick times come from the check-shot table", VOLVE, "derived", "ms"),
        "miss_repro": metric(float(abs(miss_b).mean()), "Mean absolute miss of the reprocessed version against the same picks, ms TWT", VOLVE, "derived", "ms"),
        "n_versions": metric(int(sp.surface.nunique()), "Surfaces with two published versions compared", VOLVE, "derived"),
        "line_km": metric(float(t.dist_m.max() / 1000), "Length of the line between two Ty Fm top picks, km", VOLVE, "derived", "km"),
        "n_picks_line": metric(int(len(pk)), "Well picks within 150 m of the line", VOLVE, "observed"),
        "gap_max_ms": metric(float(gap.max()), "Largest difference between the two versions along the line, ms TWT", VOLVE, "derived", "ms"),
        "gap_max_m": metric(float(gap.max() * MS_TO_M), f"The same in depth at {V_AVG:.0f} m/s, m", VOLVE, "interpreted", "m"),
        "gap_med_ms": metric(float(gap.median()), "Median difference along the line, ms TWT", VOLVE, "derived", "ms"),
        "near_lo": metric(float(near.min()), "Smallest median difference within 250 m of a well pick, over the surfaces, ms", VOLVE, "derived", "ms"),
        "near_hi": metric(float(near.max()), "Largest median difference within 250 m of a well pick, over the surfaces, ms", VOLVE, "derived", "ms"),
        "far_lo": metric(float(far.min()), "Smallest median difference beyond 2 km of a well pick (surfaces with enough nodes), ms", VOLVE, "derived", "ms"),
        "far_hi": metric(float(far.max()), "Largest median difference beyond 2 km of a well pick (surfaces with enough nodes), ms", VOLVE, "derived", "ms"),
        "n_far": metric(int(len(far)), "Surfaces with enough nodes beyond 2 km to compare", VOLVE, "derived"),
    }


def chain_metrics(d):
    c = d["chain"].set_index("link")
    s = d["stack"]
    row = lambda k: c[c.index.str.startswith(k)].iloc[0]  # noqa: E731
    return {
        "pos_h": metric(float(row("Well position").typical), "Median horizontal position uncertainty at the end of 26 Volve surveys, m; the export states neither the unit nor the confidence level (square root of covariance taken as sigma in feet)", VOLVE, "observed", "m"),
        "pos_h_max": metric(float(row("Well position").worst), "Largest of those 26, m", VOLVE, "observed", "m"),
        "rt_m": metric(float(row("Depth reference").worst), "Rotary-table elevation of the F wells above sea level, m", VOLVE, "observed", "m"),
        "stack_typical": metric(float(s.cum_typical.iloc[-1]), "Typical vertical errors combined in quadrature, m (independence assumed)", VOLVE, "interpreted", "m"),
        "stack_worst": metric(float(s.cum_worst.iloc[-1]), "Largest vertical errors on file combined in quadrature, m (independence assumed; the depth reference is a systematic offset, so this is a bound, not a forecast)", VOLVE, "interpreted", "m"),
        "n_links": metric(int(len(s)), "Vertical links in the chain of errors", VOLVE, "derived"),
    }


def depth_volume_metrics(d):
    n = d["notes"]
    F, C, V, R = n["fan"], n["closure"], n["volumes"], n["revisions"]
    vr = d["volve_reserves"].sort_values("snapshot_year")
    peak = vr.loc[vr.recoverable_oe_sm3.idxmax()]
    low = vr.loc[vr.recoverable_oe_sm3.idxmin()]
    rev = d["revisions"]
    return {
        "fan_twt_s": metric(F["twt_ms"] / 1000, "Two-way time at which every check-shot table is read, s", VOLVE, "derived", "s"),
        "fan_n": metric(F["n_tables"], "Check-shot tables in the Volve release", VOLVE, "observed"),
        "fan_wells": metric(len(F["wells"]), "Wellbore folders those tables belong to", VOLVE, "observed"),
        "fan_min": metric(F["depth_min"], "Shallowest depth any table gives for that time, m below MSL", VOLVE, "observed", "m"),
        "fan_max": metric(F["depth_max"], "Deepest depth any table gives for that time, m below MSL", VOLVE, "observed", "m"),
        "fan_range": metric(F["depth_max"] - F["depth_min"], "Spread of depth for one two-way time across the tables, m", VOLVE, "derived", "m"),
        "owc_p90": metric(C["P90"], "Oil-water contact, P90 (low case) in the 2005 plan for development, m below MSL", VOLVE, "observed", "m"),
        "owc_p50": metric(C["P50"], "Oil-water contact, P50 in the 2005 plan for development, m below MSL", VOLVE, "observed", "m"),
        "owc_p10": metric(C["P10"], "Oil-water contact, P10 (high case) in the 2005 plan for development, m below MSL", VOLVE, "observed", "m"),
        "area_p90": metric(C["area_P90"], "Closure area at the P90 contact, km² (smoothed Hugin top surface)", VOLVE, "interpreted", "km²"),
        "area_p50": metric(C["area_P50"], "Closure area at the P50 contact, km²", VOLVE, "interpreted", "km²"),
        "area_ratio": metric(C["area_P50"] / C["area_P90"], "Closure area at P50 divided by that at P90", VOLVE, "interpreted"),
        "owc_step": metric(C["P50"] - C["P90"], "Depth between the P90 and P50 contacts, m", VOLVE, "derived", "m"),
        "vol_p90": metric(V["P90"], "Simulated recoverable oil, P90 (low), Mn Sm³; illustrative parameters listed on the page", VOLVE, "interpreted", "Mn Sm³"),
        "vol_p50": metric(V["P50"], "Simulated recoverable oil, P50, Mn Sm³", VOLVE, "interpreted", "Mn Sm³"),
        "vol_p10": metric(V["P10"], "Simulated recoverable oil, P10 (high), Mn Sm³", VOLVE, "interpreted", "Mn Sm³"),
        "vol_ratio": metric(V["P10"] / V["P90"], "Simulated P10 divided by P90", VOLVE, "interpreted"),
        "sim_n": metric(V["n"], "Draws in the simulation", VOLVE, "derived"),
        "capped": metric(V["area_share_capped"], "Share of draws whose contact lies deeper than the mapped surface and takes its deepest area", VOLVE, "derived"),
        "volve_first_yr": metric(int(vr.snapshot_year.iloc[0]), "First Sodir snapshot year for Volve", SODIR, "observed"),
        "volve_first": metric(vr.recoverable_oe_sm3.iloc[0] / 1e6, "Sodir's recoverable estimate for Volve in that year, Mn Sm³ o.e.", SODIR, "observed", "Mn Sm³"),
        "volve_peak_yr": metric(int(peak.snapshot_year), "Year of the highest estimate", SODIR, "observed"),
        "volve_peak": metric(peak.recoverable_oe_sm3 / 1e6, "Highest Sodir estimate for Volve, Mn Sm³ o.e.", SODIR, "observed", "Mn Sm³"),
        "volve_low_yr": metric(int(low.snapshot_year), "Year of the lowest estimate", SODIR, "observed"),
        "volve_low": metric(low.recoverable_oe_sm3 / 1e6, "Lowest Sodir estimate for Volve, Mn Sm³ o.e.", SODIR, "observed", "Mn Sm³"),
        "volve_latest_yr": metric(int(vr.snapshot_year.iloc[-1]), "Latest snapshot year", SODIR, "observed"),
        "volve_latest": metric(vr.recoverable_oe_sm3.iloc[-1] / 1e6, "Latest Sodir estimate for Volve, Mn Sm³ o.e. (the field is produced out)", SODIR, "observed", "Mn Sm³"),
        "volve_swing": metric(peak.recoverable_oe_sm3 / low.recoverable_oe_sm3, "Highest estimate divided by lowest", SODIR, "derived"),
        "rev_n": metric(R["n_fields"], "Fields with a plan approved since 2003, at least five Sodir snapshots, and a first snapshot within a year of approval", SODIR, "derived"),
        "rev_median": metric(R["median_ratio"], "Median of latest estimate divided by first estimate", SODIR, "derived"),
        "rev_p10": metric(R["p10"], "10th percentile of that ratio", SODIR, "derived"),
        "rev_p90": metric(R["p90"], "90th percentile of that ratio", SODIR, "derived"),
        "rev_up": metric(R["share_up"], "Share of fields whose estimate grew by more than 5%", SODIR, "derived"),
        "rev_down": metric(R["share_down"], "Share of fields whose estimate fell by more than 5%", SODIR, "derived"),
        "rev_halved": metric(float((rev.ratio < 0.5).mean()), "Share of fields whose estimate at least halved", SODIR, "derived"),
        "rev_doubled": metric(float((rev.ratio > 2).mean()), "Share of fields whose estimate at least doubled", SODIR, "derived"),
    }


def metrics(d):
    return {**scale_metrics(d), **log_metrics(d), **spread_metrics(d), **chain_metrics(d), **depth_volume_metrics(d)}
