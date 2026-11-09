// Time against depth from every Volve check-shot table. One time, several depths: the fan.
// state: { at } the two-way time at which the depths are read off (ms); { zoom } narrows to it.
import { token, onSchemeChange } from "../runtime/js/subscout.js";

export default function fan(el, datasets) {
  const R = datasets.timedepth.map((r) => ({ table: r.table, t: +r.twt_ms, z: +r.tvdss_m }));
  const byT = d3.group(R, (r) => r.table);
  const svg = d3.select(el).selectAll("svg").data([0]).join("svg").attr("role", "img").attr("aria-label", "Two-way time against depth for every Volve check-shot table");
  let last = null;
  function draw(width, state = {}) {
    last = [width, state];
    const at = state.at ?? 2650;
    const narrow = width < 600;
    const H = Math.round(Math.min(Math.max(width * (narrow ? 0.6 : 0.7), narrow ? 200 : 280), window.innerHeight * (narrow ? 0.28 : 0.6)));
    const m = { l: 48, r: narrow ? 10 : 170, t: 14, b: 30 };
    svg.attr("viewBox", `0 0 ${width} ${H}`).attr("width", width).attr("height", H).selectAll("*").remove();
    const tdom = state.zoom ? [at - 150, at + 150] : [0, d3.max(R, (r) => r.t)];
    const rows = R.filter((r) => r.t >= tdom[0] && r.t <= tdom[1]);
    const zdom = state.zoom ? d3.extent(rows, (r) => r.z) : [0, d3.max(R, (r) => r.z)];
    const x = d3.scaleLinear().domain(tdom).range([m.l, width - m.r]);
    const y = d3.scaleLinear().domain(zdom).range([m.t, H - m.b]);
    const muted = token("text-muted") || "#888", ink = token("text") || "currentColor";
    svg.append("g").attr("transform", `translate(${m.l},0)`).call(d3.axisLeft(y).ticks(6).tickSize(-(width - m.l - m.r)).tickFormat((d) => `${d}`))
      .call((g) => g.select(".domain").remove()).call((g) => g.selectAll("line").attr("stroke", token("data-context")).attr("opacity", 0.3)).call((g) => g.selectAll("text").attr("fill", muted).attr("font-size", 10));
    svg.append("g").attr("transform", `translate(0,${H - m.b})`).call(d3.axisBottom(x).ticks(5).tickSize(3).tickFormat((d) => `${d}`))
      .call((g) => g.select(".domain").attr("stroke", muted)).call((g) => g.selectAll("text").attr("fill", muted).attr("font-size", 10));
    svg.append("text").attr("x", 2).attr("y", 10).attr("font-size", 10).attr("fill", muted).text("m below MSL");
    svg.append("text").attr("x", (m.l + width - m.r) / 2).attr("y", H - 2).attr("text-anchor", "middle").attr("font-size", 10.5).attr("fill", muted).text("two-way time, ms");
    const colours = [token("data-cat-1"), token("data-cat-2"), token("data-cat-3"), token("data-cat-4"), token("data-cat-5"), token("data-story-2")];
    const labels = [];
    let k = 0;
    for (const [name, pts] of byT) {
      const c = colours[k++ % colours.length];
      const p = pts.filter((r) => r.t >= tdom[0] && r.t <= tdom[1]).sort((a, b) => a.t - b.t);
      svg.append("path").attr("d", d3.line().x((r) => x(r.t)).y((r) => y(r.z))(p)).attr("fill", "none").attr("stroke", c).attr("stroke-width", 1.6);
      const hit = pts.find((r) => r.t === at);
      if (hit) labels.push({ name, c, z: hit.z });
    }
    // the fan at one time
    svg.append("line").attr("x1", x(at)).attr("x2", x(at)).attr("y1", m.t).attr("y2", H - m.b).attr("stroke", ink).attr("opacity", 0.5).attr("stroke-dasharray", "3 3");
    const zs = labels.map((l) => l.z);
    if (zs.length) {
      const z0 = d3.min(zs), z1 = d3.max(zs);
      svg.append("rect").attr("x", x(at) - 5).attr("width", 10).attr("y", y(z0)).attr("height", Math.max(2, y(z1) - y(z0))).attr("fill", token("data-highlight")).attr("opacity", 0.35);
      labels.forEach((l) => svg.append("circle").attr("cx", x(at)).attr("cy", y(l.z)).attr("r", 3.5).attr("fill", l.c));
      const left = x(at) > (m.l + width - m.r) * 0.6;
      svg.append("text").attr("x", x(at) + (left ? -10 : 10)).attr("y", y((z0 + z1) / 2) + 4).attr("text-anchor", left ? "end" : "start").attr("font-size", 11).attr("font-weight", 600).attr("fill", ink)
        .text(`${Math.round(z1 - z0)} m of depth for one time`);
      if (!narrow) {
        labels.sort((a, b) => a.z - b.z);
        for (let i = 1; i < labels.length; i++) if (y(labels[i].z) - y(labels[i - 1].z) < 13) labels[i].z = y.invert(y(labels[i - 1].z) + 13);
        labels.forEach((l) => svg.append("text").attr("x", width - m.r + 6).attr("y", y(l.z) + 4).attr("font-size", 10).attr("fill", l.c).text(l.name));
      }
    }
  }
  onSchemeChange(() => last && draw(...last));
  return { draw, repaint: () => last && draw(...last) };
}
