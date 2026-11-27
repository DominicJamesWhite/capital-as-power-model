"""Optional module: what can be sold.

THE RULE IN PLAIN WORDS

The main modules take it that firms sell all they offer. This module keeps an account of
who buys. Once a year it adds up, for the year just ended, the money that each party had and
what that money bought. The account is kept in money: what firms offer is the wage bill plus
the earnings they priced for.

  1. Wage earners buy with all the money they have: the wage bill, plus the payments they
     received, less the taxes and interest they paid, plus what households borrowed, less what
     they paid back.
  2. The government buys with what it collected in the year and did not pay out.
  3. Owners lay out on goods what they received the year before, kept level against the wage,
     and on top of that they pay for the equipment of the year's new jobs. Owners here are the
     owners of the firms and every party that receives payments as a holder of debt.

What is left is unsold. Unsold goods are income to nobody: the wages were paid, so the whole
shortfall falls on owners, and their money income of the year is the priced earnings less the
unsold amount. That lower income is what they lay out the next year.

Owners then respond, and each response lowers the unsold amount:

  - Every firm loses the same part of its priced earnings.
  - A firm outside dominant capital takes half of its loss out of its price, where it stays
    until a later rise restores it. It books the other half once, on the next year's earnings.
  - A firm of dominant capital keeps its price and books its whole loss once. It holds back
    production: its hiring rate falls by the unsold part. It seeks the same number of
    employees by buying firms.

When nothing is unsold, none of these happens. The module also reports each year whether the
two conditions of accumulation hold: differential capitalization that is not falling, and a
capitalist share of income that is not falling.

WHAT IT RESTS ON

  - "Can Capitalists Afford Recovery?" (2014): "a crisis of accumulation is not a crisis of
    production or consumption, but a crisis of capitalist power", and "for capitalists,
    redistribution is not a means to an end, but the end itself". The two conditions: "The
    first and key condition is non-negative differential accumulation", and "The second
    condition is a steady or rising capital share of income". "A significant violation of one
    or both criteria brings the threat of a major capitalist crisis."
  - Chapter 12, "Business as usual": "When business sabotage becomes excessive, pushing output
    toward the zero mark, the result is recession and low capitalist earnings."
  - Chapter 12, "From price taking to price making": in the Depression "competitive industries
    saw massive declines in their market prices, but only moderate drops in their output and
    employment", while in concentrated industries "prices declined slightly, while production
    and payroll collapsed".
  - Chapter 14, Proposition 3, on the threat of excess capacity: "Mergers and acquisitions
    alleviate the problem whereas greenfield aggravates it." Chapter 15: "the large
    accumulators have learned to 'manage' this stagnation for their own ends".

WHOSE ARGUMENT THE ACCOUNT IS

The argument that goods stay unsold because owners do not spend their income belongs to
Michal Kalecki and to Paul Baran and Paul Sweezy. Nitzan and Bichler report it (chapter 4,
"Realization and institutionalized waste"; the 2014 paper, "Underconsumption") and do not
adopt it. The paper says that workers "spend most if not all of that income on consumption"
and that capitalists "save most of it", and that its Figure 11 "certainly seems consistent"
with the argument. It then asks what a crisis is, and answers with the two conditions above.

WHAT IS ADDED

The book gives no account of how much can be sold. Everything here is an addition: the account
itself; that owners lay out what they received the year before; that the equipment of a new
job is bought on top of it, and what it costs; that the shortfall falls on every firm in
proportion to its priced earnings; how far small sellers cut prices; that dominant capital
cuts its hiring by the unsold part and buys firms in place of the jobs; and the number of
years over which the two conditions are judged.

One choice changes what the model says. A single owner saves, and the paper reports that
owners "save most" of their income. But money saved is handed to somebody: to the seller of a
firm, to a borrower, to a builder. The model has no rule by which owners as a class keep
money idle for good, so by default they do not (`hoarded` is 0), and goods stay unsold only
when priced earnings run ahead of what owners lay out. A value of `hoarded` above 0 is the
reading of Kalecki and of Baran and Sweezy: that part of owners' income buys nothing, ever.

WHAT IS LEFT OUT

Costs other than the wage are in prices and are paid to nobody the model follows; they are
left out of both sides of the account. Money paid for firms that are bought, and money that
dominant capital pays for public services, pass from owners to owners (the government retires
debt with it), so they buy no goods and take none away. The gain from burdens off the books
(optional module) is paid by nobody and is not counted as money that owners have. Military
orders (optional module) have no recorded payer, so the goods made for them are counted like
any others. People in publicly run employment are outside the list of firms and outside the
account.
"""
import numpy as np
from core import ScaleComponent, SetComponent, Publish, top_positions, WAGE_EARNERS, GOVERNMENT

# The part of a firm's markup given up by cutting its price for want of sales, as far as no later
# rise has restored it. A later rise of the firm's markup, from any rule, restores this component
# first (see Model._net in core.py). It stacks.
PRICE_CUT = "unsold goods"

# The part of its priced earnings that a firm receives this year, after the loss it books for the
# goods left unsold the year before. A level: the module sets it afresh every year, and it is 1 when
# everything was sold. It multiplies the markup. It is the only member of an overlap group of its
# own, so the core does not cancel it against other gains and losses. The sabotage module divides
# it out again, because its rule works on the markup that firms price for.
SHORTFALL = "sales shortfall"

# A cost component: what the firm laid out on the goods it did not sell, for each employee and
# counted in wages. It equals what the shortfall takes from the markup, so the price does not move.
CARRIED = "unsold goods carried"


class Sales:
    name = "sales"
    reads = ("jobs_created", "party_flows", "capital_share")
    supplies = ("unsold", "sold_part", "sales_cut", "bought_not_built", "sales_account",
                "accumulation_differential", "accumulation_share", "crisis_of_capital")
    figures = {                   # what the workbench calls each published number: label, unit, note
        "unsold": ("Unsold part", "share", "Part of the value that firms offered last year that nobody bought."),
        "sold_part": ("Priced earnings received", "share", "Part of the earnings that firms priced for last year that owners received."),
        "sales_cut": ("Hiring held back for unsold goods", "rate", "Fall in the hiring rate of the top 100 firms because goods were unsold."),
        "bought_not_built": ("Buying in place of building", "rate", "Employees that a top 100 firm seeks by buying firms in place of jobs it held back, as a part of its own."),
        "accumulation_differential": ("Differential accumulation holds", "index", "1 if differential capitalization has not fallen over the years judged, 0 if it has."),
        "accumulation_share": ("Capitalist share holds", "index", "1 if the capitalist share of income has not fallen over the years judged, 0 if it has."),
        "crisis_of_capital": ("Crisis for capital", "index", "1 if either condition of accumulation fails, 0 if both hold."),
    }

    def __init__(self, job_cost=4.0, price_give=0.5, held_back=1.0, buy_instead=1.0, hoarded=0.0,
                 judged_over=5, significant=0.01, top=100):
        self.job_cost = job_cost        # money spent on equipment for each new job, in years of the wage
        self.price_give = price_give    # part of its shortfall that a price-cutting seller takes out of its markup within a year
        self.held_back = held_back      # fall in the hiring rate of a firm of dominant capital per unit of the unsold part
        self.buy_instead = buy_instead  # employees that such a firm seeks by purchase for each job it holds back
        self.hoarded = hoarded          # part of owners' money income that is never laid out on anything
        self.judged_over = judged_over  # years over which each condition of accumulation is judged
        self.significant = significant  # a fall smaller than this part of the level counts as steady
        self.top = top
        self.standard = None            # what owners received last year, in years of the wage
        self.carried = {WAGE_EARNERS: 0.0, GOVERNMENT: 0.0}   # money that found no goods to buy last year
        self.dk, self.share = [], []    # differential capitalization and the capitalist share, year by year
        self.account = {}               # the last account, in money

    def start(self, L):
        L.add_component(PRICE_CUT, self.name)
        L.add_component(SHORTFALL, self.name, group=SHORTFALL)
        L.add_component(CARRIED, self.name, kind="cost")
        return {"unsold": 0.0, "sold_part": 1.0, "sales_cut": 0.0, "bought_not_built": 0.0, "sales_account": {},
                "accumulation_differential": 1.0, "accumulation_share": 1.0, "crisis_of_capital": 0.0}

    def reckon(self, L, asked):
        """The account of the year just ended, in money. Returns it as a dictionary."""
        A = L.accounts
        wage, n = L.shared["wage"], L.n
        wages = float(wage * n.sum())
        priced = float((n * wage * asked).sum())          # the earnings that the firms priced for
        offered = wages + priced
        if self.standard is None:                         # at the start, owners lay out what the opening prices give them
            self.standard = priced / wage

        flows = A.get("party_flows", {})
        net = {p: f["received"] - f["paid"] for p, f in flows.items()}
        holders = sum(flows[p]["received"] for p in sorted(flows) if p not in (WAGE_EARNERS, GOVERNMENT))
        to_firms = sum(float((n * L.components[name]).sum())           # what firms received less what they paid
                       for name in sorted(L.info) if L.info[name].settled)
        lent, repaid = float(A.get("household_debt_lent", 0.0)), float(A.get("household_debt_repaid", 0.0))

        # What each party had to spend.
        has_wages = max(wages + net.get(WAGE_EARNERS, 0.0) + lent - repaid, 0.0) + self.carried[WAGE_EARNERS]
        has_government = max(net.get(GOVERNMENT, 0.0), 0.0) + self.carried[GOVERNMENT]
        building = self.job_cost * wage * float(A.get("jobs_created", 0.0))
        outlay = (1.0 - self.hoarded) * self.standard * wage

        # What each bought. Wage earners and the government spend all they have. If that is more than
        # everything offered, each buys in proportion and keeps the rest of its money for next year.
        first = has_wages + has_government
        part = min(1.0, offered / first) if first > 0 else 1.0
        by_wages, by_government = has_wages * part, has_government * part
        self.carried = {WAGE_EARNERS: has_wages - by_wages, GOVERNMENT: has_government - by_government}
        rest = max(offered - by_wages - by_government, 0.0)
        by_owners = min(outlay + building, rest)
        unsold = rest - by_owners
        if unsold < 1e-12 * offered:                      # a rounding error is not unsold goods
            by_owners, unsold = rest, 0.0
        income = priced - unsold + to_firms + holders     # owners' money income of the year
        self.standard = income / wage
        return {"offered": offered, "wages": wages, "priced_earnings": priced,
                "bought_by_wage_earners": by_wages, "bought_by_government": by_government,
                "bought_by_owners": by_owners, "unsold": unsold,
                "wage_earners_had": has_wages, "government_had": has_government,
                "owners_had": income + repaid - lent, "owners_income": income,
                "owners_outlay": outlay, "building": building, "lent": lent, "repaid": repaid,
                "kept_for_next_year": self.carried[WAGE_EARNERS] + self.carried[GOVERNMENT]}

    def conditions(self, L, top):
        """Whether each of the two conditions of accumulation holds over the last `judged_over` years."""
        K = L.cap()
        self.dk.append(float(K[top].mean() / K.mean()))
        self.share.append(float(L.accounts["capital_share"]))
        if len(self.dk) <= self.judged_over:
            return 1.0, 1.0
        dk_then, share_then = self.dk[-1 - self.judged_over], self.share[-1 - self.judged_over]
        differential = float(np.log(self.dk[-1] / dk_then) >= -self.significant)
        share = float(self.share[-1] >= share_then * (1.0 - self.significant))
        return differential, share

    def propose(self, L, rng):
        top = top_positions(L.cap(), np.arange(len(L)), self.top)
        dominant = np.zeros(len(L), dtype=bool)
        dominant[top] = True
        asked = L.markup_without(SHORTFALL)               # each firm's markup as priced, before any shortfall
        a = self.account = self.reckon(L, asked)
        differential, share = self.conditions(L, top)

        unsold = a["unsold"] / a["offered"]               # the unsold part of everything offered
        sold = 1.0 - a["unsold"] / a["priced_earnings"]   # the part of priced earnings that was received
        held_back = self.held_back * unsold
        changes = [Publish("unsold", float(unsold), self.name),
                   Publish("sold_part", float(sold), self.name),
                   # the green-field module takes this off the hiring rate of dominant firms next year
                   Publish("sales_cut", float(held_back), self.name),
                   # the merger module adds this to the employees each buyer seeks next year
                   Publish("bought_not_built", float(self.buy_instead * held_back), self.name),
                   Publish("sales_account", dict(a), self.name),
                   Publish("accumulation_differential", differential, self.name),
                   Publish("accumulation_share", share, self.name),
                   Publish("crisis_of_capital", float(differential + share < 2.0), self.name)]
        # Every firm loses the same part of its priced earnings. A firm of dominant capital keeps its
        # price and books the whole loss once, on this year's earnings. Any other firm takes a part of
        # the loss out of its price, where it stays until a later rise restores it, and books the rest.
        lost = 1.0 - sold
        price_cut = np.where(dominant, 0.0, self.price_give * lost)
        changes += [SetComponent(SHORTFALL, (1.0 - lost) / (1.0 - price_cut), self.name),
                    SetComponent(CARRIED, asked * (lost - price_cut), self.name)]
        if lost > 0:
            changes.append(ScaleComponent(PRICE_CUT, 1.0 - price_cut, self.name))
        return changes
