// Exceedance curve of the simulated recoverable volume, with P90, P50 and P10 marked (oilfield convention).
import { token, onSchemeChange } from "../runtime/js/subscout.js";

export default function exceed(el, datasets, opts = {}) {
  const V = datasets.volumes.map((r) => ({ p: +r.exceedance_pct, v: +r.recoverable_mn_sm3 }));
  const svg = d3.select(el).selectAll("svg").data([0]).join("svg").attr("role", "img").attr("aria-label", "Exceedance curve of simulated recoverable volume");
  let last = null;
  function draw(width, state = {}) {
    last = [width, state];
    const narrow = width < 600;
    const H = Math.round(Math.min(Math.max(width * 0.55, 240), window.innerHeight * (narrow ? 0.28 : 0.5)));
    const m = { l: 44, r: 16, t: 22, b: 34 };
    const boe = opts.units && opts.units() === "boe";
    const f = boe ? 6.29 : 1, unit = boe ? "Mn boe" : "Mn Sm³";
    svg.attr("viewBox", `0 0 ${width} ${H}`).attr("width", width).attr("height", H).selectAll("*").remove();
    const x = d3.scaleLinear().domain([0, d3.max(V, (d) => d.v) * f]).range([m.l, width - m.r]);
    const y = d3.scaleLinear().domain([0, 100]).range([H - m.b, m.t]);
    const muted = token("text-muted") || "#888", ink = token("text") || "currentColor";
    svg.append("g").attr("transform", `translate(${m.l},0)`).call(d3.axisLeft(y).ticks(5).tickSize(-(width - m.l - m.r)).tickFormat((d) => `${d}%`))
      .call((g) => g.select(".domain").remove()).call((g) => g.selectAll("line").attr("stroke", token("data-context")).attr("opacity", 0.3)).call((g) => g.selectAll("text").attr("fill", muted).attr("font-size", 10));
    svg.append("g").attr("transform", `translate(0,${H - m.b})`).call(d3.axisBottom(x).ticks(6).tickSize(3))
      .call((g) => g.select(".domain").attr("stroke", muted)).call((g) => g.selectAll("text").attr("fill", muted).attr("font-size", 10));
    svg.append("text").attr("x", (m.l + width - m.r) / 2).attr("y", H - 2).attr("text-anchor", "middle").attr("font-size", 10.5).attr("fill", muted).text(`recoverable oil, ${unit} (simulated)`);
    svg.append("text").attr("x", m.l + 6).attr("y", m.t + 2).attr("font-size", 10).attr("fill", muted).text("chance of at least this much");
    svg.append("path").attr("d", d3.line().x((d) => x(d.v * f)).y((d) => y(d.p))(V)).attr("fill", "none").attr("stroke", token("data-story-1")).attr("stroke-width", 2.2);
    [90, 50, 10].forEach((p, i) => {
      const d = V.find((r) => r.p === p);
      if (!d) return;
      svg.append("line").attr("x1", m.l).attr("x2", x(d.v * f)).attr("y1", y(p)).attr("y2", y(p)).attr("stroke", token("data-highlight")).attr("stroke-dasharray", "3 3");
      svg.append("line").attr("x1", x(d.v * f)).attr("x2", x(d.v * f)).attr("y1", y(p)).attr("y2", H - m.b).attr("stroke", token("data-highlight")).attr("stroke-dasharray", "3 3");
      svg.append("circle").attr("cx", x(d.v * f)).attr("cy", y(p)).attr("r", 4).attr("fill", token("data-highlight"));
      svg.append("text").attr("x", x(d.v * f) + 6).attr("y", y(p) - 6).attr("font-size", 11).attr("font-weight", i === 1 ? 600 : 400).attr("fill", ink)
        .text(`P${p}${p === 90 ? " (low)" : p === 10 ? " (high)" : ""}: ${(d.v * f).toFixed(0)} ${unit}`);
    });
  }
  onSchemeChange(() => last && draw(...last));
  return { draw, repaint: () => last && draw(...last) };
}
