"""Optional module: energy capture and hierarchy (a physical account kept beside the ledger).

THE RULE IN PLAIN WORDS

The ledger counts firms in money. This module keeps a second account, in joules, of the
energy the society converts in a year. It divides that energy into two flows, as "Growing
Through Sabotage" (2020) does: hierarchical energy, which is used to impose and sustain
hierarchical power, and livelihood energy, which is everything else. It reports the part of
all energy that goes to hierarchy, which the paper writes as H. Energy never enters a price, a
markup, earnings or capitalization. The module proposes no change to any firm.

  1. Energy captured. The energy that one employee converts in a year depends on the size of
     the firm the employee works in. It is 14.3 gigajoules times the number of employees of
     that firm raised to the power 1.02. A gigajoule is one billion joules. The formula is
     Blair Fix's printed regression of energy use per head on the average size of firms,
     applied here to each firm. The energy of a firm is that figure times its employees,
     and the energy of the society is the sum over firms. People without work convert
     nothing in this account, so unemployment lowers the energy captured per head. The
     formula is not carried beyond a size of 3,000 employees: a larger firm converts per
     employee what a firm of 3,000 converts.
  2. The ranks of a firm. Every firm is a chain of command with the same span of control,
     which is the number of people in one rank divided by the number in the rank above (Fix
     2017, appendix H). The people in the third rank from the bottom and above are counted as
     managers, as Fix counts them. Their part of the firm's employees is the command part.
     It is zero in a firm too small to have three ranks, and it approaches one divided by
     the square of the span in a very large firm.
  3. Energy for command. The command part of a firm's energy is hierarchical energy.
  4. Energy for containing resistance. Resistance raises the energy that a given hierarchy
     needs. The energy for command is multiplied by one plus the level of popular resistance
     times a setting.
  5. Energy for organised force. If the organised force module is on, the energy converted
     in military jobs is hierarchical energy as well. The part of it that parts 3 and 4
     already counted is not counted twice.
  6. The two flows. Hierarchical energy is the sum of parts 3 to 5. Livelihood energy is all
     energy less hierarchical energy. The hierarchical share H is hierarchical energy divided
     by all energy (the paper's equation 2). All three flows are reported in gigajoules per
     member of the working population per year, and the total is reported in joules.
  7. The trajectory. The module compares H, livelihood energy per head and all energy per
     head with their values five years earlier, and names the trajectory with the paper's
     own table: expanding (H and livelihood energy both rise), in crisis (H rises and
     livelihood energy falls), in decline (both fall), or democratizing (H falls and
     livelihood energy rises). Crisis and democratization each have two paths, one with more
     energy per head in all and one with less.
  8. Grievance. When livelihood energy per head falls from one year to the next, the module
     publishes a number in proportion to the fall. The resistance module adds that number to
     the year's rise in popular resistance. This is the only thing in the model that reads
     the energy account. It acts on resistance and not on any price or any earnings. With the
     setting at zero the module is a readout and nothing else in a run changes.
  9. Readouts, published every year and measured at the start of the year:
       energy_total_joules         all energy converted in the year, in joules
       energy_per_head             all energy, gigajoules per member of the working population
       energy_hierarchy_per_head   hierarchical energy, the same unit
       energy_livelihood_per_head  livelihood energy, the same unit
       energy_hierarchy_share      H: hierarchical energy as a part of all energy
       energy_dominant_share       part of all energy converted inside the hundred largest firms
       energy_dominant_hierarchy   part of all hierarchical energy used inside those firms
       energy_trajectory           the name of the trajectory (part 7)
       energy_trajectory_code      the same as a number: 1 expanding, 2 tentative crisis,
                                   3 full crisis, 4 decline, 5 democratizing with more energy,
                                   6 democratizing with less energy, 0 not yet known
       energy_grievance            the number of part 8

WHAT IT RESTS ON

  - Bichler and Nitzan, "Growing Through Sabotage: Energizing Hierarchical Power" (2020).
    Section 9.2: "Our starting point
    in modelling the relationship between energy conversion and hierarchy formation is to
    split the total energy captured/converted by society into two distinct flows: (1)
    hierarchical energy that serves to impose, sustain and augment hierarchical power, and
    (2) livelihood energy that provides for subsistence and wellbeing." Section 10 defines E,
    HE, LE and H in gigajoules per head per year, with "HE + LE = E" and equation 2,
    "H = (E - LE) / E". Part 6 is that equation.
  - The same paper, section 9.1, point 4: "Since the exertion of hierarchical power against
    opposition necessitates strategic sabotage, and because sabotage requires energy to be
    carried out, hierarchical structures, regardless of their specific purpose, consume
    energy. Everything else being the same, the more hierarchical the institution or
    organization, the greater the energy needed simply to erect and sustain it." Part 3.
  - The same paper, section 8.1: these activities "consume a significant portion of society's
    energy. They imply standing armies, organized religion, education and conditioning, a
    legal system, various bureaucracies, police forces, ongoing propaganda". Section 11.1:
    "greater resistance tends to require more energy to sustain any given level of
    hierarchy". Footnote 32: "overcoming this resistance requires energy over and above that
    consumed by the higher strata of the hierarchies". Parts 4 and 5.
  - The same paper, section 11 and its Table 2, for the four trajectories of part 7, and
    section 11.2 for part 8: "as long as livelihood energy per capita is rising (Trajectory
    A), most subjects remain busy with their daily lives, paying little or no attention to
    expanding power, rising hierarchy and growing sabotage. But when livelihood energy per
    capita comes to a standstill (movement on the hec), the conflict between the two groups
    suddenly sharpens into focus; and when livelihood energy actually drops (Trajectory B1),
    the clash between wellbeing and hierarchical power comes to the fore."
  - The same paper, section 12.4, for why the account reports one flow as a level and the
    other as a share: livelihood energy is measured in an absolute yardstick ("more joules"),
    hierarchical energy in a relative one ("a greater decimal share of total energy").
  - Blair Fix, "Energy and Institution Size" (PLoS ONE, 2017),
    record 500 of the authors' archive. "As
    energy use per capita increases: 1. The small firm employment share declines; 2. The
    large firm employment share increases; 3. The mean firm size increases; 4. The government
    employment share increases." The caption of his Figure 19 prints the regression of his
    Figure 1C: "The formula is Epc = 14.3 L^1.02, where Epc is energy per capita and L is
    mean firm size." Energy is in gigajoules per head per year. His Figure 3 adds sectors
    and sub-sectors of United States industry, where "energy use is measured per worker", and
    he reports that this "serves to extend (by two orders of magnitude) the trends found at
    the national level". The 2020 paper sums up his finding as a statement about single
    organisations: "larger organizations are able to capture (and also tend to consume) more
    energy per capita than smaller ones". Part 1 applies the national formula to each firm
    on these grounds.
  - The same paper, section 4.3 and appendix H, for part 2: "All firms are 'ideal'
    hierarchies with a single span of control." "All individuals in and above the third
    hierarchical level are considered 'managers'." "If the span of control is s, then the
    asymptote occurs at 1/s2". The number of ranks is his equation 34, the bottom rank his
    equation 37, and the managers' part his equation 28.
  - Blair Fix, "Putting Power Back Into Growth Theory" (Review of Capital as Power, 2015),
    record 444 of the authors' archive. It reports "a clear
    connection (across both space and time) between corporate employment concentration and
    energy consumption per capita", and it takes the employment share of the largest
    corporations as its measure of hierarchy, "inspired by Nitzan and Bichler's (2009)
    concept of 'breadth'".
  - Why energy sets no price here. The 2020 paper, section 9.4, says of utility and labour
    time that "the very idea that a conflictual society can be understood with a single
    universal measure is an invitation for trouble", and that two languages are needed, "a
    conflictual language for power and hierarchy, and a cooperative one for subsistence and
    livelihood". A joule that set earnings would be one more universal measure. Section 9.2
    adds that the split itself "is bound to be coloured by our political, ideological and
    theoretical disposition". The account is therefore kept beside the money ledger.

WHAT IS ADDED

The 2020 paper gives the two flows, the share H, the four trajectories and the statement that
hierarchy and the containing of resistance use energy. It gives no rule for measuring either
flow, and says that the split depends on the observer. Fix gives one printed formula, for
whole countries. Everything else is added:
  - Applying Fix's formula to each firm. Fix estimated it on the average size of firms in
    whole countries. He shows that sectors lie on the same trend, and he prints no formula
    for sectors or for single firms. Two other ways of applying it do not work here. Applied
    to the average firm of the whole ledger, the formula makes energy per head fall over
    the years, because the model founds many small firms. Applied to the average firm of
    each industry, it makes energy per head rise without limit when there is no limit on
    size, and it makes energy fall whenever small firms are founded.
  - The limit of 3,000 employees on the size the formula is applied to. Fix's national data
    end at a few tens of employees and his sector data reach two orders of magnitude
    further. The number is a reading of that statement and not a printed figure.
  - Counting people without work as converting no energy.
  - Counting the managers' part of a firm's energy as hierarchical energy. Fix uses the
    managers' part of employment as a sign of hierarchy and does not turn it into energy.
  - The span of control of 2.5. Fix draws his fitted spans in a chart and prints no figure.
    He uses spans between 2 and 3 in the appendix that prints the formula of part 1.
  - The doubling of the energy for command at full resistance, the five years of part 7, and
    the rate of part 8. The form of parts 4, 5 and 8 is also added.
  - The observer. The rule takes a narrow view of hierarchical energy, between the ruler and
    the social democrat of the paper's Figure 6. The paper says that the trajectories, and
    not the levels, are what all observers can agree on.

WHAT IS MISSING

The paper's central claim about limits is not built: "the size and height of hierarchical
institutions are capped by their ability to capture energy". Nothing in this module holds a
merger back for want of energy, because the literature gives no rule for how much energy can
be had. The reverse firm, that too much hierarchy lowers the energy captured, appears only
through unemployment. The ledger holds no government organs, so the government employment
that Fix measures is absent, and so are the churches, schools, courts and police the paper
lists. The self-employed and businesses that are not corporations are not in the ledger
either, so the average size of a firm is far above the average size of a firm in Fix's data
and the level of energy per head is too high. Propaganda is not counted, although the
optional module on the shaping of wants holds a money outlay for it, because turning money
into joules would need a price of energy. The hierarchies that the paper places outside
formal organisations, in markets and networks, are not counted. The energy lost in
conversion is not kept apart. The rulers do not respond to the share H, although the paper
says it is the yardstick they care about.
"""
import numpy as np
from core import Publish, top_positions

GIGAJOULE = 1e9     # joules in one gigajoule

TRAJECTORIES = {0: "not yet known", 1: "expanding", 2: "tentative crisis", 3: "full crisis",
                4: "decline", 5: "democratizing with more energy", 6: "democratizing with less energy"}


class Energy:
    name = "energy"
    reads = ()
    supplies = ("energy_total_joules", "energy_per_head", "energy_hierarchy_per_head",
                "energy_livelihood_per_head", "energy_hierarchy_share", "energy_dominant_share",
                "energy_dominant_hierarchy", "energy_trajectory", "energy_trajectory_code",
                "energy_grievance")
    figures = {                   # what the workbench calls each published number: label, unit, note
        "energy_total_joules": ("Energy converted", "number", "All energy converted in the year, in joules."),
        "energy_per_head": ("Energy per head", "number", "Gigajoules per member of the working population."),
        "energy_hierarchy_per_head": ("Hierarchical energy per head", "number", "Gigajoules per member of the working population."),
        "energy_livelihood_per_head": ("Livelihood energy per head", "number", "Gigajoules per member of the working population."),
        "energy_hierarchy_share": ("Hierarchical energy share", "share", "Hierarchical energy as a part of all energy."),
        "energy_dominant_share": ("Energy used by the top 100", "share", "Part of all energy converted inside the top 100."),
        "energy_dominant_hierarchy": ("Hierarchical energy used by the top 100", "share", "Part of all hierarchical energy used inside the top 100."),
        "energy_trajectory_code": ("Energy trajectory", "number", "1 expanding, 2 tentative crisis, 3 full crisis, 4 decline, 5 and 6 democratizing, 0 not yet known."),
        "energy_grievance": ("Grievance from energy", "number", "Published when livelihood energy per head falls."),
    }

    def __init__(self, coefficient=14.3, exponent=1.02, largest_size=3000.0, span=2.5,
                 managers_from=3, containment=1.0, window=5, grievance=0.5, top=100):
        self.coefficient = coefficient        # gigajoules per head per year where the average firm has one member (Fix 2017, caption of Figure 19: Epc = 14.3 L^1.02); its use here is an addition: Fix fitted the formula to the average size of firms in whole countries, and the rule applies it to each single firm
        self.exponent = exponent              # power of the average size of firms in the same printed formula; its use on single firms is the same addition
        self.largest_size = largest_size      # the largest number of employees the formula is applied to; a larger firm converts per employee what a firm of this size converts; an addition, read from Fix's statement that sector data reach two orders of magnitude beyond national data
        self.span = span                      # people in one rank divided by people in the rank above, the same in every firm (Fix 2017, appendix H); 2.5 is an addition, the middle of the 2 to 3 he uses in appendix I
        self.managers_from = managers_from    # the rank, counted from the bottom, from which people count as managers; Fix 2017 uses the third
        self.containment = containment        # extra energy for command at full popular resistance, as a multiple of the energy for command; an addition
        self.window = window                  # years over which the trajectory is judged; an addition
        self.grievance = grievance            # rise in popular resistance per unit of yearly fall in livelihood energy per head (a fall of 10 per cent adds 0.05); an addition; 0 makes the module a pure readout
        self.top = top                        # the number of largest firms that stands for dominant capital
        if span <= 1.0:
            raise ValueError("each rank must hold fewer people than the rank below it")
        if (1 + containment) / span ** (managers_from - 1) >= 1.0:
            raise ValueError("hierarchical energy would reach all energy at full resistance")
        self.past = []                        # (H, livelihood energy per head, all energy per head) of earlier years

    # ------------------------------------------------------------------ pieces of the rule

    def command_part(self, employees):
        """Part 2: the managers' part of each firm's employees (Fix 2017, equations 28 and 34)."""
        s, m = self.span, self.managers_from
        size = np.maximum(np.asarray(employees, dtype=float), 0.0)
        ranks = np.maximum(np.rint(np.log1p(size * (s - 1)) / np.log(s)), 1.0)      # equation 34
        part = (s ** (1.0 - m) - s ** (-ranks)) / (1.0 - s ** (-ranks))             # equation 28, counted from the bottom rank
        return np.where(ranks >= m, part, 0.0)

    def measure(self, L):
        """The energy account of the ledger as it stands. Flows are in gigajoules per year."""
        A = L.accounts
        size = np.clip(L.n, 1.0, self.largest_size)                                # an organisation has at least one member
        energy = L.n * self.coefficient * size ** self.exponent                    # part 1
        total = energy.sum()
        need = 1.0 + self.containment * min(1.0, max(0.0, A.get("resistance", 0.0)))   # part 4
        hierarchical = energy * self.command_part(L.n) * need                        # parts 3 and 4
        H = hierarchical.sum() / total
        # part 5: military jobs (optional organised force module; 0 without it), less what is already counted
        military = A.get("force_jobs", 0.0) * L.shared["workforce"] * total / L.n.sum()
        force = military * (1.0 - H)
        H = (hierarchical.sum() + force) / total
        heads = L.shared["workforce"]
        dominant = top_positions(L.cap(), np.arange(len(L)), self.top)
        return {"total": total, "per_head": total / heads, "H": H,
                "hierarchy_per_head": H * total / heads, "livelihood_per_head": (1.0 - H) * total / heads,
                "dominant_share": energy[dominant].sum() / total,
                "dominant_hierarchy": hierarchical[dominant].sum() / max(H * total, 1e-300)}

    def trajectory(self, now):
        """Part 7: the paper's Table 2, from the change over the window."""
        if not self.past:
            return 0
        H0, LE0, E0 = self.past[-self.window] if len(self.past) >= self.window else self.past[0]
        H_up, LE_up, E_up = now["H"] >= H0, now["livelihood_per_head"] >= LE0, now["per_head"] >= E0
        if H_up and LE_up:
            return 1
        if H_up:
            return 2 if E_up else 3
        if not LE_up:
            return 4
        return 5 if E_up else 6

    def accounts(self, now, code, grievance):
        return {"energy_total_joules": float(now["total"] * GIGAJOULE),
                "energy_per_head": float(now["per_head"]),
                "energy_hierarchy_per_head": float(now["hierarchy_per_head"]),
                "energy_livelihood_per_head": float(now["livelihood_per_head"]),
                "energy_hierarchy_share": float(now["H"]),
                "energy_dominant_share": float(now["dominant_share"]),
                "energy_dominant_hierarchy": float(now["dominant_hierarchy"]),
                "energy_trajectory": TRAJECTORIES[code],
                "energy_trajectory_code": float(code),
                "energy_grievance": float(grievance)}

    # ------------------------------------------------------------------ start and yearly step

    def start(self, L):
        return self.accounts(self.measure(L), 0, 0.0)

    def propose(self, L, rng):
        now = self.measure(L)
        code = self.trajectory(now)
        grievance = 0.0
        if self.past:                                                               # part 8
            fall = 1.0 - now["livelihood_per_head"] / self.past[-1][1]
            grievance = self.grievance * max(0.0, fall)
        self.past.append((now["H"], now["livelihood_per_head"], now["per_head"]))
        return [Publish(key, value, self.name) for key, value in self.accounts(now, code, grievance).items()]
