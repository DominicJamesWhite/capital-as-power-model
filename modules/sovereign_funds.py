"""Module 38: governments as owners.

THE RULE IN PLAIN WORDS

Without this module no government organ owns any part of a firm. This module adds one
government organ that holds a reserve of money and a fund of shares. The organ is an owner
like any other. Each year its fund is judged against the average, and the verdict changes how
the organ behaves toward the mergers of dominant capital. The module changes no price, no
earnings, no employment and no capitalization directly. It changes one added number on each
firm, and it publishes one number that the resistance module reads.

  1. The reserve. The organ keeps a reserve of money. The reserve is parked in government
     bonds and earns the normal rate of return. Each year the reserve also receives a fixed
     part of all capitalist earnings, and the earnings that belong to the shares in the fund.
     The reserve therefore swells when income shifts toward capitalists, which in this model
     happens during a bout of stagflation.
  2. The lure. Each year the organ moves a fixed part of the reserve into the fund.
  3. What the fund buys. The fund follows an index, which is the hundred largest firms. It
     buys the same additional part of every firm in the index, so that it spends on each in
     proportion to its capitalization. It never holds more than a small minority stake in any
     firm. Money that finds no room under that limit stays in the reserve.
  4. What the fund sells. When a firm drops out of the index the fund sells its whole stake
     in it, and the money returns to the reserve.
  5. Mergers. When a firm in the index buys another firm, the fund's stake covers the whole
     merged firm. (This is how core.py treats every added attribute.) The fund therefore
     gains from amalgamation exactly as the readout of differential capitalization does.
  6. The verdict. Each year the module compares two rates of growth over the year just ended.
     The first is the growth in the value of the shares that the fund held, with no new money
     counted. The second is the growth of the average capitalization of all firms. The
     verdict is the first less the second. A fund that grew by 5 per cent while the average
     grew by 8 per cent has failed. A fund that shrank by 2 per cent while the average shrank
     by 6 per cent has succeeded.
  7. The lock. The module averages the verdict over the last five years. When that average
     is below zero the organ is trailing the average. The organ then wears down the
     roadblocks that stand in the way of mergers, because mergers are what lift the firms it
     holds above the average. The yearly wearing down is a setting, times the part of the
     organ's assets that is held as shares, times how far the fund trails. A fund that trails
     by 5 per cent a year counts as trailing completely. A fund that beats the average does
     nothing. The resistance module subtracts this number, times the level of roadblocks,
     from the level of roadblocks. The number is 0 when this module is off.
  8. Readouts. The module publishes the verdict, the wearing down of roadblocks, the fund as
     a part of all capitalization, the fund's part of the hundred largest firms, the fund's
     own differential capitalization (its value divided by the average capitalization of a
     firm), the rank the fund would have if it were a firm, the reserve as a part of all
     capitalization, the part of the organ's assets held as shares, and the part of the
     organ's yearly income that comes from its shares.

Nothing in the rule comes from outside. The organ's income follows capitalist earnings, the
index is dominant capital, and the verdict follows dominant capital's own differential
accumulation.

WHAT IT RESTS ON

  - Capital as Power, chapter 13, "Sovereign owners?". "Traditionally, capitalist governments
    treated their foreign reserves as a buffer for securing imports and protecting the
    currency. Consequently, the extra money was usually 'parked' in liquid foreign government
    bonds." "Massive shifts in the global distribution of income gave rise to a significant
    concentration of foreign currency assets", and "these piles of cash made the lure of
    capital too difficult to resist, as a result of which many governments started to invest
    their holdings through a new institution: the 'sovereign wealth fund'". Parts 1 and 2
    give this a form: a reserve in bonds that is fed by a shift of income, and a steady move
    from the reserve into shares.
  - The same section. "By 2006, sovereign wealth funds had amassed assets estimated at $2.5
    trillion - representing 10 per cent of all institutionally held investments in the world
    and nearly 1.5 per cent of all global financial assets." The readout sovereign_part can
    be set beside the second figure.
  - The same section. "By setting up and managing sovereign wealth funds, governments are
    further integrating, if not locking themselves, into the larger architecture of
    capitalist power." The book quotes an official of Abu Dhabi on the principles of its
    funds: "maximizing risk-adjusted returns, relative to well-established market indices;
    taking a long-term view; avoiding leverage; and investing in a well-diversified
    portfolio", with "the overwhelming share of its portfolio consisting of minority stakes
    in companies that have included no control rights". Part 3 rests on the index, the
    diversification and the minority stakes. Part 6 rests on "relative to well-established
    market indices". The five years of part 7 stand for "a long-term view". The fund never
    borrows.
  - The same section. "There is (still) no means of preventing governments from using their
    assets in line with their policy goals. But given the increasingly capitalist bent of
    these new sovereign owners of wealth, it is not clear how their investment and divestment
    decisions would differ from the business-as-usual policies of ExxonMobil, Bechtel or
    Samsung." Part 7 rests on this: an organ that owns a part of dominant capital acts for
    it.
  - Chapter 14, "Differential accumulation". "Every investment is stacked against its own
    group benchmark - and, in the abstract, against the global benchmark." "The goal is not
    to maximize but to exceed, not to meet but to beat. To achieve a 5 per-cent profit growth
    during recession is success; to gain 15 per cent when others make 30 is failure." Part 6
    is this test applied to the organ. The organ does not seek the largest possible fund.
  - Chapter 12, note on the price of oil. "The value of their sovereign wealth funds swells
    and contracts with the ups and downs of petroleum prices." Chapter 12 also lists
    "sovereign funds" among the institutional investors through which "roughly half of all
    capitalist assets are owned indirectly".
  - Chapter 13, "The state of capital": the section asks how far "the various organs of
    government have been conditioned, habituated and shaped by the logic of capital", and
    the sovereign fund is its second illustration. Chapter 13 treats corporations and
    government organs as bodies of one mode of power, so the organ is not set against
    dominant capital here.
  - Joseph Baines and Sandy Brian Hager, "From Passive Owners to Planet Savers?" (2022):
    "effective control can be exercised with stakes as low as five percent". The limit on
    the fund's stake is set at that figure, so that the fund stays below control.

The literature gives no rule.

WHAT IS ADDED

The literature says that governments became owners, that they follow indices and hold
minority stakes, and that this locks them into the order of capital. It gives no rule for
any of it. One number comes from the literature: the limit of 5 per cent on a stake. Every
other number is an addition: the organ receives 0.3 per cent of capitalist earnings a year, it
moves 10 per cent of its reserve a year, the index is the hundred largest firms, the verdict
is averaged over five years, a shortfall of 5 per cent a year counts as complete, and a
completely locked organ wears down 30 per cent of the roadblocks in a year. Feeding the
reserve from capitalist earnings is an addition. The book speaks of foreign currency earned
by governments of countries that export oil and manufactures, and this model has one country
and one currency by default. Part 7 as a whole is an addition. The book says that the organ
is locked in and that its decisions would not differ from business as usual. It does not say
which decisions of government change, and it does not name roadblocks. Judging the fund
against the average of all firms, and not against the index that it follows, is a choice:
the index is the fund itself, and the book names the average as the test in the abstract.

WHAT IS MISSING

The money that the organ receives is not taken from any firm or from wages, because the
ledger holds no taxes, so the organ's income is reported and not paid by anybody. The fund's
buying does not raise the price of shares. In the literature it would, and that rise is hype.
There is one organ and one fund, so funds of different governments cannot be judged against
each other. The fund does not cross a border even when the second country is switched on.
When the module that traces owners is also on, the two modules do not know of each other,
and the fund's stake should be read as a part of what that module calls institutional
holdings. A merger gives the fund a stake in the absorbed firm without payment, as it gives
every owner of the buyer. The organ's reserve is not counted against the government debt that
module 2 reports.
"""
import numpy as np
from core import Scale, Publish, top_positions

ATTRIBUTE = "not_sovereign"     # the part of a firm that the government organ's fund does NOT hold


class SovereignFunds:
    name = "sovereign_funds"
    reads = ()
    supplies = ("sovereign_relief", "sovereign_verdict", "sovereign_part", "sovereign_stake_top",
                "sovereign_dk", "sovereign_rank", "sovereign_reserve", "sovereign_dependence",
                "sovereign_income_from_shares")
    figures = {                   # what the workbench calls each published number: label, unit, note
        "sovereign_relief": ("Wearing down of roadblocks", "index", ""),
        'sovereign_verdict': ('Fund verdict', 'rate', "Growth of the fund's holdings less growth of the average, over the year."),
        'sovereign_part': ("Fund's share of capitalization", 'share', 'The fund as a part of all capitalization.'),
        'sovereign_stake_top': ("Fund's stake in the top 100", 'share', "The fund's part of the top 100."),
        'sovereign_dk': ("Fund's differential capitalization", 'times', "The fund's value divided by the average capitalization of a firm."),
        'sovereign_rank': ("Fund's rank", 'number', 'The rank the fund would have if it were a firm.'),
        'sovereign_reserve': ("Fund's reserve", 'share', 'The reserve as a part of all capitalization.'),
        'sovereign_dependence': ('Dependence on shares', 'share', "Part of the organ's assets held as shares."),
        'sovereign_income_from_shares': ('Income from shares', 'share', "Part of the organ's yearly income that comes from its shares."),
    }

    def __init__(self, levy=0.003, lure=0.10, stake_cap=0.05, index_size=100, judged_over=5,
                 full_shortfall=0.05, relief=0.3):
        self.levy = levy                      # part of all capitalist earnings that the organ's reserve receives each year
        self.lure = lure                      # part of the reserve that the organ moves into shares each year
        self.stake_cap = stake_cap            # the largest part of any one firm that the fund holds. The value is an addition: 5 per cent is the lowest stake Baines and Hager report as giving control over a corporation, and neither they nor the book give it as a limit on the stakes of sovereign funds
        self.index_size = index_size          # the index that the fund follows is this many of the largest firms
        self.judged_over = judged_over        # years over which the verdict is averaged ("a long-term view")
        self.full_shortfall = full_shortfall  # a fund that trails the average by this much a year counts as trailing completely
        self.relief = relief                  # part of the roadblocks that a completely locked, completely trailing organ wears down in a year; 0 makes the module a readout only
        self.reserve = 0.0                    # the organ's money, parked in government bonds
        self.fund_after = 0.0                 # value of the fund after last year's buying and selling
        self.mean_after = 1.0                 # average capitalization of a firm at that time
        self.verdicts = []                    # the yearly verdicts so far

    def start(self, L):
        L.add_attribute(ATTRIBUTE, 1.0, 1.0)      # the fund holds nothing of any firm, old or new, until it buys
        out = {key: 0.0 for key in self.supplies}
        out["sovereign_rank"] = float(len(L) + 1)
        return out

    def propose(self, L, rng):
        K, E = L.cap(), L.earnings()
        held = np.clip(1.0 - L.extra[ATTRIBUTE], 0.0, 1.0)       # the fund's part of each firm
        count = len(L)
        index = top_positions(K, np.arange(count), self.index_size)
        in_index = np.zeros(count, dtype=bool)
        in_index[index] = True
        fund_now, mean_now = float((held * K).sum()), float(K.mean())

        # part 6: the verdict on the year just ended
        verdict = 0.0
        if self.fund_after > 0 and fund_now > 0:
            verdict = float(np.log(fund_now / self.fund_after) - np.log(mean_now / self.mean_after))
            self.verdicts.append(verdict)
        recent = self.verdicts[-self.judged_over:]
        shortfall = max(0.0, -float(np.mean(recent))) if recent else 0.0

        # part 1: the organ's income of the year
        from_shares = float((held * E).sum())
        from_bonds = L.shared["nrr"] * self.reserve
        from_levy = self.levy * float(E.sum())
        income = from_shares + from_bonds + from_levy
        self.reserve += income

        # part 4: the fund sells firms that dropped out of the index
        new = held.copy()
        out_of_index = (held > 0) & ~in_index
        self.reserve += float((held[out_of_index] * K[out_of_index]).sum())
        new[out_of_index] = 0.0

        # parts 2 and 3: the same additional part of every firm in the index, up to the limit
        money = self.lure * self.reserve
        room = np.maximum(self.stake_cap - new[index], 0.0)
        Ki = K[index]
        if money >= (room * Ki).sum():
            added = room
        else:
            low, high = 0.0, self.stake_cap
            for _ in range(60):                   # find the additional part that uses up the money
                mid = 0.5 * (low + high)
                if (np.minimum(mid, room) * Ki).sum() > money:
                    high = mid
                else:
                    low = mid
            added = np.minimum(low, room)
        new[index] += added
        self.reserve -= float((added * Ki).sum())

        self.fund_after, self.mean_after = float((new * K).sum()), mean_now

        # part 7: the lock
        assets = self.fund_after + self.reserve
        dependence = self.fund_after / assets if assets > 0 else 0.0
        pressure = min(1.0, shortfall / self.full_shortfall)
        relief = self.relief * dependence * pressure

        out = {"sovereign_relief": relief,                                       # read by the resistance module
               "sovereign_verdict": verdict,                                     # growth of the fund's holdings less growth of the average, over the year just ended
               "sovereign_part": self.fund_after / float(K.sum()),               # the fund as a part of all capitalization
               "sovereign_stake_top": float((new[index] * Ki).sum() / Ki.sum()), # the fund's part of the hundred largest firms
               "sovereign_dk": self.fund_after / mean_now,                       # the fund's own differential capitalization
               "sovereign_rank": float(1 + (K > self.fund_after).sum()),         # the rank the fund would have if it were a firm
               "sovereign_reserve": self.reserve / float(K.sum()),               # the reserve as a part of all capitalization
               "sovereign_dependence": dependence,                               # part of the organ's assets held as shares
               "sovereign_income_from_shares": from_shares / income if income > 0 else 0.0}
        changes = [Publish(key, float(value), self.name) for key, value in out.items()]
        if (new != held).any():
            changes.append(Scale(ATTRIBUTE, (1.0 - new) / (1.0 - held), self.name))
        return changes
