"""Module 1: business-as-usual sabotage (Capital as Power, chapter 12).

Sabotage works through price. A firm's price is its cost plus a markup, and its earnings
per employee are the markup times the wage. The core works the price out from the wage and the
markup (see "How the price is worked out" in modules.md), so a movement of the markup under
this rule is a movement of the price against the wage, and the module proposes no price. Nobody steers the economy. Each industry follows its
own conditions, and unemployment and the capitalist share of income are totals that come out.

The rule has five parts, each tied to a passage of the book (see modules.md):
  1. Earnings come from a markup.
  2. Where an industry is not concentrated, growth of capacity beyond the growth of the
     working population wears the markup down (sellers undercut each other). The growth
     counted is the hiring that firms set out to do, so the markup also wears down when
     firms seek more people than there are and bid against each other for them.
  3. Small firms expand while the markup is above the normal level and cut back below it.
  4. Where dominant capital holds an industry, entry is barred and the markup is held toward
     a target. Raising the markup costs the dominant firms some volume.
  5. Unemployment weakens wages against prices. Each level of unemployment has a level of the
     capitalist share of income that goes with it, and markups move toward that level over
     some years. The delay comes from the authors' measurement for the United States ("Can
     Capitalists Afford Recovery?", 2014: the share follows unemployment three years earlier).
     Both slopes come from one fit to the United States national accounts in the form of this
     rule: above the unemployment at which wages keep pace with prices the level rises 0.75 for
     each point of unemployment, close to the authors' own 0.8 in the same paper; below it wage
     earners can press for more, and the level falls 2.6 for each point.

Every other rate below is an addition to the book.
"""
import numpy as np
from core import ScaleComponent, Publish, top_positions, squeeze, BASE


class Sabotage:
    name = "sabotage"
    reads = ("unemployment", "industry_growth", "industry_sought")
    supplies = ("hire_small", "hire_dominant", "entry_open")
    figures = {}           # nothing it supplies is a single yearly figure

    def __init__(self, normal_markup=0.10, target_markup=0.30, erosion=1.0, response=0.5,
                 hold=0.1, share_gain=0.75, labour_gain=2.6, gain_years=3.0, labour_holds_at=0.05, volume_cost=0.5,
                 top=100):
        self.normal_markup = normal_markup    # the markup at which small firms neither expand nor cut back
        self.target_markup = target_markup    # the markup dominant capital holds an industry toward
        self.erosion = erosion                # fall in the markup per unit of capacity growth beyond the pack (part 2)
        self.response = response              # extra hiring by small firms per unit of markup above normal (part 3)
        self.hold = hold                      # yearly speed at which a fully held industry approaches the target (part 4)
        self.volume_cost = volume_cost        # employment given up by dominant firms per unit of price rise (part 4)
        self.share_gain = share_gain          # rise in the capitalist share that goes with each unit of unemployment above the level below (part 5)
        self.labour_gain = labour_gain        # fall in that level for each unit of unemployment below the level below: the strength of wage earners when few are without work (part 5)
        self.gain_years = gain_years          # years that the share lags behind unemployment: each year 1 / gain_years of the gap is closed
        self.standing = 0.0                   # the gain in the share that unemployment has brought so far, by industry
        self.labour_holds_at = labour_holds_at  # unemployment at which wages keep pace with prices: the strength of labour
        self.resistance_shift = 0.05          # rise in that level of unemployment at full resistance
        self.top = top

    def industry_state(self, L):
        """Employees, share held by dominant capital, and markup, for each industry."""
        k = L.sector_of.size
        dominant = np.zeros(len(L), dtype=bool)
        dominant[top_positions(L.cap(), np.arange(len(L)), self.top)] = True
        n = np.bincount(L.ind, L.n, k)
        held = np.bincount(L.ind[dominant], L.n[dominant], k)
        priced = L.markup_earnings()          # earnings from the markup alone: interest and other income are left out
        # The rule works on the markup that firms price for. Where goods were unsold (another module), each
        # firm's earnings are divided by the part of them that it received; without that module the division is by 1.
        priced = priced / L.components.get("sales shortfall", 1.0)
        earnings = np.bincount(L.ind, priced, k)
        safe = np.maximum(n, 1e-12)
        markup = np.where(n > 0, earnings / (L.shared["wage"] * safe), self.normal_markup)
        held = held / safe
        held = np.maximum(held, L.accounts.get("second_country_held", 0.0))   # the part held by a second country's own dominant group (another module); 0 without it
        held = np.minimum(1.0, held + L.accounts.get("foreign_held", 0.0))   # the part owned by dominant capital across a border (another module); 0 without it
        return n, held, markup

    def hiring(self, L, held, markup, held_rise):
        g = L.shared["workforce_growth"]
        # the normal markup moves with the normal rate of return (another module); the number is 1 without it
        excess = markup - self.normal_markup * L.accounts.get("policy_rate_markup", 1.0)
        unbarred = L.accounts.get("protection_open", 1.0)   # part of each industry not under a protection (another module); 1 without it
        unbarred = unbarred * L.accounts.get("nature_open", 1.0)   # part of each industry that owners of nature leave open (another module); 1 without it
        small = g + self.response * excess * np.where(excess > 0, (1 - held) * unbarred, 1.0)   # entry barred where held
        n = np.bincount(L.ind, L.n, L.sector_of.size)
        pack = (small * n * (1 - held)).sum() / max((n * (1 - held)).sum(), 1e-12)
        dominant = min(g, pack) - self.volume_cost * held_rise / (1 + markup)
        return small, dominant

    def start(self, L):
        # This module owns the base markup. The base is a level: the markup a firm would have if no
        # gain or loss made by another rule stood on top of it. It stacks.
        L.add_component(BASE, self.name)
        n, held, markup = self.industry_state(L)
        small, dominant = self.hiring(L, held, markup, np.zeros_like(markup))
        return {"hire_small": small, "hire_dominant": dominant, "entry_open": 1 - held,
                "industry_growth": np.full(markup.size, L.shared["workforce_growth"])}

    def propose(self, L, rng):
        n, held, markup = self.industry_state(L)
        g, u = L.shared["workforce_growth"], L.accounts["unemployment"]
        # Part 2 works on the hiring that firms set out to do. In a year when they sought more people than the
        # working population held, they hired fewer than they sought, and they bid against each other for them.
        growth = L.accounts.get("industry_sought", L.accounts["industry_growth"])
        # Firms that closed took their capacity out of the industry (the failure module). Their buyers turn to the
        # firms that are left, so the part of the industry's employees that closed firms had counts as growth
        # that did not take place; 0 when no firm failed.
        growth = growth - L.accounts.get("failed_by_industry", 0.0)
        # Resistance strengthens labour: wages then keep pace with prices at a higher level of unemployment.
        # The strength of organised labour in each industry (another module) takes the place of popular resistance here.
        labour = L.accounts.get("labour_strength_by_industry", L.accounts.get("resistance", 0.0))
        holds_at = self.labour_holds_at + self.resistance_shift * labour
        holds_at = holds_at + L.accounts.get("second_country_labour", 0.0)       # a second country's own strength of labour (another module); 0 without it
        # Part 5. Unemployment sets a level for the capitalist share, and the share moves toward it. What has
        # been gained so far is remembered, so a year of unchanged unemployment adds only what is still missing.
        # When fewer people are without work than at that level, employers compete for them and wage earners press
        # for higher wages; each point of unemployment below the level then lowers the share by labour_gain.
        gap = u - holds_at
        level = np.where(gap > 0, self.share_gain * gap, self.labour_gain * gap)
        gain = (level - self.standing) / self.gain_years
        self.standing = self.standing + gain
        wages = gain * (1 + markup) ** 2          # a share s is a markup of s / (1 - s), so a small rise ds of the share is ds (1 + markup)^2 of markup
        wages = wages + L.accounts.get("currency_markup", 0.0)                    # a devaluation raises prices against wages (the currencies module); 0 without it
        undercut = -(1 - held) * self.erosion * (growth - g)                     # part 2
        grip = 1 - min(1.0, L.accounts.get("resistance", 0.0))                    # coordination weakens under resistance
        grip = grip * (1 - L.accounts.get("eruption_frees_markups", 0.0))         # an eruption suspends the hold (another module); 0 without it
        held_rise = held * self.hold * (self.target_markup * grip + self.normal_markup * (1 - grip) - markup)   # part 4
        # Part 4 adds the three changes. A rise is added; a fall is taken out of the margin as a part of what
        # is left, so it can take the markup close to nothing but never through it (squeeze in core.py).
        change = wages + undercut + held_rise
        new = squeeze(markup, change)
        # Wage earners take back only what owners still hold. Where the squeeze left part of a fall untaken, the
        # part of it that wage earners pressed for is not counted as taken back, and stays in the share's gain.
        untaken = np.maximum(new - (markup + change), 0.0)
        share_fall = np.minimum(gain * (1 + markup) ** 2, 0.0)
        falls = (share_fall + np.minimum(wages - gain * (1 + markup) ** 2, 0.0) + np.minimum(undercut, 0.0)
                 + np.minimum(held_rise, 0.0))
        pressed = np.where(falls < 0, share_fall / np.where(falls < 0, falls, 1.0), 0.0)
        self.standing = self.standing + pressed * untaken / (1 + markup) ** 2
        small, dominant = self.hiring(L, held, new, np.maximum(held_rise, 0.0))
        # The rule moves the markup of the industry as a whole. The change is proposed to the base
        # markup of every firm in the industry, in proportion. At the end of the year the core sets
        # the movement against what stands in the other stacking components of each firm: a fall
        # first takes away standing gains (such as a lead from price rises), and a rise first
        # restores standing losses (such as what was given up for unsold goods). Only the rest
        # stays in the base. See Model._net in core.py and "What a stacking component holds" in
        # modules.md. No firm's markup is changed by that reckoning.
        return [ScaleComponent(BASE, (new / markup)[L.ind], self.name),   # the price follows: the core works it out
                Publish("hire_small", small, self.name),
                Publish("hire_dominant", dominant, self.name),
                Publish("entry_open", 1 - held, self.name)]
