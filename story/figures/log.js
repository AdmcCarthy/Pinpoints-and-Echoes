// Composite log of one well: four tracks against depth below sea level. state: { zoom } true shows the
// reservoir only, so the 10 cm sampling is visible. Depth points down.
import { token, onSchemeChange } from "../runtime/js/subscout.js";

const TRACKS = [
  { key: "gr_api", label: "Gamma ray", unit: "API", dom: [0, 150] },
  { key: "rhob_g_cm3", label: "Density", unit: "g/cm³", dom: [1.95, 2.95] },
  { key: "rt_ohm_m", label: "Resistivity", unit: "ohm·m", dom: [0.2, 200], log: true },
  { key: "dt_us_ft", label: "Sonic", unit: "µs/ft", dom: [140, 40] },
];

export default function log(el, datasets, opts = {}) {
  const rows = datasets.log.map((r) => ({ z: +r.tvdss_m, gr_api: +r.gr_api, rhob_g_cm3: +r.rhob_g_cm3, rt_ohm_m: +r.rt_ohm_m, dt_us_ft: +r.dt_us_ft }));
  const res = opts.states?.find?.((s) => s.reservoir)?.reservoir ?? [3181.5, 3282.8];
  const svg = d3.select(el).selectAll("svg").data([0]).join("svg").attr("role", "img").attr("aria-label", "Composite well log, four tracks against depth");
  let last = null;

  function draw(width, state = {}) {
    last = [width, state];
    const zoom = !!state.zoom;
    const narrow = width < 600;
    const H = Math.round(Math.min(Math.max(width * 0.7, 300), window.innerHeight * (narrow ? 0.34 : 0.62)));
    const m = { l: 46, r: 8, t: 30, b: 8 };
    const tracks = narrow ? TRACKS.slice(0, 3) : TRACKS;
    svg.attr("viewBox", `0 0 ${width} ${H}`).attr("width", width).attr("height", H).selectAll("*").remove();
    const zdom = zoom ? [res[0] - 15, res[1] + 15] : d3.extent(rows, (r) => r.z);
    const y = d3.scaleLinear().domain(zdom).range([m.t, H - m.b]);
    const tw = (width - m.l - m.r) / tracks.length, gap = 10;
    const muted = token("text-muted") || "#888", ink = token("text") || "currentColor";
    // reservoir band
    svg.append("rect").attr("x", m.l).attr("width", width - m.l - m.r).attr("y", y(res[0])).attr("height", Math.max(0, y(res[1]) - y(res[0])))
      .attr("fill", token("data-highlight")).attr("opacity", 0.1);
    svg.append("text").attr("x", width - m.r - 2).attr("y", y(res[0]) - 3).attr("text-anchor", "end").attr("font-size", 10).attr("fill", token("data-highlight")).text("Hugin Fm");
    // depth axis
    svg.append("g").attr("transform", `translate(${m.l},0)`).call(d3.axisLeft(y).ticks(zoom ? 6 : 8).tickSize(-(width - m.l - m.r)).tickFormat((d) => `${d}`))
      .call((g) => g.select(".domain").remove()).call((g) => g.selectAll("line").attr("stroke", token("data-context")).attr("opacity", 0.3))
      .call((g) => g.selectAll("text").attr("fill", muted).attr("font-size", 10));
    svg.append("text").attr("x", 2).attr("y", 10).attr("font-size", 10).attr("fill", muted).text("m below MSL");
    tracks.forEach((t, i) => {
      const x0 = m.l + i * tw + gap / 2, x1 = m.l + (i + 1) * tw - gap / 2;
      const x = (t.log ? d3.scaleLog() : d3.scaleLinear()).domain(t.dom).range([x0, x1]).clamp(true);
      const colour = i === 0 ? token("data-story-1") : i === 1 ? token("data-story-2") : i === 2 ? token("data-story-3") : token("data-story-4") || token("data-story-1");
      svg.append("text").attr("x", (x0 + x1) / 2).attr("y", m.t - 16).attr("text-anchor", "middle").attr("font-size", 11).attr("font-weight", 600).attr("fill", ink).text(t.label);
      svg.append("text").attr("x", (x0 + x1) / 2).attr("y", m.t - 5).attr("text-anchor", "middle").attr("font-size", 9.5).attr("fill", muted).text(`${t.dom[0]} – ${t.dom[1]} ${t.unit}`);
      const pts = rows.filter((r) => Number.isFinite(r[t.key]) && r.z >= zdom[0] && r.z <= zdom[1]);
      const line = d3.line().x((r) => x(r[t.key])).y((r) => y(r.z)).defined((r) => Number.isFinite(r[t.key]));
      svg.append("path").attr("d", line(pts)).attr("fill", "none").attr("stroke", colour).attr("stroke-width", zoom ? 1.4 : 0.9);
      if (i) svg.append("line").attr("x1", x0 - gap / 2).attr("x2", x0 - gap / 2).attr("y1", m.t).attr("y2", H - m.b).attr("stroke", token("data-context")).attr("opacity", 0.5);
    });
  }
  onSchemeChange(() => last && draw(...last));
  return { draw, repaint: () => last && draw(...last) };
}
