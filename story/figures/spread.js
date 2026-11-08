// How far two published versions of a horizon disagree, by distance to the nearest well pick.
// Solid line: median absolute difference. Lighter line: 90th percentile. One entity, one colour.
import { token, onSchemeChange } from "../runtime/js/subscout.js";

export default function spread(el, datasets) {
  const R = datasets.spread.map((r) => ({ s: r.surface, band: r.band, med: +r.abs_median_ms, p90: +r.abs_p90_ms }));
  const bands = [...new Set(R.map((r) => r.band))];
  const surfaces = [...new Set(R.map((r) => r.s))];
  const svg = d3.select(el).selectAll("svg").data([0]).join("svg").attr("role", "img")
    .attr("aria-label", "Line chart of the disagreement between two versions of each horizon against distance to the nearest well pick");
  let last = null;

  function draw(width, state = {}) {
    last = [width, state];
    const focus = state.focus ?? null;
    const H = Math.round(Math.min(Math.max(width * 0.62, 240), window.innerHeight * (width < 600 ? 0.32 : 0.55)));
    const m = { l: 40, r: width < 520 ? 96 : 130, t: 14, b: 40 };
    svg.attr("viewBox", `0 0 ${width} ${H}`).attr("width", width).attr("height", H).selectAll("*").remove();
    const x = d3.scalePoint().domain(bands).range([m.l + 8, width - m.r]).padding(0.1);
    const y = d3.scaleLinear().domain([0, d3.max(R, (r) => r.p90) * 1.05]).range([H - m.b, m.t]);
    const muted = token("text-muted") || "#888";
    svg.append("g").attr("transform", `translate(${m.l},0)`).call(d3.axisLeft(y).ticks(4).tickSize(-(width - m.l - m.r)))
      .call((g) => g.select(".domain").remove()).call((g) => g.selectAll("line").attr("stroke", token("data-context")).attr("opacity", 0.35))
      .call((g) => g.selectAll("text").attr("fill", muted).attr("font-size", 11));
    svg.append("g").attr("transform", `translate(0,${H - m.b})`).call(d3.axisBottom(x).tickSize(3))
      .call((g) => g.select(".domain").attr("stroke", muted)).call((g) => g.selectAll("text").attr("fill", muted).attr("font-size", 10));
    svg.append("text").attr("x", 4).attr("y", m.t - 2).attr("font-size", 11).attr("fill", muted).text("ms TWT");
    svg.append("text").attr("x", (m.l + width - m.r) / 2).attr("y", H - 4).attr("text-anchor", "middle").attr("font-size", 11).attr("fill", muted).text("distance to the nearest well pick");
    const labels = [];
    surfaces.forEach((s, k) => {
      const rows = R.filter((r) => r.s === s);
      const colour = token(`data-cat-${k + 1}`);
      const on = !focus || focus === s;
      const g = svg.append("g").attr("opacity", on ? 1 : 0.18);
      const ln = (key) => d3.line().x((r) => x(r.band)).y((r) => y(r[key]))(rows);
      g.append("path").attr("d", ln("p90")).attr("fill", "none").attr("stroke", colour).attr("stroke-width", 1.5).attr("opacity", 0.4).attr("stroke-dasharray", "4 3");
      g.append("path").attr("d", ln("med")).attr("fill", "none").attr("stroke", colour).attr("stroke-width", 2.25);
      g.selectAll("circle").data(rows).join("circle").attr("cx", (r) => x(r.band)).attr("cy", (r) => y(r.med)).attr("r", 3.2).attr("fill", colour)
        .append("title").text((r) => `${s}, ${r.band}: median ${r.med.toFixed(1)} ms, 90th percentile ${r.p90.toFixed(1)} ms`);
      const e = rows[rows.length - 1];
      labels.push({ s, band: e.band, y: y(e.med) + 4, g });
    });
    labels.sort((p, q) => p.y - q.y);
    for (let i = 1; i < labels.length; i++) if (labels[i].y - labels[i - 1].y < 14) labels[i].y = labels[i - 1].y + 14;
    for (const l of labels) l.g.append("text").attr("x", x(l.band) + 8).attr("y", l.y).attr("font-size", 12).attr("font-weight", 600).attr("fill", token("text") || "currentColor").text(l.s);
  }
  onSchemeChange(() => last && draw(...last));
  return { draw, repaint: () => last && draw(...last) };
}
