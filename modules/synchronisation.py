"""Module 39: synchronisation of regimes. A readout. It changes no term of any firm.

Sources. Capital as Power (2009), chapter 14, "Spread, integration, oscillation". Chapter 17,
"Amalgamation versus stagflation", Figure 17.1 with its notes, and the endnote that reports a
moving correlation. Nitzan and Bichler, The Global Political Economy of Israel (2002), chapter 2. Bichler and Nitzan, "Francis' Buy-to-Build Estimates
for Britain and the United States" (2013).

What the literature says.
  - Chapter 14: the spread and the integration of differential accumulation "work to reinforce
    one another; and their unfolding makes the breadth-depth cycles ever more interdependent and
    synchronized across sectors and societies".
  - Chapter 17: "the spread was very uneven; and so, despite high capital mobility, initially the
    cyclical regimes in different sectors and countries were disjoined and out of step with one
    another". Only "with the progressive breaking of sectoral envelopes, and with the growing
    globalization of ownership" did "breadth and depth [grow] more stylized and inversely
    synchronized".
  - Chapter 17 measures the tightening for the United States as a whole: "the 30-year moving
    correlation between the stagflation and amalgamation indices in Figure 17.1 (with the latter
    index expressed as a natural log and measured as a deviation from its time trend) tightened
    almost to the fullest: it changed from a positive 0.06 in 1927 (virtually no correlation) to a
    negative 0.95 in 2007".
  - The stagflation index of Figure 17.1 is "the average of: (1) the standardized deviations from
    the average rate of unemployment; and (2) the standardized deviation from the average rate of
    inflation". The amalgamation index is the buy-to-build indicator. "Series are shown as 5-year
    moving averages."
  - The 2013 paper finds that the indices of Britain and the United States move together, which
    "corroborate[s] our suggestion that, over time, the global spread of differential accumulation
    helps synchronize the breadth-depth cycles across different countries".
  - The Israel book says of one country that its "cycle of breadth and depth was initially out of
    step with the rest of the world", and shows a "gradual shift from divergence to convergence".
  The literature gives one measured correlation, for one country taken whole. It gives no measure
  of how closely sectors move together, and none for countries beyond two charts.

Rule.
  1. Every firm carries a serial number that belongs to this module. A firm that was in the
     ledger last year and is gone this year was absorbed in a merger. Its employees are counted as
     merger volume of the sector (and the country) in which it sat.
  2. Each year the module records, for every sector, the employees absorbed as a part of the
     sector's employees, and the rise in the sector's price level. The price level of a sector is
     the average price of its firms, weighted by employees. If firms carry a country number, the
     module records the same two series for each country.
  3. Each year the module also records the two indices of Figure 17.1 for the whole ledger: the
     ratio of employees acquired to employees newly hired, and the average of standardized
     unemployment and standardized inflation.
  4. All series are smoothed as averages of the last five years. The correlations are taken over
     the last thirty smoothed years, and are published only once thirty are available.
  5. The module publishes: the average correlation between the merger volumes of every pair of
     sectors; the same for their price rises; the average, over sectors, of the correlation between
     a sector's own merger volume and its own price rise; the part of the sectors in which any
     merger took place; the book's correlation between the two indices for the whole ledger; and,
     with two countries, the correlation between the two countries' merger volumes and between
     their price rises. It also publishes the number of years it has on record.
  Everything the module reports describes the year before, because a module sees only the ledger
  at the start of the step.

Additions. The window of thirty years and the smoothing over five years are the book's. The use
of the correlation coefficient is the book's, for the whole economy. Applying it to pairs of
sectors and to two countries is an addition. Counting a sector's price rise as its depth is an
addition: the book's depth is stagflation, and the model holds no unemployment by sector.
Counting a merger in the sector of the firm that was absorbed is an addition. Taking the trend
of the amalgamation index within the window, and not over the whole century, is an addition.
The smallest value of the amalgamation index that the logarithm is given is an addition.
The serial number is the one thing the module writes to the ledger. Nothing else reads it, and
no term of the capitalization formula depends on it.
"""
import numpy as np
from core import Scale, Publish

SERIAL = "synchronisation_serial"    # the added per-firm number that lets the module see which firms were absorbed
NOTHING = float("nan")               # published while a correlation cannot yet be computed

KEYS = ("sync_mergers_sectors", "sync_prices_sectors", "sync_inverse_sectors", "sync_sectors_merging",
        "sync_breadth_depth", "sync_mergers_countries", "sync_prices_countries", "sync_years")


def _pairs(X):
    """Average correlation between every pair of columns that vary at all."""
    X = X[:, X.std(axis=0) > 1e-14]
    k = X.shape[1]
    if k < 2:
        return NOTHING
    C = np.corrcoef(X.T)
    return float((C.sum() - k) / (k * (k - 1)))


def _corr(a, b):
    if a.std() < 1e-14 or b.std() < 1e-14:
        return NOTHING
    return float(np.corrcoef(a, b)[0, 1])


class Synchronisation:
    name = "synchronisation"
    reads = ("merger_volume", "unemployment")
    supplies = KEYS
    figures = {                   # what the workbench calls each published number: label, unit, note
        "sync_mergers_sectors": ("Merger synchronisation across sectors", "number", "Average correlation of merger volumes between pairs of sectors."),
        "sync_prices_sectors": ("Price synchronisation across sectors", "number", "Average correlation of price rises between pairs of sectors."),
        'sync_inverse_sectors': ('Mergers against prices within sectors', 'number', "Average correlation of a sector's merger volume with its own price rise."),
        "sync_sectors_merging": ("Sectors with mergers", "share", "Part of the sectors in which any merger took place."),
        'sync_breadth_depth': ('Breadth against depth', 'number', "The book's correlation between the stagflation and amalgamation indices."),
        'sync_mergers_countries': ('Merger synchronisation across countries', 'number', "Correlation of the two countries' merger volumes."),
        'sync_prices_countries': ('Price synchronisation across countries', 'number', "Correlation of the two countries' price rises."),
        "sync_years": ("Years recorded", "number", ""),
    }

    def __init__(self, window=30, smooth=5, least_index=1e-4):
        self.window = window            # years over which each correlation is taken: the book's "30-year moving correlation"
        self.smooth = smooth            # years averaged before correlating: Figure 17.1's "5-year moving averages"
        self.least_index = least_index  # the smallest ratio of buying to hiring that is given to the logarithm (an addition)
        self.next_number = 1.0
        self.before = None              # last year's serial numbers, sectors, countries, employees and price levels
        self.sector_mergers, self.sector_prices = [], []
        self.country_mergers, self.country_prices = [], []
        self.amalgamation, self.unemployment, self.inflation = [], [], []

    def start(self, L):
        L.add_attribute(SERIAL, np.arange(1, len(L) + 1, dtype=float), -1.0)   # a new firm carries -1 until it is numbered
        self.next_number = float(len(L) + 1)
        return {k: NOTHING for k in KEYS}

    @staticmethod
    def _price(groups, p, n, k):
        return np.bincount(groups, p * n, k) / np.maximum(np.bincount(groups, n, k), 1e-12)

    def _smoothed(self, series):
        """The last `window` values of the trailing average over `smooth` years. Rows are years."""
        need = self.window + self.smooth - 1
        if len(series) < need:
            return None
        X = np.asarray(series[-need:], dtype=float).reshape(need, -1)
        c = np.vstack([np.zeros((1, X.shape[1])), np.cumsum(X, axis=0)])
        return (c[self.smooth:] - c[:-self.smooth]) / self.smooth

    def propose(self, L, rng):
        A = L.accounts
        count, n_sec = len(L), int(L.sector_of.max()) + 1
        changes = []

        # part 1: number the firms that were founded last year
        numbers = L.extra[SERIAL].copy()
        fresh = np.flatnonzero(numbers < 0)
        if fresh.size:
            given = self.next_number + np.arange(fresh.size, dtype=float)
            numbers[fresh] = given
            factor = np.ones(count)
            factor[fresh] = -given                      # -1 times -number gives the number
            changes.append(Scale(SERIAL, factor, self.name))
            self.next_number += fresh.size

        sec, n = L.sector, L.n
        has_countries = "country" in L.extra            # set by the second country module
        cty = (L.extra["country"] > 1.5).astype(int) if has_countries else np.zeros(count, dtype=int)
        # (a firm founded last year in the second country carries the first country's number for one year)
        now = {"numbers": numbers, "sec": sec.copy(), "cty": cty, "n": n.copy(),
               "p_sec": self._price(sec, L.p, n, n_sec), "p_cty": self._price(cty, L.p, n, 2),
               "p_all": float((L.p * n).sum() / n.sum())}

        b = self.before
        if b is not None:
            # parts 1 and 2: what last year did to each sector and each country
            gone = ~np.isin(b["numbers"], numbers)
            for groups, k, p_key, mergers, prices in (
                    (b["sec"], n_sec, "p_sec", self.sector_mergers, self.sector_prices),
                    (b["cty"], 2, "p_cty", self.country_mergers, self.country_prices)):
                employees = np.maximum(np.bincount(groups, b["n"], k), 1e-12)
                mergers.append(np.bincount(groups[gone], b["n"][gone], k) / employees)
                prices.append(np.log(np.maximum(now[p_key], 1e-300) / np.maximum(b[p_key], 1e-300)))
            # part 3: the two indices of Figure 17.1 for the whole ledger
            hires = float(np.sum(A.get("new_hires", 0.0)))
            acquired = float(A["merger_volume"]) * b["n"].sum()
            self.amalgamation.append(acquired / hires if hires > 0 else float(A["merger_volume"]))
            self.unemployment.append(float(A["unemployment"]))
            self.inflation.append(float(np.log(now["p_all"] / b["p_all"])))
        self.before = now

        # parts 4 and 5
        out = {k: NOTHING for k in KEYS}
        out["sync_years"] = float(len(self.amalgamation))
        M, P = self._smoothed(self.sector_mergers), self._smoothed(self.sector_prices)
        if M is not None:
            out["sync_mergers_sectors"] = _pairs(M)
            out["sync_prices_sectors"] = _pairs(P)
            own = [_corr(M[:, s], P[:, s]) for s in range(n_sec)]
            own = [c for c in own if c == c]
            out["sync_inverse_sectors"] = float(np.mean(own)) if own else NOTHING
            out["sync_sectors_merging"] = float((M.max(axis=0) > 0).mean())
            # the book's measure: stagflation index against the logarithm of the amalgamation index, less its trend
            am = np.log(np.maximum(self._smoothed(self.amalgamation)[:, 0], self.least_index))
            years = np.arange(am.size)
            am = am - np.polyval(np.polyfit(years, am, 1), years)
            u, i = self._smoothed(self.unemployment)[:, 0], self._smoothed(self.inflation)[:, 0]
            if u.std() > 1e-14 and i.std() > 1e-14:
                stagflation = ((u - u.mean()) / u.std() + (i - i.mean()) / i.std()) / 2
                out["sync_breadth_depth"] = _corr(stagflation, am)
            if has_countries:
                MC, PC = self._smoothed(self.country_mergers), self._smoothed(self.country_prices)
                out["sync_mergers_countries"] = _corr(MC[:, 0], MC[:, 1])
                out["sync_prices_countries"] = _corr(PC[:, 0], PC[:, 1])
        return changes + [Publish(k, v, self.name) for k, v in out.items()]
