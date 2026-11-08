"""Metrics and derived datasets for Pinpoints and Echoes.

Inputs are the small extracts written by scripts/make_extracts.py. Every number in the prose
comes from here, with its method, source and confidence.
"""

import math

import pandas as pd

from subscout import metric

SRC_SODIR = "sodir"
SRC_VOLVE = "volve"


def _g(d, key):
    g = d["geometry"].set_index("key").value
    return float(g[key])


def datasets(d):
    c = d["chain"]
    v = c[c.axis == "vertical"].copy()
    v["cum_typical"] = (v.typical**2).cumsum() ** 0.5  # independent errors add in quadrature
    v["cum_worst"] = (v.worst**2).cumsum() ** 0.5
    return {"stack": v.reset_index(drop=True)}


def metrics(d):
    n = _g(d, "n_wellbores")
    area = _g(d, "hull_area_km2")
    hole_m = _g(d, "reservoir_hole_mm") / 1000
    nn_m = _g(d, "nn_median_km") * 1000
    cross_km2 = n * math.pi * (hole_m / 2) ** 2 / 1e6
    c = d["chain"].set_index("link")
    s = d["stack"]
    row = lambda k: c[c.index.str.startswith(k)].iloc[0]
    return {
        "n_wellbores": metric(
            int(n),
            "Petroleum wellbores (development and exploration, sidetracks included) with a "
            "wellhead position in the Norwegian North Sea",
            SRC_SODIR,
            "observed",
        ),
        "area_km2": metric(
            area,
            "Convex hull of those wellhead positions, km²; the area they span, not the sea",
            SRC_SODIR,
            "derived",
            "km²",
        ),
        "hole_cm": metric(
            hole_m * 100,
            "Median open-hole diameter of Volve runs reaching 3,000 m MD or deeper, cm",
            SRC_VOLVE,
            "derived",
            "cm",
        ),
        "one_in": metric(
            area / cross_km2,
            "Area spanned divided by the summed cross-sections of the wellbores at that diameter: "
            "the share of the area that was ever a hole is one in this many",
            SRC_SODIR,
            "derived",
        ),
        "nn_km": metric(
            nn_m / 1000,
            "Median distance from an exploration well to the nearest other exploration site "
            "(wellhead positions, 100 m cells), km",
            SRC_SODIR,
            "derived",
            "km",
        ),
        "nn_p10": metric(_g(d, "nn_p10_km"), "10th percentile of the same distance, km", SRC_SODIR, "derived", "km"),
        "nn_p90": metric(_g(d, "nn_p90_km"), "90th percentile of the same distance, km", SRC_SODIR, "derived", "km"),
        "spacing_ratio": metric(
            nn_m / hole_m,
            "Median distance to the nearest exploration site divided by the hole diameter",
            SRC_SODIR,
            "derived",
        ),
        "coin_m": metric(
            nn_m / hole_m * 0.01,
            "If the wellbore were a 1 cm coin, the median distance to the nearest exploration site, m",
            SRC_SODIR,
            "derived",
            "m",
        ),
        "coin_span_km": metric(
            math.sqrt(area) * 1000 / hole_m * 0.01 / 1000,
            "If the wellbore were a 1 cm coin, the side of a square of the area spanned, km",
            SRC_SODIR,
            "derived",
            "km",
        ),
        "pos_h": metric(
            float(row("Well position").typical),
            "Median horizontal position uncertainty at the end of 26 Volve surveys, m; the export does not state "
            "the unit or the confidence level (square root of covariance taken as sigma in feet)",
            SRC_VOLVE,
            "observed",
            "m",
        ),
        "pos_h_max": metric(float(row("Well position").worst), "Largest of those 26, m", SRC_VOLVE, "observed", "m"),
        "stack_typical": metric(
            float(s.cum_typical.iloc[-1]),
            "Typical vertical errors combined in quadrature, m (independence assumed)",
            SRC_VOLVE,
            "interpreted",
            "m",
        ),
        "stack_worst": metric(
            float(s.cum_worst.iloc[-1]),
            "Largest vertical errors on file combined in quadrature, m (independence assumed; the depth "
            "reference is a systematic offset, so this is a bound, not a forecast)",
            SRC_VOLVE,
            "interpreted",
            "m",
        ),
        "n_links": metric(int(len(s)), "Vertical links in the chain of errors", SRC_VOLVE, "derived"),
    }
