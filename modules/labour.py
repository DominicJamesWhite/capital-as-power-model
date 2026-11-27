"""Optional module: organised labour.

THE RULE IN PLAIN WORDS

The nine modules hold one number for popular resistance, and that number does several jobs. Two
of the jobs concern wages: in the sabotage module it raises the level of unemployment at which
wages keep pace with prices, and in the stagflation module it raises the part of each price
rise that wages obtain. This module takes over those two jobs. It keeps a count of how far the
employees of each industry are organised, it works out how much they strike, and it publishes
the strength of labour. Popular resistance keeps its other jobs: it still lowers the cohesion of
dominant capital, weakens its hold on its markups, and raises its risk.

  1. Organisation. For each industry the module keeps the part of the employees who are
     organised, a number between 0 and 1. At the start it is 3 per cent in every industry.
  2. The grievance. The real wage is the wage divided by the average price. Each year the
     module compares the real wage with the best real wage of the last ten years. The
     grievance is the shortfall divided by a setting, and never more than 1. It is 0 when the
     real wage is at its best. The grievance is the same in every industry, because the model
     has one wage and one average price.
  3. Organising. Each year the unorganised part of an industry shrinks by a rate, times the
     grievance, times a number for the size of the units in the industry. That number is low
     where dominant capital holds nothing and 1 where it holds everything. Employees
     therefore organise when wages have fallen behind prices, and fastest in the industries
     that dominant capital holds.
  4. Wearing down. Each year the organised part of an industry shrinks by its own size times
     the sum of three things: a slow fading, the repression that the organised force module
     publishes (0 without that module), and a multiple of the part of the working population
     newly drawn in from outside, which the proletarianization module publishes (0 without it).
  5. Discipline and strikes. The threat of the sack mutes strikes. Discipline is unemployment
     divided by a setting, and never more than 1. Militancy is the grievance times one minus
     discipline. The strike activity of an industry is its organised part times militancy:
     the part of its employees who are on strike in the year.
  6. Co-option. An organisation that is not striking counts for only a part of its size. That
     part is smaller in the industries that dominant capital holds, because a large quiet
     union can be made into a restraint on its own members.
  7. Strength. The strength of labour in an industry is its organised part, times the sum of
     the quiet part of step 6 and the rest multiplied by militancy. It is the organised part
     in full when militancy is 1. The strength of labour in the whole economy is the average
     over industries, weighted by employees.
  8. What reads the strength. The sabotage module uses the strength in each industry in place
     of popular resistance when it sets the level of unemployment at which wages keep pace
     with prices. The stagflation module uses the strength in the whole economy in place of
     popular resistance when it sets the part of each price rise that wages obtain. Both read
     popular resistance when this module is off.
  9. The cost of strikes to owners. The risk of every firm in an industry is multiplied by 1
     plus a rate times the strike activity of the industry. The rise lasts only as long as
     the strikes: each year the module removes last year's rise and applies this year's.
 10. Readouts. The module publishes the strength in each industry and in the whole economy,
     the organised part of all employees, the organised part of the employees of the
     industries that dominant capital mostly holds, strike activity, the grievance, militancy
     and the real wage.

Nothing comes from outside. The real wage falls when markups rise, which the sabotage and
stagflation modules decide. Unemployment comes from hiring. Nobody in the rule aims at a share
of income or at a level of employment.

WHAT IT RESTS ON

  - Capital as Power (2009), chapter 16, "Workers and capitalists" and "Patterns". United States
    inflation "has been associated with a systematic redistribution of income from workers to
    firms". "But in Germany and France, two countries where labour is relatively strong, the
    impact of inflation on labour/capital redistribution has been far less clear." "Inflation
    itself is a tricky process; its consequences depend on the relative power of the leading
    firms, capital in general and labour groups, among others; this relative power can change
    over time and so can the distributional outcomes." Part 8 rests on this: the part of a
    price rise that wages obtain depends on the strength of labour, and that strength moves.
  - Chapter 16, "The politics of inflation". Under depth the underlying population "starts to
    resist and fight back; it calls for political changes; it demands to rein in the leading
    corporations; and it wants to be compensated by higher wages". Parts 2 and 3 rest on the
    words "compensated by higher wages": the grievance is the loss that calls for compensation.
  - Bichler and Nitzan, "Can Capitalists Afford Recovery?" (2014), on Figure 9. "Whenever
    unemployment rises, the rate of change of the real wage falls - and vice versa when
    unemployment falls." And: "of these many processes of sabotage, the threat and exercise of
    unemployment remains central and crucial - not only temporarily as Marx suggested, but
    permanently". The paper speaks of "the role of rising unemployment in disciplining
    workers". Part 5 rests on this. The same paper warns that after the early 1940s the level
    of the real wage rose together with unemployment, so the rule lets unemployment act on
    strikes, which move the rate of change, and not on organisation.
  - Capital as Power, chapter 13. In the bourgs "the oligarchy treated the workers and artisans
    with indifference - that is, as long as they remained docile. When they revolted (the first
    known strikes took place in Flanders during the thirteenth century) the retaliation -
    often coordinated within and between the bourgs - was usually swift and violent." "The
    capitalist class struggle, from its very inception, was never merely an 'industrial
    dispute'. It was a broad power conflict embedded in a newly emergent form of state." Part
    4 rests on this: organised force wears organisation down.
  - Chapter 1 names "the growth of large units - big business, large government and organized
    labour". "Growing Through Sabotage" (2020) speaks of "the rise of hierarchical
    organizations and large power coalitions, including giant corporations with transnational
    tentacles, large labour unions, political parties and government bureaucracies". Its
    footnote 35 reports Timothy Mitchell's view that the conditions of producing coal
    "empowered coal miners and transportation workers, making strikes - and eventually
    general strikes - an effective political weapon". Part 3 rests loosely on these: labour
    organises alongside large units.
  - Bichler and Nitzan, The Global Political Economy of Israel (2002), chapter 4, "The Histadrut
    Contra Workers". "Attempts to boost the central power of the Histadrut were aimed not to
    empower workers, but to weaken them." The union federation "has accepted its role as a
    restraining factor in the labour market". State-sanctioned unions were a means of
    "'co-opting' and 'de-classing'" workers, who "have given up their autonomy". A footnote to
    chapter 4 of the 2009 book recalls Jack London's oligarchy that "bribes the large unions
    into submission". Part 6 rests on these. The same chapter of the 2002 book reports that with
    unemployment low "Israeli industrialists were increasingly concerned that workers would
    demand a boost to their sagging income share", and quotes an adviser who wanted to end
    "over-employment" so that workers would keep a wage pact. This supports parts 2 and 5.
  - The same book, chapter 3. "By reintroducing 'free' Arab labour into the picture, it broke
    the Histadrut's monopoly." Part 4 rests on this: newly drawn-in labour dilutes organisation.
  - Nitzan and Bichler, "Going Global" (2001). "Strikes, uprisings, isolation, sanctions, or
    war - much like military spending, inflation, and gold prices - are important not for what
    they are, but through their expected impact on future profit", and they are reduced to
    "'present value' and 'risk premia'". Part 9 rests on this: a strike enters capitalization
    as risk.
  - Jordan Brennan, "Rising Corporate Concentration, Declining Trade Union Power, and the
    Growing Income Gap" (Levy Economics Institute, 2016), a study by a student of Nitzan that
    uses the book's account of inflation. It separates "the amassment of power from the
    exercise of power": union density is the first and strike activity is the second. "The
    extent of strike activity is tightly and positively correlated with the rate of growth of
    hourly earnings." "Trade union power, manifested in union density and strike activity,
    progressively redistributes income." Parts 1, 5 and 7 take the separation of organisation
    from strikes from this study. It also supplies the one figure the rule can cite: "In
    1900, unionization was below 3 percent." Union density reached "a historic high of 29
    percent in 1954". The second figure is something to compare a run with. It is not a setting.

WHAT IS ADDED

The literature says that the outcome of inflation depends on the strength of labour, that the
population demands higher wages under inflation, that unemployment disciplines workers, that
strikes meet force, that large unions can be turned against their members, and that strikes
matter to owners through risk. It gives no rule and no rate. The form of every part is an
addition. Every number below is an addition except the starting organisation of 3 per cent,
which is Brennan's figure for the United States in 1900. Brennan's study is not by Nitzan and
Bichler, and it borrows the term "countervailing power" from Galbraith, which they do not use.
The authors of the book give no account of how organisation grows. Tying organising to the
industries that dominant capital holds is an addition that rests on a few words.

WHAT IS MISSING

The model has one wage, so organised employees do not earn more than unorganised employees, and
an industry's strength acts only on its markup. A strike costs owners nothing in lost
earnings: it raises risk only. Strikes do not feed popular resistance, and the retaliation of
chapter 13 arrives only if the organised force module is on. Brennan reports that organisation
in the United States surged under laws passed in the 1930s and fell under later laws. The rule
has no laws. Co-option is a fixed discount and not a process.
"""
import numpy as np
from core import Scale, Publish, top_positions

PREMIUM = "labour_strike_premium"     # the added per-firm number: the rise in risk from strikes now inside the firm's risk


class Labour:
    name = "labour"
    reads = ("unemployment",)
    supplies = ("labour_strength", "labour_strength_by_industry", "labour_organisation", "labour_organisation_held",
                "strike_activity", "labour_grievance", "labour_militancy", "real_wage")

    def __init__(self, start=0.03, memory=10, full_grievance=0.05, organise=0.05, small_units=0.3, fade=0.03,
                 dilution=5.0, discipline_at=0.25, quiet_part=0.5, cooption=0.5, strike_risk=1.0, top=100):
        self.start_level = start              # organised part of employees at the start; "In 1900, unionization was below 3 percent" (Brennan 2016)
        self.memory = memory                  # years over which the best real wage is remembered (addition)
        self.full_grievance = full_grievance  # shortfall of the real wage below its remembered best at which the grievance is complete (addition)
        self.organise = organise              # part of the unorganised employees of a fully held industry who organise in a year of complete grievance (addition)
        self.small_units = small_units        # the same rate in an industry that dominant capital does not hold, as a part of the rate above (addition)
        self.fade = fade                      # part of organisation that lapses in a year with nothing acting on it (addition)
        self.dilution = dilution              # part of organisation lost per unit of the working population newly drawn in from outside (addition); used only with the proletarianization module
        self.discipline_at = discipline_at    # unemployment at which the threat of the sack silences strikes altogether (addition)
        self.quiet_part = quiet_part          # part of an organisation that counts toward strength when it is not striking (addition)
        self.cooption = cooption              # part of that quiet strength lost in an industry wholly held by dominant capital (addition); 0 switches co-option off
        self.strike_risk = strike_risk        # rise in the risk of a firm per unit of the part of its industry's employees on strike (addition); 0 switches it off
        self.top = top
        self.org = None                       # organised part of employees, one number per industry
        self.wages = []                       # the real wage of recent years

    # ------------------------------------------------------------------ pieces of the rule

    def held(self, L):
        """Employees in each industry, and the part of them that dominant capital holds."""
        k = L.sector_of.size
        dominant = top_positions(L.cap(), np.arange(len(L)), self.top)
        n = np.bincount(L.ind, L.n, k)
        return n, np.bincount(L.ind[dominant], L.n[dominant], k) / np.maximum(n, 1e-12)

    def strength(self, held, militancy):
        quiet = self.quiet_part * (1 - self.cooption * held)                       # part 6
        return self.org * (quiet + (1 - quiet) * militancy)                        # part 7

    def readouts(self, n, held, grievance, militancy, real_wage):
        by_industry = self.strength(held, militancy)
        total = max(n.sum(), 1e-12)
        mostly = held > 0.5
        return {"labour_strength": float((by_industry * n).sum() / total),
                "labour_strength_by_industry": by_industry,
                "labour_organisation": float((self.org * n).sum() / total),
                "labour_organisation_held": float((self.org * n)[mostly].sum() / n[mostly].sum()) if n[mostly].sum() > 0 else 0.0,
                "strike_activity": float((self.org * militancy * n).sum() / total),
                "labour_grievance": float(grievance), "labour_militancy": float(militancy),
                "real_wage": float(real_wage)}

    @staticmethod
    def real_wage(L):
        return L.shared["wage"] / ((L.p * L.n).sum() / L.n.sum())

    # ------------------------------------------------------------------ start and yearly step

    def start(self, L):
        L.add_attribute(PREMIUM, 1.0, 1.0)
        self.org = np.full(L.sector_of.size, float(self.start_level))              # part 1
        self.wages = [self.real_wage(L)]
        n, held = self.held(L)
        return self.readouts(n, held, 0.0, 0.0, self.wages[0])

    def propose(self, L, rng):
        A = L.accounts
        n, held = self.held(L)

        # Part 2: the grievance.
        now = self.real_wage(L)
        self.wages = (self.wages + [now])[-self.memory:]
        grievance = float(np.clip((1 - now / max(self.wages)) / self.full_grievance, 0.0, 1.0))

        # Parts 3 and 4: organising and wearing down.
        units = self.small_units + (1 - self.small_units) * held
        wear = self.fade + A.get("repression", 0.0) + self.dilution * A.get("proletarianization_rate", 0.0)
        self.org = np.clip(self.org + self.organise * grievance * units * (1 - self.org) - wear * self.org, 0.0, 1.0)

        # Part 5: discipline, militancy and strikes.
        discipline = float(np.clip(A["unemployment"] / self.discipline_at, 0.0, 1.0))
        militancy = grievance * (1 - discipline)
        strikes = self.org * militancy

        changes = [Publish(key, value, self.name)
                   for key, value in self.readouts(n, held, grievance, militancy, now).items()]

        # Part 9: strikes raise the risk of the firms they hit, for as long as they last.
        if self.strike_risk > 0:
            factor = (1 + self.strike_risk * strikes)[L.ind] / L.extra[PREMIUM]
            if not np.allclose(factor, 1.0, rtol=0, atol=1e-12):
                changes += [Scale("risk", factor, self.name), Scale(PREMIUM, factor, self.name)]
        return changes
