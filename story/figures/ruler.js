// A logarithmic ruler from a centimetre to a thousand kilometres, with the wellbore, the
// distance to the next well and the span of the area marked. state: { coin } rescales every
// length so that the wellbore is a 1 cm coin.
import { token, onSchemeChange } from "../runtime/js/subscout.js";

const fmtLen = (m) =>
  m < 0.1 ? `${+(m * 100).toPrecision(2)} cm` : m < 1 ? `${+(m * 100).toPrecision(2)} cm`
    : m < 1000 ? `${+m.toPrecision(3)} m` : `${(+(m / 1000).toPrecision(3)).toLocaleString("en-GB")} km`;

export default function ruler(el, datasets) {
  const geo = Object.fromEntries(datasets.geometry.map((r) => [r.key, +r.value]));
  const hole = geo.reservoir_hole_mm / 1000;
  const marks = [
    { id: "hole", row: 0, label: "wellbore", m: hole, strong: true },
    { id: "p10", row: 1, label: "nearest well, close case", m: geo.nn_p10_km * 1000 },
    { id: "med", row: 2, label: "nearest well, typical", m: geo.nn_median_km * 1000, strong: true },
    { id: "p90", row: 3, label: "nearest well, far case", m: geo.nn_p90_km * 1000 },
    { id: "span", row: 0, label: "width of an equal-area square", m: Math.sqrt(geo.hull_area_km2) * 1000, strong: true },
  ];
  const svg = d3.select(el).selectAll("svg").data([0]).join("svg").attr("role", "img")
    .attr("aria-label", "Logarithmic length ruler from the wellbore diameter to the area the wells span");
  let last = null;

  function draw(width, state = {}) {
    last = [width, state];
    const f = state.coin ? 0.01 / hole : 1; // display length = real length * f
    const H = 236;
    const m = { l: 12, r: 12, t: 20, b: 34 };
    svg.attr("viewBox", `0 0 ${width} ${H}`).attr("width", width).attr("height", H);
    const lo = Math.log10(hole * 0.5), hi = Math.log10(Math.sqrt(geo.hull_area_km2) * 1000 * 2);
    const x = d3.scaleLinear().domain([lo, hi]).range([m.l, width - m.r]);
    const ay = H - m.b;
    // ticks at round display lengths
    const ticks = d3.range(-2, 7).map((k) => 10 ** k).filter((d) => Math.log10(d / f) >= lo && Math.log10(d / f) <= hi);
    svg.selectAll("*").remove();
    svg.append("line").attr("x1", m.l).attr("x2", width - m.r).attr("y1", ay).attr("y2", ay).attr("stroke", token("text-muted") || "#888");
    for (const t of ticks) {
      const px = x(Math.log10(t / f));
      svg.append("line").attr("x1", px).attr("x2", px).attr("y1", ay).attr("y2", ay + 5).attr("stroke", token("text-muted") || "#888");
      svg.append("text").attr("x", px).attr("y", ay + 19).attr("text-anchor", "middle").attr("font-size", 11).attr("fill", token("text-muted") || "#888").text(fmtLen(t));
    }
    // marks, staggered so labels do not collide
    marks.forEach((k, i) => {
      const px = x(Math.log10(k.m));
      const top = m.t + k.row * 30;
      svg.append("line").attr("x1", px).attr("x2", px).attr("y1", top + 12).attr("y2", ay)
        .attr("stroke", k.strong ? token("data-highlight") : token("data-context")).attr("stroke-width", k.strong ? 2 : 1.25);
      svg.append("circle").attr("cx", px).attr("cy", ay).attr("r", k.strong ? 4.5 : 3).attr("fill", k.strong ? token("data-highlight") : token("data-context"));
      const anchor = px > width - 120 ? "end" : px < 120 ? "start" : "middle";
      svg.append("text").attr("x", px).attr("y", top).attr("text-anchor", anchor).attr("font-size", 12).attr("font-weight", k.strong ? 600 : 400)
        .attr("fill", token("text") || "currentColor").text(`${k.label}: ${fmtLen(k.m * f)}`);
    });
    svg.append("text").attr("x", m.l).attr("y", H - 2).attr("text-anchor", "start").attr("font-size", 11).attr("fill", token("text-muted") || "#888")
      .text(state.coin ? "scaled so the wellbore is a 1 cm coin" : "true lengths, logarithmic scale");
  }
  onSchemeChange(() => last && draw(...last));
  return { draw, repaint: () => last && draw(...last) };
}
