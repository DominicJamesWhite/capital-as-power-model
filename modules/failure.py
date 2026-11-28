"""Module 10: firms that fail (Capital as Power, chapters 11, 12 and 13).

A firm fails when it cannot pay the interest it owes. A firm that fails closes: it leaves the
list, and its employees are without work until another firm hires them. A firm among the
hundred largest that fails is kept going by its lenders.

THE RULE IN PLAIN WORDS

  1. What a firm owes. The debt module says what part of all capitalist income is paid as
     interest. Lenders lend against what a firm sells, and they take more from a small
     firm than from a large one. Of each 100 of its sales, a firm among the largest tenth
     of firms pays 1.90 in interest, a firm in the smaller half pays 5.92, and a firm in
     between pays 3.48. These figures set only the proportions: all three are scaled by the
     same number, so that the interest of all firms adds up to the total that the debt
     module gives.
  2. Its cover. A firm's cover is its earnings divided by the interest it owes. If a fifth
     of capitalist income is paid as interest and every firm paid alike, a firm with
     average earnings would have a cover of 5. A small firm has less cover than a large
     one. So has a firm with a low markup, and a firm that could not sell all it offered.
     Every firm has less when lenders take more.
  3. The chance of failing. Owners are not sure of a firm's earnings, and its risk says how
     unsure they are. The module takes a year's earnings to be the expected earnings times
     a random factor. A factor as low as one over the firm's risk, or lower, comes up about
     one year in six. The chance that the firm fails in a year is the chance that this
     factor falls below one over its cover. With a risk of 2 and a cover of 5 it is about
     1 in 100. With a cover of 2.5 it is about 9 in 100. A firm with a risk of 1 fails only
     if its cover is below 1, and then it fails for certain.
  4. A firm outside the hundred largest that fails is closed.
  5. A firm among the hundred largest that fails is not closed. Its lenders restructure it:
     it stays in the list with all its employees, and its risk rises.
  6. Its buyers. The module publishes, for each industry, the part of its employees that
     worked for firms that closed. The next year the green-field module has the firms that
     are left in the industry take on the closed firms' buyers and hire for them, in
     proportion to their size, and the sabotage module counts the closure as capacity that
     left and the hiring as capacity that came back, so a closure whose buyers are all served
     again moves no markup.
  7. Its lenders. The firms that close stop paying. The module publishes the part of the
     interest that is left, set against the earnings that are left, and the debt module
     multiplies the interest part by it the next year. It also publishes the part of all
     employees whose firms closed. The debt module takes that off the unemployment it
     reads, because it reads unemployment as a sign that the institutions of power are
     solid, and promises that are being broken are a sign of the opposite. Without this,
     failures would raise unemployment, unemployment would raise what lenders take, and
     that would cause more failures without end.

The module moves no money. The debt module works out the total of corporate debt from the
firms in the list, so the debt of a firm that closes leaves the total with it and is paid to
nobody.

WHAT IT RESTS ON

  - Chapter 12, "Is free competition free of power?": "The actual production of a single firm
    and the number of firms in operation therefore are bounded not by the state of industrial
    arts, but by what can be sold at a 'reasonable' profit." The owner is told to "produce
    only if you expect to earn at least the normal rate of return. Otherwise, shut down."
  - Chapter 12, "Material assets": "equity capitalizes the firm's differential ability to
    restrict industry for its own benefit, whereas debt capitalizes the average ability of
    all owners to limit industry at large." Part 2 rests on this: lenders take a part of
    what all owners earn, and what a firm has to meet its part with is its own.
  - Joseph Baines and Sandy Brian Hager, "The Great Debt Divergence and its Implications for
    the Covid-19 Crisis: Mapping Corporate Leverage as Power" (2021), a study that builds on
    Nitzan and Bichler. The interest expenses of small United States firms reached "5.9 per
    cent of revenues in 2019, over triple the debt servicing burden of large firms". Its
    Figure 1 gives 5.92, 3.48 and 1.90 per cent for the smaller half of firms by revenue,
    the fifth to ninth tenths, and the largest tenth. The "cost of borrowing for smaller
    firms is considerably higher". Part 1 uses these figures and these three groups.
  - Bichler and Nitzan, "New Imperialism or New Capitalism?" (2006): with debt high, "if
    prices begin falling, firms will be unable to service their debt - and then we face the
    risk of debt deflation, chain bankruptcies, and a total meltdown of accumulation".
  - Chapter 11, "The degree of confidence": "Big capitalists do not take the odds as given;
    they try to change them." Part 3 lets the firm's risk set its odds.
  - Chapter 13, "The mega-machine resurrected: capital": "even when this richer menu of power
    occasionally fails, giving rise to losses and bankruptcy, large-scale capitalist
    organizations are usually able to resurrect themselves through merger, restructuring and
    the securitization of debt." Part 5 rests on this.
  - Bichler and Nitzan, The Global Political Economy of Israel (2002), chapter 4: "dominant
    capital was bailed out by the government, whereas most of the less fortunate investors,
    including some moderately big players, realised they were left out".

WHAT IS ADDED

The literature says that a firm shuts down when it cannot earn the normal return, that debt
rests on the average and equity on the firm's own power, that small firms pay lenders more
than large ones, that firms which cannot service their debt go bankrupt in chains, and that
large firms come back. It gives no rule and no rate of failure. These are additions: using
the proportions of one country in one year for every year; the reading of risk as the
spread of a year's earnings, and the bell-shaped curve used for it; that a restructured
firm keeps everything and only its risk rises, and by how much; that the buyers of a
closed firm turn to the firms left in its industry; and that the jobs lost in closed
firms are taken off the unemployment that the debt module reads. Every source is by Nitzan and
Bichler, or builds on their work and is listed in their archive. No other study is used.

WHAT IS MISSING

Nobody receives a failed firm's plant directly, and its lenders lose what it
owed without any payment being recorded. A firm does not build up debt of its own, so a
firm that has been short of cover for years is treated like one that is short for the first
time. Baines and Hager find that the three groups paid alike in the 1950s and drew apart
after 1980; the module keeps the proportions of 2019 throughout.
"""
import numpy as np
from core import Dissolve, Scale, Publish, top_positions


def chance_below(z):
    """The chance that a bell-shaped (normal) draw falls below z. Worked out with a standard
    approximation that is right to seven decimal places (Abramowitz and Stegun, formula 7.1.26)."""
    x = np.abs(z) / np.sqrt(2.0)
    t = 1.0 / (1.0 + 0.3275911 * x)
    poly = t * (0.254829592 + t * (-0.284496736 + t * (1.421413741 + t * (-1.453152027 + t * 1.061405429))))
    tail = 0.5 * poly * np.exp(-x * x)              # the chance of falling beyond |z| on one side
    return np.where(z < 0, tail, 1.0 - tail)


class Failure:
    name = "failure"
    reads = ("interest_share",)
    supplies = ("failures", "failed_employees", "failed_by_industry", "closed_employees", "restructurings", "interest_left",
                "failure_chance", "interest_cover")
    figures = {                   # what the workbench calls each published number: label, unit, note
        "failures": ("Firms that failed", "number", "Firms outside the top 100 that closed in the year."),
        "failed_employees": ("Employees of failed firms", "share", "Employees of the firms that closed in the year, as a part of all employees."),
        "restructurings": ("Top 100 firms restructured", "number", "Top 100 firms that failed in the year and were kept going by their lenders."),
        "interest_left": ("Interest left after failures", "share", "Part of the interest share that is left once the firms that closed have stopped paying."),
        "failure_chance": ("Chance of failing", "share", "Average chance that a firm outside the top 100 fails in the year, weighted by employees."),
        "interest_cover": ("Interest cover", "times", "Earnings divided by interest owed, averaged over the firms outside the top 100 and weighted by employees."),
    }

    def __init__(self, on=True, small_burden=5.92, medium_burden=3.48, large_burden=1.90, small_part=0.5,
                 large_part=0.1, restructuring_risk=0.5, top=100):
        self.on = on                                  # False switches the module off: no firm fails and nothing else changes
        self.small_burden = small_burden              # interest paid by a small firm for each 100 of its sales; only the proportions among the three count
        self.medium_burden = medium_burden            # the same for a firm that is neither small nor large
        self.large_burden = large_burden              # the same for a large firm
        self.small_part = small_part                  # the part of all firms, counted from the smallest by sales, that are small
        self.large_part = large_part                  # the part of all firms, counted from the largest by sales, that are large
        self.restructuring_risk = restructuring_risk  # rise in the risk of a firm of dominant capital when its lenders restructure it
        self.top = top                                # the number of firms counted as dominant capital, as in the book

    def start(self, L):
        return {"failures": 0.0, "failed_employees": 0.0, "failed_by_industry": np.zeros(L.sector_of.size),
                "closed_employees": np.zeros(L.sector_of.size),
                "restructurings": 0.0, "interest_left": 1.0, "failure_chance": 0.0, "interest_cover": 0.0}

    def chances(self, L):
        """Each firm's cover and its chance of failing this year."""
        n = L.n
        earnings = n * np.maximum(L.e, 0.0)
        interest = L.accounts["interest_share"] * earnings.sum()      # the interest that all firms owe together
        sales = n * L.p
        if interest <= 0 or sales.sum() <= 0:         # nothing is owed: no firm can fall short
            return np.full(len(L), np.inf), np.zeros(len(L)), np.zeros(len(L))
        small_below, large_from = np.quantile(sales, [self.small_part, 1.0 - self.large_part])
        burden = np.where(sales >= large_from, self.large_burden,
                          np.where(sales < small_below, self.small_burden, self.medium_burden))
        owed = burden * sales * (interest / (burden * sales).sum())   # each firm's part of that interest
        with np.errstate(divide="ignore", invalid="ignore"):
            cover = np.where(owed > 0, earnings / owed, np.inf)
        spread = np.log(np.maximum(L.d, 1.0))         # a risk of 1 is full confidence: no spread
        with np.errstate(divide="ignore", invalid="ignore"):
            z = -np.log(cover) / spread
            chance = np.where(spread > 0, chance_below(z), (cover < 1.0).astype(float))
        chance = np.where(n > 0, chance, 0.0)         # a firm with nobody in it has nothing to close
        return cover, chance, owed

    def propose(self, L, rng):
        if not self.on:
            return []
        k, n = L.sector_of.size, L.n
        cover, chance, owed = self.chances(L)
        fails = rng.random(len(L)) < chance
        dominant = np.zeros(len(L), dtype=bool)
        dominant[top_positions(L.cap(), np.arange(len(L)), self.top)] = True
        closes, restructured = fails & ~dominant, fails & dominant
        employed = n.sum()
        small = ~dominant
        small_n = max(n[small].sum(), 1e-300)
        by_industry = np.bincount(L.ind[closes], n[closes], k) / np.maximum(np.bincount(L.ind, n, k), 1e-300)
        finite = np.isfinite(cover)
        # What the lenders lose. The firms that close stop paying, so the interest that is left is a smaller
        # part of the earnings that are left, if those firms owed more for each unit of earnings than the rest.
        earnings = n * np.maximum(L.e, 0.0)
        left = 1.0
        if closes.any() and owed.sum() > 0 and earnings[~closes].sum() > 0:
            left = (owed[~closes].sum() / owed.sum()) / (earnings[~closes].sum() / earnings.sum())
        changes = [Publish("failures", float(closes.sum()), self.name),
                   Publish("failed_employees", float(n[closes].sum() / max(employed, 1e-300)), self.name),
                   # the sabotage module counts this next year as capacity that has left the industry
                   Publish("failed_by_industry", by_industry, self.name),
                   # the green-field module has the firms left in each industry hire this many next year
                   Publish("closed_employees", np.bincount(L.ind[closes], n[closes], k), self.name),
                   Publish("restructurings", float(restructured.sum()), self.name),
                   # the debt module multiplies the part of capitalist income paid as interest by this next year
                   Publish("interest_left", float(left), self.name),
                   Publish("failure_chance", float((n[small] * chance[small]).sum() / small_n), self.name),
                   Publish("interest_cover",
                           float((n[small] * cover[small]).sum() / small_n) if finite.all() else 0.0, self.name)]
        if restructured.any():
            changes.append(Scale("risk", np.where(restructured, 1.0 + self.restructuring_risk, 1.0), self.name))
        if closes.any():
            changes.append(Dissolve(np.flatnonzero(closes), self.name))
        return changes
