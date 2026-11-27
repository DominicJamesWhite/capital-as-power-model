"""Optional module: price leaders and followers within an industry.

THE RULE IN PLAIN WORDS

Without this module every firm in an industry has the same markup. This module sorts the
firms into eight groups by size and lets the markups of the groups differ inside each
industry. It never changes the earnings of an industry as a whole. It only moves earnings
between the large firms and the small firms of the same industry.

  1. Eight size groups. The top group is dominant capital, the hundred largest firms. The
     seven groups below it are cut off at fixed fractions of the capitalization of the smallest
     firm in the top group. Each firm has a standing: 0 in the bottom group, 1 in the top
     group, and even steps between.
  2. Leading a rise. When the average price of an industry rose over the last year, the larger
     firms of that industry are taken to have led the rise and the smaller firms to have
     followed late and in part. The module sets the difference between the markup of a
     top-group firm and the markup of a bottom-group firm, as a fraction of the industry's
     markup, in proportion to the rate at which the industry's price rose. The difference
     lasts only while the price goes on rising. When the rise slows, the difference shrinks,
     and the large firms give back what they gained.
  3. Holding against a fall. When the average price of an industry fell over the last year,
     the larger firms are taken to keep their prices and the smaller firms to cut theirs.
     The module sets the difference between the price of a top-group firm and the price of a
     bottom-group firm equal to a part of the fall. A firm that keeps its price above the
     falling price of its industry loses employees that year in proportion to the price it
     keeps.

The module reads prices, markups, employees and capitalization from the ledger and remembers
the average price of each industry from the year before. It reads no account of another module.

WHAT IT RESTS ON

  - Chapter 12, "From price taking to price making". Gardiner Means found "not one but two
    types of prices": market prices, "relatively flexible ... and prevalent in competitive
    industries", and administered prices, "relatively inflexible, changing only infrequently,
    responding slowly to market conditions and typical of concentrated industries". In the
    Depression "competitive industries saw massive declines in their market prices, but only
    moderate drops in their output and employment", while in concentrated industries "prices
    declined slightly, while production and payroll collapsed". Part 3 of the rule applies
    this finding to the large and the small firms of one industry.
  - Chapter 12, "The markup and the target rate of return": "modern firms, particularly the
    leading ones, begin with a long-term target rate of profit, and then back-calculate the
    markup".
  - Chapter 16, "Small and large firms". The differential markup of the Fortune 500 "averaged
    1.6", and "dominant capital tended to beat the average when inflation rose and trail it
    when inflation fell". Nitzan's thesis "disaggregates US-based corporations into eight
    groups ranked by assets size, showing that the larger the firm, the greater and more
    systematic its differential gains from inflation". The largest firms "do not simply react
    passively; they take the initiative. They actively raise their prices, markup and profit
    per employee faster than the average".
  - Chapter 16, "Capitalization risk": the gains "are always short-lived: they last only as
    long as the underlying bout of inflation continues".
  - Nitzan, "Inflation as Restructuring" (1992), chapter 9. "The large corporations are the
    modern inflation makers, while the smaller firms operate as inflation takers." The first
    rises come from the core, and "these initial inflationary increases may be subsequently
    followed by smaller firms". The gains of smaller firms "are derived gains, crucially
    dependent on the inflation consensus among the large firms". The eight groups are those of
    the Quarterly Financial Reports, with "the following cuttoff levels: less than $5 million
    in assets, $5 to $10 million, $10 to $25 million, $25 to $50 million, $50 to $100 million,
    $100 to $250 million, $250 to $1 billion, and over $1 billion". For those groups "the
    relationship between inflation and the markup was much tighter for the largest firms than
    it was for the smaller ones". A footnote adds: "By treating the markup in each size
    category as a linear statistical function of a constant and PPI inflation, we found that
    both the estimated slope coefficient and as its associated significance level rose with
    corporate size." Part 2 of the rule is this linear relation.
  - The same chapter: "Direct firm-to-firm redistribution does not alter the labour share of
    income". The module moves earnings between firms and leaves the total of each industry
    unchanged.

WHAT IS ADDED

The literature gives the direction of each effect and no rates. It does not say how much of
the differential markup of large firms arises inside industries and how much arises from the
industries they sit in. The rule gives the large firms of an industry no standing advantage
when prices are still, because no passage supports a figure for one. Every number below is an
addition, with one exception: the cut-offs of the eight groups keep the proportions of the
thesis (5, 10, 25, 50, 100 and 250 million dollars against 1 billion). Placing the top group
at the hundred largest firms is the model's own convention. The even steps of standing
between the groups are an addition. The thesis compared markups with the general rate of
inflation in manufacturing, and the rule uses the price of each industry. Means compared
concentrated industries with competitive ones, and the rule applies his finding to large and
small firms inside one industry. The rule sets the difference in markups afresh each year
from the price movement of the year before.

HOW THE MODULE CHANGES THE LEDGER

The module owns one markup component, the size premium, and changes nothing else in any
firm's earnings. Each year it sets the size premium of every firm to the difference its
rule calls for. The premium is above 1 for a firm that stands above the average of its
industry and below 1 for a firm that stands below it. The size premium is a member of the
overlap group "hold on buyers", together with the premiums of the protections and wants
modules (see "How modules share a quantity" in modules.md). The module does not measure
the differences that other modules have left between the size groups of an industry, and it
does not remove them. The lead that the stagflation module gives the hundred largest firms
therefore stays in place beside this module's premium.
"""
import numpy as np
from core import Scale, SetComponent, Publish, top_positions, HOLD_ON_BUYERS

SIZE = "size premium"    # this module's markup component; a member of the overlap group "hold on buyers" (an addition)


class Leaders:
    name = "leaders"
    reads = ()
    supplies = ("leader_premium",)

    # The cut-offs of the eight size groups in Nitzan (1992, chapter 9), each as a fraction of
    # the cut-off of the top group: 5, 10, 25, 50, 100 and 250 million dollars against 1 billion.
    # Their use here is an addition. The thesis reports them as the asset classes, in dollars, of one
    # statistical report on manufacturing firms from 1973 to 1988. It does not give them as proportions
    # of the size of the hundredth largest firm, and the rule measures size by capitalization.
    CUTOFFS = np.array([0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 1.0])

    def __init__(self, lead=4.0, hold=1.0, volume_cost=0.5, most=1.0, floor=0.005, top=100, levels_others=False):
        self.lead = lead                # difference between the markups of a top-group and a bottom-group firm, as a fraction
                                        # of the industry's markup, per unit of yearly rise in the industry's price
                                        # (4 means 40 per cent of the industry's markup when its price rises 10 per cent a year)
        self.hold = hold                # part of a fall in the industry's price that a top-group firm does not follow
        self.volume_cost = volume_cost  # employees lost per unit of price kept above the industry's falling price
                                        # (the same figure as the cost of a price rise in the sabotage module)
        self.most = most                # the largest difference the rule will set, as a fraction of the industry's markup
        self.floor = floor              # a markup cannot fall below this (the same floor as in the sabotage module)
        self.top = top                  # the top group is this many of the largest firms
        self.levels_others = levels_others   # a switch for comparisons, off unless a run asks for it.
                                        # Off: the module sets its own difference and leaves alone the differences that other
                                        # modules left between the size groups of an industry. On: the premium also cancels
                                        # the difference by size that stands in the stacking part of the markups.
        self.last_price = None          # average price of each industry a year ago

    def start(self, L):
        L.add_component(SIZE, self.name, group=HOLD_ON_BUYERS)
        return {"leader_premium": 0.0}

    def standing(self, L):
        """0 for the bottom size group, 1 for the top group, in seven even steps."""
        K = L.cap()
        threshold = K[top_positions(K, np.arange(len(L)), self.top)].min()
        return np.searchsorted(self.CUTOFFS * threshold, K, side="right") / float(self.CUTOFFS.size)

    def propose(self, L, rng):
        k, ind, n = L.sector_of.size, L.ind, L.n
        n_j = np.bincount(ind, n, k)
        safe = np.maximum(n_j, 1e-12)
        price = np.where(n_j > 0, np.bincount(ind, L.p * n, k) / safe, 1.0)
        last, self.last_price = self.last_price, price
        if last is None:                 # the first year has no earlier price to compare with
            return [Publish("leader_premium", 0.0, self.name)]
        rise = np.where((n_j > 0) & (last > 0), price / np.maximum(last, 1e-12) - 1, 0.0)

        # The premium is reckoned against the part of the markup that stacks, so it does not depend on
        # any other premium in the same overlap group.
        r = L.stacking_markup()                                  # each firm's markup apart from every hold on buyers
        M = np.maximum(np.bincount(ind, n * r, k) / safe, 1e-12)  # each industry's markup, apart from every hold on buyers
        s = self.standing(L)
        s_mean = np.bincount(ind, n * s, k) / safe
        ds = s - s_mean[ind]                                     # standing against the industry's average
        spread = np.bincount(ind, n * ds * ds, k)
        mixed = spread > 1e-9 * safe                             # industries that hold more than one size group

        # The difference the rule sets: leading a rise, or holding against a fall.
        led = self.lead * np.maximum(rise, 0.0)
        held = self.hold * np.maximum(-rise, 0.0) * (1 + M) / M
        want = np.where(mixed, np.minimum(led + held, self.most), 0.0)
        held = np.minimum(held, want)

        # The module sets its own component and nothing else. The premium adds the difference the
        # rule calls for to the firm's markup apart from every hold on buyers. What the firms above the
        # industry's average standing gain, the firms below it lose.
        differ = want
        if self.levels_others:           # for comparisons: take off the difference by size that other modules left
            now = np.where(mixed, np.bincount(ind, n * ds * (r / M[ind] - 1), k) / np.maximum(spread, 1e-12), 0.0)
            differ = want - now
        size_premium = 1 + M[ind] * differ[ind] * ds / r
        size_premium = np.maximum(size_premium, np.minimum(1.0, self.floor / r))
        # A firm that keeps its price above a falling one gives up employees (Means).
        kept = np.maximum(M[ind] * held[ind] * ds, 0.0) / (1 + M[ind])
        premium = float((want * n_j).sum() / n_j.sum())
        # The price of each firm follows its markup: the core works it out from the wage and the
        # markup, and counts only the largest premium of the overlap group, as the markup does.
        return [SetComponent(SIZE, size_premium, self.name),
                Scale("employees", 1 - self.volume_cost * kept, self.name),
                Publish("leader_premium", premium, self.name)]
