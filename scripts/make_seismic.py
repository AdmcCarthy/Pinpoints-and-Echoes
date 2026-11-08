"""Seismic extracts for the echo and tie beats: one inline of the Volve ST10010 full stack (time) through a
well, the single trace at the well, and the dominant frequency around the reservoir.

Needs segyio and numpy only (the seismic_lib interpreter has both):

    ..\\seismic_lib\\.venv\\Scripts\\python.exe -I scripts\\make_seismic.py ^
        --segy "C:\\appl\\Volve\\Seismic\\ST10010ZC11_PZ_PSDM_KIRCH_FULL_T.MIG_FIN.POST_STACK.3D.JS-017536.segy" ^
        --x 436123.2 --y 6479126.0 --well "15/9-F-11 T2"

Domain: two-way time in ms (the file name says _T, the text header says PSDM in time). Samples are relative
amplitude; polarity is not stated in the headers and is reported as unknown. Coordinates are ED50 / UTM 31N
(text header), the same system as the horizon files and the well picks used to place the well.
Writes story/data/section.json (amplitudes as int8 on a stated scale, every second crossline) and
story/data/trace.csv (the trace at the well, full sample rate). The SEG-Y itself is never copied.
"""

import argparse
import json
from pathlib import Path

import numpy as np
import segyio

T0, T1 = 1800.0, 3300.0  # ms window kept
KEEP_EVERY = 2  # crosslines kept in the section
SPEC_WIN = (2300.0, 3100.0)  # ms, window for the dominant frequency around the reservoir


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--segy", required=True)
    ap.add_argument("--x", type=float, required=True)
    ap.add_argument("--y", type=float, required=True)
    ap.add_argument("--well", required=True)
    ap.add_argument("--out", type=Path, default=Path(__file__).resolve().parents[1] / "story" / "data")
    a = ap.parse_args()

    with segyio.open(a.segy, ignore_geometry=True) as f:
        il = np.asarray(f.attributes(segyio.TraceField.INLINE_3D)[:])
        xl = np.asarray(f.attributes(segyio.TraceField.CROSSLINE_3D)[:])
        sc = np.asarray(f.attributes(segyio.TraceField.SourceGroupScalar)[:]).astype(float)
        k = np.where(sc < 0, -1.0 / sc, np.where(sc > 0, sc, 1.0))
        x = np.asarray(f.attributes(segyio.TraceField.CDP_X)[:]) * k
        y = np.asarray(f.attributes(segyio.TraceField.CDP_Y)[:]) * k
        t = np.asarray(f.samples, dtype=float)
        i_well = int(np.argmin((x - a.x) ** 2 + (y - a.y) ** 2))
        d_well = float(np.hypot(x[i_well] - a.x, y[i_well] - a.y))
        line = int(il[i_well])
        sel = np.where(il == line)[0]
        sel = sel[np.argsort(xl[sel])]
        w = (t >= T0) & (t <= T1)
        data = np.stack([f.trace[int(i)][w] for i in sel])  # (ntraces, nsamples)
        trace_well = f.trace[i_well]
        text = f.text[0].decode("ascii", "replace") if hasattr(f.text[0], "decode") else str(f.text[0])

    tw = t[w]
    dt = float(t[1] - t[0])
    xs, ys = x[sel], y[sel]
    dist = np.concatenate([[0.0], np.cumsum(np.hypot(np.diff(xs), np.diff(ys)))])
    j_well = int(np.where(sel == i_well)[0][0])

    # dominant frequency: mean amplitude spectrum of the 41 traces about the well, reservoir window
    s0, s1 = np.searchsorted(t, SPEC_WIN[0]), np.searchsorted(t, SPEC_WIN[1])
    block = data[max(0, j_well - 20) : j_well + 21, s0 - np.searchsorted(t, T0) : s1 - np.searchsorted(t, T0)]
    block = block * np.hanning(block.shape[1])
    spec = np.abs(np.fft.rfft(block, axis=1)).mean(axis=0)
    freqs = np.fft.rfftfreq(block.shape[1], d=dt / 1000.0)
    f_dom = float(freqs[np.argmax(spec[1:]) + 1])
    # centroid as a second estimate
    f_cen = float((freqs * spec).sum() / spec.sum())

    kept = data[::KEEP_EVERY]
    scale = float(np.percentile(np.abs(kept), 99.5))
    amp = np.clip(np.round(kept / scale * 127), -127, 127).astype(np.int8)
    out = {
        "well": a.well,
        "inline": line,
        "domain": "two-way time, ms (PSDM stack in time)",
        "polarity": "not stated in the headers; unknown",
        "quantity": "relative amplitude, int8 on the scale below",
        "scale_abs": scale,
        "t0_ms": float(tw[0]),
        "dt_ms": dt,
        "n_samples": int(amp.shape[1]),
        "crosslines": [int(v) for v in xl[sel][::KEEP_EVERY]],
        "dist_m": [round(float(v), 1) for v in dist[::KEEP_EVERY]],
        "well_dist_m": round(float(dist[j_well]), 1),
        "well_trace_offset_m": round(d_well, 1),
        "dominant_hz": round(f_dom, 1),
        "centroid_hz": round(f_cen, 1),
        "spectrum_window_ms": list(SPEC_WIN),
        "crs": "ED50 / UTM 31N (text header)",
        "amp": amp.tolist(),
        "source": "Volve data village, ST10010ZC11 PZ PSDM Kirchhoff full stack, time, 2011 processing (WesternGeco for Statoil)",
    }
    a.out.mkdir(parents=True, exist_ok=True)
    (a.out / "section.json").write_text(json.dumps(out, separators=(",", ":")))
    with open(a.out / "trace.csv", "w") as fh:
        fh.write("t_ms,amp\n")
        for ti, ai in zip(t, trace_well):
            if T0 - 400 <= ti <= T1 + 200:
                fh.write(f"{ti:.0f},{ai / scale:.4f}\n")
    print(f"inline {line}, {len(sel)} traces, well at trace {j_well} ({d_well:.1f} m from the pick), "
          f"dominant {f_dom:.1f} Hz, centroid {f_cen:.1f} Hz, kept {amp.shape}")
    print(text[:400])


if __name__ == "__main__":
    main()
