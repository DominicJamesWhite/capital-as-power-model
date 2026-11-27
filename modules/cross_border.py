"""Optional module: cross-border ownership.

THE RULE IN PLAIN WORDS

A border runs through the ledger: the industries of the last few sectors lie in a second
country, as in the second_country module. This module lets ownership cross that border and
moves nothing else. Every firm carries one more number, which says whether the firm is owned
in the country where it sits (1) or by the dominant capital of the other country (2). A
purchase across the border changes that number from 1 to 2. The firm keeps its employees, its
industry, its price and its earnings per employee. No firm is merged and no employee moves.

  1. Each year the dominant group of each country (the hundred largest firms of the first
     country, the five largest of the second) seeks firms across the border. The employees
     it seeks are a set fraction of its own employees, times the openness of the border, times
     the part of the other country that is still locally owned and outside that country's own
     dominant group. Targets are drawn at random from those firms.
  2. The openness of the border is the number `border_open` when the second_country module
     supplies it. Without that module nothing in the model raises capital controls, and the
     border is taken to be open. In both cases buying is slowed by the roadblocks of both
     countries, and it follows the mood of the merger module (hype and eruptions) when those
     optional modules are on.
  3. Foreign owners also sell back. Each year each foreign-owned firm returns to local owners
     with a chance that is a set rate times one minus the openness of part 2, which counts the
     border, the roadblocks and the mood for mergers together. A
     foreign-owned firm that a local buyer absorbs in a merger also returns to local owners,
     because core.py leaves the buyer's ownership in place for the whole merged firm.
  4. Only dominant capital buys across the border, so all foreign earnings belong to the two
     dominant groups. The module does not add those earnings to any single firm. It reports
     them, and it reports differential capitalization for each dominant group twice: without
     its holdings abroad, and with them.
  5. A foreign-owned firm is a part of dominant capital inside the industry where it sits. The
     sabotage module therefore counts the foreign-owned part of each industry as held by
     dominant capital: entry is barred there and the markup is held toward the target.
  6. The module reports the flow each way in employees. The flow from a country is what its
     dominant group bought across the border less what it sold back or lost to local buyers.
     The gross flow is the sum of the two flows. The net flow is their difference. Both are
     given as a part of all employees and as a ratio to new hiring, which is this model's
     stand-in for green-field investment. The module also reports the foreign-owned share of
     all capitalization and of each country's capitalization.

With the second_country module on, this module takes over that module's purchases of small
firms across the border, which were mergers that carried the employees into the buyer's
country. The second_country module reads two numbers from this module so that its roadblocks
still rise with foreign purchases. It still handles the takeover of one of the five by a
larger foreign firm.

WHAT IT RESTS ON

  - Capital as Power (2009), chapter 15, "Globalization". "By definition, capital mobility is a
    purely pecuniary process. Usually, the only thing that happens is a reshuffle of ownership
    claims, in which foreign capitalists acquire an asset from (or sell one to) their domestic
    counterparts." "There is no cross-border flow of machines, structures, vehicles, technical
    know-how, or employees." "When ownership crosses a border, it alters the organization and
    institutions of power on both sides of that border." The ownership number, and the fact
    that nothing else moves, rest on this. Part 3 rests on "or sell one to".
  - Chapter 15, "Global production or global ownership?". "The key issue, therefore, is not the
    location of factories and employees, but of the capitalists." Between 1990 and 2006 "the
    global proportion of foreign-owned assets has nearly tripled, from 9 per cent to 26 per
    cent", and that of corporate stocks rose "from 9 to 27 per cent". The readout
    cb_foreign_share can be set against these figures.
  - Chapter 15, "Net or gross?". "Capitalist integration and globalization can move both ways,
    which means that the proper measure to use here is the gross flow - that is, the sum of
    inflow and outflow." "The net and gross magnitudes are the same when capital goes only in
    one direction". Flows are expressed "as a per cent of the G7's gross fixed capital
    formation", and "by 2007 the value of gross flows reached 82 per cent of green-field
    investment, compared to only 16 per cent" for net flows. "Even if the movement of capital
    indeed ebbs and flows, over time the impact it has on the level of capital stocks tends to
    be cumulative". Part 6 follows these definitions.
  - Chapter 15, "Foreign investment and differential accumulation". "Whereas exports augment
    the profits of small as well as large firms, the bulk of foreign earnings go to the largest
    corporations." "Free investment tends mostly to raise" differential accumulation. "Over 75
    per cent of all foreign direct investment takes the form of cross-border mergers and
    acquisitions." Capital mobility became "a 'necessity', mandated by the combination of
    excess capacity and the cumulative build-up of giant firms". Part 4 rests on the first
    sentence, and part 1 makes the buying grow with the size of the dominant group.
  - Chapter 15, "Capital flow and the creorder of global power". Foreign investment "consists
    of nothing more than the creation or alteration of legal entitlements", whose magnitude
    "is equal to the present value of their expected future earnings. And since the level and
    pattern of these earnings reflect the control of business over industry, it follows that
    cross-border flow of capital reflects the restructuring not of global production, but of
    global capitalist power". The share of foreign operations in United States corporate
    profit reached "one third of the total in recent years" (Figure 15.6). Part 5 rests on the
    second sentence, and the readout cb_foreign_earnings_home can be set against the third.
  - Nitzan and Bichler, The Global Political Economy of Israel (2002), chapter 6, on the
    report that invited foreign owners in: "there was complete silence on what would prevent
    foreign owners from cooperating with their domestic counterparts". Part 5 also rests on
    this.
  - Bichler and Nitzan, "New Imperialism or New Capitalism?" (2006). Foreign assets were 20 per
    cent of world output in 1900, "a mere 5%" in 1945 and 92 per cent in 2000. Chapter 15 says
    of the fall that "instability, depression, wars and capital controls hampered the movement
    of capital". Parts 2 and 3 give that fall a form.

WHAT IS ADDED

The literature gives definitions and directions and no rule or rate for cross-border buying.
Every number below is an addition. The form of part 1 copies the second_country module, which
is itself an addition. Giving all foreign earnings to dominant capital is stronger than the
book's "the bulk". Part 3 is an addition: the book says assets are sold back and that foreign
holdings fell in the first half of the twentieth century, and it gives no rule. Part 5 is an
addition: the literature says foreign ownership changes power on both sides of the border and
does not say how markups respond. Counting flows in employees is an addition that follows the
way this model already measures mergers against new hiring.

WHAT IS MISSING

A firm is owned wholly at home or wholly abroad, so portfolio holdings of a part of a firm
are not shown. Foreign earnings are not credited to any single firm, so the ledger's own
differential capitalization does not include them; only the published readouts do. A direct
credit is not made, because the cost-cutting module pulls each firm's
earnings per employee back toward its industry and would erase it. The merger modules do not
know about ownership: a local dominant firm can absorb a foreign-owned firm like any other.
The flow counted for such absorptions is the number of firms lost times their present average
size, and it is reported a year late. Debt does not cross the border. There is one currency.
Without the second_country module the border has no controls behind it and no second set of
settings, and the module then shows only what a change of owners does by itself.
"""
import numpy as np
from core import Scale, Publish

ATTRIBUTE = "owned_abroad"      # 1 when a firm is owned in the country where it sits, 2 when the other country's dominant capital owns it
LOCAL, ABROAD = 1.0, 2.0


class CrossBorder:
    name = "cross_border"
    reads = ()
    supplies = ("cross_border_on", "cross_border_inward", "cross_border_outward", "foreign_held",
                "cb_gross_flow", "cb_net_flow", "cb_gross_to_hiring", "cb_net_to_hiring",
                "cb_flow_from_home", "cb_flow_from_second",
                "cb_foreign_share", "cb_foreign_share_home", "cb_foreign_share_second",
                "cb_foreign_earnings_home", "cb_foreign_earnings_second",
                "cb_foreign_earnings_top_home", "cb_foreign_earnings_top_second",
                "cb_dk_home", "cb_dk_home_with_foreign", "cb_dk_second", "cb_dk_second_with_foreign",
                "cb_open")
    figures = {                   # what the workbench calls each published number: label, unit, note
        "cross_border_on": ("Cross-border buying on", "number", "1 while the module is on."),
        "cross_border_inward": ("Buying into the second country", "rate", "Employees of second-country firms bought by foreign owners, as a part of all employees."),
        'cross_border_outward': ('Buying into the first country', 'rate', "Employees of first-country firms bought by the second country's owners, as a part of all employees."),
        "cb_gross_flow": ("Gross flow across the border", "rate", "As a part of all employees."),
        "cb_net_flow": ("Net flow across the border", "rate", "As a part of all employees."),
        "cb_gross_to_hiring": ("Gross flow against hiring", "times", "Gross flow divided by new hires."),
        "cb_net_to_hiring": ("Net flow against hiring", "times", "Net flow divided by new hires."),
        "cb_flow_from_home": ("Net buying by the first country", "rate", "Bought less sold, as a part of all employees."),
        "cb_flow_from_second": ("Net buying by the second country", "rate", "Bought less sold, as a part of all employees."),
        "cb_foreign_share": ("Foreign-owned capitalization", "share", "Part of all capitalization owned abroad."),
        'cb_foreign_share_home': ('Foreign-owned, first country', 'share', "Part of the first country's capitalization owned abroad."),
        'cb_foreign_share_second': ('Foreign-owned, second country', 'share', "Part of the second country's capitalization owned abroad."),
        'cb_foreign_earnings_home': ('Foreign earnings, first country', 'share', "Foreign earnings as a part of all earnings of the first country's owners."),
        'cb_foreign_earnings_second': ('Foreign earnings, second country', 'share', "Foreign earnings as a part of all earnings of the second country's owners."),
        'cb_foreign_earnings_top_home': ('Foreign earnings of the top group, first country', 'share', "The same for the first country's dominant group alone."),
        'cb_foreign_earnings_top_second': ('Foreign earnings of the top group, second country', 'share', "The same for the second country's dominant group alone."),
        "cb_dk_home": ("Differential capitalization, first country", "times", ""),
        "cb_dk_home_with_foreign": ("Differential capitalization with foreign holdings, first country", "times", ""),
        "cb_dk_second": ("Differential capitalization, second country", "times", ""),
        "cb_dk_second_with_foreign": ("Differential capitalization with foreign holdings, second country", "times", ""),
        "cb_open": ("Openness of the border", "index", ""),
    }

    def __init__(self, sectors=2, top_home=100, top_second=5, rate=0.02, retreat=0.05,
                 counterforce=1.0, open_alone=1.0):
        self.sectors = sectors            # how many sectors (the last ones) lie in the second country; must match the second_country module
        self.top_home = top_home          # the first country's dominant capital: its hundred largest firms, as in the book
        self.top_second = top_second      # the second country's dominant capital: its five largest firms, as in the second_country module
        self.rate = rate                  # employees a dominant group seeks across the border each year, as a fraction of its own, at an open border with everything still to buy
        self.retreat = retreat            # yearly chance that a foreign-owned firm is sold back to local owners when the border is fully shut
        self.counterforce = counterforce  # how strongly roadblocks slow buying across the border, as in the merger module
        self.open_alone = open_alone      # openness of the border when no second_country module supplies it
        self.expected = None              # foreign-owned firms each group should hold at the next start of year, if none is absorbed

    def industries(self, L):
        """True for each industry that lies in the second country."""
        last = int(L.sector_of.max())
        return L.sector_of > last - self.sectors

    def start(self, L):
        L.add_attribute(ATTRIBUTE, LOCAL, LOCAL)     # every firm, old or new, begins in the hands of owners of its own country
        out = {key: 0.0 for key in self.supplies}
        out["cross_border_on"] = 1.0
        out["foreign_held"] = np.zeros(L.sector_of.size)
        out["cb_open"] = float(L.accounts.get("border_open", self.open_alone))
        return out

    def propose(self, L, rng):
        K, E, n, A = L.cap(), L.earnings(), L.n, L.accounts
        in_second = self.industries(L)[L.ind]          # where each firm sits
        abroad = L.extra[ATTRIBUTE] > 1.5              # whether the other country's dominant capital owns it
        total = n.sum()

        # part 2: how open the border is this year
        p = float(A.get("border_open", self.open_alone))
        slow = (1 - min(1.0, self.counterforce * A.get("roadblocks", 0.0)))
        slow = slow * (1 - min(1.0, self.counterforce * A.get("second_roadblocks", 0.0)))
        mood = float(A.get("merger_hype", 1.0)) * (1 - A.get("eruption_stops_buying", 0.0))
        openness = float(np.clip(p * slow * mood, 0.0, 1.0))

        # the two countries: where their firms sit, their dominant groups, and what each group owns abroad
        sits = {1: ~in_second, 2: in_second}
        tops, owned = {}, {}
        for c, most in (1, self.top_home), (2, self.top_second):
            cand = np.flatnonzero(sits[c] & ~abroad)
            tops[c] = cand[np.argsort(K[cand])[::-1][:most]]
            owned[c] = np.flatnonzero(sits[3 - c] & abroad)
        dominant = np.zeros(len(L), dtype=bool)
        dominant[tops[1]] = True
        dominant[tops[2]] = True

        factor = np.ones(len(L))
        flow, bought_n = {}, {}
        expected = {}
        for c in (1, 2):
            other = 3 - c
            # firms this group held abroad last year that are no longer there: absorbed by local buyers
            lost = 0.0
            if self.expected is not None and owned[c].size:
                lost = max(0, self.expected[c] - owned[c].size) * float(n[owned[c]].mean())
            # part 1: purchases across the border
            pool = np.flatnonzero(sits[other] & ~abroad & ~dominant)
            n_other = n[sits[other]].sum()
            want = self.rate * n[tops[c]].sum() * openness * (n[pool].sum() / n_other if n_other > 0 else 0.0)
            want = want * A.get("currency_buying_%d" % c, 1.0)     # a cheap currency raises buying, flight lowers it (optional currencies module); 1 without it
            pool = rng.permutation(pool)
            run = np.cumsum(n[pool])
            k = int(np.searchsorted(run, want, side="right"))      # firms that fit whole within what is sought
            if k < pool.size:                                      # the next one is bought with a chance equal to the part that fits
                left = want - (run[k - 1] if k else 0.0)
                if rng.random() < left / n[pool[k]]:
                    k += 1
            buy = pool[:k]
            factor[buy] = ABROAD / LOCAL
            # part 3: sales back to local owners
            # owners liquidate where earnings growth falls short of the world average (optional currencies module); 0 without it
            sell = owned[c][rng.random(owned[c].size) < self.retreat * (1.0 - openness) + A.get("currency_flight_%d" % c, 0.0)]
            factor[sell] = LOCAL / ABROAD
            bought_n[c] = float(n[buy].sum())
            flow[c] = bought_n[c] - float(n[sell].sum()) - lost
            expected[c] = owned[c].size + buy.size - sell.size
        self.expected = expected

        # part 6: flows, in employees
        gross = abs(flow[1]) + abs(flow[2])
        net = abs(flow[1] - flow[2])
        hires = float(A.get("new_hires", 0.0))

        # parts 4 and 6: stocks, foreign earnings and differential capitalization, at the start of the year
        def part(a, b):
            return float(a / b) if b > 0 else 0.0

        out = {}
        for c, label in (1, "home"), (2, "second"):
            mine = np.flatnonzero(sits[c] & ~abroad)             # firms of this country that its own owners hold
            t, f = tops[c], owned[c]
            out["cb_foreign_share_" + label] = part(K[sits[c] & abroad].sum(), K[sits[c]].sum())   # part of this country's capitalization owned abroad
            out["cb_foreign_earnings_" + label] = part(E[f].sum(), E[mine].sum() + E[f].sum())      # foreign earnings as a part of all earnings of this country's owners
            out["cb_foreign_earnings_top_" + label] = part(E[f].sum(), E[t].sum() + E[f].sum())     # the same for its dominant group alone
            average = K[mine].sum() / max(mine.size, 1)
            average_with = (K[mine].sum() + K[f].sum()) / max(mine.size, 1)
            out["cb_dk_" + label] = part(K[t].sum() / max(t.size, 1), average)
            out["cb_dk_" + label + "_with_foreign"] = part((K[t].sum() + K[f].sum()) / max(t.size, 1), average_with)
        k_ind = L.sector_of.size
        n_ind = np.maximum(np.bincount(L.ind, n, k_ind), 1e-12)
        out.update(
            cross_border_on=1.0,
            cross_border_inward=bought_n[1] / total,       # employees whose firms foreign owners bought in the second country, as a part of all employees
            cross_border_outward=bought_n[2] / total,      # the same for firms the second country's five bought in the first country
            foreign_held=np.bincount(L.ind[abroad], n[abroad], k_ind) / n_ind,   # part 5: the foreign-owned part of each industry
            cb_flow_from_home=flow[1] / total, cb_flow_from_second=flow[2] / total,
            cb_gross_flow=gross / total, cb_net_flow=net / total,
            cb_gross_to_hiring=part(gross, hires), cb_net_to_hiring=part(net, hires),
            cb_foreign_share=part(K[abroad].sum(), K.sum()),
            cb_open=openness)

        changes = [Publish(key, value, self.name) for key, value in out.items()]
        if (factor != 1.0).any():
            changes.append(Scale(ATTRIBUTE, factor, self.name))
        return changes
