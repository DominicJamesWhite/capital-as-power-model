"""Module 11: what can be sold.

THE RULE IN PLAIN WORDS

Without this module the model takes it that firms sell all they offer. This module keeps an account of
who buys. Once a year it adds up, for the year just ended, the money that each party had and
what that money bought. The account is kept in money: what firms offer is the wage bill, plus
the earnings they priced for, plus the costs in their prices that they lay out on what other
firms sell.

  1. Wage earners buy with all the money they have: the wage bill, plus the payments they
     received, less the taxes and interest they paid, plus what households borrowed, less what
     they paid back.
  2. An organ of government that a module names as a buyer, such as the armed forces, buys with
     all it received. Money that the government holds buys nothing: it keeps it and uses it
     before it borrows again.
  3. A tax is a rate on income set in law. Each module that taxes sets its rate once, to cover
     what it makes the government pay in its first year, and keeps it. In a slump, when
     fewer people are employed, the tax at that rate falls and what the government pays out
     does not. The core adds up what every module leaves the government short or with to
     spare, and owners lend it what it is short of after it has used what it holds; what they
     lend, they do not spend. When the taxes collect more than the government pays out, it
     repays owners, who do not spend what is repaid, and holds what is left once it owes
     nothing. These are loans in the core's record of transfers, and the debt module adds
     them to the government's debt.
  3a. People out of work. This module has the government pay each person out of work a part of
     the wage (`benefit`), from a tax at one rate on the wage bill and on earnings, set in law
     in the first year in the same way. Their pay is counted with what wage earners have.
  4. Owners lay out on goods what firms pay out to them, kept level against the wage. Firms
     decide two outlays: what they pay out, which moves each year part of the way toward a
     part of what owners earned (`paid_out`), and the equipment of the year's new jobs, which
     they buy whatever they have kept. With the capacity module on, a job needs equipment only
     where the firm's plant did not already hold it. What firms keep is not decided. It is worked out at the
     end of the year, as what owners earned less what was paid out to them, and published as a
     result. Owners here are the owners of the firms and every party that receives payments as
     a holder of debt.
  5. Firms buy from firms. A cost in a price that a module marks as laid out on what firms
     sell, such as the outlay on advertising, is collected from buyers and spent in the same
     year. It is on both sides of the account and is never unsold.

What is left is unsold. Unsold goods are income to nobody: the wages were paid, so the whole
shortfall falls on owners, and their money income of the year is the priced earnings less the
unsold amount. What they are paid the next year follows that lower income.

Owners then respond, and each response lowers the unsold amount:

  - Firms of dominant capital lose a smaller part of their priced earnings than other firms. In the
    logarithm, the fall of their sales is `top_sensitivity` times the fall of the others'. The
    parts are set so that the losses of all firms add up to the unsold amount.
  - A firm outside dominant capital takes half of its loss out of its price, where it stays
    until a later rise restores it. It books the other half once, on the next year's earnings.
  - A firm of dominant capital keeps its price and books its whole loss once. It holds back
    production: it holds back the unsold part of its own goods from the employees it would
    otherwise have. It
    seeks the same number of employees by buying firms.
  - No firm books a loss larger than the earnings it priced for. If buyers did not even pay
    back the wage bill, each firm keeps the core's allowance for rounding of its markup. Its
    lenders lend it the rest of its loss, in proportion to the earnings it priced for. The
    account shows this as money that owners lend to firms (`lent_to_firms`), as they lend to
    the government, and not as income below nothing. The failure module adds the loan to the
    firm's debt, and finds the firm with nothing to pay its interest: "produce only if you
    expect to earn at least the normal rate of return. Otherwise, shut down" (chapter 12, "Is
    free competition free of power?").

Owners' money is accounted for in full. What owners had, after what they lent the government,
households and firms, is what they bought plus what they saved (`owners_saved`). Owners save
nothing unless wage earners and the government bought every good offered. The reason is that
owners' income is the priced earnings less what was unsold, plus the transfers they received.
In a year when something is unsold, that income equals what owners laid out. In a year when
nothing is unsold, it equals the goods left after wage earners and the government bought. So
owners never hold money that found no goods, and nothing is carried for them into the next
year. When owners and firms plan to lay out more than is left, the part of the plan they could
not carry out is reported (`owners_short`). It is a plan they had no money for, not money.

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
  - The same paper, "Fiscal policy", on the slump after 2008: "policymakers have let budget
    deficits skyrocket", in an intervention "based mostly on tax cuts and automatic
    stabilizers". It "was hastily reversed", and the reason given was "the public debt".
  - Sandy Brian Hager, "Corporate Ownership of the Public Debt" (2015): "the government comes
    to finance its expenditures, on interest and everything else, by borrowing from the rich,
    instead of taxing them". His book "Public Debt, Inequality, and Power" (2016), chapter 4,
    "Fiscal Conflict": "gradual increases in government spending" are "difficult to reverse".
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
itself; that owners lay out all they are paid; that the equipment of a new
job is bought on top of it; that the shortfall falls on firms by one measure of standing alone,
whether they are of dominant capital, and on all other firms alike; how far small sellers cut prices; that dominant capital
cuts its hiring by the unsold part and buys firms in place of the jobs; and the number of
years over which the two conditions are judged; and that a payment to people out of work is a
fixed part of the wage, paid by a tax at a rate set once.

FOUR FIGURES FROM THE NATIONAL ACCOUNTS

Neither the book nor the papers give the four figures the account needs, so they are measured
from the national accounts of the United States for 1947 to 2019 (Bureau of Economic Analysis).

  - `paid_out`, 0.75, and `payout_follows`, 0.5. What firms paid out (corporate profit before
    tax plus net interest, which is the capitalist income of the book's Figure 12.2, less the
    net saving of domestic business), as a part of private wages, set against its own value a
    year before and the income of a year before, 1948 to 2019: it kept 0.49 of its earlier
    value, give or take 0.12, and in the long run paid out 0.75 of the income (0.73 in 1948 to
    1979, 0.77 in 1980 to 2019). With firms' net investment of the year before added to the
    fit, 1961 to 2019, the payout moves by 0.02 for each unit built: firms do not pay out less
    in order to build. What firms kept, 0.25 of owners' income in the same accounts (0.20 to
    0.29 in half of the years), is the result that this module publishes as `kept_part`, and
    a test of the account, not a setting. In the accounts it is what others spent beyond what
    they received: firms' keeping less their building moved with the government's borrowing
    (correlation 0.75 from year to year). The figures leave out what owners save out of the
    income paid to them, which the accounts do not separate from the saving of wage earners.
  - `job_cost`, 3.0. The plant and equipment of private business, at what it would cost to
    replace, came to 3.0 years of the wages and salaries that private business paid. In half
    of the years it lay between 2.7 and 3.3, and in all of them between 2.5 and 3.6.
  - `benefit`, 0.13. Unemployment insurance paid for each person out of work, as a part of
    the wages and salaries for each employee, 1960 to 2019 (Bureau of Economic Analysis and
    the unemployment rate): the median year 0.127, half of the years between 0.10 and 0.15,
    0.16 before 1984 and 0.11 after it. The 2014 paper names these "automatic stabilizers". In
    terms of power: what wage earners won as a claim on the government for those the firms
    do not employ, which shrank as their organisation weakened after 1980.

WHO BEARS A SHORTFALL

Within one industry the book says little. Nitzan's thesis (1992, chapter 8, "Inflationary
restructuring: why?") reports the dual-economy finding that firms in the "big economy" enjoyed
higher returns and that "their performance in terms of key financial indicators was much more
stable and far less risky". The figure is from outside the tradition: Crouzet and Mehrotra
(American Economic Review, 2020), from the Quarterly Financial Report of United States
manufacturing, 1977 to 2014. They find that "a 1 percent drop in GDP is associated with a 2.5
percent drop in sales at the top 1 percent of firms and a 3.1 percent drop in sales in the bottom
99 percent", that the difference holds with industry controls, and that it is "concentrated at the
very top of the distribution", with no measurable difference within the bottom 99 per cent.
`top_sensitivity`, 0.81, is 2.5 ÷ 3.1; one standard error of their difference gives 0.74 to 0.87. In
terms of power: the largest firms hold their buyers, and the others bear more of what goes unsold.
A top 100 of 30,000 to 300,000 firms is the top 0.03 to 0.3 per cent, at the top of their scale.

With the first three figures, the account is the one the paper reports from Kalecki
and from Baran and Sweezy: the part of owners' income that is not paid out and not built with
buys nothing, and that much stays unsold. Setting `paid_out` and `payout_follows` to 1 gives
the other reading, in which owners as a class lay out all they receive a year late.

WHAT IS LEFT OUT

The record shows the rate of tax falling a little in a slump, through taxes on income that rise
faster than income and through cuts. Here a rate set in law does not fall. Only the holders of
the debt (the debt module) move what is collected.

Money paid for firms that are bought, and money that dominant capital pays for public
services, pass from owners to owners (the government retires debt with it), so they buy no
goods and take none away. Two costs in prices are not payments to anybody and are left out:
the difference that cost cutting makes to a firm's costs, which is a saving or a lag against
the wage, and this module's own entry for goods left unsold. The part of the gain from burdens
off the books (another module) that falls on later years is an entry in a firm's accounts
and not money, so owners cannot spend it. The services of public employees are not sold, so
they are not among the goods offered; their pay is counted with what wage earners have.
"""
import numpy as np
from core import (ScaleComponent, SetComponent, SetAttribute, Publish, Transfer, top_positions, lend_to_government,
                  WAGE_EARNERS, GOVERNMENT, ROUNDING)
from modules.capacity import PLANT

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

BENEFIT_TAX = "tax for pay to people out of work"      # this module's income component; the core sets it
BENEFIT_EARNINGS = "tax on earnings for pay to people out of work"
BENEFIT_WAGES = "tax on wages for pay to people out of work"
BENEFIT = "pay to people out of work"
BENEFIT_LENT = "lent to the government for pay to people out of work"   # below 0 in a year, repaid by it

# An attribute: what lenders lent each firm last year to cover a loss beyond the earnings it priced
# for, in money. It is above 0 only in a year in which buyers did not even pay back the wage bill.
# The failure module adds it to the firm's debt.
UNCOVERED = "lent for a loss beyond earnings"


class Sales:
    name = "sales"
    reads = ("jobs_created", "party_flows", "transfers", "capital_share", "unemployment")
    supplies = ("unsold", "sold_part", "sales_cut", "bought_not_built", "sales_account", "kept_part",
                "deficit_part", "benefit_paid", "accumulation_differential", "accumulation_share", "crisis_of_capital")
    figures = {                   # what the workbench calls each published number: label, unit, note
        "unsold": ("Unsold part", "share", "Part of the value that firms offered last year that nobody bought."),
        "sold_part": ("Priced earnings received", "share", "Part of the earnings that firms priced for last year that owners received."),
        "sales_cut": ("Hiring held back for unsold goods", "rate", "Fall in the hiring rate of the top 100 firms because goods were unsold."),
        "bought_not_built": ("Buying in place of building", "rate", "Employees that a top 100 firm seeks by buying firms in place of jobs it held back, as a part of its own."),
        "kept_part": ("Kept by firms", "share", "What owners earned last year less what firms paid out to them, as a part of the earnings that firms priced for."),
        "deficit_part": ("Government borrowing", "share", "What owners lent the government last year, less what it repaid them, as a part of the wages and priced earnings of the year."),
        "benefit_paid": ("Pay to people out of work", "share", "What the government pays people out of work this year, as a part of the wage bill."),
        "accumulation_differential": ("Differential accumulation holds", "index", "1 if differential capitalization has not fallen over the years judged, 0 if it has."),
        "accumulation_share": ("Capitalist share holds", "index", "1 if the capitalist share of income has not fallen over the years judged, 0 if it has."),
        "crisis_of_capital": ("Crisis for capital", "index", "1 if either condition of accumulation fails, 0 if both hold."),
    }

    def __init__(self, job_cost=3.0, price_give=0.5, held_back=1.0, buy_instead=1.0, paid_out=0.75,
                 payout_follows=0.5, benefit=0.13, judged_over=5, significant=0.01, top=100, top_sensitivity=0.81):
        self.job_cost = job_cost        # money spent on equipment for each new job, in years of the wage
        self.price_give = price_give    # part of its shortfall that a price-cutting seller takes out of its markup within a year
        self.held_back = held_back      # fall in the hiring rate of a firm of dominant capital per unit of the unsold part
        self.buy_instead = buy_instead  # employees that such a firm seeks by purchase for each job it holds back
        self.paid_out = paid_out        # part of owners' money income that firms pay out to them in the long run
        self.benefit = benefit          # pay to each person out of work, as a part of the wage (unemployment insurance, 1960 to 2019)
        self.benefit_rate = None        # the rate of tax on earnings for that pay, set in law in the first year and then moved only as the debt module orders
        self.benefit_wage_rate = None   # the rate on wages: the same when set, then moved as the debt module orders
        self.judged_over = judged_over  # years over which each condition of accumulation is judged
        self.significant = significant  # a fall smaller than this part of the level counts as steady
        self.top = top
        self.top_sensitivity = top_sensitivity  # fall of a dominant firm's sales, in logarithms, for each unit of the fall of the others' (Crouzet and Mehrotra 2020)
        self.payout_follows = payout_follows   # part of the gap between what owners are paid and the paid-out part of the last income that closes in a year
        self.payout = None              # what owners are paid and lay out in a year, in years of the wage
        self.carried = {WAGE_EARNERS: 0.0, GOVERNMENT: 0.0}   # money that found no goods to buy last year
        self.dk, self.share = [], []    # differential capitalization and the capitalist share, year by year
        self.account = {}               # the last account, in money

    def register(self, L):
        L.add_attribute(UNCOVERED, 0.0, 0.0, adds=True, owner=self.name)

    def start(self, L):
        L.add_component(PRICE_CUT, self.name)
        L.add_component(SHORTFALL, self.name, group=SHORTFALL, unpriced=True)
        L.add_component(CARRIED, self.name, kind="cost")
        L.add_component(BENEFIT_TAX, self.name, kind="income", transfers=True)
        return {"unsold": 0.0, "sold_part": 1.0, "sales_cut": 0.0, "bought_not_built": 0.0, "sales_account": {}, "kept_part": 0.0,
                "deficit_part": 0.0, "benefit_paid": 0.0, "accumulation_differential": 1.0, "accumulation_share": 1.0, "crisis_of_capital": 0.0}

    def reckon(self, L, asked):
        """The account of the year just ended, in money. Returns it as a dictionary."""
        A = L.accounts
        wage, n = L.shared["wage"], L.n
        wages = float(wage * n.sum())
        priced = float((n * wage * asked).sum())          # the earnings that the firms priced for
        outlays = float((n * wage * L.outlays_on_firms()).sum())      # costs in prices that firms lay out on what firms sell
        goods = wages + priced                            # what is offered to wage earners, the government and owners
        offered = goods + outlays
        if self.payout is None:                           # a run starts with everything sold: owners lay out what the opening prices ask
            self.payout = priced / wage

        flows = A.get("party_flows", {})
        net = {p: f["received"] - f["paid"] for p, f in flows.items()}
        organs = sum(flows[p]["received"] for p in sorted(flows) if p in L.buyers)     # parties that spend all they receive
        holders = sum(flows[p]["received"] for p in sorted(flows)
                      if p not in (WAGE_EARNERS, GOVERNMENT) and p not in L.buyers)
        # What firms received less what they paid, from the core's record of transfers. A firm that closed in the
        # year took no part in them, so this is also the total of the firms' components that record them.
        record = A.get("transfers", {})
        to_firms = sum(record[label].get("to_firms", 0.0) for label in sorted(record))
        lent, repaid = float(A.get("household_debt_lent", 0.0)), float(A.get("household_debt_repaid", 0.0))

        # What owners lent the government in the year, less what it repaid them (loans in the record of transfers).
        # It is part of what the government received, and owners do not spend it.
        borrowed = sum(row.get("lent_to_government", 0.0) for row in A.get("transfers", {}).values())

        # What each party had to spend.
        has_wages = (max(wages + net.get(WAGE_EARNERS, 0.0) + lent - repaid, 0.0)
                     + self.carried[WAGE_EARNERS])
        # The government buys through the organs that a module names as buyers. What it collects and does not
        # pay out it holds, and uses before it borrows: money held buys nothing.
        has_government = organs + self.carried[GOVERNMENT]
        # The equipment of the jobs that firms added last year. With the capacity module on, only the jobs that
        # plant did not already hold need equipment: people taken back on into idle plant need none.
        held = L.extra.get(PLANT)
        added = float(A.get("jobs_created", 0.0)) if held is None else float(np.maximum(n - held, 0.0).sum())
        building = self.job_cost * wage * added
        # What is paid out is below nothing after a year in which owners lost more than they earned: they
        # then pay money into the firms to meet the wages that sales did not pay back, and buy no goods.
        outlay = max(self.payout, 0.0) * wage

        # What each bought. Wage earners and the government spend all they have. If that is more than
        # everything offered, each buys in proportion and keeps the rest of its money for next year.
        first = has_wages + has_government
        part = min(1.0, goods / first) if first > 0 else 1.0
        by_wages, by_government = has_wages * part, has_government * part
        self.carried = {WAGE_EARNERS: has_wages - by_wages, GOVERNMENT: has_government - by_government}
        rest = max(goods - by_wages - by_government, 0.0)
        by_owners = min(outlay + building, rest)
        unsold = rest - by_owners
        if unsold < 1e-12 * offered:                      # a rounding error is not unsold goods
            by_owners, unsold = rest, 0.0
        # The part of the unsold goods beyond what firms can book as a loss: their lenders lend it to them.
        beyond = max(unsold - (1.0 - ROUNDING) * priced, 0.0)
        income = priced - unsold + beyond + to_firms + holders     # owners' money income of the year
        had = income - borrowed + repaid - lent - beyond  # what owners had, after what they lent and were repaid
        # What is paid out to owners moves part of the way toward the paid-out part of the year's income.
        # What firms kept is the result: what owners earned less what was paid out to them.
        self.payout += self.payout_follows * (self.paid_out * income / wage - self.payout)
        return {"offered": offered, "wages": wages, "priced_earnings": priced,
                "bought_by_wage_earners": by_wages, "bought_by_government": by_government,
                "bought_by_owners": by_owners, "bought_by_firms": outlays, "unsold": unsold,
                "wage_earners_had": has_wages, "government_had": has_government,
                "owners_had": had, "owners_income": income, "owners_saved": had - by_owners,
                "owners_short": max(outlay + building - by_owners, 0.0), "lent_to_firms": beyond,
                "owners_outlay": outlay, "kept": income - outlay, "building": building, "lent": lent, "repaid": repaid,
                "borrowed_by_government": borrowed, "to_firms": to_firms,
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
        total = min(1.0 - sold, 1.0 - ROUNDING)
        lost = self.split(L.n * asked, dominant, total)
        kept = 1.0 - lost
        if total >= 1.0 - ROUNDING:                       # buyers did not even pay back the wage bill: every firm
            kept = np.full(len(L), ROUNDING)              # keeps exactly the allowance for rounding
            lost = 1.0 - kept
        # A firm of dominant capital holds back the unsold part of its own goods.
        held_back = self.held_back * unsold * (float(lost[dominant][0]) / total if total > 0 and dominant.any() else 1.0)
        changes = [Publish("unsold", float(unsold), self.name),
                   Publish("sold_part", float(sold), self.name),
                   # the green-field module takes this off the hiring rate of dominant firms next year
                   Publish("sales_cut", float(held_back), self.name),
                   # the merger module adds this to the employees each buyer seeks next year
                   Publish("bought_not_built", float(self.buy_instead * held_back), self.name),
                   Publish("sales_account", dict(a), self.name),
                   Publish("kept_part", float(a["kept"] / a["priced_earnings"]), self.name),
                   Publish("deficit_part", float(a["borrowed_by_government"] / (a["wages"] + a["priced_earnings"])), self.name),
                   Publish("accumulation_differential", differential, self.name),
                   Publish("accumulation_share", share, self.name),
                   Publish("crisis_of_capital", float(differential + share < 2.0), self.name)]
        # Firms of dominant capital lose a smaller part of their priced earnings than the rest: in the
        # logarithm, their fall is `top_sensitivity` times the fall of the other firms. The parts are set
        # so that the losses add up to the unsold amount. A firm of dominant capital keeps its price and
        # books the whole loss once, on this year's earnings. Any other firm takes a part of the loss out
        # of its price, where it stays until a later rise restores it, and books the rest. A firm cannot
        # book a loss larger than the earnings it priced for. When buyers did not even pay back the wage
        # bill, the rest of the loss is paid out of what owners hold, which is not part of any firm's
        # earnings, such as public debt repaid to them, and the firm keeps the core's allowance for
        # rounding. The failure module then finds it with no cover for its interest.
        price_cut = np.where(dominant, 0.0, self.price_give * lost)
        # What lenders lend each firm for a loss beyond its priced earnings, in proportion to those earnings.
        weight = L.n * asked if (L.n * asked).sum() > 0 else L.n
        uncovered = a["lent_to_firms"] * weight / weight.sum() if a["lent_to_firms"] > 0 else np.zeros(len(L))
        changes += [SetComponent(SHORTFALL, kept / (1.0 - price_cut), self.name),
                    SetComponent(CARRIED, asked * (lost - price_cut), self.name),
                    SetAttribute(UNCOVERED, uncovered, self.name)]
        if total > 0:
            changes.append(ScaleComponent(PRICE_CUT, 1.0 - price_cut, self.name))
        return changes + self.pay_out_of_work(L)

    def split(self, priced, dominant, total):
        """Each firm's lost part of its priced earnings, when `total` of all priced earnings went unsold.

        A firm outside dominant capital keeps the part x of its priced earnings and a firm of dominant
        capital keeps x to the power `top_sensitivity`, with x set so that the losses, weighted by priced
        earnings, add up to `total`."""
        r = self.top_sensitivity
        if total <= 0 or r == 1.0:
            return np.full(priced.size, total)
        top, rest = float(priced[dominant].sum()), float(priced[~dominant].sum())
        target = total * (top + rest)
        lo, hi = 0.0, 1.0                   # what is lost falls as x rises: find x by halving the interval
        for _ in range(100):
            x = 0.5 * (lo + hi)
            if top * (1.0 - x ** r) + rest * (1.0 - x) > target:
                lo = x
            else:
                hi = x
        x = 0.5 * (lo + hi)
        return np.where(dominant, 1.0 - x ** r, 1.0 - x)

    def pay_out_of_work(self, L):
        """Part 3a: pay to people out of work, from a tax at a rate set in law in the first year."""
        wage = L.shared["wage"]
        employed = L.n.sum()
        wages = wage * employed
        pay = self.benefit * wage * max(L.shared["workforce"] - employed, 0.0)
        base = np.maximum(L.earnings() - L.n * L.components[BENEFIT_TAX], 0.0)
        if self.benefit_rate is not None:   # once in law, the rates move as the debt module orders after a surplus or a deficit
            self.benefit_rate *= L.accounts.get("tax_kept_earnings", 1.0)
            self.benefit_wage_rate *= L.accounts.get("tax_kept_wages", 1.0)
        if self.benefit_rate is None and pay > 0:
            self.benefit_rate = self.benefit_wage_rate = float(pay / (wages + base.sum()))
        if self.benefit_rate is None:
            return [Publish("benefit_paid", 0.0, self.name)]
        rate, wage_rate = self.benefit_rate, self.benefit_wage_rate
        taxed = (rate * base.sum(), wage_rate * wages)
        tax = rate * (wages + base.sum()) if wage_rate == rate else sum(taxed)
        out = [Transfer(BENEFIT_EARNINGS, payer=rate * base, receiver=GOVERNMENT, source=self.name),
               Transfer(BENEFIT_WAGES, payer=WAGE_EARNERS, receiver=GOVERNMENT, source=self.name, amount=wage_rate * wages),
               Publish("benefit_paid", float(pay / wages), self.name)]
        out += lend_to_government(BENEFIT_LENT, float(pay - tax), L, GOVERNMENT, self.name, taxed, (base.sum(), wages))
        if pay > 0:
            out.append(Transfer(BENEFIT, payer=GOVERNMENT, receiver=WAGE_EARNERS, source=self.name, amount=pay))
        return out

