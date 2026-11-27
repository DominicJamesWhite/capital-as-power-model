"""Optional module: protections as barred entry.

THE RULE IN PLAIN WORDS

A protection is a patent, a copyright, a licence, a concession or an exclusive contract. It is
a right, enforced by government organs, to keep others out. A claim that holds one sells at a
markup above the markup of its unprotected neighbours, and others are kept from entering beside
it. The module holds no knowledge, no invention and no productivity. It holds only the
protection, which is the thing the book says is capitalized.

  1. The tie. Each claim has a tie to government organs, between 0 and 1. The tie grows with
     the claim's capitalization measured against the average claim. A claim of average size
     has a tie near 0.01. A claim one hundred times the average has a tie of one half.
  2. Grants. Each year a claim that holds no protection obtains one with a small probability.
     The probability has a part that every claim has and a part in proportion to the tie.
     A protection is granted for fifteen years.
  3. What a protection does to the markup. The module owns one markup component, the
     protection premium. Each year it sets the premium of a protected claim to a fixed number
     above 1 and the premium of every other claim to 1. The premium multiplies the claim's
     own markup, and the module changes nothing else in a claim's earnings. The premium is a
     member of the overlap group "hold on buyers", together with the premiums of the price
     leaders and wants modules (see "How modules share a quantity" in modules.md). The price
     of the claim moves with its markup, and the wage does not. In the year of the grant the
     claim gives up employees in proportion to the rise of its price. (Before 26 November
     2026 the module set the whole markup of a protected claim to the markup of the
     unprotected claims of its industry times the fixed number.)
  4. What a protection does to entry. The module publishes, for each industry, the part of
     the industry that is not under protection. The part under protection is the protected
     claims' part of the industry's employees. The green-field module founds fewer new claims
     in proportion, and the sabotage module allows less of the extra hiring that a high markup
     would otherwise bring. These are two optional reads, and the number is 1 when this module
     is off.
  5. Lapse and renewal. When the fifteen years are over, the protection is renewed for
     another fifteen with a probability equal to the claim's tie. Otherwise it lapses. The
     premium of a claim whose protection lapses returns at once to 1.
  6. Enforcement. A protection is worth what its enforcement is worth. The excess markup of
     part 3 and the bar of part 4 are both multiplied by one minus the level of popular
     resistance.
  7. Readouts. The module publishes the part of all employees that works for protected
     claims, the part of the hundred largest claims that hold a protection, the average tie
     of the hundred largest, the markup of protected claims against their unprotected
     neighbours as it stood at the start of the year, and the numbers of grants, renewals
     and lapses.

The years a claim's protection has left are kept as an added number on the claim. In a merger
the buyer keeps its own number, so a protected buyer extends its protection over what it buys
and the protection of an acquired claim ends.

WHAT IT RESTS ON

  - Chapter 12, "Immaterial assets". "The real issue is not whether Microsoft's knowledge
    'originates' inside or outside the company, but whether that knowledge - whatever its
    source - can be protected. Note that on its books, Microsoft - like any other corporation
    - capitalizes not the invention itself, but the patent or copyright that defends it. And
    by now the reason shouldn't be surprising: unless the innovation is protected, everyone
    can use it, and what everyone can use nobody can profit from. Conclusion: a corporation -
    no matter how 'innovative' it claims to be - can only capitalize the protection of
    knowledge, never the knowledge itself." Part 3 gives the excess markup to the protection
    and to nothing else.
  - Chapter 12, "The differential underpinnings of universal sabotage". "For the profits of one
    owner (or a coalition of owners) to beat the average, others must be prevented from
    accessing the same earnings." The means "include direct limitations, such as predatory
    pricing, formal and informal collusion, advertising and exclusive contracts. They also
    include broader strategies like targeted education, patent and copyright laws, industrial
    policies, financial regulations, preferential tax treatment, legal monopolies". "For the
    benefiting owner, the differential gain accrues because the necessary industrial
    limitation is borne by other owners." And: "when exclusion cannot be ensured, like in the
    case of software development or the manufacturing of microchips, soaring production often
    overshoots into excess capacity and falling profits". Part 4 rests on these sentences.
  - Chapter 13, "Government capitalized". "The owners of Microsoft can profit differentially
    from this software only insofar as they can prevent others from using it without pay. And
    this prevention depends crucially on the existence and enforcement of intellectual
    property rights - that is, on the extent to which Microsoft can harness the government
    apparatus to its own end. Now negate this ability and assume that the government no longer
    protects Microsoft's software. The most likely result is that Microsoft's earnings and
    capitalization will drop sharply if not collapse altogether. The magnitude of the drop
    represents the extent to which Microsoft capitalizes the government." Part 5 is this
    thought experiment made into a yearly possibility. The footnote adds that Microsoft earns
    most of its profit where "software piracy can cost the trespasser up to five years in
    jail", and that elsewhere the governments' "contribution to Microsoft's bottom line is
    likely to remain negligible". Part 6 rests on the footnote.
  - Chapter 9. Businesses "dealing with patents and copyrights depend on the enforcement of
    intellectual property rights, and in that sense capitalize both the law and the extent to
    which it is enforced".
  - Chapter 16, "Cost cutting". "Unlike final commodities that can often be protected through
    patents, copyrights and other exclusionary threats, improvements in the social
    organization of production tend to proliferate easily, and this rapid spread quickly
    dilutes the initial advantage of whoever implemented them first." The cost cutting module
    already wears down any difference between a claim and its industry. A protection is what
    stands against that wear.
  - Chapter 14. "The fact that a certain corporation was granted a patent, that it had the
    government move to its side ... cannot, in and of itself, tell us much about that
    company's rate of differential accumulation." "In principle there is nothing to prevent
    ... a university dropout from incorporating Microsoft." Part 2 therefore lets a small
    claim obtain a protection, and the module does not promise that a protected claim gains
    against the average.
  - Chapter 15, footnote to "Differential advantage": consolidation "makes it easier for
    firms to collude as well as to fuse with government organs". Part 1 makes the tie grow
    with size for this reason.
  - Bichler and Nitzan, The Global Political Economy of Israel (2002). In the 1950s the
    government worked "through the selective handout of exclusive concessions, certificates
    and licences", and "these property rights quickly turned into gold mines for those lucky
    enough to get them". In the financial sector "the core groups reigned supreme, with a
    government 'licence' against domestic competition". In the 1990s the cable companies
    fought "to renew their exclusive free licence to deliver cable services for another 15
    years" and "to extend this licence into internet and telephone services", each side
    working through its own minister. The term of fifteen years is this figure. On patents:
    "if technology advances in leaps and bounds, but its protection consolidates even faster,
    the result would be fatter margins", and of all innovations "only a fraction could be
    'protected' by intellectual property rights".
  - Bichler and Nitzan, "Dominant Capital and the New Wars" (2004). Microsoft's profit and
    capitalization "were entirely dependent on intellectual property rights, on the state
    sanction that backed up these rights, and on Microsoft's ability to harness this sanction
    to its own differential ends". "The only barrier preventing this latter act is the law."
  - Baines and Hager, "Rentiership and Intellectual Monopoly in Contemporary Capitalism"
    (2023). "Without the legal protection that patents provide to make their products
    artificially scarce, the rents of pharmaceutical companies would quickly evaporate." The
    top tenth of pharmaceutical firms "record the highest profit margins of any company
    grouping in this study", and the bottom half record "by far the lowest".

WHAT IS ADDED

The literature says that a protection is what is capitalized, that it works by exclusion,
that it depends on enforcement by government organs, and that earnings collapse when it is
withdrawn. It gives no rule and no rate for who obtains a protection, for how much a
protection raises a markup, or for how often one is renewed. The form of every part is
therefore an addition. Every number is an addition except the term of fifteen years, which is
the term of one Israeli cable licence applied to every protection. Measuring a claim's tie by
its size against the average claim is an addition. Letting popular resistance weaken
enforcement is an addition; the same form is used for the hold of dominant capital in the
sabotage module. Measuring the bar on entry by the protected claims' part of the industry's
employees is an addition.

WHAT IS MISSING

A protection does not lower the risk of its holder, although chapter 13 says that government
power bears on "earnings and risk". The rule has no contest between rival claims over a grant
or a renewal, although the Israeli cable case is such a contest. A dominant claim cannot buy a
small claim in order to take over its protection, although the 2002 book describes this,
because the core lets a buyer keep only its own added numbers. All protections are alike in
strength and term. Protections do not differ between countries, because the model has one.
"""
import numpy as np
from core import Scale, SetComponent, Publish, top_positions, HOLD_ON_BUYERS

PREMIUM = "protection premium"    # this module's markup component; a member of the overlap group "hold on buyers" (an addition)


class Protections:
    name = "protections"
    reads = ()
    supplies = ("protection_open", "protected_share", "protected_top", "protection_tie_top",
                "protection_premium", "protection_grants", "protection_renewals", "protection_lapses")

    def __init__(self, premium=0.5, term=15, grant_any=0.002, grant_tied=0.10, renew=1.0,
                 tie_size=100.0, bar=1.0, volume_cost=0.5, top=100, against="own"):
        self.premium = premium        # excess of a protected claim's markup over what its markup would be without the protection, as a fraction
                                      # of that, under full enforcement (0.5 means one and a half times) (addition)
        self.term = int(term)         # years a protection lasts. The value is an addition: fifteen years is the renewal that the Israeli cable companies sought for one licence in Bichler and Nitzan (2002), which is one case, and the literature gives no general term
        self.grant_any = grant_any    # yearly probability that any unprotected claim obtains a protection, whatever its tie (addition)
        self.grant_tied = grant_tied  # further yearly probability at a complete tie to government organs (addition)
        self.renew = renew            # probability that a lapsing protection is renewed, at a complete tie (addition)
        self.tie_size = tie_size      # capitalization, in multiples of the average claim's, at which a claim's tie is one half (addition)
        self.bar = bar                # part of entry that is barred in an industry wholly under protection, under full enforcement (addition)
        self.volume_cost = volume_cost  # employees given up per unit of price rise in the year of the grant
                                        # (the same figure as the cost of a price rise in the sabotage module) (addition)
        self.top = top                # the number of claims counted as dominant capital, as in the book
        if against not in ("own", "neighbours"):
            raise ValueError("protections: against must be 'own' or 'neighbours'")
        self.against = against        # what the premium is reckoned against (addition; item 34 of backlog.md).
                                      # "own": the premium multiplies the claim's own markup, so a protected claim keeps
                                      # its own cost-cutting edge and its own lead from price rises. "neighbours" is kept
                                      # for comparisons: the premium is set so that the stacking part of the claim's
                                      # markup, times the premium, is one plus the setting times the average stacking
                                      # markup of the unprotected claims of its industry.

    ATTRIBUTE = "protection_years"    # one plus the years of protection a claim has left; 1 means no protection

    def start(self, L):
        L.add_attribute(self.ATTRIBUTE, 1.0, 1.0)      # nobody holds a protection at the start
        L.add_component(PREMIUM, self.name, group=HOLD_ON_BUYERS)
        return {"protection_open": np.ones(L.sector_of.size), "protected_share": 0.0, "protected_top": 0.0,
                "protection_tie_top": 0.0, "protection_premium": 1.0, "protection_grants": 0.0,
                "protection_renewals": 0.0, "protection_lapses": 0.0}

    def propose(self, L, rng):
        A = L.accounts
        k, ind, n = L.sector_of.size, L.ind, L.n
        count = len(L)
        stored = L.extra[self.ATTRIBUTE]
        years = np.rint(stored - 1.0)                  # years left, counting this year
        holds = years >= 1
        K = L.cap()

        # part 1: the tie grows with size against the average claim
        tie = K / (K + self.tie_size * K.mean())
        # part 6: popular resistance weakens enforcement
        enforced = 1.0 - min(1.0, max(0.0, A.get("resistance", 0.0)))

        # parts 2 and 5: grants, renewals and lapses, each drawn for every claim so that the
        # draws do not depend on who holds what
        draw_grant, draw_renew = rng.random(count), rng.random(count)
        granted = ~holds & (draw_grant < self.grant_any + self.grant_tied * tie)
        ending = holds & (years <= 1)
        renewed = ending & (draw_renew < self.renew * tie)
        lapsed = ending & ~renewed
        protected = (holds & ~lapsed) | granted        # claims that hold a protection through this year
        new_years = np.where(granted | renewed, float(self.term),
                             np.where(lapsed, 0.0, np.where(holds, years - 1.0, 0.0)))

        # part 3: the markup of a protected claim against its unprotected neighbours
        m = L.markup()
        n_j = np.bincount(ind, n, k)
        free_n = np.bincount(ind[~holds], n[~holds], k)
        free_m = np.bincount(ind[~holds], (n * m)[~holds], k)
        every_m = np.bincount(ind, n * m, k) / np.maximum(n_j, 1e-12)
        ref = np.where(free_n > 0, free_m / np.maximum(free_n, 1e-12), every_m)[ind]
        # The module sets its own component and nothing else: the premium of a protected claim is
        # one plus the setting, under full enforcement, and the premium of every other claim is 1.
        # A lapse returns the premium to 1.
        value = np.where(protected, 1.0 + self.premium * enforced, 1.0)
        if self.against == "neighbours":               # for comparisons: the rule as it stood before the named components
            r = L.stacking_markup()                    # reckoned on the stacking part, so no other hold on buyers is read
            free_r = np.bincount(ind[~holds], (n * r)[~holds], k)
            every_r = np.bincount(ind, n * r, k) / np.maximum(n_j, 1e-12)
            ref_r = np.where(free_n > 0, free_r / np.maximum(free_n, 1e-12), every_r)[ind]
            value = np.where(protected, value * ref_r / r, 1.0)
        new = L.markup_with(PREMIUM, value)            # the claim's markup if nothing else changed
        price = (1.0 + new) / (1.0 + m)
        # "the specific level at which they set the price already embodies the power to incapacitate"
        gives_up = np.where(granted, self.volume_cost * np.maximum(price - 1.0, 0.0), 0.0)

        # part 4: the part of each industry that is not under protection
        covered = np.bincount(ind[protected], n[protected], k) / np.maximum(n_j, 1e-12)
        open_part = 1.0 - np.clip(self.bar * enforced * covered, 0.0, 1.0)

        top = top_positions(K, np.arange(count), self.top)
        was = holds & (ref > 0)
        premium_now = float((n[was] * m[was] / ref[was]).sum() / n[was].sum()) if was.any() else 1.0
        changes = [Publish("protection_open", open_part, self.name),
                   Publish("protected_share", float(n[protected].sum() / n.sum()), self.name),
                   Publish("protected_top", float(protected[top].mean()), self.name),
                   Publish("protection_tie_top", float(tie[top].mean()), self.name),
                   Publish("protection_premium", premium_now, self.name),
                   Publish("protection_grants", float(granted.sum()), self.name),
                   Publish("protection_renewals", float(renewed.sum()), self.name),
                   Publish("protection_lapses", float(lapsed.sum()), self.name)]
        if protected.any() or lapsed.any():
            changes += [SetComponent(PREMIUM, value, self.name),   # the price follows: the core works it out
                        Scale(self.ATTRIBUTE, (1.0 + new_years) / stored, self.name)]
            if gives_up.any():
                changes.append(Scale("employees", 1.0 - gives_up, self.name))
        return changes
