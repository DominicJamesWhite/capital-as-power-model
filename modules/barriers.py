"""Module 25: specific barriers won by resistance.

THE RULE IN PLAIN WORDS

Without this module the model holds one number for all roadblocks against mergers. This module turns that
number into barriers against particular groups. A barrier here is a prohibition that holds the
dominant firms of one sector inside their own line of business. The line of business of a
firm is its industry. The module keeps one barrier for each sector, a number between 0 and 1.

  1. The record of what was bought. The ledger does not say what a firm bought across which
     boundary. The module therefore keeps its own estimate. It gives every firm a number, so
     that it can see which firms disappeared in the last year. Every firm that disappeared
     was bought, because nothing else in the model removes a firm. The module does not know
     which buyer took which firm. It divides the employees of the firms that disappeared
     from each industry among last year's dominant firms, in proportion to the chance that
     each of them was the buyer under the rule of the merger module. For each firm that has
     been dominant, the module keeps the part of its employees that it bought in each
     industry other than its own. These parts are the firm's outside holdings.
  2. What raises a barrier. The counter-force is the level of roadblocks plus a part of the
     level of popular resistance, and never more than 1. The exposure of a sector is the
     outside holdings of the dominant firms seated in it, as a part of all employees in the
     economy, divided by a setting, and never more than 1. Each year the barrier of a sector
     rises by a rate, times the counter-force, times the exposure. The barrier therefore
     rises fastest against the groups that hold most outside their own lines. A sector whose
     dominant firms never left their own industries gets no barrier.
  3. What a barrier does to buying. The merger module multiplies the openness of the sector
     boundary and of the national boundary, as a buyer seated in the sector sees them, by one
     minus the barrier. Buying inside the buyer's own industry is not touched.
  4. Forced sales. While the barrier of a sector stands above a threshold, each dominant firm
     seated in the sector must sell a fixed part of each of its outside holdings every year.
     When that part would be smaller than the average small firm, the whole holding is
     sold. A holding that is itself smaller than the average small firm is not sold. Each
     sold holding becomes a new firm in the industry where it was bought. The new firm
     takes the seller's earnings per employee, price, hype and risk, so the sale changes who
     holds the employees and does not change total capitalization. The new firms are free
     to be bought again by dominant firms that are under no barrier.
  5. What wears a barrier down. Each year a barrier falls by a rate, times its own height,
     times the push of dominant capital on its boundaries. The push is the number that the
     boundary contest module publishes. Without that module it is the part of its reach that
     dominant capital already holds, which the envelope module publishes as pressure. A
     barrier does not fade by itself.
  6. The bargain. Forced sales are counted as a part of the employees of dominant capital. A
     running level of these sales, multiplied by a rate and never more than 1, is published
     as the bargain. The boundary contest module lowers its hold on the next boundary in that
     proportion. The envelope module does not read the bargain.
  7. Readouts. The module publishes the barrier of each sector, the average barrier as
     dominant capital meets it, the highest barrier, the lowest barrier among sectors that
     have a dominant firm, the number of sectors under forced sale, the part of dominant
     capital's employees in outside holdings, the year's forced sales as a part of all
     employees, and the bargain.

Nothing comes from outside. Roadblocks rise with the volume of mergers, popular resistance
rises with inflation and unemployment, and the push comes from the depletion of targets.

WHAT IT RESTS ON

  - Capital as Power (2009), chapter 15, "Three transformations". Amalgamation "is restricted
    by the ability of broader state institutions to quickly accommodate the new corporate
    formations", and "as amalgamation builds up momentum, it also generates higher and higher
    roadblocks, contradictions and counter-forces". Part 2 rests on this: the barrier grows
    out of the roadblocks that mergers themselves raise.
  - The footnote to that sentence. "The 1933 Glass-Steagall Act, for instance, barred US banks
    from making industrial investments, a prohibition that only recently has been relaxed.
    Similar transformational effects were brought on by the post-war dismantling of the
    Japanese Zaibatsu, by the 1990s unbundling of South African holding groups and the
    divestment of Israeli banks of their 'non-financial' holdings". Part 3 is the bar of the
    first sentence. Part 4 is the dismantling, unbundling and divestment of the second. The
    words "only recently has been relaxed" are the ground for part 5.
  - Bichler and Nitzan, "Regimes of Differential Accumulation" (2001), conclusion. "The more
    immediate barrier on further global amalgamation will likely be regulatory or financial.
    In many sectors global amalgamation is approaching 'antitrust thresholds' as they are now
    called, and in some of them ... it has already triggered regulatory intervention." The
    barrier is specific to a sector, and it is triggered by how far amalgamation has gone
    there. This is the ground for the exposure in part 2.
  - Nitzan and Bichler, "Going Global: Differential Accumulation and the Great U-turn in South
    Africa and Israel" (2001). Mergers are "inherently limited
    ... by societal and technological barriers on corporate concentration". In the new South
    Africa, "dominant capital accepts the need to unbundle its oligopolistic 'stranglehold'
    over the economy (selling parts of it to black entrepreneurs, including the unions) in
    return for gradual capital decontrols and the ability to diversify abroad". Anglo
    American "began to disentangle its complicated cross-ownership ties, divesting some of
    its holdings". The pact was made with the African National Congress and the unions. This
    is the ground for letting popular resistance add to the counter-force in part 2, for the
    new firms of part 4, and for the bargain of part 6.
  - Bichler and Nitzan, The Global Political Economy of Israel (2002), chapter 6, on the Brodet
    Report of 1995. The banks were to "reduce their holdings in any 'real' company to 20 per
    cent or less". "The great octopus of domestic assets had to be first chopped down into
    vendible units." The committee "said nothing on how to prevent the divested companies
    from being re-amalgamated into different groupings", and its solutions "could be easily
    circumvented". "The real purpose of the report was never to lower concentration, but to
    change its nature." Part 4 leaves the sold firms free to be bought again for this reason.
  - Capital as Power, chapter 15, "Breaking the envelope". "Amalgamation is simply too
    important to give up." The same section says that the de-conglomeration of the global
    wave "is bound to become exhausted, pushing dominant capital back toward conglomeration".
    Part 5 rests on these: the push that opens boundaries also wears barriers down.
  - Chapter 13 treats corporations and government organs as bodies of one mode of power. A
    barrier is therefore not an act of a government set against business. It is the form
    that a counter-force takes inside the same order, and dominant capital wears it down
    from inside the same order.

WHAT IS ADDED

The literature names the barriers, says that amalgamation generates them, and says that they
were relaxed or circumvented. It gives no rule for which group a barrier falls on, how fast it
rises, or how it is worn down, and it gives no rates. The form of every part is an addition,
and every number below is an addition. Three choices need saying. First, the book says that
the population is "impartial to breadth", and the rule nevertheless lets popular resistance
add to the counter-force, on the ground of the South African pact. The setting for this can be
put to zero. Second, the footnote speaks of banks and of holding groups, and the rule applies
one barrier to all the dominant firms seated in a sector. Third, the estimate in part 1 is a
reckoning of chances and not a record.

WHAT IS MISSING

A barrier bars the firms seated in a sector from buying outside their industry. It does not
bar outsiders from buying into the sector, although the separation of banking from industry
worked in both directions. The dismantling of the Zaibatsu was carried out by an occupying
power, and the rule has no place for one. The Brodet Report made room for foreign buyers, and
the model has one country. The sold firms are not handed to particular new owners. A firm
that was once dominant and is later bought loses its record, and its outside holdings are then
counted as part of its own industry.
"""
import numpy as np
from core import Scale, Found, Publish, top_positions
from modules.capacity import PLANT

ID = "barrier_firm_number"     # the added per-firm number that lets the module see which firms disappeared


class Barriers:
    name = "barriers"
    reads = ("pressure", "roadblocks", "resistance")
    supplies = ("line_barrier", "barrier_bargain", "barrier_level", "barrier_highest", "barrier_lowest", "barrier_sectors_selling",
                "barrier_outside_part", "barrier_sales")
    figures = {                   # what the workbench calls each published number: label, unit, note
        "barrier_bargain": ("Bargain", "index", "A running level of forced sales, times a rate."),
        "barrier_level": ("Average barrier", "index", "Average barrier as the top 100 meet it."),
        "barrier_highest": ("Highest barrier", "index", ""),
        "barrier_lowest": ("Lowest barrier", "index", "Lowest barrier among sectors that have a top 100 firm."),
        "barrier_sectors_selling": ("Sectors under forced sale", "number", ""),
        'barrier_outside_part': ('Top 100 employees in outside holdings', 'share', "Part of the top 100's employees in outside holdings."),
        'barrier_sales': ('Forced sales', 'rate', "The year's forced sales as a part of all employees."),
    }

    def __init__(self, raise_rate=0.3, full_exposure=0.01, popular_part=0.5, wear_rate=0.05, sell_above=0.5,
                 sell_part=0.25, bargain_rate=1.0, bargain_keep=0.8, top=100):
        self.raise_rate = raise_rate      # yearly rise of a barrier at full counter-force and full exposure
        self.full_exposure = full_exposure   # a sector's exposure is complete when the outside holdings of its dominant firms reach this part of all employees
        self.popular_part = popular_part  # how much of popular resistance counts toward the counter-force beside roadblocks; 0 leaves roadblocks alone
        self.wear_rate = wear_rate        # part of a barrier that dominant capital wears away in a year at full push
        self.sell_above = sell_above      # height of a barrier above which the sector's dominant firms must sell outside holdings
        self.sell_part = sell_part        # part of each outside line sold in a year of forced sale
        self.bargain_rate = bargain_rate  # fall in the hold on the next boundary per unit of forced sales, as a part of dominant capital's employees
        self.bargain_keep = bargain_keep  # part of the running level of forced sales that carries over to the next year
        self.top = top
        self.barrier = None               # one barrier per sector
        self.outside = {}                 # firm number -> the part of the firm's employees bought in each other industry
        self.sold_level = 0.0             # running level of forced sales, as a part of dominant capital's employees
        self.next_number = 1
        self.prev = None                  # last year's firms and the chances that each dominant firm was a buyer

    # ------------------------------------------------------------------ start

    def start(self, L):
        L.add_attribute(ID, np.arange(1, len(L) + 1, dtype=float), -1.0)   # a new firm carries -1 until it is numbered
        self.next_number = len(L) + 1
        n_sec = int(L.sector_of.max()) + 1
        self.barrier = np.zeros(n_sec)
        return {"line_barrier": self.barrier.copy(), "barrier_bargain": 0.0, "barrier_level": 0.0,
                "barrier_highest": 0.0, "barrier_lowest": 0.0, "barrier_sectors_selling": 0.0, "barrier_outside_part": 0.0,
                "barrier_sales": 0.0}

    # ------------------------------------------------------------------ part 1: who probably bought what

    def buyer_chances(self, L, top, dominant):
        """For each dominant firm and each industry, a weight in proportion to the employees the
        firm is expected to buy there this year, following the rule of the merger module."""
        n, ind, sec = L.n, L.ind, L.sector
        n_ind, n_sec = L.sector_of.size, int(L.sector_of.max()) + 1
        A = L.accounts
        barred = np.broadcast_to(np.asarray(A.get("line_barrier", 0.0), dtype=float), n_sec)   # the value the merger module uses this year
        appetite = np.broadcast_to(np.asarray(A.get("merger_appetite", 1.0), dtype=float), n_sec)
        open_sector, open_nation = L.shared.get("perm_sector", 0.0), L.shared.get("perm_nation", 0.0)
        free_i = np.bincount(ind[~dominant], n[~dominant], n_ind)
        held_i = np.bincount(ind[dominant], n[dominant], n_ind)
        free_s = np.bincount(sec[~dominant], n[~dominant], n_sec)
        held_s = np.bincount(sec[dominant], n[dominant], n_sec)
        free_n, held_n = n[~dominant].sum(), n[dominant].sum()
        left = np.bincount(ind[~dominant], minlength=n_ind).astype(float)       # free firms per industry
        i, s = ind[top], sec[top]
        o_s, o_n = open_sector * (1 - barred[s]), open_nation * (1 - barred[s])
        free = free_i[i] + o_s * (free_s[s] - free_i[i]) + o_n * (free_n - free_s[s])
        held = held_i[i] + o_s * (held_s[s] - held_i[i]) + o_n * (held_n - held_s[s])
        want = np.where(free > 0, n[top] * free / np.maximum(free + held, 1e-300), 0.0) * appetite[s]
        reach = np.where(L.sector_of[None, :] == s[:, None], o_s[:, None], o_n[:, None])
        reach[np.arange(top.size), i] = 1.0
        draw = left[None, :] * reach
        total = draw.sum(axis=1)
        return np.where(total[:, None] > 0, want[:, None] * reach / np.maximum(total, 1e-300)[:, None], 0.0)

    def update_record(self, L, numbers):
        """Divide last year's disappeared firms among last year's dominant firms."""
        P = self.prev
        if P is None:
            return
        where = np.full(self.next_number, -1, dtype=np.int64)
        where[numbers.astype(np.int64)] = np.arange(len(L))
        gone = where[P["numbers"]] < 0
        if not gone.any():
            return
        n_ind = L.sector_of.size
        vanished = np.bincount(P["ind"][gone], P["n"][gone], n_ind)             # employees bought, by industry
        col = P["chances"].sum(axis=0)
        gains = P["chances"] / np.where(col > 0, col, 1.0) * vanished           # buyer by industry
        for row, number in enumerate(P["top_numbers"]):
            pos = where[number]
            got = gains[row]
            if pos < 0 or got.sum() <= 0:
                continue
            outside_gain = got.copy()
            outside_gain[P["top_ind"][row]] = 0.0                               # buying in the home industry is not an outside holding
            before = max(L.n[pos] - got.sum(), 0.0)                             # the firm's employees before this year's buying
            old = self.outside.get(number)
            if old is None and outside_gain.sum() <= 0:
                continue
            old = np.zeros(n_ind) if old is None else old
            new = (old * before + outside_gain) / (before + got.sum())
            if new.sum() > 1.0:
                new /= new.sum()
            self.outside[number] = new

    # ------------------------------------------------------------------ the yearly step

    def propose(self, L, rng):
        A = L.accounts
        count, n_ind, n_sec = len(L), L.sector_of.size, int(L.sector_of.max()) + 1
        changes = []

        # Number the firms that were founded last year.
        numbers = L.extra[ID].copy()
        fresh = np.flatnonzero(numbers < 0)
        if fresh.size:
            given = self.next_number + np.arange(fresh.size, dtype=float)
            numbers[fresh] = given
            factor = np.ones(count)
            factor[fresh] = -given                                             # -1 times -number gives the number
            changes.append(Scale(ID, factor, self.name))
            self.next_number += fresh.size

        self.update_record(L, numbers)                                          # part 1

        top = top_positions(L.cap(), np.arange(count), self.top)
        dominant = np.zeros(count, dtype=bool)
        dominant[top] = True
        sec_top, n_top = L.sector[top], L.n[top]
        held = n_top.sum()
        out_part = np.array([self.outside[k].sum() if k in self.outside else 0.0 for k in numbers[top]])

        # Part 4: forced sales, under the barrier in force at the start of the year.
        in_force = self.barrier
        factor = np.ones(count)
        new_n, new_ind, new_from = [], [], []
        smallest = L.n[~dominant].mean() if (~dominant).any() else 0.0          # a sold holding below the size of an average small firm stays where it is
        for pos, number, s in zip(top, numbers[top], sec_top):
            if in_force[s] <= self.sell_above or number not in self.outside:
                continue
            parts = self.outside[number]
            sold_total = 0.0
            for j in np.argsort(parts)[::-1]:                                  # largest outside line first
                if parts[j] * L.n[pos] < smallest or parts[j] <= 0 or sold_total + parts[j] > 0.9:
                    break                                                      # too small to make a firm (or the firm would sell itself away)
                sold = self.sell_part * parts[j]
                if sold * L.n[pos] < smallest:
                    sold = parts[j]                                            # a small holding is sold whole
                new_n.append(sold * L.n[pos]); new_ind.append(j); new_from.append(pos)
                parts[j] -= sold
                sold_total += sold
            if sold_total > 0:
                factor[pos] = 1 - sold_total
                self.outside[number] = parts / (1 - sold_total)
        sales = float(np.sum(new_n))
        if new_n:
            src = np.array(new_from)
            changes.append(Scale("employees", factor, self.name))
            # a holding that is sold keeps every component of the firm that sold it: markup, other income
            # and named costs. Its price is therefore the seller's, and the core works it out.
            # With the capacity module on, the holding takes its part of the seller's plant: a forced sale
            # moves plant from one owner to another and builds none.
            extra = None
            if PLANT in L.extra:
                changes.append(Scale(PLANT, factor, self.name))
                extra = {PLANT: L.extra[PLANT][src] * np.array(new_n) / L.n[src]}
            changes.append(Found(np.array(new_n), None, L.h[src].copy(), L.d[src].copy(),
                                 np.array(new_ind, dtype=int), self.name, extra=extra,
                                 components=L.components_of(src)))

        # Part 2: the counter-force and each sector's exposure raise its barrier.
        counter = min(1.0, A["roadblocks"] + self.popular_part * A["resistance"])
        held_s = np.bincount(sec_top, n_top, n_sec)
        out_s = np.bincount(sec_top, n_top * out_part, n_sec)
        exposure = np.minimum(1.0, out_s / (self.full_exposure * L.n.sum()))
        # Part 5: the push of dominant capital wears every barrier down.
        push = float(np.clip(A.get("boundary_push", A["pressure"]), 0.0, 1.0))
        self.barrier = np.clip(self.barrier + self.raise_rate * counter * exposure
                               - self.wear_rate * push * self.barrier, 0.0, 1.0)

        # Part 6: the bargain.
        self.sold_level = self.bargain_keep * self.sold_level + (sales / held if held > 0 else 0.0)
        bargain = float(min(1.0, self.bargain_rate * self.sold_level))

        # Remember this year's firms and chances for next year's reckoning.
        self.prev = {"numbers": numbers.astype(np.int64), "n": L.n.copy(), "ind": L.ind.copy(),
                     "top_numbers": numbers[top].astype(np.int64), "top_ind": L.ind[top].copy(),
                     "chances": self.buyer_chances(L, top, dominant)}

        # Part 7: readouts.
        out = {"line_barrier": self.barrier.copy(),
               "barrier_bargain": bargain,
               "barrier_level": float((self.barrier * held_s).sum() / held) if held > 0 else 0.0,
               "barrier_highest": float(self.barrier.max()),
               "barrier_lowest": float(self.barrier[held_s > 0].min()) if held > 0 else 0.0,
               "barrier_sectors_selling": float((self.barrier > self.sell_above).sum()),
               "barrier_outside_part": float((n_top * out_part).sum() / held) if held > 0 else 0.0,
               "barrier_sales": sales / L.n.sum()}
        return changes + [Publish(k, v, self.name) for k, v in out.items()]
