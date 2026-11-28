"""Three ways to start a run.

- stated: conditions the model states for itself. Many small firms of similar size, as in what the
  book calls "the golden age of 'free competition'" (chapter 12). Years are counted from 0.
  With draws on, each seed takes the unemployment, the growth of the working population and the
  organised part of employees of one year picked at random from the US data of 1950 to 2025.
- 1950: the conditions of the United States in 1950, from the files in data/.
- present: the conditions of the United States in the last five years of data, from data/.

Only the starting point of a historical start is historical. Every later year is made by the modules.

The figures a start takes are states: how many people are out of work, how fast the working
population grows, how many employees are organised, and how firms differ in size. Results, such as
the capitalist share of income, differential capitalization and the pace of mergers, are not fed in.
`compare` gives the figures in the data that a run can be set against.
"""
import csv
from pathlib import Path
import numpy as np
from core import Ledger
from modules.sabotage import Sabotage

DATA = Path(__file__).resolve().parent / "data"
COUNT = 300_000      # firms in a run unless the run says otherwise
NAMES = ("stated", "1950", "present")
PRESENT = range(2021, 2026)   # the last five years of data
SIZES_YEAR = 2023             # the last year of the Census table of firm sizes


def series(name, column):
    """One column of a file in data/, as {year: value}, leaving out blank cells."""
    with open(DATA / f"{name}.csv", newline="", encoding="utf-8") as f:
        return {int(row["year"]): float(row[column]) for row in csv.DictReader(f) if row[column] != ""}


def organised():
    """Union members as a part of wage and salary workers: Mayer (2004) to 1981, the BLS from 1983."""
    mayer = series("union_membership", "pct_wage_salary_mayer")
    bls = series("union_membership", "pct_wage_salary_bls")
    return {**{y: v for y, v in mayer.items() if y < 1983}, **bls}


def us_conditions():
    """Unemployment, growth of the labour force and the organised part of employees, by year, as parts of 1."""
    u = series("unemployment", "unemployment_pct")
    g = series("labour_force", "growth_pct")
    o = organised()
    return {y: {"unemployment": u[y] / 100, "growth": g[y] / 100, "organised": o[y] / 100}
            for y in sorted(set(u) & set(g) & set(o)) if y >= 1950}


def size_classes(year=SIZES_YEAR):
    """The Census table of employer firms by size for one year: (lowest, highest or None, firms, employees)."""
    out = []
    with open(DATA / "firm_sizes.csv", newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if int(row["year"]) != year:
                continue
            band = row["employees_per_firm"]
            lo, hi = (int(band[:-1]), None) if band.endswith("+") else map(int, band.split(" to "))
            out.append((lo, hi, int(row["firms"]), int(row["employees"])))
    return out


def census_sizes(rng, count, year=SIZES_YEAR):
    """Employees of `count` firms drawn with the spread of sizes of US employer firms in one year.

    Each firm falls in a size class with the part of firms the Census counts in it. Inside a class
    of fixed bounds, its size is drawn evenly on a log scale between them. Inside the open top class,
    it is drawn from a Pareto curve whose mean is that class's employees for each firm."""
    classes = size_classes(year)
    firms = np.array([c[2] for c in classes], float)
    which = rng.choice(len(classes), size=count, p=firms / firms.sum())
    sizes = np.empty(count)
    for i, (lo, hi, n, e) in enumerate(classes):
        here = which == i
        k = int(here.sum())
        if hi is not None:
            sizes[here] = np.exp(rng.uniform(np.log(lo), np.log(hi + 1), k))
        else:
            mean = e / n
            shape = mean / (mean - lo)       # a Pareto curve from `lo` with this mean
            sizes[here] = lo * (1 - rng.random(k)) ** (-1 / shape)
    return sizes


def conditions(name="stated", seed=0, draws=False):
    """The conditions of a start, as a dict. `year` is the label of the starting year (0 for stated)."""
    if name not in NAMES:
        raise ValueError(f"No start is called '{name}'. The starts are {', '.join(NAMES)}.")
    sab = Sabotage()
    if name == "stated":
        c = {"name": name, "year": 0, "unemployment": sab.labour_holds_at, "growth": 0.017,
             "organised": None, "sizes": "stated", "drawn_from": None}
        if draws:
            us = us_conditions()
            year = sorted(us)[np.random.default_rng([seed, 57]).integers(len(us))]
            c.update(us[year], drawn_from=year)
        return c
    us = us_conditions()
    if name == "1950":
        return {"name": name, "year": 1950, **us[1950], "sizes": "stated", "drawn_from": None}
    mean = {k: float(np.mean([us[y][k] for y in PRESENT])) for k in ("unemployment", "growth", "organised")}
    return {"name": name, "year": PRESENT[-1], **mean, "sizes": SIZES_YEAR, "drawn_from": None}


def starting_ledger(seed=0, count=None, industries=400, sectors=20, start=None):
    """The firms and shared figures of the first year. `start` is a dict from `conditions`."""
    count = count or COUNT
    start = start or conditions()
    rng = np.random.default_rng(seed)
    if start["sizes"] == "stated":
        employees = rng.lognormal(np.log(100), 0.8, count)    # many small firms of similar size
    else:
        employees = census_sizes(rng, count, start["sizes"])
    sab = Sabotage()
    return Ledger(employees=employees, epe=sab.normal_markup, risk=2.0,
                  industry=rng.integers(0, industries, count),
                  sector_of_industry=np.arange(industries) % sectors,
                  shared={"workforce": employees.sum() / (1 - start["unemployment"]),
                          "workforce_growth": start["growth"], "perm_sector": 0.0, "perm_nation": 0.0})


def apply(start, modules):
    """Set the settings of modules that a start fixes. The labour module starts from the organised part."""
    if start.get("organised") is None:
        return
    for m in modules:
        if getattr(m, "name", None) == "labour":
            m.start_level = start["organised"]


def compare(start):
    """Figures in the data for the starting year that a run produces and can be set against."""
    if start["name"] == "stated":
        return {}
    share = series("capitalist_share", "capitalist_share_pct")
    profit = series("dominant_capital", "diff_net_profit_top100_vs_all")
    years = [1950] if start["name"] == "1950" else list(PRESENT)
    got = lambda s: [s[y] for y in years if y in s]
    corporations = series("corporations", "corporations")
    part = series("dominant_capital", "profit_share_top100_pct_5y")
    out = {"capitalist share of income": float(np.mean(got(share))) / 100}
    if start["name"] == "1950":
        out["corporations"] = corporations[1950]
        out["net profit of the 100 largest against the average corporation"] = profit[1950]
        out["part of all profit earned by the 100 largest (1954, the first year)"] = part[min(part)] / 100
    else:
        five = series("dominant_capital", "diff_net_profit_top100_vs_all_5y")
        out["corporations"] = corporations[max(corporations)]
        out["net profit of the 100 largest against the average corporation"] = five[max(five)]
        out["part of all profit earned by the 100 largest"] = part[max(part)] / 100
    return out
