"""Module 6: stagflation (Capital as Power, chapter 16).

Inflation is a struggle over distribution carried out through prices. When the compass raises
the intensity, the firms of dominant capital raise their prices. Other firms raise theirs by
part of that amount, and wages rise by another part. A firm gains when its price rises faster
than wages. The module also cuts hiring, and that cut is the crisis: the book says the
conditions inflation needs "have to be actively created and instituted by the key players".
Inflation raises the risk of dominant capital, and it feeds resistance.

Additions to the book: the size of the price rises, the parts obtained by small firms and by
wages, the cut in hiring, and the rise in risk.
"""
import numpy as np
from core import Scale, ScaleComponent, Set, Publish, top_positions, squeeze

# The part of what a firm's price rises gained it over wages that still stands. The book says the
# gains "last only as long as the underlying bout of inflation continues" (chapter 16,
# "Capitalization risk"). A later fall of the firm's markup, from any rule, is taken out of this
# component first (see Model._net in core.py). A markup component that stacks.
LEAD = "stagflation lead"


class Stagflation:
    name = "stagflation"
    reads = ("stagflation_intensity", "unemployment")
    supplies = ("crisis", "inflation_push")
    figures = {                   # what the workbench calls each published number: label, unit, note
        "crisis": ("Cut in hiring from stagflation", "rate", "The cut in every hiring rate in the year."),
        'inflation_push': ('Price rise by the top 100', 'rate', "Yearly price rise by the top 100's firms."),
    }

    def __init__(self, max_rise=0.10, small_part=0.6, wage_part=0.5, crisis=0.06, risk_rise=0.5,
                 catch_up=0.03, slack=2.0, usual_unemployment=0.05, top=100):
        self.max_rise = max_rise      # yearly price rise by dominant firms at full intensity
        self.small_part = small_part  # part of that rise that other firms obtain
        self.wage_part = wage_part    # part that wages obtain; near 1 where labour is strong
        self.crisis = crisis          # cut in every hiring rate at full intensity
        self.risk_rise = risk_rise    # rise in dominant capital's risk per unit of its price rise
        self.catch_up = catch_up      # yearly rise in the part small firms obtain while a bout lasts
        self.slack = slack            # fall in the part wages obtain per unit of unemployment above usual
        self.usual_unemployment = usual_unemployment
        self.years = 0                # how long the present bout has lasted
        self.top = top

    def start(self, L):
        L.add_component(LEAD, self.name)
        return {"crisis": 0.0, "inflation_push": 0.0}

    def propose(self, L, rng):
        x = max(L.accounts["stagflation_intensity"], L.accounts.get("conflict_spark", 0.0))   # a coalition's spark (another module)
        x = x * (1 - L.accounts.get("eruption_stops_price_rises", 0.0))   # an eruption suspends concerted price rises (another module); 0 without it
        changes = [Publish("crisis", self.crisis * x, self.name),
                   Publish("inflation_push", self.max_rise * x, self.name)]
        self.years = self.years + 1 if x > 0 else 0
        if x <= 0:
            return changes
        dominant = np.zeros(len(L), dtype=bool)
        dominant[top_positions(L.cap(), np.arange(len(L)), self.top)] = True
        push = self.max_rise * x
        # The strength of organised labour (another module) takes the place of popular resistance here.
        resistance = min(1.0, L.accounts.get("labour_strength", L.accounts.get("resistance", 0.0)))
        # The parts are not fixed: the outcome depends on "the relative power of the leading firms,
        # capital in general and labour groups" (chapter 16). Wages do better where resistance is
        # high and worse where unemployment is high; other firms catch up as the bout goes on.
        weak = self.slack * max(0.0, L.accounts["unemployment"] - self.usual_unemployment)
        wage_part = np.clip(self.wage_part + (1 - self.wage_part) * resistance - weak, 0.0, 1.0)
        small_part = min(1.0, self.small_part + self.catch_up * self.years)
        wage_rise = push * wage_part
        price_rise = np.where(dominant, push, push * small_part)
        wage = L.shared["wage"]
        # The rule moves prices, so it works on the markup that each firm's price asks. Where goods were unsold
        # (another module), a firm received less than that this year, and the part it did not receive is no
        # part of its price.
        markup = L.priced_markup()
        # The new markup is the one at which the firm's wage and markup together have risen by its price
        # rise. Where wages rise faster than the price, the firm's margin bears the difference, and a fall
        # is taken out of the margin as a part of what is left (squeeze in core.py).
        new_markup = squeeze(markup, (1 + markup) * ((1 + price_rise) / (1 + wage_rise) - 1))
        # The markup changes through this module's own component. The core works out earnings per
        # employee and the price from the new wage and the new markup, so the price rises by the firm's
        # price rise, or a little more where its margin was squeezed. (A firm that carries a named cost of another
        # module sees that cost rise with the wage and not with the price.) At the end of the year
        # the core keeps in the component only the part of the gain that no fall of the markup has
        # taken away.
        changes += [ScaleComponent(LEAD, new_markup / markup, self.name),
                    Scale("risk", np.where(dominant, 1 + self.risk_rise * push, 1.0), self.name),
                    Set("wage", wage * (1 + wage_rise), self.name)]
        return changes
