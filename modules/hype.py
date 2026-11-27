"""Optional module: hype as a lever (rebuilt).

This file replaces a first version. The first version had three faults. It turned the
insiders' push around when the hype of dominant capital reached 1.43 times the average, and
1.43 is only the largest reading of one index in one sample. It did not count what insiders
gain. It built its own systemic fear. All three are corrected here, and the section
"WHAT WAS REMOVED" at the end lists every number that went with them.

WHAT HYPE IS HERE

The book defines hype as "the ratio of expected future earnings to actual future earnings"
(chapter 11, "Decomposition"). It is "the ex post collective error of capitalists when pricing
the asset", and it "is revealed only once the earnings are reported". Hype is never a
departure from a "true value". This module keeps to that definition in the following way.

The earnings in the ledger at the start of a year are the earnings that have already arrived.
The hype term of a claim at that moment is the earnings that owners expect for the coming
year, divided by the earnings that have arrived. The module calls this number the multiple.
A year later the ledger shows what did arrive. The module then divides what was expected by
what arrived. That ratio is the book's hype for the year just ended, and the module calls it
the revealed hype. Every correction in the rule acts on the revealed hype. Nothing in the rule
pulls a price toward a value, and nothing in the rule names a level at which hype turns.

THE TWO GROUPS OF OWNERS

Insiders are the owners who know what is about to happen to the multiple of a claim of
dominant capital, and who can shape it. Outsiders are all other owners. The module does not
count how much of each claim the insiders usually hold. It counts only how far they depart
from that: the part of a claim they have bought from outsiders beyond their usual part, or
have sold to outsiders. A sale can go beyond what they hold, which is a short sale.

THE RULE IN PLAIN WORDS

  1. Revealed error. For each claim the module remembers the earnings per employee of a year
     ago. The revealed hype of a claim is last year's multiple, times the earnings per
     employee of a year ago, divided by the earnings per employee now. The revealed hype of
     the whole envelope is the same ratio for all claims taken together.
  2. The herd. Each year all forecasters revise all multiples by one common amount. The
     common amount removes a fixed part of the error that the arrived earnings revealed for
     all claims together. The herd corrects only part of the error, and corrects it a year
     late.
  3. Each claim. The multiple of a single claim is also corrected, more slowly, for the
     amount by which its own revealed error differs from the common one.
  4. Mergers. The claims of dominant capital receive an upward push in proportion to the
     employees that dominant capital acquired in the year before, measured against its own
     employees. The push ends when the acquisitions end.
  5. Insiders trade. Insiders know the change that parts 2, 3 and 4 are about to bring to the
     multiple of each claim of dominant capital, because they know the reported earnings, the
     habits of the herd and the acquisitions under way. They buy a claim in proportion to the
     rise that is coming and sell it in proportion to the fall that is coming. Their position
     in a claim cannot exceed a fixed part of the claim in either direction. They close their
     position in a claim that has dropped out of dominant capital.
  6. Insiders push. Insiders talk up the claims in which they hold more than their usual
     part, and talk down the claims that they have sold short. The yearly push on a claim's
     multiple is in proportion to their position in it and to the cohesion of dominant
     capital, which says how far its members can act in concert.
  7. Hype feeds mergers. The module publishes the hype of dominant capital divided by the
     hype of all claims. The merger module multiplies the amount each buyer seeks by this
     number. This is the only change to an existing module, and the number is one when this
     module is off.
  8. What insiders gain. The change that the year brings to a claim's multiple changes its
     capitalization. The insiders' gain on a claim is their position in it times that
     change. It is positive when they hold more than usual and hype rises, and when they are
     short and hype falls. Outsiders hold the other side of every position, so the gain of
     insiders is the loss of outsiders against what they would have had if nobody had traded.
     The module adds the gains of the year together and divides by the capitalization of all
     claims. It publishes that yearly part and its running sum.
  9. With the owners module on. The owners module keeps, for every claim, the part held
     directly by the claim's own large owners. The rest is held through funds. The hype
     module treats the direct owners of dominant capital as the insiders and the funds as the
     outsiders. Each purchase or sale of part 5 moves the same part of the claim between
     direct holdings and the funds. The gain of part 8 is taken in shares: direct owners use
     it to buy more of the claim from the funds at the new price, and they sell shares to
     cover a loss. Direct holdings cannot go above the whole claim and cannot be pushed below
     the controlling block of the owners module, so a short sale does not show in them.

HOW A SWING REVERSES

No part of the rule tells hype when to turn. A rise in the multiples of dominant capital is
followed a year later by reported earnings that fall short of what was expected. Parts 2 and
3 then pull the multiples down. The pull grows with the error, so at some point the fall that
is coming outweighs the rise that is coming. From that year the insiders of part 5 sell.
Their push in part 6 weakens as they sell and turns downward when they are short. When the
multiples have fallen below what the arriving earnings bear out, the same parts work in the
other direction and insiders buy again.

WHAT THE MODULE PUBLISHES

  hype_average           the multiple of all claims taken together
  hype_dominant          the multiple of dominant capital
  hype_revealed          the book's hype for the year just ended, all claims together
  hype_insiders          the insiders' position in dominant capital as a part of the largest
                         position they may hold (+1 fully bought, -1 fully sold short)
  merger_hype            the number that the merger module reads (part 7)
  hype_passed_year       the part of all capitalization that passed from outsiders to
                         insiders in the year (negative when insiders lost)
  hype_passed            the running sum of hype_passed_year
  hype_passed_dominant   the same running sum, with each year's gain divided by the
                         capitalization of dominant capital alone
  hype_shift             with the owners module on, the running sum of the yearly parts of
                         all capitalization that part 9 moved from the funds into direct
                         holdings (trades and gains together); 0 otherwise

The module changes the hype term of claims through Scale. It keeps two per-claim attributes
of its own (last year's earnings per employee, and the insiders' position). With the owners
module on it also scales that module's attribute "held_directly".

THE LINK LEFT FOR SYSTEMIC FEAR

The module reads L.accounts.get("systemic_fear", 0.0). No module supplies that number yet. A
later module on the power index is meant to. When the number is 0 the read has no effect.
When it is above 0, every upward push of parts 4 and 6 is multiplied by one minus the
number. This rests on Bichler and Nitzan, "A CasP Model of the Stock Market" (2016): when
"the level of hype" is "already high", "increasing it further ... becomes harder and
harder". The form of the link is an addition and the later module may replace it.

WHAT IT RESTS ON

  - Chapter 11, "Decomposition": the definition quoted above, and "When they are excessively
    optimistic, the hype factor is greater than 1. When they are exceedingly pessimistic,
    hype is less than 1."
  - Chapter 11, "Movers and shakers of hype". Expectations "eventually converge to actual
    earnings", so the hype coefficient "tends to revert to a long-term mean value of 1".
    Parts 2 and 3 are that convergence. If the movements of hype are large and patterned,
    "this situation would open the door for 'insiders' to practically print their own money
    and therefore to try to manipulate hype to that end". The insider "knows something about
    future earnings that other capitalists do not"; examples are "a KKR partner who is
    secretly orchestrating a big leveraged buyout" and a financier "discretely informed of an
    imminent Fed-financed bailout". This knowledge "allows them to buy assets for which
    earning expectations fall short of 'true' earnings - and wait". Part 5 rests on this. The
    active insider "knows not only how to identify hype, but also how to shape its
    trajectory", and "tends to operate not individually, but in loosely organized pacts of
    capitalists, public officials, pundits and assorted 'opinion makers'". "The active
    insiders in the scheme leveraged their positions - and then stirred the capitalist
    imagination and frothed the hype to amplify their gains many times over." Part 6 rests on
    this: the position comes first and the push follows it. On gains and on the reversal:
    "By definition, a rise in hype inflates the fortunes of outsiders who unknowingly
    happened to ride the bandwagon." "Since hype is a cyclical process, its reversion works
    both ways. And so, as the upswing builds momentum and hype becomes excessive, those 'in
    the know' start selling the market short to those who are not in the know. Eventually -
    and if need be with a little inside push - the market tips. And as prices reverse
    direction, the short-positioned insiders see their fortunes swell as fast as the market
    sinks. Finally, when the market bottoms, the insider starts accumulating under-hyped
    assets so that the process can start anew." Parts 5, 6 and 8 follow this passage.
  - Chapter 11, "Flocks of experts and the inefficiency of markets": forecast errors "tend to
    be large, persistent and very similar to those of their peers. They do not seem to learn
    from their own mistakes, they act as a herd, and when they do respond to circumstances,
    their adjustment is painfully lethargic." Analysts "pay far more attention to the
    changing sentiment of other analysts than to the changing facts". Part 2 moves all
    multiples together and only part of the way for this reason. Part 3 is slower than part 2
    for this reason.
  - Chapter 11, "Let there be hype": "there is no built-in 'mechanism' to stop the
    insiders". "Since the experts tend to move in a flock, it is enough to influence or
    co-opt those who lead (the mean estimate) in order to shift the entire pack". "A dollar
    invested in changing earning expectations could yield a return far greater than a dollar
    spent on increasing the earnings themselves."
  - Appendix to chapter 11, Figure 11.2. The estimates of strategists "are usually set at the
    beginning of the year as some positive multiple of current earnings". The strategists
    "underestimate earning when they are rising" and "overestimate them when they are stable
    or falling". The module takes from the appendix only the idea of a multiple of current
    earnings. The direction of the errors is not a setting: it follows from parts 1 and 2,
    because a multiple set before earnings rise turns out too low. The appendix also reports
    readings from 1.43 to 0.74, a mean of 1.02, an average multiple of 1.08 and a cycle of
    "four to five years". These are observations of one index of five hundred firms between
    1988 and 2006. None of them is used as a setting here.
  - Chapter 12, on goodwill: what makes the capitalization of a merged firm "greater than
    the sum of its parts is the additional social power generated by the merger: the power
    to increase differential earnings, raise differential hype and reduce differential
    uncertainty". Chapter 15, "Differential advantage": "mergers often generate differential
    hype that owners can leverage to their own advantage". Part 4 rests on these.
  - Chapter 17: "'high-technology' was firing up both investor's hype and the stock market,
    giving mergers and acquisition repeated shots of adrenalin". Nitzan and Bichler,
    "Dominant Capital and the New Wars" (2004): "Corporate takeover thrives on investors'
    hype and an open takeover pool". Part 7 rests on these.
  - Chapter 12, "The absentee ownership of power": owners through funds "merely buy and sell
    shares of these assets and collect the flow of dividends. Often, their diversification is
    so extensive that they don't know exactly what they own." Part 9 treats the funds as the
    outsiders for this reason.

WHAT IS ADDED

The literature gives the definition of hype, the direction of every effect and the order of
the insiders' moves. It gives no rule and no rate. Every number in the rule is therefore an
addition, and none is taken from a figure in the literature:
  - the herd removes 50 per cent of the common revealed error each year;
  - 20 per cent of a claim's own further error is removed each year;
  - the push from mergers is half of the employees acquired, as a part of dominant capital's
    own employees;
  - insiders buy 1 per cent of a claim for each per cent of rise that is coming;
  - their position is at most 10 per cent of a claim in either direction;
  - their yearly push at the largest position equals the cohesion of dominant capital;
  - buyers seek 1 per cent more for each per cent of differential hype;
  - with the owners module on, direct holdings are not pushed below 10 per cent, which is the
    controlling block of that module.
The forms are additions as well. Insiders are taken to know the coming change exactly, where
the book says only that they know more than others. Their push is tied to cohesion. Insiders
trade only the claims of dominant capital. Part 7 uses differential hype, where the first
version used the hype of dominant capital alone; a buyer pays with claims that are dear
against what it buys, and the passages speak of hype in general. Forecasters are taken to
forecast earnings per employee, so they are taken to foresee the employees a claim gains by
merger. Part 8 counts only the gains that come from changes in hype. Part 9 follows the
owners module in letting a buyer's pattern of ownership stand for the whole merged claim, and
the same holds for the insiders' position. In part 9 the gain is taken in shares each year
and money is not tracked.

WHAT IS MISSING

The insiders are one group and the module does not say which owners belong to it. Outsiders
are not divided, so the module cannot say which of them lose. The owners module does not
learn of the trades of part 9 when it reckons the make-up of the funds. The correction of
part 2 arrives one year after the error, because a module sees only the ledger at the start
of a year. The level of the average multiple has no effect on any other module; only the
differential part of hype and the insiders' gains have consequences. The press findings of
this project are not used.

WHAT WAS REMOVED FROM THE FIRST VERSION

  - The turning level of 1.43 and the floor of 1 for the insiders' push. See the top of this
    file.
  - The swing of four and a half years. The first version built a swing of that length into
    the herd's revisions. The appendix reports "four to five years" as the cycle it observed
    in the errors of strategists for one index. It is an outcome, so it may not be a setting.
  - The setting for the part of a swing that survives each year, which belonged to the same
    built-in swing.
  - Systemic fear, with its threshold of two standard deviations, its waiting time of thirty
    years and its rate. The two standard deviations in the 2016 paper belong to the share
    price index divided by the wage rate. The subject belongs to a later module.
"""
import numpy as np
from core import Scale, Publish, top_positions

SEEN = "hype_epe_seen"        # earnings per employee of each claim a year ago; negative means "none yet"
BOOK = "hype_insider_book"    # one plus the part of a claim that insiders hold beyond their usual part (below one: sold, or sold short)
OWNED = "held_directly"       # the attribute of the owners module, used only when that module is on


class Hype:
    name = "hype"
    reads = ("merger_volume", "cohesion")
    supplies = ("hype_average", "hype_dominant", "hype_revealed", "hype_insiders", "merger_hype",
                "hype_passed_year", "hype_passed", "hype_passed_dominant", "hype_shift")

    def __init__(self, herd=0.5, own=0.2, trade=1.0, bound=0.10, lever=1.0, goodwill=0.5,
                 takeover=1.0, block=0.10, top=100):
        self.herd = herd           # part of the common revealed error that all forecasters remove from every multiple each year (addition; "painfully lethargic")
        self.own = own             # part of a claim's own revealed error, beyond the common one, that is removed each year (addition; forecasters attend to each other more than to the facts)
        self.trade = trade         # part of a claim that insiders buy in a year for each unit by which the logarithm of its revealed hype is below zero, and sell for each unit above (addition)
        self.bound = bound         # the largest part of a claim that insiders can hold beyond their usual part, or sell short (addition; a limit on positions, not on hype)
        self.lever = lever         # yearly push on a claim's multiple when insiders hold their largest position in it and dominant capital acts fully in concert (addition)
        self.goodwill = goodwill   # push on the multiples of dominant capital per unit of employees it acquired last year, as a part of its own (addition)
        self.takeover = takeover   # per cent change in what buyers seek for each per cent by which the hype of dominant capital exceeds the hype of all claims (addition)
        self.block = block         # with the owners module on: the part of a claim that direct owners never sell; the same 10 per cent as in that module
        self.top = top
        self.passed = 0.0          # running sum of the yearly parts of all capitalization that passed from outsiders to insiders
        self.passed_dominant = 0.0  # the same, with each year measured against the capitalization of dominant capital
        self.shift = 0.0           # with the owners module on: running sum of the yearly parts of all capitalization moved into direct holdings

    def start(self, L):
        L.add_attribute(SEEN, -1.0, -1.0)
        L.add_attribute(BOOK, 1.0, 1.0)
        return {"hype_average": 1.0, "hype_dominant": 1.0, "hype_revealed": 1.0, "hype_insiders": 0.0,
                "merger_hype": 1.0, "hype_passed_year": 0.0, "hype_passed": 0.0,
                "hype_passed_dominant": 0.0, "hype_shift": 0.0}

    def propose(self, L, rng):
        A = L.accounts
        E, h, e, n, seen = L.earnings(), L.h, L.e, L.n, L.extra[SEEN]
        held = L.extra[BOOK] - 1.0
        K = L.cap()
        top = top_positions(K, np.arange(len(L)), self.top)
        dominant = np.zeros(len(L), dtype=bool)
        dominant[top] = True

        # part 1: what was expected a year ago over what arrived
        known = seen > 0
        revealed = np.where(known, h * np.where(known, seen, 1.0) / e, 1.0)
        herd_revealed = float((E * revealed).sum() / E.sum())
        err, herd_err = np.log(revealed), np.log(herd_revealed)

        # part 2: the herd removes part of the common error; part 3: and, more slowly, part of each claim's own
        change = -self.herd * herd_err - self.own * (err - herd_err)

        # part 4: acquisitions of the year before raise the multiples of dominant capital
        # (the optional link to the power index and systemic fear module weakens upward pushes; 0, no effect, when that module is off)
        fear = float(np.clip(A.get("systemic_fear", 0.0), 0.0, 1.0))
        merged = self.goodwill * A["merger_volume"] * n.sum() / n[top].sum() * (1 - fear)
        change = change + np.where(dominant, merged, 0.0)
        # (optional link to the fear module: near the ceiling of the power index owners hold the multiple of current
        # earnings still, so every change of the year is multiplied by one minus "power_fear"; 0, no effect, without that module)
        hold = 1.0 - float(np.clip(A.get("power_fear", 0.0), 0.0, 1.0))
        change = change * hold

        # part 5: insiders know the change that is coming; they buy before a rise and sell before a fall
        position = np.where(dominant, np.clip(held + self.trade * change, -self.bound, self.bound), 0.0)
        bought = position - held

        # part 6: insiders talk up what they hold and talk down what they have sold short
        push = self.lever * A["cohesion"] * position / self.bound
        push = np.where(push > 0, push * (1 - fear), push) * hold
        factor = np.exp(change + push)

        # part 8: what the year's change in hype moves from outsiders to insiders
        gain = position * K * (factor - 1.0)
        passed_year = float(gain.sum() / K.sum())
        self.passed += passed_year
        self.passed_dominant += float(gain.sum() / K[top].sum())

        hype_dominant = float((E[top] * h[top]).sum() / E[top].sum())
        hype_average = float((E * h).sum() / E.sum())
        changes = [Scale("hype", factor, self.name),
                   Scale(SEEN, e / seen, self.name),                 # remember this year's earnings per employee
                   Scale(BOOK, (1.0 + position) / (1.0 + held), self.name)]

        # part 9: with the owners module on, the trades and the gains show in who holds the claims
        if OWNED in L.extra:
            d = L.extra[OWNED]
            wanted = d + bought + position * (1.0 - 1.0 / factor)    # the trade, and the year's gain taken in shares at the new price
            new = np.minimum(1.0, np.maximum(wanted, np.minimum(d, self.block)))
            self.shift += float(((new - d) * K).sum() / K.sum())
            changes.append(Scale(OWNED, np.where(d > 0, new / np.where(d > 0, d, 1.0), 1.0), self.name))

        return changes + [
            Publish("hype_average", hype_average, self.name),
            Publish("hype_dominant", hype_dominant, self.name),
            Publish("hype_revealed", herd_revealed, self.name),
            Publish("hype_insiders", float((position[top] * K[top]).sum() / (self.bound * K[top].sum())), self.name),
            # part 7: buyers whose claims are hyped above the rest seek more
            Publish("merger_hype", (hype_dominant / hype_average) ** self.takeover, self.name),
            Publish("hype_passed_year", passed_year, self.name),
            Publish("hype_passed", self.passed, self.name),
            Publish("hype_passed_dominant", self.passed_dominant, self.name),
            Publish("hype_shift", self.shift, self.name)]
