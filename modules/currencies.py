"""Module 37: currencies and devaluation.

THE RULE IN PLAIN WORDS

A border runs through the ledger, around the last few sectors, as in the second_country and
cross_border modules. This module gives the second country a currency of its own. The first
country's currency is the unit in which everything is counted, as the United States dollar is
in the literature. The module holds one number: the value of the second country's currency in
units of the first. With two countries there is only one such number, and a fall of one
currency is a rise of the other. The number starts at 1.

  1. The currency moves only as owners enter and leave. Each year the module takes the
     employees of the firms that owners of the first country bought in the second country,
     less those they sold back, and subtracts the same figure for the second country's owners
     in the first country. It divides the result by the employees of the second country. The
     currency rises by a set multiple of that number when it is positive and falls when it is
     negative. Nothing else moves the currency.
  2. Each year the module measures earnings per employee in each country and in both together,
     with the second country's earnings counted in the first country's currency. It takes the
     yearly growth of each over the last few years. The shortfall of a country is the growth of
     the two together less the growth of that country, when that is positive.
  3. Foreign owners liquidate where earnings growth falls short. Each foreign-owned firm in a
     country is sold back to local owners with an added yearly chance equal to a set multiple
     of that country's shortfall, up to a limit. The cross_border module carries out the sales,
     because it keeps the record of who owns what. While owners are leaving a country they buy
     less there.
  4. A fallen currency makes firms cheap for owners who hold the other currency. The employees
     that a dominant group seeks across the border are multiplied by a power of the other
     currency's cheapness, up to a limit.
  5. A fall of the currency raises prices against wages in the country whose currency fell,
     and it does the opposite, weakly, in the other country. The sabotage module adds a set
     multiple of the year's fall to the markup of every industry of the country whose currency
     fell, weighted by the other country's part of all employees, and takes the mirror amount
     from the markups of the other country, weighted by the first country's part.
  6. The module publishes the value of the currency, its yearly change, the two shortfalls, the
     two added chances of sale, and three readouts counted in the first country's currency: the
     differential capitalization of the hundred largest firms of both countries, the second
     country's part of all capitalization, and the year's gain or loss on foreign holdings in
     the second country as a part of the capitalization of the first country's hundred.

The module itself returns no change to any firm. It acts only through three numbers that the
cross_border module reads and one that the sabotage module reads, all one year late. Without
the cross_border module (or a second_country module whose border has opened) no owner crosses
the border, the currency stays at 1, and a run is identical to a run without this module.

WHAT IT RESTS ON

  - Capital as Power (2009), chapter 17, "The retreat of breadth". "The rapid breadth
    expansion, particularly in the emerging markets of Asia, created a massive build-up of
    excess capacity and loosened the grip of business sabotage. Green-field investment in the
    1990s grew in leaps and bounds - much faster than world consumption and with disastrous
    consequences for profit margins. The implications for differential accumulation were not
    lost on absentee investors, who began liquidating their holdings in peripheral regions
    where earnings growth fell short of the world average (Nitzan 1997; 1998a). The first
    victim was the Mexican peso circa 1994, followed in 1997 by the Thai baht and the rest of
    the Asian currencies. From there the centrifugal forces of excessive external breadth
    spread devaluation throughout the developing world". Parts 1, 2 and 3 give this passage a
    form: the test is earnings growth against the world average, the act is liquidation by
    absentee owners, and the fall of the currency follows the act.
  - Chapter 15, "Globalization". "The only thing that happens is a reshuffle of ownership
    claims, in which foreign capitalists acquire an asset from (or sell one to) their domestic
    counterparts." Entering and leaving are therefore changes of owner and nothing else.
  - Chapter 9. "What previously required military conquest can now be done through currency
    devaluation". Part 4 rests on this sentence and on the next source.
  - Jonathan Nitzan, "Asian Equities: Not for the Fainthearted" (The BCA Emerging Markets
    Strategist, February 1998).
    Holdings are counted in the owners' currency: "With the Asian asset class having lost over
    50% in US$ terms since June 1997, the short-term upside for investors is significant".
    Earnings are compared with the world: Asian "earnings per share" are set "relative to the
    world benchmark", and "since 1996, Asian earnings per share were actually falling against
    a rising world trend". The paper's index of sentiment shows "how much more or less
    investors are willing to pay for 1 US$ of Asian earnings relative to 1 US$ of world
    earnings". On what devaluation does inside the country: "a combination of mass layoffs,
    wage reductions and rising prices of basic necessities". On what it does to other
    countries: "devaluation cannot be a solution for all countries: it solves the problem in
    one country only by passing it to others". Parts 2, 4 and 5 rest on these sentences.
  - Nitzan and Bichler, The Global Political Economy of Israel (2002), chapter 4. Before the
    1983 crash "investors, who expected an imminent exchange rate correction, naturally sold
    their stocks to buy dollars". The plan that followed "followed the standard IMF template
    of devaluation, tight monetary and fiscal policy and, of course, a significant wage
    erosion". Parts 1 and 5 rest on these.

WHAT IS ADDED

The literature says who sells, where, and that the currency then falls. It gives no rule and
no rate for any of this. Every number below is an addition. Measuring "earnings growth" as
earnings per employee over three years is an addition; the 1998 paper uses earnings per share.
Making the currency move in proportion to the net change of owners is an addition. The whole
of part 4 is an addition in form: the 1998 paper calls the fall "a short-term buying
opportunity" and warns against it in the same breath. Part 5 gives a form to "wage reductions
and rising prices"; the weights by each country's part of all employees stand for how much
each country buys from the other, which the model does not hold. Applying part 5 to a rise of
the currency as well as to a fall is an addition.

WHAT IS MISSING

There are two countries and so one exchange rate; the spread of devaluation from one
peripheral country to the next, which chapter 17 describes, needs at least three. Debt does not
cross the border, so the 1998 paper's point that a fallen currency makes foreign debt heavier
cannot be shown. The paper says the "risk premium is now much higher" after the fall; this
module does not change any firm's risk. It says "social unrest" follows; the model has one
number for popular resistance in both countries, and this module does not raise it. No
government organ defends the currency, and there are no reserves and no interest-rate spread.
The ledger's own capitalization is not converted: only the three published readouts are
counted in the first country's currency. Flows are counted in employees, because that is what
the cross_border module publishes.
"""
import numpy as np
from core import Publish, top_positions


class Currencies:
    name = "currencies"
    reads = ()
    supplies = ("currency_second", "currency_change", "currency_inflow",
                "currency_shortfall_second", "currency_shortfall_home",
                "currency_flight_1", "currency_flight_2", "currency_buying_1", "currency_buying_2",
                "currency_markup", "currency_dk_common", "currency_second_cap_part",
                "currency_holding_gain")
    figures = {                   # what the workbench calls each published number: label, unit, note
        "currency_second": ("Value of the second currency", "number", "In units of the first currency. It starts at 1."),
        "currency_change": ("Change in the second currency", "rate", "Yearly change, on a log scale."),
        "currency_inflow": ("Net inflow of owners", "number", "Net buying into the second country, divided by its employees."),
        "currency_shortfall_second": ("Earnings shortfall, second country", "rate", "Growth of both countries together less growth of the second, when positive."),
        "currency_shortfall_home": ("Earnings shortfall, first country", "rate", "Growth of both countries together less growth of the first, when positive."),
        'currency_flight_1': ("Added chance of sale, first country's owners", 'share', ''),
        'currency_flight_2': ("Added chance of sale, second country's owners", 'share', ''),
        'currency_buying_1': ("Buying factor, first country's owners", 'times', ''),
        'currency_buying_2': ("Buying factor, second country's owners", 'times', ''),
        'currency_dk_common': ('Differential capitalization in one currency', 'times', "Top 100 of both countries, counted in the first country's currency."),
        'currency_second_cap_part': ("Second country's share of capitalization", 'share', "Counted in the first country's currency."),
        'currency_holding_gain': ('Gain on foreign holdings', 'rate', "The year's gain or loss on holdings in the second country, as a part of the first country's top 100 capitalization."),
    }

    def __init__(self, sectors=2, sensitivity=2.0, max_move=0.5, window=3, flight_rate=10.0,
                 max_flight=0.5, cheapness=1.0, max_buying=3.0, pass_through=0.1, top=100):
        self.sectors = sectors            # how many sectors (the last ones) lie in the second country; must match the second_country and cross_border modules
        self.sensitivity = sensitivity    # proportional rise of the currency when owners from abroad buy firms holding 1 per cent of the country's employees, per 1 per cent (part 1)
        self.max_move = max_move          # the largest change of the currency in one year, as a change of its logarithm
        self.window = window              # years over which earnings growth is measured (part 2)
        self.flight_rate = flight_rate    # added yearly chance that a foreign-owned firm is sold, per unit of shortfall in yearly earnings growth (part 3)
        self.max_flight = max_flight      # the largest added yearly chance of sale
        self.cheapness = cheapness        # how strongly a cheap currency raises buying from abroad: buying is multiplied by the cheapness to this power (part 4)
        self.max_buying = max_buying      # the largest multiple by which a cheap currency can raise buying
        self.pass_through = pass_through  # rise in the markup of a country per unit of fall of its currency, when the other country is nearly all of the world (part 5)
        self.top = top                    # dominant capital: the hundred largest firms, as in the book
        self.value = 1.0                  # value of the second country's currency in units of the first
        self.levels = []                  # past earnings per employee (logarithms): second country, first country, both, in the first country's currency
        self.last_bought = (0.0, 0.0)     # the second_country module's running totals, used only when cross_border is off

    def industries(self, L):
        """True for each industry that lies in the second country."""
        last = int(L.sector_of.max())
        return L.sector_of > last - self.sectors

    def start(self, L):
        out = {key: 0.0 for key in self.supplies}
        out.update(currency_second=1.0, currency_buying_1=1.0, currency_buying_2=1.0,
                   currency_markup=np.zeros(L.sector_of.size), currency_second_cap_part=0.0,
                   currency_dk_common=0.0)
        return out

    def propose(self, L, rng):
        A, n, E, K = L.accounts, L.n, L.earnings(), L.cap()
        ind_second = self.industries(L)
        second = ind_second[L.ind]
        n2, n1 = float(n[second].sum()), float(n[~second].sum())
        total = n1 + n2
        part2 = n2 / total
        x = self.value                                   # the currency at the start of the year

        # part 2: earnings per employee and its growth, counted in the first country's currency
        tiny = 1e-300
        E2, E1 = float(E[second].sum()) * x, float(E[~second].sum())
        self.levels.append((np.log(max(E2, tiny) / max(n2, tiny)), np.log(max(E1, tiny) / max(n1, tiny)),
                            np.log(max(E1 + E2, tiny) / total)))
        back = min(self.window, len(self.levels) - 1)
        short2 = short1 = 0.0
        if back > 0 and n2 > 0:
            g2, g1, g_all = [(now - then) / back for now, then in zip(self.levels[-1], self.levels[-1 - back])]
            short2, short1 = max(0.0, g_all - g2), max(0.0, g_all - g1)

        # part 3: the added chance that a foreign-owned firm is sold. Group 1 (the first country's
        # owners) holds firms in the second country, and group 2 holds firms in the first.
        flight1 = min(self.max_flight, self.flight_rate * short2)
        flight2 = min(self.max_flight, self.flight_rate * short1)

        # part 4: a cheap currency raises buying from abroad; owners who are leaving buy less
        buying1 = min(self.max_buying, x ** -self.cheapness) * (1.0 - flight1 / self.max_flight)
        buying2 = min(self.max_buying, x ** self.cheapness) * (1.0 - flight2 / self.max_flight)

        # part 1: owners who entered and left during the last year, in employees as a part of all employees
        if A.get("cross_border_on", 0.0):
            into_second, into_home = float(A.get("cb_flow_from_home", 0.0)), float(A.get("cb_flow_from_second", 0.0))
        else:                                            # the second_country module's own purchases; 0 without it
            now = (float(A.get("bought_inward", 0.0)), float(A.get("bought_outward", 0.0)))
            into_second, into_home = now[0] - self.last_bought[0], now[1] - self.last_bought[1]
            self.last_bought = now
        inflow = (into_second - into_home) / part2 if part2 > 0 else 0.0
        move = float(np.clip(self.sensitivity * inflow, -self.max_move, self.max_move))
        self.value = x * float(np.exp(move))

        # part 5: a fall of the currency raises markups at home and lowers them, weakly, abroad
        markup = np.where(ind_second, -self.pass_through * move * (1.0 - part2),
                          self.pass_through * move * part2)

        # part 6: readouts counted in the first country's currency, at the start of the year
        Kc = np.where(second, K * x, K)
        top = top_positions(Kc, np.arange(len(L)), self.top)
        dk_common = float(Kc[top].mean() / Kc.mean())
        cap_part = float(Kc[second].sum() / Kc.sum())
        gain = 0.0
        if "owned_abroad" in L.extra:                    # the cross_border module's record of ownership
            held = second & (L.extra["owned_abroad"] > 1.5)
            home_pos = np.flatnonzero(~second)
            home_top = top_positions(K, home_pos, self.top)
            gain = float((np.exp(move) - 1.0) * Kc[held].sum() / K[home_top].sum())

        out = dict(currency_second=self.value, currency_change=move, currency_inflow=inflow,
                   currency_shortfall_second=short2, currency_shortfall_home=short1,
                   currency_flight_1=flight1, currency_flight_2=flight2,
                   currency_buying_1=buying1, currency_buying_2=buying2,
                   currency_markup=markup, currency_dk_common=dk_common,
                   currency_second_cap_part=cap_part, currency_holding_gain=gain)
        return [Publish(key, value, self.name) for key, value in out.items()]
