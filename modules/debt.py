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
2008, so the record supports anything from a little below 0 to about 0.1. With federal military
spending held apart as well, as Bohn does, it is 0.061 (give or take 0.032) for 1960 to 2007. In terms of power:
what the holders of the debt can make the government collect from everybody else, for them.
With no added debt the tax is nothing, so the main modules alone are unchanged.

The holders press only in a lasting recovery: when unemployment has fallen in each of the last
`recovery_years` years, 2. Hager writes that "Any effort to drastically reduce the debt without a
sustained recovery would likely encounter resistance from dominant owners" (chapter 4, "Fixing or
Flipping?"). How many years of falling unemployment make a recovery lasting is our own choice. In
the United States record, 1981 to 2017, the change of federal receipts that came from changes of
effective rates rose with the debt held by the public in such years (0.003 of the debt, give or
take 0.008) and fell with it in other years (0.027, give or take 0.014), so the record leans the
same way, weakly. The record does not settle the number of years: in the regression of the
primary surplus on the debt, split by whether unemployment had fallen in each of the last 1 to 4
years, holders pressed harder in recovery years over 1960 to 2007, the more so the longer the
recovery (by 0.04 of the debt after one year, 0.07 after two, 0.10 after three), but less hard over
1960 to 1989 alone and over 1990 to 2019 alone. With `recovery_years` at 0 the holders press every year.

The government never refuses to pay. Hager writes of the first holders of the United States
debt that they "would provide a powerful force against repudiation" (chapter 1), and reports
the argument that a government can instead lower its debt by inflation, a "default by
stealth" (chapter 5). Here the debt is kept in money, so rising prices and wages lower it as a
part of income. When the taxes do not reach, the core pays holders only what the government
has; what it does not repay stays owed, and interest it does not pay is lost to them.

The rates of the taxes set in law move with the government's account. After a surplus, owners
have them cut by `cut_part` of it, theirs faster: Hager, after Streeck, writes of the "successful
tax resistance waged on the part of increasingly powerful elites" (chapter 4). After a deficit
the rates rise to bring in `rise_part` of it; most of the time governments "come to rely on
borrowing from elites instead of taxing them" (the same chapter). Both parts and the pace of the
rise come from the United States federal accounts, 1951 to 2017: the change of receipts that came
from changes of effective federal rates on corporate profits and on the pay of employees, as a
part of national product, against last year's federal balance, with the wars, the growth of
profits against wages, and the year's change of unemployment held apart. The last is held apart
because effective rates also move by themselves with the cycle, as incomes move between brackets,
and rates set in law in the model do not. A surplus of 1 per cent of national product was
followed by cuts that took 0.24 per cent off receipts (give or take 0.15), and a deficit of 1 per
cent by rises that brought in 0.045 per cent (give or take 0.033). The rise came as much after a
deficit run in a slump as after one run in a recovery. After a deficit the effective rate on
profits rose 5.2 times as fast as the rate on wages, in proportion, and the rise of the rate on
wages is smaller than its error, so that figure is loose. Whatever the balance, owners also wear
the rate on earnings down by `owners_resist` of itself a year: in the same fit the effective rate
on profits fell by 3.9 per cent of itself a year apart from the balance (give or take 1.8), and
the rate on wages did not fall. The rise after deficits and this fall belong together: with the
average deficit of those years, 2.2 per cent of national product, they give a fall of the rate
on profits of 1.7 per cent of itself a year, against 1.9 in the record from 1951 to 2017. Part
of that fall may be profits taxed abroad, which the model does not have. About a third of it came
after 1984 (the rate fell from 22 to 14 per cent), and Hager and Baines ("The Tax Advantage of Big
Business", 2020) find from company accounts that after 1984 "the domestic ETR of the top decile
increases slightly over the entire period, from 30 percent in 1984-89 to 34 percent in 2010-18",
while the rate paid abroad fell from 47 to 25 per cent. So `owners_resist` may be too high by up
to a third for a model with no abroad; the fit has not been redone on profits earned at home. In
terms of power: how much of what the government lacks owners let it take back, how much of what
it does not need they take for themselves, and their steady power to resist being taxed.

With `rise_kept`, on by default, a rise after a deficit takes a part of what is kept, and
`rise_part` and `rise_pace` are not used. The part of firms' earnings kept after all the rates in law, added up,
falls by `kept_earnings` times last year's deficit as a part of all income, in proportion, and the
part of wages kept by `kept_wages` times it. For example, a rate of 0.2 on earnings and a deficit
of a tenth of all income leave owners 0.8 × exp(-0.0155) of their earnings, so the rate becomes
0.212. A rate set this way comes closer to the whole of earnings after each deficit and never
reaches it. A rule that brings in a part of the deficit raises the rate on earnings 5.2 times as
fast as the rate on wages, in proportion, and in a run with a deep slump that rule took the rate
for public pay to 5.4 times firms' earnings: when earnings had all but vanished, the money had to
come from wages, and the rate on earnings rose eight times in a year. Both figures are from the
same accounts as the rest, with the change of military spending as a part of national product held
apart: a deficit of 1 per cent of national product was followed by a fall of the part of profits
kept of 0.155 per cent (give or take 0.156) and of the part of pay kept of 0.054 per cent (give or
take 0.071). Both are smaller than their errors: once war is held apart, the record shows little
rise after deficits. In the record the rates lay between 0.10 and 0.47 on profits and between 0.14
and 0.29 on pay, where the change of a rate and the change of the part kept fit about as well (on
profits a share of the variation explained of 0.33 for the part kept and 0.36 for the rate). The
record cannot tell the two apart; the part kept is chosen because a rate of tax is a part of the
income it is charged on.

Rates also rise in a war. Nitzan and Bichler write that after the Second World War "sharp
increases in corporate taxation" lowered the share of after-tax profit and interest in national
income, and that "Subsequently, though, the effective tax rate drifted downwards" (chapter 13,
"Owners and technocrats", note). When military jobs (the force module) rose last year as a part
of the working population, the part of earnings kept falls by `war_earnings`, 1.80, times the
rise, in proportion, and the part of wages kept by `war_wages`, 0.25, times it. In the same
accounts a rise of federal military spending of 1 per cent of national product came with a fall of
the part of profits kept of 1.80 per cent (give or take 0.45) and of the part of pay kept of 0.25
per cent (give or take 0.20) in the same year. A fall of military spending came with a cut less
than twice its error, which is left out. The force module's military jobs as a part of the working population
stand for its orders as a part of all income. In the record the rise comes in the same year as the
spending; here it comes in the year after the force module publishes it. In terms of power: in a
war, owners let the government tax them to pay for the war that their own contractors supply.

Additions to the book: the interest part of the first year, the government's interest stream
as a fixed part of all income, the stock that bailouts add to the debt and proceeds take from
it, the tax pressed by the holders of the added debt and its single rate on all income, the
number of years of falling unemployment before they press, repaying them in proportion to
capitalization, the form of the rise as a part of what is kept, and military jobs standing for
military spending.
"""
import numpy as np
from core import Publish, Transfer, lend_to_government, WAGE_EARNERS, GOVERNMENT

PRESSED = "tax pressed by the holders of the public debt"   # this module's income component; the core sets it
PRESSED_EARNINGS = "tax on earnings pressed by the holders of the public debt"
PRESSED_WAGES = "tax on wages pressed by the holders of the public debt"
REPAID = "repaid to the holders of the public debt"


class Debt:
    name = "debt"
    reads = ("transfers", "unemployment")
    supplies = ("interest_share", "corporate_debt", "government_debt", "government_debt_dominant",
                "tax_kept_earnings", "tax_kept_wages")
    figures = {                   # what the workbench calls each published number: label, unit, note
        "interest_share": ("Interest terms", "share", "Interest that firms owe, as a part of their earnings (the failure module); without it, the part of the first year."),
        "corporate_debt": ("Corporate debt", "number", "The debt that firms owe, in money (the failure module); without it, the interest capitalized at the normal rate of return."),
        'government_debt': ('Government debt', 'number', "Capitalized value of the government's interest payments, in money."),
        'government_debt_dominant': ('Government debt held by the top 100', 'number', "Taken to equal the top 100's part of all capitalization, in money."),
        "tax_kept_earnings": ("Rate on earnings kept", "share", "Each rate of tax in law on firms' earnings next year, as a part of this year's: below 1 after a surplus, above 1 after a deficit."),
        "tax_kept_wages": ("Rate on wages kept", "share", "Each rate of tax in law on wages next year, as a part of this year's: below 1 after a surplus, above 1 after a deficit."),
    }

    def __init__(self, government_part=0.02, start=0.20, holders_press=0.05, cut_surplus=True, owners_pace=2.3,
                 cut_part=0.24, rise_part=0.045, rise_pace=5.2, owners_resist=0.039, recovery_years=2,
                 rise_kept=True, kept_earnings=0.155, kept_wages=0.054, war_earnings=1.80, war_wages=0.25):
        self.government_part = government_part   # government interest payments as a part of all income
        self.share = start
        self.holders_press = holders_press   # tax pressed by the holders of the added debt, as a part of it in a year (Bohn 1998)
        self.cut_surplus = cut_surplus       # owners have the rates in law cut by what they bring in beyond what the government pays (Hager 2016, chapter 4)
        self.owners_pace = owners_pace       # how many times as fast the rate on earnings falls as the rate on wages, in proportion (Hager 2016, chapter 4: effective rates of the largest corporations and of households)
        self.cut_part = cut_part             # the part of a surplus that the cut takes away in a year (United States federal accounts, 1951 to 2017)
        self.rise_part = rise_part           # the part of a deficit that a rise of the rates brings in, in a year (the same accounts)
        self.rise_pace = rise_pace           # how many times as fast the rate on earnings rises as the rate on wages, in proportion (the same accounts)
        self.owners_resist = owners_resist   # the part of itself by which the rate on earnings falls each year whatever the balance, in proportion (the same accounts)
        self.recovery_years = recovery_years # years running of falling unemployment before the holders press (Hager 2016, chapter 4; the number is our own)
        self.rise_kept = rise_kept           # after a deficit, the rise takes a part of what is kept after the rates in law (True), or brings in `rise_part` of the deficit (False)
        self.kept_earnings = kept_earnings   # how far the part of earnings kept falls, in proportion, for a deficit of all income (United States federal accounts, 1951 to 2017)
        self.kept_wages = kept_wages         # the same for the part of wages kept (the same accounts)
        self.war_earnings = war_earnings     # how far the part of earnings kept falls, in proportion, when military jobs rise by the whole working population (the same accounts)
        self.war_wages = war_wages           # the same for the part of wages kept (the same accounts)
        self.military = None                 # military jobs last year, as a part of the working population (the force module); None without it
        self.jobless = []                    # unemployment of past years, as the core published it
        self.ordered = (1.0, 1.0)            # the change ordered last year: each rate on earnings and on wages next year, as a part of this year's
        self.published = (1.0, 1.0)          # the same change with the owners' wearing down, as published
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
        # The holders of the added debt press for repayment in a lasting recovery: one rate on the wage bill
        # and on every firm's earnings before this tax, and the government repays them what it collects.
        if "unemployment" in A:
            self.jobless.append(float(A["unemployment"]))
        press = self.holders_press * max(self.added, 0.0) if self.recovering() else 0.0
        if press > 0:
            wages = L.shared["wage"] * L.n.sum()
            base = np.maximum(L.earnings() - L.n * L.components[PRESSED], 0.0)
            rate = press / (wages + base.sum())
            changes += [Transfer(PRESSED_EARNINGS, payer=rate * base, receiver=GOVERNMENT, source=self.name),
                        Transfer(PRESSED_WAGES, payer=WAGE_EARNERS, receiver=GOVERNMENT, source=self.name,
                                 amount=rate * wages)]
            changes += lend_to_government(REPAID, -press, L, GOVERNMENT, self.name)
        # The rise of military jobs last year, as a part of the working population (the force module).
        armed = 0.0
        if "force_jobs" in A:
            jobs = float(A["force_jobs"])
            if self.military is not None:
                armed = max(jobs - self.military, 0.0)
            self.military = jobs
        income = float(L.earnings().sum()) + L.shared["wage"] * L.n.sum()
        changes += self.order_cut(A.get("government", {}), income, armed)
        return changes

    def recovering(self):
        """Whether unemployment has fallen in each of the last `recovery_years` years."""
        n = int(self.recovery_years)
        if n <= 0:
            return True
        u = self.jobless[-(n + 1):]
        return len(u) == n + 1 and all(b < a for a, b in zip(u, u[1:]))

    def order_cut(self, G, income=0.0, armed=0.0):
        """Move the rates in law by last year's balance of the taxes at those rates, less what the change
        ordered last year will already do. The tax pressed by the holders of the debt is not counted: it
        is collected to repay them. In a surplus, owners have the rates cut by `cut_part` of it, the rate
        on earnings falling `owners_pace` times as fast as the rate on wages, in proportion. In a deficit,
        with `rise_kept`, the part of earnings kept after all the rates in law falls by `kept_earnings`
        times the deficit as a part of `income`, in proportion, and the part of wages kept by
        `kept_wages` times it; without it the rates rise to bring in `rise_part` of the deficit, the
        rate on earnings rising `rise_pace` times as fast as the rate on wages. When military jobs rose
        last year by `armed` of the working population, the parts kept fall further, by `war_earnings`
        and `war_wages` times it. The modules that tax at a rate in law apply the change the next year."""
        if not self.cut_surplus:
            return []
        te, tw = float(G.get("taxed_earnings", 0.0)), float(G.get("taxed_wages", 0.0))
        # the rates in law added up, as they stand this year after the change published last year
        re = float(G.get("rate_earnings", 0.0)) * self.published[0]
        rw = float(G.get("rate_wages", 0.0)) * self.published[1]
        gaps = G.get("gaps", {})
        surplus = -sum(gaps[k] for k in sorted(gaps) if k != REPAID)
        ke, kw = self.ordered
        left = surplus - te * (1.0 - ke) - tw * (1.0 - kw)   # what remains after the change already ordered
        self.ordered = (1.0, 1.0)
        if left > 0 and te + tw > 0:         # a surplus: owners have a part of it cut, theirs faster
            want, a = self.cut_part * left, self.owners_pace
            if want >= te + tw:              # the taxes brought in more than all they pay for: no rate is left
                self.ordered = (0.0, 0.0)
            else:
                k = self._solve(lambda k: te * (1.0 - np.exp(-a * k)) + tw * (1.0 - np.exp(-k)), want)
                self.ordered = (float(np.exp(-a * k)), float(np.exp(-k)))
        elif left < 0 and self.rise_kept and te + tw > 0 and income > 0:   # a deficit: a part of what is kept is taken
            d = -left / income
            self.ordered = (self._kept(re, self.kept_earnings * d), self._kept(rw, self.kept_wages * d))
        elif left < 0 and not self.rise_kept and self.rise_part > 0 and te + tw > 0:   # a deficit: a part of it is raised
            want, b = -self.rise_part * left, self.rise_pace
            k = self._solve(lambda k: te * (np.exp(b * k) - 1.0) + tw * (np.exp(k) - 1.0), want)
            self.ordered = (float(np.exp(b * k)), float(np.exp(k)))
        if armed > 0 and te + tw > 0:        # military orders grew: a further part of what is kept is taken
            ke, kw = self.ordered
            self.ordered = (ke * self._kept(re * ke, self.war_earnings * armed),
                            kw * self._kept(rw * kw, self.war_wages * armed))
        resisted = float(np.exp(-self.owners_resist))   # owners wear the rate on earnings down, whatever the balance
        self.published = (self.ordered[0] * resisted, self.ordered[1])
        return [Publish("tax_kept_earnings", self.published[0], self.name),
                Publish("tax_kept_wages", self.published[1], self.name)]

    @staticmethod
    def _kept(rate, fall):
        """What a rate is multiplied by when the part of the income kept after it, 1 - rate, falls by
        `fall` in proportion (in logarithms). The new rate is 1 - (1 - rate) * exp(-fall): it rises by
        about `fall` itself while the rate is small, and comes ever closer to the whole income without
        reaching it. A rate of 0 has nothing to rise from, and a rate of 1 or more leaves nothing kept."""
        if fall <= 0 or not 0.0 < rate < 1.0:
            return 1.0
        return float((1.0 - (1.0 - rate) * np.exp(-fall)) / rate)

    @staticmethod
    def _solve(taken, want):
        """The k at which `taken`, which rises with k from 0, comes to `want`: found by halving the interval."""
        lo, hi = 0.0, 1.0
        while taken(hi) < want:
            hi *= 2.0
        for _ in range(100):
            mid = 0.5 * (lo + hi)
            lo, hi = (mid, hi) if taken(mid) < want else (lo, mid)
        return 0.5 * (lo + hi)
