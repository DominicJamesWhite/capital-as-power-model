"""Module 2: debt and equity (Capital as Power, chapters 12 and 13).

"Equity capitalizes the firm's differential ability to restrict industry for its own benefit,
whereas debt capitalizes the average ability of all owners to limit industry at large."
Interest is the return on average sabotage and profit the return on differential sabotage.
The part of capitalist income paid as interest is not set by this module. The failure module
keeps each firm's debt, which it carries from year to year at the rate at which it was lent, and
publishes the interest that firms owe as a part of their earnings and the debt that they owe.
This module reports both. Without the failure module the interest part stays at its first
value and corporate debt is that interest capitalized at the normal rate of return. The book's
Figure 12.4, the ratio of interest to profit against unemployment, is then a result of a run to
be measured, not a rule.

The module keeps its own accounts and changes no entry in the ledger: it divides the
capitalist income of the envelope into interest and profit, and puts a price on two running
totals of debt, one for corporations and one for the government (the power to tax).

Sandy Brian Hager's work on the ownership of the United States public debt finds that it is
concentrated in the hands of large owners and paid for by taxes levied broadly. The module
therefore reports the part of the government's debt held by dominant capital, taken to equal
dominant capital's part of all capitalization. It does not pay that interest to those firms.

Optional modules change the government's debt, and the numbers they publish are 0 when they
are off. The risk shaping module publishes what the government borrows to bail out dominant
capital. The modules that tax at a rate set in law (public debt, privatisation, organised
force, sales, and this module) report what they leave the government short of or with to
spare, and the core keeps one account for the government: owners lend it what it is short of
after it has used the money it holds, and it repays them with what is left over, no more than
this module last reported it owes. The record of transfers shows what was lent and what was
repaid. The privatisation module publishes what
dominant capital pays for the public services it takes over, and the government retires debt
with it. The module keeps the sum as a stock of money and adds it to the debt. A government
whose proceeds exceed its whole debt has no debt, and the rest of the proceeds is set against
later borrowing.

The holders of that added debt press for repayment. Each year the module charges a tax at one
rate on the wage bill and on every firm's earnings, of `holders_press` times the added debt.
The tax goes into the government's one account, so it first pays for what the other taxes do
not cover, such as interest on the debt, and what is left repays owners, in proportion to the
capitalization of each firm. For example, with an added debt of 1,000 the tax is 50; if the
other modules leave the government 30 short, owners are repaid 20.
Sandy Brian Hager writes that the interests of the large holders of the debt "are best served
by an austerity program of social spending cuts" (Public Debt, Inequality, and Power, 2016,
chapter 1), and Bichler and Nitzan that the deficits after 2008 were reversed "because of the
public debt" ("Can Capitalists Afford Recovery?", 2014). Neither gives a figure.
`holders_press`, 0.05, is our own choice from the record. Henning Bohn ("The Behavior of U.S.
Public Debt and Deficits", 1998) is reported to find that the primary surplus of the United
States rose by about 0.05 of national income for each year of national income that the debt
held by the public came to, 1916 to 1995; the paper is not on disk and the figure has not been
checked against it. The same regression on the national accounts gives 0.07 (give or take
0.035) for 1960 to 2007 and below 0 for 1960 to 2019, when holders accepted more debt after
2008, so the record supports anything from a little below 0 to about 0.1. In terms of power:
what the holders of the debt can make the government collect from everybody else, for them.
With no added debt the tax is nothing, so the main modules alone are unchanged.

The government never refuses to pay. Hager writes of the first holders of the United States
debt that they "would provide a powerful force against repudiation" (chapter 1), and reports
the argument that a government can instead lower its debt by inflation, a "default by
stealth" (chapter 5). Here the debt is kept in money, so rising prices and wages lower it as a
part of income. When the taxes do not reach, the core pays holders only what the government
has; what it does not repay stays owed, and interest it does not pay is lost to them.

Additions to the book: the interest part of the first year, the government's interest stream
as a fixed part of all income, the stock that bailouts add to the debt and proceeds take from
it, the tax pressed by the holders of the added debt and its single rate on all income, and
repaying them in proportion to capitalization.
"""
import numpy as np
from core import Publish, Transfer, lend_to_government, WAGE_EARNERS, GOVERNMENT

PRESSED = "tax pressed by the holders of the public debt"   # this module's income component; the core sets it
PRESSED_EARNINGS = "tax on earnings pressed by the holders of the public debt"
PRESSED_WAGES = "tax on wages pressed by the holders of the public debt"
REPAID = "repaid to the holders of the public debt"


class Debt:
    name = "debt"
    reads = ("transfers",)
    supplies = ("interest_share", "corporate_debt", "government_debt", "government_debt_dominant",
                "tax_kept_earnings", "tax_kept_wages")
    figures = {                   # what the workbench calls each published number: label, unit, note
        "interest_share": ("Interest terms", "share", "Interest that firms owe, as a part of their earnings (the failure module); without it, the part of the first year."),
        "corporate_debt": ("Corporate debt", "number", "The debt that firms owe, in money (the failure module); without it, the interest capitalized at the normal rate of return."),
        'government_debt': ('Government debt', 'number', "Capitalized value of the government's interest payments, in money."),
        'government_debt_dominant': ('Government debt held by the top 100', 'number', "Taken to equal the top 100's part of all capitalization, in money."),
        "tax_kept_earnings": ("Rate on earnings kept", "share", "The part of each rate of tax in law on firms' earnings that is kept next year, after owners have it cut for last year's surplus."),
        "tax_kept_wages": ("Rate on wages kept", "share", "The part of each rate of tax in law on wages that is kept next year, after owners have it cut for last year's surplus."),
    }

    def __init__(self, government_part=0.02, start=0.20, holders_press=0.05, cut_surplus=True, owners_pace=2.3):
        self.government_part = government_part   # government interest payments as a part of all income
        self.share = start
        self.holders_press = holders_press   # tax pressed by the holders of the added debt, as a part of it in a year (Bohn 1998)
        self.cut_surplus = cut_surplus       # owners have the rates in law cut by what they bring in beyond what the government pays (Hager 2016, chapter 4)
        self.owners_pace = owners_pace       # how many times as fast the rate on earnings falls as the rate on wages, in proportion (Hager 2016, chapter 4: effective rates of the largest corporations and of households)
        self.ordered = (1.0, 1.0)            # the cut ordered last year: the part of the rate on earnings and of the rate on wages to be kept
        self.debt = None                  # the debt that firms owe (the failure module); None without it
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
                # the debt firms owe; without the failure module, a promised return at a risk of one
                "corporate_debt": self.debt if self.debt is not None else self.share * capitalist / nrr,
                "government_debt": government}

    def start(self, L):
        L.add_component(PRESSED, self.name, kind="income", transfers=True)
        return dict(self.accounts(L), tax_kept_earnings=1.0, tax_kept_wages=1.0)

    def propose(self, L, rng):
        A = L.accounts
        # Last year's borrowing for bailouts and in place of tax, less last year's repayment and proceeds of
        # privatisation (optional modules; 0 without them).
        lent = sum(row.get("lent_to_government", 0.0) for row in A.get("transfers", {}).values())
        self.added += A.get("bailout_borrowing", 0.0) + lent - A.get("privatisation_proceeds", 0.0)
        # What firms owed last year and the debt they owed (the failure module).
        if "interest_owed" in A:
            self.share = float(A["interest_owed"])
        if "debt_owed" in A:
            self.debt = float(A["debt_owed"])
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
        changes += self.order_cut(A.get("government", {}))
        return changes

    def order_cut(self, G):
        """Owners have the rates in law cut by what the taxes at those rates brought in last year beyond
        what the government paid for with them, less what the cut ordered last year will already take
        off. The tax pressed by the holders of the debt is not counted: it is collected to repay them.
        The rate on earnings falls `owners_pace` times as fast as the rate on wages, in proportion, and
        the cut is sized so that last year's taxes would have come to exactly what was paid. A deficit
        orders no cut and no rise. The modules that tax at a rate in law apply the cut the next year."""
        if not self.cut_surplus:
            return []
        te, tw = float(G.get("taxed_earnings", 0.0)), float(G.get("taxed_wages", 0.0))
        gaps = G.get("gaps", {})
        surplus = -sum(gaps[k] for k in sorted(gaps) if k != REPAID)
        ke, kw = self.ordered
        want = surplus - te * (1.0 - ke) - tw * (1.0 - kw)
        self.ordered = (1.0, 1.0)
        if want > 0 and te + tw > 0:
            a = self.owners_pace
            if want >= te + tw:              # the taxes brought in more than all they pay for: no rate is left
                self.ordered = (0.0, 0.0)
            else:
                taken = lambda k: te * (1.0 - np.exp(-a * k)) + tw * (1.0 - np.exp(-k))
                lo, hi = 0.0, 1.0
                while taken(hi) < want:
                    hi *= 2.0
                for _ in range(100):         # what is taken rises with k: find k by halving the interval
                    mid = 0.5 * (lo + hi)
                    lo, hi = (mid, hi) if taken(mid) < want else (lo, mid)
                k = 0.5 * (lo + hi)
                self.ordered = (float(np.exp(-a * k)), float(np.exp(-k)))
        return [Publish("tax_kept_earnings", self.ordered[0], self.name),
                Publish("tax_kept_wages", self.ordered[1], self.name)]
