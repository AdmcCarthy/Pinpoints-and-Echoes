// One inline of the Volve full stack through the well, drawn as variable density on a canvas.
// state: { horizons } draws the published interpretation on top; { zoom } narrows to the reservoir.
import { token, onSchemeChange } from "../runtime/js/subscout.js";

export default function section(el, datasets) {
  const S = datasets.section;
  const H = datasets.horizons.map((r) => ({ h: r.horizon, xl: +r.crossline, t: +r.twt_ms }));
  const byH = d3.group(H, (r) => r.h);
  const n = S.crosslines.length, ns = S.n_samples;
  const xlIndex = new Map(S.crosslines.map((v, i) => [v, i]));
  const wrap = d3.select(el).selectAll("div.ss-section").data([0]).join("div").attr("class", "ss-section").style("position", "relative");
  const canvas = wrap.selectAll("canvas").data([0]).join("canvas").style("display", "block").style("position", "absolute").style("left", 0).style("top", 0);
  const svg = wrap.selectAll("svg").data([0]).join("svg").style("position", "absolute").style("left", 0).style("top", 0).attr("role", "img")
    .attr("aria-label", "Seismic inline through the well, two-way time against distance, with the published horizons");
  const img = document.createElement("canvas");
  img.width = n; img.height = ns;
  const g0 = img.getContext("2d"), id = g0.createImageData(n, ns);
  let dark = false;
  function paint() {
    dark = (getComputedStyle(document.documentElement).getPropertyValue("color-scheme") || "").includes("dark") || document.documentElement.dataset.colourScheme === "dark";
    for (let i = 0; i < n; i++) for (let j = 0; j < ns; j++) {
      const a = S.amp[i][j] / 127; // -1..1
      const v = dark ? 128 + a * 110 : 128 - a * 115; // positive dark on light, light on dark
      const k = (j * n + i) * 4;
      id.data[k] = id.data[k + 1] = id.data[k + 2] = Math.max(0, Math.min(255, v)); id.data[k + 3] = 255;
    }
    g0.putImageData(id, 0, 0);
  }
  paint();
  let last = null;

  function draw(width, state = {}) {
    last = [width, state];
    const narrow = width < 600;
    const Hpx = Math.round(Math.min(Math.max(width * 0.6, 260), window.innerHeight * (narrow ? 0.34 : 0.6)));
    const m = { l: 44, r: 8, t: 8, b: 26 };
    const t0 = S.t0_ms, t1 = S.t0_ms + (ns - 1) * S.dt_ms;
    const wellX = S.well_dist_m;
    const xdom = state.zoom ? [wellX - 1500, wellX + 1500] : [S.dist_m[0], S.dist_m[n - 1]];
    const tdom = state.zoom ? [2450, 3000] : [t0, t1];
    wrap.style("height", `${Hpx}px`);
    const x = d3.scaleLinear().domain(xdom).range([m.l, width - m.r]);
    const y = d3.scaleLinear().domain(tdom).range([m.t, Hpx - m.b]);
    const dpr = window.devicePixelRatio || 1;
    canvas.attr("width", width * dpr).attr("height", Hpx * dpr).style("width", `${width}px`).style("height", `${Hpx}px`);
    const g = canvas.node().getContext("2d");
    g.setTransform(dpr, 0, 0, dpr, 0, 0); g.clearRect(0, 0, width, Hpx);
    g.imageSmoothingEnabled = true;
    // source rect in image pixels
    const di = (S.dist_m[n - 1] - S.dist_m[0]) / (n - 1);
    const sx0 = (xdom[0] - S.dist_m[0]) / di, sx1 = (xdom[1] - S.dist_m[0]) / di;
    const sy0 = (tdom[0] - t0) / S.dt_ms, sy1 = (tdom[1] - t0) / S.dt_ms;
    g.save(); g.beginPath(); g.rect(m.l, m.t, width - m.l - m.r, Hpx - m.t - m.b); g.clip();
    g.drawImage(img, sx0, sy0, sx1 - sx0, sy1 - sy0, m.l, m.t, width - m.l - m.r, Hpx - m.t - m.b);
    g.restore();
    svg.attr("viewBox", `0 0 ${width} ${Hpx}`).attr("width", width).attr("height", Hpx).selectAll("*").remove();
    const muted = token("text-muted") || "#888";
    svg.append("g").attr("transform", `translate(${m.l},0)`).call(d3.axisLeft(y).ticks(5).tickSize(3).tickFormat((d) => `${d}`))
      .call((gg) => gg.select(".domain").remove()).call((gg) => gg.selectAll("text").attr("fill", muted).attr("font-size", 10));
    svg.append("text").attr("x", 2).attr("y", m.t + 9).attr("font-size", 10).attr("fill", muted).text("ms");
    svg.append("g").attr("transform", `translate(0,${Hpx - m.b})`).call(d3.axisBottom(x).tickValues(d3.range(Math.ceil((xdom[0] - wellX) / 1000) * 1000, xdom[1] - wellX + 1, narrow ? 2000 : 1000).map((v) => v + wellX)).tickSize(3).tickFormat((d) => `${Math.round((d - wellX) / 1000)} km`))
      .call((gg) => gg.select(".domain").remove()).call((gg) => gg.selectAll("text").attr("fill", muted).attr("font-size", 10));
    // well
    svg.append("line").attr("x1", x(wellX)).attr("x2", x(wellX)).attr("y1", m.t).attr("y2", Hpx - m.b).attr("stroke", token("data-highlight")).attr("stroke-width", 2).attr("stroke-dasharray", "4 3");
    svg.append("text").attr("x", x(wellX) + 5).attr("y", m.t + 13).attr("font-size", 11).attr("font-weight", 600).attr("fill", token("data-highlight")).attr("paint-order", "stroke").attr("stroke", dark ? "#1b2430" : "#fff").attr("stroke-width", 3).text(S.well);
    if (state.horizons) {
      const colours = [token("data-cat-1"), token("data-cat-2"), token("data-cat-3"), token("data-cat-4"), token("data-cat-5")];
      let k = 0;
      const labs = [];
      for (const [name, pts] of byH) {
        const p = pts.filter((r) => xlIndex.has(r.xl)).map((r) => ({ d: S.dist_m[xlIndex.get(r.xl)], t: r.t })).filter((r) => r.d >= xdom[0] && r.d <= xdom[1] && r.t >= tdom[0] && r.t <= tdom[1]).sort((a, b) => a.d - b.d);
        if (!p.length) { k++; continue; }
        const c = colours[k++ % colours.length];
        svg.append("path").attr("d", d3.line().x((r) => x(r.d)).y((r) => y(r.t))(p)).attr("fill", "none").attr("stroke", c).attr("stroke-width", 1.8);
        const lab = p[p.length - 1];
        labs.push({ name, c, x: Math.min(x(lab.d), width - m.r - 4), y: y(lab.t) - 4 });
      }
      labs.sort((a, b) => a.y - b.y);
      for (let i = 1; i < labs.length; i++) if (labs[i].y - labs[i - 1].y < 13) labs[i].y = labs[i - 1].y + 13;
      for (const l of labs) svg.append("text").attr("x", l.x).attr("y", l.y).attr("text-anchor", "end").attr("font-size", 10.5).attr("font-weight", 600)
        .attr("fill", l.c).attr("paint-order", "stroke").attr("stroke", dark ? "#1b2430" : "#fff").attr("stroke-width", 3).text(l.name);
    }
  }
  onSchemeChange(() => { paint(); last && draw(...last); });
  return { draw, repaint: () => { paint(); last && draw(...last); } };
}
