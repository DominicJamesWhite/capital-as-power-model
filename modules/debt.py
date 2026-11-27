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

Two optional modules change the government's debt, and each publishes a number that this
module reads. Both numbers are 0 when those modules are off, and they then change
nothing. The risk shaping module publishes what the government borrows to
bail out dominant capital. The privatisation module publishes what dominant capital pays for
the public services it takes over, and the government retires debt with it. The module keeps
the sum of the two as a stock of money and adds it to the debt. A government whose proceeds
exceed its whole debt has no debt, and the rest of the proceeds is set against later borrowing.

Additions to the book: the speed and slope of the interest share, pooling corporate debt into
one total, the government's interest stream as a fixed part of all income, and the stock that
bailouts add to the debt and proceeds take from it.
"""
import numpy as np
from core import Publish


class Debt:
    name = "debt"
    reads = ("unemployment",)
    supplies = ("interest_share", "corporate_debt", "government_debt", "government_debt_dominant")
    figures = {                   # what the workbench calls each published number: label, unit, note
        "interest_share": ("Interest share", "share", "Part of capitalist income paid as interest."),
        "corporate_debt": ("Corporate debt", "number", "Capitalized value of the interest that corporations pay, in money."),
        'government_debt': ('Government debt', 'number', "Capitalized value of the government's interest payments, in money."),
        'government_debt_dominant': ('Government debt held by the top 100', 'number', "Taken to equal the top 100's part of all capitalization, in money."),
    }

    def __init__(self, base=0.10, slope=4.0, usual_unemployment=0.05, years=5, speed=0.1,
                 government_part=0.02, start=0.20):
        self.base = base                  # interest as a part of capitalist income when unemployment is at its usual level
        self.slope = slope                # rise in that part per unit of unemployment above the usual level
        self.usual_unemployment = usual_unemployment
        self.years = years                # years over which unemployment is averaged
        self.speed = speed                # yearly speed of adjustment
        self.government_part = government_part   # government interest payments as a part of all income
        self.share = start
        self.past = []
        self.added = 0.0                  # debt added by bailouts less debt retired with the proceeds of privatisation, in money

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
        return self.accounts(L)

    def propose(self, L, rng):
        A = L.accounts
        # Last year's borrowing for bailouts, less last year's proceeds of privatisation (optional modules; 0 without them).
        self.added += A.get("bailout_borrowing", 0.0) - A.get("privatisation_proceeds", 0.0)
        self.past = (self.past + [L.accounts["unemployment"]])[-self.years:]
        target = self.base + self.slope * (np.mean(self.past) - self.usual_unemployment)
        self.share = float(np.clip(self.share + self.speed * (target - self.share), 0.0, 0.9))
        return [Publish(k, v, self.name) for k, v in self.accounts(L).items()]
