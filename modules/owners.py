"""Module 18: who owns the firms.

THE RULE IN PLAIN WORDS

Without this module the ledger holds firms and says nothing about who owns them. This module
gives every firm one more number: the part of the firm that its own large owners hold
directly. The rest of the firm is held through institutional investors, which are funds that
hold many firms at once. The module changes only this number. It changes no price, no
earnings, no employment and no capitalization, so every other figure of a run stays the same.

  1. At the start every firm is held wholly and directly by its own owners. A newly founded
     firm is also held wholly and directly.
  2. The listed firms are the largest firms by capitalization: one firm in every five
     hundred, and never fewer than the top hundred. Only listed firms can be bought by
     institutional investors.
  3. Each year the direct owners of a listed firm offer for sale a fixed part of what they
     hold above a controlling block. They never sell the controlling block.
  4. Two kinds of institutional investor bring money each year. Funds of the first kind are
     fed from wages and stand for pension funds. They bring a fixed part of the wage bill.
     Funds of the second kind are fed from capitalist earnings and stand for mutual funds,
     hedge funds and the like. They bring a fixed part of all earnings. The two kinds buy the
     shares on offer in proportion to the money each brings. If the money is less than the
     value of the shares on offer, only that much is sold.
  5. A merger leaves the buyer's pattern of ownership in place for the whole merged firm.
     The owners of the target are paid off and hold nothing in it afterwards. (This is how
     core.py treats every added attribute.)
  6. The module traces each firm's capitalization and earnings back along the chain: from
     the firm, to direct owners or to one of the two kinds of fund, and from there to two
     groups of households. The first group is the richest one per cent of households, which
     stands for the small minority that holds assets for accumulation. The second group is
     everybody else. The parts that the richest one per cent hold of directly held shares, of
     pension funds and of mutual funds are three settings taken from Sandy Brian Hager's
     tables.
  7. The module publishes these readouts every year, measured at the start of the year:
       owners_indirect            part of all capitalization held through institutional investors
       owners_indirect_top        the same part for the top hundred firms
       owners_wide                part of the institutional holdings that is in funds fed from wages
       owners_income_direct       part of all capitalist earnings that goes to direct owners
       owners_income_wage_funds   part that goes to funds fed from wages
       owners_income_profit_funds part that goes to funds fed from capitalist earnings
       owners_top_percent_cap     part of all capitalization that belongs in the end to the richest one per cent
       owners_top_percent_income  part of all income (wages and earnings) that reaches the richest one per cent as owners
       owners_reach               part of all employees who work in firms where the institutional
                                  investors together hold at least a controlling block
       owners_placed              part of the funds' new money that found shares to buy

No existing module reads these numbers. Ownership is reported and has no effect on conduct.
That is a choice that follows the literature (see the last passage below), not an oversight.

WHAT IT RESTS ON

  - Capital as Power, chapter 12, "The absentee ownership of power". "Modern capitalists have
    become investors of 'funds', absentee owners of pecuniary wealth with no direct
    industrial dealings." "Currently, roughly half of all capitalist assets are owned
    indirectly through institutional investors such as pension and mutual funds, hedge and
    sovereign funds, insurance companies, banks and corporations. The ultimate owners of
    these assets, whether big or small, exercise little voice in the management of the
    underlying production processes. For the most part, they merely buy and sell shares of
    these assets and collect the flow of dividends. Often, their diversification is so
    extensive that they don't know exactly what they own." The chapter adds that "many of
    the largest direct investors" are "equally removed from any industrial dealings" and
    spend their energies on "cutting and pasting assets through endless deals of divestment
    and merger". Parts 1 to 4 give this passage a form: direct owners, institutional
    investors, and "roughly half" as the figure the readout owners_indirect can be set against.
  - Chapter 14, "The universe of owners". There are "two types of assets: those that are held
    for use and those that are held for accumulation. The vast majority of owners hold the
    first type", which includes "primarily savings and pensions". "The aggregate magnitude of
    these assets could be substantial, but their individual size tends to be small. Most
    importantly, these assets give their owners little or no control over other people."
    "A small minority of owners holds the second type of assets", which "give their owners
    direct and indirect control over other people". The same section says: "we focus not on
    individual owners, but on groups of owners". The two kinds of fund in part 4 and the two
    groups of households in part 6 rest on this.
  - Chapter 13, "Owners and technocrats". "The separation of ownership from control was never
    much more than a 'pseudofact'." "It is not the engineers and bureaucrats, but the
    capitalists who are in the driver seat." "And whether the capitalists are absent or
    present, the logic of their mega-machine seems to enforce this accumulation on society
    with increasing mechanical exactitude." The controlling block in part 3 rests on the
    first two sentences. The choice that ownership changes no conduct rests on the third.
  - Chapter 13, "Sovereign owners?". By setting up sovereign wealth funds "governments are
    further integrating, if not locking themselves, into the larger architecture of
    capitalist power". The module does not hold government funds apart from other funds.
  - Sandy Brian Hager, "What Happened to the Bondholding Class?" (2013), Table 2. The richest
    one per cent of United States households held 61.5 per cent of corporate stocks in 1922,
    76 per cent in 1953 and 51.3 per cent in 2010. They held 8 per cent of pension assets in
    1922 and 15.3 per cent in 2010. Hager uses the richest one per cent as his stand-in for
    the owning class.
  - Sandy Brian Hager, "Corporate Ownership of the Public Debt" (2015). "Pensions funds, for
    their part, are indeed widely owned, with the top percentile of US households owning only
    15 percent of their total assets in 2010 (up from eight percent in 1983). The ownership of
    mutual funds, however, is heavily concentrated, with the top percentile owning 47 percent
    of their total assets in 2010 (up from 40 percent in 1983)."
  - Joseph Baines and Sandy Brian Hager, "From Passive Owners to Planet Savers? Asset
    Managers, Carbon Majors and the Limits of Sustainable Finance" (2022).
    "The Big
    Three own more than 20 percent of shares in the average S&P 500 company". "With dispersed
    shareholding, effective control can be exercised with stakes as low as five percent", and
    Maurice Zeitlin showed "that control can be exercised effectively with as little as five
    to 10 percent ownership stakes". Index funds "have a reputation for passively following
    broad market indices". The paper finds that the three largest managers "much more often
    than not oppose rather than support" shareholder resolutions on the environment. The
    controlling block of 10 per cent in parts 3 and 7, and buying in proportion to what is on
    offer among the largest firms, rest on this paper.

WHAT IS ADDED

The literature says who the owners are and how much they hold at certain dates. It gives no
rule for how ownership passes from direct owners to institutional investors. Parts 2, 3 and 4
are therefore additions. The four numbers from the literature are the controlling block of
10 per cent and the three parts held by the richest one per cent (51.3, 15.3 and 47 per cent
in 2010). Holding those three parts fixed for the whole run is an addition, because Hager
shows that they moved. Every other number is an addition: one firm in five hundred is
listed, direct owners offer 5 per cent a year, funds fed from wages bring 3 per cent of the
wage bill, and funds fed from earnings bring 20 per cent of earnings. Part 5 is an addition
that comes from core.py: it treats every merger as a purchase for money and none as an
exchange of shares.

WHAT IS MISSING

The institutional investors are two pools and not separate bodies, so the module cannot show
three managers holding a fifth of every large firm. Funds never sell: pension funds pay
nothing out to pensioners. Money that finds no shares disappears from the account; in the
literature money that chases shares raises their prices, which is hype, and hype is held at
one in this model. Banks, insurance companies and corporations that hold other corporations
are not held apart. Ownership of the corporate debt and the government's debt of module 2 is not traced. The richest
one per cent also receive salaries, and those are counted as wages here. Jongchul Kim's paper
on money market funds ("Propertization", 2018) was looked at and gives nothing this ledger
could hold.
"""
import numpy as np
from core import Scale, Publish, top_positions

ATTRIBUTE = "held_directly"     # the part of a firm that its own large owners hold directly


class Owners:
    name = "owners"
    reads = ()
    supplies = ("owners_indirect", "owners_indirect_top", "owners_wide", "owners_income_direct",
                "owners_income_wage_funds", "owners_income_profit_funds", "owners_top_percent_cap",
                "owners_top_percent_income", "owners_reach", "owners_placed")
    figures = {                   # what the workbench calls each published number: label, unit, note
        "owners_indirect": ("Held through funds", "share", "Part of all capitalization held through institutional investors."),
        'owners_indirect_top': ('Top 100 held through funds', 'share', "Part of the top 100's capitalization held through institutional investors."),
        "owners_wide": ("Fund holdings fed from wages", "share", "Part of institutional holdings in funds fed from wages."),
        "owners_income_direct": ("Earnings to direct owners", "share", "Part of all capitalist earnings that goes to direct owners."),
        "owners_income_wage_funds": ("Earnings to funds fed from wages", "share", "Part of all capitalist earnings that goes to funds fed from wages."),
        "owners_income_profit_funds": ("Earnings to funds fed from profits", "share", "Part of all capitalist earnings that goes to funds fed from capitalist earnings."),
        "owners_top_percent_cap": ("Capitalization owned by the richest 1%", "share", "Part of all capitalization that belongs in the end to the richest 1%."),
        "owners_top_percent_income": ("Income to the richest 1% as owners", "share", "Part of all income that reaches the richest 1% as owners."),
        "owners_reach": ("Employees in fund-controlled firms", "share", "Part of all employees in firms where funds together hold a controlling block."),
        'owners_placed': ('Fund money placed', 'share', "Part of the funds' new money that found shares to buy."),
    }

    def __init__(self, listed_one_in=500, sell_rate=0.05, control_block=0.10, save_wages=0.03,
                 save_earnings=0.20, rich_direct=0.513, rich_wage_funds=0.153, rich_profit_funds=0.47,
                 top=100):
        self.listed_one_in = listed_one_in   # one firm in this many is listed and can be bought by funds (never fewer than the top hundred)
        self.sell_rate = sell_rate           # part of their holding above the controlling block that direct owners of a listed firm offer each year
        self.control_block = control_block   # the block that direct owners never sell; 10 per cent is the upper figure Baines and Hager report from Zeitlin
        self.save_wages = save_wages         # part of the wage bill that funds fed from wages (pension funds) bring each year
        self.save_earnings = save_earnings   # part of all earnings that funds fed from capitalist earnings (mutual funds and the like) bring each year
        self.rich_direct = rich_direct              # part of directly held shares that belongs to the richest one per cent (Hager 2013, Table 2, corporate stocks, 2010); one year's reading held fixed for the whole run, which is an addition: the same table gives 76 per cent for 1953
        self.rich_wage_funds = rich_wage_funds      # part of pension assets that belongs to the richest one per cent (Hager 2013, Table 2, 2010); one year's reading held fixed for the whole run, which is an addition: the same table gives 5.5 per cent for 1953
        self.rich_profit_funds = rich_profit_funds  # part of mutual fund assets that belongs to the richest one per cent (Hager 2015, for 2010); one year's reading held fixed for the whole run, which is an addition: Hager gives 40 per cent for 1983
        self.top = top
        self.wide = 0.0                      # part of all institutional holdings that is in funds fed from wages

    def measure(self, L):
        """The readouts, from the ledger as it stands."""
        K, E, n, d = L.cap(), L.earnings(), L.n, L.extra[ATTRIBUTE]
        top = top_positions(K, np.arange(len(L)), self.top)
        through = 1.0 - d                                    # part of each firm held through funds
        # part of each firm that belongs in the end to the richest one per cent of households
        rich = d * self.rich_direct + through * (self.wide * self.rich_wage_funds
                                                 + (1.0 - self.wide) * self.rich_profit_funds)
        income = E.sum() + L.shared["wage"] * n.sum()
        e_through = float((through * E).sum() / E.sum())
        return {"owners_indirect": float((through * K).sum() / K.sum()),
                "owners_indirect_top": float((through[top] * K[top]).sum() / K[top].sum()),
                "owners_wide": float(self.wide),
                "owners_income_direct": 1.0 - e_through,
                "owners_income_wage_funds": e_through * self.wide,
                "owners_income_profit_funds": e_through * (1.0 - self.wide),
                "owners_top_percent_cap": float((rich * K).sum() / K.sum()),
                "owners_top_percent_income": float((rich * E).sum() / income),
                "owners_reach": float(n[through >= self.control_block - 1e-12].sum() / n.sum())}

    def start(self, L):
        L.add_attribute(ATTRIBUTE, 1.0, 1.0)     # every firm, old or new, begins wholly in the hands of its own owners
        out = self.measure(L)
        out["owners_placed"] = 0.0
        return out

    def propose(self, L, rng):
        K, E, d = L.cap(), L.earnings(), L.extra[ATTRIBUTE]
        count = len(L)
        out = self.measure(L)

        # part 2: the listed firms
        listed = top_positions(K, np.arange(count), max(self.top, count // self.listed_one_in))
        # part 3: what direct owners offer this year, in money
        offer = np.zeros(count)
        offer[listed] = self.sell_rate * np.maximum(d[listed] - self.control_block, 0.0) * K[listed]
        # part 4: the money the two kinds of fund bring
        from_wages = self.save_wages * L.shared["wage"] * L.n.sum()
        from_earnings = self.save_earnings * E.sum()
        money = from_wages + from_earnings
        offered = offer.sum()
        sold = offer * min(1.0, money / offered) if offered > 0 else offer
        spent = sold.sum()
        out["owners_placed"] = float(spent / money) if money > 0 else 0.0

        # the make-up of the institutional holdings after this year's purchases
        held = ((1.0 - d) * K).sum()
        if held + spent > 0 and money > 0:
            self.wide = float((self.wide * held + spent * from_wages / money) / (held + spent))

        changes = [Publish(key, value, self.name) for key, value in out.items()]
        if spent > 0:
            changes.append(Scale(ATTRIBUTE, (d - sold / K) / d, self.name))
        return changes
