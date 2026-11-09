// The synthetic wedge: a bed thinning from 80 m to nothing, seen through the data's wavelet. Left, the
// seismic response as variable density; right, apparent against true thickness. Synthetic, and says so.
import { token, onSchemeChange } from "../runtime/js/subscout.js";

export default function wedge(el, datasets) {
  const W = datasets.wedge;
  const nT = W.thickness_m.length, nS = W.t_ms.length;
  const wrap = d3.select(el).selectAll("div.ss-wedge").data([0]).join("div").attr("class", "ss-wedge").style("position", "relative");
  const canvas = wrap.selectAll("canvas").data([0]).join("canvas").style("display", "block").style("position", "absolute").style("left", 0).style("top", 0);
  const svg = wrap.selectAll("svg").data([0]).join("svg").style("position", "absolute").style("left", 0).style("top", 0).attr("role", "img")
    .attr("aria-label", "Synthetic wedge model and apparent thickness against true thickness");
  const img = document.createElement("canvas"); img.width = nT; img.height = nS;
  const ctx = img.getContext("2d"), id = ctx.createImageData(nT, nS);
  function paint(dark) {
    for (let i = 0; i < nT; i++) for (let j = 0; j < nS; j++) {
      const a = W.amp[i][j], v = dark ? 128 + a * 110 : 128 - a * 115, k = (j * nT + i) * 4;
      id.data[k] = id.data[k + 1] = id.data[k + 2] = Math.max(0, Math.min(255, v)); id.data[k + 3] = 255;
    }
    ctx.putImageData(id, 0, 0);
  }
  let last = null;
  function draw(width, state = {}) {
    last = [width, state];
    const dark = document.documentElement.dataset.colourScheme === "dark" || ((getComputedStyle(document.documentElement).getPropertyValue("color-scheme") || "").includes("dark"));
    paint(dark);
    const narrow = width < 600;
    const H = Math.round(Math.min(Math.max(width * 0.5, 240), window.innerHeight * (narrow ? 0.28 : 0.5)));
    const m = { l: 40, r: 8, t: 22, b: 30 }, split = narrow ? width : Math.round(width * 0.58);
    const v = W.v_m_s;
    const tdom = [20, 20 + 160];
    wrap.style("height", `${H}px`);
    const x = d3.scaleLinear().domain([0, 80]).range([m.l, split - 16]);
    const y = d3.scaleLinear().domain(tdom).range([m.t, H - m.b]);
    const dpr = window.devicePixelRatio || 1;
    canvas.attr("width", width * dpr).attr("height", H * dpr).style("width", `${width}px`).style("height", `${H}px`);
    const g = canvas.node().getContext("2d"); g.setTransform(dpr, 0, 0, dpr, 0, 0); g.clearRect(0, 0, width, H);
    const sy0 = tdom[0], sy1 = tdom[1];
    g.drawImage(img, 0, sy0, nT, sy1 - sy0, x(0), y(tdom[0]), x(80) - x(0), y(tdom[1]) - y(tdom[0]));
    svg.attr("viewBox", `0 0 ${width} ${H}`).attr("width", width).attr("height", H).selectAll("*").remove();
    const muted = token("text-muted") || "#888", ink = token("text") || "currentColor", hi = token("data-highlight");
    // true top and base of the bed
    svg.append("line").attr("x1", x(0)).attr("x2", x(80)).attr("y1", y(W.top_ms)).attr("y2", y(W.top_ms)).attr("stroke", hi).attr("stroke-width", 1.2).attr("stroke-dasharray", "4 3");
    svg.append("line").attr("x1", x(0)).attr("x2", x(80)).attr("y1", y(W.top_ms)).attr("y2", y(W.top_ms + 2 * 80 / v * 1000)).attr("stroke", hi).attr("stroke-width", 1.2).attr("stroke-dasharray", "4 3");
    svg.append("text").attr("x", x(2)).attr("y", y(W.top_ms) - 5).attr("font-size", 10.5).attr("fill", hi).attr("paint-order", "stroke").attr("stroke", dark ? "#1b2430" : "#fff").attr("stroke-width", 3).text("true top and base of the bed (dashed)");
    svg.append("g").attr("transform", `translate(0,${H - m.b})`).call(d3.axisBottom(x).ticks(5).tickSize(3).tickFormat((d) => `${d} m`))
      .call((gg) => gg.select(".domain").remove()).call((gg) => gg.selectAll("text").attr("fill", muted).attr("font-size", 10));
    svg.append("text").attr("x", (x(0) + x(80)) / 2).attr("y", H - 2).attr("text-anchor", "middle").attr("font-size", 10.5).attr("fill", muted).text("true thickness of the bed");
    svg.append("g").attr("transform", `translate(${m.l},0)`).call(d3.axisLeft(y).ticks(4).tickSize(3).tickFormat((d) => `${d}`))
      .call((gg) => gg.select(".domain").remove()).call((gg) => gg.selectAll("text").attr("fill", muted).attr("font-size", 10));
    svg.append("text").attr("x", 2).attr("y", 10).attr("font-size", 10).attr("fill", muted).text("ms");
    svg.append("text").attr("x", x(0)).attr("y", m.t - 8).attr("font-size", 11).attr("font-weight", 600).attr("fill", ink).text(narrow ? `Synthetic, ${W.f_hz} Hz wavelet` : `Seismic response, synthetic (${W.f_hz} Hz wavelet, ${v.toLocaleString("en-GB")} m/s)`);
    // tuning marker
    svg.append("line").attr("x1", x(W.tuning_m)).attr("x2", x(W.tuning_m)).attr("y1", y(tdom[0])).attr("y2", y(tdom[1])).attr("stroke", ink).attr("stroke-width", 1).attr("opacity", 0.6);
    svg.append("text").attr("x", x(W.tuning_m) + 4).attr("y", y(tdom[1]) - 6).attr("font-size", 10.5).attr("fill", ink).attr("paint-order", "stroke").attr("stroke", dark ? "#1b2430" : "#fff").attr("stroke-width", 3).text(`tuning ${W.tuning_m} m`);
    if (narrow) return;
    // right: apparent vs true thickness
    const x2 = d3.scaleLinear().domain([0, 80]).range([split + 34, width - m.r]);
    const y2 = d3.scaleLinear().domain([0, 80]).range([H - m.b, m.t]);
    svg.append("g").attr("transform", `translate(0,${H - m.b})`).call(d3.axisBottom(x2).ticks(4).tickSize(3).tickFormat((d) => `${d}`))
      .call((gg) => gg.select(".domain").remove()).call((gg) => gg.selectAll("text").attr("fill", muted).attr("font-size", 10));
    svg.append("g").attr("transform", `translate(${split + 34},0)`).call(d3.axisLeft(y2).ticks(4).tickSize(-(width - m.r - split - 34)).tickFormat((d) => `${d}`))
      .call((gg) => gg.select(".domain").remove()).call((gg) => gg.selectAll("line").attr("stroke", token("data-context")).attr("opacity", 0.35)).call((gg) => gg.selectAll("text").attr("fill", muted).attr("font-size", 10));
    svg.append("text").attr("x", split + 34).attr("y", m.t - 8).attr("font-size", 11).attr("font-weight", 600).attr("fill", ink).text("Thickness the echo reports, m");
    svg.append("text").attr("x", (x2(0) + x2(80)) / 2).attr("y", H - 2).attr("text-anchor", "middle").attr("font-size", 10.5).attr("fill", muted).text("true thickness, m");
    svg.append("line").attr("x1", x2(0)).attr("x2", x2(80)).attr("y1", y2(0)).attr("y2", y2(80)).attr("stroke", token("data-context")).attr("stroke-dasharray", "3 3");
    const pts = W.thickness_m.map((t, i) => ({ t, a: W.apparent_m[i] })).filter((p) => p.t > 0);
    svg.append("path").attr("d", d3.line().x((p) => x2(p.t)).y((p) => y2(Math.min(p.a, 80)))(pts)).attr("fill", "none").attr("stroke", token("data-story-1")).attr("stroke-width", 2);
    svg.append("line").attr("x1", x2(W.tuning_m)).attr("x2", x2(W.tuning_m)).attr("y1", y2(0)).attr("y2", y2(80)).attr("stroke", ink).attr("opacity", 0.6);
    svg.append("text").attr("x", x2(W.tuning_m) + 4).attr("y", y2(70)).attr("font-size", 10.5).attr("fill", ink).text("below this, the two");
    svg.append("text").attr("x", x2(W.tuning_m) + 4).attr("y", y2(70) + 13).attr("font-size", 10.5).attr("fill", ink).text("echoes blur into one");
  }
  onSchemeChange(() => last && draw(...last));
  return { draw, repaint: () => last && draw(...last) };
}
