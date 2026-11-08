// Two published versions of one horizon along a line between well picks, in two-way time.
// state: { stage } 1 = well picks only, 2 = + base survey, 3 = + reprocessed survey and the gap.
import { token, onSchemeChange } from "../runtime/js/subscout.js";

export default function transect(el, datasets) {
  const T = datasets.transect.map((r) => ({ d: +r.dist_m, a: +r.twt_base_ms, b: +r.twt_reprocessed_ms }));
  const P = datasets.picks.map((r) => ({ d: +r.dist_m, t: +r.pick_twt_ms, well: r.well }));
  const svg = d3.select(el).selectAll("svg").data([0]).join("svg").attr("role", "img")
    .attr("aria-label", "Two-way time of one horizon along a line, two published versions and the well picks");
  let last = null;

  function draw(width, state = {}) {
    last = [width, state];
    const stage = state.stage ?? 3;
    const H = Math.round(Math.min(Math.max(width * 0.55, 220), window.innerHeight * (width < 600 ? 0.3 : 0.5)));
    const m = { l: 44, r: 12, t: 12, b: 30 };
    svg.attr("viewBox", `0 0 ${width} ${H}`).attr("width", width).attr("height", H).selectAll("*").remove();
    const all = [...T.flatMap((r) => [r.a, r.b]), ...P.map((p) => p.t)];
    const pad = 6, [lo, hi] = [d3.min(all) - pad, d3.max(all) + pad];
    const x = d3.scaleLinear().domain([0, d3.max(T, (r) => r.d)]).range([m.l, width - m.r]);
    const y = d3.scaleLinear().domain([lo, hi]).range([m.t, H - m.b]); // time increases downward
    const muted = token("text-muted") || "#888", ink = token("text") || "currentColor";
    svg.append("g").attr("transform", `translate(${m.l},0)`).call(d3.axisLeft(y).ticks(4).tickSize(-(width - m.l - m.r)).tickFormat((d) => `${d}`))
      .call((g) => g.select(".domain").remove()).call((g) => g.selectAll("line").attr("stroke", token("data-context")).attr("opacity", 0.35))
      .call((g) => g.selectAll("text").attr("fill", muted).attr("font-size", 11));
    svg.append("g").attr("transform", `translate(0,${H - m.b})`).call(d3.axisBottom(x).ticks(5).tickFormat((d) => `${d / 1000} km`))
      .call((g) => g.select(".domain").attr("stroke", muted)).call((g) => g.selectAll("text").attr("fill", muted).attr("font-size", 11));
    svg.append("text").attr("x", 4).attr("y", m.t + 8).attr("font-size", 11).attr("fill", muted).text("ms TWT");
    const c1 = token("data-story-1"), c2 = token("data-highlight");
    if (stage >= 3) {
      svg.append("path").attr("fill", c2).attr("opacity", 0.18).attr("d", d3.area().x((r) => x(r.d)).y0((r) => y(r.a)).y1((r) => y(r.b))(T));
    }
    const line = (k) => d3.line().x((r) => x(r.d)).y((r) => y(r[k]))(T);
    if (stage >= 2) svg.append("path").attr("d", line("a")).attr("fill", "none").attr("stroke", c1).attr("stroke-width", 2);
    if (stage >= 3) svg.append("path").attr("d", line("b")).attr("fill", "none").attr("stroke", c2).attr("stroke-width", 2);
    const w = T.reduce((p, r) => (Math.abs(r.a - r.b) > Math.abs(p.a - p.b) ? r : p));
    const aUp = w.a < w.b; // smaller time plots higher
    const lab = (txt, c, tv, up) => svg.append("text").attr("x", x(w.d)).attr("y", y(tv) + (up ? -8 : 17)).attr("text-anchor", w.d > T[T.length - 1].d * 0.8 ? "end" : "middle")
      .attr("font-size", 12).attr("font-weight", 600).attr("fill", c).text(txt);
    if (stage >= 2) lab("base survey", c1, w.a, aUp);
    if (stage >= 3) lab("reprocessed survey", c2, w.b, !aUp);
    svg.selectAll("circle.pick").data(P).join("circle").attr("class", "pick").attr("cx", (p) => x(p.d)).attr("cy", (p) => y(p.t)).attr("r", 4.5)
      .attr("fill", "none").attr("stroke", ink).attr("stroke-width", 1.75).append("title").text((p) => `${p.well}: ${p.t.toFixed(0)} ms`);
    svg.append("text").attr("x", width - m.r).attr("y", m.t + 8).attr("text-anchor", "end").attr("font-size", 11).attr("fill", muted).text("○ well picks within 150 m of the line");
  }
  onSchemeChange(() => last && draw(...last));
  return { draw, repaint: () => last && draw(...last) };
}
