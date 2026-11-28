"""How close a run comes to US data.

Each test sets one figure that a run produces beside the same figure in published data. The run's
figure is taken over its last `WINDOW` years. The data give a typical value, the mean of the
years they cover, and a range: the middle half of those years, from the lowest quarter to the
highest quarter. Where a source gives only two figures, the range runs from one to the other.

The figures here are results. No module reads them, and none of them is fed into a run.

To add a test, add one entry to TESTS. The workbench reads this list each time its page loads,
so a new test appears there without any change to the workbench.

Each entry has:

    key       a short name
    label     what the figure is called on screen
    unit      share, rate or number
    model     what the run's figure measures, in one sentence
    data      what the published figure measures, in one sentence
    source    where the published figure comes from
    us        the typical value in the data, or None
    low, high the range in the data
    range     what the range is, if it is not the middle half of the years
    span      the years the data cover
    yearly    a function of one year of a run that returns (part, whole); the run's figure is the
              sum of the parts over the window divided by the sum of the wholes, so that a year
              with a small whole does not swamp the others

`python scorecard.py` prints the tests and the data.
"""
import csv
from pathlib import Path
import numpy as np

DATA = Path(__file__).resolve().parent / "data"
WINDOW = 20                    # the last years of a run that a test looks at


def column(name, col, first=None, last=None):
    """One column of a file in data/, as {year: value}, leaving out blank cells."""
    key = "birth_year" if name == "firm_survival" else "year"
    out = {}
    with open(DATA / f"{name}.csv", newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            y = int(row[key])
            if row[col] != "" and (first is None or y >= first) and (last is None or y <= last):
                out[y] = float(row[col])
    return out


def spread(values, scale=1.0):
    """The mean and the middle half of a list of yearly values."""
    v = np.array(list(values)) * scale
    return float(v.mean()), float(np.quantile(v, 0.25)), float(np.quantile(v, 0.75))


def published(year, key):
    """A number a module published in this year of a run, or 0 if no module did."""
    return float(year["published"].get(key, 0.0) or 0.0)


def account(year, key):
    """A figure of the sales account in this year of a run, or None if the sales module is not in the run."""
    acc = year["published"].get("sales_account") or {}
    return acc.get(key)


def kept(year):
    inc = account(year, "owners_income")
    return None if inc is None else (account(year, "kept"), inc)


def borrowed(year):
    inc = account(year, "owners_income")
    return None if inc is None else (account(year, "borrowed_by_government"), inc)


def closing(year):
    if "failures" not in year["published"]:
        return None
    closed = published(year, "failures")
    return closed, year["firms"] + closed


def surviving(year):
    founded = year.get("founded_five_years_before")
    if not founded:
        return None
    return published(year, "five_year_survivors"), founded


def zombies(year):
    if "zombie_share" not in year["published"]:
        return None
    return published(year, "zombie_share"), 1.0


def make_tests():
    share = spread(column("capitalist_share", "capitalist_share_pct", 1950).values(), 0.01)
    unemp = spread(column("unemployment", "unemployment_pct", 1950).values(), 0.01)
    k = spread(column("kept_and_borrowed", "kept_part", 1960, 2019).values())
    g = spread(column("kept_and_borrowed", "government_borrowed_part", 1960, 2019).values())
    d = column("firm_deaths", "death_rate")
    s = column("firm_survival", "survival_5_years")
    return [
        dict(key="capitalist_share", label="Capitalist share of income", unit="share",
             model="Owners' earnings as a part of all income, each income counted once.",
             data="Corporate profit with inventory and capital consumption adjustments, plus net interest, as a part of "
                  "national income. This is the measure of the book's Figure 12.2.",
             source="Bureau of Economic Analysis, series A051RC, W255RC and A032RC, in data/capitalist_share.csv.",
             us=share[0], low=share[1], high=share[2], span="1950 to 2025",
             yearly=lambda y: (y["capital_share"], 1.0)),
        dict(key="unemployment", label="Unemployment", unit="share",
             model="People without paid work as a part of the working population, as the model reports it.",
             data="The civilian unemployment rate.",
             source="Bureau of Labor Statistics, series UNRATE, in data/unemployment.csv.",
             us=unemp[0], low=unemp[1], high=unemp[2], span="1950 to 2025",
             yearly=lambda y: (y["unemployment"], 1.0)),
        dict(key="kept", label="What firms keep of owners' income", unit="share",
             model="Owners' income less what firms paid out to owners, from the sales account, as a part of owners' income.",
             data="The net saving of domestic business, as a part of corporate profit before tax plus net interest.",
             source="Bureau of Economic Analysis, series A127RC, A053RC and W255RC, in data/kept_and_borrowed.csv.",
             us=k[0], low=k[1], high=k[2], span="1960 to 2019", yearly=kept),
        dict(key="borrowed", label="What the government borrows", unit="share",
             model="What owners lent the government less what it repaid them, from the sales account, as a part of owners' income.",
             data="The net borrowing of government at all levels, as a part of corporate profit before tax plus net interest.",
             source="Bureau of Economic Analysis, series A922RC, A053RC and W255RC, in data/kept_and_borrowed.csv.",
             us=g[0], low=g[1], high=g[2], span="1960 to 2019", yearly=borrowed),
        dict(key="closing", label="Firms that close in a year", unit="rate",
             model="Firms that closed in a year, as a part of the firms left at the end of the year and those that closed. "
                   "Firms bought by other firms are not counted.",
             data="Employer firms that closed all their establishments in a year, as a part of the firms of the year before. "
                  "Firms bought by other firms are not counted.",
             source="Census Bureau, Business Dynamics Statistics, 2023 release, table by firm age, in data/firm_deaths.csv.",
             us=float(np.mean(list(d.values()))), low=float(np.quantile(list(d.values()), 0.25)),
             high=float(np.quantile(list(d.values()), 0.75)), span="1979 to 2023", yearly=closing),
        dict(key="survival", label="New firms still there after five years", unit="share",
             model="Firms that entered the list five years before and are still in it, as a part of the firms that entered "
                   "then. A firm that was bought counts as gone.",
             data="Employer firms aged 5 as a part of the firms aged 0 five years before.",
             source="Census Bureau, Business Dynamics Statistics, 2023 release, table by firm age, in data/firm_survival.csv.",
             us=float(np.mean(list(s.values()))), low=float(np.quantile(list(s.values()), 0.25)),
             high=float(np.quantile(list(s.values()), 0.75)), span="firms founded 1978 to 2018", yearly=surviving),
        dict(key="zombies", label="Firms kept alive by lenders", unit="share",
             model="Firms at least 10 years in the list that earned less than their interest for at least 3 years in a row, "
                   "as a part of all firms at least 10 years in the list.",
             data="Listed firms outside finance, over 10 years old, whose earnings were below their interest for three "
                  "years in a row, as a part of such firms in 14 rich countries. The study gives 'around 2% in the late "
                  "1980s' and 'some 12% in 2016'.",
             source="Ryan Banerjee and Boris Hofmann, 'The rise of zombie firms: causes and consequences', "
                    "BIS Quarterly Review, September 2018.",
             us=None, low=0.02, high=0.12, span="14 rich countries", range="the figures of the study for the late 1980s and for 2016", yearly=zombies),
    ]


TESTS = make_tests()


class Card:
    """Collects what the tests need from each year of one run."""

    def __init__(self, tests=None):
        self.tests = tests or TESTS
        self.years = []
        self.founded = []

    def add(self, r):
        """Add one year: `r` is what Model.step returned."""
        year = {"published": r.get("published", {}), "capital_share": r["capital_share"],
                "unemployment": r["unemployment"], "firms": r["firms"]}
        p = year["published"]
        self.founded.append(float(p.get("new_firms", 0.0) or 0.0))
        if len(self.founded) > 5:
            year["founded_five_years_before"] = self.founded[-6]
        self.years.append({k: year[k] for k in year if k != "published"} | {"parts": self._parts(year)})

    def _parts(self, year):
        out = {}
        for t in self.tests:
            try:
                got = t["yearly"](year)
            except (KeyError, TypeError):
                got = None
            out[t["key"]] = None if got is None or got[0] is None or got[1] is None else (float(got[0]), float(got[1]))
        return out

    def results(self):
        """Each test with the run's figure over the last WINDOW years, or None where the run has no such figure."""
        last = self.years[-WINDOW:]
        out = []
        for t in self.tests:
            got = [y["parts"][t["key"]] for y in last if y["parts"][t["key"]] is not None]
            whole = sum(g[1] for g in got)
            value = sum(g[0] for g in got) / whole if got and whole else None
            out.append({"key": t["key"], "value": value, "years": len(got)})
        return out


def describe():
    """The tests without their functions, for the workbench."""
    return [{"range": "the middle half of the years"} | {k: v for k, v in t.items() if k != "yearly"} | {"window": WINDOW}
            for t in TESTS]


if __name__ == "__main__":
    for t in TESTS:
        us = "" if t["us"] is None else f"typical {t['us']:.3f}, "
        print(f"{t['label']}: {us}{t['low']:.3f} to {t['high']:.3f} ({t.get('range', 'the middle half of the years')}, {t['span']})")
