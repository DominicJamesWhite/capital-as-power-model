"""Optional module: capitalization against plant and equipment. A readout. It changes nothing.

The module keeps a record, in money, of the plant and equipment that green-field hiring has paid
for. It reports the ratio of all capitalization to that record, and the growth rates of the two.
No module reads what it publishes. The record never enters earnings, hype, risk, price or
capitalization, so a run with this module gives exactly the figures of the run without it.

SOURCE

Capital as Power (2009), chapter 10, "Capitalization: fiction, mirror or distortion?", the
sections "Tobin's Q: adding intangibles", "Boom and bust: adding irrationality" and "The gods must
be crazy", with Figures 10.2, 10.3 and 10.4 and the endnote on deflated series. Chapter 12, the
passage on book value. Chapter 15, the section "Tobin's Q" with Figure 15.3, and the last note of
the Data Appendix. The 2001 regimes paper and the 2002 book on Israel repeat the argument of
chapter 15.

WHAT THE LITERATURE SAYS

  - The measure. Figure 10.2 "takes the market value of all outstanding corporate stocks and
    bonds and divides it by the current replacement cost of corporate fixed assets (plant and
    equipment)". "Since both magnitudes are denominated in current prices, the ratio between them
    is a pure number."
  - The level. If capitalization mirrored plant, the ratio "should have been 1". In fact "the
    historical mean value of the series is not 1, but 1.24", and "over the past 75 years it has
    oscillated between a low of 0.6 and a high of 2.8". The book finds no reason for the level:
    "the question remains as to why Tobin's Q should average 1.24, rather than 1.01 or 20".
  - The growth rates. Figure 10.4 shows both growth rates "smoothed as 10-year moving averages".
    "The gyrations of capitalization, instead of amplifying those of 'real' assets, move in
    exactly the opposite direction." These are "very long-term waves of roughly 30-year
    duration". "Whenever the growth rate of 'real' assets decelerates, the growth rate of
    capitalization accelerates, and vice versa." "During the 1940s and 1970s, when the dollar
    value of 'real assets' expanded the fastest, capitalists saw their capitalization growth
    dwindle." The endnote adds that deflating both series gives a similar result.
  - What the record is not. "A collection of capital goods cannot have a definite physical
    quantity." The comparison is made only by assuming "that the material quantity of capital
    goods (whether that quantity 'exists' or not) can be measured by their prices". Chapter 12:
    "on the company books, physical assets are recorded not at current market value, but at
    cost", and "the very cost of producing plant and equipment is already a manifestation of
    systemic conflict and struggle".
  - Building and buying. Chapter 15: "we use the term 'green-field investment' to denote the
    purchase of newly produced plant and equipment. The production of these items is distinct
    from the process of accumulation." In a merger "no new capacity is created". The ratio and
    the ratio of buying to building move "not inversely, but together", and "Tobin's Q turns from
    a cause to a consequence: it goes up when investors happen to buy and down when they decide
    to build".
  - The conclusion. "For the capitalist, the real thing is the nominal capitalization of future
    earnings. This capitalization is not 'connected' to reality; it is the reality."
  The literature gives the measure, three figures for its level (1.24, 0.6 and 2.8), the ten-year
  smoothing and the length of the waves. It gives no rule for how much plant a new employee
  needs, for how plant wears out, or for the size of the opposite movement.

RULE

  1. The opening record. In the first year the record is set equal to all capitalization divided
     by the starting ratio, which is 1. The cost of plant for one employee, in opening prices, is
     the opening record divided by the number of employees. That cost stays fixed in opening
     prices for the whole run.
  2. Building. Each year the module counts the employees newly hired in every industry that grew
     in the year before. The plant built for them costs their number, times the cost of plant
     for one employee, times the price level. The price level is the average price of all
     firms, weighted by employees. A merger builds nothing, so it adds nothing to the record.
  3. Wear. Each year a fixed part of the plant wears out. The worn plant of employees who are
     still employed is replaced at current prices. Plant that has no employee, because its
     employees were dismissed, wears out and is not replaced.
  4. Two records. The record at cost adds each year's building and replacement at the prices paid
     and never revalues them. The record at current cost is revalued every year by the rise in
     the price level, as the book's "current replacement cost" is.
  5. The readouts. The module publishes all capitalization divided by the record at current cost,
     which is the ratio of Figure 10.2, and all capitalization divided by the record at cost. It
     publishes the mean, the lowest and the highest value of the first ratio so far. It publishes
     the yearly growth of capitalization and of the record at current cost, each averaged over
     the last ten years, as in Figure 10.4. It publishes the correlation between those two
     averaged growth rates over the last thirty years. It publishes the part of the record that
     has no employee. It publishes the correlation, over the last thirty years, between the ratio
     and the ratio of employees acquired to employees hired, both averaged over five years, as in
     Figure 15.3.

Every reading describes the start of the year, because a module sees only the start-of-step
ledger. The module uses no random numbers.

WHAT IS ADDED

The ratio, the current-cost basis, the ten-year smoothing and the five-year smoothing of Figure
15.3 are the book's. Everything else is an addition:
  - the starting ratio of 1. The book says the level has no explanation, so the level in the model
    is a convention and only the movement carries meaning;
  - a fixed cost of plant for one employee. The book denies that plant has a material quantity.
    The model counts employees and nothing else, so the record is a count of employees hired,
    stated in money;
  - pricing plant at the average price of all firms;
  - the yearly rate of wear, and the replacement of worn plant only where employees remain;
  - counting hiring industry by industry, so that dismissals in one industry do not cancel
    building in another, and building new plant for every hire even when idle plant stands
    elsewhere;
  - taking the capitalization of all firms as "stocks and bonds". The debt module divides the
    same earnings into interest and profit, so the firms in the ledger already capitalize both;
  - the correlation coefficient and the window of thirty years. The book shows a chart and
    reports no coefficient. Thirty years is the length it gives for one wave.

WHAT IS MISSING

The record is one number for the whole ledger. A merged firm keeps only the buyer's value of an
added attribute, so a record held firm by firm would lose the plant of every acquired firm.
The module therefore cannot show the book's comparison of Microsoft with General Motors, or the
ratio of dominant capital alone. Employees hired by the force module and employees who arrive
through privatisation are not counted as building.
"""
import numpy as np
from core import Publish

NOTHING = float("nan")     # published while a reading cannot yet be computed

KEYS = ("plant_ratio", "plant_ratio_at_cost", "plant_ratio_mean", "plant_ratio_low", "plant_ratio_high",
        "plant_record", "plant_record_at_cost", "plant_built", "plant_idle",
        "plant_growth_capitalization", "plant_growth_record", "plant_growth_correlation",
        "plant_buy_build_correlation")


def _trailing(series, smooth, window):
    """The last `window` values of the average over `smooth` years, or None while too few exist."""
    need = window + smooth - 1
    if len(series) < need:
        return None
    c = np.concatenate([[0.0], np.cumsum(np.asarray(series[-need:], dtype=float))])
    return (c[smooth:] - c[:-smooth]) / smooth


def _corr(a, b):
    if a is None or b is None or a.std() < 1e-14 or b.std() < 1e-14:
        return NOTHING
    return float(np.corrcoef(a, b)[0, 1])


class Plant:
    name = "plant"
    reads = ("industry_growth",)
    supplies = KEYS
    figures = {                   # what the workbench calls each published number: label, unit, note
        "plant_ratio": ("Capitalization against plant", "times", "All capitalization divided by plant at current cost."),
        "plant_ratio_at_cost": ("Capitalization against plant at cost", "times", "All capitalization divided by plant at the prices paid."),
        "plant_ratio_mean": ("Capitalization against plant, mean so far", "times", ""),
        "plant_ratio_low": ("Capitalization against plant, lowest so far", "times", ""),
        "plant_ratio_high": ("Capitalization against plant, highest so far", "times", ""),
        "plant_record": ("Plant at current cost", "number", "In money."),
        "plant_record_at_cost": ("Plant at cost", "number", "In money."),
        "plant_built": ("Plant built", "number", "Building and replacement in the year, in money."),
        "plant_idle": ("Idle plant", "share", "Part of the plant record that has no employee."),
        "plant_growth_capitalization": ("Growth of capitalization", "rate", "Averaged over the last 10 years."),
        "plant_growth_record": ("Growth of plant", "rate", "Averaged over the last 10 years."),
        "plant_growth_correlation": ("Capitalization against plant growth", "number", "Correlation of the two growth rates over the last 30 years."),
        "plant_buy_build_correlation": ("Ratio against buying", "number", "Correlation over the last 30 years between the ratio and employees bought for each employee hired."),
    }

    def __init__(self, start_ratio=1.0, wear=0.05, smooth=10, window=30, smooth_ratio=5):
        self.start_ratio = start_ratio    # capitalization divided by the record in the first year (addition; 1 is the value the book says a mirror would give)
        self.wear = wear                  # part of the plant that wears out each year (addition)
        self.smooth = smooth              # years over which each growth rate is averaged: Figure 10.4's "10-year moving averages"
        self.window = window              # years over which each correlation is taken (addition; the book's waves are "of roughly 30-year duration")
        self.smooth_ratio = smooth_ratio  # years over which the ratio and the buying-to-building ratio are averaged: Figure 15.3's "5-year moving averages"
        self.per_employee = None          # cost of plant for one employee, in opening prices; fixed by part 1
        self.current = self.cost = None   # the record at current cost and the record at cost
        self.before = None                # last year's employees by industry, price level, capitalization and record
        self.ratios, self.growth_cap, self.growth_record, self.buy_build = [], [], [], []

    def start(self, L):
        return {k: NOTHING for k in KEYS}

    def propose(self, L, rng):
        A = L.accounts
        employees = float(L.n.sum())
        price = float((L.p * L.n).sum() / employees)
        cap = float(L.cap().sum())
        by_industry = np.bincount(L.ind, L.n, L.sector_of.size)
        built, b = 0.0, self.before

        if b is None:                                      # part 1: the opening record
            self.current = self.cost = cap / self.start_ratio
            self.per_employee = self.current / (price * employees)
        else:
            # part 2: plant for the employees hired last year, industry by industry
            growth = np.broadcast_to(np.asarray(A["industry_growth"], dtype=float), by_industry.size)
            hired = float((np.maximum(growth, 0.0) * b["by_industry"]).sum())
            new = hired * self.per_employee * price
            # part 4: the record at current cost is revalued; the record at cost is not
            revalued = self.current * price / b["price"]
            # part 3: worn plant is replaced only where employees remain
            in_use = min(revalued, self.per_employee * price * employees)
            replaced = self.wear * in_use
            built = new + replaced
            self.current = revalued * (1 - self.wear) + built
            self.cost = self.cost * (1 - self.wear) + built
            self.growth_cap.append(float(np.log(cap / b["cap"])))
            self.growth_record.append(float(np.log(self.current / b["current"])))
            hires = float(np.sum(A.get("new_hires", 0.0)))
            bought = float(A.get("merger_volume", 0.0)) * b["employees"]
            self.buy_build.append(bought / hires if hires > 0 else NOTHING)
        self.before = {"by_industry": by_industry, "price": price, "cap": cap,
                       "current": self.current, "employees": employees}

        # part 5: the readouts
        ratio = cap / self.current
        self.ratios.append(ratio)
        out = {k: NOTHING for k in KEYS}
        out.update(plant_ratio=ratio, plant_ratio_at_cost=cap / self.cost,
                   plant_ratio_mean=float(np.mean(self.ratios)), plant_ratio_low=float(np.min(self.ratios)),
                   plant_ratio_high=float(np.max(self.ratios)),
                   plant_record=self.current, plant_record_at_cost=self.cost, plant_built=built,
                   plant_idle=max(0.0, 1.0 - self.per_employee * price * employees / self.current))
        if len(self.growth_cap) >= self.smooth:
            out["plant_growth_capitalization"] = float(np.mean(self.growth_cap[-self.smooth:]))
            out["plant_growth_record"] = float(np.mean(self.growth_record[-self.smooth:]))
        out["plant_growth_correlation"] = _corr(_trailing(self.growth_cap, self.smooth, self.window),
                                                _trailing(self.growth_record, self.smooth, self.window))
        q = _trailing(self.ratios[1:], self.smooth_ratio, self.window)      # ratios[1:] lines up with buy_build
        bb = _trailing(self.buy_build, self.smooth_ratio, self.window)
        if bb is not None and not np.isnan(bb).any():
            out["plant_buy_build_correlation"] = _corr(q, bb)
        return [Publish(k, v, self.name) for k, v in out.items()]
