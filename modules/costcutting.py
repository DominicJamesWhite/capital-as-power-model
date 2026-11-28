"""Module 5: cost cutting (Capital as Power, chapters 14 and 16).

Every firm tries to cut costs, and each year each firm draws a small gain in earnings per
employee. The gains do not last: methods spread and cheaper inputs become available to all, so
each firm's earnings per employee drift back toward the level of its industry. A large firm is many parts whose luck partly cancels
out, so its draw is smaller (Amaral and others, 1997: the spread of firms' yearly growth falls as size
to the power -0.18; the book: mergers "stabilize earnings growth", chapter 15). The luck of the draws
therefore does less for the largest firms. Cost cutting lets dominant capital "meet the average, not beat
it", and the module exists to show that.

The book gives no size for the draws and no speed for the spread. Both are unsourced. They are taken from a
study outside the tradition that measures something else: a plant's sales for each unit of all its inputs, where
the model spreads earnings for each employee (see modules.md). Syverson, "What determines productivity?" (2011): within industries "the average difference in
logged total factor productivity (TFP) between an industry's 90th and 10th percentile plants is 0.651", and
the yearly persistence is "on the order of 0.6 to 0.8". In terms of power: for the same people and plant one
firm obtains almost twice what a neighbour obtains, and the difference fades as methods spread. The draws
are sized each year so that all the firms of an industry, large and small together, lie that far apart once
the drift back has acted. They are also what sets a firm
behind its neighbours, so that some firms come to owe more than they are worth (see the failure module).

The module owns one markup component, the cost-cutting edge. The drift back is reckoned on the
part of a firm's markup that stacks (see "How modules share a quantity" in modules.md). Premiums
that rest on a hold on buyers, and income that is not a markup, do not drift back. That choice is
an addition.

The module also owns one cost component, the cost difference. Chapter 16 writes earnings per
employee as "(unit price - unit cost) x units per employee" and lists "lowering unit cost faster
than the average" as a route apart from "increasing unit price faster than the average". Cutting
costs therefore moves a firm's earnings and leaves its price where it was. The core works the
price out as cost plus markup, so the module has to say which of its movements are movements of
cost. It does so in two steps, and both are additions, because the book gives no rule.

  1. The yearly draw is a movement of cost. A firm that draws a gain has lower costs, and its
     cost difference falls by the amount its markup rose. Its price does not move.
  2. The drift back first removes the cost difference that stands. A firm whose costs are below
     those of its industry loses that saving as "improvements ... proliferate". The drift back
     takes away no more saving than the firm has, and it turns no saving into a lag. Whatever
     the drift back moves beyond that is a movement of the firm's price toward the prices of
     its industry. This matters for a firm that stands above its industry for another reason,
     such as the lead from price rises: the wearing away of that lead is a fall of its price
     against the wage, and not a rise of its costs.
"""
import numpy as np
from core import ScaleComponent, SetComponent, squeeze

# What still stands of a firm's edge over its industry from cutting costs, or of its lag behind
# it. A markup component that stacks. The drift back toward the industry is proposed to this
# component; the core then takes it out of whatever gain or loss it wears away (Model._net).
EDGE = "cost-cutting edge"

# The cost difference: the amount, for each employee and counted in wages, by which the firm's
# cost stands above or below the wage as a result of its yearly draws. Below 0: the firm has cut
# its costs and the saving still stands. Above 0: the firm lags. A cost component.
COST = "cost difference"


def normal_below(z):
    """The part of a normal distribution with mean 0 and spread 1 that lies below z, from the approximation to the error
    function in Abramowitz and Stegun (1964), 7.1.26, which is out by less than 1.5e-7."""
    a = np.abs(z) / np.sqrt(2.0)
    t = 1.0 / (1.0 + 0.3275911 * a)
    erf = 1.0 - t * (0.254829592 + t * (-0.284496736 + t * (1.421413741 + t * (-1.453152027 + t * 1.061405429)))) * np.exp(-a * a)
    return 0.5 * (1.0 + np.sign(z) * erf)


class CostCutting:
    name = "cost cutting"
    reads = ()
    supplies = ()
    figures = {}           # nothing it supplies is a single yearly figure

    def __init__(self, gap=0.651, spread=0.3, size_scale=0.18, whole_spread=True, gain=0.18, wears_holds=False):
        self.gap = gap          # how far apart the firms of one industry lie, in logarithms of their markups, between the
                                # 90th and the 10th percentile: Syverson (2011) finds 0.651 between the plants of one industry
        self.spread = spread    # part of any difference from the industry that disappears each year: 1 less the
                                # yearly persistence of 0.6 to 0.8 that Syverson (2011) reports
        self.whole_spread = whole_spread   # on: each year the draws are sized so that all firms together, large and small,
                                           # lie `gap` apart once the drift back has acted (step 1b). Off, kept for
                                           # comparisons: the firm of median size draws `gain`
        self.gain = gain        # with `whole_spread` off, the yearly gain or loss of a firm of median size, in logarithms of its
                                # markup: 0.651 is a spread of 0.254, and 0.254 x sqrt(1 - 0.7 x 0.7) = 0.18
        self.size_scale = size_scale   # how fast the draw shrinks with the size of a firm, against the typical (median)
                                       # firm: Amaral and others (1997) find the spread of firms' yearly growth falls as
                                       # size to the power -0.18 +/- 0.03, measured in employees. Independent parts
                                       # would give 0.5; 0 gives every firm the same draw
        self.wears_holds = wears_holds   # a switch for comparisons, off unless a run asks for it.
                                         # Off: the drift back is reckoned on the part of the markup that stacks, so a
                                         # premium that rests on a hold on buyers is not worn down. On: the drift back is
                                         # reckoned on the whole markup, premiums included.

    def typical_gain(self, shrink):
        """The draw of a firm of median size that sets all firms `gap` apart (step 1b). A firm whose draws have a spread
        g x shrink, and which loses `spread` of its difference each year, settles at a spread of g x shrink / sqrt(1 - p^2),
        where p = 1 - spread. All firms together are a mixture of such spreads. The point x that 90 per cent of that mixture
        lies below is found by halving, for g = 1, and g is then gap / (2 x)."""
        settle = np.sqrt(1.0 - (1.0 - self.spread) ** 2)
        low, high = 0.0, 10.0 * shrink.max()
        for _ in range(60):
            x = 0.5 * (low + high)
            if normal_below(x / shrink).mean() < 0.9:
                low = x
            else:
                high = x
        return self.gap * settle / (2.0 * 0.5 * (low + high))

    def start(self, L):
        L.add_component(EDGE, self.name)
        L.add_component(COST, self.name, kind="cost")
        return {}

    def propose(self, L, rng):
        k = L.sector_of.size
        # The drift back is reckoned on the part of the markup that stacks: the base, the lead from
        # price rises and this module's own edge. Premiums that rest on a hold on buyers (an overlap
        # group) and income that is not a markup are left alone: the spread of methods does not
        # wear them down. The whole change is made to this module's own component.
        m = L.markup() if self.wears_holds else L.stacking_markup()
        level = np.bincount(L.ind, L.n * m, k) / np.maximum(np.bincount(L.ind, L.n, k), 1e-12)
        back = (level[L.ind] / m) ** self.spread
        # A firm is many parts, and the luck of its parts partly averages out: the typical (median) firm draws a gain g,
        # and a firm k times its size draws g / k^size_scale (step 1a). A firm with no employees has no parts to average.
        # g is set so that all the firms together lie as far apart as Syverson's plants (step 1b), so firms smaller
        # than the median lie further apart than that and larger firms closer.
        n = L.n
        typical = np.median(n[n > 0]) if (n > 0).any() else 1.0
        parts = np.where(n > 0, n / typical, 1.0)
        shrink = parts ** -self.size_scale
        gain = self.typical_gain(shrink) if self.whole_spread else self.gain
        draw = np.exp(rng.normal(0.0, gain, len(L)) * shrink)
        # The edge stacks, so the firm's whole markup moves by the same factor as the edge. The
        # movement is divided into the draw and the drift back, each as an amount in wages.
        whole = L.markup()
        drawn = whole * (draw - 1.0)                   # step 1: the draw is a movement of cost
        drift = whole * draw * (back - 1.0)            # the drift back, reckoned after the draw
        # A saving is taken out of the firm's cost of production, the wage and this module's own cost difference,
        # as a part of it, by the core's rule for a fall (squeeze), so that cost is never cut through nothing. Other
        # costs, such as an outlay on wants, are not costs of production and are not cut. A small saving comes to
        # almost the whole draw. What a large saving leaves of the draw is a rise of the firm's price, because the
        # core adds markup and cost.
        unit = 1.0 + L.components[COST]
        cost = squeeze(unit, -drawn) - 1.0
        # step 2: the drift back removes the cost difference that stands, and no more than stands.
        # A drift downward removes a saving (a cost below 0); a drift upward removes a lag (a cost
        # above 0). The rest of the drift moves the price, because the core adds markup and cost.
        removes = (drift * cost) > 0
        removed = np.where(removes, np.sign(drift) * np.minimum(np.abs(drift), np.abs(cost)), 0.0)
        return [ScaleComponent(EDGE, back * draw, self.name),
                SetComponent(COST, cost - removed, self.name)]
