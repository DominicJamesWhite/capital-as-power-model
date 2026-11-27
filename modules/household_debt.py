"""Optional module: household debt.

THE RULE IN PLAIN WORDS

The main modules pay the whole wage bill to wage earners. This module pledges a part of the wage
bill as interest on the debts of households. The interest becomes part of the earnings of the
firms in the ledger, and most of all of the firms that sit in the industries that dominant
capital holds. Nothing in the rule comes from outside the model. Prices, wages and employment
come from the other modules, and the debt grows out of them.

  1. Reach. The module keeps the part of wage earners to whom lenders extend credit, a number
     between 0 and 1. It starts low. Each year the part not yet reached shrinks by a rate times
     the top hundred's part of all employees. Lending therefore spreads as dominant capital grows.
  2. The wage that households keep. The module takes the wage, removes the part that was pledged
     as interest in the previous year, and divides by the average price. It compares the result
     with the best level of the last ten years. The shortfall is the part by which the present
     level stands below that best level. It is 0 when wages have kept pace with prices.
  3. Borrowing. Households borrow to make up a part of the shortfall. The new borrowing of the
     year is a set part of the shortfall, times the reach of part 1, times the wage bill.
  4. Repayment. Each year a set part of the outstanding principal is repaid.
  5. The interest. Household loans carry a rate that is a multiple of the normal rate of return.
     The interest of the year is that rate times the principal.
  6. The limit and default. Interest cannot take more than a set part of the wage bill. When it
     would, the principal above the limit is written off. A fall in employment shrinks the wage
     bill, so lay-offs bring write-offs once the limit is near.
  7. Who receives the interest. Each industry receives interest in proportion to its earnings
     before interest, multiplied by a weight. The weight is 1 in an industry where dominant
     capital holds nothing and rises in proportion to a set multiple in an industry that the
     hundred largest firms hold entirely. Every firm in an industry receives the same
     proportion of its other earnings.
  8. The change to the ledger. The module proposes one transfer: wage earners pay the year's
     interest, and the firms receive it in the proportions of part 7. The core settles it
     (see "The record of transfers" in modules.md) and enters what each firm receives in an
     income component that this module owns. Wage earners cannot pay more than the wage bill.
     The amount is replaced each year, so interest is never added twice. The interest is not a
     markup, and the core keeps it apart from the markup. No money is taken from the lenders
     when they lend.
  9. Placation. New borrowing wears down popular resistance. The module publishes a number, a
     set multiple of the year's new borrowing as a part of the wage bill, and the resistance
     module lowers popular resistance by that number times its level. The number is 0 when this
     module is off.
 10. Readouts. The module publishes the capitalized value of the debt, the principal, the
     pledged part of the wage bill, the reach, the shortfall, the new borrowing, the write-offs,
     the top hundred's part of the interest, and the capitalist share of income with the interest
     counted once. It also publishes, for each industry, the part of earnings that comes from
     sources other than household interest. No module reads that number.

The wage in the ledger is not changed, because no entry in the ledger stands for wage
earners. Wage earners are the payer of the transfer, so the core's own readout of the
capitalist share counts the interest once in total income.

WHAT IT RESTS ON

  - Capital as Power (2009), chapter 9, "The capitalization of every thing" and "Human beings".
    "Nowadays, every expected income stream is a fair candidate for capitalization." Of workers
    who "borrow money to buy a car, take a mortgage to purchase a home, or open a line of
    credit to acquire what they otherwise can't with their immediate income": "As borrowers,
    they commit themselves to repaying the principal and interest, a liability that the lending
    institution happily discounts as an asset. Now, to settle their debt the workers need to
    work (or beg) for an income. In other words, they need to devote part of their life to the
    bank. And it is this part of the worker's life that the bank capitalizes as an asset on its
    balance sheet." Parts 5, 7 and 8 rest on this. The footnote to the passage: "For the moment,
    these options are available only to a minority of the world's workers, although
    'micro-credit' banks and similar innovations gradually extend the Bernoullian principle even
    to the most wretched." Part 1 rests on this.
  - Bichler and Nitzan, "New Imperialism or New Capitalism?" (2006). "The capitalization logic
    determines the present value of a worker (the value of her mortgaged home, car, and line of
    credit together being dependent on her expected lifetime earnings and the risk of her being
    laid off)." Part 6 and the risk in the capitalized value of part 10 rest on this.
  - Chapter 13: in the early history of credit each type of instrument had "its own 'benchmark'
    and 'normal rate of return'". Part 5 gives household loans their own rate.
  - Tim Di Muzio and Richard H. Robbins, Debt as Power (2016).
    "Since the vast
    majority of money is released into the economy as capitalized money bearing interest to the
    owners and managers of banks, this means that one way to expand earnings is by expanding the
    pool of debtors. One of the major inventions here was the creation and development of the
    consumer and various types of consumer credit 'products'". Part 1 rests on this. "As wages
    have stagnated or fallen for the majority in mature economies, there has been an increasing
    reliance on consumer credit to finance necessities like food, medicine, and electricity".
    Parts 2 and 3 rest on this. "Borrowers are not borrowing money that exists when they use
    bank products, but money created on computer screens." Part 8 rests on this: lending takes
    nothing from the lender's earnings. "The entire commercial banking system depends on this
    type of exclusive right to issue credit"; "through interlocking ownership, commercial banks
    have come to capitalize one another so they have what could be called an 'effective
    monopoly' on creating the money supply". Part 7 rests on this. "There is always more debt in
    the system than the ability to repay", and "domestic banks and other lending institutions
    can send in lawyers, judges, and police". The book reports that the ratio of household debt
    to disposable income in the rich countries rose "by an average of 30 percentage points, to
    130%" between 2000 and 2007. That figure is something to compare a run with. It is not a
    setting.
  - Sandy Brian Hager, Public Debt, Inequality, and Power (2016), chapters 1 and 5. "Access to
    cheap credit allows low- and middle-income Americans to maintain consumption habits in the
    face of decades-long wage stagnation." "Household debt serves as a compensatory mechanism in
    the face of wealth and income stagnation for low- and middle-income households." Widespread
    access to credit "helps to dampen resentment toward the top percentile" and "relieves some
    of the domestic tensions associated with growing wealth and income inequality". Parts 2, 3
    and 9 rest on this. Hager reports ratios of debt to income for the lower half of United
    States households of 0.61 in 1989 and 1.37 in 2007.
  - Capital as Power, chapter 16: inflation in the United States "has been associated with a
    systematic redistribution of income from workers to firms". The other modules produce the
    lag of wages behind prices that part 2 measures.

WHAT IS ADDED

The literature says that a household loan is a capitalized right to a part of the borrower's
working life, that lenders enlarge their earnings by enlarging the pool of debtors, that
households borrow when wages stagnate, that the borrowing dampens resentment, and that the worth
of the loan depends on the risk of lay-off. It gives no rule and no rate. The form of every
part is an addition, and every number below is an addition. Three choices need to be stated.
The model has no banks, so part 7 places lending in the industries that dominant capital holds;
every firm in such an industry gains, including the small ones, which is how the sabotage
module already treats the markup. Measuring the lag of wages by the best level of the last ten
years is an addition, and it means that a lower level is forgotten as a grievance after ten
years. Di Muzio and Robbins are not Nitzan and Bichler; they use the theory of capital as power
and add an account of money created as debt, which this module uses only to say that lending
costs the lender nothing.

WHAT IS MISSING

Repayment and new borrowing change no income in the model. The module publishes the money lent
and the money repaid in the year, and the optional sales module counts them in what wage
earners have to spend; with that module off, nothing follows from them. Di Muzio and Robbins hold that
the cost of interest forces growth and is passed into prices; the rule has neither. Household debt is
not traded and has no price of its own apart from the published capitalized value. The
discipline that debt imposes on an indebted worker does not reach the module for organised
labour. Mortgages, student loans and card debt are not told apart.
"""
import numpy as np
from core import Transfer, Publish, top_positions, WAGE_EARNERS

INCOME = "household interest"   # this module's income component: interest from households, for each employee of the firm; the core sets it from the transfer below
INTEREST = "interest on household debt"


class HouseholdDebt:
    name = "household_debt"
    reads = ("unemployment", "concentration")
    supplies = ("household_debt", "household_debt_principal", "household_debt_pledged",
                "household_debt_reach", "household_debt_shortfall", "household_debt_borrowing",
                "household_debt_written_off", "household_debt_dominant", "household_debt_capital_share",
                "household_debt_markup_part", "household_debt_placation", "household_debt_lent",
                "household_debt_repaid")
    figures = {                   # what the workbench calls each published number: label, unit, note
        "household_debt": ("Household debt", "number", "Capitalized value of household interest, in money."),
        "household_debt_principal": ("Household debt owed", "number", "The money owed."),
        "household_debt_lent": ("Money lent to households", "number", "What lenders handed to wage earners in the year."),
        "household_debt_repaid": ("Money repaid by households", "number", "What wage earners paid back to lenders in the year."),
        "household_debt_pledged": ("Interest pledged from wages", "share", "Household interest as a part of the wage bill."),
        "household_debt_reach": ("Reach of household lending", "share", ""),
        "household_debt_shortfall": ("Shortfall of kept income", "share", ""),
        "household_debt_borrowing": ("New household borrowing", "share", "New borrowing as a part of the wage bill."),
        "household_debt_written_off": ("Household debt written off", "share", "Defaulted principal as a part of the wage bill."),
        'household_debt_dominant': ('Household interest to the top 100', 'share', "The top 100's part of household interest."),
        "household_debt_capital_share": ("Capitalist share with household interest", "share", "Capitalist share of income, with the interest counted once."),
        "household_debt_placation": ("Placation", "rate", "Fall in popular resistance from new borrowing, as a part of its level."),
    }

    def __init__(self, start_reach=0.10, extend=0.20, memory=10, cover=0.5, repay=0.10,
                 rate_multiple=2.0, ceiling=0.15, lender_weight=5.0, placate=2.0,
                 layoff_risk=1.0, start_principal=0.0, top=100):
        self.start_reach = start_reach        # part of wage earners to whom credit is extended at the start; the book says "a minority" (addition)
        self.extend = extend                  # yearly shrinking of the part not yet reached, per unit of the top hundred's part of all employees (addition)
        self.memory = memory                  # years over which the best level of the wage that households keep is remembered (addition)
        self.cover = cover                    # part of the shortfall that households with access to credit make up by borrowing (addition)
        self.repay = repay                    # part of the outstanding principal that is repaid each year (addition)
        self.rate_multiple = rate_multiple    # the rate on household loans as a multiple of the normal rate of return (addition)
        self.ceiling = ceiling                # the largest part of the wage bill that interest can take; principal above it is written off (addition)
        self.lender_weight = lender_weight    # interest received per unit of other earnings in an industry wholly held by dominant capital, as a multiple of an industry it does not hold (addition)
        self.placate = placate                # fall in popular resistance, as a part of its level, per unit of new borrowing measured as a part of the wage bill (addition); 0 switches it off
        self.layoff_risk = layoff_risk        # rise in the risk of household debt as a whole per unit of unemployment (addition); used in a readout only
        self.start_principal = start_principal   # principal at the start, as a part of the yearly wage bill (addition)
        self.top = top
        self.reach = float(start_reach)
        self.principal = None                 # outstanding principal, in money
        self.pledged = 0.0                    # part of the wage bill paid as interest in the previous year
        self.kept = []                        # the wage that households keep, measured against prices, in recent years

    def start(self, L):
        k = L.sector_of.size
        L.add_component(INCOME, self.name, kind="income", transfers=True)   # the interest is a transfer that wage earners pay
        self.principal = self.start_principal * L.shared["wage"] * L.n.sum()
        out = {key: 0.0 for key in self.supplies}
        out["household_debt_markup_part"] = np.ones(k)
        out["household_debt_reach"] = self.reach
        out["household_debt_principal"] = self.principal
        return out

    def propose(self, L, rng):
        A = L.accounts
        k = L.sector_of.size
        wage, employed = L.shared["wage"], L.n.sum()
        wages = wage * employed
        price = (L.p * L.n).sum() / employed
        rate = L.shared["nrr"] * self.rate_multiple                                   # part 5

        # part 1: lenders extend credit as dominant capital grows
        self.reach = float(np.clip(self.reach + self.extend * A["concentration"] * (1 - self.reach), 0.0, 1.0))

        # part 2: the wage that households keep, against prices
        self.kept = (self.kept + [wage * (1 - self.pledged) / price])[-self.memory:]
        shortfall = float(max(0.0, 1 - self.kept[-1] / max(self.kept)))

        # parts 3 and 4: borrowing and repayment
        borrowing = self.cover * self.reach * shortfall * wages
        repaid = self.principal * self.repay
        self.principal = self.principal * (1 - self.repay) + borrowing

        # parts 5 and 6: the interest, its limit, and default
        limit = self.ceiling * wages / rate
        written_off = max(0.0, self.principal - limit)
        self.principal -= written_off
        interest = rate * self.principal
        self.pledged = interest / wages

        # part 7: who receives the interest
        dominant = top_positions(L.cap(), np.arange(len(L)), self.top)
        n = np.bincount(L.ind, L.n, k)
        held = np.bincount(L.ind[dominant], L.n[dominant], k) / np.maximum(n, 1e-12)
        base_firm = L.earnings() - L.n * L.components[INCOME]                        # each firm's earnings before household interest
        base = np.bincount(L.ind, base_firm, k)                                      # the same for each industry
        weight = 1 + (self.lender_weight - 1) * held
        new = 1 + interest / (base * weight).sum() * weight

        # part 10: readouts
        risk = 1 + self.layoff_risk * A["unemployment"]
        to_top = (base_firm[dominant] * (new[L.ind[dominant]] - 1)).sum()
        out = {
            "household_debt": interest / (risk * L.shared["nrr"]),                    # the price put on the future interest of all household debt
            "household_debt_principal": self.principal,                               # the money owed
            "household_debt_pledged": self.pledged,                                   # interest as a part of the wage bill
            "household_debt_reach": self.reach,
            "household_debt_shortfall": shortfall,
            "household_debt_borrowing": borrowing / wages,                            # new borrowing as a part of the wage bill
            "household_debt_written_off": written_off / wages,                        # defaulted principal as a part of the wage bill
            "household_debt_dominant": float(to_top / interest) if interest > 0 else 0.0,   # the top hundred's part of the interest
            "household_debt_capital_share": float((base.sum() + interest) / (base.sum() + wages)),   # interest counted once
            "household_debt_markup_part": 1 / new,                                    # by industry; no module reads it
            "household_debt_placation": self.placate * borrowing / wages,             # part 9, read by the resistance module
            "household_debt_lent": borrowing,                                         # the money that lenders handed to wage earners this year
            "household_debt_repaid": repaid,                                          # the money that wage earners paid back to lenders this year
        }
        changes = [Publish(key, value, self.name) for key, value in out.items()]

        # part 8: wage earners pay this year's interest, and the firms receive it
        if interest > 0:
            changes.append(Transfer(INTEREST, payer=WAGE_EARNERS, receiver=(new[L.ind] - 1) * base_firm,
                                    source=self.name, amount=interest))
        return changes
