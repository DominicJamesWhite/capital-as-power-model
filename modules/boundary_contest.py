"""Optional module: the contest over a boundary. It runs in place of module 9 (envelope.py).

THE RULE IN PLAIN WORDS

A boundary (first the sector, then the nation) is the object of a contest with two sides.

The push. Dominant capital pushes on a boundary together with the government organs it is
tied to. The push is the product of three numbers, each between 0 and 1:
  1. The need: the part of its reach that dominant capital already holds. This is the same
     number the envelope module calls pressure, and the merger module supplies it.
  2. The sway: how far dominant capital and government organs act as one body. It is measured
     by the part of the government's debt that dominant capital holds, which the debt module
     reports. The sway is complete when that part reaches a setting.
  3. The commitment: one minus the intensity of stagflation. While dominant capital is gaining
     through prices, it does not press for openings that would let rivals at its margins.

The hold. The boundary is held by roadblocks, the number the resistance module raises with the
volume of mergers. Popular resistance takes no part, because the population is "impartial to
breadth".

The outcome. When the push exceeds the hold, the nearest closed boundary opens at a speed in
proportion to the excess. When the hold exceeds the push by a margin, the widest open boundary
closes again. In a year in which a boundary opens, every claim of dominant capital loses a
little of its markup, in proportion to the opening, because the wider field brings new rivals.

WHAT IT RESTS ON (Capital as Power, 2009, unless another source is named)

  - Chapter 14, Proposition 5: "For amalgamation to run ahead of overall growth, dominant
    capital must successively break its 'envelopes', spreading from the industry, to the
    sector, to the national economy, and ultimately to the world as a whole."
  - Chapter 15, "Three transformations": dominant capital "is bound to reach its 'envelope',
    namely the boundaries of its own corporate universe with few or no takeover targets to
    speak of". Amalgamation "is restricted by the ability of broader state institutions to
    quickly accommodate the new corporate formations", and "as amalgamation builds up momentum,
    it also generates higher and higher roadblocks, contradictions and counter-forces".
  - The footnote to that sentence: "The 1933 Glass-Steagall Act, for instance, barred US banks
    from making industrial investments", and "similar transformational effects were brought on
    by the post-war dismantling of the Japanese Zaibatsu". The 2001 regimes paper says the Act
    "reversed an earlier diversification trend". This is the ground for a boundary closing.
  - Chapter 15, "Breaking the envelope": "amalgamation is simply too important to give up",
    and "to take advantage of this broader pool, dominant capital has to break through its
    original 'envelope'". Mergers "create a strong drive toward 'jurisdictional integration',
    to use Olson's terminology (1982). Yet this very integration pits dominant capital against
    new rivals under new circumstances".
  - The footnote on South Africa: "With capital trapped at home, they gobbled up all available
    companies in their industries before acquiring companies in other sectors and becoming
    conglomerates." This is the ground for the inner boundary giving way before the outer one.
  - Chapter 15, "Differential advantage": mergers make the fused entities "increasingly
    intertwined with other larger firms and government bodies, and more involved in setting
    polices and regulations". Chapter 14 defines dominant capital as "the leading
    corporate-government coalitions". Chapter 17 names an alliance of merger firms "backed by
    Third-Way governments", under which "capital controls gave way to deregulation".
  - Sandy Brian Hager, "What Happened to the Bondholding Class?" (2013), reporting Henry Carter
    Adams: "Through concentrated ownership of government bonds, the bondholding class exerts
    control over the government apparatus". This is the ground for measuring the sway by
    dominant capital's part of the government's debt.
  - Chapter 15, "Globalization": "dominant capital is often half-hearted about indiscriminate
    deregulation, particularly when such deregulation allows competitors to undermine its
    differential margins". Chapter 17: "the power processes that support one type of
    differential accumulation tend to undermine the other". These are the ground for the
    commitment and for the loss of markup when a boundary opens.
  - The footnote that criticises studies which treat deregulation "as external societal
    'shocks' to which business 'responds' with amalgamation". Nothing here comes from outside.

WHAT IS ADDED

The literature says who opens a boundary, why, and what holds it. It gives no rule for the
contest and no rates. The product of three numbers, the comparison with roadblocks, and every
setting below are additions. Olson's own argument (that a wider jurisdiction breaks up the
coalitions formed inside the narrower ones) is not in the texts on disk; the book borrows only
his term, and the loss of markup follows the book's sentences, not his.

WHAT IS MISSING

The dismantling of the Zaibatsu and the unbundling of the South African groups were forced
sales. The ledger does not record which of a claim's employees were acquired across which
boundary, so this module cannot make dominant capital sell what a closed boundary forbids.
A closing only stops further buying across the boundary.
"""
import numpy as np
from core import ScaleComponent, Set, Publish, top_positions

COST = "rival cost"    # this module's markup component: the markup lost to new rivals when a boundary opens; it stacks


class BoundaryContest:
    name = "boundary contest"
    replaces = ("envelope",)      # full.py leaves the envelope module out when this one is switched on
    reads = ("pool_open", "concentration")
    supplies = ("pressure", "boundary_push", "boundary_hold")

    def __init__(self, full_sway=0.25, hold=1.0, speed=0.3, close_margin=0.3, rival_cost=0.10, top=100):
        self.full_sway = full_sway        # the part of the government's debt dominant capital must hold for its sway to be complete
        self.hold = hold                  # how much push one unit of roadblocks holds back
        self.speed = speed                # yearly movement of a boundary per unit by which the push exceeds the hold
        self.close_margin = close_margin  # how far the hold must exceed the push before a boundary closes again
        self.rival_cost = rival_cost      # part of dominant capital's markup lost to new rivals when a boundary opens fully
        self.top = top

    def start(self, L):
        L.add_component(COST, self.name)
        return {"pressure": 0.0, "boundary_push": 0.0, "boundary_hold": 0.0}

    def sway(self, L):
        """How far dominant capital and government organs act as one body, from 0 to 1."""
        A = L.accounts
        debt = A.get("government_debt", 0.0)
        if debt > 0:                                       # dominant capital's part of the government's debt (debt module)
            tie = A.get("government_debt_dominant", 0.0) / debt
        else:                                              # without the debt module: its part of all employees
            tie = A["concentration"]
        return float(min(1.0, tie / self.full_sway))

    def propose(self, L, rng):
        A = L.accounts
        need = 1.0 - A["pool_open"]                        # the part of its reach that dominant capital already holds
        commitment = 1.0 - min(1.0, A.get("stagflation_intensity", 0.0))
        push = need * self.sway(L) * commitment
        hold = self.hold * A.get("roadblocks", 0.0)
        hold = hold * (1.0 - A.get("barrier_bargain", 0.0))   # forced sales at home traded for an opening (optional module); 0 without it
        net = push - hold
        sector, nation = L.shared.get("perm_sector", 0.0), L.shared.get("perm_nation", 0.0)
        changes = [Publish("pressure", need, self.name),
                   Publish("boundary_push", push, self.name),
                   Publish("boundary_hold", hold, self.name)]
        opened = 0.0
        if net > 0:                                        # the nearest closed boundary gives way first
            if sector < 1.0:
                new = min(1.0, sector + self.speed * net)
                opened = new - sector
                changes.append(Set("perm_sector", new, self.name))
            elif nation < 1.0:
                new = min(1.0, nation + self.speed * net)
                opened = new - nation
                changes.append(Set("perm_nation", new, self.name))
        elif -net > self.close_margin:                     # the hold wins: the widest open boundary closes first
            back = self.speed * (-net - self.close_margin)
            if nation > 0.0:
                changes.append(Set("perm_nation", max(0.0, nation - back), self.name))
            elif sector > 0.0:
                changes.append(Set("perm_sector", max(0.0, sector - back), self.name))
        if opened > 0 and self.rival_cost > 0:             # the wider field brings new rivals to dominant capital's margins
            dominant = np.zeros(len(L), dtype=bool)
            dominant[top_positions(L.cap(), np.arange(len(L)), self.top)] = True
            f = np.where(dominant, 1.0 - self.rival_cost * opened, 1.0)
            changes.append(ScaleComponent(COST, f, self.name))   # the price falls with the markup: the core works it out
        return changes
