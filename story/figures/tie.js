// The well tie: the synthetic seismogram made from the log beside the real trace at the well, in time.
// state: { shifted } shows the synthetic after the single bulk shift reported in the ledger.
import { token, onSchemeChange } from "../runtime/js/subscout.js";

export default function tie(el, datasets) {
  const T = datasets.tie.map((r) => ({ t: +r.t_ms, real: +r.real, syn: +r.synthetic, shf: +r.synthetic_shifted }));
  const svg = d3.select(el).selectAll("svg").data([0]).join("svg").attr("role", "img").attr("aria-label", "Synthetic seismogram from the log beside the real trace at the well");
  let last = null;
  function wiggle(g, x0, pts, key, colour, y, scale, fillPos) {
    const line = d3.line().x((p) => x0 + p[key] * scale).y((p) => y(p.t)).curve(d3.curveMonotoneY);
    if (fillPos) {
      const area = d3.area().x0(x0).x1((p) => x0 + Math.max(0, p[key]) * scale).y((p) => y(p.t)).curve(d3.curveMonotoneY);
      g.append("path").attr("d", area(pts)).attr("fill", colour).attr("opacity", 0.45);
    }
    g.append("path").attr("d", line(pts)).attr("fill", "none").attr("stroke", colour).attr("stroke-width", 1.2);
  }
  function draw(width, state = {}) {
    last = [width, state];
    const narrow = width < 600;
    const H = Math.round(Math.min(Math.max(width * 0.75, 320), window.innerHeight * (narrow ? 0.28 : 0.62)));
    const m = { l: 44, r: 8, t: 26, b: 8 };
    const tdom = [2300, 3100];
    const y = d3.scaleLinear().domain(tdom).range([m.t, H - m.b]);
    svg.attr("viewBox", `0 0 ${width} ${H}`).attr("width", width).attr("height", H).selectAll("*").remove();
    const muted = token("text-muted") || "#888", ink = token("text") || "currentColor";
    svg.append("g").attr("transform", `translate(${m.l},0)`).call(d3.axisLeft(y).ticks(8).tickSize(-(width - m.l - m.r)).tickFormat((d) => `${d}`))
      .call((g) => g.select(".domain").remove()).call((g) => g.selectAll("line").attr("stroke", token("data-context")).attr("opacity", 0.3)).call((g) => g.selectAll("text").attr("fill", muted).attr("font-size", 10));
    svg.append("text").attr("x", 2).attr("y", 10).attr("font-size", 10).attr("fill", muted).text("ms TWT");
    const pts = T.filter((p) => p.t >= tdom[0] && p.t <= tdom[1]);
    const amax = d3.max(pts, (p) => Math.max(Math.abs(p.real), Math.abs(p.syn))) || 1;
    const lanes = [
      { key: state.shifted ? "shf" : "syn", label: state.shifted ? "synthetic from the log, shifted" : "synthetic from the log", colour: token("data-story-1") },
      { key: "real", label: "real trace at the well", colour: token("data-highlight") },
    ];
    const laneW = (width - m.l - m.r) / lanes.length;
    lanes.forEach((L, i) => {
      const x0 = m.l + laneW * (i + 0.5);
      const scale = (laneW * 0.42) / amax;
      svg.append("line").attr("x1", x0).attr("x2", x0).attr("y1", m.t).attr("y2", H - m.b).attr("stroke", token("data-context")).attr("opacity", 0.6);
      wiggle(svg, x0, pts, L.key, L.colour, y, scale, true);
      svg.append("text").attr("x", x0).attr("y", m.t - 10).attr("text-anchor", "middle").attr("font-size", 11).attr("font-weight", 600).attr("fill", ink).text(L.label);
    });
  }
  onSchemeChange(() => last && draw(...last));
  return { draw, repaint: () => last && draw(...last) };
}
