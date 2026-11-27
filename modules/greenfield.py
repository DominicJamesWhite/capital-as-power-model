"""Module 3: green-field growth (Capital as Power, chapters 14 and 15).

Claims hire at the rates that the sabotage module supplies for their industry: one rate for
dominant claims and one for the rest. Part of the hiring by small claims goes to newly founded
claims, each much smaller than the average, and less of it where entry to the industry is
barred. The average size of a claim therefore falls as the economy grows.

A new claim is staffed out of the year's new employment of the small claims of its industry and
takes nobody from an existing claim. It starts with the part of its industry's markup that stacks
and with no premium or other income that it does not hold.

Additions to the book: the part of new employment that goes to new claims, their size, and the
markup at which a new claim starts.
"""
import numpy as np
from core import Scale, Found, Set, Publish, top_positions


class Greenfield:
    name = "greenfield"
    reads = ("hire_small", "hire_dominant", "entry_open")
    supplies = ("new_hires", "industry_growth")

    def __init__(self, new_claim_share=0.35, new_claim_size=0.15, floor=0.005, top=100):
        self.new_claim_share = new_claim_share   # part of small claims' new employment that goes to new claims
        self.new_claim_size = new_claim_size     # size of a new claim, as a fraction of the average claim
        self.floor = floor                       # unemployment cannot fall below this
        self.top = top
        self.founded = 0      # new claims founded so far in this run
        self.withheld = 0     # new claims that the rounding asked for and the year's hiring could not staff

    def start(self, L):
        return {"new_hires": 0.0}

    def propose(self, L, rng):
        k, ind, n = L.sector_of.size, L.ind, L.n
        employed = n.sum()
        workforce = L.shared["workforce"] * (1 + L.shared["workforce_growth"])
        workforce = workforce + L.accounts.get("public_workforce_change", 0.0)   # people entering from, or leaving for, publicly run employment (optional module); 0 without it
        dominant = np.zeros(len(L), dtype=bool)
        dominant[top_positions(L.cap(), np.arange(len(L)), self.top)] = True
        A = L.accounts
        rate = np.where(dominant, A["hire_dominant"][ind], A["hire_small"][ind])
        rate = rate - A.get("crisis", 0.0)                       # stagflation's cut in hiring: the crisis
        rate = rate - np.where(dominant, A.get("sales_cut", 0.0), 0.0)   # dismissals for want of sales (optional module)
        jobs = rate * n
        up = jobs > 0
        jobs[up] *= 1 - min(1.0, A.get("hiring_drag", 0.0))      # money spent on buying is not spent on building
        room = workforce * (1 - self.floor) - employed - jobs[~up].sum()
        room = room - A.get("force_hires", 0.0)                  # military hiring planned for this year (optional module)
        room = room - A.get("privatisation_jobs", 0.0)           # privatised employees arrive with their jobs (optional module); 0 without it
        if jobs[up].sum() > room:                                # hiring cannot exceed the working population
            jobs[up] *= max(room, 0.0) / jobs[up].sum()

        # part of small claims' hiring founds new claims, less where entry is barred
        entry = A["entry_open"] * A.get("protection_open", 1.0)   # protections bar entry too (optional module); 1 without it
        entry = entry * A.get("nature_open", 1.0)                 # owners of nature bar entry too (optional module); 1 without it
        to_new = np.where(up & ~dominant, jobs * self.new_claim_share * entry[ind], 0.0)
        size = self.new_claim_size * employed / len(L)
        wanted = np.bincount(ind, to_new, k) / size
        count = np.floor(wanted + rng.random(k)).astype(int)
        # The people who staff a new claim are people whom the small claims of its industry would
        # otherwise have hired this year: small firms grow "in number (through the birth of new
        # firms) as well as in size (by hiring more workers)" (chapter 15, "Running with the pack").
        # A birth is part of the year's new employment and takes nobody from an existing claim. So an
        # industry cannot found more claims in a year than its small claims' new employment can
        # staff. Without this, the rounding above could found a claim in an industry whose small
        # claims hired less than one new claim employs, and take the difference out of those claims.
        hiring = np.bincount(ind, np.where(up & ~dominant, jobs, 0.0), k)
        staffed = np.floor(hiring / size).astype(int)
        self.withheld += int(np.maximum(count - staffed, 0).sum())   # a count kept for reports; nothing reads it
        count = np.minimum(count, staffed)
        self.founded += int(count.sum())
        founded = count * size
        given = np.bincount(ind, to_new, k)
        back = np.where(given > 0, founded / np.maximum(given, 1e-12), 0.0)   # rounding returns the remainder
        kept = jobs - to_new * back[ind]

        changes = [Set("workforce", workforce, self.name),
                   Publish("new_hires", float(jobs.sum()), self.name),
                   Publish("industry_growth", np.bincount(ind, jobs, k) / np.maximum(np.bincount(ind, n, k), 1e-12),
                           self.name),
                   Scale("employees", 1 + kept / n, self.name)]
        if count.sum():
            n_j = np.maximum(np.bincount(ind, n, k), 1e-12)
            EH = L.earnings() * L.h
            where = np.repeat(np.arange(k), count)
            total = int(count.sum())
            # A new claim starts with the part of its industry's markup that stacks, averaged over
            # the industry's employees. It takes no part of a premium that rests on a hold on buyers
            # (a protection, a size premium, a hold on wants) and no other income, because it holds
            # none of these. The module hands the core the earnings per employee that this markup
            # gives at the wage of the start of the year, and the core places them in the new
            # claim's base markup. Every other component of the new claim takes its starting value.
            # As before, the figure is an amount of money fixed at the start of the year: in a year
            # when the wage rises, the new claim's markup is lower by the rise (backlog item 42).
            # The core works out the new claim's price from the wage and that markup, so no price
            # is handed over. A new claim starts with no named cost of any module.
            stacking = n * (L.shared["wage"] * L.stacking_markup())   # earnings from the stacking part of the markup
            changes.append(Found(
                employees=np.full(total, size),
                epe=(np.bincount(ind, stacking, k) / n_j)[where],
                hype=np.ones(total),
                risk=np.full(total, EH.sum() / (EH / L.d).sum()),      # the average risk
                industry=where, source=self.name))
        return changes
