"""Optional module: the power index and systemic fear. A readout, with one optional link.

The module changes no term of any claim. It measures two things that Bichler and Nitzan define in
"A CasP Model of the Stock Market" (2016), and it publishes one number that the optional hype
module reads. With the hype module off, a run with this module gives exactly the figures of the
run without it.

SOURCE

Bichler and Nitzan, "A CasP Model of the Stock Market" (2016), sections 5.1, 5.3, 6.1, 6.2, 6.5
and 6.6 (data/bn_archives/papers/stock_market_2016). Bichler and Nitzan, "Systemic Fear, Modern
Finance and the Future of Capitalism" (2010) (data/bn_archives/papers/systemic_fear_2010), for
the earlier way of measuring fear.

WHAT THE LITERATURE SAYS

  - The power index "is defined as the ratio between the S&P 500 price index and the average wage
    rate, normalized with its historical mean=100". The authors "compare not overall purchasing
    power and income services, but merely prices". The two prices "represent a conflict: the
    clash between those who own the capitalized means of power and those who are controlled by
    them". The wage rate is used "not as a measure of productivity or wellbeing, but as a
    benchmark against which to gauge the differential power of owners".
  - The index returns toward its mean because of resistance. "Everything else being the same, it
    is easier for capitalists to augment their power when the power index is at one or two
    standard deviations below its average ... than when the index is one or two standard
    deviations above it". "It is this changing intensity of resistance - and the fact that
    resistance goes hand in hand with power - that makes our power index mean reverting".
  - The ceiling. "It seems that two standard deviations above the mean is the historical
    asymptote, or limit, of capitalized equity power in the United States." "When capitalized
    power approaches its asymptotes, capitalists have good reason to fear their very own power."
  - Systemic fear is "an apprehension that the current mode of power might crumble". It is known
    by what owners do: "they effectively negate and abandon their core ritual of forward-looking
    capitalization; and we can know the degree to which they negate this ritual by the extent to
    which their asset pricing comes to depend on current rather than future earnings".
  - The systemic fear index is computed by "(1) computing the 12-month trailing correlation
    between price and EPS (earnings per share) of the S&P 500 index; (2) calculating the ten-year
    trailing average of the 12-month moving correlation". It runs "from a Pearson coefficient of
    0 (or less), which indicates that forward-looking capitalists do not fear for their system,
    to a Pearson coefficient of +1". The 2010 paper had correlated "the annual rates of change of
    equity prices and current earnings per share".
  - The two indices move together, with a correlation of +0.83 over 132 years: "the greater the
    capitalized power of equity owners relative to the underlying population, the greater their
    systemic fear and therefore the greater their reliance on current earnings when pricing
    their stocks".
  - Why. When the index is low there is "scope for increasing it further: income can be further
    redistributed in favour of profit, hype can be further amplified, profit volatility can be
    further decreased and the normal rate of return can be further lowered". When it is high,
    "when the profit share of income and the level of hype are already high and income volatility
    and the normal rate of return already low - increasing it further ... becomes harder and
    harder". "And since the future is too bleak to rely on, this reassurance can come only from
    current profit."
  The literature gives the two definitions, one figure for the ceiling (two standard deviations)
  and the direction of the link. It gives no rule that turns the distance of the power index
  from its mean into a degree of fear.

RULE

  1. The power index. The model has no shares. The price of a share is taken to be the
     capitalization of dominant capital divided by its employees, because a claim that grows by
     merger adds employees much as a firm that pays for a merger in shares adds shares. The power
     index is that price divided by the wage. Dominant capital is the hundred largest claims.
  2. Its own history. The module keeps every yearly reading of the index since the start of the
     run. It publishes the index with the mean of those readings set to 100. It publishes the
     distance of the index from its mean, counted in standard deviations of the logarithm of the
     readings, because the paper draws its bands on a logarithmic scale. Until thirty readings
     exist the distance is published as 0.
  3. The ceiling. The ceiling is two standard deviations above the mean, which is the paper's
     figure. The module publishes the gap between the index and the ceiling.
  4. The fear index, measured. Each year the module records the share price of part 1 and the
     current earnings of dominant capital for each employee. The fear index is the correlation,
     over the last ten years, between the yearly change of the logarithm of the price and the
     yearly change of the logarithm of the earnings. A reading near 1 means that capitalization
     followed current earnings. A reading near 0 means that it did not.
  5. The link. The module publishes a number between 0 and 1 named "power_fear". The number is 0
     when the power index is at or below its mean. It rises in a straight line with the distance
     of part 2 and is 1 at the ceiling. The hype module multiplies every change that the year
     would bring to a multiple by one minus the number. This covers the corrections of the herd,
     the push from mergers and the push of insiders, upward and downward alike. The multiple of
     a claim is the earnings that owners expect divided by the earnings that have arrived. At
     the ceiling the multiple stands still, so owners price each claim on its current earnings
     alone and capitalization follows current earnings. The number has no effect on anything
     when the hype module is off.

The module acts on nothing else. Every reading describes the year before, because a module sees
only the ledger at the start of a step.

WHAT IS ADDED

The ratio, the normalisation to a mean of 100, the two standard deviations and the window of ten
years are the paper's. Everything else is an addition:
  - taking capitalization for each employee of the hundred largest claims as the share price;
  - using only the history of the run so far, where the authors look back over the whole record;
  - waiting for thirty readings before the distance is reported (with fewer, a slow early rise
    reads as a ceiling, because the index has hardly varied yet);
  - correlating yearly changes over ten years, where the 2016 paper correlates monthly levels
    over twelve months and then averages ten years of those correlations (the model has no
    months, and yearly levels over ten years of rising prices would correlate for that reason
    alone);
  - the form of part 5: fear is 0 at the mean, rises in a straight line, and is 1 at the ceiling;
  - the route of part 5 through the hype module, and the holding still of the multiple. The
    paper says that pricing "comes to depend on current rather than future earnings". It does
    not say that the corrections of forecasters stop. Holding the multiple still is the plainest
    way to make price depend on current earnings in a formula where the multiple is the only
    forward-looking term. The read of "power_fear" in the hype module is the only change to an
    existing module.
  - The hype module also reads a number named "systemic_fear", which the eruptions module
    supplies. This module publishes under a different name so that the two cannot collide.

WHAT IS MISSING

The paper says that resistance is what turns the index back from its ceiling. This module does
not tell the resistance module anything, so the index is turned back only by what the model
already contains. The paper also names the profit share, risk and the normal rate of return as
things that become harder to move near the ceiling. Only hype is linked here. The risk shaping
module is not linked, because it would read a lasting high index as a lasting crisis.
"""
import numpy as np
from core import Publish, top_positions

NOTHING = float("nan")     # published while a reading cannot yet be computed

KEYS = ("power_index", "power_index_100", "power_distance", "power_ceiling_gap", "power_fear",
        "fear_index", "power_years_at_ceiling")


class Fear:
    name = "fear"
    reads = ()
    supplies = KEYS

    def __init__(self, ceiling=2.0, calm=0.0, least_years=30, window=10, link=1.0, top=100):
        self.ceiling = ceiling          # standard deviations above the mean at which the power index meets its limit: the paper's "two standard deviations above the mean is the historical asymptote". Its use as a setting is an addition: the paper says "it seems", it describes three moments in the record of the United States, and the index here is the model's own, measured against the history of the run
        self.calm = calm                # standard deviations from the mean at or below which there is no fear (addition; the paper reports fear near zero in the decades when the index stood below its mean)
        self.least_years = least_years  # readings needed before the mean and the standard deviation are used (addition)
        self.window = window            # years over which price and current earnings are correlated: the paper's ten-year average (its use on yearly changes is an addition)
        self.link = link                # part of the fear that is passed to the hype module; 0 leaves the module a pure readout (addition)
        self.top = top                  # dominant capital is the hundred largest claims, as in the book
        self.index, self.price, self.earnings = [], [], []
        self.at_ceiling = 0

    def start(self, L):
        out = {k: NOTHING for k in KEYS}
        out.update(power_distance=0.0, power_fear=0.0, power_years_at_ceiling=0.0)
        return out

    def propose(self, L, rng):
        K = L.cap()
        top = top_positions(K, np.arange(len(L)), self.top)
        employees = float(L.n[top].sum())
        price = float(K[top].sum()) / employees                 # part 1: the stand-in for the price of a share
        earnings = float(L.earnings()[top].sum()) / employees   # current earnings for each employee
        index = price / L.shared["wage"]
        self.index.append(index)
        self.price.append(price)
        self.earnings.append(earnings)

        # parts 2 and 3: the index against its own history so far
        readings = np.asarray(self.index)
        logs = np.log(readings)
        distance, gap = 0.0, NOTHING
        if readings.size >= self.least_years and logs.std() > 1e-12:
            distance = float((logs[-1] - logs.mean()) / logs.std())
            gap = self.ceiling - distance
            if distance >= self.ceiling:
                self.at_ceiling += 1

        # part 4: how closely the price followed current earnings over the last ten years
        measured = NOTHING
        if len(self.price) > self.window:
            dp = np.diff(np.log(self.price[-self.window - 1:]))
            de = np.diff(np.log(self.earnings[-self.window - 1:]))
            if dp.std() > 1e-12 and de.std() > 1e-12:
                measured = float(np.corrcoef(dp, de)[0, 1])

        # part 5: fear rises in a straight line from the mean to the ceiling
        fear = float(np.clip((distance - self.calm) / (self.ceiling - self.calm), 0.0, 1.0)) * self.link

        out = {"power_index": index, "power_index_100": 100.0 * index / float(readings.mean()),
               "power_distance": distance, "power_ceiling_gap": gap, "power_fear": fear,
               "fear_index": measured, "power_years_at_ceiling": float(self.at_ceiling)}
        return [Publish(k, v, self.name) for k, v in out.items()]
