"""Module 10: firms that fail (Capital as Power, chapters 9, 11, 12 and 13).

Each firm carries a debt from year to year, and owes interest on it at the rate at which it was
lent. A firm that cannot pay its interest is lent the shortfall. When it has owed more than it is
worth for `patience` years in a row, its lenders refuse to lend more. A firm outside
the hundred largest is then closed: it leaves the list, and its employees are without work until
another firm hires them. A firm among the hundred largest is restructured by its lenders.

THE RULE IN PLAIN WORDS

  1. The first year. Lenders lend against what a firm sells, and they take more from a small
     firm than from a large one. Of each 100 of its sales, a firm in the smaller half of firms
     pays 5.92 in interest, a firm among the largest tenth pays 1.90, and a firm in between
     pays 3.48. One number scales the three so that the interest of all firms is the part of
     capitalist income that the debt module gives in the first year. The size of a firm is its
     sales counted in wages, and the two sizes that divide the three groups are those of the
     first year.
  2. The rate. A small firm borrows at 7.8 for each 5.1 that a firm in between pays, and a large
     firm at 3.9. The firm in between pays the normal rate of return. A firm's debt in the first
     year is its interest divided by its rate. Its debt for each unit of its sales is the
     amount that lenders will lend it against its sales in every later year.
  3. Each year a part of every debt falls due: one year in `term`. The firm repays it and
     borrows again, at the rate of the year for a firm of its size, up to what lenders will
     lend against its sales. If its sales have grown it borrows more. If they have fallen, it
     repays what lenders will no longer lend. The rest of its debt keeps the rate at which it
     was lent. So a firm whose sales fall still owes what it borrowed, and only over the years
     does what it owes come to follow its sales.
  4. A firm whose earnings fall short of its interest and of what it has to repay is lent the
     shortfall, at the rate of the year, and its debt grows.
  5. Lenders refuse to lend more when a firm has owed more than it is worth for three years
     in a row (`patience`). What it is worth is its capitalization, the price owners put on
     all its expected earnings. Owners then have had nothing left in the firm for years, and
     lending more puts lenders' own money behind a claim already worth less than it promises.
     Lenders wait because closing a firm loses them its whole debt. A firm outside the hundred
     largest that lenders refuse is closed.
  6. A firm among the hundred largest that lenders refuse is not closed. Its lenders write its
     debt down to the debt of the average firm for what it is worth, with the interest in the
     same proportion, and its risk rises.
  7. Its buyers. The module publishes, for each industry, the part of its employees that
     worked for firms that closed. The next year the green-field module has the firms that
     are left in the industry take on the closed firms' buyers and hire for them, and the
     sabotage module counts the closure as capacity that left and the hiring as capacity that
     came back.
  8. Its lenders. A firm that closes takes its debt with it, and lenders lose it. The module
     publishes the interest that the firms left owe, as a part of their earnings, and the
     debt that they owe, and the debt module reports both.

The module moves no money. Interest is a division of a firm's earnings between its lenders and
its owners, and the module only keeps count of it.

WHAT IT RESTS ON

  - Chapter 12, "Is free competition free of power?": "The actual production of a single firm
    and the number of firms in operation therefore are bounded not by the state of industrial
    arts, but by what can be sold at a 'reasonable' profit."
  - Chapter 12, "The maturity of capitalism": "economic fluctuations affect profit more than
    interest, so when unemployment rises so should the ratio of interest to profit. However,
    this triviality holds only in the short term. In the longer haul, interest payments are
    much more flexible". Debt is "a promise of return". Parts 3 and 4 rest on this: what a firm
    owes is fixed when it borrows, and comes to follow its sales only as its debt falls due.
  - Chapter 9, "Capitalization: a brief anthropology", quoting Bernoulli: the man "pressed by
    creditors" who would demand a thousand ducats to give up his prospects is worth a thousand,
    "though in common parlance the former owns nothing and the latter less than nothing". Part
    5 measures a firm's worth by the price put on its expected earnings and sets it against
    what it owes.
  - Joseph Baines and Sandy Brian Hager, "The Great Debt Divergence and its Implications for
    the Covid-19 Crisis: Mapping Corporate Leverage as Power" (2021), a study that builds on
    Nitzan and Bichler. Its Figure 1 gives interest of 5.92, 3.48 and 1.90 per cent of revenues
    in 2019 for the smaller half of United States listed firms, the fifth to ninth tenths and
    the largest tenth, and "Large firms see their cost of borrowing fall to 3.9 per cent,
    medium-size firms to 5.1 per cent, and small firms to 7.8 per cent". The smaller half show
    "consistently negative profit margins" for decades. Parts 1, 2 and 4 use these figures.
  - Ryan Banerjee and Boris Hofmann, "The rise of zombie firms: causes and consequences" (BIS
    Quarterly Review, September 2018), a study from outside the tradition that Baines and Hager
    cite. Firms whose interest cover "has been less than one for at least three consecutive
    years" were about 12 per cent of listed firms in 14 advanced economies in 2016, and the
    chance that such a firm was still one the next year rose from 60 to 85 per cent, because
    "banks have incentives to roll over loans to non-viable firms rather than writing them
    off". In terms of power: whether a firm that cannot pay goes on is the lenders' choice. Part
    4 rests on this.
  - Chapter 13, "The mega-machine resurrected: capital": "large-scale capitalist organizations
    are usually able to resurrect themselves through merger, restructuring and the
    securitization of debt". Part 6 rests on this.

WHAT IS ADDED

The literature says that a firm's debt is a promise fixed when it is made, that small firms pay
more for each unit of sales and at a higher rate, that firms which cannot pay are often carried
by their lenders for years, and that large firms come back. It gives no rule for when lenders
stop. These are additions: that lenders lend against sales at the first year's terms for each
size; that the firm in between borrows at the normal rate of return; that a firm is refused
when it has owed more than it is worth for `patience` years, 3, which is the span over which
Banerjee and Hofmann count a firm as kept alive by its lenders; what a restructuring writes off; the proportions of one
country in one year for every year; and the sizes that divide the groups, fixed in the first
year. `term`, 5 years, lies between the median remaining maturity of rated debt of United
States firms that S&P Global Ratings reported for 1 January 2024: 5.9 years for investment
grade and 3.9 years for speculative grade, read from a summary of that report.

WHAT IS MISSING

Nobody receives a failed firm's plant, and its lenders lose what it owed without any payment
being recorded. Borrowing buys nothing: the firm's debt follows its sales, and its sales do not
follow its debt.
"""
import numpy as np
from core import Dissolve, Scale, Publish, SetAttribute, top_positions

DEBT = "debt"            # each firm's debt, in money
INTEREST = "interest"    # the interest a firm owes on it in a year, in money, at the rates at which it was lent
UNDER = "years owing more than worth"   # the years in a row that a firm has owed more than it is worth


class Failure:
    name = "failure"
    reads = ("interest_share",)
    supplies = ("failures", "failed_employees", "failed_by_industry", "closed_employees", "restructurings", "interest_owed",
                "debt_owed", "short_of_cover", "interest_cover")
    figures = {                   # what the workbench calls each published number: label, unit, note
        "failures": ("Firms that failed", "number", "Firms outside the top 100 that closed in the year."),
        "failed_employees": ("Employees of failed firms", "share", "Employees of the firms that closed in the year, as a part of all employees."),
        "restructurings": ("Top 100 firms restructured", "number", "Top 100 firms that failed in the year and were kept going by their lenders."),
        "interest_owed": ("Interest owed", "share", "Interest that the firms left owe, as a part of their earnings."),
        "debt_owed": ("Debt owed by firms", "number", "The debt that the firms left owe, in money."),
        "short_of_cover": ("Firms carried by lenders", "share", "Employees of firms outside the top 100 whose earnings fell short of their interest, as a part of all their employees."),
        "interest_cover": ("Interest cover", "times", "Earnings divided by interest owed, over the firms outside the top 100."),
    }

    def __init__(self, on=True, small_burden=5.92, medium_burden=3.48, large_burden=1.90,
                 small_rate=7.8, medium_rate=5.1, large_rate=3.9, small_part=0.5, large_part=0.1,
                 term=5.0, patience=3, restructuring_risk=0.5, top=100):
        self.on = on                                  # False switches the module off: no firm fails and nothing else changes
        self.small_burden = small_burden              # interest paid by a small firm for each 100 of its sales in the first year; only the proportions among the three count
        self.medium_burden = medium_burden            # the same for a firm that is neither small nor large
        self.large_burden = large_burden              # the same for a large firm
        self.small_rate = small_rate                  # the rate a small firm borrows at, for each medium_rate that a firm in between pays
        self.medium_rate = medium_rate                # a firm in between borrows at the normal rate of return
        self.large_rate = large_rate                  # the same for a large firm
        self.small_part = small_part                  # the part of all firms, counted from the smallest by sales, that are small
        self.large_part = large_part                  # the part of all firms, counted from the largest by sales, that are large
        self.term = term                              # years over which a debt falls due: one part in `term` each year
        self.patience = patience                      # years in a row that lenders carry a firm that owes more than it is worth
        self.restructuring_risk = restructuring_risk  # rise in the risk of a firm of dominant capital when its lenders restructure it
        self.top = top                                # the number of firms counted as dominant capital, as in the book
        self.terms = None                             # the two sizes that divide the groups, set in the first year

    def register(self, L):
        L.add_attribute(DEBT, 0.0, 0.0, adds=True, owner=self.name)
        L.add_attribute(INTEREST, 0.0, 0.0, adds=True, owner=self.name)
        L.add_attribute(UNDER, 0.0, 0.0, owner=self.name)

    def start(self, L):
        return {"failures": 0.0, "failed_employees": 0.0, "failed_by_industry": np.zeros(L.sector_of.size),
                "closed_employees": np.zeros(L.sector_of.size), "restructurings": 0.0, "short_of_cover": 0.0,
                "interest_cover": 0.0}

    def groups(self, L):
        """Each firm's group by size: 0 small, 1 in between, 2 large."""
        size = L.n * L.p / L.shared["wage"]           # sales counted in wages, so that a rise of all wages moves nobody
        if self.terms is None:
            self.terms = tuple(np.quantile(size, [self.small_part, 1.0 - self.large_part])) if len(L) else (0.0, 0.0)
        small_below, large_from = self.terms
        return np.where(size >= large_from, 2, np.where(size < small_below, 0, 1))

    def rates(self):
        """The rate of each group, as a multiple of the normal rate of return."""
        return np.array([self.small_rate, self.medium_rate, self.large_rate]) / self.medium_rate

    def first_year(self, L):
        """Each firm's debt and interest in the first year, and the debt that lenders lend for each unit of sales."""
        g = self.groups(L)
        weight = np.array([self.small_burden, self.medium_burden, self.large_burden])
        sales = L.n * L.p
        share = max(float(L.accounts.get("interest_share", 0.0)), 0.0)
        scale = share * (L.n * np.maximum(L.e, 0.0)).sum() / max((weight[g] * sales).sum(), 1e-300)
        self.lend = scale * weight / (self.rates() * L.shared["nrr"])
        debt = self.lend[g] * sales
        return debt, debt * self.rates()[g] * L.shared["nrr"]

    def year(self, L):
        """This year's interest, each firm's debt and interest at the end of the year if lenders go on lending, and
        which firms earn less than their interest."""
        if self.terms is None:
            debt, interest = self.first_year(L)
        else:
            debt, interest = L.extra[DEBT].copy(), L.extra[INTEREST].copy()
        g = self.groups(L)
        lends = self.lend[g] * L.n * L.p              # what lenders lend against the firm's sales
        rate = self.rates()[g] * L.shared["nrr"]      # this year's rate for a firm of its size
        kept = debt * (1.0 - 1.0 / self.term)         # what does not fall due this year keeps its rate
        planned = np.maximum(lends, kept)
        borrowed = planned - kept
        repaid = np.maximum(debt - planned, 0.0)
        earnings = L.n * np.maximum(L.e, 0.0)
        short = np.maximum(interest + repaid - earnings, 0.0)   # what lenders lend to cover what the firm cannot pay
        new_interest = interest * (1.0 - 1.0 / self.term) + rate * (borrowed + short)
        return interest, planned + short, new_interest, interest > earnings

    def propose(self, L, rng):
        if not self.on:                               # nobody fails, and firms owe the terms that lenders set
            return [Publish("interest_owed", float(L.accounts["interest_share"]), self.name)]
        k, n = L.sector_of.size, L.n
        interest, debt, owed, short = self.year(L)
        K = L.cap()
        dominant = np.zeros(len(L), dtype=bool)
        dominant[top_positions(K, np.arange(len(L)), self.top)] = True
        under = np.where(debt > K, L.extra[UNDER] + 1.0, 0.0)   # the firm owes more than it is worth, this year too
        refused = (under >= self.patience) & (n > 0)
        closes, restructured = refused & ~dominant, refused & dominant
        # A restructured firm keeps the debt of the average firm for what it is worth after its risk has risen.
        good = ~refused & (K > 0)
        average = debt[good].sum() / K[good].sum() if K[good].sum() > 0 else 0.0
        written = np.where(restructured, average * np.maximum(K, 0.0) / (1.0 + self.restructuring_risk), debt)
        with np.errstate(divide="ignore", invalid="ignore"):
            owed = np.where(restructured, np.where(debt > 0, owed * written / debt, 0.0), owed)
        debt = written
        employed = n.sum()
        small = ~dominant
        small_n = max(n[small].sum(), 1e-300)
        by_industry = np.bincount(L.ind[closes], n[closes], k) / np.maximum(np.bincount(L.ind, n, k), 1e-300)
        earnings = n * np.maximum(L.e, 0.0)
        left = ~closes
        under = np.where(restructured, 0.0, under)
        changes = [SetAttribute(DEBT, debt, self.name), SetAttribute(INTEREST, owed, self.name),
                   SetAttribute(UNDER, under, self.name),
                   Publish("failures", float(closes.sum()), self.name),
                   Publish("failed_employees", float(n[closes].sum() / max(employed, 1e-300)), self.name),
                   # the sabotage module counts this next year as capacity that has left the industry
                   Publish("failed_by_industry", by_industry, self.name),
                   # the green-field module has the firms left in each industry hire this many next year
                   Publish("closed_employees", np.bincount(L.ind[closes], n[closes], k), self.name),
                   Publish("restructurings", float(restructured.sum()), self.name),
                   # the debt module reports these next year
                   Publish("interest_owed", float(interest[left].sum() / earnings[left].sum()) if earnings[left].sum() > 0 else 0.0,
                           self.name),
                   Publish("debt_owed", float(debt[left].sum()), self.name),
                   Publish("short_of_cover", float((n[small] * short[small]).sum() / small_n), self.name),
                   Publish("interest_cover", float(earnings[small].sum() / interest[small].sum())
                           if interest[small].sum() > 0 else 0.0, self.name)]
        if restructured.any():
            changes.append(Scale("risk", np.where(restructured, 1.0 + self.restructuring_risk, 1.0), self.name))
        if closes.any():
            changes.append(Dissolve(np.flatnonzero(closes), self.name))
        return changes
