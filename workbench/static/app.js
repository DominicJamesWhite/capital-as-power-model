/* The workbench page. Everything about the modules comes from the server, which reads it
   from the model when asked. Nothing here lists the modules or their settings. */
"use strict";

// ---------------------------------------------------------------- words

const GLOSSARY = [
  ["Firm", "In this model a firm is valued by what its owners expect to earn from it. The model holds one record for each firm, with its employees, its earnings for each employee, hype and risk. The model also keeps government debt and the debt of all firms together as records of the same kind."],
  ["Capitalization", "What a firm is worth to its owners: the earnings they expect from it, priced today. In the model it depends on the firm's employees, its earnings for each employee, hype and risk."],
  ["Dominant capital", "The 100 firms with the highest capitalization, called the top hundred on this page. The book uses the 100 largest firms as a stand-in for the leading groups of firms and government bodies."],
  ["Differential", "Compared with the average. The theory says that owners aim to beat the average, not only to grow."],
  ["Differential capitalization", "How many times larger the average top-hundred firm is than the average firm, measured by capitalization. It is the main measure of the theory. It is made up of breadth and depth."],
  ["Differential accumulation", "The growth of differential capitalization over time. When it is positive, the top hundred are pulling further ahead of the average."],
  ["Breadth", "The part of differential capitalization that comes from size: how many times more people the average top-hundred firm employs than the average firm. The top hundred gain breadth mainly by buying other firms and by hiring."],
  ["Depth", "The part of differential capitalization that comes from earnings: how many times more the top hundred earn for each person they employ than the average firm does. The top hundred gain depth mainly by raising prices faster than others and by cutting costs."],
  ["Sabotage", "The theory's word for the way owners hold back or limit production so that prices and earnings stay high. In this theory, earnings come from this power to limit, not from producing more."],
  ["Stagflation", "Rising prices at a time of high or rising unemployment. In the theory it is one way for the top hundred to gain depth."],
  ["Markup", "How much a firm adds on top of its wage cost when it sets its price. A markup of 0.1 means the price is 10% above the wage cost."],
  ["Hype", "How far owners' hopes for earnings run above or below the earnings that arrive. A hype of 1 means hopes match earnings."],
  ["Risk", "How unsure owners are about future earnings. Higher risk lowers capitalization."],
  ["Envelope or boundary", "The limit of where the top hundred can buy other firms. At first they can only buy in their own industry. When the sector boundary opens they can buy across their sector, and when the national boundary opens, across the whole country."],
  ["Resistance", "One number from 0 to 1 for how strongly people push back against rising prices, unemployment and the power of the top hundred."],
  ["Capitalist share of income", "The part of all income that goes to owners as earnings. The rest is mostly wages."],
  ["Module", "One part of the theory written as a rule, for example mergers or resistance. Nine modules always run. Others can be switched on."],
  ["Setting", "A number that controls how strong or how fast a module's rule is."],
  ["Default", "The value of a setting that the model's builders chose. Every setting starts at its default."],
  ["Seed", "A number that fixes the chances used by some rules. Runs with the same seed and settings give the same results."],
  ["Gain by source", "Each year differential capitalization rises or falls. The gain by source shows how much of that change each module caused."],
  ["Log scale", "A way of drawing a chart where equal steps up the chart mean equal percentage rises. It makes a figure that grows from 10 to 10,000 easier to read."],
  ["Year labels", "The model counts years from a start labelled 1890. The labels are not real dates, and the model is not meant to match real history."],
];

// The main figures, in the order they are shown. A figure the run does not report is skipped.
const MAIN = [
  { key: "dk", title: "Differential capitalization of the top hundred", unit: "times", axis: "Times the average firm", log: true,
    explain: "How many times larger the average top-hundred firm is than the average firm, measured by what owners think the firms are worth. It is breadth times depth, adjusted for hype and risk." },
  { key: "breadth", title: "Breadth: how much bigger the top hundred are", unit: "times", axis: "Times the average firm", log: true,
    explain: "How many times more people the average top-hundred firm employs than the average firm. The top hundred gain breadth mainly by buying other firms." },
  { key: "depth", title: "Depth: how much more the top hundred earn for each employee", unit: "times", axis: "Times the average firm",
    explain: "How many times more the top hundred earn for each person they employ than the average firm does. They gain depth mainly by raising prices faster than others." },
  { key: "unemployment", title: "Unemployment", unit: "pct", axis: "Per cent of the working population",
    explain: "The part of the working population without a paid job." },
  { key: "capital_share", title: "Capitalist share of income", unit: "pct", axis: "Per cent of all income",
    explain: "The part of all income that goes to owners as earnings. The rest is mostly wages." },
  { key: "price_level", title: "Price level", unit: "num", axis: "Average price, in wages at the start", log: true,
    explain: "The average price of what one employee makes in a year. At the start the wage is 1. How it rises and falls matters more than its level." },
  { key: "inflation", title: "Inflation", unit: "pct", axis: "Per cent a year",
    explain: "How much the price level rose since the year before. Below zero means prices fell." },
  { key: "mergers_against_hiring", title: "Mergers against new hiring", unit: "num", axis: "Employees bought for each new hire",
    explain: "For each person newly hired in the whole economy, how many employees the top hundred gained by buying other firms. It stands in for the book's measure of buying firms against building new ones." },
  { key: "resistance", title: "Resistance", unit: "num", axis: "0 means none, 1 means the most", fixed: [0, 1],
    explain: "How strongly people push back against rising prices, unemployment and the power of the top hundred, from 0 to 1." },
  { key: "roadblocks", title: "Roadblocks against mergers", unit: "num", axis: "0 means none, 1 means the most", fixed: [0, 1],
    explain: "How strongly institutions slow down mergers and keep boundaries closed, from 0 to 1. Mergers themselves make roadblocks rise." },
  { key: "perm_sector", title: "Opening of the sector boundary", unit: "num", axis: "0 means closed, 1 means fully open", fixed: [0, 1],
    explain: "How freely the top hundred can buy firms outside their own industry but inside their sector." },
  { key: "perm_nation", title: "Opening of the national boundary", unit: "num", axis: "0 means closed, 1 means fully open", fixed: [0, 1],
    explain: "How freely the top hundred can buy firms anywhere in the country, outside their own sector." },
];
const MAIN_KEYS = new Set(MAIN.map(m => m.key));

// Plain names for some other figures. Any figure not named here is still listed, under its own name.
const NAMES = {
  claims: "Number of firms", firms: "Number of firms", d_earnings: "Differential earnings for each claim", d_hype: "Differential hype",
  d_risk: "Differential risk", top_share_employees: "Top hundred's share of all employees",
  top_share_cap: "Top hundred's share of all capitalization", other_costs: "Average cost other than the wage",
  power_index: "Power index: capitalization of the average top-hundred firm, in wages", employment: "Number of people employed",
  markup: "Average markup", markup_top: "Average markup of the top hundred", other_income_part: "Other income as a part of capitalist income",
  other_income_part_top: "Other income as a part of the top hundred's income", da: "Differential accumulation in the year",
  wage: "Wage", workforce: "Working population", workforce_growth: "Growth of the working population", nrr: "Normal rate of return",
  stagflation_intensity: "Intensity of stagflation", cohesion: "Cohesion of the top hundred", interest_share: "Interest as a part of capitalist income",
  pressure: "Pressure on boundaries", merger_volume: "Merger volume", new_hires: "New hires", pool_open: "Part of reachable firms not yet held by the top hundred",
  hiring_drag: "Cut in hiring caused by mergers", crisis: "Crisis level", inflation_push: "Price rise pushed by the top hundred",
  corporate_debt: "Corporate debt", government_debt: "Government debt", government_debt_dominant: "Government debt held by the top hundred",
  wage_earners_net: "Transfers to wage earners, as a part of the wage bill", concentration: "Top hundred's share of all employees (as the modules read it)",
};
const PCT_KEYS = new Set(["unemployment", "capital_share", "inflation", "top_share_employees", "top_share_cap", "interest_share",
  "other_income_part", "other_income_part_top", "workforce_growth", "nrr"]);

const SOURCE_NAMES = {
  "turnover": "Changes in which firms are in the top hundred",
  "risk floor": "The lowest level that risk can fall to",
};

// ---------------------------------------------------------------- small helpers

// The page always says "firm". The model's own names and texts may say "claim" (for example a
// figure called "claims", or "new_claim_share"); this turns each such word into "firm" on screen.
function firmify(text) {
  return String(text).replace(/(?<![A-Za-z])([Cc])laim(s?)(?![A-Za-z])/g, (_, c, s) => (c === "C" ? "Firm" : "firm") + s);
}
function el(tag, attrs, ...kids) {
  const e = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs || {})) {
    if (v === null || v === undefined || v === false) continue;
    if (k === "class") e.className = v;
    else if (k === "text") e.textContent = firmify(v);
    else if (k.startsWith("on")) e.addEventListener(k.slice(2), v);
    else if (k === "aria-label" || k === "title") e.setAttribute(k, firmify(v));
    else e.setAttribute(k, v === true ? "" : v);
  }
  for (const k of kids.flat()) {
    if (k === null || k === undefined || k === false) continue;
    e.append(k instanceof Node ? k : document.createTextNode(firmify(String(k))));
  }
  return e;
}
const $ = id => document.getElementById(id);
const SVGNS = "http://www.w3.org/2000/svg";
function svg(tag, attrs) {
  const e = document.createElementNS(SVGNS, tag);
  for (const [k, v] of Object.entries(attrs || {})) e.setAttribute(k, v);
  return e;
}
function store(key, value) { try { localStorage.setItem("workbench:" + key, JSON.stringify(value)); } catch (e) { /* not needed */ } }
function recall(key, fallback) {
  try { const v = localStorage.getItem("workbench:" + key); return v === null ? fallback : JSON.parse(v); } catch (e) { return fallback; }
}
async function api(path, method, body) {
  const opts = { method: method || "GET", headers: {} };
  if (body !== undefined) { opts.body = JSON.stringify(body); opts.headers["Content-Type"] = "application/json"; }
  let res;
  try { res = await fetch(path, opts); } catch (e) {
    throw new Error("The page cannot reach the workbench. Check that the workbench window is still open, then reload this page.");
  }
  let data = {};
  try { data = await res.json(); } catch (e) { /* empty */ }
  if (!res.ok) { const err = new Error(data.error || "Something went wrong."); err.detail = data.detail; throw err; }
  return data;
}
function humanise(name) {
  const s = String(name).replace(/_/g, " ").trim();
  return s.charAt(0).toUpperCase() + s.slice(1);
}
function plural(n, one, many) { return `${n.toLocaleString("en-GB")} ${n === 1 ? one : many}`; }
function listWords(items) {
  if (items.length <= 1) return items.join("");
  return items.slice(0, -1).join(", ") + " and " + items[items.length - 1];
}
function fmtNumber(v, digits) {
  if (v === null || v === undefined || !isFinite(v)) return "no figure";
  const a = Math.abs(v);
  if (digits !== undefined) return v.toLocaleString("en-GB", { minimumFractionDigits: digits, maximumFractionDigits: digits });
  if (a >= 1000) return v.toLocaleString("en-GB", { maximumFractionDigits: 0 });
  if (a >= 100) return v.toLocaleString("en-GB", { maximumFractionDigits: 1 });
  if (a >= 1) return v.toLocaleString("en-GB", { maximumFractionDigits: 2 });
  if (a === 0) return "0";
  return v.toLocaleString("en-GB", { maximumSignificantDigits: 3 });
}
function fmtValue(v, unit) {
  if (v === null || v === undefined || !isFinite(v)) return "no figure";
  if (unit === "pct") return (v * 100).toLocaleString("en-GB", { maximumFractionDigits: Math.abs(v) < 0.1 ? 2 : 1 }) + "%";
  if (unit === "times") return fmtNumber(v) + " times";
  if (unit === "gain") return (v > 0 ? "+" : "") + v.toLocaleString("en-GB", { maximumFractionDigits: 3, minimumFractionDigits: 3 });
  return fmtNumber(v);
}
function cssVar(name) { return getComputedStyle(document.documentElement).getPropertyValue(name).trim(); }
function seriesColour(slot) { return cssVar(`--s${(slot % 8) + 1}`); }

// ---------------------------------------------------------------- state

const state = {
  cat: null,
  modules: {},            // id -> catalogue entry
  form: { optional: new Set(), settings: {} },
  runs: {},               // id -> {meta, rows, detail}
  shown: new Set(recall("shown", [])),
  extra: recall("extra", []),
  gainRun: null,
  gainMode: recall("gainMode", "year"),
  logCharts: new Set(recall("log", [])),
  editing: null,
  listSignature: "",
  lastStarted: null,
};

// ---------------------------------------------------------------- tabs

function setupTabs() {
  const tabs = [...document.querySelectorAll('[role="tab"]')];
  function select(tab, focus) {
    for (const t of tabs) {
      const on = t === tab;
      t.setAttribute("aria-selected", on ? "true" : "false");
      t.tabIndex = on ? 0 : -1;
      $(t.getAttribute("aria-controls")).hidden = !on;
    }
    if (focus) tab.focus();
    store("tab", tab.id);
    if (tab.id === "tab-results") drawAllCharts();
  }
  tabs.forEach((t, i) => {
    t.addEventListener("click", () => select(t));
    t.addEventListener("keydown", e => {
      let j = null;
      if (e.key === "ArrowRight") j = (i + 1) % tabs.length;
      if (e.key === "ArrowLeft") j = (i - 1 + tabs.length) % tabs.length;
      if (e.key === "Home") j = 0;
      if (e.key === "End") j = tabs.length - 1;
      if (j !== null) { e.preventDefault(); select(tabs[j], true); }
    });
  });
  const fromLink = { "#setup": "tab-setup", "#results": "tab-results", "#words": "tab-words" }[location.hash];
  const saved = $(fromLink || recall("tab", "tab-setup"));
  if (saved) select(saved);
  return id => select($(id));
}
let showTab = () => {};

function banner(kind, title, ...body) {
  const b = $("banner");
  b.className = "banner" + (kind === "success" ? "" : " " + kind);
  b.replaceChildren(el("p", { class: "banner-title", text: title }), el("div", { class: "banner-body" }, ...body));
  b.hidden = false;
  b.focus();
}

// ---------------------------------------------------------------- glossary

function renderGlossary() {
  const dl = $("glossary");
  for (const [term, text] of GLOSSARY) dl.append(el("dt", { text: term }), el("dd", { text }));
}

// ---------------------------------------------------------------- the module catalogue and the form

function defaultString(s) {
  if (s.kind === "list") return (s.default || []).join(", ");
  if (s.kind === "none" || s.default === null) return "";
  if (s.kind === "bool") return s.default ? "true" : "false";
  return String(s.default);
}
function moduleLabel(m) { return m.title || humanise(m.name); }
function settingDomId(modId, name) { return "set-" + modId.replace(/[^a-z0-9]/gi, "-") + "-" + name; }

async function loadCatalogue(again) {
  const status = $("catalogue-status");
  status.textContent = again ? "Reading the list of modules from the model again…" : "Reading the list of modules from the model…";
  let cat;
  try { cat = await api("/api/catalogue"); } catch (e) {
    status.textContent = "";
    $("catalogue-problems").replaceChildren(el("div", { class: "problem-box" },
      el("p", {}, el("b", { text: "The list of modules could not be read from the model. " }), e.message),
      el("p", { text: "This can happen while someone is changing the model. Wait a moment, then select Read the modules again." }),
      e.detail ? el("details", {}, el("summary", { text: "Technical details" }), el("pre", { text: e.detail })) : null));
    return;
  }
  state.cat = cat;
  state.modules = {};
  for (const m of [...cat.core, ...cat.optional]) state.modules[m.id] = m;
  // keep choices that still apply
  const lost = [];
  for (const id of [...state.form.optional]) if (!state.modules["opt:" + id]) { state.form.optional.delete(id); lost.push(id); }
  for (const [modId, vals] of Object.entries(state.form.settings)) {
    const m = state.modules[modId];
    for (const name of Object.keys(vals)) {
      if (!m || !m.settings.some(s => s.name === name)) { delete vals[name]; lost.push(`${modId.slice(modId.indexOf(":") + 1)}: ${name}`); }
    }
  }
  const problems = (cat.problems || []).map(p => el("div", { class: "problem-box" }, el("p", { text: p })));
  $("catalogue-problems").replaceChildren(...problems);
  status.textContent = `The model has ${plural(cat.core.length, "module that always runs", "modules that always run")} and ${plural(cat.optional.length, "module", "modules")} you can switch on.`;
  if (again && lost.length) banner("info", "The model has changed", el("p", { text: "These choices no longer apply and have been removed: " + lost.join("; ") + "." }));
  renderModules();
  updateRunSummary();
  fillExtraSelect();
}

function renderModules() {
  const core = $("core-modules"), opt = $("optional-modules");
  core.replaceChildren(...state.cat.core.map(m => moduleCard(m, false)));
  opt.replaceChildren(...state.cat.optional.map(m => moduleCard(m, true)));
  applyFilter();
}

function paragraphs(list) {
  const out = [];
  let ol = null;
  for (const p of list) {
    const m = p.match(/^(\d+)\.\s+(.*)$/);
    if (m) {
      if (!ol) { ol = el("ol"); out.push(ol); }
      ol.append(el("li", { text: m[2] }));
    } else if (/^-\s+/.test(p)) {
      if (!ol || ol.tagName !== "UL") { ol = el("ul"); out.push(ol); }
      ol.append(el("li", { text: p.replace(/^-\s+/, "") }));
    } else { ol = null; out.push(el("p", { text: p })); }
  }
  return out;
}

function moduleCard(m, optional) {
  const key = m.id.slice(m.id.indexOf(":") + 1);
  const card = el("div", { class: "module", id: "mod-" + m.id.replace(/[^a-z0-9]/gi, "-"), "data-search": [m.name, m.title, m.summary, m.class].join(" ").toLowerCase() });
  const head = el("div", { class: "head" });
  if (optional) {
    const box = el("input", { type: "checkbox", id: "on-" + key, disabled: m.error ? true : null });
    box.checked = state.form.optional.has(key);
    box.addEventListener("change", () => {
      if (box.checked) state.form.optional.add(key); else state.form.optional.delete(key);
      card.classList.toggle("on", box.checked);
      updateRunSummary();
    });
    card.classList.toggle("on", box.checked);
    head.append(el("div", { class: "checkbox" }, box, el("label", { for: "on-" + key }, "Switch on: ", moduleLabel(m))));
  } else {
    head.append(el("h5", { text: moduleLabel(m) }), el("span", { class: "tag", text: "Always runs" }));
  }
  const changedTag = el("span", { class: "tag changed", hidden: true });
  head.append(changedTag);
  card.append(head);
  card.append(el("p", { class: "code-name", text: `Name in the model: ${m.name}` }));
  if (m.error) {
    card.classList.add("broken");
    card.append(el("div", { class: "problem-box" },
      el("p", { text: "This module could not be loaded from the model, so it cannot be switched on. This often happens while someone is changing the module. The model said:" }),
      el("pre", { text: m.error })));
    return card;
  }
  if (m.summary) card.append(el("p", { class: "summary", text: m.summary }));
  if (m.class_note) card.append(el("p", { class: "note", text: m.class_note }));
  if (m.doc_note) card.append(el("p", { class: "note", text: m.doc_note }));
  if (m.replaces && m.replaces.length) {
    const names = m.replaces.map(r => { const c = state.modules["core:" + r]; return c ? `${moduleLabel(c)} (${r})` : r; });
    card.append(el("p", { class: "note", text: `When you switch this on, it runs in place of ${listWords(names)}.` }));
  }
  if ((m.rule && m.rule.length) || (m.book && m.book.length) || (m.additions && m.additions.length)) {
    const more = el("div", { class: "more" });
    if (m.rule.length) more.append(el("h5", { text: "How the rule works" }), ...paragraphs(m.rule));
    if (m.book.length) more.append(el("h5", { text: "What the book says" }), ...paragraphs(m.book));
    if (m.additions.length) more.append(el("h5", { text: "What the model adds to the book" }), ...paragraphs(m.additions));
    card.append(el("details", {}, el("summary", { text: "More about this module" }), more));
  }
  if (m.settings.length) {
    const tbody = el("tbody");
    const sumText = el("span");
    const details = el("details", {}, el("summary", {}, sumText),
      el("table", { class: "settings-table" },
        el("thead", {}, el("tr", {}, el("th", { text: "Setting" }), el("th", { text: "Value" }), el("th", { text: "Default" }), el("th", {}, el("span", { class: "visually-hidden", text: "Reset" })))),
        tbody));
    const refresh = () => {
      const n = Object.keys(state.form.settings[m.id] || {}).length;
      sumText.textContent = `Settings (${m.settings.length})` + (n ? `, ${n} changed` : "");
      changedTag.hidden = !n;
      changedTag.textContent = n === 1 ? "1 setting changed" : `${n} settings changed`;
    };
    for (const s of m.settings) tbody.append(settingRow(m, s, refresh));
    refresh();
    card.append(details);
    card._refresh = refresh;
  } else {
    card.append(el("p", { class: "hint", text: "This module has no settings." }));
  }
  return card;
}

function settingRow(m, s, refresh) {
  const id = settingDomId(m.id, s.name);
  const def = defaultString(s);
  const current = (state.form.settings[m.id] || {})[s.name];
  const value = current !== undefined ? current : def;
  let input;
  if (s.kind === "bool") {
    input = el("select", { class: "select", id }, el("option", { value: "true", text: "Yes" }), el("option", { value: "false", text: "No" }));
    input.value = value;
  } else {
    input = el("input", { class: "input setting", id, type: "text", autocomplete: "off", inputmode: (s.kind === "int" || s.kind === "float") ? "decimal" : null });
    input.value = value;
  }
  const errorSpot = el("span", { class: "error-message", id: id + "-error", hidden: true });
  const reset = el("button", { type: "button", class: "button secondary small", text: "Reset", "aria-label": `Reset ${humanise(s.name)} to its default` });
  const changedNote = el("span", { class: "tag changed", text: "Changed", hidden: true });
  const sync = () => {
    const v = input.value;
    const vals = state.form.settings[m.id] || (state.form.settings[m.id] = {});
    if (v.trim() === def.trim()) delete vals[s.name]; else vals[s.name] = v;
    if (!Object.keys(vals).length) delete state.form.settings[m.id];
    const changed = vals[s.name] !== undefined;
    reset.disabled = !changed;
    changedNote.hidden = !changed;
    input.classList.remove("error");
    errorSpot.hidden = true;
    refresh();
    updateRunSummary();
  };
  input.addEventListener(s.kind === "bool" ? "change" : "input", sync);
  reset.addEventListener("click", () => { input.value = def; sync(); input.focus(); });
  const kindHint = { int: "A whole number.", float: "A number.", list: "Numbers separated by commas.", bool: "Yes or no.", none: "Leave empty for none.", text: "Text.", other: "", required: "No default. You must enter a value." }[s.kind] || "";
  const defText = s.kind === "bool" ? (s.default ? "Yes" : "No") : (def === "" ? "None" : def);
  const row = el("tr", {},
    el("td", {},
      el("label", { class: "setting-name", for: id, text: humanise(s.name) }),
      s.note ? el("p", { class: "setting-note", text: s.note.charAt(0).toUpperCase() + s.note.slice(1) }) : null,
      el("div", { class: "setting-code", text: s.name })),
    el("td", {}, errorSpot, input, " ", changedNote, el("div", { class: "setting-note", text: kindHint })),
    el("td", { text: defText }),
    el("td", {}, reset));
  input.setAttribute("aria-describedby", id + "-error");
  reset.disabled = current === undefined;
  changedNote.hidden = current === undefined;
  input._check = () => checkSetting(s, input.value);
  input._show = msg => { errorSpot.textContent = msg; errorSpot.hidden = !msg; input.classList.toggle("error", !!msg); };
  return row;
}

function checkSetting(s, v) {
  const t = String(v).trim();
  if (s.kind === "int") return /^-?\d+$/.test(t) ? "" : `Enter a whole number, like ${defaultString(s) || 1}`;
  if (s.kind === "float") return (t !== "" && isFinite(Number(t))) ? "" : `Enter a number, like ${defaultString(s) || 1}`;
  if (s.kind === "list") return t.split(",").every(x => x.trim() !== "" && isFinite(Number(x))) ? "" : "Enter numbers separated by commas, like 0, 1";
  if (s.kind === "required") return t ? "" : "Enter a value";
  return "";
}

function applyFilter() {
  const q = $("module-filter").value.trim().toLowerCase();
  for (const card of document.querySelectorAll(".module")) {
    card.classList.toggle("hidden-by-filter", q !== "" && !card.dataset.search.includes(q));
  }
}

function changedCount() { return Object.values(state.form.settings).reduce((n, v) => n + Object.keys(v).length, 0); }

function readClaims() {
  const r = document.querySelector('input[name="claims"]:checked');
  if (!r) return NaN;
  if (r.value === "other") return Number(String($("claims-number").value).replace(/[, ]/g, ""));
  return Number(r.value);
}

function updateRunSummary() {
  if (!state.cat) return;
  const claims = readClaims(), years = Number($("years").value);
  const parts = [];
  parts.push(`This run will start with ${isFinite(claims) && claims > 0 ? claims.toLocaleString("en-GB") : "the number of"} firms and last ${isFinite(years) && years > 0 ? plural(years, "year", "years") : "the number of years you choose"}.`);
  const on = [...state.form.optional];
  parts.push(on.length ? `${on.length === 1 ? "1 optional module is" : on.length + " optional modules are"} switched on: ${listWords(on)}.` : "No optional modules are switched on.");
  const n = changedCount();
  parts.push(n ? `${n === 1 ? "1 setting has" : n + " settings have"} been changed from the default.` : "All settings are at their defaults.");
  $("run-summary").textContent = parts.join(" ");
}

function showErrors(errors) {
  const box = $("error-summary"), list = $("error-list");
  if (!errors.length) { box.hidden = true; return; }
  list.replaceChildren(...errors.map(([target, text]) => el("li", {}, el("a", { href: "#" + target, onclick: e => {
    e.preventDefault();
    const t = $(target);
    if (!t) return;
    const det = t.closest("details");
    if (det) det.open = true;
    t.focus();
  } }, text))));
  box.hidden = false;
  box.focus();
}

async function startRun() {
  const errors = [];
  for (const id of ["years", "seed", "claims-number"]) { const e = $(id); e.classList.remove("error"); }
  const claims = readClaims();
  if (!Number.isInteger(claims) || claims < 1000 || claims > 3000000) {
    errors.push(["claims-number", "Enter a number of firms between 1,000 and 3,000,000"]);
    $("claims-other").checked = true; $("claims-other-box").hidden = false; $("claims-number").classList.add("error");
  }
  const years = Number($("years").value);
  if (!Number.isInteger(years) || years < 1 || years > 1000) { errors.push(["years", "Enter a number of years between 1 and 1,000"]); $("years").classList.add("error"); }
  const seed = Number($("seed").value);
  if (!Number.isInteger(seed) || seed < 0) { errors.push(["seed", "Enter a seed that is a whole number, 0 or more"]); $("seed").classList.add("error"); }
  // settings
  const used = [...state.cat.core.map(m => m.id), ...[...state.form.optional].map(k => "opt:" + k)];
  for (const modId of used) {
    const m = state.modules[modId];
    for (const s of m.settings) {
      const input = $(settingDomId(modId, s.name));
      if (!input || !input._check) continue;
      const msg = input._check();
      input._show(msg);
      if (msg) errors.push([input.id, `${moduleLabel(m)}, ${humanise(s.name).toLowerCase()}: ${msg}`]);
    }
  }
  // optional modules that cannot run together
  const chosen = [...state.form.optional].map(k => state.modules["opt:" + k]);
  for (let i = 0; i < chosen.length; i++) for (let j = i + 1; j < chosen.length; j++) {
    const a = chosen[i], b = chosen[j];
    const both = (a.replaces || []).filter(r => (b.replaces || []).includes(r));
    if (a.model_name && a.model_name === b.model_name) errors.push(["on-" + b.name, `${a.name} and ${b.name} are the same module. Switch one of them off`]);
    else if (both.length) errors.push(["on-" + b.name, `${a.name} and ${b.name} both run in place of ${listWords(both)}, so they cannot run together. Switch one of them off`]);
  }
  showErrors(errors);
  if (errors.length) return;
  const settings = {};
  for (const [modId, vals] of Object.entries(state.form.settings)) {
    if (!used.includes(modId) || !Object.keys(vals).length) continue;
    settings[modId] = { ...vals };
  }
  const spec = { name: $("run-name").value.trim(), claims, years, seed, optional: [...state.form.optional], settings };
  const button = $("start-run");
  button.disabled = true;
  try {
    const res = await api("/api/runs", "POST", spec);
    state.shown.add(res.id);
    store("shown", [...state.shown]);
    state.gainRun = res.id;
    state.lastStarted = res.id;
    $("run-name").value = "";
    showTab("tab-results");
    banner("success", "Your run has been added",
      el("p", { text: "The charts below fill in year by year while the model runs. Runs go one at a time, so a new run waits until the one before it has finished." }));
    poll(true);
  } catch (e) {
    showErrors([["start-run", e.message]]);
  } finally { button.disabled = false; }
}

function resetSettings() {
  state.form.settings = {};
  renderModules();
  updateRunSummary();
  $("reset-settings").focus();
}

function useSettingsOf(run) {
  const spec = run.detail && run.detail.spec;
  if (!spec || !state.cat) return;
  const lost = [];
  state.form.optional = new Set();
  for (const k of spec.optional || []) { if (state.modules["opt:" + k] && !state.modules["opt:" + k].error) state.form.optional.add(k); else lost.push(k); }
  state.form.settings = {};
  for (const [modId, vals] of Object.entries(spec.settings || {})) {
    const m = state.modules[modId];
    for (const [name, v] of Object.entries(vals)) {
      const s = m && m.settings.find(x => x.name === name);
      if (!s) { lost.push(`${modId.slice(modId.indexOf(":") + 1)}: ${name}`); continue; }
      const text = Array.isArray(v) ? v.join(", ") : String(v);
      if (text.trim() !== defaultString(s).trim()) (state.form.settings[modId] = state.form.settings[modId] || {})[name] = text;
    }
  }
  const preset = document.querySelector(`input[name="claims"][value="${spec.claims}"]`);
  if (preset) { preset.checked = true; $("claims-other-box").hidden = true; }
  else { $("claims-other").checked = true; $("claims-other-box").hidden = false; $("claims-number").value = spec.claims; }
  $("years").value = spec.years;
  $("seed").value = spec.seed;
  $("run-name").value = "";
  renderModules();
  updateRunSummary();
  showTab("tab-setup");
  const body = [el("p", { text: `The settings of "${run.meta.name}" are now in the form. Change the one thing you want to test, give the run a new name, then select Start run.` })];
  if (lost.length) body.push(el("p", { text: "These choices no longer exist in the model and were left out: " + lost.join("; ") + "." }));
  banner("info", "Settings copied", ...body);
}

// ---------------------------------------------------------------- runs

let pollTimer = null;
async function poll(now) {
  clearTimeout(pollTimer);
  let list;
  try { list = (await api("/api/runs")).runs; } catch (e) {
    $("progress-area").replaceChildren(el("div", { class: "problem-box" }, el("p", { text: e.message })));
    pollTimer = setTimeout(poll, 4000);
    return;
  }
  const seen = new Set();
  let changed = false;
  if (recall("shown", null) === null && list.length) {      // first visit: show the latest two finished runs
    for (const m of list.filter(x => x.status === "finished").slice(-2)) state.shown.add(m.id);
    store("shown", [...state.shown]);
  }
  for (const meta of list) {
    seen.add(meta.id);
    const r = state.runs[meta.id] || (state.runs[meta.id] = { meta, rows: [], detail: null });
    const statusChanged = r.meta.status !== meta.status;
    r.meta = meta;
    const want = state.shown.has(meta.id) || meta.status === "running" || meta.status === "failed";
    if (want && (r.rows.length < meta.rows_count || !r.detail || statusChanged)) {
      try {
        const d = await api(`/api/runs/${meta.id}?since=${r.rows.length}`);
        if (d.since === r.rows.length) r.rows.push(...d.rows);
        r.detail = d;
        changed = true;
      } catch (e) { /* try again next time */ }
    }
  }
  for (const id of Object.keys(state.runs)) if (!seen.has(id)) { delete state.runs[id]; state.shown.delete(id); changed = true; }
  renderRuns();
  renderProgress();
  if (changed) { fillExtraSelect(); scheduleCharts(); }
  const busy = list.some(m => m.status === "running" || m.status === "waiting");
  $("tab-running").textContent = busy ? "(running)" : "";
  pollTimer = setTimeout(poll, busy ? 800 : 5000);
}

function statusText(meta) {
  switch (meta.status) {
    case "waiting": return "Waiting to start";
    case "running": return "Running";
    case "finished": return "Finished";
    case "stopped": return "Stopped";
    case "failed": return "Stopped by an error";
    default: return meta.status;
  }
}

function whatText(meta) {
  const bits = [`${meta.claims.toLocaleString("en-GB")} claims`, plural(meta.years, "year", "years"), `seed ${meta.seed}`];
  const opt = meta.optional || [];
  bits.push(opt.length ? `switched on: ${opt.join(", ")}` : "no optional modules");
  if (meta.changed) bits.push(meta.changed === 1 ? "1 setting changed" : `${meta.changed} settings changed`);
  return bits.join("; ");
}

function renderRuns() {
  const metas = Object.values(state.runs).map(r => r.meta).sort((a, b) => a.created < b.created ? -1 : 1);
  const sig = JSON.stringify(metas.map(m => [m.id, m.name, m.status, m.colour, m.message, m.warnings])) + [...state.shown].join() + state.editing;
  if (sig === state.listSignature) { updateSteps(); return; }
  state.listSignature = sig;
  const area = $("runs-area");
  if (!metas.length) { area.replaceChildren(el("p", { class: "inset", text: "You have no runs yet. Go to Set up a run to start one." })); return; }
  const tbody = el("tbody");
  for (const meta of metas) tbody.append(runRow(meta));
  area.replaceChildren(el("div", { class: "table-wrap" }, el("table", { class: "runs-table" },
    el("caption", { class: "visually-hidden", text: "Your runs" }),
    el("thead", {}, el("tr", {}, el("th", { text: "Show on charts" }), el("th", { text: "Run" }), el("th", { text: "Status" }), el("th", { text: "Actions" }))),
    tbody)));
  updateSteps();
  renderDifferences();
}

function runRow(meta) {
  const run = state.runs[meta.id];
  const box = el("input", { type: "checkbox", id: "show-" + meta.id });
  box.checked = state.shown.has(meta.id);
  box.addEventListener("change", () => {
    if (box.checked) state.shown.add(meta.id); else state.shown.delete(meta.id);
    store("shown", [...state.shown]);
    state.listSignature = "";
    poll();
    scheduleCharts();
  });
  const showCell = el("td", {}, el("div", { class: "checkbox" }, box,
    el("label", { for: "show-" + meta.id }, el("span", { class: "swatch", style: `border-color: ${seriesColour(meta.colour || 0)}` }),
      el("span", { class: "visually-hidden", text: `Show ${meta.name} on the charts` }))));
  let nameCell;
  if (state.editing === meta.id) {
    const input = el("input", { class: "input", id: "rename-" + meta.id, type: "text", maxlength: "120", value: meta.name });
    const save = async () => {
      const name = input.value.trim();
      if (!name) { input.classList.add("error"); input.focus(); return; }
      try { await api(`/api/runs/${meta.id}/rename`, "POST", { name }); } catch (e) { alert(e.message); return; }
      state.editing = null; state.listSignature = ""; await poll();
    };
    input.addEventListener("keydown", e => { if (e.key === "Enter") save(); if (e.key === "Escape") { state.editing = null; state.listSignature = ""; renderRuns(); } });
    nameCell = el("td", {}, el("label", { class: "label small", for: input.id, text: "New name" }), input,
      el("div", { class: "button-group" },
        el("button", { type: "button", class: "button small", onclick: save, text: "Save name" }),
        el("button", { type: "button", class: "button secondary small", text: "Cancel", onclick: () => { state.editing = null; state.listSignature = ""; renderRuns(); } })));
    setTimeout(() => input.focus(), 0);
  } else {
    nameCell = el("td", {}, el("div", { class: "name", text: meta.name }), el("div", { class: "what", text: whatText(meta) }),
      el("div", { class: "what", text: "Started " + new Date(meta.created).toLocaleString("en-GB", { dateStyle: "medium", timeStyle: "short" }) }));
  }
  const statusCell = el("td", {}, el("span", { class: "tag " + meta.status, text: statusText(meta) }), el("div", { class: "what step-text", "data-id": meta.id }));
  if (meta.status === "failed" || (meta.warnings && meta.warnings.length) || (meta.status === "stopped" && meta.message)) {
    statusCell.append(el("details", {}, el("summary", { text: meta.status === "failed" ? "What went wrong" : "Notes" }), problemText(run)));
  }
  const actions = el("td", { class: "button-group" });
  if (meta.status === "running" || meta.status === "waiting") {
    actions.append(el("button", { type: "button", class: "button warning small", text: meta.status === "running" ? "Stop run" : "Remove from the queue",
      onclick: () => stopRun(meta) }));
  } else {
    actions.append(
      el("button", { type: "button", class: "button secondary small", text: "Rename", "aria-label": `Rename ${meta.name}`, onclick: () => { state.editing = meta.id; state.listSignature = ""; renderRuns(); } }),
      el("button", { type: "button", class: "button secondary small", text: "Use these settings", "aria-label": `Use the settings of ${meta.name} for a new run`,
        onclick: async () => { if (!run.detail) { try { run.detail = await api(`/api/runs/${meta.id}?since=999999`); } catch (e) { return; } } useSettingsOf(run); } }),
      el("a", { class: "button secondary small", href: `/api/runs/${meta.id}/csv`, download: "", "aria-label": `Download the figures of ${meta.name} as a CSV file`, text: "Download figures (CSV)" }),
      el("button", { type: "button", class: "button warning small", text: "Delete", "aria-label": `Delete ${meta.name}`, onclick: () => deleteRun(meta) }));
  }
  return el("tr", {}, showCell, nameCell, statusCell, actions);
}

function problemText(run) {
  const meta = run.meta, d = run.detail || {};
  const out = el("div", { class: "problem-box" });
  if (meta.status === "failed") {
    const where = d.error_year ? `The run stopped in the year labelled ${d.error_year}, which is year ${d.error_step} of ${meta.years}.` :
      "The run stopped before its first year.";
    out.append(el("p", {}, el("b", { text: where })));
    if (d.guard) out.append(el("p", { text: "The model stops a run when it finds a value that cannot happen, such as a negative number of employees. The message below names the modules that changed the firms concerned. A setting far from its default is the usual cause." }));
    else if (d.detail) out.append(el("p", { text: "A module could not carry on. This usually means a setting is outside the range the module can work with, or the model was being changed while the run started." }));
    out.append(el("p", { text: "The model said:" }), el("p", { class: "message", text: meta.message }));
    if (run.rows.length > 1) out.append(el("p", { text: "The figures up to that year have been kept, and you can still chart them." }));
    if (d.detail) out.append(el("details", {}, el("summary", { text: "Technical details" }), el("pre", { text: d.detail })));
  } else if (meta.message) out.append(el("p", { text: meta.message }));
  for (const w of meta.warnings || []) out.append(el("p", { text: w }));
  return out;
}

function updateSteps() {
  for (const node of document.querySelectorAll(".step-text")) {
    const r = state.runs[node.dataset.id];
    if (!r) continue;
    const m = r.meta;
    if (m.status === "running") node.textContent = `Year ${m.step} of ${m.years}`;
    else if (m.status === "stopped" || m.status === "failed") node.textContent = m.step ? `Reached year ${m.step} of ${m.years}` : "";
    else if (m.status === "waiting") node.textContent = "It starts when the run before it has finished.";
    else node.textContent = "";
  }
}

function renderProgress() {
  const area = $("progress-area");
  const metas = Object.values(state.runs).map(r => r.meta);
  const running = metas.find(m => m.status === "running");
  const waiting = metas.filter(m => m.status === "waiting");
  const kids = [];
  if (running) {
    const pct = Math.round(100 * running.step / running.years);
    const r = state.runs[running.id];
    const last = r.rows.length ? r.rows[r.rows.length - 1] : null;
    kids.push(el("div", { class: "progress-box" },
      el("p", {}, el("b", { text: `Running "${running.name}": year ${running.step} of ${running.years}` }), last ? ` (the year labelled ${last.year})` : ""),
      el("progress", { max: running.years, value: running.step, "aria-label": `Progress of ${running.name}` }, `${pct}%`),
      el("p", { class: "hint", text: "You can keep using the page while the model runs." }),
      el("button", { type: "button", class: "button warning", text: "Stop run", onclick: () => stopRun(running) })));
  }
  if (waiting.length) kids.push(el("p", { text: `${plural(waiting.length, "run is", "runs are")} waiting to start: ${listWords(waiting.map(w => `"${w.name}"`))}.` }));
  const lastId = state.lastStarted;
  if (lastId && state.runs[lastId] && state.runs[lastId].meta.status === "failed") {
    const r = state.runs[lastId];
    kids.push(el("div", {}, el("h3", { text: `"${r.meta.name}" stopped because of an error` }), problemText(r)));
  }
  const sig = JSON.stringify([running && running.id, running && running.step, waiting.map(w => w.id), lastId && state.runs[lastId] && state.runs[lastId].meta.status, lastId && state.runs[lastId] && !!state.runs[lastId].detail]);
  if (area.dataset.sig !== sig) { area.dataset.sig = sig; area.replaceChildren(...kids); }
}

async function stopRun(meta) {
  try { await api(`/api/runs/${meta.id}/stop`, "POST", {}); } catch (e) { alert(e.message); }
  poll();
}
async function deleteRun(meta) {
  if (!confirm(`Delete the run "${meta.name}"? This cannot be undone.`)) return;
  try { await api(`/api/runs/${meta.id}/delete`, "POST", {}); } catch (e) { alert(e.message); return; }
  delete state.runs[meta.id];
  state.shown.delete(meta.id);
  store("shown", [...state.shown]);
  state.listSignature = "";
  poll();
  scheduleCharts();
}

function shownRuns() {
  return Object.values(state.runs).filter(r => state.shown.has(r.meta.id)).sort((a, b) => a.meta.created < b.meta.created ? -1 : 1);
}

// ---------------------------------------------------------------- differences between runs

function titleOf(modId) {
  const m = state.modules[modId];
  return m ? moduleLabel(m) : humanise(modId.slice(modId.indexOf(":") + 1));
}

function renderDifferences() {
  const area = $("differences-area");
  const runs = shownRuns();
  if (runs.length < 2) { area.replaceChildren(); return; }
  if (runs.some(r => !r.detail)) { area.replaceChildren(el("p", { class: "hint", text: "Reading the settings of the runs you ticked…" })); return; }
  const rows = [];
  const same = vals => vals.every(v => JSON.stringify(v) === JSON.stringify(vals[0]));
  const basic = [["Number of claims", r => r.meta.claims.toLocaleString("en-GB")], ["Years", r => r.meta.years], ["Seed", r => r.meta.seed]];
  for (const [label, f] of basic) { const vals = runs.map(f); if (!same(vals)) rows.push([label, vals]); }
  const used = runs.map(r => r.detail.settings_used || {});
  const ids = [...new Set(used.flatMap(u => Object.keys(u)))].sort();
  for (const id of ids) {
    const on = used.map(u => id in u);
    if (!same(on)) rows.push([`${titleOf(id)} (${id.slice(id.indexOf(":") + 1)})`, on.map(x => x ? "On" : "Off")]);
    const names = [...new Set(used.flatMap(u => Object.keys(u[id] || {})))];
    for (const name of names) {
      const vals = used.map(u => (u[id] && name in u[id]) ? u[id][name] : undefined);
      const present = vals.filter(v => v !== undefined);
      if (present.length > 1 && !same(present)) {
        rows.push([`${titleOf(id)}: ${humanise(name).toLowerCase()} (${name})`, vals.map(v => v === undefined ? "Module off" : Array.isArray(v) ? v.join(", ") : String(v))]);
      }
    }
  }
  const kids = [el("h3", { text: "What is different between the runs you ticked" })];
  if (!rows.length) {
    kids.push(el("p", { text: "These runs have the same settings. They can still differ if the model itself was changed between the times they were run." }));
  } else {
    kids.push(el("div", { class: "table-wrap" }, el("table", { class: "diff-table" },
      el("thead", {}, el("tr", {}, el("th", { text: "What differs" }), ...runs.map(r => el("th", {}, el("span", { class: "swatch", style: `border-color: ${seriesColour(r.meta.colour || 0)}` }), r.meta.name)))),
      el("tbody", {}, ...rows.map(([label, vals]) => el("tr", {}, el("th", { text: label }), ...vals.map(v => el("td", { text: String(v) }))))))));
    kids.push(el("p", { class: "hint", text: "Only differences are listed. Runs made on different days can also differ because the model was changed in between." }));
  }
  area.replaceChildren(...kids);
}

// ---------------------------------------------------------------- charts

let chartTimer = null;
function scheduleCharts() { clearTimeout(chartTimer); chartTimer = setTimeout(drawAllCharts, 60); }

function metaOf(key) {
  const m = MAIN.find(x => x.key === key);
  if (m) return m;
  const notes = (state.cat && state.cat.readout_notes) || {};
  const name = NAMES[key] || humanise(key);
  const note = notes[key] ? notes[key].charAt(0).toUpperCase() + notes[key].slice(1) + "." : "";
  const pct = PCT_KEYS.has(key);
  return { key, title: name, unit: pct ? "pct" : "num", axis: pct ? "Per cent" : "Value", explain: note, log: !pct, code: key };
}

function allKeys() {
  const keys = new Set();
  for (const r of Object.values(state.runs)) for (const row of r.rows) for (const k of Object.keys(row.values)) keys.add(k);
  return keys;
}

function fillExtraSelect() {
  const sel = $("extra-select");
  const keys = [...allKeys()].filter(k => !MAIN_KEYS.has(k));
  const opts = keys.map(k => [k, metaOf(k).title]).sort((a, b) => a[1].localeCompare(b[1]));
  const current = sel.value;
  sel.replaceChildren(...(opts.length ? opts.map(([k, t]) => el("option", { value: k, text: `${t}${NAMES[k] ? "" : ""}` })) : [el("option", { value: "", text: "No figures yet. Start a run first." })]));
  if (current && keys.includes(current)) sel.value = current;
}

function seriesFor(key) {
  const runs = shownRuns();
  const dashCount = {};
  return runs.map(r => {
    const slot = r.meta.colour || 0;
    const nth = dashCount[slot % 8] = (dashCount[slot % 8] || 0) + 1;
    return {
      label: r.meta.name, colour: seriesColour(slot), dash: nth > 1 ? "7 4" : null,
      pts: r.rows.map(row => [row.year, row.values[key]]).filter(p => p[1] !== undefined),
    };
  });
}

function chartCard(meta, removable) {
  const box = el("div", { class: "chart-box" });
  const card = el("div", { class: "chart-card" },
    el("h5", { text: meta.title }),
    meta.explain ? el("p", { class: "explain", text: meta.explain }) : null,
    meta.code ? el("p", { class: "explain", text: `Name in the model: ${meta.code}` }) : null);
  const tools = el("div", { class: "chart-tools" });
  if (meta.log) {
    const id = "log-" + meta.key;
    const cb = el("input", { type: "checkbox", id });
    cb.checked = state.logCharts.has(meta.key);
    cb.addEventListener("change", () => { if (cb.checked) state.logCharts.add(meta.key); else state.logCharts.delete(meta.key); store("log", [...state.logCharts]); drawAllCharts(); });
    tools.append(el("div", { class: "checkbox" }, cb, el("label", { for: id, text: "Use a log scale (equal steps up mean equal percentage rises)" })));
  }
  if (removable) tools.append(el("button", { type: "button", class: "button secondary small", text: "Remove chart", "aria-label": `Remove the chart of ${meta.title}`,
    onclick: () => { state.extra = state.extra.filter(k => k !== meta.key); store("extra", state.extra); drawAllCharts(); } }));
  card.append(tools, box);
  const legend = el("ul", { class: "legend" });
  const table = el("details", {}, el("summary", { text: "Show the figures as a table" }));
  card.append(legend, table);
  return { card, box, legend, table };
}

function drawAllCharts() {
  if ($("panel-results").hidden) return;
  const runs = shownRuns();
  $("charts-empty").hidden = runs.length > 0;
  const keys = allKeys();
  const main = $("main-charts");
  main.replaceChildren();
  for (const meta of MAIN) {
    if (runs.length && !runs.some(r => r.rows.some(row => meta.key in row.values))) continue;
    if (!runs.length && !keys.has(meta.key)) continue;
    const c = chartCard(meta, false);
    main.append(c.card);
    drawSeriesChart(c, meta, seriesFor(meta.key));
  }
  const extra = $("extra-charts");
  extra.replaceChildren();
  for (const key of state.extra) {
    const meta = metaOf(key);
    const c = chartCard(meta, true);
    extra.append(c.card);
    drawSeriesChart(c, meta, seriesFor(key));
  }
  drawGain();
}

function drawSeriesChart(c, meta, series) {
  const useLog = meta.log && state.logCharts.has(meta.key);
  c.legend.replaceChildren(...series.map(s => el("li", {}, el("span", { class: "swatch" + (s.dash ? " dash" : ""), style: `border-color: ${s.colour}` }), s.label)));
  if (series.length < 2) c.legend.hidden = true;
  if (!series.length || series.every(s => !s.pts.some(p => p[1] !== null))) {
    c.box.replaceChildren(el("p", { class: "empty-chart", text: series.length ? "There are no figures for this yet." : "Tick a run in the list of runs to show it here." }));
    c.table.hidden = true;
    return;
  }
  lineChart(c.box, { title: meta.title, series, unit: meta.unit, yTitle: meta.axis, log: useLog, fixed: meta.fixed });
  c.table.hidden = false;
  c.table.addEventListener("toggle", () => { if (c.table.open && !c.table.querySelector("table")) c.table.append(dataTable(series, meta.unit)); });
}

function dataTable(series, unit) {
  const years = [...new Set(series.flatMap(s => s.pts.map(p => p[0])))].sort((a, b) => a - b);
  const maps = series.map(s => new Map(s.pts));
  return el("div", { class: "data-scroll", tabindex: "0" }, el("table", { class: "data-table" },
    el("thead", {}, el("tr", {}, el("th", { text: "Year label" }), ...series.map(s => el("th", { text: s.label })))),
    el("tbody", {}, ...years.map(y => el("tr", {}, el("td", { text: y }), ...maps.map(m => el("td", { text: m.has(y) ? fmtValue(m.get(y), unit) : "" })))))));
}

function niceStep(range, target) {
  const raw = range / Math.max(1, target);
  const mag = Math.pow(10, Math.floor(Math.log10(raw)));
  const n = raw / mag;
  return (n < 1.5 ? 1 : n < 3 ? 2 : n < 7 ? 5 : 10) * mag;
}
function tickLabel(v, unit, step) {
  if (unit === "pct") {
    const d = Math.max(0, -Math.floor(Math.log10(step * 100) + 1e-9));
    return (v * 100).toLocaleString("en-GB", { minimumFractionDigits: Math.min(d, 2), maximumFractionDigits: Math.min(d, 2) }) + "%";
  }
  const d = Math.max(0, -Math.floor(Math.log10(step) + 1e-9));
  return v.toLocaleString("en-GB", { minimumFractionDigits: Math.min(d, 4), maximumFractionDigits: Math.min(d, 4) });
}

function lineChart(box, cfg) {
  const W = Math.max(320, box.clientWidth || 600);
  const H = 300;
  const narrow = W < 560;
  const direct = !narrow && cfg.series.length >= 2 && cfg.series.length <= 4;
  const m = { l: 70, r: direct ? 120 : 18, t: 12, b: 52 };
  const all = cfg.series.flatMap(s => s.pts.filter(p => p[1] !== null && isFinite(p[1])));
  let xs = all.map(p => p[0]);
  let x0 = Math.min(...xs), x1 = Math.max(...xs);
  if (x0 === x1) { x0 -= 1; x1 += 1; }
  let ys = all.map(p => p[1]);
  let log = cfg.log && ys.every(v => v > 0);
  let y0 = Math.min(...ys), y1 = Math.max(...ys);
  if (cfg.fixed && !log) { y0 = Math.min(y0, cfg.fixed[0]); y1 = Math.max(y1, cfg.fixed[1]); }
  let ticks = [];
  let ty;
  if (log) {
    let l0 = Math.log10(y0), l1 = Math.log10(y1);
    if (l1 - l0 < 0.3) { l0 -= 0.15; l1 += 0.15; }
    const lo = Math.floor(l0), hi = Math.ceil(l1);
    for (let e = lo; e <= hi; e++) for (const k of [1, 2, 5]) { const v = k * Math.pow(10, e); if (v >= Math.pow(10, l0) * 0.999 && v <= Math.pow(10, l1) * 1.001) ticks.push(v); }
    if (hi - lo > 3) ticks = ticks.filter(v => Math.abs(Math.log10(v) - Math.round(Math.log10(v))) < 1e-9);
    if (ticks.length < 2) ticks = [Math.pow(10, l0), Math.pow(10, l1)];
    ty = v => m.t + (H - m.t - m.b) * (1 - (Math.log10(v) - l0) / (l1 - l0));
  } else {
    if (y0 === y1) { const pad = Math.abs(y0) * 0.1 || 0.1; y0 -= pad; y1 += pad; }
    if (y0 > 0 && y0 < (y1 - y0) * 0.5) y0 = 0;           // start at zero where that costs little
    if (y1 < 0 && -y1 < (y1 - y0) * 0.5) y1 = 0;
    const step = niceStep(y1 - y0, 5);
    const lo = Math.floor(y0 / step + 1e-9) * step, hi = Math.ceil(y1 / step - 1e-9) * step;
    y0 = lo; y1 = hi;
    for (let v = lo; v <= hi + step * 0.5; v += step) ticks.push(Math.abs(v) < step * 1e-9 ? 0 : v);
    ty = v => m.t + (H - m.t - m.b) * (1 - (v - y0) / (y1 - y0));
    ticks.step = step;
  }
  const tx = v => m.l + (W - m.l - m.r) * (v - x0) / (x1 - x0);
  const s = svg("svg", { viewBox: `0 0 ${W} ${H}`, width: W, height: H, role: "img", tabindex: "0",
    "aria-label": firmify(`${cfg.title}. Chart of ${cfg.series.map(x => x.label).join(", ")}. Use the left and right arrow keys to read the figures year by year.`) });
  // grid and y ticks
  const tstep = ticks.step || null;
  for (const v of ticks) {
    const y = ty(v);
    s.append(svg("line", { x1: m.l, x2: W - m.r, y1: y, y2: y, class: v === 0 ? "zero" : "grid" }));
    const t = svg("text", { x: m.l - 8, y: y + 4, "text-anchor": "end" });
    t.textContent = log ? (cfg.unit === "pct" ? fmtValue(v, "pct") : fmtNumber(v)) : tickLabel(v, cfg.unit, tstep);
    s.append(t);
  }
  // x ticks
  const xstep = niceStep(x1 - x0, narrow ? 4 : 8);
  for (let v = Math.ceil(x0 / xstep) * xstep; v <= x1; v += xstep) {
    const x = tx(v);
    s.append(svg("line", { x1: x, x2: x, y1: H - m.b, y2: H - m.b + 5, class: "axis" }));
    const t = svg("text", { x, y: H - m.b + 20, "text-anchor": "middle" });
    t.textContent = String(Math.round(v));
    s.append(t);
  }
  s.append(svg("line", { x1: m.l, x2: W - m.r, y1: H - m.b, y2: H - m.b, class: "axis" }));
  const xt = svg("text", { x: m.l + (W - m.l - m.r) / 2, y: H - 8, "text-anchor": "middle", class: "axis-title" });
  xt.textContent = "Year label, counted from a start labelled " + (state.cat && state.cat.start_year != null ? state.cat.start_year : "1890");
  s.append(xt);
  const yt = svg("text", { x: 14, y: m.t + (H - m.t - m.b) / 2, "text-anchor": "middle", class: "axis-title", transform: `rotate(-90 14 ${m.t + (H - m.t - m.b) / 2})` });
  yt.textContent = firmify(cfg.yTitle + (log ? " (log scale)" : ""));
  s.append(yt);
  // lines
  const ends = [];
  for (const ser of cfg.series) {
    let d = "", pen = false;
    for (const [x, y] of ser.pts) {
      if (y === null || !isFinite(y) || (log && y <= 0)) { pen = false; continue; }
      d += (pen ? "L" : "M") + tx(x).toFixed(1) + " " + ty(y).toFixed(1);
      pen = true;
    }
    const p = svg("path", { d, class: "series", stroke: ser.colour });
    if (ser.dash) p.setAttribute("stroke-dasharray", ser.dash);
    s.append(p);
    const last = [...ser.pts].reverse().find(q => q[1] !== null && isFinite(q[1]) && (!log || q[1] > 0));
    if (last) ends.push({ x: tx(last[0]), y: ty(last[1]), label: ser.label });
  }
  if (direct) {
    ends.sort((a, b) => a.y - b.y);
    for (let i = 1; i < ends.length; i++) if (ends[i].y - ends[i - 1].y < 15) ends[i].y = ends[i - 1].y + 15;
    for (const e of ends) {
      const t = svg("text", { x: e.x + 8, y: e.y + 4, class: "end-label" });
      const label = firmify(e.label);
      t.textContent = label.length > 16 ? label.slice(0, 15) + "…" : label;
      s.append(t);
    }
  }
  // hover and keyboard reading
  const years = [...new Set(all.map(p => p[0]))].sort((a, b) => a - b);
  const maps = cfg.series.map(ser => new Map(ser.pts));
  const cross = svg("line", { y1: m.t, y2: H - m.b, class: "cross", visibility: "hidden" });
  s.append(cross);
  const dots = cfg.series.map(ser => { const c = svg("circle", { r: 4.5, fill: ser.colour, stroke: cssVar("--surface"), "stroke-width": 2, visibility: "hidden" }); s.append(c); return c; });
  const tip = el("div", { class: "tooltip", hidden: true, "aria-live": "polite" });
  let idx = -1;
  const show = i => {
    if (!years.length) return;
    idx = Math.max(0, Math.min(years.length - 1, i));
    const yr = years[idx], x = tx(yr);
    cross.setAttribute("x1", x); cross.setAttribute("x2", x); cross.setAttribute("visibility", "visible");
    const rows = [el("div", { class: "t-year", text: `Year labelled ${yr}` })];
    cfg.series.forEach((ser, k) => {
      const v = maps[k].get(yr);
      const ok = v !== undefined && v !== null && isFinite(v) && (!log || v > 0);
      dots[k].setAttribute("visibility", ok ? "visible" : "hidden");
      if (ok) { dots[k].setAttribute("cx", x); dots[k].setAttribute("cy", ty(v)); }
      rows.push(el("div", { class: "t-row" }, el("span", {}, el("span", { class: "swatch" + (ser.dash ? " dash" : ""), style: `border-color: ${ser.colour}; width: 16px` }), ser.label),
        el("b", { text: v === undefined ? "no figure" : fmtValue(v, cfg.unit) })));
    });
    tip.replaceChildren(...rows);
    tip.hidden = false;
    const scale = box.clientWidth / W;
    const left = x * scale;
    tip.style.top = "8px";
    if (left > box.clientWidth / 2) { tip.style.left = ""; tip.style.right = (box.clientWidth - left + 12) + "px"; }
    else { tip.style.right = ""; tip.style.left = (left + 12) + "px"; }
  };
  const hide = () => { tip.hidden = true; cross.setAttribute("visibility", "hidden"); dots.forEach(d => d.setAttribute("visibility", "hidden")); };
  s.addEventListener("pointermove", e => {
    const rect = s.getBoundingClientRect();
    const x = (e.clientX - rect.left) * W / rect.width;
    if (x < m.l - 10 || x > W - m.r + 10) { hide(); return; }
    const yr = x0 + (x - m.l) / (W - m.l - m.r) * (x1 - x0);
    let best = 0;
    for (let i = 0; i < years.length; i++) if (Math.abs(years[i] - yr) < Math.abs(years[best] - yr)) best = i;
    show(best);
  });
  s.addEventListener("pointerleave", hide);
  s.addEventListener("blur", hide);
  s.addEventListener("keydown", e => {
    if (e.key === "ArrowRight") { e.preventDefault(); show(idx < 0 ? 0 : idx + 1); }
    else if (e.key === "ArrowLeft") { e.preventDefault(); show(idx < 0 ? years.length - 1 : idx - 1); }
    else if (e.key === "Home") { e.preventDefault(); show(0); }
    else if (e.key === "End") { e.preventDefault(); show(years.length - 1); }
    else if (e.key === "Escape") hide();
  });
  box.replaceChildren(s, tip);
}

// ---------------------------------------------------------------- gain by source

function sourceLabel(src) {
  if (SOURCE_NAMES[src]) return `${SOURCE_NAMES[src]} (${src})`;
  const m = Object.values(state.modules).find(x => x.name === src || x.model_name === src);
  if (m && m.title && m.title.toLowerCase() !== src.toLowerCase()) return `${m.title} (${src})`;
  return humanise(src);
}

function drawGain() {
  const area = $("gain-area");
  const runs = shownRuns();
  const intro = el("p", { text: "Each year differential capitalization rises or falls. This chart shows which modules moved it, and by how much. A line above zero means the module helped the top hundred pull ahead of the average that year. A line below zero means it held them back." });
  if (!runs.length) { area.replaceChildren(intro, el("p", { class: "inset", text: "Tick a run in the list of runs to show it here." })); return; }
  if (!runs.some(r => r.meta.id === state.gainRun)) state.gainRun = runs[runs.length - 1].meta.id;
  const run = state.runs[state.gainRun];
  const sel = el("select", { class: "select", id: "gain-run" }, ...runs.map(r => el("option", { value: r.meta.id, text: r.meta.name })));
  sel.value = state.gainRun;
  sel.addEventListener("change", () => { state.gainRun = sel.value; drawGain(); $("gain-run").focus(); });
  const modes = el("div", { class: "chart-tools", role: "radiogroup", "aria-label": "How to show the gain" });
  for (const [v, text] of [["year", "Each year"], ["total", "Added up since the start"]]) {
    const r = el("input", { type: "radio", name: "gain-mode", id: "gain-" + v, value: v });
    r.checked = state.gainMode === v;
    r.addEventListener("change", () => { state.gainMode = v; store("gainMode", v); drawGain(); $("gain-" + v).focus(); });
    modes.append(el("div", { class: "radio" }, r, el("label", { for: "gain-" + v, text })));
  }
  const rows = run.rows.filter(r => r.step > 0);
  const totals = {};
  for (const row of rows) for (const [k, v] of Object.entries(row.gain)) if (v !== null) totals[k] = (totals[k] || 0) + v;
  const order = Object.keys(totals).sort((a, b) => Math.abs(totals[b]) - Math.abs(totals[a]));
  const keep = order.length > 8 ? order.slice(0, 7) : order;
  const rest = order.filter(k => !keep.includes(k));
  const groups = keep.map((k, i) => ({ label: sourceLabel(k), colour: seriesColour(i), keys: [k] }));
  if (rest.length) groups.push({ label: `All other sources (${rest.length})`, colour: cssVar("--other"), keys: rest, dash: "6 4" });
  const series = groups.map(g => {
    let sum = 0;
    return { label: g.label, colour: g.colour, dash: g.dash || null, pts: rows.map(row => {
      const v = g.keys.reduce((a, k) => a + (row.gain[k] || 0), 0);
      sum += v;
      return [row.year, state.gainMode === "total" ? sum : v];
    }) };
  });
  const card = el("div", { class: "chart-card" });
  card.append(el("h5", { text: `Gain by source: ${run.meta.name}` }));
  const mostUp = order.filter(k => totals[k] > 0)[0], mostDown = order.filter(k => totals[k] < 0)[0];
  const lines = [];
  if (mostUp) lines.push(`Over the run so far, ${sourceLabel(mostUp)} added the most (${fmtValue(totals[mostUp], "gain")}).`);
  if (mostDown) lines.push(`${sourceLabel(mostDown)} took away the most (${fmtValue(totals[mostDown], "gain")}).`);
  if (lines.length) card.append(el("p", {}, el("b", { text: lines.join(" ") })));
  card.append(el("p", { class: "explain", text: state.gainMode === "total"
    ? "Added up since the start. A total of 0.69 means the module on its own doubled differential capitalization. A total of −0.69 means it halved it."
    : "The change is measured on a log scale. For small values it is close to a percentage change: 0.05 means the module raised differential capitalization by about 5% that year." }));
  card.append(el("div", { class: "field inline-field" }, el("label", { class: "label small", for: "gain-run", text: "Run" }), sel), modes);
  const box = el("div", { class: "chart-box" });
  const legend = el("ul", { class: "legend" }, ...series.map(s => el("li", {}, el("span", { class: "swatch" + (s.dash ? " dash" : ""), style: `border-color: ${s.colour}` }), s.label)));
  const table = el("details", {}, el("summary", { text: "Show the figures as a table" }));
  card.append(box, legend, table);
  if (rest.length) card.append(el("p", { class: "explain", text: `"All other sources" adds up ${listWords(rest.map(sourceLabel))}.` }));
  area.replaceChildren(intro, card);
  if (!series.length || !rows.length) { box.replaceChildren(el("p", { class: "empty-chart", text: "There are no figures for this yet." })); return; }
  lineChart(box, { title: "Gain by source", series, unit: "gain", yTitle: state.gainMode === "total" ? "Change added up (log scale units)" : "Change in the year (0.01 is about 1%)" });
  table.addEventListener("toggle", () => { if (table.open && !table.querySelector("table")) table.append(dataTable(series, "gain")); });
}

// ---------------------------------------------------------------- start

function init() {
  showTab = setupTabs();
  renderGlossary();
  for (const r of document.querySelectorAll('input[name="claims"]')) r.addEventListener("change", () => {
    $("claims-other-box").hidden = !$("claims-other").checked;
    updateRunSummary();
  });
  for (const id of ["years", "claims-number", "seed"]) $(id).addEventListener("input", updateRunSummary);
  $("module-filter").addEventListener("input", applyFilter);
  $("start-run").addEventListener("click", startRun);
  $("reset-settings").addEventListener("click", resetSettings);
  $("reload-catalogue").addEventListener("click", () => loadCatalogue(true));
  $("add-chart").addEventListener("click", () => {
    const k = $("extra-select").value;
    if (k && !state.extra.includes(k)) { state.extra.push(k); store("extra", state.extra); drawAllCharts(); }
  });
  let lastW = window.innerWidth;
  window.addEventListener("resize", () => { if (Math.abs(window.innerWidth - lastW) > 40) { lastW = window.innerWidth; scheduleCharts(); } });
  window.matchMedia("(prefers-color-scheme: dark)").addEventListener("change", () => { state.listSignature = ""; renderRuns(); scheduleCharts(); });
  loadCatalogue(false);
  poll(true);
}
document.addEventListener("DOMContentLoaded", init);
