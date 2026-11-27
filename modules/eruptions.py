"""Optional module: eruptions that change the rules.

THE RULE IN PLAIN WORDS

The resistance module holds a level of popular resistance that contests power inside the rules:
it wins wages, loosens the concert of dominant capital and raises its risk. This module adds
the other kind of resistance, the kind that for a short time puts the rules themselves out of
force. It holds one number, the level of the eruption, between 0 and 1. The number is 0 in
ordinary years.

  1. The strain. Each year in which popular resistance stands at or above a threshold adds one
     to a count of years. A year below the threshold puts the count back to zero.
  2. The eruption. In each year without an eruption, the chance that one begins is a fixed
     rate times the count of years, and never more than 1. The module draws a random number
     from its own stream to decide. Sustained opposition therefore makes an eruption likely,
     and the year in which it comes is still not fixed in advance.
  3. Its course. An eruption stands at full strength for a few years. After that the level
     falls by a fixed part of itself each year, and it is put to zero when it is small. No
     new eruption can begin while one lasts, and the count of years starts again from zero.
  4. What it suspends. While the level is above zero the module publishes four numbers, each
     equal to the level times a setting. Four existing modules read them.
       - The sabotage module multiplies the grip of dominant capital on its target markup by
         one minus the first number. At a full eruption the industries that dominant capital
         holds drift toward the normal markup like any other industry.
       - The stagflation module multiplies the intensity of stagflation by one minus the
         second number. At a full eruption there are no concerted price rises and no cut in
         hiring.
       - The merger module multiplies the employees that each buyer seeks by one minus the
         third number. At a full eruption nobody buys a firm.
       - The resistance module multiplies the repression that the organised force module
         publishes by one minus the fourth number. At a full eruption force wears down no
         resistance. This number matters only when the organised force module is on.
  5. Fear. The risk of every firm is multiplied by 1 plus a setting times the level. The
     module removes last year's rise before it applies this year's, so the rise lasts only as
     long as the eruption. Every firm is treated alike, so the rise lowers all capitalization
     and leaves differential capitalization nearly unchanged. The module also publishes the
     level under the name "systemic_fear", which the optional hype and risk shaping modules
     already read.
  6. Readouts. The module publishes the level, the count of years of strain, and the number
     of eruptions so far.

The module invents no new rule. It cannot. An eruption in the literature is the appearance of
something new: "autonomy and cooperation", "direct self-rule". The module can only switch off,
for a time, rules that the model already has. What people build while the rules are off is
outside the model, and when the eruption fades the old rules come back exactly as they were.

Nothing comes from outside. Popular resistance is produced by the inflation, the unemployment
and the concentration that dominant capital itself produces. The random draw stands for the
statement of the book that the moment of an eruption cannot be anticipated. It is not a dated
event and it can do nothing unless resistance has stayed high.

WHAT IT RESTS ON

  - Bichler and Nitzan, "Growing Through Sabotage" (2020), section 8.1. Resistance "takes two
    forms: power-replacing and power-negating. The two forms can coexist in actual struggles,
    but they are clearly distinct conceptually. The first form is internal to the power
    struggle itself". "The second type of resistance is external to the power struggle
    proper. It originates not from a quest for power, but from its very negation - namely,
    the desire to undo hierarchy altogether in favour of autonomy and cooperation. This
    latter drive is often latent, buried under the dead weight of hierarchical power, but it
    is always there". The resistance module is the first form. This module is the second.
  - The same paper, section 11.1. "Most of the time, this quest for autonomy is latent and
    largely invisible. But occasionally it erupts, usually unpredictably, to stir society, if
    only for a brief historical moment, toward greater creativity, cooperation and
    self-rule." A footnote lists eruptions from the English Civil War to the Arab Spring.
    The same section says that after such a shift "the ever-present Machiavellian force is
    likely to kick back". Part 3 rests on the words "brief historical moment" and "kick back".
  - Capital as Power (2009), chapter 17, the last page before the postscript. The patterns
    of accumulation "show the conviction of the rulers that they are in command - and that
    those whom they command cannot resist. This conviction, though, is never certain.
    Confronted with sufficient opposition, whether explicit or implicit, it can crumble. And
    when it does crumble, the result is to shatter the 'determinism' of the rulers, the
    patterns of their differential accumulation and, possibly, the entire state of capital
    that defines their rule." Parts 1 and 2 rest on "sufficient opposition". Part 4 rests on
    "shatter ... the patterns of their differential accumulation": both of the model's
    regimes, buying and concerted price rises, are suspended.
  - Chapter 17, postscript. "Power is confidence in obedience: it represents the certainty of
    the rulers in the submissiveness of the ruled. In modern capitalism, this certainty is
    manifested in the ability of capitalists to control and systematize the upward movement
    of prices." The first two numbers of part 4 rest on this sentence: when the certainty
    goes, the control over prices goes with it.
  - Chapter 1, "The capitalist creorder and humane society". The humane society "exists
    mostly as an unknown potential. Usually, it is dormant and therefore invisible.
    Occasionally, though, it erupts, often without warning, to challenge and sometimes
    threaten the institutions of capitalist power. These eruptions - and their consequences
    - do not follow a pre-set pattern. They cannot be systematically theorized." The
    language of capitalist power "can never anticipate when and how they will erupt". The
    determinism of capitalization "works only insofar as the ruling class rules", and when
    people see that the rules are imposed by other people, "determinism disappears, replaced
    - if only for a historical instant - by the humane promise of
    autonomy-democracy-philosophy". This passage is the reason for the random draw of part 2,
    and it is also a warning against this whole module, which is repeated below.
  - Bichler and Nitzan, "Systemic Fear, Modern Finance and the Future of Capitalism" (2010).
    "When the ruling class is no longer certain of its ability to govern, it becomes
    indecisive; indecision inhibits ruthlessness; lack of ruthlessness fuels opposition; and
    effective opposition is the other side of disintegrating rule." The fourth number of
    part 4 is the lack of ruthlessness. "Under the surface, redistribution requires greater
    sabotage and larger doses of force, and as social stress builds up, the stage is set for
    the crucial inversion." Part 1 is that building up. Of the 1930s the paper says that
    "the rulers were no longer confident in the obedience of the ruled", and that "the very
    institution of capitalization was put into question, so even if future earnings could
    somehow be predicted, it didn't seem certain that future ownership claims on these
    earnings could be priced and transacted". The third number of part 4, the stop to the
    buying of firms, rests on the last sentence.
  - Chapter 11, "The degree of confidence". The risk coefficient expresses, inversely, "the
    degree of confidence capitalists have in their own predictions", and "when capitalists
    are fully confident" it is 1. Part 5 rests on this.

WHAT IS ADDED

The literature says that eruptions happen, that they are brief, that sufficient opposition
can make the confidence of the rulers crumble, and that the patterns of accumulation are then
shattered. It gives no rule and no rate, and it says that there can be none. Every number
below is an addition. The form of every part is an addition. Three choices need saying.
First, the book says that eruptions "cannot be systematically theorized" and that nobody can
anticipate "when and how" they come. A rule that makes an eruption likely after some years of
high resistance goes against the letter of that passage. The rule keeps the timing open by a
random draw, and it rests on the other passages, which tie the crumbling of confidence to
"sufficient opposition" and to stress that "builds up". Second, the module measures the
latent drive toward autonomy by the same number that measures resistance inside the rules.
The 2020 paper says that the two forms are "clearly distinct conceptually" and "can coexist
in actual struggles", and the model holds only one level of popular resistance. Third, the
book says that the population is "impartial to breadth", and the rule still stops the buying
of firms during an eruption, on the ground of the 2010 paper.

WHAT IS MISSING

The module says nothing about what people do while the rules are suspended. It closes no
boundary and breaks up no firm. It does not let an eruption end the rule of capital: the old
rules always return, and they return unchanged, where the 2020 paper expects the returning
hierarchy to stand higher than before. The module does not let an eruption be put down by
force before it has run its course. It does not let the fear of an eruption act on the rulers
before one begins. The 2016 paper measures systemic fear by the way owners price shares, and
this module only sets the number "systemic_fear" equal to the level of the eruption.
"""
import numpy as np
from core import Scale, Publish


class Eruptions:
    name = "eruptions"
    reads = ("resistance",)
    supplies = ("eruption", "eruption_frees_markups", "eruption_stops_price_rises", "eruption_stops_buying",
                "eruption_stays_force", "systemic_fear", "eruption_strain", "eruption_count")

    def __init__(self, threshold=0.4, chance=0.1, lasts=3, restore=0.5, least=0.05,
                 frees_markups=1.0, stops_price_rises=1.0, stops_buying=1.0, stays_force=1.0, fear_risk=0.5):
        self.threshold = threshold    # level of popular resistance that counts as very high (the bouts of the nine modules reach 0.4 to 0.5)
        self.chance = chance          # yearly chance of an eruption for each year in a row that resistance has stood at or above the threshold
        self.lasts = lasts            # years an eruption stands at full strength: the "brief historical moment"
        self.restore = restore        # part of the level that is lost each year after that, as the old rules return
        self.least = least            # a level below this is put to zero
        self.frees_markups = frees_markups          # part of dominant capital's grip on its target markup that a full eruption removes (sabotage module)
        self.stops_price_rises = stops_price_rises  # part of the intensity of stagflation that a full eruption removes (stagflation module)
        self.stops_buying = stops_buying            # part of the buying of firms that a full eruption stops (merger module)
        self.stays_force = stays_force              # part of repression that a full eruption stays (resistance module, with the organised force module)
        self.fear_risk = fear_risk    # rise in the risk of every firm at a full eruption
        self.level = 0.0              # the level of the eruption, from 0 to 1
        self.years_high = 0           # years in a row with resistance at or above the threshold
        self.years_left = 0           # years of full strength still to come
        self.count = 0                # eruptions so far
        self.risk_applied = 1.0       # the factor now standing in the risk of the firms

    def readouts(self):
        x = self.level
        out = {"eruption": x,
               "eruption_frees_markups": self.frees_markups * x,
               "eruption_stops_price_rises": self.stops_price_rises * x,
               "eruption_stops_buying": self.stops_buying * x,
               "eruption_stays_force": self.stays_force * x,
               "systemic_fear": x,
               "eruption_strain": float(self.years_high),
               "eruption_count": float(self.count)}
        return [Publish(k, float(v), self.name) for k, v in out.items()]

    def start(self, L):
        return {c.key: c.value for c in self.readouts()}

    def propose(self, L, rng):
        resistance = float(L.accounts["resistance"])
        draw = rng.random()                         # drawn every year, so that the stream does not depend on the state
        if self.level > 0.0:                        # part 3: the course of an eruption
            if self.years_left > 0:
                self.years_left -= 1
            else:
                self.level *= 1.0 - self.restore
                if self.level < self.least:
                    self.level = 0.0
        else:
            self.years_high = self.years_high + 1 if resistance >= self.threshold else 0   # part 1
            if draw < min(1.0, self.chance * self.years_high):                             # part 2
                self.level, self.years_left, self.years_high = 1.0, self.lasts - 1, 0
                self.count += 1
        changes = self.readouts()                   # parts 4 and 6
        wanted = 1.0 + self.fear_risk * self.level  # part 5
        if wanted != self.risk_applied:
            changes.append(Scale("risk", wanted / self.risk_applied, self.name))
            self.risk_applied = wanted
        return changes
