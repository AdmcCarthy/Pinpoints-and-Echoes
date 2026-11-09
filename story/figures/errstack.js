// A chain of vertical errors at the target, one row per link, then the combined spread.
// Solid bar: typical value. Lighter extension: largest value on file. state: { upto } reveals links.
import { token, onSchemeChange } from "../runtime/js/subscout.js";

export default function errstack(el, datasets) {
  const rows = datasets.stack.map((r) => ({ ...r, typical: +r.typical, worst: +r.worst, cum_typical: +r.cum_typical, cum_worst: +r.cum_worst }));
  const last_ = rows[rows.length - 1];
  const all = [...rows, { link: "Combined at the target", typical: last_.cum_typical, worst: last_.cum_worst, total: true }];
  const svg = d3.select(el).selectAll("svg").data([0]).join("svg").attr("role", "img")
    .attr("aria-label", "Bar chart of vertical errors by link, with their combined spread");
  let last = null;
  const fmt = (v) => (v < 10 ? v.toFixed(1) : Math.round(v).toString());

  function draw(width, state = {}) {
    last = [width, state];
    const upto = state.upto ?? all.length;
    const narrow = width < 520;
    const m = { l: narrow ? 8 : 190, r: 52, t: 8, b: 30 };
    const rowH = narrow ? 40 : 36, H = m.t + m.b + all.length * rowH;
    svg.attr("viewBox", `0 0 ${width} ${H}`).attr("width", width).attr("height", H);
    const x = d3.scaleLinear().domain([0, d3.max(all, (r) => r.worst) * 1.05]).range([m.l, width - m.r]);
    svg.selectAll("*").remove();
    const ay = H - m.b;
    svg.append("g").attr("transform", `translate(0,${ay})`).call(d3.axisBottom(x).ticks(5).tickSize(4).tickFormat((d) => `${d} m`))
      .call((g) => g.select(".domain").attr("stroke", token("text-muted") || "#888"))
      .call((g) => g.selectAll("text").attr("fill", token("text-muted") || "#888").attr("font-size", 11));
    all.forEach((r, i) => {
      const shown = r.total ? upto >= all.length : i < upto;
      const y = m.t + i * rowH, colour = r.total ? token("data-highlight") : token("data-story-1") || token("data-context");
      const g = svg.append("g").attr("opacity", shown ? 1 : 0.1);
      g.append("text").attr("x", narrow ? m.l : m.l - 8).attr("y", narrow ? y + 11 : y + rowH / 2 + 4).attr("text-anchor", narrow ? "start" : "end")
        .attr("font-size", 12).attr("font-weight", r.total ? 600 : 400).attr("fill", token("text") || "currentColor").text(r.link);
      const by = narrow ? y + 18 : y + rowH / 2 - 8, bh = 16;
      g.append("rect").attr("x", x(0)).attr("y", by).attr("height", bh).attr("width", Math.max(1, x(r.worst) - x(0))).attr("fill", colour).attr("opacity", 0.3);
      g.append("rect").attr("x", x(0)).attr("y", by).attr("height", bh).attr("width", Math.max(1.5, x(r.typical) - x(0))).attr("fill", colour);
      g.append("text").attr("x", x(r.worst) + 6).attr("y", by + 12).attr("font-size", 11).attr("fill", token("text") || "currentColor")
        .text(`${fmt(r.typical)} | ${fmt(r.worst)} m`);
    });
  }
  onSchemeChange(() => last && draw(...last));
  return { draw, repaint: () => last && draw(...last) };
}
