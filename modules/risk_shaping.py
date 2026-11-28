"""Module 20: risk shaping.

THE RULE IN PLAIN WORDS

The risk term of a firm is the book's risk coefficient. It is 1 when owners are fully
confident of the earnings they expect, and larger when they are less confident. The nine
modules raise the risk of dominant capital under inflation and under resistance, and only a
merger lowers it. This module adds what the book says the largest owners do about their own
risk: they shape it, through their fusion with government organs. Nothing in the rule comes
from outside the model. The tie, the crisis and the resistance are all produced by other rules.

  1. The tie. The module measures how far dominant capital is fused with government organs
     by the part of all capitalization that the hundred largest firms hold. The tie is 0 when
     they hold nothing and 1 when they hold everything.
  2. The crisis. The level of crisis in a year is the largest of three numbers, each between
     0 and 1: unemployment above its usual level, where five points above counts as complete;
     the intensity of stagflation; and the level of systemic fear, if the eruptions module is on.
  3. The hold of the population. Government organs protect dominant capital less when popular
     resistance is high. The protection is multiplied by one minus the level of popular
     resistance.
  4. Routine protection. Each year every firm of dominant capital loses a small part of the
     amount by which its risk stands above 1. The part is a routine rate, times the tie,
     times the number of part 3. This stands for regulation, policy and stabilisation that
     the fused bodies set for themselves.
  5. Guarantees and bailouts. In a crisis every firm of dominant capital loses a further
     part of the amount by which its risk stands above 1. The part is a bailout rate, times
     the level of crisis, times the tie, times the number of part 3. No other firm receives
     this protection.
  5a. Who pays for the bailout. A bailout is a guarantee by the government, and the government
     backs it with bonds. The module works out what the guarantee is worth: the amount by
     which the bailout of part 5 raises the capitalization of dominant capital in the year.
     It publishes that amount as the government's borrowing for the bailout. Module 2 adds
     it to the government's debt in the following year. The interest on that debt is then
     paid from taxes for as long as the debt stands. When the public debt module is on, it
     collects the tax from wage earners and from firms and pays the interest to the holders
     of the debt, and the core records both sides. When it is off, module 2 only reports the
     debt, as it does for all government debt.
  5b. A guarantee is worth what the taxes behind it are worth. The public debt module
     publishes the part of last year's interest that the government was able to pay. The
     bailout of part 5 is multiplied by that part. It is 1 when every taxpayer could pay,
     and it is taken as 1 when the public debt module is off.
  6. Anger at the bailout. The module works out how far part 5 alone lowered the risk of
     dominant capital in the year, as a fall in the logarithm of the top hundred's risk. It
     publishes that fall times an anger rate. The resistance module adds the published number
     to the yearly rise of popular resistance. That is the only change to an existing module,
     and the number is 0 when this module is off. Popular resistance then weakens the next
     year's protection through part 3, and the resistance module raises the risk of dominant
     capital as it does for any rise in resistance.
  7. Readouts. The module publishes the tie, the level of crisis, the yearly fall in the risk
     of dominant capital from routine protection and from bailouts, the anger, the risk
     of dominant capital divided by the risk of all firms, and the borrowing of part 5a.

The module changes only the risk term, through Scale. The core does not let risk fall below 1.

WHAT IT RESTS ON

  - Chapter 11, "The degree of confidence". "Sometimes capitalist power is sufficiently
    secure to make capitalists certain of their strategy and the earnings it will generate;
    at other times, their power is tenuous and future predictions more hesitant. The degree
    of confidence that emerges from these considerations is expressed, inversely, by the
    'risk coefficient'. When capitalists are fully confident, [it] is 1." "Big capitalists do
    not take the odds as given; they try to change them. They struggle to increase their
    earnings and surrounding hype, and they similarly try to tame volatility. They are not
    only risk takers, they are also risk shapers." "For the large capitalists, reducing
    earning volatility is a major obsession." The same section says of the benchmark rate
    that "the absence of 'risk' here is secured by ... the government!" Parts 4 and 5 act on
    the amount by which risk stands above 1 because 1 is the book's mark of full confidence.
  - Chapter 11, "Risk and power": "earnings are a matter of power and conflict; the conflict
    over earnings invites resistance; and resistance breeds volatility and uncertainty".
    Parts 3 and 6 rest on this.
  - Chapter 12, "The rise of the modern corporation": "although incorporation certainly reduces risk, as we have
    argued in Chapter 11 and will show further in Chapter 13, risk reduction has more to do
    with power than with efficiency".
  - Chapter 15, "Differential advantage": "by making the fused entities ever larger,
    increasingly intertwined with other larger firms and government bodies, and more involved
    in setting polices and regulations, mergers stabilize earnings growth and therefore reduce
    differential risk". The footnote adds that consolidation "makes it easier for firms to
    collude as well as to fuse with government organs", and that after Standard Oil absorbed
    the independent refiners "the political-economic regime imposed by Standard Oil brought a
    more stable flow of earnings and greatly reduced risk". Part 1 makes the tie grow with
    the size of dominant capital for this reason, and part 4 is this passage.
  - Chapter 13, "Owners and technocrats", with Figure 13.1: "the volatility of the income
    share ... has declined. Given that capitalization is boosted by higher earnings and lower
    risk, the combination of these two processes attests to the extent to which the
    mega-machine of capital has strengthened its grip over society." The same chapter says:
    "capital must be seen as incorporating government power. In that sense, the government
    has become part of capital."
  - Chapter 17, postscript: "governments the world over have suspended their commitment to
    'free markets' and 'sound finance' in favour of massive bailout packages for dominant
    capital". Part 5 gives the bailout to dominant capital alone because of this sentence.
    A footnote to the same chapter reports Kalecki's view of governments as "torn between
    their need to maintain their popular legitimacy on the one hand and to protect the
    capitalist class on the other". Part 3 rests on that sentence.
  - Chapter 16, "Capitalization risk": "If the perceived increase in risk for dominant
    capital exceeds that of the business sector, the negative effect can outweigh the positive
    gain in differential earnings, causing differential capitalization to decline." And, in
    "The politics of inflation": the government "risks losing its legitimacy as a 'neutral'
    body".
  - Bichler and Nitzan, The Global Political Economy of Israel (2002), chapter 4. "When the
    crash finally came, dominant capital was bailed out by the government, whereas most of
    the less fortunate investors, including some moderately big players, realised they were
    left out". "To prevent a decumulation meltdown, the government stepped in with a massive
    bailout plan, which turned the banking stocks into government bonds". "But capitalist
    confidence was seriously shaken, and with the middle class badly hurt and no longer
    willing to hold shares, the income redistribution mechanism from labour to capital was
    beginning to crack." Chapter 1 of that book adds that "those who benefit from instability
    are often different from those who foot up the bill". Part 5a rests on the words "turned
    the banking stocks into government bonds": the bailout was paid for with public debt.
    The same passage says the bonds were "redeemable at 60 per cent of their value one week
    before the crash", so the guarantee was reckoned on the capitalization it stood behind,
    and that the stabilisation plan which followed brought "a significant wage erosion".
  - Capital as Power, chapter 13, "The government bond". The bond "marks the first systematic
    capitalization of power, namely, the power of government to tax". Parts 5a and 5b rest
    on this: what the government borrows is a right to future taxes, and it is worth what the
    taxes are worth.
  - Tim Di Muzio and Richard H. Robbins, Debt as Power (2016), chapter 1: in the contraction
    of 2007 and 2008 "the claims of capital or creditors were the first honored, even if
    that required taxpayer bailouts, or the taking of money from other public resources
    (e.g., education health and welfare) or from labor's share of the national income".
  - Bichler and Nitzan, "Systemic Fear, Modern Finance and the Future of Capitalism" (2010):
    "the broader consolidation of power relations and the establishment of capital-friendly
    regulations and macro stabilization policies helped them reduce earning volatility - and,
    by extension, their own perceptions of risk".
  - Bichler and Nitzan, "A CasP Model of the Stock Market" (2016): "The greater the power,
    the greater the resistance to power." When income volatility is already low, increasing
    power further "becomes harder and harder".
  - Bichler and Nitzan, "Can Capitalists Afford Recovery?" (2014): "if we take volatility as
    a proxy for risk, we would conclude that the risk facing capitalists has declined".
  - Sandy Brian Hager, "Corporate Ownership of the Public Debt" (2015): in the crisis after
    2007 "it is overwhelmingly large corporations at the top of the business hierarchy that
    have enjoyed the current 'flight to safety'" into federal bonds.

WHAT IS ADDED

The literature says that large owners shape their risk, that they do it through size and
through fusion with government, that bailouts go to dominant capital, and that power meets
resistance. It gives no rule and no rate. The whole form of the rule is therefore an
addition, and every number in it is an addition. Measuring the tie by the top hundred's part
of all capitalization is an addition. The debt module uses the same figure for the part of
the public debt that dominant capital holds. Reckoning crisis from unemployment, the
intensity of stagflation and systemic fear is an addition. The literature contains no
sentence that says bailouts raise popular resistance. Part 6 applies the general statements
about power and resistance to bailouts, and it is the least supported part of the rule.

On part 5a, the literature says that the government pays
for a bailout with bonds and that taxpayers and wage earners bear it. It gives no rule for
the amount. Taking the amount to be the rise in capitalization that the bailout brings is an
addition. It uses no number. Leaving the bailout debt standing for ever is an addition: the
Israeli bonds ran for five years. Part 5b is an addition with no passage of its own.

WHAT IS MISSING

The bailout debt is never redeemed. With the public debt module off, nobody is taxed for
it and it is only reported. The rule does not pass risk on to smaller firms, although the Israeli case suggests that smaller
owners were left with the losses. The rule protects all hundred firms alike, and holds no
single firm to be more closely tied to government than another. The rule lowers the risk
coefficient directly. It does not lower the year-to-year variation of earnings, which is what
Figure 13.1 measures.
"""
import numpy as np
from core import Scale, Publish, top_positions


class RiskShaping:
    name = "risk shaping"
    reads = ("unemployment",)
    supplies = ("government_tie", "crisis_level", "risk_relief_routine", "risk_relief_bailout",
                "protection_anger", "risk_differential", "bailout_borrowing")
    figures = {                   # what the workbench calls each published number: label, unit, note
        'government_tie': ('Tie to government', 'share', "Measured as the top 100's part of all capitalization."),
        "crisis_level": ("Level of crisis", "index", ""),
        'risk_relief_routine': ('Risk relief from routine protection', 'rate', "Yearly fall in the top 100's risk from routine protection, on a log scale."),
        'risk_relief_bailout': ('Risk relief from bailouts', 'rate', "Yearly fall in the top 100's risk from bailouts, on a log scale."),
        "protection_anger": ("Anger at bailouts", "number", "Rise in popular resistance caused by bailouts."),
        "risk_differential": ("Differential risk", "times", "Risk of the top 100 divided by the risk of all firms."),
        "bailout_borrowing": ("Bailout borrowing", "number", "What the government borrows to bail out the top 100, in money."),
    }

    def __init__(self, routine=0.05, bailout=0.5, anger=1.0, usual_unemployment=0.05,
                 crisis_span=0.05, top=100):
        self.routine = routine     # yearly part of a dominant firm's risk above 1 that routine protection removes, at a complete tie and with no resistance (addition)
        self.bailout = bailout     # further yearly part removed in a complete crisis, at a complete tie and with no resistance (addition)
        self.anger = anger         # rise in popular resistance per unit fall in the logarithm of dominant capital's risk that bailouts bring (addition)
        self.usual_unemployment = usual_unemployment   # unemployment that counts as no crisis; the same setting as in the resistance module (addition)
        self.crisis_span = crisis_span   # points of unemployment above the usual level that count as a complete crisis; copied from the consensus compass (addition)
        self.top = top             # the number of firms counted as dominant capital, as in the book

    def start(self, L):
        return {"government_tie": 0.0, "crisis_level": 0.0, "risk_relief_routine": 0.0,
                "risk_relief_bailout": 0.0, "protection_anger": 0.0, "risk_differential": 1.0,
                "bailout_borrowing": 0.0}

    @staticmethod
    def _risk(EH, d, idx):
        """The risk of a group of firms, reckoned as the core's readouts reckon it."""
        return EH[idx].sum() / (EH[idx] / d[idx]).sum()

    def propose(self, L, rng):
        A = L.accounts
        K, d = L.cap(), L.d
        top = top_positions(K, np.arange(len(L)), self.top)
        EH = L.earnings() * L.h

        # part 1: the tie is dominant capital's part of all capitalization
        tie = float(K[top].sum() / K.sum())
        # part 2: the crises that the model itself produces
        slack = (A["unemployment"] - self.usual_unemployment) / self.crisis_span
        crisis = float(np.clip(max(slack, A.get("stagflation_intensity", 0.0),
                                   A.get("systemic_fear", 0.0)), 0.0, 1.0))
        # part 3: popular resistance limits what government organs can grant
        allowed = 1.0 - min(1.0, max(0.0, A.get("resistance", 0.0)))

        # parts 4 and 5: the parts of the risk above 1 that are removed
        cut_routine = min(1.0, self.routine * tie * allowed)
        # part 5b: a guarantee is worth what the taxes behind it are worth (1 without the public debt module)
        backed = float(np.clip(A.get("public_debt_service", 1.0), 0.0, 1.0))
        cut_bailout = min(1.0 - cut_routine, self.bailout * crisis * tie * allowed * backed)
        excess = d[top] - 1.0
        after_routine, after_bailout, after_both = d.copy(), d.copy(), d.copy()
        after_routine[top] = 1.0 + excess * (1.0 - cut_routine)
        after_bailout[top] = 1.0 + excess * (1.0 - cut_bailout)
        after_both[top] = 1.0 + excess * (1.0 - cut_routine - cut_bailout)

        before = self._risk(EH, d, top)
        relief_routine = float(np.log(before / self._risk(EH, after_routine, top)))
        relief_bailout = float(np.log(before / self._risk(EH, after_bailout, top)))
        everyone = np.arange(len(L))
        # part 5a: what the guarantee is worth is the capitalization it adds; the government borrows that much
        borrowing = float((K[top] * (d[top] / after_both[top] - d[top] / after_routine[top])).sum())

        changes = [Publish("government_tie", tie, self.name),
                   Publish("crisis_level", crisis, self.name),
                   Publish("risk_relief_routine", relief_routine, self.name),
                   Publish("risk_relief_bailout", relief_bailout, self.name),
                   # part 6: the bailout is seen, and it is resented
                   Publish("protection_anger", self.anger * relief_bailout, self.name),
                   Publish("risk_differential", float(before / self._risk(EH, d, everyone)), self.name),
                   Publish("bailout_borrowing", borrowing, self.name)]      # read by module 2, which adds it to the government's debt
        if cut_routine + cut_bailout > 0:
            changes.append(Scale("risk", after_both / d, self.name))
        return changes
