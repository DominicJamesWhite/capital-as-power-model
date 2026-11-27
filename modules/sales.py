"""Optional module: what can be sold.

THE RULE IN PLAIN WORDS

Every year the claims offer goods at their going prices. The value offered is the wage bill plus
the earnings that the claims price for. The module adds up the money that comes back to buy
those goods, by who spends it:

  1. Wages are all spent.
  2. Capitalists spend a fixed part of their income on their own consumption.
  3. The rest of capitalist income is money for expansion. It buys goods only when it is spent
     on new capacity, and new capacity costs a fixed number of years of wages for each new job.
     Money that pays for existing claims (mergers) buys no goods, and neither does money for
     which there is no new job to equip.

The part of the value offered that no money comes back for is the unsold part. It is never
negative, because nobody in this account spends more than an income. The unsold part then
falls on the claims in two different ways, following Gardiner Means:

  - In the part of an industry that dominant capital does not hold, sellers cut prices. The
    markup and the price fall, and employment is left to the sabotage rule.
  - In the part that dominant capital holds, prices are kept. The claims of dominant capital
    dismiss employees in proportion to the unsold part, except for the overhead staff, who
    cannot be dismissed in step with sales. Because the overhead cost stays, earnings per
    employee fall there too, although the price does not.

Dismissals lower the wage bill, and lower markups stop small claims from hiring, so less is
built the next year and still less money comes back. A fall can therefore feed on itself. It
ends because the unsold part shrinks with capitalist income: when markups are low there is
little unspent capitalist income left.

WHAT IT RESTS ON

  - Chapter 12, "Business as usual": "When business sabotage becomes excessive, pushing output
    toward the zero mark, the result is recession and low capitalist earnings." Figure 12.2
    shows "the negative effect on business ... of excessive industrial sabotage until the early
    1940s". The 2014 note "Nonlinearities of the Sabotage-Redistribution Process" gives the
    slope: before the war "sabotage was excessive and unemployment undermined the capitalist
    share of income (regression slope = -0.35)".
  - Chapter 12, "From price taking to price making": in the Depression "competitive industries
    saw massive declines in their market prices, but only moderate drops in their output and
    employment", while in concentrated industries "prices declined slightly, while production
    and payroll collapsed, sometimes by as much as 80 per cent".
  - Chapter 12, "The markup and the target rate of return": firms calculate "the cost at
    'normal' levels of output", add "a 'conventional' markup", and keep the price "stable in the
    face of cyclical variations in demand". "In sum" speaks of "a target rate of return at some
    standard capacity utilization". A price reckoned on normal output earns less than its
    markup when sales are below normal, because some costs do not fall with sales.
  - Chapter 15, "Tobin's Q": "glut means the disintegration of full-cost pricing; and if prices
    end up dropping faster than costs, the consequence is falling profit".
  - Chapter 14, Proposition 3, and chapter 15: the shift "from building to buying" has as its
    "broader consequence ... creeping stagnation".
  - "Can Capitalists Afford Recovery?" (2014), section "Underconsumption": workers "spend most
    if not all of that income on consumption", capitalists "save most of it", and so, on
    Kalecki's argument, the higher "the income share of capital" the greater "the tendency
    toward deficient demand and stagnation". The authors report this argument and say that
    their Figure 11 "certainly seems consistent" with it. They do not adopt it as their own.

WHAT IS ADDED

The book gives no account of how much can be sold. A footnote to chapter 14 calls the notion of
excess capacity "admittedly problematic". The whole account of spending above is therefore an
addition, taken from the argument of Kalecki as the authors report it, and joined to the book's
distinction between building and buying. Every number is an addition: the part of their income
that capitalists consume, the cost of equipping a new job, the part of the unsold value that
sellers take out of their prices within a year, the part of costs that is overhead, and the
number of years of hiring and buying over which spending on expansion is reckoned. (Reckoning
it on one year made the model lurch between selling everything and selling far too little.) The
unsold part is taken to be the same in every industry, because the model has no account of
what buyers want and must not have one that rests on utility. The money paid for acquired
claims is reckoned at the average capitalization per employee of the claims outside dominant
capital. Sellers of acquired claims are capitalists, and the rule treats what they receive as
unspent.
"""
import numpy as np
from core import ScaleComponent, SetComponent, Publish, top_positions

# This module's markup component: the part of the markup given up for want of sales that has not
# been recovered since. A later rise of the claim's markup, from any rule, restores this component
# first (see Model._net in core.py). It stacks.
UNSOLD = "unsold goods"

# This module's cost component: the overhead that sellers who keep their prices carry on goods
# they did not sell, for each employee and counted in wages. Chapter 12 says such sellers reckon
# their price on "the cost at 'normal' levels of output" and keep it "stable in the face of
# cyclical variations in demand", so a fall in sales raises their cost and not their price. The
# component is the running sum of the yearly rises. The rule has no recovery of its own, so
# nothing is taken off it (backlog items 45 and 47).
OVERHEAD = "idle overhead"


class Sales:
    name = "sales"
    reads = ("new_hires",)
    supplies = ("unsold", "sales_cut", "build_money_share")

    def __init__(self, consumed=0.4, job_cost=4.0, price_give=0.5, overhead=0.3, years=3,
                 floor=0.005, top=100):
        self.consumed = consumed      # part of capitalist income spent on capitalists' own consumption ("save most of it")
        self.job_cost = job_cost      # money spent on new capacity for each new job, in years of the wage
        self.price_give = price_give  # part of the unsold value that price-cutting sellers take out of their markups within a year
        self.overhead = overhead      # part of a price-holding claim's costs that does not fall when its sales fall
        self.years = years            # years of hiring and buying over which spending on expansion is reckoned
        self.floor = floor            # a markup cannot fall below this (the same floor as in the sabotage module)
        self.top = top
        self.started = False
        self.hired, self.bought = [], []   # recent hiring and buying, each as a fraction of employment

    def start(self, L):
        L.add_component(UNSOLD, self.name)
        L.add_component(OVERHEAD, self.name, kind="cost")
        return {"unsold": 0.0, "sales_cut": 0.0, "build_money_share": 1.0}

    def unsold(self, L, dominant):
        """The part of the value offered that no spending comes back for, and the part of
        expansion money that was spent on new capacity."""
        A = L.accounts
        wage, employed = L.shared["wage"], L.n.sum()
        wages = wage * employed
        earnings = L.earnings().sum()
        expansion_money = (1 - self.consumed) * earnings
        build = self.job_cost * wage * max(float(np.mean(self.hired)), 0.0) * employed   # what recent new jobs cost to equip
        acquired = float(np.mean(self.bought)) * employed                       # employees bought, not hired
        price_per_employee = L.cap()[~dominant].sum() / max(L.n[~dominant].sum(), 1e-12)
        buy = acquired * price_per_employee                                     # what recent acquisitions cost
        if build + buy <= 0 or expansion_money <= 0:
            spent_on_capacity = 0.0
        else:       # building and buying share the money when together they would take more than there is
            spent_on_capacity = min(build, expansion_money * build / (build + buy))
        left = max(expansion_money - spent_on_capacity, 0.0)
        share = spent_on_capacity / expansion_money if expansion_money > 0 else 1.0
        return left / (wages + earnings), share

    def propose(self, L, rng):
        if not self.started:
            self.started = True      # the first year has no record of hiring to read
            return [Publish("unsold", 0.0, self.name), Publish("sales_cut", 0.0, self.name),
                    Publish("build_money_share", 1.0, self.name)]
        self.hired = (self.hired + [float(L.accounts["new_hires"]) / L.n.sum()])[-self.years:]
        self.bought = (self.bought + [float(L.accounts.get("merger_volume", 0.0))])[-self.years:]
        k = L.sector_of.size
        dominant = np.zeros(len(L), dtype=bool)
        dominant[top_positions(L.cap(), np.arange(len(L)), self.top)] = True
        x, share = self.unsold(L, dominant)

        n = np.bincount(L.ind, L.n, k)
        safe = np.maximum(n, 1e-12)
        held = np.bincount(L.ind[dominant], L.n[dominant], k) / safe
        markup = np.where(n > 0, np.bincount(L.ind, L.markup_earnings(), k) / (L.shared["wage"] * safe), 1.0)

        # Sellers who cut prices: the markup and the price fall together.
        price_cut = (1 - held) * self.price_give * x * (1 + markup)
        # Sellers who hold prices: the price stays, but overhead is spread over fewer sales.
        cost_rise = held * self.overhead * x * (1 + markup)
        new = np.maximum(markup - price_cut - cost_rise, np.minimum(markup, self.floor))
        after_price = np.maximum(markup - price_cut, np.minimum(markup, self.floor))
        # The core works the price out from the wage, the markup and the costs. The whole fall of
        # the markup would therefore lower the price. The part that comes from overhead is a rise of
        # cost at a kept price, so it is entered as a cost of the same amount. Each claim's markup
        # moves in the proportion of its industry's, and so does its cost.
        carried = L.markup() * ((after_price - new) / markup)[L.ind]
        return [ScaleComponent(UNSOLD, (new / markup)[L.ind], self.name),
                SetComponent(OVERHEAD, L.components[OVERHEAD] + carried, self.name),
                Publish("unsold", float(x), self.name),
                # dominant claims dismiss in proportion to the unsold part, overhead staff excepted;
                # the green-field module subtracts this from their hiring rate next year
                Publish("sales_cut", float(x * (1 - self.overhead)), self.name),
                Publish("build_money_share", float(share), self.name)]
