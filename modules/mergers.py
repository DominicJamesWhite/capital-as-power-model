"""Module 4: mergers and acquisitions (Capital as Power, chapters 14 and 15).

Firms in dominant capital acquire firms they can reach. A firm can reach targets in its own
industry, and targets in its sector and in the rest of the nation to the extent that those
boundaries are open. The volume acquired falls as dominant capital comes to hold most of what
it can reach, so a merger wave inside a closed envelope runs out by itself.

A merger adds employees and earnings and leaves total capitalization unchanged, then lowers
the buyer's risk a little. It also lowers hiring, because money spent on buying is not spent
on building.

Additions to the book: the base rate, the fall in risk, the drag on hiring, and the choice of
targets at random.
"""
import numpy as np
from core import Merge, Publish


class Mergers:
    name = "mergers"
    reads = ()
    supplies = ("merger_volume", "hiring_drag", "pool_open")

    def __init__(self, base_rate=0.15, risk_cut=0.99, drag=2.0, counterforce=1.0, top=100):
        self.base_rate = base_rate    # employees a buyer seeks each year, as a fraction of its own, when targets are plentiful
        self.risk_cut = risk_cut      # the buyer's risk is multiplied by this after a merger
        self.drag = drag              # fall in the hiring rate per unit of merger volume
        self.counterforce = counterforce   # how strongly resistance slows mergers
        self.top = top
        self.max_targets = 200        # the most firms one buyer can absorb in a year

    def start(self, L):
        return {"merger_volume": 0.0, "hiring_drag": 0.0, "pool_open": 1.0}

    def propose(self, L, rng):
        K, n, ind, sec = L.cap(), L.n, L.ind, L.sector
        count = len(L)
        top = np.argsort(K)[::-1][:self.top]
        dominant = np.zeros(count, dtype=bool)
        dominant[top] = True
        open_sector = L.shared.get("perm_sector", 0.0)
        open_nation = L.shared.get("perm_nation", 0.0)
        slow = min(1.0, self.counterforce * L.accounts.get("roadblocks", 0.0))
        hyped = L.accounts.get("merger_hype", 1.0)     # takeover "thrives on investors' hype" (optional module); 1 without it

        n_ind, n_sec = L.sector_of.size, int(L.sector_of.max()) + 1
        appetite = np.broadcast_to(np.asarray(L.accounts.get("merger_appetite", 1.0), dtype=float), n_sec)
        free_i = np.bincount(ind[~dominant], n[~dominant], n_ind)
        held_i = np.bincount(ind[dominant], n[dominant], n_ind)
        free_s = np.bincount(sec[~dominant], n[~dominant], n_sec)
        held_s = np.bincount(sec[dominant], n[dominant], n_sec)
        free_n, held_n = n[~dominant].sum(), n[dominant].sum()

        # Free firms of each industry, in random order, so that a target can be drawn quickly.
        free_pos = rng.permutation(np.flatnonzero(~dominant))
        free_pos = free_pos[np.argsort(ind[free_pos], kind="stable")]
        left = np.bincount(ind[free_pos], minlength=n_ind).astype(float)   # free firms left per industry
        nxt = np.concatenate([[0], np.cumsum(left)[:-1]]).astype(int)      # next free firm per industry

        buyers, targets, acquired = [], [], 0.0
        open_sum = weight_sum = 0.0
        # a barrier that holds the dominant firms of a sector inside their own industry (optional module); 0 without it
        barred = np.broadcast_to(np.asarray(L.accounts.get("line_barrier", 0.0), dtype=float), n_sec)
        open_sector_all, open_nation_all = open_sector, open_nation
        for a in rng.permutation(top):
            i, s = ind[a], sec[a]
            open_sector, open_nation = open_sector_all * (1.0 - barred[s]), open_nation_all * (1.0 - barred[s])
            free = free_i[i] + open_sector * (free_s[s] - free_i[i]) + open_nation * (free_n - free_s[s])
            held = held_i[i] + open_sector * (held_s[s] - held_i[i]) + open_nation * (held_n - held_s[s])
            if free <= 0:
                weight_sum += n[a]
                continue
            open_sum += n[a] * free / (free + held); weight_sum += n[a]
            want = self.base_rate * n[a] * free / (free + held) * (1 - slow)
            want = want * appetite[s]      # a coalition's appetite for buying (optional module); 1 without it
            want = want * hyped
            want = want * (1 - L.accounts.get("eruption_stops_buying", 0.0))   # an eruption suspends the buying of firms (optional module); 0 without it
            reach = np.where(L.sector_of == s, open_sector, open_nation)   # openness toward each industry
            reach[i] = 1.0
            got = 0.0
            for _ in range(self.max_targets):
                w = left * reach
                total = w.sum()
                if got >= want or total <= 0:
                    break
                j = int(np.searchsorted(np.cumsum(w), rng.random() * total, side="right"))
                t = free_pos[nxt[j]]
                if got + n[t] > want and rng.random() > (want - got) / n[t]:
                    break
                nxt[j] += 1; left[j] -= 1
                buyers.append(a); targets.append(t)
                got += n[t]
            acquired += got
        volume = acquired / n.sum()
        changes = [Publish("merger_volume", volume, self.name),
                   Publish("hiring_drag", self.drag * volume, self.name),
                   # the part of dominant capital's reach that it does not yet hold
                   Publish("pool_open", open_sum / weight_sum if weight_sum else 0.0, self.name)]
        if targets:
            changes.append(Merge(np.array(buyers), np.array(targets), self.name, self.risk_cut))
        return changes
