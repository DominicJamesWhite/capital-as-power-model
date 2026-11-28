"""Optional module: who holds the public debt and who pays for it.

THE RULE IN PLAIN WORDS

Module 2 keeps the government's debt as one running total and only reports it. This module says who
holds that debt and who pays its interest. The interest that a firm in the ledger receives,
less the tax that the firm pays toward all interest, becomes part of the firm's earnings.
Nothing in the rule comes from outside the model. The size of the debt comes from module 2,
and the crisis, the concentration and the resistance come from the other rules.

  1. The interest. The government's yearly interest payment is the government debt that
     module 2 publishes, times the normal rate of return.
  2. Three groups of holders. The firms in the ledger hold a fixed part of the debt.
     Households hold a second fixed part directly. Government bodies and holders abroad hold
     the rest, and the module does not follow what they receive.
  3. Holdings among firms. Each firm holds public debt in proportion to its capitalization.
     Dominant capital's part of the firms' holdings is therefore its part of all
     capitalization.
  4. The flight to safety. When unemployment is above its usual level, the holdings of the
     firms of dominant capital count for more in that proportion. Five points of
     unemployment above the usual level count as a complete crisis.
  5. The tax. The whole interest of the year is paid from a tax of the same year. The tax is
     one rate on all income: on the wage bill, and on each firm's earnings before any income
     from the public debt. A tax on income takes a part of income, so a firm whose earnings
     are below nothing (because it paid other modules more than it now earns) pays none, and a
     firm whose capitalization is below nothing holds no debt.
  6. The tax advantage. Dominant capital pays a lower rate than everybody else. Its rate,
     as a part of the rate of others, is one minus the top hundred's part of all
     capitalization, and the reduction shrinks when popular resistance is high. Wages and the
     other firms make up what dominant capital does not pay. When 100 firms or fewer are left,
     all of them are dominant capital and hold all capitalization, so with no resistance they
     pay no tax and wages carry all of it.
  7. The change to the ledger. The module proposes six transfers, and the core settles them
     (see "The record of transfers" in modules.md). Two are the tax: each firm pays its tax
     to the government, and wage earners pay theirs. Four are the interest, which the
     government pays out of what it has received: to the firms, in proportion to their
     holdings; to wage earners, for the households outside the richest one per cent; to the
     richest one per cent of households; and to the holders that the module does not follow.
     No payer pays more than it has. A firm cannot pay more tax than its earnings of the
     year, wage earners cannot pay more than the wage bill, and the government cannot pay
     more interest than the tax it collected. The core enters, for each firm, the interest
     received less the tax paid in an income component that this module owns. The amount is
     replaced each year and never added twice. The income is not a markup, and the core
     keeps it apart from the markup.
  8. Readouts. The module publishes who holds, who receives and who pays (listed in
     `supplies` below). It also publishes, for each industry, the part of earnings that comes
     from sources other than public-debt income. No module reads that number. A readout that
     is a part of something that is nothing, such as the gain of the firms outside the top
     hundred when there are none, is 0.

The wage in the ledger is not changed. Wage earners are a party to the transfers: the core
records what they pay and what they receive, and no entry in the ledger stands for
them.

The module also publishes the part of last year's interest that the
government was able to pay. It is 1 unless the taxpayers could not pay the tax in full. The
risk shaping module reads it.

WHAT IT RESTS ON

  - Capital as Power, chapter 13, "The government bond". "This financial instrument marks the
    first systematic capitalization of power, namely, the power of government to tax. And
    since this power is backed by institutionalized force, the government bond represents a
    share in the organized violence of society." Parts 1 and 5 give this a form: the bond is
    a right to future taxes.
  - Chapter 13, "Government capitalized". "As capital grew into a state, the interaction
    between its organizational bodies of corporations and governments multiplied and
    intensified." "The government bond market has become the heart of modern finance."
    Government activities "all bear on the differential level and temporal pattern of
    capitalist income", and they include "tax arrangements with various governments". "A
    significant proportion of all private property is, in fact, capitalized government
    power." Part 7 rests on this: public-debt income is part of the earnings that a firm's
    capitalization discounts.
  - Chapter 5 notes that interest on the public debt is "paid usually to capitalist owners of
    the public debt".
  - Sandy Brian Hager, "What Happened to the Bondholding Class?" (2013). "If the group that
    receives the interest payments on the public debt (that is, the public creditors) is not
    the same as the group that pays the taxes that finances those interest payments (that is,
    the taxpayers), then the public debt will serve as a mode of redistribution from the
    latter to the former." The richest one per cent of households held 45 per cent of the
    public debt in 1922, 17 per cent in 1969 and 42 per cent in 2010 (Figure 2 and Table 2).
    "The federal income tax system has done little to offset the growing inequity in the
    distribution of federal interest payments." "There is technically no way to determine
    precisely who pays the taxes that finance interest payments", because no tax is earmarked
    for interest. Part 5 (one rate on all income) rests on the last two sentences.
  - Sandy Brian Hager, "Corporate Ownership of the Public Debt" (2015), Table 1 and note 1.
    The 2,500 largest corporations held 66 per cent of the corporate share of the public debt
    in 1957-61, 65 per cent in 1977-81 and 82 per cent in 2006-10. They held 62, 70 and 81
    per cent of all corporate assets in the same periods: "What stands out is the remarkable
    synchronicity of public debt and general asset concentration." Part 3 rests on this.
    "In 2006 before the onset of the crisis, large corporations owned 77 percent of the
    corporate share of the public debt and this share grew to 86 percent in 2010"; "it is
    overwhelmingly large corporations at the top of the business hierarchy that have enjoyed
    the current 'flight to safety'". Part 4 rests on this. In the 1950s "US households owned
    on average 31 percent of the US public debt, US businesses 52 percent and the rest of the
    world only three percent". Part 2 uses these figures. "Corporate income taxes make up
    only 10 percent of total US federal revenues", and the largest 2,500 corporations paid
    68 per cent of them. Their effective tax rate was 45 per cent in 1956-61 and 22 to 23 per
    cent afterwards. Hager takes from Wolfgang Streeck that tax stagnation is due to "the
    successful tax resistance waged on the part of increasingly powerful elites".
  - Sandy Brian Hager, Public Debt, Inequality, and Power (2016).
    "When the
    share of wealth owned by wealthy households and large corporations increases or
    decreases, so too does their share of the public debt." The richest one per cent of
    households held 56 per cent of the household share by 2013. "The federal government has
    come to rely on borrowing from wealthy households and large corporations instead of
    taxing them."
  - Sandy Brian Hager and Joseph Baines, "The Tax Advantage of Big Business" (2020).
    "We should
    expect an increase in the degree of monopoly (power) of large corporations to be bound up
    with a decrease in their ETR relative to smaller corporations." In recent years the top
    tenth of corporations paid a worldwide effective tax rate of 28 per cent and the other
    nine tenths 41 per cent. Part 6 rests on this paper.

WHAT IS ADDED

The literature measures who holds the public debt and what large owners pay in tax at certain
dates. It gives no rule that moves either. Four numbers come from figures in the literature:
the firms' part of the debt (52 per cent) and the households' part (31 per cent), both for
the 1950s; the richest one per cent's part of household holdings (42 per cent, for 2010); and
the weight of 1.83 in a complete crisis, which is what turns a part of 77 per cent into a part
of 86 per cent. Holding the first three fixed for a whole run is an addition, because Hager
shows that they moved. Applying the weight of 2006-10 to every crisis, and measuring crisis by
unemployment, are additions. The form of part 6 is an addition: the literature says that the
tax rate of large corporations falls as their power rises and gives no formula. The setting
of 1.0 makes a top hundred that holds a third of all capitalization pay about two thirds of
the rate of others, which is near 28 against 41. That popular resistance shrinks the
advantage is an addition. Paying all interest from the taxes of the same year is an addition,
and so is taxing earnings before public-debt income and not after. Using the hundred largest
firms where Hager uses the 2,500 largest corporations is an addition. Counting the households
outside the richest one per cent as wage earners is an addition. The tax is reckoned on the
figures at the start of the year and is collected at the end of it, which is an addition.

WHAT IS MISSING

The debt does not grow. Hager's main argument about the present is that the government
borrows from large owners instead of taxing them, so the debt rises as their tax falls. Module
2 fixes the interest as a part of all income, and this module does not change that. Financial
corporations are not held apart, although Hager finds that they hold nearly all of the
corporate share. Holders abroad and government trust funds are not followed. The ownership
of the firms is not traced, so the module cannot add what the richest households receive
through the corporations and funds that they own. Hager's finding that policy papers came to
speak the language of bondholders has no place in this rule.
"""
import numpy as np
from core import Transfer, Publish, top_positions, lend_to_government, WAGE_EARNERS, GOVERNMENT

INCOME = "public debt income"   # this module's income component: interest received less tax paid, for each employee; the core sets it from the transfers below
RICH = "richest households"                             # a party that only receives: the richest one per cent of households
REST = "holders of the public debt outside the ledger"  # a party that only receives: government bodies and holders abroad

TAX_EARNINGS = "tax on earnings for interest on the public debt"
TAX_WAGES = "tax on wages for interest on the public debt"
TO_FIRMS = "interest on the public debt, to firms"
TO_WAGES = "interest on the public debt, to households outside the richest one per cent"
TO_RICH = "interest on the public debt, to the richest one per cent of households"
TO_REST = "interest on the public debt, to holders outside the ledger"
INTEREST = (TO_FIRMS, TO_WAGES, TO_RICH, TO_REST)
LENT = "lent to the government for interest on the public debt"   # below 0 in a year, repaid by it


class PublicDebt:
    name = "public_debt"
    reads = ("government_debt", "unemployment")
    supplies = ("public_debt_markup_part", "public_debt_dominant", "public_debt_dominant_of_firms",
                "public_debt_tax_dominant", "public_debt_tax_wages", "public_debt_relative_tax",
                "public_debt_net_dominant", "public_debt_net_others", "public_debt_net_firms",
                "public_debt_net_wages", "public_debt_rich_households", "public_debt_flight",
                "public_debt_service")
    figures = {                   # what the workbench calls each published number: label, unit, note
        'public_debt_dominant': ('Public debt held by the top 100', 'share', "The top 100's part of the whole public debt."),
        'public_debt_dominant_of_firms': ("Top 100's part of firms' public debt", 'share', "The top 100's part of the public debt that firms hold."),
        "public_debt_tax_dominant": ("Tax for interest paid by the top 100", "share", "Part of the tax for interest that the top 100 pay."),
        "public_debt_tax_wages": ("Tax for interest paid from wages", "share", "Part of the tax for interest that is paid from wages."),
        'public_debt_relative_tax': ('Relative tax rate of the top 100', 'times', "The top 100's tax rate divided by the rate of others."),
        "public_debt_net_dominant": ("Net gain of the top 100 from public debt", "share", "As a part of their other earnings."),
        "public_debt_net_others": ("Net gain of other firms from public debt", "share", "As a part of their other earnings."),
        "public_debt_net_firms": ("Net gain of all firms from public debt", "share", "As a part of all income."),
        "public_debt_net_wages": ("Net gain of households from public debt", "number", "Interest to households outside the richest 1%, less the tax on wages, as a part of the wage bill."),
        "public_debt_rich_households": ("Interest paid to the richest 1%", "share", "Part of all interest paid directly to the richest 1% of households."),
        "public_debt_flight": ("Flight to safety", "index", "The level of crisis that drives the flight to safety."),
        'public_debt_service': ('Interest paid by the government', 'share', "Part of last year's interest that the government was able to pay."),
    }

    def __init__(self, firms_part=0.52, household_part=0.31, rich_households=0.42,
                 flight_weight=1.83, usual_unemployment=0.05, crisis_span=0.05,
                 tax_advantage=1.0, wage_tax=1.0, top=100):
        self.firms_part = firms_part          # part of the public debt held by the firms in the ledger (Hager 2015, note 1: United States businesses in the 1950s); the average of one decade held fixed for the whole run, which is an addition: the same note gives 23 per cent for 2009 to 2014
        self.household_part = household_part    # part held directly by households (same note, the 1950s); held fixed for the whole run, which is an addition: the note gives 9 per cent for 2009 to 2014
        self.rich_households = rich_households  # part of household holdings that belongs to the richest one per cent (Hager 2013, Table 2, for 2010); one year's reading held fixed for the whole run, which is an addition: the table gives 24.6 per cent for 1962
        self.flight_weight = flight_weight      # in a complete crisis a unit of dominant capital's capitalization holds this many times the debt of any other unit (the value is an addition: Hager 2015 prints no such weight; it was worked out for this module from his report that the largest 2,500 corporations held 77 per cent of the corporate share of the debt in 2006 and 86 per cent in 2010, which is one crisis and a different group from the hundred largest firms)
        self.usual_unemployment = usual_unemployment   # unemployment at which there is no flight to safety
        self.crisis_span = crisis_span          # points of unemployment above the usual level that count as a complete crisis
        self.tax_advantage = tax_advantage      # fall in dominant capital's tax rate, as a part of the rate of others, per unit of the top hundred's part of all capitalization
        self.wage_tax = wage_tax                # the rate on wages as a part of the rate on earnings; 1 means one rate on all income
        self.top = top
        self.rate = None                        # the rate of tax for interest, set in law in the first year and kept

    def start(self, L):
        # No firm, old or new, starts with public-debt income. The core sets the component each year
        # from this module's transfers, and every one of them has a payer.
        L.add_component(INCOME, self.name, kind="income", transfers=True)
        L.add_party(RICH)
        L.add_party(REST)
        out = {key: 0.0 for key in self.supplies}
        out["public_debt_markup_part"] = np.ones(L.sector_of.size)
        out["public_debt_relative_tax"] = 1.0
        out["public_debt_service"] = 1.0
        return out

    def propose(self, L, rng):
        A = L.accounts
        K, E = L.cap(), L.earnings()
        count, k = len(L), L.sector_of.size
        # Earnings before public-debt income. A firm whose earnings, after what it paid other modules
        # last year, are below nothing has no income to tax and pays no tax on it.
        base = np.maximum(E - L.n * L.components[INCOME], 0.0)
        K = np.maximum(K, 0.0)                               # a firm worth nothing holds no public debt
        wages = L.shared["wage"] * L.n.sum()
        top = top_positions(K, np.arange(count), self.top)
        dominant = np.zeros(count, dtype=bool)
        dominant[top] = True

        # part 1: the interest of the year
        interest = float(A["government_debt"]) * L.shared["nrr"]

        # parts 3 and 4: holdings among firms, with the flight to safety
        crisis = float(np.clip((A["unemployment"] - self.usual_unemployment) / self.crisis_span, 0.0, 1.0))
        weight = K * np.where(dominant, 1.0 + (self.flight_weight - 1.0) * crisis, 1.0)
        holding = weight / weight.sum()                      # each firm's part of the firms' holdings
        received = self.firms_part * interest * holding

        # parts 5 and 6: one rate on all income, less for dominant capital
        tie = K[top].sum() / K.sum()
        resistance = min(1.0, A.get("resistance", 0.0))
        relative = 1.0 - float(np.clip(self.tax_advantage * tie * (1.0 - resistance), 0.0, 1.0))
        liable = base * np.where(dominant, relative, 1.0)
        taxable = self.wage_tax * wages + liable.sum()
        if self.rate is None and interest > 0:  # the rate in law covers the first year's interest and stays put
            self.rate = float(interest / taxable)
        rate = self.rate or 0.0
        paid = rate * liable
        wage_tax = rate * self.wage_tax * wages

        # part 7: the transfers. The tax goes to the government, and the government pays the interest
        # out of it. The core limits each payment to what its payer has.
        to_wages = self.household_part * (1.0 - self.rich_households) * interest
        to_rich = self.household_part * self.rich_households * interest
        to_rest = (1.0 - self.firms_part - self.household_part) * interest
        transfers = [Transfer(TAX_EARNINGS, payer=paid, receiver=GOVERNMENT, source=self.name),
                     Transfer(TAX_WAGES, payer=WAGE_EARNERS, receiver=GOVERNMENT, source=self.name, amount=wage_tax),
                     Transfer(TO_FIRMS, payer=GOVERNMENT, receiver=holding, source=self.name,
                              amount=self.firms_part * interest),
                     Transfer(TO_WAGES, payer=GOVERNMENT, receiver=WAGE_EARNERS, source=self.name, amount=to_wages),
                     Transfer(TO_RICH, payer=GOVERNMENT, receiver=RICH, source=self.name, amount=to_rich),
                     Transfer(TO_REST, payer=GOVERNMENT, receiver=REST, source=self.name, amount=to_rest)]
        # Owners lend what the tax at the rate in law does not cover, or are repaid what it collects beyond the interest.
        transfers += lend_to_government(LENT, float(interest - rate * taxable), L, GOVERNMENT, self.name)
        # The part of last year's interest that the government was able to pay (1 in the first year).
        last = A.get("transfers", {})
        asked = sum(last[label]["asked"] for label in INTEREST if label in last)
        service = sum(last[label]["paid"] for label in INTEREST if label in last) / asked if asked > 0 else 1.0

        # part 8: readouts, reckoned on the amounts asked for
        after = base + received - paid
        by_industry = np.bincount(L.ind, after, k)
        markup_part = np.where(by_industry > 0, np.bincount(L.ind, base, k) / np.maximum(by_industry, 1e-300), 1.0)
        to_others = to_wages

        def part(a, b):         # a as a part of b; 0 when there is nothing to measure against, as when no firm is left outside the top hundred
            return float(a / b) if b > 0 else 0.0

        out = {
            "public_debt_markup_part": markup_part,                                        # by industry; no module reads it
            "public_debt_dominant": float(self.firms_part * holding[top].sum()),          # top hundred's part of the whole public debt
            "public_debt_dominant_of_firms": float(holding[top].sum()),                   # top hundred's part of what firms hold
            "public_debt_tax_dominant": part(paid[top].sum(), paid.sum() + wage_tax),     # part of the tax that the top hundred pay
            "public_debt_tax_wages": part(wage_tax, paid.sum() + wage_tax),               # part of the tax that is paid from wages
            "public_debt_relative_tax": relative,                                          # dominant capital's rate as a part of the rate of others
            "public_debt_net_dominant": part((received[top] - paid[top]).sum(), base[top].sum()),            # net gain of the top hundred, as a part of their other earnings
            "public_debt_net_others": part((received[~dominant] - paid[~dominant]).sum(), base[~dominant].sum()),   # the same for all other firms
            "public_debt_net_firms": part((received - paid).sum(), base.sum() + wages),   # net gain of all firms, as a part of all income
            "public_debt_net_wages": part(to_others - wage_tax, wages),                   # interest to households outside the richest one per cent less the tax on wages, as a part of the wage bill
            "public_debt_rich_households": float(self.household_part * self.rich_households),   # part of all interest paid directly to the richest one per cent of households
            "public_debt_flight": crisis,                                                  # the level of crisis that drives the flight to safety
            "public_debt_service": float(service),                                         # the part of last year's interest that was paid; read by the risk shaping module
        }
        return [Publish(key, value, self.name) for key, value in out.items()] + transfers
