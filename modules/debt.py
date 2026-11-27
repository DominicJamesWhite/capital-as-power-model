"""Module 2: debt and equity (Capital as Power, chapters 12 and 13).

"Equity capitalizes the firm's differential ability to restrict industry for its own benefit,
whereas debt capitalizes the average ability of all owners to limit industry at large."
Interest is the return on average sabotage and profit the return on differential sabotage.
The part of capitalist income paid as interest rises when the institutions of power are
settled, which the book measures by unemployment averaged over several years.

The module keeps its own accounts and changes no entry in the ledger: it divides the
capitalist income of the envelope into interest and profit, and puts a price on two running
totals of debt, one for corporations and one for the government (the power to tax).

Sandy Brian Hager's work on the ownership of the United States public debt finds that it is
concentrated in the hands of large owners and paid for by taxes levied broadly. The module
therefore reports the part of the government's debt held by dominant capital, taken to equal
dominant capital's part of all capitalization. It does not pay that interest to those firms.

The failure module closes firms that cannot pay their lenders, and it publishes two numbers
that this module reads. Both change nothing when no firm closes. The first is the part of the
interest that is left once the closed firms have stopped paying, and the interest part is
multiplied by it. The second is the part of all employees whose firms closed, which is taken
off the unemployment that this module reads: the book ties debt to "the strength and solidity
of existing power institutions", and promises that are being broken are no sign of solidity.

Optional modules change the government's debt, and the numbers they publish are 0 when they
are off. The risk shaping module publishes what the government borrows to bail out dominant
capital. The modules that tax at a rate set in law (public debt, privatisation, organised
force, sales) have owners lend the government what the tax does not cover, and the record of
transfers shows what was lent and what was repaid. The privatisation module publishes what
dominant capital pays for the public services it takes over, and the government retires debt
with it. The module keeps the sum as a stock of money and adds it to the debt. A government
whose proceeds exceed its whole debt has no debt, and the rest of the proceeds is set against
later borrowing.

The holders of that added debt press for repayment. Each year the module charges a tax at one
rate on the wage bill and on every firm's earnings, of `holders_press` times the added debt,
and the government repays as much to owners, in proportion to the capitalization of each firm.
Sandy Brian Hager writes that the interests of the large holders of the debt "are best served
by an austerity program of social spending cuts" (Public Debt, Inequality, and Power, 2016),
and Bichler and Nitzan that the deficits after 2008 were reversed "because of the public debt"
("Can Capitalists Afford Recovery?", 2014). Neither gives a figure. `holders_press`, 0.05, is
Henning Bohn's measure for the United States, 1916 to 1995 ("The Behavior of U.S. Public Debt
and Deficits", 1998): the primary surplus rose by about 0.05 of national income for each year
of national income that the debt held by the public came to. The same regression on the
national accounts gives 0.07 (give or take 0.035) for 1960 to 2007 and below 0 for 1960 to
2019, when holders accepted more debt after 2008. In terms of power: what the holders of the
debt can make the government collect from everybody else, for them. With no added debt the
tax is nothing, so the main modules alone are unchanged.

Additions to the book: the speed and slope of the interest share, pooling corporate debt into
one total, the government's interest stream as a fixed part of all income, the stock that
bailouts add to the debt and proceeds take from it, and taking the jobs lost in closed firms
off the unemployment that the module reads, the tax pressed by the holders of the added debt
and its single rate on all income, and repaying them in proportion to capitalization.
"""
import numpy as np
from core import Publish, Transfer, lend_to_government, WAGE_EARNERS, GOVERNMENT

PRESSED = "tax pressed by the holders of the public debt"   # this module's income component; the core sets it
PRESSED_EARNINGS = "tax on earnings pressed by the holders of the public debt"
PRESSED_WAGES = "tax on wages pressed by the holders of the public debt"
REPAID = "repaid to the holders of the public debt"


class Debt:
    name = "debt"
    reads = ("unemployment", "transfers")
    supplies = ("interest_share", "corporate_debt", "government_debt", "government_debt_dominant")
    figures = {                   # what the workbench calls each published number: label, unit, note
        "interest_share": ("Interest share", "share", "Part of capitalist income paid as interest."),
        "corporate_debt": ("Corporate debt", "number", "Capitalized value of the interest that corporations pay, in money."),
        'government_debt': ('Government debt', 'number', "Capitalized value of the government's interest payments, in money."),
        'government_debt_dominant': ('Government debt held by the top 100', 'number', "Taken to equal the top 100's part of all capitalization, in money."),
    }

    def __init__(self, base=0.10, slope=4.0, usual_unemployment=0.05, years=5, speed=0.1,
                 government_part=0.02, start=0.20, holders_press=0.05):
        self.base = base                  # interest as a part of capitalist income when unemployment is at its usual level
        self.slope = slope                # rise in that part per unit of unemployment above the usual level
        self.usual_unemployment = usual_unemployment
        self.years = years                # years over which unemployment is averaged
        self.speed = speed                # yearly speed of adjustment
        self.government_part = government_part   # government interest payments as a part of all income
        self.share = start
        self.holders_press = holders_press   # tax pressed by the holders of the added debt, as a part of it in a year (Bohn 1998)
        self.past = []
        self.added = 0.0                  # debt added by bailouts and by borrowing to spend, less debt retired with the proceeds of privatisation, in money

    def accounts(self, L):
        capitalist = L.earnings().sum()
        income = capitalist + L.shared["wage"] * L.n.sum()
        nrr = L.shared["nrr"]
        K = L.cap()
        top = np.sort(K)[-100:].sum() / K.sum()       # dominant capital's part of all capitalization
        government = self.government_part * income / nrr + self.added
        dominant = top * self.government_part * income / nrr + top * self.added
        if government < 0:                # proceeds exceed the whole debt: there is no debt, and the rest waits in self.added
            government = dominant = 0.0
        return {"government_debt_dominant": dominant,
                "interest_share": self.share,
                "corporate_debt": self.share * capitalist / nrr,          # a promised return: risk of one
                "government_debt": government}

    def start(self, L):
        L.add_component(PRESSED, self.name, kind="income", transfers=True)
        return self.accounts(L)

    def propose(self, L, rng):
        A = L.accounts
        # Last year's borrowing for bailouts and in place of tax, less last year's repayment and proceeds of
        # privatisation (optional modules; 0 without them).
        lent = sum(row.get("lent_to_government", 0.0) for row in A.get("transfers", {}).values())
        self.added += A.get("bailout_borrowing", 0.0) + lent - A.get("privatisation_proceeds", 0.0)
        # Firms that closed last year stopped paying their lenders (the failure module); 1 when no firm closed.
        self.share = self.share * A.get("interest_left", 1.0)
        # Unemployment stands here for how solid the institutions of power are. People who lost their jobs
        # because their firm could not pay its lenders show the opposite, so the part of all employees whose
        # firms closed in a year is taken off that year's unemployment (the failure module; 0 without it).
        self.past = (self.past + [L.accounts["unemployment"] - A.get("failed_employees", 0.0)])[-self.years:]
        target = self.base + self.slope * (np.mean(self.past) - self.usual_unemployment)
        self.share = float(np.clip(self.share + self.speed * (target - self.share), 0.0, 0.9))
        changes = [Publish(k, v, self.name) for k, v in self.accounts(L).items()]
        # The holders of the added debt press for repayment: one rate on the wage bill and on every firm's
        # earnings before this tax, and the government repays them what it collects.
        press = self.holders_press * max(self.added, 0.0)
        if press > 0:
            wages = L.shared["wage"] * L.n.sum()
            base = np.maximum(L.earnings() - L.n * L.components[PRESSED], 0.0)
            rate = press / (wages + base.sum())
            changes += [Transfer(PRESSED_EARNINGS, payer=rate * base, receiver=GOVERNMENT, source=self.name),
                        Transfer(PRESSED_WAGES, payer=WAGE_EARNERS, receiver=GOVERNMENT, source=self.name,
                                 amount=rate * wages)]
            changes += lend_to_government(REPAID, -press, L, GOVERNMENT, self.name)
        return changes
