"""Module 5: cost cutting (Capital as Power, chapters 14 and 16).

Every firm tries to cut costs, and each year each firm draws a small gain in earnings per
employee. The gains do not last: methods spread and cheaper inputs become available to all, so
each firm's earnings per employee drift back toward the level of its industry. The size of the
draw does not depend on the size of the firm. Cost cutting therefore lets dominant capital
"meet the average, not beat it", and the module exists to show that.

Additions to the book: the size of the draws and the speed at which gains spread.

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
from core import ScaleComponent, SetComponent

# What still stands of a firm's edge over its industry from cutting costs, or of its lag behind
# it. A markup component that stacks. The drift back toward the industry is proposed to this
# component; the core then takes it out of whatever gain or loss it wears away (Model._net).
EDGE = "cost-cutting edge"

# The cost difference: the amount, for each employee and counted in wages, by which the firm's
# cost stands above or below the wage as a result of its yearly draws. Below 0: the firm has cut
# its costs and the saving still stands. Above 0: the firm lags. A cost component.
COST = "cost difference"


class CostCutting:
    name = "cost cutting"
    reads = ()
    supplies = ()
    figures = {}           # nothing it supplies is a single yearly figure

    def __init__(self, gain=0.02, spread=0.3, wears_holds=False):
        self.gain = gain        # typical yearly gain or loss of one firm against its neighbours
        self.spread = spread    # part of any difference from the industry that disappears each year
        self.wears_holds = wears_holds   # a switch for comparisons, off unless a run asks for it.
                                         # Off: the drift back is reckoned on the part of the markup that stacks, so a
                                         # premium that rests on a hold on buyers is not worn down. On: the drift back is
                                         # reckoned on the whole markup, premiums included.

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
        draw = np.exp(rng.normal(0.0, self.gain, len(L)))
        # The edge stacks, so the firm's whole markup moves by the same factor as the edge. The
        # movement is divided into the draw and the drift back, each as an amount in wages.
        whole = L.markup()
        drawn = whole * (draw - 1.0)                   # step 1: the draw is a movement of cost
        drift = whole * draw * (back - 1.0)            # the drift back, reckoned after the draw
        cost = L.components[COST] - drawn
        # step 2: the drift back removes the cost difference that stands, and no more than stands.
        # A drift downward removes a saving (a cost below 0); a drift upward removes a lag (a cost
        # above 0). The rest of the drift moves the price, because the core adds markup and cost.
        removes = (drift * cost) > 0
        removed = np.where(removes, np.sign(drift) * np.minimum(np.abs(drift), np.abs(cost)), 0.0)
        return [ScaleComponent(EDGE, back * draw, self.name),
                SetComponent(COST, cost - removed, self.name)]
