/* The workbench page. It reads the modules, runs and experiments from the server.
   Every run belongs to an experiment. Nothing here lists the modules or their settings. */
"use strict";
let CAT = { core: [], optional: [], core_figures: [], problems: [] };
const $ = id => document.getElementById(id);
function el(tag, attrs, ...kids) {
  const n = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs || {})) {
    if (v == null || v === false) continue;
    if (k === "text") n.textContent = v;
    else if (k === "html") n.innerHTML = v;
    else if (k.startsWith("on")) n.addEventListener(k.slice(2), v);
    else n.setAttribute(k, v === true ? "" : v);
  }
  for (const c of kids.flat()) if (c != null && c !== false) n.append(c.nodeType ? c : document.createTextNode(c));
  return n;
}
const SVGNS = "http://www.w3.org/2000/svg";
function s(tag, attrs) { const n = document.createElementNS(SVGNS, tag); for (const [k, v] of Object.entries(attrs || {})) if (v != null) n.setAttribute(k, v); return n; }
const css = v => getComputedStyle(document.documentElement).getPropertyValue(v).trim();
const esc = t => String(t).replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
const mean = a => a.reduce((x, y) => x + y, 0) / a.length;

// ================================================ words
const TERMS = {
  dk: "How many times larger the average top-100 firm is than the average firm, measured by capitalization.",
  capitalization: "What owners think a firm is worth: its expected earnings, priced today.",
  breadth: "How many times more people the average top-100 firm employs than the average firm.",
  depth: "How many times more the top 100 earn for each employee than the average firm.",
  top100: "The 100 firms with the highest capitalization each year. The theory calls them dominant capital.",
  baseline: "The run that other runs are compared with.",
  gain: "How much a module raised or lowered differential capitalization, on a log scale. 0.05 is about 5%.",
  seed: "A number that fixes the chance events in a run. The same seed and settings give the same result.",
  resistance: "Push-back against rising prices, unemployment and the power of the top 100, from 0 to 1.",
  ledger: "The model's list of firms and its bookkeeping. It works out some figures itself each year.",
  spread: "The lowest and highest result across seeds.",
  markup: "How much a firm adds to its wage cost when it sets a price.",
};
const term = (key, text) => el("span", { class: "term", tabindex: "0", "data-tip": TERMS[key] }, text);

// ================================================ figures
const FIGS = [
  { key: "dk", title: "Differential capitalization", short: "Average top-100 firm's capitalization, as a multiple of the average firm's.", line: () => [term("capitalization", "Capitalization"), " of the average ", term("top100", "top-100"), " firm, divided by the average firm's."], unit: "x", log: true },
  { key: "breadth", title: "Breadth", short: "Employees of the average top-100 firm, as a multiple of the average firm's.", line: () => ["Employees of the average ", term("top100", "top-100"), " firm, divided by the average firm's."], unit: "x", log: true },
  { key: "depth", title: "Depth", short: "Earnings per employee of the top 100, as a multiple of the average firm's.", line: () => ["Earnings per employee of the top 100, divided by the average firm's."], unit: "x" },
  { key: "unemployment", title: "Unemployment", short: "Per cent of the working population without paid work.", line: () => ["Per cent of the working population without paid work."], unit: "pct" },
  { key: "capital_share", title: "Capitalist share of income", short: "Per cent of all income that goes to owners.", line: () => ["Per cent of all income that goes to owners."], unit: "pct" },
  { key: "price_level", title: "Price level", short: "Average price. The wage at the start is 1.", line: () => ["Average price. The wage at the start is 1."], unit: "num", log: true },
  { key: "inflation", title: "Inflation", short: "Change in the price level from the year before.", line: () => ["Change in the price level from the year before."], unit: "pct" },
  { key: "resistance", title: "Resistance", short: "From 0 (none) to 1 (most).", line: () => [term("resistance", "Resistance"), " from 0 (none) to 1 (most)."], unit: "num", fixed: [0, 1] },
  { key: "mergers_against_hiring", title: "Mergers against new hiring", short: "Employees bought by the top 100 for each new hire.", line: () => ["Employees bought by the top 100 for each new hire."], unit: "num" },
];
const FIG = Object.fromEntries(FIGS.map(f => [f.key, f]));
const OTHER_NAMES = {
  firms: "Number of firms", d_risk: "Differential risk", d_hype: "Differential hype", top_share_employees: "Top 100's share of employees",
  top_share_cap: "Top 100's share of capitalization", markup: "Average markup", markup_top: "Average markup of the top 100",
  employment: "People employed", wage: "Wage", roadblocks: "Roadblocks against mergers", perm_sector: "Sector boundary opening",
  perm_nation: "National boundary opening", government_debt: "Government debt", corporate_debt: "Corporate debt",
  interest_share: "Interest share of capitalist income", merger_volume: "Merger volume", crisis: "Crisis level",
  stagflation_intensity: "Stagflation intensity", cohesion: "Cohesion of the top 100", power_index: "Power index", nrr: "Normal rate of return",
};
const PCT = new Set(["unemployment", "capital_share", "inflation", "top_share_employees", "top_share_cap", "interest_share", "nrr"]);
function fmt(v, unit) {
  if (v == null || !isFinite(v)) return "–";
  if (unit === "pct") return (v * 100).toFixed(1) + "%";
  const a = Math.abs(v);
  if (a >= 1000) return Math.round(v).toLocaleString("en-GB");
  if (a >= 100) return v.toFixed(0);
  if (a >= 10) return v.toFixed(1);
  return v.toFixed(2);
}
const signed = (v, d = 2) => v == null ? "–" : (v > 0 ? "+" : v < 0 ? "−" : "") + Math.abs(v).toFixed(d);

// ================================================ modules
const HUB = "ledger";
const SHORT = { sabotage: "Sabotage", debt: "Debt", greenfield: "Green-field growth", mergers: "Mergers", "cost cutting": "Cost cutting",
  stagflation: "Stagflation", compass: "Compass", resistance: "Resistance", envelope: "Envelope", turnover: "Changes in the top 100",
  compasses: "Compass: impunity", compass_targets: "Compass: targets", compass_ahead: "Compass: lead", compass_consensus: "Compass: consensus",
  boundary_contest: "Boundary contest", second_country: "Second country", public_debt: "Public debt", household_debt: "Household debt",
  risk_shaping: "Risk shaping", policy_rate: "Policy rate", sovereign_funds: "Sovereign funds", cross_border: "Cross-border",
  concentration_measures: "Concentration", proletarianization: "Proletarianization", labour: "Organised labour", force: "Organised force",
  sales: "Sales", leaders: "Price leaders", coalitions: "Coalitions", owners: "Owners", hype: "Hype", protections: "Protections",
  privatisation: "Privatisation", barriers: "Barriers", hierarchy: "Hierarchy", wants: "Wants", eruptions: "Eruptions", energy: "Energy",
  externalisation: "Externalisation", nature: "Nature", currencies: "Currencies", synchronisation: "Synchronisation", fear: "Fear", plant: "Plant" };
const LINE = {
  sabotage: "Sets each firm's markup. Firms in industries that a few large firms control add more.",
  debt: "Records lending to government, firms and households.",
  greenfield: "Firms hire new workers, and new small firms are founded.",
  mergers: "Large firms buy other firms they can reach.",
  "cost cutting": "Firms lower their costs. Rivals copy them, so the gain does not last.",
  stagflation: "Large firms raise prices faster than small ones.",
  compass: "Decides whether large firms lean towards mergers or price rises.",
  resistance: "People push back against price rises, unemployment and mergers.",
  envelope: "Opens the boundaries between industries, sectors and countries.",
  sales: "Works out how much of what firms offer can be sold.",
  leaders: "Splits each industry into price leaders and followers.",
  boundary_contest: "Sets each boundary by a contest between pressure to open it and the hold that keeps it shut.",
  compasses: "Turns to price rises when large firms can act with impunity.",
  compass_targets: "Turns to price rises when firms to buy run out.",
  compass_ahead: "Turns to price rises when large firms lead in size.",
  compass_consensus: "Turns to price rises when most large firms agree.",
  coalitions: "Groups large firms into coalitions that cooperate or fight.",
  force: "Holds a level of organised force that rises with stagflation.",
  owners: "Records who owns each firm, directly or through funds.",
  hype: "Lets owners' expectations run ahead of earnings and fall back.",
  risk_shaping: "Lets large firms use ties to government to lower their risk.",
  public_debt: "Records who holds the public debt and who pays the interest.",
  policy_rate: "Moves the normal rate of return with employment and resistance.",
  protections: "Lets firms with ties to government bar others from their industry.",
  privatisation: "Moves jobs from public employment to firms.",
  barriers: "Lets resistance win barriers against buying in some sectors.",
  proletarianization: "Moves people from outside wage work into the working population.",
  labour: "Organises employees by industry. Organised labour pushes against markups.",
  household_debt: "Lends to wage earners and records what they owe.",
  hierarchy: "Adds ranks and pay inside each firm.",
  wants: "Firms spend part of their earnings on shaping what people want.",
  eruptions: "Lets resistance erupt and change the rules for a time.",
  energy: "Records energy use and how it is shared.",
  externalisation: "Lets firms push costs onto employees, communities and later years.",
  nature: "Treats ownership of nature as a source of markup.",
  second_country: "Adds a second country with its own firms and mergers.",
  cross_border: "Lets firms own firms in the other country.",
  currencies: "Gives the second country its own currency.",
  sovereign_funds: "Adds a government fund that owns shares.",
  synchronisation: "Measures whether mergers and price rises move together across sectors.",
  fear: "Measures the power index and systemic fear.",
  plant: "Compares capitalization with the value of plant and equipment.",
  concentration_measures: "Measures concentration in 18 other ways.",
};
const SETTING_LABEL = { new_claim_share: "Share to new firms", new_claim_size: "New firm size", base_rate: "Base rate", max_rise: "Maximum price rise",
  short: "Short window, years", long: "Long window, years", government_part: "Government share", from_mergers: "From mergers", from_inflation: "From inflation" };
const firmify = t => String(t || "").replace(/\bdominant capital\b/gi, "the top 100").replace(/\bclaims\b/g, "firms").replace(/\bclaim\b/g, "firm").replace(/\bClaims\b/g, "Firms").replace(/\bClaim\b/g, "Firm");
const human = n => { const t = n.replace(/_/g, " ").replace(/\bclaim\b/g, "firm"); return t.charAt(0).toUpperCase() + t.slice(1); };
const setLabel = n => SETTING_LABEL[n] || human(n);
const MODS = {};
const CORE_ORDER = ["sabotage", "greenfield", "mergers", "cost cutting", "stagflation", "compass", "resistance", "envelope", "debt"];
const keyOf = mid => mid.replace(/^(core|opt):/, "");
const midOf = name => (MODS[name] && MODS[name].core ? "core:" : "opt:") + name;
const modName = n => n === HUB ? "Ledger" : SHORT[keyOf(n)] || (MODS[keyOf(n)] || {}).title || human(keyOf(n));
const optGroup = m => (m.replaces && m.replaces.length) ? "instead" : (/\breadout\b|changes nothing|changes no term/i.test(m.doc_note || "") ? "measure" : "rule");
function defaultOf(mid, name) { const m = MODS[keyOf(mid)]; const st = m && m.settings.find(x => x.name === name); return st ? st.default : undefined; }
function valueIn(spec, mid, name) { const v = ((spec.settings || {})[mid] || {})[name]; return v !== undefined ? v : defaultOf(mid, name); }
const same = (a, b) => String(a) === String(b) || (isFinite(+a) && isFinite(+b) && String(a) !== "" && String(b) !== "" && Math.abs(+a - +b) < 1e-12);
const modLink = (name, text) => el("button", { class: "modlink", type: "button", "data-tip": "Open on the map", onclick: e => { e.stopPropagation(); openModule(name); } }, text || modName(name));

// ================================================ runs and experiments, as the page holds them
let runs = [], groups = [];
const byId = id => runs.find(r => r.id === id);
const gById = id => groups.find(g => g.id === id);
const membersOf = g => g.runIds.map(byId).filter(Boolean);
const showVal = v => v === true ? "On" : v === false ? "Off" : String(v);
const comboKey = r => (r.vals || []).map(showVal).join(" · ");
function combos(g) { const out = []; for (const r of membersOf(g)) { const k = comboKey(r); if (!out.includes(k)) out.push(k); } return out; }
// A value column takes the colour of its first ticked run.
const comboColour = (g, k) => { const ms = membersOf(g).filter(r => comboKey(r) === k); return colourOf(ms.find(r => state.shown.has(r.id)) || ms[0]); };
const ENDED = new Set(["done", "stopped", "failed"]);
const hasData = r => r.rows.length > 0 && r.step >= 0;
const runLabel = r => r.name;
const fullName = r => r.name;
function colLabel(c) { return c.kind === "module" ? `${modName(c.name)} on or off` : `${modName(c.mod)} › ${setLabel(c.name)}`; }
function colBase(c, baseRun) { return c.kind === "module" ? (baseRun.optional || []).includes(c.name) : valueIn(baseRun, c.mod, c.name); }
let DEFAULT_BASE = null;
const baseOf = id => byId(id) || DEFAULT_BASE;
function startFromOptions(selId) { return runs.some(hasData) ? runOptions(() => true, selId) : [el("option", { value: "__default", text: DEFAULT_BASE.name })]; }
const startBtn = () => el("button", { class: "btn primary", type: "button", text: "Start a run", onclick: () => openSetup(null, null) });
function emptyState(text, withStart) { return el("div", { class: "empty" }, el("p", { text }), withStart ? startBtn() : null); }
const noRuns = () => !runs.length;
// The reference for Diff and Experiment: the baseline if it is ticked, otherwise the first ticked run.
function refOf(shown) { const b = byId(state.baseline); return shown.includes(b) ? b : shown[0]; }

const state = {
  shown: new Set(), slot: new Map(), baseline: null, tab: "charts",
  open: new Set(), closed: new Set(), renaming: null, hover: null, extra: [], log: { dk: true }, gainRun: null,
  expView: "grid", sumFig: "dk", recent: null,
  map: { run: null, vs: "", measure: "run", year: 1920, sel: null, hiFig: null, fig: null },
};

// ---- run colours: given when a run is ticked, the first colour no other ticked run uses
const PALETTE = 8;
function tick(id) {
  state.shown.add(id);
  if (!state.slot.has(id)) { const used = new Set(state.slot.values()); let i = 0; while (used.has(i) && i < PALETTE) i++; state.slot.set(id, i < PALETTE ? i : state.slot.size % PALETTE); }
}
function untick(id) { state.shown.delete(id); state.slot.delete(id); }
function setTicks(ids) { for (const id of [...state.shown]) if (!ids.includes(id)) untick(id); for (const id of ids) tick(id); }
function colourOf(r) { return r && state.slot.has(r.id) ? css(`--s${state.slot.get(r.id) + 1}`) : css("--unticked"); }
function saveView() { store("ticks", [...state.slot.entries()]); store("baseline", state.baseline); store("tab", state.tab); }

// ---- module colours: a fixed, muted palette that shares no hue with the run colours
const MOD_COLOURS = { sabotage: "#8c6d5a", greenfield: "#7d8a5c", mergers: "#5d6f86", "cost cutting": "#a8926a", stagflation: "#8a5f6e", compass: "#6f7f7a",
  resistance: "#6b5b7b", envelope: "#9c8a7a", debt: "#5f7a70", turnover: "#9a9a9a", labour: "#7a6a50", public_debt: "#6d7f94" };
const MOD_EXTRA = ["#7f7461", "#68727d", "#8d7b6b", "#6e7a62", "#7c6b78", "#8a8670", "#5f6b6b", "#957f72"];
function modColour(name) {
  if (MOD_COLOURS[name]) return MOD_COLOURS[name];
  let h = 0; for (const c of name) h = (h * 31 + c.charCodeAt(0)) >>> 0;
  return MOD_EXTRA[h % MOD_EXTRA.length];
}

// ---- experiment details kept in this browser: the run a table started from, and its columns
const expMeta = id => recall("exp:" + id, null);
function deriveCols(ms) {
  if (ms.length < 2) return [];
  const cols = [];
  const opts = [...new Set(ms.flatMap(r => r.optional))];
  for (const k of opts) if (ms.some(r => r.optional.includes(k) !== ms[0].optional.includes(k))) cols.push({ kind: "module", name: k });
  const keys = new Map();
  for (const r of ms) for (const mid of Object.keys(r.settings || {})) for (const n of Object.keys(r.settings[mid])) keys.set(mid + "|" + n, [mid, n]);
  for (const [mid, n] of keys.values()) if (ms.some(r => !same(valueIn(r, mid, n), valueIn(ms[0], mid, n)))) cols.push({ kind: "setting", mod: mid, name: n });
  return cols;
}
function deriveAll() {
  for (const g of groups) {
    const ms = membersOf(g), meta = expMeta(g.id);
    g.base = meta && byId(meta.base) ? meta.base : ms[0] ? ms[0].id : null;
    g.claims = ms[0] ? ms[0].claims : 30000; g.years = ms[0] ? ms[0].years : 119;
    const cols = meta && meta.cols && meta.cols.length ? meta.cols : deriveCols(ms);
    // Group by value only when the runs vary one or more settings and nothing else but the seed.
    g.cols = cols.length === 1 || (meta && meta.cols && meta.cols.length) ? cols : [];
    for (const r of ms) r.vals = g.cols.length ? g.cols.map(c => c.kind === "module" ? r.optional.includes(c.name) : valueIn(r, c.mod, c.name)) : null;
  }
}

function diffs(run, base) {
  const out = [];
  if (!base || run === base) return out;
  if (run.claims !== base.claims) out.push(["Firms", base.claims.toLocaleString("en-GB"), run.claims.toLocaleString("en-GB")]);
  if (run.years !== base.years) out.push(["Years", base.years, run.years]);
  if (run.seed !== base.seed) out.push(["Seed", base.seed, run.seed]);
  const ob = new Set(base.optional), or = new Set(run.optional);
  for (const k of or) if (!ob.has(k)) out.push([modName(k), "Off", "On", k]);
  for (const k of ob) if (!or.has(k)) out.push([modName(k), "On", "Off", k]);
  const mods = new Set([...Object.keys(run.settings || {}), ...Object.keys(base.settings || {})]);
  for (const mid of mods) {
    const a = (base.settings || {})[mid] || {}, b = (run.settings || {})[mid] || {};
    for (const n of new Set([...Object.keys(a), ...Object.keys(b)])) {
      const av = valueIn(base, mid, n), bv = valueIn(run, mid, n);
      if (!same(av, bv)) out.push([`${modName(mid)} › ${setLabel(n)}`, av, bv, keyOf(mid)]);
    }
  }
  return out;
}
const diffLabel = d => d[3] ? [modLink(d[3], d[0].split(" › ")[0]), d[0].includes(" › ") ? " › " + d[0].split(" › ")[1] : ""] : [d[0]];
const diffLines = d => d.map(x => `${x[0]}: ${x[1]} → ${x[2]}`).join("\n");

// ================================================ server
async function api(path, method, body) {
  let res;
  try {
    res = await fetch(path, { method: method || "GET", headers: body ? { "Content-Type": "application/json" } : {}, body: body ? JSON.stringify(body) : undefined });
  } catch (e) { throw new Error("The workbench server is not responding. Check that it is still running."); }
  const text = await res.text();
  let data = {};
  try { data = text ? JSON.parse(text) : {}; } catch (e) { data = { error: text }; }
  if (!res.ok) throw new Error(data.error || `The server said: ${res.status}`);
  return data;
}
function store(key, value) { try { localStorage.setItem("workbench:" + key, JSON.stringify(value)); } catch (e) { /* not needed */ } }
function recall(key, fallback) { try { const v = localStorage.getItem("workbench:" + key); return v === null ? fallback : JSON.parse(v); } catch (e) { return fallback; } }
const STATUS = { finished: "done", running: "running", waiting: "waiting", stopped: "stopped", failed: "failed" };
// A run records its modules, and their gain, under each module's own name (for example "risk
// shaping"). The page knows optional modules by their name in registry.py ("risk_shaping"). Two
// registry names can share one module ("compasses" and "compass_consensus"), so prefer the one
// the run switched on.
function keyFor(n, optional) {
  if (MODS[n]) return n;
  const keys = CAT.optional.filter(m => m.model_name === n).map(m => m.name);
  return keys.find(k => optional.includes(k)) || keys[0] || n;
}
function keyedGain(gain, optional) { const out = {}; for (const [k, v] of Object.entries(gain || {})) out[keyFor(k, optional)] = v; return out; }
function toRun(sm, old) {
  const r = old || { rows: [] };
  Object.assign(r, { id: sm.id, name: sm.name, claims: sm.claims, years: sm.years, seed: sm.seed, optional: sm.optional || [], settings: sm.settings || {},
    group: sm.experiment, srv: sm.status, status: STATUS[sm.status] || sm.status, message: sm.message || "", rowsCount: sm.rows_count || 0, created: sm.created });
  r.modules = sm.modules && sm.modules.length ? sm.modules.map(n => keyFor(n, r.optional)) : [...CORE_ORDER, ...r.optional];
  r.step = r.rows.length - 1;
  return r;
}
async function fetchRows(r) {
  const d = await api(`/api/runs/${encodeURIComponent(r.id)}?since=${r.rows.length}`);
  for (const x of d.rows || []) if (x.year != null || x.step != null) r.rows.push({ year: x.year ?? (CAT.start_year || 1890) + x.step, v: x.values || {}, gain: keyedGain(x.gain, r.optional) });
  r.step = r.rows.length - 1;
  r.errorYear = d.error_year; r.guard = d.guard;
}
let pollTimer = null, lastSig = "";
async function refresh(force) {
  clearTimeout(pollTimer);
  try {
    const [rs, ex] = await Promise.all([api("/api/runs"), api("/api/experiments")]);
    const old = new Map(runs.map(r => [r.id, r]));
    runs = (rs.runs || []).map(sm => toRun(sm, old.get(sm.id)));
    const need = runs.filter(r => r.rowsCount > r.rows.length);
    for (let i = 0; i < need.length; i += 6) await Promise.all(need.slice(i, i + 6).map(fetchRows));
    groups = (ex.experiments || []).map(e => ({ id: e.id, name: e.name, created: e.created, runIds: e.run_ids || [] }));
    deriveAll();
    for (const id of [...state.shown]) if (!byId(id)) untick(id);
    if (!byId(state.baseline)) { const r = runs.find(hasData); state.baseline = r ? r.id : null; }
    if (!gById(state.recent)) state.recent = groups.length ? groups[groups.length - 1].id : null;
    for (const g of groups) if (!state.closed.has(g.id) && membersOf(g).length <= 6) state.open.add(g.id);
    const sig = JSON.stringify([runs.map(r => [r.id, r.name, r.status, r.rows.length, r.message, r.group]), groups.map(g => [g.id, g.name, g.runIds.length])]);
    if (force || sig !== lastSig) { lastSig = sig; if (pop.hidden && !state.renaming) renderAll(); else renderTab(); }
  } catch (e) { toast(e.message); }
  if (runs.some(r => r.status === "running" || r.status === "waiting")) pollTimer = setTimeout(() => refresh(), 1000);
}
async function act(path, body, done) {
  try { const d = await api(path, "POST", body || {}); if (done) done(d); await refresh(true); return d; }
  catch (e) { toast(e.message); return null; }
}

// ================================================ runs column
function openFolderInTab(g) { setTicks(membersOf(g).filter(r => hasData(r) || r.status === "failed").map(r => r.id)); saveView(); setTab("experiment"); renderRuns(); renderLegend(); }
function setBaseline(r) { state.baseline = r.id; saveView(); renderAll(); }
function renameInput(current, done) {
  let finished = false;
  const fin = v => { if (finished) return; finished = true; done(v); };
  return el("input", { class: "rename-input", value: current, "aria-label": "New name",
    onkeydown: e => { if (e.key === "Enter") fin(e.target.value.trim()); if (e.key === "Escape") fin(null); },
    onblur: e => fin(e.target.value.trim()) });
}
function kebab(label, open) {
  return el("button", { class: "kebab", type: "button", "aria-label": label, "aria-haspopup": "menu", "data-tip": "More actions", text: "⋯",
    onclick: e => { e.stopPropagation(); open(e.currentTarget, e.detail === 0); } });
}
function metaText(r) {
  const facts = `${r.claims.toLocaleString("en-GB")} firms · ${r.years} years · seed ${r.seed}`;
  if (r.status === "running") return [el("span", { class: "running", text: `Running, year ${Math.max(r.step, 0)} of ${r.years}` }), " · " + facts];
  if (r.status === "waiting") return [el("span", { class: "running", text: "Waiting" }), " · " + facts];
  if (r.status === "failed") return [el("span", { class: "failed", text: r.message ? `Stopped by the model: ${r.message}` : "Stopped by the model" })];
  if (r.status === "stopped") return [facts + ` · Stopped at year ${Math.max(r.step, 0)}`];
  return [facts];
}
function runRow(r) {
  const canTick = hasData(r) || r.status === "failed";
  const box = el("input", { type: "checkbox", id: "show-" + r.id, "aria-label": `Show ${r.name} on the charts`, disabled: !canTick || null,
    onchange: e => { e.target.checked ? tick(r.id) : untick(r.id); saveView(); renderAll(); } });
  box.checked = state.shown.has(r.id);
  const isBase = state.baseline === r.id;
  const star = el("button", { class: "star" + (isBase ? " on" : ""), type: "button", "aria-label": isBase ? `${r.name} is the baseline` : `Set ${r.name} as baseline`,
    "data-tip": isBase ? "Baseline" : "Set as baseline", text: isBase ? "★" : "☆", disabled: !hasData(r) || null, onclick: () => setBaseline(r) });
  const name = state.renaming === r.id
    ? renameInput(r.name, v => { state.renaming = null; if (v && v !== r.name) act(`/api/runs/${r.id}/rename`, { name: v }); else renderRuns(); })
    : el("label", { class: "run-name", for: "show-" + r.id }, el("span", { class: "swatch", style: `background:${colourOf(r)}` }), el("span", { text: r.name }));
  const meta = el("div", { class: "run-meta", "data-tip": r.status === "failed" && r.message ? r.message : null }, ...metaText(r));
  return el("div", { class: "run" + (r.status === "failed" ? " is-failed" : ""), "data-id": r.id }, box, el("div", { class: "run-main" }, name, meta), star,
    kebab(`Actions for ${r.name}`, (a, f) => openRunMenu(r, a, f)));
}
function groupStatus(g) {
  const ms = membersOf(g), ended = ms.filter(r => ENDED.has(r.status)).length, running = ms.filter(r => r.status === "running").length,
    waiting = ms.filter(r => r.status === "waiting").length, failed = ms.filter(r => r.status === "failed").length;
  const n = `${ms.length} run${ms.length === 1 ? "" : "s"}`;
  if (!ms.length) return { text: "No runs", busy: false };
  if (ended === ms.length) return { text: `${n} · Finished` + (failed ? ` · ${failed} stopped by the model` : ""), busy: false };
  return { text: `${n} · ${ended} finished` + (running ? ` · ${running} running` : "") + (waiting ? ` · ${waiting} waiting` : ""), busy: true };
}
function folderRow(g) {
  const ms = membersOf(g), tickable = ms.filter(r => hasData(r) || r.status === "failed"), shownN = ms.filter(r => state.shown.has(r.id)).length;
  const open = state.open.has(g.id), st = groupStatus(g);
  const box = el("input", { type: "checkbox", "aria-label": `Show all runs in ${g.name}`, disabled: !tickable.length || null,
    onchange: e => { for (const r of tickable) e.target.checked ? tick(r.id) : untick(r.id); saveView(); renderAll(); } });
  box.checked = tickable.length > 0 && shownN === tickable.length;
  box.indeterminate = shownN > 0 && !box.checked;
  const toggleOpen = () => { if (open) { state.open.delete(g.id); state.closed.add(g.id); } else { state.open.add(g.id); state.closed.delete(g.id); } renderRuns(); };
  const caret = el("button", { class: "caret", type: "button", "aria-expanded": String(open), "aria-label": open ? `Close ${g.name}` : `Open ${g.name}`, text: open ? "▾" : "▸", onclick: toggleOpen });
  const name = state.renaming === "g:" + g.id
    ? renameInput(g.name, v => { state.renaming = null; if (v && v !== g.name) act(`/api/experiments/${g.id}/rename`, { name: v }); else renderRuns(); })
    : el("button", { class: "folder-name", type: "button", "aria-expanded": String(open), text: g.name, onclick: toggleOpen });
  const head = el("div", { class: "folder-head" }, box, caret,
    el("div", { class: "run-main" }, name, el("div", { class: "run-meta" }, el("span", { class: st.busy ? "running" : "", text: st.text }))),
    kebab(`Actions for ${g.name}`, (a, f) => openFolderMenu(g, a, f)));
  return el("div", { class: "folder", "data-id": g.id }, head, open && ms.length ? el("div", { class: "folder-runs" }, ms.map(runRow)) : null);
}
function renderRuns() {
  const list = $("runs-list"), keep = list.scrollTop;
  list.replaceChildren(...(groups.length ? groups.map(folderRow) : [el("p", { class: "empty-col", text: "No runs yet. Select + New to start one." })]));
  list.scrollTop = keep;
  const ri = list.querySelector(".rename-input"); if (ri) { ri.focus(); ri.select(); }
}
// menus
const pop = $("pop");
function openPop(anchor, kids, focus) {
  pop.replaceChildren(...kids.filter(Boolean));
  pop.hidden = false;
  const b = anchor.getBoundingClientRect();
  pop.style.left = Math.max(8, Math.min(b.right - pop.offsetWidth, innerWidth - pop.offsetWidth - 8)) + "px";
  pop.style.top = (b.bottom + 4 + pop.offsetHeight > innerHeight ? Math.max(8, b.top - pop.offsetHeight - 4) : b.bottom + 4) + "px";
  if (focus) { const first = pop.querySelector("button:not([aria-disabled=true])"); if (first) first.focus({ preventScroll: true }); }
}
function closePop() { pop.hidden = true; pop.classList.remove("wide"); }
const mi = (label, fn, cls) => el("button", { class: "mi" + (cls ? " " + cls : ""), role: "menuitem", type: "button", text: label, onclick: e => { e.stopPropagation(); fn(); } });
function confirmInPop(anchor, question, yes, fn) {
  openPop(anchor, [el("p", { class: "q", text: question }), el("div", { class: "qa" },
    el("button", { class: "btn sm danger", type: "button", text: yes, onclick: () => { closePop(); fn(); } }),
    el("button", { class: "btn sm", type: "button", text: "Cancel", onclick: closePop }))], true);
}
const busy = r => r.status === "running" || r.status === "waiting";
function download(href) { const a = el("a", { href, download: "" }); document.body.append(a); a.click(); a.remove(); }
function openRunMenu(r, anchor, focus) {
  openPop(anchor, [
    mi("Rename", () => { closePop(); state.renaming = r.id; renderRuns(); }),
    mi("New run with these settings", () => { closePop(); openSetup(r, r.group); }),
    mi("New experiment from this run", () => { closePop(); openExpSetup(null, r); }),
    r.id === state.baseline || !hasData(r) ? null : mi("Set as baseline", () => { closePop(); setBaseline(r); }),
    hasData(r) ? mi("Download CSV", () => { closePop(); download(`/api/runs/${r.id}/csv`); }) : null,
    busy(r) ? mi("Stop run", () => { closePop(); act(`/api/runs/${r.id}/stop`); }) : null,
    el("hr"),
    busy(r) ? null : mi("Delete", () => confirmInPop(anchor, `Delete ${r.name}?`, "Delete run", () => act(`/api/runs/${r.id}/delete`, {}, () => { untick(r.id); toast(`Deleted ${r.name}`); })), "danger"),
  ], focus);
}
function openFolderMenu(g, anchor, focus) {
  const ms = membersOf(g), anyBusy = ms.some(busy);
  openPop(anchor, [
    mi("Open in Experiment tab", () => { closePop(); openFolderInTab(g); }),
    mi("Edit as table", () => { closePop(); openExpSetup(g); }),
    mi("Add a run", () => { closePop(); openSetup(byId(g.base) || ms.find(hasData) || null, g.id); }),
    mi("Rename", () => { closePop(); state.renaming = "g:" + g.id; renderRuns(); }),
    ms.some(hasData) ? mi("Download CSV (all runs)", () => { closePop(); download(`/api/experiments/${g.id}/csv`); }) : null,
    anyBusy ? mi("Stop all runs", () => { closePop(); act(`/api/experiments/${g.id}/stop`); }) : null,
    el("hr"),
    anyBusy ? null : mi("Delete", () => confirmInPop(anchor, `Delete ${g.name} and its ${ms.length} run${ms.length === 1 ? "" : "s"}?`, "Delete experiment",
      () => act(`/api/experiments/${g.id}/delete`, {}, () => { for (const r of ms) untick(r.id); store("exp:" + g.id, null); toast(`Deleted ${g.name}`); })), "danger"),
  ], focus);
}

// ================================================ line chart (from A)
// Year labels: every 5, 10 or 20 years, to suit the length of the run.
const yearStep = span => span <= 30 ? 5 : span <= 70 ? 10 : 20;
function lineChart(cfg) {
  const W = cfg.width || 400, H = cfg.height || 170, L = 44, R = 8, T = 8, B = 22;
  const svg = s("svg", { viewBox: `0 0 ${W} ${H}`, role: "img" });
  const all = cfg.series.flatMap(x => x.pts.map(p => p[1])).filter(v => v != null && isFinite(v) && (!cfg.log || v > 0));
  const years = cfg.series.flatMap(x => x.pts.map(p => p[0]));
  svg._setYear = () => {};
  if (!all.length) return svg;
  let lo = cfg.fixed ? cfg.fixed[0] : Math.min(...all), hi = cfg.fixed ? cfg.fixed[1] : Math.max(...all);
  if (cfg.zero) { lo = Math.min(lo, 0); hi = Math.max(hi, 0); }
  if (!cfg.log && !cfg.fixed) { const pad = (hi - lo) * 0.06 || Math.abs(hi) * 0.1 || 1; lo = (lo >= 0 && lo - pad < 0) ? 0 : lo - pad; hi += pad; }
  const x0 = Math.min(...years), x1 = Math.max(...years);
  const f = cfg.log ? Math.log10 : v => v;
  const flo = f(lo), fhi = f(hi) === f(lo) ? f(lo) + 1 : f(hi);
  const tx = x => L + (x - x0) / (x1 - x0 || 1) * (W - L - R);
  const ty = v => T + (1 - (f(v) - flo) / (fhi - flo)) * (H - T - B);
  let ticks = [];
  if (cfg.log) { for (let e = Math.floor(flo); e <= Math.ceil(fhi); e++) for (const m of [1, 2, 5]) { const v = m * 10 ** e; if (v >= lo * 0.999 && v <= hi * 1.001) ticks.push(v); } if (ticks.length > 6) ticks = ticks.filter(v => /^1/.test(String(v))); }
  else { const raw = (hi - lo) / 4, mag = 10 ** Math.floor(Math.log10(raw)), step = [1, 2, 2.5, 5, 10].map(m => m * mag).find(st => st >= raw);
    for (let v = Math.ceil(lo / step) * step; v <= hi + 1e-9; v += step) ticks.push(+v.toFixed(10)); }
  for (const v of ticks) {
    svg.append(s("line", { x1: L, x2: W - R, y1: ty(v), y2: ty(v), class: "gridline" }));
    const t = s("text", { x: L - 6, y: ty(v) + 3, "text-anchor": "end" }); t.textContent = cfg.unit === "pct" ? Math.round(v * 1000) / 10 + "%" : fmt(v, "num"); svg.append(t);
  }
  if (cfg.zero && lo < 0 && hi > 0) svg.append(s("line", { x1: L, x2: W - R, y1: ty(0), y2: ty(0), class: "axisline" }));
  const ys = yearStep(x1 - x0);
  for (let y = Math.ceil(x0 / ys) * ys; y <= x1; y += ys) { const t = s("text", { x: tx(y), y: H - 6, "text-anchor": "middle" }); t.textContent = y; svg.append(t); }
  svg.append(s("line", { x1: L, x2: W - R, y1: H - B, y2: H - B, class: "axisline" }));
  for (const ser of cfg.series) {
    let d = "", pen = false;
    for (const [x, v] of ser.pts) { if (v == null || !isFinite(v) || (cfg.log && v <= 0)) { pen = false; continue; } d += (pen ? "L" : "M") + tx(x).toFixed(1) + " " + ty(v).toFixed(1); pen = true; }
    svg.append(s("path", { d, class: "series", stroke: ser.colour, "stroke-dasharray": ser.dash || "", "stroke-width": ser.width || null, opacity: ser.opacity ?? null }));
  }
  const cursor = s("line", { y1: T, y2: H - B, class: "cursor", visibility: "hidden" });
  svg.append(cursor);
  const hit = s("rect", { x: L, y: T, width: W - L - R, height: H - T - B, fill: "transparent" });
  svg.append(hit);
  svg._setYear = y => { if (y == null || y < x0 || y > x1) { cursor.setAttribute("visibility", "hidden"); return; } cursor.setAttribute("x1", tx(y)); cursor.setAttribute("x2", tx(y)); cursor.setAttribute("visibility", "visible"); };
  hit.addEventListener("mousemove", e => { const b = svg.getBoundingClientRect(); const x = (e.clientX - b.left) / b.width * W; setHover(Math.round(x0 + (x - L) / (W - L - R) * (x1 - x0))); });
  hit.addEventListener("mouseleave", () => setHover(null));
  return svg;
}
const hoverables = [];
function setHover(y) { state.hover = y; for (const h of hoverables) h(y); }

// ================================================ figures from the catalogue
let FIGMETA = {};
const SOURCE = {};
function buildFigures() {
  FIGMETA = {};
  for (const f of CAT.core_figures || []) { FIGMETA[f.key] = { ...f, source: null }; }
  for (const m of [...CAT.core, ...CAT.optional]) for (const f of m.figures || []) if (!FIGMETA[f.key]) FIGMETA[f.key] = { ...f, source: m.name };
}
function figInfo(key) {
  const f = FIGMETA[key];
  const label = f ? (f.declared ? f.label : OTHER_NAMES[key] || f.label) : OTHER_NAMES[key] || human(key);
  let unit = "num", fixed = null, suffix = "";
  if (f && f.declared) {
    if (f.unit === "share") unit = "pct";
    else if (f.unit === "rate") { unit = "pct"; suffix = " a year"; }
    else if (f.unit === "index") fixed = [0, 1];
  } else if (PCT.has(key)) unit = "pct";
  return { key, title: label, unit, fixed, suffix, note: f && f.note ? f.note : "", source: f ? f.source : undefined };
}
const fromLink = src => src === null ? modLink(HUB, "From the ledger") : src ? modLink(src, `From ${modName(src)}`) : null;

// ================================================ charts tab (from A)
const ptsOf = (r, key) => r.rows.slice(0, r.step + 1).map(x => [x.year, x.v[key]]);
function shownRuns() { return runs.filter(r => hasData(r) && state.shown.has(r.id)); }
function chartCard(fig, removable) {
  const shown = shownRuns();
  const logBox = fig.log ? el("label", { class: "opts" }, (() => { const c = el("input", { type: "checkbox", onchange: e => { state.log[fig.key] = e.target.checked; renderCharts(); } }); c.checked = !!state.log[fig.key]; return c; })(), "Log scale") : null;
  const svg = lineChart({ series: shown.map(r => ({ colour: colourOf(r), pts: ptsOf(r, fig.key), width: shown.length > 6 ? 1.1 : null })), unit: fig.unit, log: fig.log && state.log[fig.key], fixed: fig.fixed, zero: fig.key === "inflation" });
  const read = el("div", { class: "readout" });
  const upd = y => {
    svg._setYear(y);
    const yr = y ?? Math.max(...shown.map(r => r.rows[r.step].year));
    const at = r => { const row = r.rows[yr - r.rows[0].year]; return row && r.rows.indexOf(row) <= r.step ? row.v[fig.key] : null; };
    const bits = [];
    for (const g of groups) {
      const rs = shown.filter(r => r.group === g.id); if (!rs.length) continue;
      if (rs.length > 3) { const vs = rs.map(at).filter(v => v != null); if (vs.length) bits.push(el("span", { text: `${g.name}: ${fmt(Math.min(...vs), fig.unit)} to ${fmt(Math.max(...vs), fig.unit)}` })); }
      else bits.push(...rs.map(r => el("span", {}, el("i", { class: "swatch", style: `background:${colourOf(r)}` }), fmt(at(r), fig.unit))));
    }
    read.replaceChildren(el("span", {}, el("b", { text: String(yr) })), ...bits);
  };
  hoverables.push(upd); upd(state.hover);
  const line = fig.line ? fig.line() : [fig.note ? fig.note.replace(/\.?$/, ".") + " " : "", fig.suffix ? `Per cent${fig.suffix}. ` : "", fromLink(fig.source)];
  return el("div", { class: "card chart" },
    el("div", { class: "card-head" }, el("h2", { text: fig.title }), removable ? el("button", { class: "link small", text: "Remove", onclick: () => { state.extra = state.extra.filter(k => k !== fig.key); store("extra", state.extra); renderCharts(); } }) : logBox),
    el("p", { class: "line" }, ...line.filter(Boolean)), svg, read);
}
function renderCharts() {
  hoverables.length = 0;
  const p = $("panel-charts");
  const head = el("p", { class: "view-line", text: "The ticked runs on each figure. Point at a chart to read one year on every chart." });
  if (noRuns()) { p.replaceChildren(emptyState("There are no runs yet.", true)); return; }
  if (!shownRuns().length) { p.replaceChildren(...[notices()].filter(Boolean), emptyState("Tick a run in the list to show it on the charts.")); return; }
  const extras = state.extra.map(figInfo);
  p.replaceChildren(...[notices()].filter(Boolean), head,
    el("div", { class: "chart-grid" }, FIGS.map(f => chartCard(f)), extras.map(f => chartCard(f, true))),
    el("div", { class: "add-chart" }, el("button", { class: "btn sm", type: "button", id: "add-chart", "aria-haspopup": "dialog", text: "+ Add a chart", onclick: e => { e.stopPropagation(); openFigurePicker(e.currentTarget); } })));
}
// The list of figures, grouped by where they come from.
function openFigurePicker(anchor) {
  const shown = shownRuns();
  const inData = new Set(shown.flatMap(r => { const keys = new Set(); for (const row of r.rows) for (const [k, v] of Object.entries(row.v)) if (v != null) keys.add(k); return [...keys]; }));
  const modsOn = new Set(shown.flatMap(r => r.modules));
  const used = new Set([...FIGS.map(f => f.key), ...state.extra]);
  const item = (key, src) => {
    const f = figInfo(key), taken = used.has(key);
    const can = !taken && inData.has(key);
    const why = taken ? "Shown" : can ? "" : src && !modsOn.has(src) ? `Switch on ${modName(src)} to see this` : "Not recorded each year";
    return el("div", { class: "fig-opt" + (can ? "" : " off") },
      el("button", { type: "button", class: "fig-pick", "aria-disabled": can ? null : "true",
        onclick: e => { e.stopPropagation(); if (!can) return; state.extra.push(key); store("extra", state.extra); closePop(); renderCharts(); } },
        el("span", { class: "fl", text: f.title }), why ? el("span", { class: "fw", text: why }) : null),
      src !== undefined ? fromLink(src) : null);
  };
  const sections = [];
  const coreKeys = (CAT.core_figures || []).map(f => f.key);
  sections.push(["Core figures", coreKeys.map(k => item(k, null))]);
  for (const m of [...CAT.core, ...CAT.optional]) if ((m.figures || []).length) sections.push([modName(m.name), m.figures.map(f => item(f.key, m.name))]);
  const known = new Set([...coreKeys, ...[...CAT.core, ...CAT.optional].flatMap(m => (m.figures || []).map(f => f.key))]);
  const other = [...inData].filter(k => !known.has(k) && !FIG[k]).sort();
  if (other.length) sections.push(["Other figures", other.map(k => item(k))]);
  pop.classList.add("wide");
  openPop(anchor, [el("p", { class: "q", text: "Add a chart. Figures you cannot add yet say why." }),
    el("div", { class: "fig-list" }, sections.map(([title, items]) => el("section", {}, el("h3", { class: "section-label", text: title }), items)))], true);
}
// Runs the model stopped, among the ticked runs.
function notices() {
  const bad = runs.filter(r => state.shown.has(r.id) && r.status === "failed");
  if (!bad.length) return null;
  return el("div", { class: "notice", role: "status" }, el("h2", { text: bad.length === 1 ? "A ticked run was stopped by the model" : `${bad.length} ticked runs were stopped by the model` }),
    el("ul", {}, bad.map(r => el("li", {}, el("b", { text: r.name }), r.errorYear ? `, in ${r.errorYear}: ` : ": ", r.message || "No message."))));
}
function renderLegend() {
  const shown = shownRuns();
  if (shown.length <= 4) { $("legend").replaceChildren(...shown.map(r => el("span", {}, el("i", { class: "swatch", style: `background:${colourOf(r)}` }), (r.id === state.baseline ? "★ " : "") + fullName(r)))); return; }
  $("legend").replaceChildren(...groups.map(g => { const rs = shown.filter(r => r.group === g.id); if (!rs.length) return null;
    return el("span", {}, el("span", { style: "display:inline-flex;gap:1px" }, rs.slice(0, 8).map(r => el("i", { style: `width:4px;height:10px;display:inline-block;background:${colourOf(r)}` }))), `${g.name} (${rs.length})`); }).filter(Boolean));
}
function runOptions(filter, selId) {
  return groups.map(g => { const ms = membersOf(g).filter(r => hasData(r) && filter(r));
    return ms.length ? el("optgroup", { label: g.name }, ms.map(r => el("option", { value: r.id, text: runLabel(r), selected: r.id === selId || null }))) : null; }).filter(Boolean);
}

// ================================================ compare tab (from A)
const CMP_FIGS = ["dk", "breadth", "depth", "unemployment", "capital_share", "price_level", "inflation", "resistance"];
function renderCompare() {
  hoverables.length = 0;
  const p = $("panel-compare");
  const shown = shownRuns();
  if (noRuns()) { p.replaceChildren(emptyState("There are no runs yet.", true)); return; }
  if (shown.length < 2) { p.replaceChildren(emptyState("Tick 2 or more runs to see their differences.")); return; }
  const ref = refOf(shown), cols = [ref, ...shown.filter(r => r !== ref)];
  const isBase = ref.id === state.baseline, base = byId(state.baseline);
  // settings that differ between any of the ticked runs
  const rows = [];
  const add = (label, get, mod) => { const vals = cols.map(get); if (vals.some(v => !same(v, vals[0]))) rows.push({ label, vals, mod }); };
  add("Firms", r => r.claims.toLocaleString("en-GB")); add("Years", r => r.years); add("Seed", r => r.seed);
  for (const k of [...new Set(cols.flatMap(r => r.optional))]) add(modName(k), r => r.optional.includes(k) ? "On" : "Off", k);
  const keys = new Map();
  for (const r of cols) for (const mid of Object.keys(r.settings || {})) for (const n of Object.keys(r.settings[mid])) keys.set(mid + "|" + n, [mid, n]);
  for (const [mid, n] of keys.values()) add(`${modName(mid)} › ${setLabel(n)}`, r => valueIn(r, mid, n), keyOf(mid));
  const labelCell = row => { if (!row.mod) return row.label; const [a, b] = row.label.split(" › "); return b ? [modLink(row.mod, a), " › " + b] : [modLink(row.mod, a)]; };
  const head = () => el("tr", {}, el("th", { text: "" }), cols.map((r, i) => el("th", { class: "colth" },
    el("button", { class: "colhead" + (i === 0 ? " ref" : ""), type: "button", "data-tip": i === 0 ? (isBase ? "The baseline" : "The reference run") : "Select to make this run the baseline",
      onclick: () => { if (r.id !== state.baseline) setBaseline(r); } },
      el("span", { class: "nm" }, el("i", { class: "swatch", style: `background:${colourOf(r)}` }), (r.id === state.baseline ? "★ " : "") + fullName(r)),
      el("span", { class: "sub", text: i === 0 ? (isBase ? "Baseline" : "Reference") : "Make baseline" })))));
  const wide = cols.length > 6 ? " wide" : "";
  const settingsTable = el("div", { class: "dwrap" }, el("table", { class: "tbl dtable" + wide },
    el("thead", {}, head()),
    el("tbody", {}, rows.length ? rows.map(row => el("tr", {}, el("th", { scope: "row" }, ...[].concat(labelCell(row))),
      row.vals.map((v, i) => el("td", { class: i > 0 && same(v, row.vals[0]) ? "muted" : null, text: String(v) }))))
      : el("tr", {}, el("td", { colspan: String(cols.length + 1), class: "muted", text: "No settings differ." })))));
  const year = Math.min(...cols.map(r => r.rows[r.step].year));
  const at = (r, k) => { const row = r.rows.find(x => x.year === year); return row ? row.v[k] : null; };
  const gap = (f, a, b) => {
    if (a == null || b == null) return "";
    if (f.unit === "pct") { const g = (b - a) * 100; return (g >= 0 ? "+" : "") + g.toFixed(1) + " points"; }
    if (f.key === "resistance") { const g = b - a; return (g >= 0 ? "+" : "") + g.toFixed(2); }
    const g = (b / a - 1) * 100; return (g >= 0 ? "+" : "") + g.toFixed(0) + "%";
  };
  const resultsTable = el("div", { class: "dwrap" }, el("table", { class: "tbl dtable" + wide },
    el("thead", {}, head()),
    el("tbody", {}, CMP_FIGS.map(k => { const f = FIG[k], a = at(ref, k);
      return el("tr", {}, el("th", { scope: "row", text: f.title }), cols.map((r, i) => { const v = at(r, k);
        return el("td", { class: "n" }, el("span", { text: fmt(v, f.unit) }), i > 0 ? el("span", { class: "gap", text: gap(f, a, v) }) : null); })); }))));
  const charts = ["dk", "unemployment", "capital_share", "price_level"].map(k => {
    const f = FIG[k];
    const svg = lineChart({ series: cols.map((r, i) => ({ colour: colourOf(r), pts: ptsOf(r, k), dash: i === 0 ? "4 3" : "", width: cols.length > 6 ? 1.1 : null })), unit: f.unit, log: f.log && state.log[k], height: 150 });
    const read = el("div", { class: "readout" });
    const upd = y => { svg._setYear(y); const yr = y ?? year; const v = r => { const row = r.rows.find(x => x.year === yr); return row ? row.v[k] : null; };
      const others = cols.slice(1).map(v).filter(x => x != null);
      read.replaceChildren(el("span", {}, el("b", { text: String(yr) })), el("span", { text: `${isBase ? "★" : "Reference"} ${fmt(v(ref), f.unit)}` }),
        ...(cols.length <= 4 ? cols.slice(1).map(r => el("span", {}, el("i", { class: "swatch", style: `background:${colourOf(r)}` }), fmt(v(r), f.unit)))
          : others.length ? [el("span", { text: `Others ${fmt(Math.min(...others), f.unit)} to ${fmt(Math.max(...others), f.unit)}` })] : [])); };
    hoverables.push(upd); upd(state.hover);
    return el("div", { class: "card chart" }, el("div", { class: "card-head" }, el("h2", { text: f.title })), svg, read);
  });
  p.replaceChildren(
    el("p", { class: "view-line", text: `Differences between the ${cols.length} ticked runs. Select a column heading to make that run the baseline.` }),
    ...(isBase ? [] : [el("p", { class: "ref-note", text: base ? `★ ${fullName(base)} is not ticked. ${fullName(ref)} is the reference.` : `${fullName(ref)} is the reference.` })]),
    el("h3", { class: "dh", text: `Settings that differ (${rows.length})` }), settingsTable,
    el("h3", { class: "dh", text: `Results in ${year}` }), resultsTable,
    el("div", { class: "dcharts" }, charts));
}

// ================================================ gain tab (from A)
const GAIN_ORDER = ["mergers", "greenfield", "sabotage", "stagflation", "cost cutting", "resistance", "labour", "public_debt", "turnover"];
const gcol = src => modColour(src);
const gainName = k => k === "turnover" ? SHORT.turnover : modName(k);
const gainLink = k => modLink(k === "turnover" ? HUB : k, gainName(k));
function renderGain() {
  hoverables.length = 0;
  const p = $("panel-gain");
  if (noRuns()) { p.replaceChildren(emptyState("There are no runs yet.", true)); return; }
  const shownG = shownRuns();
  if (!shownG.length) { p.replaceChildren(emptyState("Tick a run to see what each module added each year.")); return; }
  // The run shown: the chosen one while it is ticked, otherwise the first ticked run.
  const r = shownG.includes(byId(state.gainRun)) ? byId(state.gainRun) : shownG[0];
  state.gainRun = r.id;
  const rows = r.rows.slice(1, r.step + 1);
  const srcs = [...new Set(rows.flatMap(x => Object.keys(x.gain)))].sort((a, b) => (GAIN_ORDER.indexOf(a) + 99 * (GAIN_ORDER.indexOf(a) < 0)) - (GAIN_ORDER.indexOf(b) + 99 * (GAIN_ORDER.indexOf(b) < 0)));
  const W = 820, H = 300, L = 44, R = 8, T = 10, B = 24;
  let maxUp = 0, maxDn = 0;
  for (const x of rows) { let u = 0, d = 0; for (const v of Object.values(x.gain)) v > 0 ? u += v : d += v; maxUp = Math.max(maxUp, u); maxDn = Math.min(maxDn, d); }
  const span = Math.max(maxUp, -maxDn, 0.05), lo = -span, hi = span;
  const ty = v => T + (hi - v) / (hi - lo) * (H - T - B);
  const bw = (W - L - R) / rows.length;
  const svg = s("svg", { viewBox: `0 0 ${W} ${H}`, role: "img" });
  for (const v of [lo, lo / 2, 0, hi / 2, hi]) { svg.append(s("line", { x1: L, x2: W - R, y1: ty(v), y2: ty(v), class: v === 0 ? "axisline" : "gridline" })); const t = s("text", { x: L - 6, y: ty(v) + 3, "text-anchor": "end" }); t.textContent = (v > 0 ? "+" : "") + v.toFixed(2); svg.append(t); }
  rows.forEach((x, i) => {
    let up = 0, dn = 0;
    for (const src of srcs) { const v = x.gain[src]; if (!v) continue;
      const y0 = v > 0 ? up : dn, y1 = y0 + v; v > 0 ? up = y1 : dn = y1;
      svg.append(s("rect", { x: L + i * bw + 0.5, width: Math.max(bw - 1, 1), y: ty(Math.max(y0, y1)), height: Math.abs(ty(y0) - ty(y1)), fill: gcol(src) })); }
    if (x.year % yearStep(rows.length) === 0) { const t = s("text", { x: L + i * bw + bw / 2, y: H - 6, "text-anchor": "middle" }); t.textContent = x.year; svg.append(t); }
  });
  const cursor = s("rect", { y: T, height: H - T - B, width: bw, fill: "currentColor", opacity: 0.08, visibility: "hidden" });
  svg.append(cursor);
  const hit = s("rect", { x: L, y: T, width: W - L - R, height: H - T - B, fill: "transparent" }); svg.append(hit);
  const read = el("div", { class: "readout" });
  const upd = y => {
    const i = y == null ? -1 : rows.findIndex(x => x.year === y);
    if (i < 0) { cursor.setAttribute("visibility", "hidden"); read.replaceChildren(el("span", { text: "Point at a year to see its sources." })); return; }
    cursor.setAttribute("x", L + i * bw); cursor.setAttribute("visibility", "visible");
    const g = rows[i].gain;
    read.replaceChildren(el("span", {}, el("b", { text: String(rows[i].year) })), ...srcs.filter(k => g[k]).map(k => el("span", {}, el("i", { class: "swatch", style: `background:${gcol(k)};height:8px;width:8px` }), `${gainName(k)} ${g[k] > 0 ? "+" : ""}${g[k].toFixed(3)}`)));
  };
  hit.addEventListener("mousemove", e => { const b = svg.getBoundingClientRect(); const xx = (e.clientX - b.left) / b.width * W; const i = Math.floor((xx - L) / bw); if (rows[i]) setHover(rows[i].year); });
  hit.addEventListener("mouseleave", () => setHover(null));
  hoverables.push(upd); upd(state.hover);
  const tot = srcs.map(k => [k, rows.reduce((a, x) => a + (x.gain[k] || 0), 0)]).sort((a, b) => b[1] - a[1]);
  const tmax = Math.max(...tot.map(t => Math.abs(t[1])), 0.01);
  const total = tot.reduce((a, t) => a + t[1], 0);
  p.replaceChildren(
    el("p", { class: "view-line" }, "Change in ", term("dk", "differential capitalization"), " each year, split by the module that caused it. Select a module to open it on the map."),
    el("div", { class: "gain-head" }, el("h2", { id: "gain-title" }, el("i", { class: "swatch", style: `background:${colourOf(r)}` }), fullName(r)),
      el("p", { class: "run-meta", text: `${r.claims.toLocaleString("en-GB")} firms · ${r.years} years · seed ${r.seed}` })),
    el("div", { class: "gain-cols" },
      el("div", { class: "card chart" }, el("div", { class: "card-head" }, el("h2", {}, term("gain", "Gain"), " each year")), svg, read,
        el("div", { class: "gain-legend" }, srcs.map(k => el("span", {}, el("i", { style: `background:${gcol(k)}` }), gainLink(k))))),
      el("div", { class: "card" }, el("div", { class: "card-head" }, el("h2", { text: `Over the run, ${rows[0].year} to ${rows[rows.length - 1].year}` })),
        el("p", { class: "line", text: `Total change: ${total >= 0 ? "+" : ""}${total.toFixed(2)} on a log scale.` }),
        tot.map(([k, v]) => el("div", { class: "bar-row" }, el("span", {}, gainLink(k)),
          el("div", { class: "bar-track" }, el("div", { class: "zero" }), el("div", { class: "bar", style: `background:${gcol(k)};${v >= 0 ? `left:50%;width:${v / tmax * 50}%` : `right:50%;width:${-v / tmax * 50}%`}` })),
          el("span", { style: "text-align:right", text: (v >= 0 ? "+" : "") + v.toFixed(2) }))))),
    ...(shownG.length > 1 ? [gainRunList(shownG, r)] : []));
}
// The ticked runs as a radio group. Selecting a row shows that run.
function gainRunList(shownG, cur) {
  const totalOf = x => x.rows.slice(1, x.step + 1).reduce((a, row) => a + Object.values(row.gain).reduce((b, v) => b + v, 0), 0);
  const pick = x => { state.gainRun = x.id; renderGain(); const n = document.querySelector(`.gain-run[data-id="${x.id}"]`); if (n) n.focus(); };
  const items = shownG.map(x => {
    const on = x === cur, tot = totalOf(x), g = gById(x.group);
    return el("div", { class: "gain-run" + (on ? " on" : ""), role: "radio", "aria-checked": String(on), tabindex: on ? "0" : "-1", "data-id": x.id,
      onclick: () => pick(x),
      onkeydown: e => {
        const i = shownG.indexOf(x);
        if (e.key === "ArrowDown" || e.key === "ArrowRight") { e.preventDefault(); pick(shownG[(i + 1) % shownG.length]); }
        else if (e.key === "ArrowUp" || e.key === "ArrowLeft") { e.preventDefault(); pick(shownG[(i - 1 + shownG.length) % shownG.length]); }
        else if (e.key === "Home") { e.preventDefault(); pick(shownG[0]); }
        else if (e.key === "End") { e.preventDefault(); pick(shownG[shownG.length - 1]); }
        else if (e.key === " " || e.key === "Enter") { e.preventDefault(); pick(x); }
      } },
      el("i", { class: "swatch", style: `background:${colourOf(x)}` }), el("span", { class: "nm", text: fullName(x) }), el("span", { class: "fd", text: g ? g.name : "" }),
      el("span", { class: "tot", text: (tot >= 0 ? "+" : "") + tot.toFixed(2) }));
  });
  return el("section", { class: "gain-runs" }, el("h3", { class: "section-label", id: "gain-runs-h", text: `Ticked runs (${shownG.length})` }),
    el("div", { class: "gain-run gain-run-head", "aria-hidden": "true" }, el("span"), el("span", { text: "Run" }), el("span", { text: "Experiment" }), el("span", { class: "tot", text: "Gain over the run" })),
    el("div", { role: "radiogroup", "aria-labelledby": "gain-runs-h" }, items));
}

// ================================================ map tab (from E)
const FIGNAME = { unemployment: "Unemployment", concentration: "Top 100's share of employees", industry_growth: "Growth of each industry",
  hire_small: "Hiring rate of small firms", hire_dominant: "Hiring rate of the top 100", entry_open: "Room for new firms",
  new_hires: "New hires", merger_volume: "Merger volume", hiring_drag: "Cut in hiring caused by mergers", pool_open: "Firms the top 100 can still buy",
  stagflation_intensity: "Intensity of stagflation", cohesion: "Cohesion of the top 100", crisis: "Crisis level", inflation_push: "Price rise pushed by the top 100",
  resistance: "Resistance", roadblocks: "Roadblocks against mergers", pressure: "Pressure on boundaries", government_debt: "Government debt",
  interest_share: "Interest share", corporate_debt: "Corporate debt", government_debt_dominant: "Government debt held by the top 100" };
const figName = k => FIGMETA[k] ? figInfo(k).title : FIGNAME[k] || human(k);
const MS = state.map;
const mapRun = () => { const shown = shownRuns(); if (!shown.length) return null; const r = byId(MS.run); return shown.includes(r) ? r : refOf(shown); };
const mapVs = () => { const A = mapRun(), B = MS.vs ? byId(MS.vs) : null; return A && B && B !== A && shownRuns().includes(B) ? B : null; };
const NOMARKS = { changed: new Map(), added: new Set(), removed: new Set() };
const hasGain = (run, name) => name === HUB || run.rows.some(r => (name in r.gain));
function gainSeries(run, name) { return run.rows.map(r => r.gain[name === HUB ? "turnover" : name] ?? (r.year === run.rows[0].year ? null : 0)); }
function gainTotal(run, name) { return run.rows.reduce((a, r) => a + (r.gain[name === HUB ? "turnover" : name] || 0), 0); }
function gainIn(run, name, year) { const r = run.rows.find(x => x.year === year); return r ? (r.gain[name === HUB ? "turnover" : name] || 0) : 0; }
const inRun = (run, name) => name === HUB || run.modules.includes(name);
const POS = {
  greenfield: [170, 120], sabotage: [390, 120], compass: [610, 120], mergers: [830, 120],
  debt: [170, 320], [HUB]: [390, 320], stagflation: [610, 320], envelope: [830, 320],
  resistance: [390, 520], "cost cutting": [610, 520],
};
const SLOTS = [[170, 520], [830, 520], [55, 220], [945, 220], [55, 420], [945, 420], [280, 220], [500, 220], [720, 220],
  [280, 420], [500, 420], [720, 420], [55, 600], [945, 600], [280, 605], [500, 605], [720, 605], [55, 40], [945, 40],
  [280, 30], [500, 30], [720, 30], [170, 600], [830, 600], [170, 30], [830, 30], [390, 605], [610, 605], [390, 30], [610, 30]];
// Changes in the set-up screen that have not run yet, as the map shows them.
function draftMarks() {
  const out = { changed: new Map(), added: new Set(), removed: new Set() };
  if (!form || form.kind !== "run") return out;
  for (const d of draftDiffs()) if (d.mod) {
    if (d.optional === "added") out.added.add(d.mod); else if (d.optional === "removed") out.removed.add(d.mod);
    else out.changed.set(d.mod, (out.changed.get(d.mod) || 0) + 1);
  }
  return out;
}
function activeNames(run, marks) {
  const names = new Set((run ? run.modules : CORE_ORDER).filter(n => MODS[n]));
  for (const n of marks.added) names.add(n);
  for (const n of [...names]) if (!marks.removed.has(n)) for (const r of (MODS[n] && MODS[n].replaces) || []) names.delete(r);
  return names;
}
function sharesWith(a, b) { if (!a || !b) return false; return (a.supplies || []).some(f => (b.reads || []).includes(f)) || (b.supplies || []).some(f => (a.reads || []).includes(f)); }
function hubMod(names) {
  const supplied = new Set([...names].flatMap(n => MODS[n].supplies || []));
  const fromLedger = [...new Set([...names].flatMap(n => MODS[n].reads || []))].filter(f => !supplied.has(f)).sort();
  return { name: HUB, title: "Ledger", supplies: fromLedger, reads: [] };
}
function layout(names) {
  const pos = { [HUB]: POS[HUB] };
  for (const n of names) if (POS[n]) pos[n] = POS[n];
  for (const n of names) for (const r of (MODS[n] && MODS[n].replaces) || []) if (POS[r] && !names.has(r)) pos[n] = POS[r];
  const free = SLOTS.filter(sl => !Object.values(pos).some(p => Math.hypot(p[0] - sl[0], p[1] - sl[1]) < 40));
  for (const n of [...names].filter(x => !pos[x])) {
    const m = MODS[n];
    const linked = Object.keys(pos).filter(o => o !== n && sharesWith(m, MODS[o] || hubMod(names)));
    const cx = linked.length ? linked.reduce((a, o) => a + pos[o][0], 0) / linked.length : 500;
    const cy = linked.length ? linked.reduce((a, o) => a + pos[o][1], 0) / linked.length : 320;
    free.sort((a, b) => Math.hypot(a[0] - cx, a[1] - cy) - Math.hypot(b[0] - cx, b[1] - cy));
    pos[n] = free.shift() || [500, 320];
  }
  return pos;
}
function edgesFor(names) {
  const hub = hubMod(names);
  const nodes = [...names].map(n => MODS[n]).concat([hub]);
  const out = [];
  for (const a of nodes) for (const b of nodes) {
    if (a === b) continue;
    const figs = (a.supplies || []).filter(f => (b.reads || []).includes(f));
    if (figs.length) out.push({ from: a.name, to: b.name, figs, core: a.name === HUB });
  }
  return out;
}
function measureOf(name, ctx) {
  const A = ctx.run, B = ctx.vs;
  if (!A || !inRun(A, name)) return null;
  if (ctx.measure === "year") return gainIn(A, name, ctx.year);
  if (ctx.measure === "diff" && B) return inRun(B, name) ? gainTotal(A, name) - gainTotal(B, name) : gainTotal(A, name);
  return gainTotal(A, name);
}
function mix(c1, c2, t) {
  const p = c => { const x = c.replace("#", ""); return [0, 2, 4].map(i => parseInt(x.slice(i, i + 2), 16)); };
  const a = p(c1), b = p(c2);
  return "#" + a.map((x, i) => Math.round(x + (b[i] - x) * t).toString(16).padStart(2, "0")).join("");
}
function colourFor(v, max) {
  if (v == null || v === 0) return css("--zero");
  const t = Math.min(1, Math.abs(v) / (max || 1));
  return mix(css("--zero"), v >= 0 ? css("--pos") : css("--neg"), 0.25 + 0.75 * Math.sqrt(t));
}
function drawMap(ctx) {
  const marks = ctx.marks, names = activeNames(ctx.run, marks);
  for (const n of marks.removed) names.add(n);
  const pos = layout(names), edges = edgesFor(new Set([...names].filter(n => !marks.removed.has(n))));
  const all = [...names, HUB];
  const vals = Object.fromEntries(all.map(n => [n, measureOf(n, ctx)]));
  const max = Math.max(0.01, ...all.filter(n => n !== HUB).map(n => Math.abs(vals[n] || 0)));
  const E = ctx.E, N = ctx.N, P = ctx.prefix, sel = ctx.sel;
  E.replaceChildren(); N.replaceChildren();
  const radius = n => n === HUB ? 30 : (vals[n] == null ? 22 : 20 + 22 * Math.sqrt(Math.abs(vals[n]) / max));
  for (const e of edges) {
    const [x1, y1] = pos[e.from], [x2, y2] = pos[e.to];
    const back = edges.some(o => o.from === e.to && o.to === e.from);
    const dx = x2 - x1, dy = y2 - y1, len = Math.hypot(dx, dy) || 1, bend = back ? 26 : 10;
    const mx = (x1 + x2) / 2 - dy / len * bend, my = (y1 + y2) / 2 + dx / len * bend;
    const r1 = radius(e.from) + 4, r2 = radius(e.to) + 7;
    const a1 = Math.atan2(my - y1, mx - x1), a2 = Math.atan2(my - y2, mx - x2);
    const d = `M${(x1 + Math.cos(a1) * r1).toFixed(1)},${(y1 + Math.sin(a1) * r1).toFixed(1)} Q${mx.toFixed(1)},${my.toFixed(1)} ${(x2 + Math.cos(a2) * r2).toFixed(1)},${(y2 + Math.sin(a2) * r2).toFixed(1)}`;
    const touches = sel && (e.from === sel || e.to === sel);
    const hi = !!(ctx.hiFig && e.figs.includes(ctx.hiFig) && touches);
    E.append(s("path", { d, class: "edge" + (e.core ? " core" : "") + (hi ? " hi" : "") + (sel && !touches ? " dim" : ""), "marker-end": hi ? `url(#${P}arr-hi)` : e.core ? `url(#${P}arr-core)` : `url(#${P}arr)` }));
    const hit = s("path", { d, class: "edge-hit" });
    hit.dataset.tip = `${modName(e.from)} → ${modName(e.to)}: ${e.figs.map(figName).join(", ")}`;
    E.append(hit);
  }
  const linked = sel ? new Set(edges.filter(e => e.from === sel || e.to === sel).flatMap(e => [e.from, e.to])) : null;
  const A0 = ctx.run, B0 = ctx.vs;
  for (const n of all) {
    const [x, y] = pos[n];
    const m = n === HUB ? null : MODS[n];
    const added = marks.added.has(n), removed = marks.removed.has(n), changed = marks.changed.get(n);
    const blank = !A0;
    const off = n !== HUB && vals[n] == null && !added && !blank;
    const cls = "node" + (n === HUB ? " hub" : "") + (off ? " off" : "") + (added ? " added" : "") + (removed ? " removed" : "") + (blank && n !== HUB ? " blank" : "") + (changed ? " changed" : "") + (sel === n ? " sel" : "") + (linked && !linked.has(n) && sel !== n ? " dim" : "");
    const g = s("g", { class: cls, transform: `translate(${x},${y})`, tabindex: 0, role: "button", "aria-label": modName(n) });
    const r = radius(n);
    g.append(s("circle", { class: "ring", r: r + 5, fill: "none" }));
    if (changed) g.append(s("circle", { class: "mark", r: r + 9 }));
    const c = s("circle", { class: "body", r }); c.style.fill = n === HUB ? "" : colourFor(vals[n], max); g.append(c);
    if (n === HUB) { const t = s("text", { class: "inner", y: 4 }); t.textContent = "Ledger"; g.append(t); }
    else if (!m.core) { const t = s("text", { class: "inner", y: 4 }); t.textContent = "+"; if (off || added || removed) t.style.fill = css("--muted"); g.append(t); }
    const lbl = s("text", { class: "lbl", y: r + 17 }); lbl.textContent = n === HUB ? "" : modName(n); g.append(lbl);
    const val = s("text", { class: "val" + (added || removed || changed ? " draft" : ""), y: n === HUB ? r + 16 : r + 32 });
    val.textContent = n === HUB ? "" : added ? "Added, not run yet" : removed ? "Removed, not run yet"
      : blank ? (changed ? `${changed} changed` : "") : off ? "Not in this run" : !hasGain(A0, n) ? (changed ? `No direct gain · ${changed} changed` : "No direct gain")
      : signed(vals[n]) + (changed ? ` · ${changed} changed` : "") + (ctx.measure === "diff" && B0 && !inRun(B0, n) ? " (only in this run)" : "");
    g.append(val);
    g.dataset.tip = n === HUB ? "Figures the ledger works out each year, such as unemployment. Modules read them." : (ctx.tipSuffix ? (LINE[n] || m.title) + " " + ctx.tipSuffix : LINE[n] || m.title);
    g.addEventListener("click", () => ctx.onSelect(n));
    g.addEventListener("keydown", ev => { if (ev.key === "Enter" || ev.key === " ") { ev.preventDefault(); ctx.onSelect(n); } });
    N.append(g);
  }
  if (!A0) {
    const anyM = marks.added.size || marks.removed.size || marks.changed.size;
    ctx.legend.replaceChildren(...[el("span", { text: ctx.blankLine }), ctx.blankStart ? startBtn() : null,
      anyM ? el("div", { class: "keys" }, el("span", {}, dot(css("--surface"), css("--accent"), "4 2"), " Not run yet")) : null].filter(Boolean));
    return;
  }
  const what = ctx.measure === "year" ? `Gain in ${ctx.year}` : ctx.measure === "diff" && B0 ? `Gain in ${fullName(A0)} minus gain in ${fullName(B0)}` : `Gain over the run in ${fullName(A0)}`;
  const bar = el("div", { class: "bar", style: `background:linear-gradient(90deg, ${css("--neg")}, ${css("--zero")}, ${css("--pos")})` });
  const ln = dash => { const v = s("svg", { width: 26, height: 10 }); v.append(s("line", { x1: 0, y1: 5, x2: 26, y2: 5, stroke: css("--edge"), "stroke-width": 1.6, "stroke-dasharray": dash })); return v; };
  const anyMarks = marks.added.size || marks.removed.size || marks.changed.size;
  ctx.legend.replaceChildren(
    el("span", {}, el("b", { text: what }), ". Size and colour show the ", term("gain", "gain"), "."),
    el("span", { class: "scale" }, el("span", { text: signed(-max) }), bar, el("span", { text: signed(max) })),
    el("div", { class: "keys" },
      anyMarks ? el("span", {}, dot(css("--surface"), css("--accent"), "4 2"), " Not run yet") : el("span", {}, dot(css("--surface"), css("--border-strong"), "3 2"), " Not in this run"),
      el("span", {}, ln(""), " From a module"),
      el("span", {}, ln("3 4"), " From the ", term("ledger", "ledger"))));
}
function dot(fill, stroke, dash) { const v = s("svg", { width: 16, height: 16 }); v.append(s("circle", { cx: 8, cy: 8, r: 6, fill, stroke, "stroke-dasharray": dash, "stroke-width": 1.5 })); return v; }
function mainCtx() {
  return { E: $("mp-edges"), N: $("mp-nodes"), legend: $("mp-legend"), run: mapRun(), vs: mapVs(), measure: MS.measure, year: MS.year,
    sel: MS.sel, hiFig: MS.hiFig, marks: NOMARKS, prefix: "", onSelect: selectNode,
    blankLine: noRuns() ? "Start a run to colour the modules by their gain." : "Tick a run to colour the modules by their gain.", blankStart: noRuns() };
}
function drawMainMap() { drawMap(mainCtx()); }
function spark(series, w, h, opts = {}) {
  const v = s("svg", { viewBox: `0 0 ${w} ${h}`, preserveAspectRatio: "none" });
  const all = series.flatMap(x => x.values).filter(x => x != null && isFinite(x));
  if (!all.length) return v;
  let lo = Math.min(...all), hi = Math.max(...all);
  if (opts.zero) { lo = Math.min(lo, 0); hi = Math.max(hi, 0); }
  if (hi === lo) { hi += 1; lo -= 1; }
  const n = Math.max(...series.map(x => x.values.length));
  const X = i => i / (n - 1) * w, Y = y => h - 2 - (y - lo) / (hi - lo) * (h - 4);
  if (opts.zero) v.append(s("line", { x1: 0, x2: w, y1: Y(0), y2: Y(0), stroke: css("--axis"), "stroke-width": 1, "vector-effect": "non-scaling-stroke" }));
  for (const x of series) {
    let d = "", pen = false;
    x.values.forEach((y, i) => { if (y == null || !isFinite(y)) { pen = false; return; } d += (pen ? "L" : "M") + X(i).toFixed(1) + " " + Y(y).toFixed(1); pen = true; });
    v.append(s("path", { d, fill: "none", stroke: x.colour, "stroke-width": 1.6, "stroke-dasharray": x.dash, "vector-effect": "non-scaling-stroke" }));
  }
  if (opts.cursor != null) v.append(s("line", { x1: X(opts.cursor), x2: X(opts.cursor), y1: 0, y2: h, class: "cursor-line", "vector-effect": "non-scaling-stroke" }));
  return v;
}
function mpChip(f, where) {
  return el("button", { class: "mp-chip" + (MS.hiFig === f ? " on" : ""), type: "button", "data-tip": figName(f) + ", " + where, text: figName(f),
    onclick: () => { MS.hiFig = MS.hiFig === f ? null : f; drawMainMap(); drawInspector(); } });
}
function drawInspector() {
  const box = $("mp-insp"), n = MS.sel;
  if (!mapRun()) { box.replaceChildren(el("p", { class: "empty-insp", text: noRuns() ? "Start a run to see each module's gain and settings." : "Tick a run to see each module's gain and settings." })); return; }
  if (!n) { box.replaceChildren(el("p", { class: "empty-insp", text: "Select a module to see its gain, the figures it reads and supplies, and its settings." })); return; }
  const A = mapRun(), B = mapVs();
  const names = activeNames(A, NOMARKS);
  if (n === HUB) {
    const hub = hubMod(names);
    const readers = f => [...names].filter(x => (MODS[x].reads || []).includes(f));
    box.replaceChildren(el("h2", { text: "Ledger" }), el("p", { class: "kind", text: "Part of the model, not a module" }),
      el("p", { class: "sum", text: "The ledger holds every firm and works out some figures itself each year. Modules read them." }),
      el("h3", { text: "Figures it supplies" }), el("div", { class: "mp-chips" }, ...hub.supplies.map(f => mpChip(f, "to " + readers(f).map(modName).join(", ")))),
      el("h3", { text: "Changes in the top 100" }),
      el("p", { class: "sum", text: `Gain from firms entering and leaving the top 100, over the run: ${signed(gainTotal(A, HUB), 3)}.` }));
    return;
  }
  const m = MODS[n], marks = NOMARKS;
  const inA = inRun(A, n), inB = B ? inRun(B, n) : false;
  const kids = [];
  if (m.image) {
    const pic = el("picture", {}, m.image_dark ? el("source", { srcset: m.image_dark, media: "(prefers-color-scheme: dark)" }) : null, el("img", { src: m.image, alt: "" }));
    const wrap = el("div", { class: "pic" }, pic); pic.querySelector("img").addEventListener("error", () => wrap.remove()); kids.push(wrap);
  }
  const kind = m.core ? "Main module. Always runs." : (m.replaces && m.replaces.length ? `Optional. Runs in place of ${m.replaces.map(r => modName(r).toLowerCase()).join(", ")}.` : "Optional module");
  kids.push(el("h2", { text: modName(n) }), el("p", { class: "kind", text: kind }), el("p", { class: "sum", text: LINE[n] || "" }));
  if (marks.added.has(n)) kids.push(el("p", { class: "replaced-note", text: "Added in your set-up. Not run yet." }));
  if (marks.removed.has(n)) kids.push(el("p", { class: "replaced-note", text: "Removed in your set-up. Not run yet." }));
  kids.push(el("h3", {}, term("gain", "Gain")));
  if (!inA) kids.push(el("p", { class: "none", text: `Not in ${fullName(A)}.` }));
  else if (!hasGain(A, n)) kids.push(el("p", { class: "none", text: "It changes no firm's earnings directly. It acts through the figures it supplies." }));
  else {
    const yearIdx = A.rows.findIndex(r => r.year === MS.year);
    kids.push(el("div", { class: "stat" },
      el("div", {}, el("b", { text: signed(gainTotal(A, n)) }), el("br"), el("span", { text: B ? runLabel(A) : "Over the run" })),
      el("div", {}, el("b", { text: signed(gainIn(A, n, MS.year), 3) }), el("br"), el("span", { text: "In " + MS.year })),
      B ? el("div", {}, el("b", { text: inB ? signed(gainTotal(B, n)) : "–" }), el("br"), el("span", { text: runLabel(B) })) : null));
    const ser = [{ values: gainSeries(A, n), colour: css("--s1") }];
    if (B && inB) ser.push({ values: gainSeries(B, n), colour: css("--s2"), dash: "4 3" });
    const sp = spark(ser, 300, 60, { zero: true, cursor: MS.measure === "year" ? yearIdx : null });
    sp.style.width = "100%"; sp.style.height = "60px"; sp.style.marginTop = "8px";
    kids.push(sp, el("div", { style: "display:flex;justify-content:space-between;color:var(--muted);font-size:12px" }, el("span", { text: String(A.rows[0].year) }), el("span", { text: "Gain each year" }), el("span", { text: String(A.rows[A.step].year) })));
  }
  const readers = f => [...names].filter(x => x !== n && (MODS[x].reads || []).includes(f));
  const suppliers = f => { const x = [...names].filter(y => y !== n && (MODS[y].supplies || []).includes(f)); return x.length ? x : [HUB]; };
  kids.push(el("h3", { text: "Reads" }),
    (m.reads || []).length ? el("div", { class: "mp-chips" }, ...m.reads.map(f => mpChip(f, "from " + suppliers(f).map(x => x === HUB ? "the ledger" : modName(x)).join(", ")))) : el("p", { class: "none", text: "No figures from other modules." }),
    el("h3", { text: "Supplies" }),
    (m.supplies || []).length ? el("div", { class: "mp-chips" }, ...m.supplies.slice(0, 14).map(f => { const r = readers(f); return mpChip(f, r.length ? "to " + r.map(modName).join(", ") : "not read by a module on the map"); })) : el("p", { class: "none", text: "No figures. It changes firms' earnings directly." }));
  // Settings: edits go into the set-up draft.
  const mid = midOf(n);
  const spec = A;
  kids.push(el("h3", { text: `Settings (${m.settings.length})` }), el("p", { class: "none", style: "margin-bottom:6px", text: "Change a value to set up a new run with it." }));
  for (const st of m.settings) {
    const id = "mi-" + n.replace(/\W/g, "") + "-" + st.name;
    const v = valueIn(spec, mid, st.name), baseV = valueIn(A, mid, st.name);
    const input = el("input", { type: "text", id, value: Array.isArray(v) ? v.join(", ") : String(v ?? ""), inputmode: "decimal", class: same(v, baseV) ? null : "changed" });
    input.addEventListener("change", () => {
      const t = input.value.trim(), num = Number(t);
      openSetup(A, A.group); setDraft(mid, st.name, t !== "" && isFinite(num) ? num : t); renderSetup();
    });
    const note = st.note ? firmify(st.note.charAt(0).toUpperCase() + st.note.slice(1)) + "." : "";
    kids.push(el("div", { class: "mp-set" }, el("label", { for: id, text: setLabel(st.name) }), input,
      el("span", { class: "n", text: (note ? note + " " : "") + `Default ${Array.isArray(st.default) ? st.default.join(", ") : st.default}.` })));
  }
  box.replaceChildren(...kids);
}
const STRIP = ["dk", "breadth", "depth", "unemployment", "capital_share", "price_level", "inflation", "resistance"];
function drawStrip() {
  const A = mapRun(), B = mapVs();
  $("mp-strip").replaceChildren(...STRIP.map(k => {
    const F = FIG[k];
    if (!A) return el("div", { class: "tile off" }, el("span", { class: "name", text: F.title }), el("span", { class: "num", text: "–" }));
    const a = A.rows.map(r => r.v[k]), last = a[a.length - 1];
    const ser = [{ values: a, colour: css("--s1") }];
    let sub = null;
    if (B) { const b = B.rows.map(r => r.v[k]); ser.push({ values: b, colour: css("--s2"), dash: "3 3" }); sub = el("small", { text: "vs " + fmt(b[b.length - 1], F.unit) }); }
    return el("button", { class: "tile" + (MS.fig === k ? " on" : ""), type: "button", "data-tip": F.short, onclick: () => { MS.fig = MS.fig === k ? null : k; drawStrip(); drawDrawer(); } },
      el("span", { class: "name", text: F.title }), el("span", { class: "num" }, fmt(last, F.unit), sub), spark(ser, 160, 30));
  }));
}
function drawDrawer() {
  const d = $("mp-drawer");
  if (!MS.fig || !mapRun()) { d.hidden = true; return; }
  const F = FIG[MS.fig], A = mapRun(), B = mapVs();
  d.hidden = false;
  const svg = lineChart({ series: [{ colour: css("--s1"), pts: ptsOf(A, F.key) }].concat(B ? [{ colour: css("--s2"), pts: ptsOf(B, F.key), dash: "5 4" }] : []), unit: F.unit, log: F.log && state.log[F.key], fixed: F.fixed, width: 1000, height: 250 });
  d.replaceChildren(el("header", {}, el("h2", { text: F.title }), el("span", { class: "dline", text: F.short }),
    el("button", { class: "btn sm", type: "button", text: "Close", onclick: () => { MS.fig = null; drawStrip(); drawDrawer(); } })), svg);
}
function syncMapTop() {
  const A = mapRun(), B = mapVs();
  const ticked = r => state.shown.has(r.id);
  $("mp-run").replaceChildren(...(A ? runOptions(ticked, A.id) : [el("option", { text: "No run ticked" })]));
  $("mp-run").disabled = !A; $("mp-run").previousElementSibling.hidden = !A;
  const others = A ? runOptions(r => ticked(r) && r.id !== A.id, B && B.id) : [];
  $("mp-vs").replaceChildren(el("option", { value: "", text: others.length ? "No comparison" : "Tick another run to compare" }), ...others);
  $("mp-vs").disabled = !others.length;
  $("mp-measure").disabled = !A;
  if (!B && MS.measure === "diff") MS.measure = "run";
  $("mp-measure").value = MS.measure;
  $("mp-measure").querySelector('option[value="diff"]').disabled = !B;
  $("mp-vs-ln").hidden = !B;
  $("mp-year-ctl").hidden = MS.measure !== "year" || !A;
  if (A) { const y0 = A.rows[0].year + 1, y1 = A.rows[A.step].year; $("mp-year").min = y0; $("mp-year").max = y1; if (MS.year < y0 || MS.year > y1) MS.year = Math.min(y1, y0 + 30); }
  $("mp-year").value = MS.year; $("mp-year-out").textContent = MS.year;
}
function renderMap() { syncMapTop(); drawMainMap(); drawInspector(); drawStrip(); drawDrawer(); }
function selectNode(n) { MS.sel = MS.sel === n ? null : n; MS.hiFig = null; renderMap(); }
function openModule(name) { MS.sel = name; MS.hiFig = null; setTab("map"); }
$("mp-run").addEventListener("change", e => { MS.run = e.target.value; if (MS.vs === MS.run) MS.vs = ""; renderMap(); });
$("mp-vs").addEventListener("change", e => { MS.vs = e.target.value; if (MS.vs) MS.measure = "diff"; else if (MS.measure === "diff") MS.measure = "run"; renderMap(); });
$("mp-measure").addEventListener("change", e => { MS.measure = e.target.value; renderMap(); });
$("mp-year").addEventListener("input", e => { MS.year = +e.target.value; renderMap(); });

// ================================================ experiment tab (from H)
const EXP_FIGS = ["dk", "breadth", "depth", "unemployment", "capital_share", "resistance"];
function niceTicks(lo, hi, n, log) {
  if (log) { const out = []; for (let e = Math.floor(Math.log10(lo)); e <= Math.ceil(Math.log10(hi)); e++) for (const m of [1, 2, 5]) { const v = m * 10 ** e; if (v >= lo * 0.999 && v <= hi * 1.001) out.push(v); } return out.length > n + 1 ? out.filter(v => /^1/.test(String(v))) : out; }
  const raw = (hi - lo) / n, p = 10 ** Math.floor(Math.log10(raw)), f = raw / p;
  const step = (f < 1.5 ? 1 : f < 3 ? 2 : f < 7 ? 5 : 10) * p;
  const out = []; for (let v = Math.ceil(lo / step) * step; v <= hi + step * 1e-6; v += step) out.push(+v.toFixed(10));
  return out;
}
function extent(key, lists) {
  const f = FIG[key];
  if (f.fixed) return f.fixed;
  let lo = Infinity, hi = -Infinity;
  for (const l of lists) for (const [, v] of l) if (v != null && isFinite(v) && (!f.log || v > 0)) { lo = Math.min(lo, v); hi = Math.max(hi, v); }
  if (!isFinite(lo)) return [0, 1];
  if (f.log) return [lo / 1.15, hi * 1.15];
  if (f.unit === "pct" || lo >= 0) lo = Math.min(lo, 0);
  return [lo, hi + ((hi - lo) * 0.06 || 1)];
}
function xchart(svgEl, opts) {
  const { key, lines, bands = [], yDom, compact } = opts, f = FIG[key];
  const W = svgEl.clientWidth || 300, H = svgEl.clientHeight || 100;
  const L = compact ? 4 : 46, R = compact ? 4 : 10, T = compact ? 18 : 8, B = compact ? 4 : 24;
  const yrs = lines.flatMap(l => l.pts.map(p => p[0]));
  if (!yrs.length) yrs.push(0, 1);
  const [lo, hi] = yDom, x0 = Math.min(...yrs), x1 = Math.max(x0 + 1, ...yrs);
  const tx = x => L + (x - x0) / (x1 - x0) * (W - L - R);
  const ty = v => f.log ? T + (1 - (Math.log(Math.max(v, lo)) - Math.log(lo)) / (Math.log(hi) - Math.log(lo))) * (H - T - B) : T + (1 - (v - lo) / (hi - lo)) * (H - T - B);
  let out = "";
  for (const t of niceTicks(lo, hi, compact ? 2 : 4, f.log)) {
    out += `<line x1="${L}" x2="${W - R}" y1="${ty(t)}" y2="${ty(t)}" stroke="var(--grid)"/>`;
    if (!compact) out += `<text x="${L - 6}" y="${ty(t) + 4}" text-anchor="end" font-size="11" fill="var(--muted)">${fmt(t, f.unit)}</text>`;
  }
  const ys = yearStep(x1 - x0);
  if (!compact) for (let yr = Math.ceil(x0 / ys) * ys; yr <= x1; yr += ys) out += `<text x="${tx(yr)}" y="${H - 6}" text-anchor="middle" font-size="11" fill="var(--muted)">${yr}</text>`;
  for (const b of bands) {
    const top = b.hi.map(([x, y]) => `${tx(x).toFixed(1)},${ty(y).toFixed(1)}`), bot = b.lo.slice().reverse().map(([x, y]) => `${tx(x).toFixed(1)},${ty(y).toFixed(1)}`);
    out += `<polygon points="${top.concat(bot).join(" ")}" fill="${b.colour}" opacity="0.16"/>`;
  }
  for (const l of lines) {
    let d = "", pen = false;
    for (const [x, y] of l.pts) { if (y == null || !isFinite(y)) { pen = false; continue; } d += (pen ? "L" : "M") + tx(x).toFixed(1) + " " + ty(y).toFixed(1); pen = true; }
    out += `<path d="${d}" fill="none" stroke="${l.colour}" stroke-width="${l.width || 1.5}" opacity="${l.opacity ?? 1}" stroke-linejoin="round"/>`;
  }
  out += `<line class="xcur" x1="0" x2="0" y1="${T}" y2="${H - B}" stroke="var(--text)" stroke-width="1" opacity="0"/>`;
  svgEl.innerHTML = out;
  svgEl._tx = tx; svgEl._L = L; svgEl._R = R; svgEl._W = W; svgEl._x0 = x0; svgEl._x1 = x1;
}
function attachHover(node, svgEl, rowsFn) {
  const tip = $("hovtip");
  node.addEventListener("mousemove", e => {
    const box = svgEl.getBoundingClientRect(), px = (e.clientX - box.left) / box.width * svgEl._W;
    const year = Math.round(svgEl._x0 + Math.min(1, Math.max(0, (px - svgEl._L) / (svgEl._W - svgEl._L - svgEl._R))) * (svgEl._x1 - svgEl._x0));
    const cur = svgEl.querySelector(".xcur"); cur.setAttribute("x1", svgEl._tx(year)); cur.setAttribute("x2", svgEl._tx(year)); cur.setAttribute("opacity", 0.35);
    tip.innerHTML = `<div class="yr">${year}</div>` + rowsFn(year); tip.hidden = false;
    const tw = tip.offsetWidth; tip.style.left = (e.clientX + 14 + tw > innerWidth ? e.clientX - tw - 14 : e.clientX + 14) + "px"; tip.style.top = (e.clientY + 14) + "px";
  });
  node.addEventListener("mouseleave", () => { tip.hidden = true; const c = svgEl.querySelector(".xcur"); c && c.setAttribute("opacity", 0); });
}
const seriesOf = (r, key) => r.rows.slice(0, r.step + 1).map(x => [x.year, x.v[key]]);
const atYear = (r, key, yr) => { const row = r.rows[yr - r.rows[0].year]; return row && r.rows.indexOf(row) <= r.step ? row.v[key] : null; };
function meanSeries(rs, key) { const n = Math.min(...rs.map(r => r.step + 1)); return rs[0].rows.slice(0, n).map((row, i) => [row.year, mean(rs.map(x => x.rows[i].v[key]).filter(y => y != null && isFinite(y)))]); }
function comboIsBase(g, k) { const base = byId(g.base) || membersOf(g)[0]; return !!base && k === g.cols.map(c => showVal(colBase(c, base))).join(" · "); }
function expColumns(shown, ref) {
  const gids = [...new Set(shown.map(r => r.group))];
  const one = gids.length === 1 ? gById(gids[0]) : null;
  if (one && one.cols.length) {
    const keys = combos(one).filter(k => shown.some(r => comboKey(r) === k));
    return { one, byRun: false, cols: keys.map(k => ({ label: k, colour: comboColour(one, k), runs: shown.filter(r => comboKey(r) === k), isBase: comboIsBase(one, k) })) };
  }
  return { one, byRun: true, cols: shown.map(r => {
    const d = r === ref ? null : diffs(r, ref);
    return { label: one ? runLabel(r) : fullName(r), colour: colourOf(r), runs: [r], isBase: r === ref, run: r,
      note: d === null ? (r.id === state.baseline ? "Baseline" : "Reference") : d.length ? d.map(x => `${x[0]}: ${x[1]} → ${x[2]}`).join(", ") : "Same settings" };
  }) };
}
function renderExperiment() {
  const p = $("panel-experiment");
  if (noRuns()) { p.replaceChildren(emptyState("There are no runs yet.", true)); return; }
  const shown = shownRuns();
  if (shown.length < 2) { p.replaceChildren(emptyState("Tick 2 or more runs to compare them as an experiment.")); return; }
  const ref = refOf(shown);
  const { one, byRun, cols } = expColumns(shown, ref);
  const seeds = [...new Set(shown.map(r => r.seed))];
  const gids = [...new Set(shown.map(r => r.group))];
  const seg = el("div", { class: "seg", role: "group", "aria-label": "View" },
    ["grid", "overlay"].map(v => el("button", { type: "button", "aria-pressed": String(state.expView === v), text: v === "grid" ? "Grid" : "Overlay", onclick: () => { state.expView = v; renderExperiment(); } })));
  const title = one ? one.name : `${shown.length} ticked runs`;
  const sub = one ? `${shown.length} of ${membersOf(one).length} runs ticked · ${one.claims.toLocaleString("en-GB")} firms · ${one.years} years · seed${seeds.length === 1 ? "" : "s"} ${seeds.join(", ")}`
    : `From ${gids.length} experiments: ${gids.map(id => gById(id).name).join(", ")}`;
  const body = el("div");
  p.replaceChildren(
    el("div", { class: "exp-head" }, el("div", {}, el("h2", { text: title }), el("p", { class: "sub", text: sub })),
      el("div", { class: "exp-tools" }, one ? el("button", { class: "btn sm", text: "Edit as table", onclick: () => openExpSetup(one) }) : null, seg)),
    el("p", { class: "view-line" }, ...(byRun ? [`Each column is one ticked run. The line under each name says what it changes from ${ref.id === state.baseline ? "the baseline" : "the reference run"}.`]
      : ["Each column is one value of what the experiment varies. Thin lines are ", term("seed", "seeds"), ". The thick line is their mean."])),
    body, el("div", { class: "xsum", id: "xsum" }));
  if (state.expView === "grid") {
    const wide = cols.length > 6;
    const grid = el("div", { class: "xgrid", style: `grid-template-columns: 190px repeat(${cols.length}, minmax(${wide ? "150px" : "0"},1fr))` },
      el("div", { class: "gh", text: byRun ? "Run" : one.cols.map(colLabel).join(" and ") }),
      cols.map(c => el("div", { class: "gh" + (byRun ? " ghrun" : "") }, el("div", { class: "ghl" }, el("span", { class: "dot", style: `background:${c.colour}` }), el("span", { text: c.label }), !byRun && c.isBase ? el("span", { class: "def-tag", text: "base" }) : null),
        byRun ? el("div", { class: "ghnote", text: c.note }) : null)));
    for (const key of EXP_FIGS) {
      const f = FIG[key];
      grid.append(el("div", { class: "rowlab" }, el("span", { class: "t" }, ["dk", "breadth", "depth"].includes(key) ? term(key, f.title) : f.title), el("span", { class: "x", text: f.short })));
      cols.forEach((c, i) => grid.append(el("div", { class: "cell", "data-key": key, "data-i": i }, el("span", { class: "fin" }), s("svg"))));
    }
    body.append(el("div", { class: "xscroll" }, grid));
    requestAnimationFrame(() => {
      for (const key of EXP_FIGS) {
        const dom = extent(key, cols.flatMap(c => c.runs.map(r => seriesOf(r, key))));
        for (const cell of body.querySelectorAll(`.cell[data-key="${key}"]`)) {
          const c = cols[+cell.dataset.i], rs = c.runs, svgEl = cell.querySelector("svg");
          const ms = meanSeries(rs, key);
          xchart(svgEl, { key, compact: true, yDom: dom, lines: [...rs.map(r => ({ pts: seriesOf(r, key), colour: c.colour, width: rs.length > 1 ? 1 : 1.6, opacity: rs.length > 1 ? 0.35 : 1 })), ...(rs.length > 1 ? [{ pts: ms, colour: c.colour, width: 2 }] : [])] });
          cell.querySelector(".fin").textContent = fmt(ms[ms.length - 1][1], FIG[key].unit);
          attachHover(cell, svgEl, yr => rs.map(r => `<div class="r"><span>${byRun ? esc(c.label) : "Seed " + r.seed}</span><span>${fmt(atYear(r, key, yr), FIG[key].unit)}</span></div>`).join("")
            + (rs.length > 1 ? `<div class="r"><span><b>Mean</b></span><span><b>${fmt(mean(rs.map(r => atYear(r, key, yr)).filter(v => v != null)), FIG[key].unit)}</b></span></div>` : ""));
        }
      }
    });
  } else {
    body.append(el("div", { class: "xlegend" }, cols.map(c => el("span", {}, el("span", { class: "sw", style: `background:${c.colour}` }), c.label + (!byRun && c.isBase ? " (base)" : ""))),
      !byRun && seeds.length > 1 ? el("span", { text: `Shaded: lowest to highest across ${seeds.length} seeds` }) : null));
    const og = el("div", { class: "overlay-grid" }, EXP_FIGS.map(key => el("div", { class: "ocard", "data-key": key }, el("h3", { style: "font-size:var(--step-0)", text: FIG[key].title }), el("p", { class: "small muted", text: FIG[key].short }), s("svg"))));
    body.append(og);
    requestAnimationFrame(() => {
      for (const card of og.querySelectorAll(".ocard")) {
        const key = card.dataset.key, svgEl = card.querySelector("svg"), lines = [], bands = [];
        for (const c of cols) {
          const rs = c.runs, n = Math.min(...rs.map(r => r.step + 1));
          if (rs.length > 1) bands.push({ colour: c.colour, lo: rs[0].rows.slice(0, n).map((row, j) => [row.year, Math.min(...rs.map(x => x.rows[j].v[key]))]), hi: rs[0].rows.slice(0, n).map((row, j) => [row.year, Math.max(...rs.map(x => x.rows[j].v[key]))]) });
          lines.push({ pts: meanSeries(rs, key), colour: c.colour, width: 2 });
        }
        xchart(svgEl, { key, yDom: extent(key, bands.length ? [...bands.map(b => b.lo), ...bands.map(b => b.hi), ...lines.map(l => l.pts)] : lines.map(l => l.pts)), lines, bands });
        attachHover(card, svgEl, yr => cols.map(c => `<div class="r"><span><span class="dot" style="background:${c.colour}"></span> ${esc(c.label)}</span><span>${fmt(mean(c.runs.map(r => atYear(r, key, yr)).filter(v => v != null)), FIG[key].unit)}</span></div>`).join(""));
      }
    });
  }
  renderExpSummary(one, cols, byRun);
}
function renderExpSummary(g, cols, byRun) {
  const key = EXP_FIGS.includes(state.sumFig) ? state.sumFig : "dk", f = FIG[key];
  const stats = cols.map(c => { const rs = c.runs.filter(r => r.status === "done"); if (!rs.length) return null; const fins = rs.map(r => r.rows[r.step].v[key]); return { c, mean: mean(fins), lo: Math.min(...fins), hi: Math.max(...fins), n: rs.length }; });
  const base = stats.find(x => x && x.c.isBase);
  const gapText = (a, b) => f.unit === "pct" ? `${(a - b) * 100 > 0 ? "+" : ""}${((a - b) * 100).toFixed(1)} points` : `${(a / b - 1) * 100 > 0 ? "+" : ""}${((a / b - 1) * 100).toFixed(0)}%`;
  const sel = el("select", { class: "select", "aria-label": "Figure", onchange: e => { state.sumFig = e.target.value; renderExpSummary(g, cols, byRun); } }, EXP_FIGS.map(k => el("option", { value: k, text: FIG[k].title, selected: k === key || null })));
  $("xsum").replaceChildren(
    el("div", { class: "section-head" }, el("h3", { text: `Final year: ${Math.max(...cols.flatMap(c => c.runs.map(r => r.rows[r.step].year)))}` }), el("label", { class: "small" }, "Figure ", sel)),
    el("table", { class: "tbl" }, el("thead", {}, el("tr", {}, el("th", { text: byRun ? "Run" : g.cols.map(colLabel).join(" and ") }), el("th", { class: "n", text: byRun ? "Value" : "Mean" }), byRun ? null : el("th", { class: "n" }, term("spread", "Spread")), el("th", { class: "n", text: byRun ? "Change from reference" : "Change from base" }))),
      el("tbody", {}, stats.map((x, i) => x ? el("tr", {}, el("td", {}, el("span", { class: "dot", style: `background:${x.c.colour};margin-right:8px` }), x.c.label + (x.c.isBase ? (byRun ? " (reference)" : " (base)") : "")),
        el("td", { class: "n", text: fmt(x.mean, f.unit) }), byRun ? null : el("td", { class: "n", text: x.n > 1 ? `${fmt(x.lo, f.unit)} to ${fmt(x.hi, f.unit)}` : "–" }),
        el("td", { class: "n", text: base && x !== base ? gapText(x.mean, base.mean) : "–" }))
        : el("tr", {}, el("td", { text: cols[i].label }), el("td", { class: "n muted", colspan: byRun ? "2" : "3", text: "Not finished" }))))));
}


// ================================================ set-up: new run (modal, cards from B)
let form = null;
function newRunForm(from, folder) {
  const src = from && hasData(from) ? from : (byId(state.baseline) || DEFAULT_BASE);
  form = { kind: "run", name: "", claims: src.claims, years: src.years, seed: src.seed, basedOn: src.id,
    optional: new Set(src.optional), settings: JSON.parse(JSON.stringify(src.settings || {})),
    folder: folder && gById(folder) ? folder : gById(state.recent) ? state.recent : groups.length ? groups[groups.length - 1].id : "__new",
    newFolder: "", view: "cards", mapSel: null, pick: new Set(), errors: [] };
}
function formSpec() { return { optional: [...form.optional], settings: form.settings, seed: form.seed }; }
function setDraft(mid, name, v) {
  const ms = form.settings[mid] || (form.settings[mid] = {});
  if (same(v, defaultOf(mid, name))) delete ms[name]; else ms[name] = v;
  if (!Object.keys(ms).length) delete form.settings[mid];
}
function draftDiffs() {
  if (!form || form.kind !== "run") return [];
  const base = baseOf(form.basedOn), spec = formSpec(), out = [];
  const ob = new Set(base.optional);
  for (const k of form.optional) if (!ob.has(k)) out.push({ label: modName(k), a: "Off", b: "On", mod: k, optional: "added" });
  for (const k of ob) if (!form.optional.has(k)) out.push({ label: modName(k), a: "On", b: "Off", mod: k, optional: "removed" });
  for (const mid of new Set([...Object.keys(spec.settings), ...Object.keys(base.settings || {})])) {
    const names = new Set([...Object.keys(spec.settings[mid] || {}), ...Object.keys((base.settings || {})[mid] || {})]);
    for (const n of names) { const a = valueIn(base, mid, n), b = valueIn(spec, mid, n); if (!same(a, b)) out.push({ label: `${modName(mid)} › ${setLabel(n)}`, a, b, mod: keyOf(mid) }); }
  }
  if (!same(form.seed, base.seed)) out.push({ label: "Seed", a: base.seed, b: form.seed });
  return out;
}
const numeric = st => (st.kind === "float" || st.kind === "int") && typeof st.default === "number";
function replacedBy() { const out = {}; for (const o of form.optional) for (const r of (MODS[o] && MODS[o].replaces) || []) out[r] = o; return out; }
function moduleCard(m) {
  const mid = midOf(m.name), base = baseOf(form.basedOn);
  const rep = m.core ? replacedBy()[m.name] : null;
  const changedHere = () => m.settings.filter(st => !same(valueIn(base, mid, st.name), valueIn(formSpec(), mid, st.name))).length;
  const badge = el("span", { class: "badge" });
  const card = el("article", { class: "mcard" + (m.core ? "" : " optional") + (rep ? " replaced" : ""), id: "card-" + m.name.replace(/\W/g, "-") });
  const refresh = () => { const n = changedHere(); badge.hidden = !n; badge.textContent = `${n} changed`; card.classList.toggle("changed", !!n); updateFoot(); };
  card.append(el("div", { class: "mcard-top" },
    m.image ? el("img", { src: m.image, alt: "", loading: "lazy", onerror: e => e.target.remove() }) : null,
    el("div", {}, el("h4", {}, el("button", { class: "modlink", type: "button", "data-tip": "Show on the map", onclick: () => { form.view = "map"; form.mapSel = m.name; renderSetup(); } }, modName(m.name)), badge), el("div", { class: "kind", text: m.core ? "Always runs" : (m.replaces && m.replaces.length ? `Runs in place of ${m.replaces.map(r => modName(r).toLowerCase()).join(", ")}` : "Optional") }))),
    ...(m.core ? [] : [el("button", { class: "x", type: "button", "aria-label": `Remove ${modName(m.name)}`, "data-tip": "Remove this module", text: "×", onclick: () => { form.optional.delete(m.name); afterDraftChange(); } })]),
    el("p", { class: "what", text: LINE[m.name] || "" }));
  if (rep) { card.append(el("p", { class: "replaced-note", text: `Replaced by ${modName(rep)}.` })); refreshLater(refresh); return card; }
  const tip = st => st.note ? firmify(st.note.charAt(0).toUpperCase() + st.note.slice(1)) + "." : null;
  for (const st of m.settings) {
    const name = st.name, id = `lv-${m.name.replace(/\W/g, "-")}-${name}`;
    const baseV = valueIn(base, mid, name), val = valueIn(formSpec(), mid, name);
    const reset = el("button", { class: "link reset", type: "button" });
    let row, setShown;
    if (numeric(st)) {
      const box = el("input", { class: "box", id, type: "text", inputmode: "decimal", value: String(val), "aria-label": setLabel(name), "data-kind": st.kind });
      row = el("div", { class: "lev plain" }, el("label", { for: id, "data-tip": tip(st), text: setLabel(name) }), box, reset);
      setShown = v => { box.value = v; };
      box.addEventListener("input", () => {
        const t = box.value.trim(), v = Number(t);
        const ok = t !== "" && isFinite(v) && (st.kind !== "int" || Number.isInteger(v));
        box.classList.toggle("bad", !ok);
        if (ok) { setDraft(mid, name, v); mark(); }
      });
    } else if (st.kind === "bool") {
      const sel = el("select", { class: "select box", id }, el("option", { value: "true", text: "Yes" }), el("option", { value: "false", text: "No" }));
      sel.value = String(!!val);
      row = el("div", { class: "lev plain" }, el("label", { for: id, "data-tip": tip(st), text: setLabel(name) }), sel, reset);
      setShown = v => { sel.value = String(!!v); };
      sel.addEventListener("change", () => { setDraft(mid, name, sel.value === "true"); mark(); });
    } else {
      const shown = v => Array.isArray(v) ? v.join(", ") : v == null ? "" : String(v);
      const box = el("input", { class: "box wide", id, type: "text", value: shown(val), "aria-label": setLabel(name) });
      row = el("div", { class: "lev plain" }, el("label", { for: id, "data-tip": tip(st), text: setLabel(name) }), box, reset);
      setShown = v => { box.value = shown(v); };
      box.addEventListener("input", () => {
        const t = box.value.trim();
        let v = t;
        if (st.kind === "list") { const parts = t.split(",").map(x => Number(x.trim())); if (t && parts.every(isFinite)) v = parts; }
        else if (st.kind === "none" && t === "") v = null;
        else if (t !== "" && isFinite(Number(t))) v = Number(t);
        setDraft(mid, name, v); mark();
      });
    }
    const mark = () => { const ch = !same(valueIn(formSpec(), mid, name), baseV); row.classList.toggle("is-changed", ch); reset.hidden = !ch; reset.textContent = `Reset to ${Array.isArray(baseV) ? baseV.join(", ") : baseV}`; refresh(); };
    reset.addEventListener("click", () => { setDraft(mid, name, baseV); setShown(baseV); mark(); });
    refreshLater(mark);
    card.append(row);
  }
  refreshLater(refresh);
  return card;
}
const later = [];
const refreshLater = fn => later.push(fn);
function afterDraftChange() { if (!form) return; form.kind === "run" ? renderSetup() : renderExpSetup(); }
// Time for one run, from the number of firms and years. The server runs 3 at once.
function runSeconds(claims, years) {
  const c = +claims || 30000;
  const s = c <= 30000 ? 10 * c / 30000 : c <= 100000 ? 10 + 50 * (c - 30000) / 70000 : 60 + 540 * (c - 100000) / 200000;
  return Number.isInteger(+years) && +years > 0 ? Math.max(1, s * +years / 119) : NaN;
}
function aboutTime(sec) {
  if (!isFinite(sec)) return "";
  if (sec < 60) { const s = Math.max(5, Math.round(sec / 5) * 5); return `about ${s} seconds`; }
  const m = Math.round(sec / 60); return `about ${m} minute${m === 1 ? "" : "s"}`;
}
// The number of firms: 3 usual sizes, or another number.
function firmsField(p) {
  const other = form.claimsOther || !FIRM_OPTIONS.some(([v]) => v === form.claims);
  const sel = el("select", { class: "select", id: p + "-claims", onchange: e => {
      if (e.target.value === "other") form.claimsOther = true; else { form.claimsOther = false; form.claims = +e.target.value; }
      afterDraftChange(); if (form.claimsOther) setTimeout(() => $(p + "-claims-n") && $(p + "-claims-n").focus()); } },
    FIRM_OPTIONS.map(([v, t]) => el("option", { value: v, text: t, selected: !other && v === form.claims || null })),
    el("option", { value: "other", text: "Another number", selected: other || null }));
  return el("span", { class: "firms" }, sel, other ? el("input", { class: "input num", id: p + "-claims-n", value: form.claims, inputmode: "numeric", "aria-label": "Number of firms",
    oninput: e => { form.claims = +e.target.value.replace(/[, ]/g, "") || 0; updateFoot(); } }) : null);
}
const FIRM_OPTIONS = [[30000, "30,000 (about 10 seconds)"], [100000, "100,000 (about 1 minute)"], [300000, "300,000 (about 10 minutes)"]];
function updateFoot() {
  const f = $("setup-summary"), b = $("start-btn"); if (!f || !form) return;
  if (form.kind === "run") {
    const n = draftDiffs().length, base = baseOf(form.basedOn);
    f.textContent = `${form.claims.toLocaleString("en-GB")} firms · ${form.years} years · seed ${form.seed} · ${n === 0 ? `No changes from ${fullName(base)}` : n === 1 ? `1 change from ${fullName(base)}` : `${n} changes from ${fullName(base)}`}` + (aboutTime(runSeconds(form.claims, form.years)) ? ` · ${aboutTime(runSeconds(form.claims, form.years))}` : "");
    b.textContent = "Start run";
  } else {
    const n = form.rows.length;
    const est = aboutTime(Math.ceil(n / 3) * runSeconds(form.claims, form.years));
    f.textContent = `${n} run${n === 1 ? "" : "s"}, 3 at a time` + (est ? ` · ${est}` : "");
    b.textContent = `Start ${n} run${n === 1 ? "" : "s"}`; b.disabled = !n;
  }
}
// GOV.UK error summary at the top of the set-up screen.
function showErrors(list) {
  form.errors = list;
  const body = $("setup-body"); if (!body) return;
  const old = body.querySelector(".error-summary"); if (old) old.remove();
  if (!list.length) return;
  const box = el("div", { class: "error-summary", role: "alert", tabindex: "-1", "aria-labelledby": "err-title" },
    el("h2", { id: "err-title", text: "There is a problem" }), el("ul", {}, list.map(([text, target]) => el("li", {}, target
      ? el("a", { href: "#" + target, onclick: e => { e.preventDefault(); const t = $(target); if (t) t.focus(); } }, text) : text))));
  body.prepend(box); body.scrollTop = 0; box.focus();
}
function setupShell(title, body, startLabel, onStart) {
  const box = $("setup"); box.hidden = false;
  box.replaceChildren(
    el("div", { class: "setup-head" }, el("p", { class: "app-name", text: "Capital as power workbench" }), el("h2", { id: "setup-title", text: title })),
    el("div", { class: "setup-body", id: "setup-body" }, body),
    el("div", { class: "setup-foot" }, el("p", { class: "summary", id: "setup-summary" }),
      el("button", { class: "btn", type: "button", text: "Cancel", onclick: requestCancel }),
      el("button", { class: "btn primary", id: "start-btn", type: "button", text: startLabel, onclick: onStart })));
  box.setAttribute("aria-labelledby", "setup-title");
}
function openSetup(from, folder) { newRunForm(from, folder); if (from) form.name = `${runLabel(from)} (copy)`; renderSetup(); }
function folderFields() {
  const sel = el("select", { class: "select", id: "f-folder", onchange: e => { form.folder = e.target.value; renderSetup(); if (form.folder === "__new") setTimeout(() => $("f-newfolder") && $("f-newfolder").focus()); } },
    groups.map(g => el("option", { value: g.id, text: g.name, selected: form.folder === g.id || null })),
    el("option", { value: "__new", text: "New experiment…", selected: form.folder === "__new" || null }));
  return [el("div", {}, el("label", { class: "lbl", for: "f-folder", text: "Experiment" }), sel),
    form.folder === "__new" ? el("div", {}, el("label", { class: "lbl", for: "f-newfolder", text: "Name of the new experiment" }),
      el("input", { class: "input", id: "f-newfolder", value: form.newFolder, placeholder: "For example: Labour tests", style: "width:15rem", oninput: e => form.newFolder = e.target.value })) : null];
}
function setupCtx() {
  const b = baseOf(form.basedOn);
  return { E: $("su-edges"), N: $("su-nodes"), legend: $("su-legend"), run: b.rows.length ? b : null, vs: null, measure: "run", year: 1920, blankLine: "Gains show once the start run has results.",
    sel: form.mapSel, hiFig: null, marks: draftMarks(), prefix: "su-", onSelect: jumpToCard, tipSuffix: "Select it to go to its card." };
}
const SU_MAP = `<svg id="su-svg" viewBox="0 0 1000 640" preserveAspectRatio="xMidYMid meet" role="img" aria-label="Map of modules with changes not run yet">
  <defs>
    <marker id="su-arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,1 L9,5 L0,9 z" fill="var(--edge)"/></marker>
    <marker id="su-arr-core" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,1 L9,5 L0,9 z" fill="var(--edge-core)"/></marker>
    <marker id="su-arr-hi" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,1 L9,5 L0,9 z" fill="var(--accent)"/></marker>
  </defs><g id="su-edges"></g><g id="su-nodes"></g></svg><div class="mp-legend" id="su-legend"></div>`;
function renderSetup() {
  const keep = $("setup-body") ? $("setup-body").scrollTop : 0;
  later.length = 0;
  const basedSel = el("select", { class: "select", id: "f-based", onchange: e => { const f = form.folder, nf = form.newFolder; newRunForm(byId(e.target.value), f); form.newFolder = nf; renderSetup(); } },
    startFromOptions(form.basedOn));
  const firms = firmsField("f");
  const view = form.view;
  const seg = el("div", { class: "seg", role: "group", "aria-label": "Show modules as" },
    [["cards", "Cards"], ["map", "Map"]].map(([v, l]) => el("button", { type: "button", "aria-pressed": String(view === v), text: l, onclick: () => { form.view = v; if (v === "cards") form.mapSel = null; renderSetup(); } })));
  const nOpt = form.optional.size;
  let content;
  if (view === "cards") {
    content = el("div", { class: "mcards" }, CORE_ORDER.map(n => moduleCard(MODS[n])), [...form.optional].map(n => moduleCard(MODS[n])),
      el("button", { class: "addcard", type: "button", onclick: openPicker }, el("b", { text: "+" }), "Add modules", el("span", { class: "small", text: `${CAT.optional.length - nOpt} optional modules` })));
  } else { content = el("div", { class: "su-map" }); content.innerHTML = SU_MAP; }
  const body = el("div", {},
    el("div", { class: "basics" }, ...folderFields(),
      el("div", {}, el("label", { class: "lbl", for: "f-name", text: "Name" }), el("input", { class: "input", id: "f-name", value: form.name, placeholder: "For example: Labour on", style: "width:15rem", oninput: e => form.name = e.target.value })),
      el("div", {}, el("label", { class: "lbl", for: "f-based", text: "Start from" }), basedSel),
      el("div", {}, el("label", { class: "lbl", for: "f-claims", text: "Firms at the start" }), firms),
      el("div", {}, el("label", { class: "lbl", for: "f-years", text: "Years" }), el("input", { class: "input num", id: "f-years", value: form.years, inputmode: "numeric", oninput: e => { form.years = e.target.value.trim(); updateFoot(); } })),
      el("div", {}, el("label", { class: "lbl", for: "f-seed" }, term("seed", "Seed")), el("input", { class: "input num", id: "f-seed", value: form.seed, inputmode: "numeric", oninput: e => { form.seed = e.target.value.trim(); updateFoot(); } }))),
    el("div", { class: "su-sec-head" }, el("h3", { text: "Modules" }), seg, el("span", { class: "spacer" }),
      view === "map" ? el("button", { class: "btn sm", type: "button", text: "+ Add modules", onclick: openPicker }) : null),
    el("p", { class: "sub", text: view === "cards"
      ? `The 10 main modules always run. ${nOpt} optional module${nOpt === 1 ? " is" : "s are"} on. Select a module's name to see it on the map.`
      : "Dashed rings mark changes that have not run yet. Select a module to go to its card." }),
    content);
  setupShell("New run", body, "Start run", startRun);
  for (const fn of later) fn();
  if (view === "map") drawMap(setupCtx());
  updateFoot();
  $("setup-body").scrollTop = view === "map" ? 0 : keep;
}
const flash = c => c.animate([{ boxShadow: "0 0 0 3px var(--accent)" }, { boxShadow: "0 0 0 0 transparent" }], { duration: 1400 });
function jumpToCard(n) {
  if (n === HUB) { toast("The ledger is part of the model. It has no settings."); return; }
  form.view = "cards"; form.mapSel = null; renderSetup();
  const c = $("card-" + n.replace(/\W/g, "-"));
  if (!c) { toast(`${modName(n)} is not on. Add it with Add modules.`); return; }
  c.scrollIntoView({ block: "center" }); flash(c);
}
function pendingCount() {
  if (!form) return 0;
  if (form.kind === "run") return draftDiffs().length;
  return form.cols.length || form.rows.length > 1 ? form.rows.length : 0;
}
function requestCancel() {
  const n = pendingCount();
  if (!n) { closeForm(); return; }
  const isRun = form.kind === "run", c = $("confirm");
  const keepBtn = el("button", { class: "btn", type: "button", text: "Keep editing", onclick: () => { c.hidden = true; } });
  c.replaceChildren(el("div", { class: "dialog", role: "alertdialog", "aria-modal": "true", "aria-labelledby": "cf-t", "aria-describedby": "cf-d" },
    el("h2", { id: "cf-t", text: isRun ? "Cancel this run?" : "Cancel this experiment?" }),
    el("p", { id: "cf-d", text: isRun ? `Your ${n} change${n === 1 ? "" : "s"} will be lost.` : `Your table of ${n} run${n === 1 ? "" : "s"} will be lost.` }),
    el("div", { class: "qa" }, el("button", { class: "btn danger", type: "button", text: isRun ? "Cancel run" : "Cancel experiment", onclick: () => { c.hidden = true; closeForm(); } }), keepBtn)));
  c.hidden = false;
  setTimeout(() => keepBtn.focus());
}
function closeForm() { form = null; const b = $("setup"); b.hidden = true; b.replaceChildren(); closePicker(); renderAll(); }
function checkBasics(f) {
  const errs = [];
  if (!(Number.isInteger(+f.claims) && +f.claims >= 1000 && +f.claims <= 3000000)) errs.push(["Enter the number of firms as a whole number from 1,000 to 3,000,000", (f.kind === "run" ? "f" : "x") + "-claims-n"]);
  if (!(Number.isInteger(+f.years) && +f.years >= 1 && +f.years <= 500)) errs.push(["Enter the number of years as a whole number from 1 to 500", f.kind === "run" ? "f-years" : "x-years"]);
  if (f.kind === "run" && !Number.isInteger(+f.seed)) errs.push(["Enter the seed as a whole number", "f-seed"]);
  if (f.kind === "run" && f.folder === "__new" && !(f.newFolder || "").trim()) errs.push(["Enter a name for the new experiment", "f-newfolder"]);
  return errs;
}
function settingsBody(spec) {
  const out = {};
  for (const [mid, vals] of Object.entries(spec.settings || {})) for (const [n, v] of Object.entries(vals)) if (!same(v, defaultOf(mid, n))) (out[mid] || (out[mid] = {}))[n] = v;
  return out;
}
async function startRun() {
  const errs = checkBasics(form);
  for (const box of document.querySelectorAll("#setup input.box.bad")) {
    const label = document.querySelector(`label[for="${box.id}"]`), card = box.closest(".mcard");
    const mod = card ? card.querySelector("h4 .modlink").textContent : "";
    errs.push([`${mod ? mod + " › " : ""}${label ? label.textContent : "Setting"}: enter a ${box.dataset.kind === "int" ? "whole number" : "number"}`, box.id]);
  }
  if (errs.length) { showErrors(errs); return; }
  const b = $("start-btn"); b.disabled = true;
  const body = { name: form.name.trim() || `Run ${runs.length + 1}`, claims: form.claims, years: +form.years, seed: +form.seed, optional: [...form.optional], settings: settingsBody(formSpec()) };
  if (form.folder === "__new" || !gById(form.folder)) body.new_experiment = form.newFolder.trim() || `Experiment ${groups.length + 1}`; else body.experiment = form.folder;
  try {
    const d = await api("/api/runs", "POST", body);
    tick(d.id); state.recent = d.experiment || state.recent; if (d.experiment) { state.open.add(d.experiment); state.closed.delete(d.experiment); }
    if (!byId(state.baseline)) state.baseline = d.id;
    saveView();
    form = null; $("setup").hidden = true; $("setup").replaceChildren(); closePicker();
    setTab("charts");
    await refresh(true);
  } catch (e) { b.disabled = false; showErrors([[e.message]]); }
}

// ================================================ picker: add several modules at once
function openPicker() {
  const back = $("picker"); back.hidden = false;
  const errs = {};
  const q = el("input", { class: "input", type: "search", placeholder: "Find a module, for example debt", style: "width:18rem", "aria-label": "Find a module" });
  const body = el("div", { class: "modal-body" });
  const count = el("p", { class: "summary", "aria-live": "polite" });
  const addBtn = el("button", { class: "btn primary", type: "button", onclick: addPicked });
  const allBtn = el("button", { class: "btn", type: "button" });
  const note = el("p", { class: "summary muted", "aria-live": "polite" });
  const matches = () => { const t = q.value.trim().toLowerCase(); return CAT.optional.filter(m => !m.error && (!t || (m.name + " " + modName(m.name) + " " + (LINE[m.name] || "")).toLowerCase().includes(t))); };
  const free = () => matches().filter(m => !form.optional.has(m.name));
  // Two modules that run in place of the same main module cannot run together, so Select all
  // keeps the first of them and leaves the others out.
  const clashes = (m, names) => (m.replaces || []).length && names.find(o => o !== m.name && (MODS[o].replaces || []).some(r => m.replaces.includes(r)));
  const allPicked = ms => ms.some(m => form.pick.has(m.name)) && ms.every(m => form.pick.has(m.name) || clashes(m, [...form.pick, ...form.optional]));
  allBtn.addEventListener("click", () => {
    const ms = free();
    if (allPicked(ms)) { for (const m of ms) form.pick.delete(m.name); note.textContent = ""; draw(); return; }
    const left = [];
    for (const m of ms) {
      if (form.pick.has(m.name)) continue;
      const other = clashes(m, [...form.pick, ...form.optional]);
      if (other) left.push(modName(m.name)); else form.pick.add(m.name);
    }
    note.textContent = left.length ? `${left.length} left out because another module already runs in place of the same main module: ${left.join(", ")}.` : "";
    draw();
  });
  const draw = focusId => {
    const keep = body.scrollTop, t = q.value.trim().toLowerCase();
    const grpTitles = [["rule", "Add a rule"], ["instead", "Run in place of a main module"], ["measure", "Measure only. Changes no results."]];
    body.replaceChildren(...grpTitles.flatMap(([gk, title]) => {
      const ms = CAT.optional.filter(m => optGroup(m) === gk && (!t || (m.name + " " + modName(m.name) + " " + (LINE[m.name] || "")).toLowerCase().includes(t)));
      if (!ms.length) return [];
      return [el("h3", { text: `${title} (${ms.length})` }), el("div", { class: "ptiles" }, ms.map(m => {
        const on = form.optional.has(m.name), picked = form.pick.has(m.name), id = "pk-" + m.name;
        const box = el("input", { type: "checkbox", class: "tick", id, disabled: on || null, "aria-describedby": errs[m.name] ? id + "-err" : null,
          onchange: e => {
            delete errs[m.name];
            if (e.target.checked) {
              const conflict = (m.replaces || []).length && [...form.pick].find(o => (MODS[o].replaces || []).some(r => m.replaces.includes(r)));
              if (conflict) { errs[m.name] = `${modName(conflict)} already runs in place of ${modName(m.replaces[0])}. Untick it first.`; }
              else form.pick.add(m.name);
            } else form.pick.delete(m.name);
            draw(id);
          } });
        box.checked = picked || on;
        return el("label", { class: "ptile" + (picked ? " picked" : "") + (on ? " added" : "") + (errs[m.name] ? " has-err" : ""), for: id },
          el("div", { class: "img" }, m.image ? el("img", { src: m.image, alt: "", loading: "lazy", onerror: e => e.target.remove() }) : null), box,
          el("div", { class: "t" }, modName(m.name), on ? el("span", { class: "on", text: " · Added" }) : null),
          el("div", { class: "l", text: LINE[m.name] || "" }),
          errs[m.name] ? el("p", { class: "err", id: id + "-err", text: errs[m.name] }) : null);
      }))];
    }));
    if (!body.children.length) body.append(el("p", { class: "muted", style: "padding:1rem 0", text: "No module matches." }));
    const n = form.pick.size;
    count.textContent = n ? `${n} selected` : "None selected";
    addBtn.textContent = n === 1 ? "Add 1 module" : `Add ${n} modules`; addBtn.disabled = !n;
    const ms = free();
    allBtn.textContent = allPicked(ms) ? "Clear selection" : t ? `Select all ${ms.length} shown` : "Select all";
    allBtn.disabled = !ms.length;
    body.scrollTop = keep;
    if (focusId && $(focusId)) $(focusId).focus({ preventScroll: true });
  };
  q.addEventListener("input", () => { note.textContent = ""; draw(); });
  back.replaceChildren(el("div", { class: "modal", role: "dialog", "aria-modal": "true", "aria-label": "Add modules" },
    el("div", { class: "modal-head" }, el("h2", { text: "Add modules" }), el("div", { class: "pick-tools" }, q, allBtn)),
    body,
    el("div", { class: "modal-foot" }, el("div", { class: "pick-count" }, count, note), el("button", { class: "btn", type: "button", text: "Close", onclick: closePicker }), addBtn)));
  draw(); setTimeout(() => q.focus());
}
function closePicker() { $("picker").hidden = true; }
$("picker").addEventListener("click", e => { if (e.target === $("picker")) closePicker(); });
function addPicked() {
  const names = [...form.pick];
  for (const name of names) {
    const m = MODS[name];
    for (const o of [...form.optional]) if ((MODS[o].replaces || []).some(r => (m.replaces || []).includes(r))) form.optional.delete(o);
    form.optional.add(name);
  }
  form.pick.clear(); closePicker(); form.view = "cards"; renderSetup();
  const cards = names.map(n => $("card-" + n.replace(/\W/g, "-"))).filter(Boolean);
  if (cards[0]) cards[0].scrollIntoView({ block: "center" });
  cards.forEach(flash);
}


// ================================================ set-up: new experiment (modal table of runs)
function tableFromFolder(g) {
  const ms = membersOf(g), base = byId(g.base) || ms[0];
  if (g.cols.length) return { base, cols: g.cols.map(c => ({ ...c })), rows: ms.map(r => ({ vals: [...r.vals], seed: r.seed })) };
  const cols = [];
  const addCol = c => { if (!cols.some(x => x.kind === c.kind && x.name === c.name && x.mod === c.mod)) cols.push(c); };
  for (const r of ms) {
    for (const k of new Set([...r.optional, ...base.optional])) if (r.optional.includes(k) !== base.optional.includes(k)) addCol({ kind: "module", name: k });
    for (const mid of new Set([...Object.keys(r.settings || {}), ...Object.keys(base.settings || {})]))
      for (const n of new Set([...Object.keys((r.settings || {})[mid] || {}), ...Object.keys((base.settings || {})[mid] || {})]))
        if (!same(valueIn(r, mid, n), valueIn(base, mid, n))) addCol({ kind: "setting", mod: mid, name: n });
  }
  return { base, cols, rows: ms.map(r => ({ vals: cols.map(c => c.kind === "module" ? r.optional.includes(c.name) : valueIn(r, c.mod, c.name)), seed: r.seed })) };
}
function newExpForm(g, fromRun) {
  if (g) { const t = tableFromFolder(g); form = { kind: "exp", title: `New experiment from ${g.name}`, name: `${g.name} (copy)`, basedOn: t.base.id, claims: g.claims, years: g.years, cols: t.cols, rows: t.rows, tool: null }; return; }
  const base = fromRun && hasData(fromRun) ? fromRun : (byId(state.baseline) || DEFAULT_BASE);
  form = { kind: "exp", title: "New experiment", name: "", basedOn: base.id, claims: base.claims, years: base.years, cols: [], rows: [{ vals: [], seed: base.seed }], tool: null };
}
function openExpSetup(g, fromRun) { newExpForm(g || null, fromRun || null); form.errors = []; renderExpSetup(); }
function parseCell(c, t) { if (c.kind === "module") return !!t; const n = Number(String(t).trim()); return String(t).trim() !== "" && isFinite(n) ? n : t; }
function renderExpSetup() {
  const keep = $("setup-body") ? $("setup-body").scrollTop : 0;
  const base = baseOf(form.basedOn);
  const basedSel = el("select", { class: "select", id: "x-based", onchange: e => { form.basedOn = e.target.value; renderExpSetup(); } },
    startFromOptions(form.basedOn));
  const thead = el("tr", {}, el("th", { text: "Run" }),
    form.cols.map((c, ci) => el("th", {}, el("div", { class: "colname", text: colLabel(c) }),
      el("div", { class: "colmeta", text: `In ${runLabel(base)}: ${showVal(colBase(c, base))}` }),
      el("div", { class: "coltools" },
        c.kind === "setting" ? el("button", { class: "link", type: "button", text: "Fill column", onclick: () => { form.tool = { type: "fill", col: ci }; renderExpSetup(); } }) : null,
        el("button", { class: "link danger", type: "button", text: "Remove", onclick: () => { form.cols.splice(ci, 1); for (const r of form.rows) r.vals.splice(ci, 1); renderExpSetup(); } })))),
    el("th", {}, el("div", { class: "colname" }, term("seed", "Seed"))),
    el("th", { class: "add-col" }, el("button", { class: "btn sm", type: "button", text: "+ Column", onclick: () => { form.tool = { type: "col" }; renderExpSetup(); } })));
  const tbody = el("tbody", {}, form.rows.map((row, ri) => el("tr", {},
    el("td", { class: "rn", text: String(ri + 1) }),
    form.cols.map((c, ci) => {
      const v = row.vals[ci], isBase = same(v, colBase(c, base));
      if (c.kind === "module") { const box = el("input", { type: "checkbox", "aria-label": `Run ${ri + 1}, ${colLabel(c)}`, onchange: e => { row.vals[ci] = e.target.checked; renderExpSetup(); } }); box.checked = !!v;
        return el("td", {}, el("label", { class: "toggle-cell" + (isBase ? " muted" : "") }, box, v ? "On" : "Off")); }
      return el("td", {}, el("input", { class: "cell-in" + (isBase ? " base" : ""), value: String(v), inputmode: "decimal", "aria-label": `Run ${ri + 1}, ${colLabel(c)}`,
        oninput: e => { row.vals[ci] = parseCell(c, e.target.value); e.target.classList.toggle("base", same(row.vals[ci], colBase(c, base))); } }));
    }),
    el("td", {}, el("input", { class: "cell-in seed-in", value: String(row.seed), inputmode: "numeric", "aria-label": `Run ${ri + 1}, seed`, oninput: e => { row.seed = parseInt(e.target.value, 10) || 0; } })),
    el("td", {}, el("button", { class: "del", type: "button", "aria-label": `Delete run ${ri + 1}`, "data-tip": "Delete this run", text: "×", onclick: () => { form.rows.splice(ri, 1); renderExpSetup(); } })))));
  const table = el("table", { class: "xtable" }, el("thead", {}, thead), tbody);
  const tools = el("div", { class: "xtools" },
    el("button", { class: "btn sm", type: "button", text: "+ Row", onclick: () => { const last = form.rows[form.rows.length - 1]; form.rows.push(last ? { vals: [...last.vals], seed: last.seed } : { vals: form.cols.map(c => colBase(c, base)), seed: 0 }); renderExpSetup(); } }),
    el("button", { class: "btn sm", type: "button", text: "Repeat for seeds", onclick: () => { form.tool = { type: "seeds" }; renderExpSetup(); } }));
  const body = el("div", {},
    el("div", { class: "basics" },
      el("div", {}, el("label", { class: "lbl", for: "x-name", text: "Name" }), el("input", { class: "input", id: "x-name", value: form.name, placeholder: "For example: Mergers base rate", style: "width:16rem", oninput: e => form.name = e.target.value })),
      el("div", {}, el("label", { class: "lbl", for: "x-based", text: "Start from" }), basedSel),
      el("div", {}, el("label", { class: "lbl", for: "x-claims", text: "Firms at the start" }), firmsField("x")),
      el("div", {}, el("label", { class: "lbl", for: "x-years", text: "Years" }), el("input", { class: "input num", id: "x-years", value: form.years, inputmode: "numeric", oninput: e => { form.years = e.target.value.trim(); updateFoot(); } }))),
    el("h3", { text: "Runs" }),
    el("p", { class: "sub", text: "One row is one run. Add a column for each setting you want to vary. Values that match the start run are grey." }),
    table, tools, toolForm(base));
  setupShell(form.title || "New experiment", body, "Start runs", startExperiment);
  updateFoot();
  $("setup-body").scrollTop = keep;
}
function toolForm(base) {
  const t = form.tool; if (!t) return null;
  const close = el("button", { class: "btn sm", type: "button", text: "Cancel", onclick: () => { form.tool = null; renderExpSetup(); } });
  if (t.type === "col") {
    t.mod = t.mod || "core:mergers";
    const m = MODS[keyOf(t.mod)];
    const modSel = el("select", { class: "select", id: "c-mod", onchange: e => { t.mod = e.target.value; t.name = null; renderExpSetup(); } },
      el("optgroup", { label: "Main modules" }, CORE_ORDER.map(n => el("option", { value: "core:" + n, text: modName(n), selected: t.mod === "core:" + n || null }))),
      el("optgroup", { label: "Optional modules" }, CAT.optional.map(o => el("option", { value: "opt:" + o.name, text: modName(o.name), selected: t.mod === "opt:" + o.name || null }))));
    const opts = (m.core ? [] : [{ name: "__onoff", label: "On or off" }]).concat(m.settings.filter(x => x.name !== "top").map(x => ({ name: x.name, label: setLabel(x.name) })));
    t.name = t.name && opts.some(o => o.name === t.name) ? t.name : opts[0].name;
    const setSel = el("select", { class: "select", id: "c-set", onchange: e => { t.name = e.target.value; renderExpSetup(); } }, opts.map(o => el("option", { value: o.name, text: o.label, selected: o.name === t.name || null })));
    const st = m.settings.find(x => x.name === t.name);
    const hint = t.name === "__onoff" ? `${LINE[m.name] || ""} ${(base.optional || []).includes(m.name) ? "On" : "Off"} in ${base.name}.`
      : `${st && st.note ? firmify(st.note.charAt(0).toUpperCase() + st.note.slice(1)) + ". " : ""}Default ${st ? st.default : "–"}. In ${base.name}: ${valueIn(base, t.mod, t.name)}.`;
    return el("div", { class: "inline-form" },
      el("div", { class: "field" }, el("label", { for: "c-mod", text: "Module" }), modSel),
      el("div", { class: "field" }, el("label", { for: "c-set", text: "Setting" }), setSel),
      el("button", { class: "btn primary sm", type: "button", text: "Add column", onclick: () => {
        const c = t.name === "__onoff" ? { kind: "module", name: m.name } : { kind: "setting", mod: t.mod, name: t.name };
        form.cols.push(c); for (const r of form.rows) r.vals.push(colBase(c, base)); form.tool = null; renderExpSetup(); } }),
      close, el("p", { class: "hint", text: hint }));
  }
  if (t.type === "fill") {
    const c = form.cols[t.col], bv = colBase(c, base);
    const from = el("input", { class: "input w-s", id: "f-from", value: t.from ?? +(bv / 2).toPrecision(3), inputmode: "decimal" });
    const to = el("input", { class: "input w-s", id: "f-to", value: t.to ?? +(bv * 2).toPrecision(3), inputmode: "decimal" });
    const n = el("input", { class: "input w-s", id: "f-n", value: t.n ?? 4, inputmode: "numeric" });
    const preview = el("p", { class: "hint" });
    const vals = () => { const a = +from.value, b = +to.value, k = Math.max(1, parseInt(n.value, 10) || 1); return Array.from({ length: k }, (_, i) => +(k === 1 ? a : a + (b - a) * i / (k - 1)).toPrecision(4)); };
    const upd = () => { preview.textContent = `Values: ${vals().join(", ")}. This makes ${vals().length} rows.`; };
    for (const i of [from, to, n]) i.addEventListener("input", upd);
    upd();
    return el("div", { class: "inline-form" },
      el("div", { class: "field" }, el("label", { for: "f-from", text: "From" }), from),
      el("div", { class: "field" }, el("label", { for: "f-to", text: "To" }), to),
      el("div", { class: "field" }, el("label", { for: "f-n", text: "Number of values" }), n),
      el("button", { class: "btn primary sm", type: "button", text: `Fill ${colLabel(c)}`, onclick: () => {
        const vs = vals();
        const rows = vs.map((v, i) => { const src = form.rows[Math.min(i, form.rows.length - 1)] || { vals: form.cols.map(x => colBase(x, base)), seed: 0 }; const r = { vals: [...src.vals], seed: src.seed }; r.vals[t.col] = v; return r; });
        form.rows = rows; form.tool = null; renderExpSetup(); } }),
      close, preview);
  }
  if (t.type === "seeds") {
    const inp = el("input", { class: "input", id: "s-list", value: t.list || "0, 1, 2", style: "width:10rem" });
    return el("div", { class: "inline-form" },
      el("div", { class: "field" }, el("label", { for: "s-list" }, term("seed", "Seeds"), ", separated by commas"), inp),
      el("button", { class: "btn primary sm", type: "button", text: "Repeat each run", onclick: () => {
        const seeds = inp.value.split(",").map(x => parseInt(x, 10)).filter(x => isFinite(x));
        if (!seeds.length) return;
        const uniq = []; for (const r of form.rows) if (!uniq.some(u => u.vals.every((v, i) => same(v, r.vals[i])))) uniq.push(r);
        form.rows = uniq.flatMap(r => seeds.map(sd => ({ vals: [...r.vals], seed: sd }))); form.tool = null; renderExpSetup(); } }),
      close, el("p", { class: "hint", text: `Each different row is repeated once for each seed. Now: ${form.rows.length} rows.` }));
  }
  return null;
}
async function startExperiment() {
  const errs = checkBasics(form);
  if (!form.rows.length) errs.push(["Add at least one row"]);
  form.rows.forEach((row, i) => form.cols.forEach((c, ci) => { if (c.kind === "setting" && (row.vals[ci] === "" || row.vals[ci] == null)) errs.push([`Enter a value for run ${i + 1}, ${colLabel(c)}`]); }));
  if (errs.length) { showErrors(errs); return; }
  const base = baseOf(form.basedOn);
  const name = form.name.trim() || (form.cols.length ? form.cols.map(colLabel).join(" and ") : "Experiment");
  const specs = form.rows.map(row => {
    const settings = JSON.parse(JSON.stringify(base.settings || {})), optional = new Set(base.optional);
    form.cols.forEach((c, ci) => { if (c.kind === "module") row.vals[ci] ? optional.add(c.name) : optional.delete(c.name); else (settings[c.mod] || (settings[c.mod] = {}))[c.name] = row.vals[ci]; });
    const label = form.cols.length ? form.cols.map((c, ci) => `${c.kind === "module" ? modName(c.name) : setLabel(c.name)} ${showVal(row.vals[ci])}`).join(", ") : base.name;
    return { name: `${label}, seed ${row.seed}`, claims: form.claims, years: +form.years, seed: row.seed, optional: [...optional], settings: settingsBody({ settings }) };
  });
  const b = $("start-btn"); b.disabled = true;
  let expId = null;
  try {
    expId = (await api("/api/experiments", "POST", { name })).id;
    const d = await api(`/api/experiments/${expId}/runs`, "POST", { runs: specs });
    store("exp:" + expId, { base: byId(base.id) ? base.id : null, cols: form.cols });
    setTicks(d.ids || []); state.recent = expId; state.open.add(expId);
    saveView();
    form = null; $("setup").hidden = true; $("setup").replaceChildren(); closePicker();
    setTab("experiment");
    await refresh(true);
  } catch (e) {
    if (expId) { try { await api(`/api/experiments/${expId}/delete`, "POST", {}); } catch (x) { /* leave it */ } }
    b.disabled = false; showErrors([[e.message]]);
  }
}

// ================================================ tabs and wiring
const ICON = {
  charts: '<path d="M4 19h16M5 15l4-5 4 3 6-7"/>',
  map: '<circle cx="6" cy="7" r="2.4"/><circle cx="18" cy="7" r="2.4"/><circle cx="12" cy="17" r="2.4"/><path d="M8.2 8.2l2.6 6.6M15.8 8.2l-2.6 6.6M8.5 7h7"/>',
  compare: '<path d="M4 8h14l-3-3M20 16H6l3 3"/>',
  gain: '<path d="M4 12h16M7 12V6M11 12V9M15 12v5M19 12v3"/>',
  experiment: '<rect x="4" y="4" width="7" height="7" rx="1"/><rect x="13" y="4" width="7" height="7" rx="1"/><rect x="4" y="13" width="7" height="7" rx="1"/><rect x="13" y="13" width="7" height="7" rx="1"/>',
};
const TABS = [["charts", "Charts", "Every figure for the ticked runs"], ["map", "Map", "Modules and the figures they pass to each other"], ["compare", "Diff", "Differences between the ticked runs"],
  ["gain", "Gain by source", "What each module added each year"], ["experiment", "Experiment", "Results of a series of runs"]];
TABS.forEach(([id, label, line], i) => {
  const b = el("button", { class: "tab", role: "tab", "data-tab": id, "data-tip": `${line}. Key: ${i + 1}`, onclick: () => setTab(id) });
  b.innerHTML = `<svg viewBox="0 0 24 24" aria-hidden="true">${ICON[id]}</svg>`;
  b.append(label);
  $("tabs").insertBefore(b, $("tabs").querySelector(".spacer"));
});
function setTab(t) {
  state.tab = t;
  for (const b of document.querySelectorAll(".tab")) b.setAttribute("aria-selected", String(b.dataset.tab === t));
  for (const [n] of TABS) $("panel-" + n).hidden = n !== t;
  $("hovtip").hidden = true;
  store("tab", t);
  syncTabs();
  renderTab();
 
}
function renderTab() { ({ charts: renderCharts, map: renderMap, compare: renderCompare, gain: renderGain, experiment: renderExperiment })[state.tab](); }
function syncTabs() {
  const few = shownRuns().length < 2;
  for (const id of ["compare", "experiment"]) {
    const b = document.querySelector(`.tab[data-tab="${id}"]`);
    b.classList.toggle("faded", few);
    const line = TABS.find(x => x[0] === id)[2], key = TABS.findIndex(x => x[0] === id) + 1;
    b.dataset.tip = few ? `Tick 2 or more runs to use this tab. Key: ${key}` : `${line}. Key: ${key}`;
  }
}
function renderAll() {
  if (!byId(state.baseline)) { const r = runs.find(hasData); state.baseline = r ? r.id : null; }
  renderRuns(); renderLegend(); syncTabs(); renderTab();
}
function toast(msg) { const t = el("div", { class: "toast", role: "status", text: msg }); document.body.append(t); setTimeout(() => t.remove(), 2600); }

const menu = $("new-menu");
$("new-btn").addEventListener("click", e => { e.stopPropagation(); closePop(); menu.hidden = !menu.hidden; $("new-btn").setAttribute("aria-expanded", String(!menu.hidden)); });
document.addEventListener("click", e => { menu.hidden = true; $("new-btn").setAttribute("aria-expanded", "false"); if (!pop.hidden && !pop.contains(e.target)) closePop(); });
$("m-run").addEventListener("click", () => openSetup(null, null));
$("m-exp").addEventListener("click", () => openExpSetup(null));
// Scrolling the page moves the anchor away from a pop-up, so close it; scrolling inside the pop-up does not.
addEventListener("scroll", e => { if (!pop.hidden && !pop.contains(e.target)) closePop(); }, true);
document.addEventListener("keydown", e => {
  const typing = /INPUT|SELECT|TEXTAREA/.test(document.activeElement.tagName);
  if (e.key === "Escape") {
    $("tip").hidden = true;
    if (!$("confirm").hidden) $("confirm").hidden = true;
    else if (!pop.hidden) closePop();
    else if (!$("picker").hidden) closePicker();
    else if (!$("setup").hidden) requestCancel();
    else if (MS.fig) { MS.fig = null; renderMap(); }
    return;
  }
  if (!typing && !e.metaKey && !e.ctrlKey && /^[1-5]$/.test(e.key) && $("setup").hidden) setTab(TABS[+e.key - 1][0]);
});
// tooltips: any [data-tip]
const tip = $("tip");
function placeTip(x, y) { tip.style.left = Math.min(x, innerWidth - tip.offsetWidth - 8) + "px"; tip.style.top = (y + tip.offsetHeight + 24 > innerHeight ? y - tip.offsetHeight - 12 : y + 18) + "px"; }
document.addEventListener("mouseover", e => { const t = e.target.closest && e.target.closest("[data-tip]"); if (!t || !t.dataset.tip) { tip.hidden = true; return; } tip.textContent = t.dataset.tip; tip.hidden = false; placeTip(e.clientX + 12, e.clientY); });
document.addEventListener("mousemove", e => { if (!tip.hidden) placeTip(e.clientX + 12, e.clientY); });
document.addEventListener("focusin", e => { const t = e.target.closest && e.target.closest("[data-tip]"); if (!t || !t.dataset.tip) { tip.hidden = true; return; } tip.textContent = t.dataset.tip; tip.hidden = false; const b = t.getBoundingClientRect(); placeTip(b.left, b.bottom - 12); });
addEventListener("resize", () => { if (state.tab === "experiment") renderExperiment(); });

// ================================================ start
async function boot() {
  try { CAT = await api("/api/catalogue"); }
  catch (e) { $("panel-charts").replaceChildren(el("div", { class: "notice" }, el("h2", { text: "The page could not read the model" }), el("p", { text: e.message }))); return; }
  for (const m of CAT.core) MODS[m.name] = { ...m, title: firmify(m.title), core: true };
  for (const m of CAT.optional) MODS[m.name] = { ...m, title: firmify(m.title), core: false };
  CORE_ORDER.splice(0, CORE_ORDER.length, ...CAT.core.map(m => m.name));
  DEFAULT_BASE = { id: "__default", name: "The main modules", claims: 30000, years: 119, seed: 0, optional: [], settings: {}, modules: CAT.core.map(m => m.name), rows: [], step: -1, group: null };
  buildFigures();
  if ((CAT.problems || []).length) toast(CAT.problems[0]);
  const ticks = recall("ticks", []);
  for (const [id, slot] of ticks) { state.shown.add(id); state.slot.set(id, slot); }
  state.baseline = recall("baseline", null);
  state.extra = recall("extra", []);
  await refresh(true);
  if (!state.shown.size) { const r = [...runs].reverse().find(x => x.status === "done"); if (r) { tick(r.id); saveView(); } }
  const h = location.hash.slice(1);
  setTab(TABS.some(t => t[0] === h) ? h : recall("tab", "charts"));
  renderRuns(); renderLegend();
  if (h === "new") openSetup(null, null);
  if (h === "newexp") openExpSetup(null);
}
boot();
