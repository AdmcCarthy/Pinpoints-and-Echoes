// Wellbores at true scale on a map of the area they span, and the same wells enlarged.
// state: { mag } where mag is the enlargement of each wellbore (1 = true size).
// Wellhead positions only; the dots are enlarged by exactly the stated factor.
import { token, onSchemeChange } from "../runtime/js/subscout.js";

export default function scale(el, datasets, opts = {}) {
  const wells = datasets.wells;
  const geo = Object.fromEntries(datasets.geometry.map((r) => [r.key, +r.value]));
  const holeM = geo.reservoir_hole_mm / 1000;
  const lat0 = d3.mean(wells, (w) => +w.lat);
  const kx = Math.cos((lat0 * Math.PI) / 180);
  const pts = wells.map((w) => [+w.lon * kx, +w.lat]);
  const hull = d3.polygonHull(pts);
  const [x0, x1] = d3.extent(pts, (p) => p[0]);
  const [y0, y1] = d3.extent(pts, (p) => p[1]);
  const kmPerUnit = 111.195; // km per degree of latitude
  const canvas = d3.select(el).selectAll("canvas").data([0]).join("canvas").node();
  const note = d3.select(el).selectAll("div.ss-scale-note").data([0]).join("div").attr("class", "ss-scale-note")
    .style("font-size", "var(--ss-text-sm, 0.8rem)").style("color", "var(--ss-text-muted, inherit)").style("margin-top", "0.4rem");
  let last = null;

  function draw(width, state = {}) {
    last = [width, state];
    const mag = state.mag ?? 1;
    const aspect = (y1 - y0) / (x1 - x0);
    const H = Math.round(Math.min(width * aspect, Math.max(180, window.innerHeight * (width < 600 ? 0.26 : 0.58))));
    const dpr = window.devicePixelRatio || 1;
    canvas.width = width * dpr; canvas.height = H * dpr;
    canvas.style.width = `${width}px`; canvas.style.height = `${H}px`;
    const g = canvas.getContext("2d");
    g.setTransform(dpr, 0, 0, dpr, 0, 0);
    const pad = 6, s = Math.min((width - 2 * pad) / (x1 - x0), (H - 2 * pad) / (y1 - y0));
    const X = (p) => pad + (p[0] - x0) * s, Y = (p) => H - pad - (p[1] - y0) * s;
    const mPerPx = (kmPerUnit * 1000) / s;
    const diamPx = (holeM * mag) / mPerPx;
    g.clearRect(0, 0, width, H);
    g.beginPath();
    hull.forEach((p, i) => (i ? g.lineTo(X(p), Y(p)) : g.moveTo(X(p), Y(p))));
    g.closePath();
    g.strokeStyle = token("data-context"); g.lineWidth = 1; g.setLineDash([4, 4]); g.stroke(); g.setLineDash([]);
    if (diamPx >= 0.35) {
      g.fillStyle = token("data-highlight");
      g.globalAlpha = 0.8;
      for (const p of pts) { g.beginPath(); g.arc(X(p), Y(p), Math.max(diamPx / 2, 0.5), 0, 6.2832); g.fill(); }
      g.globalAlpha = 1;
    }
    const km = (x1 - x0) * kmPerUnit;
    note.text(
      mag === 1
        ? `${wells.length.toLocaleString("en-GB")} wellbores drawn at true size: each dot would be one ${Number((1 / diamPx).toPrecision(2)).toLocaleString("en-GB")}th of a pixel wide. The area shown is about ${Math.round(km).toLocaleString("en-GB")} km across.`
        : `Each wellbore enlarged ${Math.round(mag).toLocaleString("en-GB")} times, to ${diamPx.toFixed(1)} px. Wellhead positions only.`
    );
  }
  onSchemeChange(() => last && draw(...last));
  return { draw, repaint: () => last && draw(...last) };
}
