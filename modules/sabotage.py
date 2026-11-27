"""Module 1: business-as-usual sabotage (Capital as Power, chapter 12).

Sabotage works through price. A claim's price is its cost plus a markup, and its earnings
per employee are the markup times the wage. The core works the price out from the wage and the
markup (see "How the price is worked out" in modules.md), so a movement of the markup under
this rule is a movement of the price against the wage, and the module proposes no price. Nobody steers the economy. Each industry follows its
own conditions, and unemployment and the capitalist share of income are totals that come out.

The rule has five parts, each tied to a passage of the book (see modules.md):
  1. Earnings come from a markup.
  2. Where an industry is not concentrated, growth of capacity beyond the growth of the
     working population wears the markup down (sellers undercut each other).
  3. Small claims expand while the markup is above the normal level and cut back below it.
  4. Where dominant capital holds an industry, entry is barred and the markup is held toward
     a target. Raising the markup costs the dominant claims some volume.
  5. Unemployment weakens wages against prices, which raises markups everywhere.

Every rate below is an addition to the book.
"""
import numpy as np
from core import ScaleComponent, Publish, top_positions, BASE


class Sabotage:
    name = "sabotage"
    reads = ("unemployment", "industry_growth")
    supplies = ("hire_small", "hire_dominant", "entry_open")

    def __init__(self, normal_markup=0.10, target_markup=0.30, erosion=1.0, response=0.5,
                 hold=0.1, wage_weakness=0.2, labour_holds_at=0.05, volume_cost=0.5,
                 floor=0.005, top=100):
        self.normal_markup = normal_markup    # the markup at which small claims neither expand nor cut back
        self.target_markup = target_markup    # the markup dominant capital holds an industry toward
        self.erosion = erosion                # fall in the markup per unit of capacity growth beyond the pack (part 2)
        self.response = response              # extra hiring by small claims per unit of markup above normal (part 3)
        self.hold = hold                      # yearly speed at which a fully held industry approaches the target (part 4)
        self.volume_cost = volume_cost        # employment given up by dominant claims per unit of price rise (part 4)
        self.wage_weakness = wage_weakness    # rise in every markup per unit of unemployment above the level below (part 5)
        self.labour_holds_at = labour_holds_at  # unemployment at which wages keep pace with prices: the strength of labour
        self.floor = floor                    # a markup cannot fall below this
        self.resistance_shift = 0.05          # rise in that level of unemployment at full resistance
        self.top = top

    def industry_state(self, L):
        """Employees, share held by dominant capital, and markup, for each industry."""
        k = L.sector_of.size
        dominant = np.zeros(len(L), dtype=bool)
        dominant[top_positions(L.cap(), np.arange(len(L)), self.top)] = True
        n = np.bincount(L.ind, L.n, k)
        held = np.bincount(L.ind[dominant], L.n[dominant], k)
        earnings = np.bincount(L.ind, L.markup_earnings(), k)   # earnings from the markup alone: interest and other income are left out
        safe = np.maximum(n, 1e-12)
        markup = np.where(n > 0, earnings / (L.shared["wage"] * safe), self.normal_markup)
        held = held / safe
        held = np.maximum(held, L.accounts.get("second_country_held", 0.0))   # the part held by a second country's own dominant group (optional module); 0 without it
        held = np.minimum(1.0, held + L.accounts.get("foreign_held", 0.0))   # the part owned by dominant capital across a border (optional module); 0 without it
        return n, held, markup

    def hiring(self, L, held, markup, held_rise):
        g = L.shared["workforce_growth"]
        # the normal markup moves with the normal rate of return (optional module); the number is 1 without it
        excess = markup - self.normal_markup * L.accounts.get("policy_rate_markup", 1.0)
        unbarred = L.accounts.get("protection_open", 1.0)   # part of each industry not under a protection (optional module); 1 without it
        unbarred = unbarred * L.accounts.get("nature_open", 1.0)   # part of each industry that owners of nature leave open (optional module); 1 without it
        small = g + self.response * excess * np.where(excess > 0, (1 - held) * unbarred, 1.0)   # entry barred where held
        n = np.bincount(L.ind, L.n, L.sector_of.size)
        pack = (small * n * (1 - held)).sum() / max((n * (1 - held)).sum(), 1e-12)
        dominant = min(g, pack) - self.volume_cost * held_rise / (1 + markup)
        return small, dominant

    def start(self, L):
        # This module owns the base markup. The base is a level: the markup a claim would have if no
        # gain or loss made by another rule stood on top of it. It stacks.
        L.add_component(BASE, self.name)
        n, held, markup = self.industry_state(L)
        small, dominant = self.hiring(L, held, markup, np.zeros_like(markup))
        return {"hire_small": small, "hire_dominant": dominant, "entry_open": 1 - held,
                "industry_growth": np.full(markup.size, L.shared["workforce_growth"])}

    def propose(self, L, rng):
        n, held, markup = self.industry_state(L)
        g, u = L.shared["workforce_growth"], L.accounts["unemployment"]
        growth = L.accounts["industry_growth"]
        # Resistance strengthens labour: wages then keep pace with prices at a higher level of unemployment.
        # The strength of organised labour in each industry (optional module) takes the place of popular resistance here.
        labour = L.accounts.get("labour_strength_by_industry", L.accounts.get("resistance", 0.0))
        holds_at = self.labour_holds_at + self.resistance_shift * labour
        holds_at = holds_at + L.accounts.get("second_country_labour", 0.0)       # a second country's own strength of labour (optional module); 0 without it
        wages = self.wage_weakness * (u - holds_at)                               # part 5
        wages = wages + L.accounts.get("currency_markup", 0.0)                    # a devaluation raises prices against wages (optional currencies module); 0 without it
        undercut = -(1 - held) * self.erosion * (growth - g)                     # part 2
        grip = 1 - min(1.0, L.accounts.get("resistance", 0.0))                    # coordination weakens under resistance
        grip = grip * (1 - L.accounts.get("eruption_frees_markups", 0.0))         # an eruption suspends the hold (optional module); 0 without it
        held_rise = held * self.hold * (self.target_markup * grip + self.normal_markup * (1 - grip) - markup)   # part 4
        new = np.maximum(markup + wages + undercut + held_rise, self.floor)
        small, dominant = self.hiring(L, held, new, np.maximum(held_rise, 0.0))
        # The rule moves the markup of the industry as a whole. The change is proposed to the base
        # markup of every claim in the industry, in proportion. At the end of the year the core sets
        # the movement against what stands in the other stacking components of each claim: a fall
        # first takes away standing gains (such as a lead from price rises), and a rise first
        # restores standing losses (such as what was given up for unsold goods). Only the rest
        # stays in the base. See Model._net in core.py and "What a stacking component holds" in
        # modules.md. No claim's markup is changed by that reckoning.
        return [ScaleComponent(BASE, (new / markup)[L.ind], self.name),   # the price follows: the core works it out
                Publish("hire_small", small, self.name),
                Publish("hire_dominant", dominant, self.name),
                Publish("entry_open", 1 - held, self.name)]
