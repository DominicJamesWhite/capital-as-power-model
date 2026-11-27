"""Optional module: three alternative compasses. Each runs in place of module 7 (compass.py).

WHY

The compass decides when dominant capital turns from mergers to raising prices. The rule in
compass.py compares the volume of mergers over the last five years with the volume over the
last twenty. The full run then showed bouts of stagflation about every twenty-two years, and a
rule with a twenty-year memory can produce such a rhythm by itself. The three rules below use
no window of years at all. The only thing each remembers is the present intensity of
stagflation, and (for two of them) last year's total employment.

All three keep the cohesion of compass.py unchanged, so that a comparison between compasses
shows the effect of the trigger alone. All three still limit the intensity by cohesion.

THE THREE RULES IN PLAIN WORDS

1. TargetsCompass (--with compass_targets). The turn depends on a state, not on a history.
   The merger module reports the part of its reach that dominant capital does not yet hold.
   While dominant capital holds more than a set part of its reach, the gains from breadth have
   dried up and the intensity of stagflation rises each year. While it holds less, because a
   boundary has opened or new claims have refilled the pool, the intensity falls each year.

2. AheadCompass (--with compass_ahead). The turn depends on this year's figures only. The rule
   compares the rate at which dominant capital grew by buying (employees acquired, as a
   fraction of its own employees) with the rate at which total employment grew over the same
   year. While buying runs ahead of overall growth, the intensity falls. While it does not,
   the intensity rises.

3. ConsensusCompass (--with compass_consensus, and also --with compasses). The motive is the
   same as in rule 1: dominant capital holds more than a set part of its reach. A motive is not
   enough. The large owners are hesitant, so with a motive alone the intensity creeps up
   slowly. It rises fast only when people cannot resist: when unemployment is above its usual
   level and popular resistance is low. The slow creep itself cuts hiring (through the
   stagflation module), so dominant capital makes the slack that lets its own consensus form.
   The consensus dissolves in three ways. Employment that grows faster than the working
   population breaks coordination into a price war. Popular resistance sets the rulers
   bickering over whether to stop. And the motive disappears when targets are again within reach.

WHAT IT RESTS ON (Capital as Power, 2009, unless another source is named)

  - Chapter 16, "Stop-gap": inflation "is not the weapon of first choice. It is only when the
    gains from breadth dry up that dominant capital, seeing its differential accumulation
    undermined, moves reluctantly toward relying on inflationary redistribution". The benefits
    "come with mounting 'risks' which the large owners and leading government officials are
    often hesitant to take". (Rules 1 and 3: the motive; rule 3: the slow creep.)
  - Chapter 15, "Three transformations": dominant capital "is bound to reach its 'envelope',
    namely the boundaries of its own corporate universe with few or no takeover targets to
    speak of". (Rule 1: drying up is read from the pool of targets.)
  - Chapter 17, "Amalgamation versus stagflation": "when amalgamation resumed, with dominant
    capital breaking through its existing envelope and into a broader universe, stagflation
    promptly abated". (Rules 1 and 3: the intensity falls when the pool is open again.)
  - Chapter 14, Proposition 5: "For amalgamation to run ahead of overall growth, dominant
    capital must successively break its 'envelopes'". Proposition 7: inflation is "a much more
    potent response to declining mergers and acquisitions", and it is "often facilitated by
    previous corporate centralization". Proposition 8: "Occasional discontinuities in the
    process ... push dominant capital toward an alternative regime of stagflationary
    redistribution." (Rule 2: the test is whether amalgamation runs ahead of overall growth.)
  - Chapter 16, "The stagflation norm": buyers "are forced. And the way to force them is by
    creating, imposing and maintaining various forms of social crisis, apparent or real".
    "The effect of these crises on inflation is twofold. On the one hand, they undermine the
    ability of most people to resist price increases. On the other hand, they enable a
    consensus to emerge within dominant capital that inflation can be used with relative
    impunity." (Rule 3: the fast rise needs slack and low resistance.)
  - Chapter 16, "The imperative of crisis": bottlenecks "have to be actively created and
    instituted by the key players", and "unless it manages to cap overall growth, coordination
    is bound to disintegrate into a price war, leading to disinflation or even outright
    deflation". Growth "works to cool it off by undermining the ability to coordinate".
    (Rule 3: the creep makes the slack; growth dissolves the consensus.)
  - Chapter 16, "The politics of inflation": "The ruling class itself starts to bicker over the
    spoils of the process, over how to manage it and over whether or not to terminate it."
    (Rule 3: resistance dissolves the consensus.)
  - Chapter 17, "A new type of cycle": "there is nothing automatic or equilibrating about
    them", and "there is no inherent reason why amalgamation and stagflation should be cyclical
    in the first place". (No rule here contains a period.)
  - Nitzan, "Regimes of differential accumulation" (2001): "Previous crises were defused when
    dominant capital broke its 'envelope' ... And if, after this merger wave ends, there is
    indeed no new universe to conquer, what will bring stagflation to an end?" (Rule 1 can
    produce a bout that the compass never ends.)

WHAT IS ADDED

The literature describes conduct and gives no rule, no threshold and no rate. Every number
below is an addition. So are these choices: reading "the gains from breadth dry up" from the
part of its reach that dominant capital holds (rules 1 and 3); reading it from one year's
buying against one year's growth of employment (rule 2); measuring the inability of people to
resist by unemployment above its usual level times one minus popular resistance (rule 3); and
adding the three ways a consensus dissolves as separate yearly amounts (rule 3). Cohesion and
the limit it places on the intensity are copied from compass.py and are additions there too.

WHAT IS MISSING

The book's crises include war, reparations, default and oil embargoes. The only crisis these
rules can see is slack in employment. The book's consensus is formed among particular
coalitions; here dominant capital is one body with one intensity.
"""
import numpy as np
from core import Publish
from modules.compass import Compass


class _Replacement:
    """What the three compasses share: the cohesion of compass.py and the limit it sets."""
    replaces = ("compass",)       # full.py leaves compass.py out when one of these is switched on

    def __init__(self, rise=0.15, fall=0.10, concert=4.0, slack=20.0, usual_unemployment=0.05):
        self.rise = rise          # yearly rise in intensity while the trigger holds (same figure as compass.py)
        self.fall = fall          # yearly fall in intensity while it does not (same figure as compass.py)
        self.concert = concert    # the intensity cannot exceed this many times cohesion (compass.py uses 4)
        self.usual_unemployment = usual_unemployment   # unemployment above this level counts as slack
        self._cohesion = Compass(slack=slack, usual_unemployment=usual_unemployment).cohesion
        self.intensity = 0.0
        self.employment = None    # total employment at the start of last year

    def start(self, L):
        out = {"cohesion": self._cohesion(L), "stagflation_intensity": 0.0}
        out.update({k: 0.0 for k in self.supplies[2:]})
        return out

    def growth(self, L):
        """Growth of total employment over the last year (zero in the first year)."""
        now = float(L.n.sum())
        g = 0.0 if self.employment is None else now / self.employment - 1.0
        self.employment = now
        return g

    def finish(self, L, extra):
        c = self._cohesion(L)
        self.intensity = float(np.clip(self.intensity, 0.0, min(1.0, self.concert * c)))   # no concert, no inflation
        return [Publish("cohesion", c, self.name),
                Publish("stagflation_intensity", self.intensity, self.name)] \
            + [Publish(k, float(v), self.name) for k, v in extra.items()]


class TargetsCompass(_Replacement):
    """Rule 1: the turn comes when the pool of takeover targets within reach is used up."""
    name = "compass by targets"
    reads = ("concentration", "unemployment", "pool_open")
    supplies = ("cohesion", "stagflation_intensity", "breadth_dried")

    def __init__(self, dry=0.5, **common):
        super().__init__(**common)
        self.dry = dry            # the part of its reach dominant capital must hold before breadth counts as dried up
                                  # (the envelope module uses the same figure for the pressure that opens a boundary)

    def propose(self, L, rng):
        held = 1.0 - L.accounts["pool_open"]          # the part of its reach that dominant capital already holds
        dried = held > self.dry
        self.intensity += self.rise if dried else -self.fall
        return self.finish(L, {"breadth_dried": held})


class AheadCompass(_Replacement):
    """Rule 2: the turn comes in any year in which buying does not run ahead of overall growth."""
    name = "compass by lead"
    reads = ("concentration", "unemployment", "merger_volume")
    supplies = ("cohesion", "stagflation_intensity", "breadth_lead")

    def propose(self, L, rng):
        A = L.accounts
        first_year = self.employment is None          # nothing has been bought or hired yet, so there is nothing to compare
        growth = self.growth(L)
        # employees acquired last year, as a fraction of dominant capital's own employees
        bought = A["merger_volume"] / max(A["concentration"], 1e-12)
        lead = bought - growth
        if not first_year:
            self.intensity += -self.fall if lead > 0 else self.rise
        return self.finish(L, {"breadth_lead": lead})


class ConsensusCompass(_Replacement):
    """Rule 3: a motive, and a consensus that crisis lets form and that growth and resistance dissolve."""
    name = "compass by consensus"
    reads = ("concentration", "unemployment", "pool_open")
    supplies = ("cohesion", "stagflation_intensity", "impunity")

    def __init__(self, dry=0.5, hesitant=0.02, full_slack=0.05, price_war=5.0, bicker=0.2, **common):
        super().__init__(**common)
        self.dry = dry                # as in rule 1
        self.hesitant = hesitant      # yearly rise in intensity with a motive and no impunity: the reluctant owners
        self.full_slack = full_slack  # unemployment this far above its usual level leaves people unable to resist
        self.price_war = price_war    # yearly fall in intensity per unit by which employment growth exceeds
                                      # the growth of the working population
        self.bicker = bicker          # yearly fall in intensity at full popular resistance

    def propose(self, L, rng):
        A = L.accounts
        growth = self.growth(L)
        resistance = min(1.0, A.get("resistance", 0.0))
        slack = float(np.clip((A["unemployment"] - self.usual_unemployment) / self.full_slack, 0.0, 1.0))
        impunity = slack * (1.0 - resistance)
        motive = (1.0 - A["pool_open"]) > self.dry
        if motive:
            self.intensity += self.hesitant + (self.rise - self.hesitant) * impunity
        else:
            self.intensity -= self.fall
        self.intensity -= self.price_war * max(0.0, growth - L.shared["workforce_growth"])
        self.intensity -= self.bicker * resistance
        return self.finish(L, {"impunity": impunity})
