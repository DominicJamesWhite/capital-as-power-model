"""Optional module: a second country behind capital controls.

Sources. Capital as Power (2009), chapter 14, Proposition 5; chapter 15, "Breaking the envelope", the
section "Globalization", and the footnote on South Africa. Nitzan and Bichler, "Going Global:
Differential Accumulation and the Great U-turn in South Africa and Israel" (2001), section 8.
Nitzan and Bichler, The Global Political Economy of Israel (2002), chapters 2, 3, 4 and 6.

What the literature says.
  - A country is a boundary around a set of firms, the last of the "successive social
    'envelopes' - from the industry, to the sector, to the nation-state, to the world as a whole".
  - Capital crossing a border is a change of owner and nothing else: "the only thing that happens
    is a reshuffle of ownership claims, in which foreign capitalists acquire an asset from (or
    sell one to) their domestic counterparts".
  - Under exchange controls in South Africa "large companies were prevented from expanding
    overseas. With capital trapped at home, they gobbled up all available companies in their
    industries before acquiring companies in other sectors and becoming conglomerates".
  - Dominant capital in such a country is measured against its own country: the Israel book
    takes "the five largest corporate groups" and compares them with the country's average.
  - The controls rest on the country's regime, and dominant capital itself has them lifted once
    it has "grown 'too big'" for its own economy: "the only way to continue and accumulate
    differentially is to break the domestic 'envelope'", and "if dominant capital were to expand
    beyond the country's border, capital movement had to be made free".
  - When the border opens, ownership moves both ways. Foreign owners buy local firms, local
    dominant capital buys abroad, and a merger between a firm of a large country and a firm of a
    small country "is likely to be not 'a merger of equals', but a takeover of the latter by
    the former".

Rule.
  1. The firms of a few sectors form the second country. Every firm carries a country number
     (1 for the first country, 2 for the second). A firm founded in an industry of the second
     country belongs to the second country.
  2. This module runs in place of the merger module. It applies the merger module's own rule
     twice: once to the firms of the first country with the first country's settings and its
     hundred largest firms, and once to the firms of the second country with the second
     country's settings and its five largest firms. Neither group can reach the other
     country's firms through this part of the rule.
  3. Inside the second country the boundary between industries opens when the five largest
     firms hold more than a set part of what they can reach, less the country's own roadblocks.
     This is conglomeration. The roadblocks of the second country rise with its own mergers.
  4. The border has a permeability between 0 (full controls) and 1. It starts at 0. It rises
     only after the internal boundary is fully open, and only while the five largest firms
     hold more than the set part of their whole country, less the roadblocks. It also rises
     when the first country's dominant capital has opened its own national boundary fully and
     holds more than the set part of its reach. It falls when roadblocks exceed the pressure by
     a margin.
  5. While the border is partly open, firms change owners across it. The first country's
     hundred largest firms buy small firms of the second country, the second country's five
     largest firms buy small firms of the first country, and each year each of the five
     may be absorbed whole by a larger firm of the first country's hundred. A purchase across
     the border is slowed by the roadblocks of both countries.
  6. The module publishes, for the sabotage module, the part of each industry of the second
     country that its five largest firms hold, and a shift in the strength of labour in the
     second country. It publishes differential capitalization for each country and for both.

Additions. The literature gives no rates and no rule for when controls are lifted. Every number
below is an addition except the count of five. The form of parts 3 to 5 copies the model's own
envelope module, which is itself an addition. All mergers are tagged "mergers", because the core
divides a year's merger gain equally among the tags it finds.

What is missing. The second country has its own firms, its own dominant group, its own merger
settings, its own roadblocks, its own permeability and its own strength of labour. It does not
have its own wage, working population, unemployment, currency, compass, stagflation or popular
resistance: those are still single numbers for both countries. The other modules still pick
their hundred largest firms from both countries together. Employees of a firm bought across
the border are counted in the buyer's industry afterwards, because a firm has one industry.
"""
import numpy as np
from core import Merge, Scale, Publish, readouts
from modules.mergers import Mergers

HOME, SECOND = 1.0, 2.0      # the country numbers carried by each firm


class _View:
    """The firms of one country, presented to the merger rule as if they were a whole ledger."""

    def __init__(self, L, pos, K, shared, accounts):
        self.pos, self.n, self.ind, self._K = pos, L.n[pos], L.ind[pos], K[pos]
        self.sector_of, self.shared, self.accounts = L.sector_of, shared, accounts

    def __len__(self):
        return self.pos.size

    @property
    def sector(self):
        return self.sector_of[self.ind]

    def cap(self):
        return self._K


class SecondCountry:
    name = "second_country"
    replaces = ("mergers",)      # full.py leaves the merger module out; this module applies its rule to each country
    reads = ()
    supplies = ("merger_volume", "hiring_drag", "pool_open",
                "second_country_held", "second_country_labour", "border_open", "second_conglomerate",
                "second_roadblocks", "dk_home", "dk_second", "dk_both")
    figures = {                   # what the workbench calls each published number: label, unit, note
        "merger_volume": ("Merger volume", "rate", "Employees bought in the year in both countries, as a part of all employees."),
        "hiring_drag": ("Cut in hiring caused by mergers", "rate", "Fall in the hiring rate, because money spent on buying is not spent on building."),
        'pool_open': ('Reach not yet held', 'share', "Part of the first country's top 100's reach that it does not yet hold."),
        "border_open": ("Opening of the border", "index", ""),
        'second_conglomerate': ("Second country's internal boundary", 'index', ''),
        "second_roadblocks": ("Roadblocks in the second country", "index", ""),
        "dk_home": ("Differential capitalization, first country", "times", ""),
        "dk_second": ("Differential capitalization, second country", "times", ""),
        "dk_both": ("Differential capitalization, both countries", "times", ""),
    }

    def __init__(self, sectors=2, top=5, base_rate=0.15, risk_cut=0.99, counterforce=1.0,
                 from_mergers=3.0, fade=0.08, threshold=0.5, speed=0.2, close_margin=0.3,
                 start_permeability=0.0, takeover=0.05, labour_shift=0.0, home=None):
        self.sectors = sectors              # how many sectors (the last ones) form the second country
        self.top = top                      # the second country's dominant capital: "the five largest corporate groups" (Israel book)
        self.from_mergers = from_mergers    # rise in the second country's roadblocks per unit of its own merger volume
        self.fade = fade                    # yearly decay of those roadblocks
        self.threshold = threshold          # part of its reach the dominant group must hold before a boundary gives
        self.speed = speed                  # yearly movement of a boundary per unit of net pressure
        self.close_margin = close_margin    # how far roadblocks must exceed pressure to close a boundary
        self.permeability = start_permeability   # how freely firms are bought across the border; 0 is full controls
        self.takeover = takeover            # yearly chance, at a fully open border, that one of the five is absorbed by a larger foreign firm
        self.labour_shift = labour_shift    # added to the unemployment level at which wages keep pace with prices, in the second country only
        self.home = home or Mergers()       # the first country's merger settings
        # the second country's own merger settings: yearly appetite, fall in risk after a merger, effect of roadblocks
        self.local = Mergers(base_rate=base_rate, risk_cut=risk_cut, counterforce=counterforce, top=top)
        self.conglomerate = 0.0             # openness of the boundary between industries inside the second country
        self.roadblocks = 0.0               # the second country's own counterforce to mergers
        self.bought_in = self.bought_out = 0.0   # employees acquired across the border so far, inward and outward

    def industries(self, L):
        """True for each industry that lies in the second country."""
        last = int(L.sector_of.max())
        return L.sector_of > last - self.sectors

    def start(self, L):
        second = self.industries(L)
        L.add_attribute("country", np.where(second[L.ind], SECOND, HOME), HOME)
        out = dict(self.home.start(L))
        out.update(second_country_held=np.zeros(second.size), second_country_labour=self.labour_shift * second,
                   border_open=self.permeability, second_conglomerate=0.0, second_roadblocks=0.0)
        return out

    @staticmethod
    def _buy(buyers, wants, pool, n, rng, most):
        """Each buyer takes firms from the pool, in random order, up to the employees it wants."""
        b_out, t_out, k, acquired = [], [], 0, 0.0
        pool = rng.permutation(pool)
        for j in rng.permutation(len(buyers)):
            got = 0.0
            for _ in range(most):
                if got >= wants[j] or k >= pool.size:
                    break
                t = pool[k]
                if got + n[t] > wants[j] and rng.random() > (wants[j] - got) / n[t]:
                    break
                k += 1
                b_out.append(buyers[j]); t_out.append(t)
                got += n[t]
            acquired += got
        return b_out, t_out, acquired

    def propose(self, L, rng):
        K, n, A = L.cap(), L.n, L.accounts
        ind_second = self.industries(L)
        second = ind_second[L.ind]
        home_pos, sec_pos = np.flatnonzero(~second), np.flatnonzero(second)
        changes = []

        # part 1: a firm founded last year in an industry of the second country takes its country number
        wrong = second & (L.extra["country"] < 1.5)
        if wrong.any():
            changes.append(Scale("country", np.where(wrong, SECOND / HOME, 1.0), self.name))

        p, c = self.permeability, self.conglomerate
        top1 = home_pos[np.argsort(K[home_pos])[::-1][:self.home.top]]
        top2 = sec_pos[np.argsort(K[sec_pos])[::-1][:self.top]]

        # part 5, first half: "a takeover of the latter by the former"
        cross_b, cross_t, absorbed_n = [], [], 0.0
        if p > 0:
            for t in top2:
                larger = top1[K[top1] > K[t]]
                if rng.random() < p * self.takeover and larger.size:
                    cross_b.append(int(rng.choice(larger))); cross_t.append(int(t))
                    absorbed_n += n[t]
        gone = np.zeros(len(L), dtype=bool)
        gone[cross_t] = True

        # part 2: the merger rule, once for each country
        def apply(rule, pos, shared, accounts):
            view = _View(L, pos, K, shared, accounts)
            published, b, t = {}, np.zeros(0, int), np.zeros(0, int)
            for ch in rule.propose(view, rng):
                if isinstance(ch, Publish):
                    published[ch.key] = ch.value
                elif isinstance(ch, Merge):
                    b, t = pos[ch.buyers], pos[ch.targets]
            return published, b, t

        pub1, b1, t1 = apply(self.home, home_pos, L.shared, A)
        own = dict(A)
        own["roadblocks"] = self.roadblocks
        stay = sec_pos[~gone[sec_pos]]
        pub2, b2, t2 = {}, np.zeros(0, int), np.zeros(0, int)
        if stay.size:                                    # nothing to do once every firm of the country has been bought
            pub2, b2, t2 = apply(self.local, stay, {"perm_sector": c, "perm_nation": c}, own)
        if t1.size:
            changes.append(Merge(b1, t1, "mergers", self.home.risk_cut))
        if t2.size:
            changes.append(Merge(b2, t2, "mergers", self.local.risk_cut))

        # part 5, second half: small firms change owners across the border
        n_home, n_second = n[home_pos].sum(), n[sec_pos].sum()
        inward = outward = 0.0
        # the cross-border ownership module (optional) takes over these purchases and moves no employees; 0 without it
        if p > 0 and sec_pos.size and not A.get("cross_border_on", 0.0):
            taken = gone.copy()
            taken[t1] = True; taken[t2] = True; taken[top1] = True; taken[top2] = True
            free1, free2 = home_pos[~taken[home_pos]], sec_pos[~taken[sec_pos]]
            mood = A.get("merger_hype", 1.0) * (1 - A.get("eruption_stops_buying", 0.0))   # as in the merger module; 1 without those modules
            # a purchase across the border meets the roadblocks of both countries
            mood = mood * (1 - min(1.0, self.home.counterforce * A.get("roadblocks", 0.0)))
            mood = mood * (1 - min(1.0, self.local.counterforce * self.roadblocks))
            want1 = self.home.base_rate * n[top1] * p * n[free2].sum() / n_second * mood
            b, t, inward = self._buy(top1, want1, free2, n, rng, self.home.max_targets)
            cross_b += [int(x) for x in b]; cross_t += [int(x) for x in t]
            buyers2 = top2[~gone[top2]]
            want2 = self.local.base_rate * n[buyers2] * p * n[free1].sum() / n_home * mood
            ob, ot, outward = self._buy(buyers2, want2, free1, n, rng, self.local.max_targets)
            if ot:
                changes.append(Merge(np.array(ob), np.array(ot), "mergers", self.local.risk_cut))
        if cross_t:
            changes.append(Merge(np.array(cross_b), np.array(cross_t), "mergers", self.home.risk_cut))
        inward += absorbed_n
        # employees whose firms changed owners across the border without a merger (optional module); 0 without it
        inward += A.get("cross_border_inward", 0.0) * n.sum()
        outward += A.get("cross_border_outward", 0.0) * n.sum()
        self.bought_in += inward
        self.bought_out += outward

        # parts 3 and 4: the second country's roadblocks, its internal boundary and its border
        within = pub2.get("merger_volume", 0.0) * n[stay].sum()     # employees acquired inside the second country
        self.roadblocks = float(np.clip(self.roadblocks + self.from_mergers * (within + inward) / max(n_second, 1e-12)
                                        - self.fade * self.roadblocks, 0.0, 1.0))
        inside = 1.0 - pub2.get("pool_open", 1.0)        # the part of its reach that the second country's dominant group holds
        outside = 1.0 - pub1.get("pool_open", 1.0)       # the same for the first country's dominant capital
        push_in = inside - self.threshold - self.roadblocks
        push_out = outside - self.threshold - self.roadblocks if L.shared.get("perm_nation", 0.0) >= 1.0 else 0.0
        if push_in > 0 and c < 1.0:                      # the nearest closed boundary gives way first: conglomeration
            self.conglomerate = min(1.0, c + self.speed * push_in)
        elif max(push_in, push_out) > 0:                 # then the border
            self.permeability = min(1.0, p + self.speed * max(push_in, push_out))
        elif self.roadblocks - inside > self.close_margin:   # the counterforce wins: the border closes first
            back = self.speed * (self.roadblocks - inside - self.close_margin)
            if p > 0:
                self.permeability = max(0.0, p - back)
            else:
                self.conglomerate = max(0.0, c - back)

        # what the other modules read
        total = n.sum()
        volume = (pub1.get("merger_volume", 0.0) * n_home + within + inward + outward) / total
        k = ind_second.size
        dominant2 = np.zeros(len(L), dtype=bool)
        dominant2[top2] = True
        n_ind = np.maximum(np.bincount(L.ind, n, k), 1e-12)
        held = np.where(ind_second, np.bincount(L.ind[dominant2], n[dominant2], k) / n_ind, 0.0)
        r1 = readouts(L, self.home.top, mask=~second)
        empty = {"dk": 0.0, "top_share_employees": 0.0, "depth": 0.0, "firms": 0}
        r2 = readouts(L, self.top, mask=second) if sec_pos.size else empty
        both = readouts(L, self.home.top)
        for key, value in (
                ("merger_volume", volume),
                ("hiring_drag", self.home.drag * volume),
                ("pool_open", pub1.get("pool_open", 0.0)),            # the first country's pool: its envelope module moves its boundaries
                ("second_country_held", held),                        # the sabotage module holds these industries toward the target markup
                ("second_country_labour", self.labour_shift * ind_second),
                ("border_open", self.permeability),
                ("second_conglomerate", self.conglomerate),
                ("second_roadblocks", self.roadblocks),
                ("second_pool_open", pub2.get("pool_open", 1.0)),
                ("second_merger_volume", within / max(n_second, 1e-12)),
                ("bought_inward", self.bought_in / total),            # employees acquired across the border so far, as a part of all employees
                ("bought_outward", self.bought_out / total),
                ("dk_home", r1["dk"]), ("dk_second", r2["dk"]), ("dk_both", both["dk"]),
                ("second_top_share", r2["top_share_employees"]),      # the five's part of their country's employees
                ("home_top_share", r1["top_share_employees"]),
                ("second_depth", r2["depth"]), ("home_depth", r1["depth"]),
                ("second_firms", r2["firms"]),
                ("second_part_of_employees", n_second / total)):
            changes.append(Publish(key, value, self.name))
        return changes
