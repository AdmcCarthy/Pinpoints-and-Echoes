// Closure area against depth for the Volve high on the Hugin top, with the published contact cases.
// Depth points down; area grows to the right. state: { cases } draws the P90/P50/P10 contacts.
import { token, onSchemeChange } from "../runtime/js/subscout.js";

export default function closure(el, datasets) {
  const C = datasets.closure.map((r) => ({ z: +r.depth_m, a: +r.area_km2 })).sort((p, q) => p.z - q.z);
  const K = datasets.contact.map((r) => ({ z: +r.depth_m, exc: +r.exceedance_pct, p: +r.probability_pct }));
  const svg = d3.select(el).selectAll("svg").data([0]).join("svg").attr("role", "img").attr("aria-label", "Closure area against depth with the published contact distribution");
  let last = null;
  function draw(width, state = {}) {
    last = [width, state];
    const narrow = width < 600;
    const H = Math.round(Math.min(Math.max(width * 0.65, 260), window.innerHeight * (narrow ? 0.28 : 0.58)));
    const m = { l: 48, r: narrow ? 12 : 24, t: 14, b: 32 };
    svg.attr("viewBox", `0 0 ${width} ${H}`).attr("width", width).attr("height", H).selectAll("*").remove();
    const zmax = Math.max(d3.max(C, (p) => p.z), state.cases ? 3270 : 0);
    const y = d3.scaleLinear().domain([C[0].z - 10, zmax + 10]).range([m.t, H - m.b]);
    const x = d3.scaleLinear().domain([0, d3.max(C, (p) => p.a) * 1.05]).range([m.l, width - m.r]);
    const muted = token("text-muted") || "#888", ink = token("text") || "currentColor";
    svg.append("g").attr("transform", `translate(${m.l},0)`).call(d3.axisLeft(y).ticks(6).tickSize(-(width - m.l - m.r)).tickFormat((d) => `${d}`))
      .call((g) => g.select(".domain").remove()).call((g) => g.selectAll("line").attr("stroke", token("data-context")).attr("opacity", 0.3)).call((g) => g.selectAll("text").attr("fill", muted).attr("font-size", 10));
    svg.append("g").attr("transform", `translate(0,${H - m.b})`).call(d3.axisBottom(x).ticks(5).tickSize(3).tickFormat((d) => `${d}`))
      .call((g) => g.select(".domain").attr("stroke", muted)).call((g) => g.selectAll("text").attr("fill", muted).attr("font-size", 10));
    svg.append("text").attr("x", 2).attr("y", 10).attr("font-size", 10).attr("fill", muted).text("m below MSL");
    svg.append("text").attr("x", (m.l + width - m.r) / 2).attr("y", H - 2).attr("text-anchor", "middle").attr("font-size", 10.5).attr("fill", muted).text("area inside the closing contour, km²");
    const area = d3.area().x0(m.l).x1((p) => x(p.a)).y((p) => y(p.z)).curve(d3.curveStepAfter);
    svg.append("path").attr("d", area(C)).attr("fill", token("data-story-1")).attr("opacity", 0.18);
    svg.append("path").attr("d", d3.line().x((p) => x(p.a)).y((p) => y(p.z)).curve(d3.curveStepAfter)(C)).attr("fill", "none").attr("stroke", token("data-story-1")).attr("stroke-width", 2);
    const zEnd = C[C.length - 1].z;
    svg.append("text").attr("x", x(C[C.length - 1].a) - 4).attr("y", y(zEnd) + 14).attr("text-anchor", "end").attr("font-size", 10).attr("fill", muted).text("surface not mapped deeper");
    if (state.cases) {
      const cases = [{ name: "P90 (low)", z: 3105 }, { name: "P50", z: 3135 }, { name: "P10 (high)", z: 3260 }];
      cases.forEach((c, i) => {
        const inMap = c.z <= zEnd;
        const a = inMap ? C.filter((p) => p.z <= c.z).slice(-1)[0]?.a : null;
        svg.append("line").attr("x1", m.l).attr("x2", width - m.r).attr("y1", y(c.z)).attr("y2", y(c.z)).attr("stroke", token("data-highlight")).attr("stroke-width", i === 1 ? 2 : 1.2).attr("stroke-dasharray", i === 1 ? null : "4 3");
        svg.append("text").attr("x", width - m.r - 4).attr("y", y(c.z) - 4).attr("text-anchor", "end").attr("font-size", 11).attr("font-weight", i === 1 ? 600 : 400).attr("fill", token("data-highlight"))
          .text(`contact ${c.name}: ${c.z} m${a != null ? `, ${a.toFixed(1)} km²` : ", beyond the mapped surface"}`);
        if (a != null) svg.append("circle").attr("cx", x(a)).attr("cy", y(c.z)).attr("r", 4).attr("fill", token("data-highlight"));
      });
    }
  }
  onSchemeChange(() => last && draw(...last));
  return { draw, repaint: () => last && draw(...last) };
}
