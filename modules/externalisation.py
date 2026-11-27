"""Optional module: externalisation (an account of burdens that no firm's books carry).

THE RULE IN PLAIN WORDS

The activity of a firm has consequences that somebody has to bear: injury at work, a fouled
river, a changed climate. A burden is on the books of a firm when the firm pays for it. It
is off the books when somebody else bears it without payment. This module keeps an account of
the burdens that are off the books. Each burden is tagged with the firm that shifted it and
with who bears it. A burden is measured as a yearly amount for each employee of the firm, in
units of the yearly wage.

  1. Who bears. There are three bearers. The first is the firm's own employees. The second
     is the communities around the firm, which means everybody else alive now. The third is
     later years, which means people who will bear the consequence after it has built up.
  2. How weak each bearer is. Communities are weak in proportion to one minus the level of
     popular resistance. Employees are weak in the same proportion, times unemployment
     divided by a setting, and never more than 1. Later years are always fully weak, because
     nobody speaks for them.
  3. The power of a firm to shift. The power of a firm is its capitalization divided by
     the average capitalization of the hundred largest firms, and never more than 1. A part
     of the power to shift is open to every firm. The rest is in proportion to that power.
  4. Shifting. Each year each firm shifts onto each bearer a yearly attempt, times the
     weakness of the bearer, times the firm's power to shift, times the room left under a
     ceiling. Shifting a burden raises the firm's earnings per employee by the amount
     shifted times the wage. The price of the firm does not change.
  5. Return by uprisings and court rulings. Each year a part of the burdens on employees and
     on communities returns to the books. The part is a rate times the level of popular
     resistance, and it is larger for a firm with more power, because campaigns pick the
     prominent. A returned burden lowers earnings per employee by the same amount times the
     wage, and it raises the risk of the firm in proportion to the earnings lost.
  6. Return by disaster. The burden on later years builds up, year by year, into a stock for
     each firm. Each year each firm has a chance of a disaster in proportion to its own
     stock. No date is entered and no event comes from outside: the chance is produced by
     what the firm itself has shifted. A disaster puts the firm's whole burden on later
     years back on its books, multiplies its risk by a factor, and empties its stock. The
     emptied stock falls on the communities in that year.
  7. Risk fades. The rise in risk that this module has given a firm fades by a part each
     year. The module keeps a mark on each firm so that it takes back only what it gave.
  8. Grievance. The module publishes a rate times the burdens that employees and communities
     bear in the year, including the stock that disasters released, for each member of the
     working population. The resistance module adds that number to the year's rise in
     popular resistance. Burdens on later years add nothing until a disaster releases them.
  9. Readouts, published every year:
       externalisation_burden_part       all burdens off the books, in money, as a part of all earnings
       externalisation_on_employees      burden borne by employees, per employee, as a part of the wage
       externalisation_on_communities    the same for communities
       externalisation_on_later_years    the same for later years
       externalisation_stock             built-up burden on later years, per employee, in years of the wage
       externalisation_differential      burden per employee of the hundred largest firms divided by the average
       externalisation_shifted           burden shifted off the books in the year, per employee, as a part of the wage
       externalisation_returned          burden returned to the books in the year, the same unit
       externalisation_struck            number of firms struck by a disaster in the year
       externalisation_struck_dominant   number of those among the hundred largest firms
       externalisation_grievance         the number of part 8

WHAT IT RESTS ON

  - DT Cochrane, "From Colonialism to Climate Change: The Power to Externalize" (2017), a talk
    in the Third Speaker Series on the Capitalist Mode of Power, record 519 of the authors'
    archive. The archive holds a video and a one-page abstract and no paper. The abstract
    reads in full: "The
    history of capitalism is a history of externalization. While benefits were tallied, costs
    were routinely excluded from accounts. In this presentation I examine the history of
    externalization as a power process. A history of brutality and destruction marketed as
    innovation and efficiency, externalization has been the shadowy counterpart to
    accumulation. From colonialism to climate change, I will describe how negative effects of
    economic activity are systematically imposed on vulnerable communities via the
    interconnected processes of production and accounting. Finally, I will consider how
    externalities have made their way back onto the books through uprisings, court rulings
    and environmental disasters." The account itself, parts 1 and 4, rests on "costs were
    routinely excluded from accounts". Parts 2 and 3 rest on "a power process" and "imposed
    on vulnerable communities". Parts 5 and 6 are the three ways back that he names.
  - DT Cochrane, "Disobedient Things: The Deepwater Horizon Oil Spill and Accounting for
    Disaster" (Valuation Studies, 2020), record 636 of the
    authors' archive. Of the costs of the disaster:
    "These costs would reduce expected earnings and could increase the risk to earnings."
    Parts 5 and 6 therefore act on earnings and on risk. Of the size of the fall: "The bottom
    would come two weeks later, on June 25, when BP's market capitalization would be just
    over half its pre-disaster value." The factor of part 6 is set from that figure. Of the
    recovery: "Over the next 20 days, the company would recover about 20 percent of its
    relative pre-disaster value". Part 7 rests on this. The paper defines power as
    "confidence in obedience" and says that things can disobey as people can, which is the
    ground for a disaster that needs no uprising.
  - Jeffrey Monaghan and DT Cochrane, "Fight to Win! Tools for Confronting Capital" (2012),
    record 667 of the authors' archive.
    Of Nike: "following the logic of accumulation, it sought to boost earnings by pushing
    down costs. To this end, it began to ship jobs to low-wage zones in Asia. It was hardly
    unique in this. However, its own success would bring blowback as its high profile led
    anti-sweatshop activists to focus their attention on the sportswear company". And: "The
    company differentially accumulated 13.5 percent per year from 1981 to 1996, then from
    1996 to 1999 it differentially deccumulated at a stunning 28 percent per year." The
    larger return for firms with more power in part 5 rests on this.
  - Capital as Power (2009), chapter 13, "Absorptiveness". The discounters look to see
    "whether environmental policies raise the effective penalty for polluters ... Any regular
    effect on profit is instantly discounted into present value, and the power process this
    effect emanates from henceforth becomes part of capital." A burden that returns to the
    books is capitalized like any other effect on profit.
  - Capital as Power, chapter 9. Catastrophe bonds have "given capitalists the illusion they
    can somehow 'externalize' the more cataclysmic impacts of nature on society", and "on
    the one hand they contribute to climate change, while on the other they cheerfully
    discount the boom in the doom". The same chapter shows that damage a hundred years away
    has a present value near nothing at an ordinary discount rate. This is the ground for
    treating later years as a bearer that cannot resist.
  - Capital as Power, chapter 16, "Cost cutting" and "Input prices". Cost cutting "helps
    dominant capital meet the average, not beat it", and "even when large firms do control
    input prices, the benefits quickly tend to spill over to other firms". Shifting a burden
    is a way of cutting cost. The part of the power to shift that is open to every firm is
    this spill-over. The gains of this module are an income component that
    it owns, and the cost cutting module leaves them alone.
  - Capital as Power, chapter 12. Unemployment weakens employees against owners. This is the
    ground for the weakness of employees in part 2.

WHAT IS ADDED

The literature says that costs are kept off the books, that this is a power process, that
the burdens fall on the vulnerable, and that they return through uprisings, court rulings and
disasters. It gives no rule and, apart from the fall of BP, no figure. Everything that turns
these statements into numbers is added:
  - The three bearers and the rule that says how weak each is.
  - The measure of a firm's power to shift, and the part open to every firm. The book says
    that cost cutting does not let dominant capital beat the average. Cochrane calls
    externalisation a power process. The rule lets size count, which goes beyond the book.
  - The yearly attempt, the ceiling, and the form of part 4.
  - The rate of return, its doubling for the most powerful firms, and the rise in risk for
    each unit of earnings lost.
  - The chance of a disaster, its form, and the rule that the stock falls on communities.
  - The factor of 1.8 on risk. It makes the capitalization of a struck firm fall to about
    0.55 of its level, which is Cochrane's "just over half" for BP. One case is not a rate.
  - The fading of the added risk, and the rate of the grievance.
  - In a merger the buyer keeps its own burden for each employee, as if it carried its own
    practice into what it bought. A new firm starts with nothing off the books.

WHAT IS MISSING

Colonialism is in the title of the talk and is not in the rule. The model has one country, so
there is no bearer abroad. Nike's shift of jobs to low-wage zones is absent for the same
reason. The rule does not say what a burden is made of, so it cannot tell a poisoned river
from an unsafe mine. The bearers do not carry the burden as a loss of anything in the ledger:
their wage and their employment are unchanged, and only their resistance responds. A disaster
strikes one firm. Cochrane shows that the drilling moratorium also lowered the value of
other oil companies, and the rule has no such spread. The earnings from shifted burdens
are an income component that this module owns. The core keeps them apart from the markup,
and the sabotage module does not read them as markup. The content of the talk beyond its
abstract is not used.
"""
import numpy as np
from core import Scale, SetComponent, Publish, top_positions

INCOME = "burdens off the books"   # this module's income component: what a firm gains for each employee from burdens it does not pay for

BEARERS = ("employees", "communities", "later_years")
# Added per-firm numbers. Each holds one plus the quantity, because a change can only multiply.
ON = {b: "offbooks_on_" + b for b in BEARERS}     # yearly burden per employee on each bearer, in units of the wage
STOCK = "offbooks_stock"                          # built-up burden on later years per employee, in years of the wage
MARK = "offbooks_risk_mark"                       # the factor by which this module has raised the firm's risk


class Externalisation:
    name = "externalisation"
    reads = ("resistance", "unemployment")
    supplies = ("externalisation_burden_part", "externalisation_on_employees", "externalisation_on_communities",
                "externalisation_on_later_years", "externalisation_stock", "externalisation_differential",
                "externalisation_shifted", "externalisation_returned", "externalisation_struck",
                "externalisation_struck_dominant", "externalisation_grievance")

    def __init__(self, attempt=0.0015, ceiling=0.015, open_to_all=0.3, labour_helpless_at=0.10,
                 return_rate=0.2, focus=1.0, return_risk=1.0, hazard=0.05, largest_chance=0.05,
                 strike_risk=1.8, calm=0.2, deepest_cut=0.5, grievance=0.3, top=100):
        self.attempt = attempt                  # burden a firm with full power shifts onto a fully weak bearer in a year, per employee, as a part of the wage; an addition
        self.ceiling = ceiling                  # the largest burden per employee that one bearer can be made to carry, as a part of the wage; an addition
        self.open_to_all = open_to_all          # part of the power to shift that every firm has whatever its size (chapter 16: benefits "spill over to other firms"); the number is an addition
        self.labour_helpless_at = labour_helpless_at   # unemployment at which employees cannot refuse a burden at all; an addition
        self.return_rate = return_rate          # part of the burdens on employees and communities that returns to the books in a year at full popular resistance, for a firm without power; an addition
        self.focus = focus                      # how much more is returned from a firm with full power (1 doubles it); the direction is from Monaghan and Cochrane on Nike, the number is an addition
        self.return_risk = return_risk          # rise in a firm's risk per unit of the part of its earnings that a return takes away; an addition
        self.hazard = hazard                    # yearly chance of a disaster per unit of a firm's built-up burden on later years (in years of the wage per employee); an addition
        self.largest_chance = largest_chance    # the yearly chance of a disaster never exceeds this; an addition
        self.strike_risk = strike_risk          # a disaster multiplies the firm's risk by this; 1.8 lowers capitalization to about 0.55, after Cochrane (2020): BP fell to "just over half its pre-disaster value"; the value is an addition: it copies the lowest point of one company after one disaster, and the literature gives no general figure
        self.calm = calm                        # part of the risk added by this module that fades each year; Cochrane (2020) reports a partial recovery within weeks, the number is an addition
        self.deepest_cut = deepest_cut          # the largest part of a firm's earnings per employee that returns can take away in one year; an addition that keeps earnings positive
        self.grievance = grievance              # rise in popular resistance per unit of burden borne by employees and communities, per member of the working population, in units of the wage; an addition
        self.top = top                          # the number of largest firms that stands for dominant capital

    def start(self, L):
        for name in list(ON.values()) + [STOCK, MARK]:
            L.add_attribute(name, 1.0, 1.0)     # one plus zero: nothing is off the books at the start
        # The gain is not paid out of wages or out of any other income in the ledger, so it counts as income of its own.
        L.add_component(INCOME, self.name, kind="income")
        return {key: 0.0 for key in self.supplies}

    def propose(self, L, rng):
        A, wage, count = L.accounts, L.shared["wage"], len(L)
        n, e = L.n, L.e
        R = float(np.clip(A.get("resistance", 0.0), 0.0, 1.0))
        u = float(A["unemployment"])
        x = {b: L.extra[ON[b]] - 1.0 for b in BEARERS}
        stock = L.extra[STOCK] - 1.0
        mark = L.extra[MARK]

        # Part 3: the power of each firm to shift.
        K = L.cap()
        top = top_positions(K, np.arange(count), self.top)
        strength = np.minimum(1.0, K / K[top].mean())
        power = self.open_to_all + (1.0 - self.open_to_all) * strength

        # Part 2: how weak each bearer is.
        weak = {"employees": float(np.clip(u / self.labour_helpless_at, 0.0, 1.0)) * (1.0 - R),
                "communities": 1.0 - R,
                "later_years": 1.0}

        # Part 6: disasters, drawn from each firm's own built-up burden.
        chance = np.minimum(self.largest_chance, self.hazard * np.maximum(stock, 0.0))
        struck = rng.random(count) < chance

        # Parts 4 to 6: what is shifted and what returns.
        shifted, back = {}, {}
        for b in BEARERS:
            room = np.maximum(0.0, 1.0 - x[b] / self.ceiling)
            shifted[b] = self.attempt * weak[b] * power * room
        returned_part = np.minimum(1.0, self.return_rate * R * (1.0 + self.focus * strength))
        back["employees"] = x["employees"] * returned_part
        back["communities"] = x["communities"] * returned_part
        back["later_years"] = np.where(struck, x["later_years"], 0.0)
        shifted["later_years"] = np.where(struck, 0.0, shifted["later_years"])
        new_x = {b: np.maximum(x[b] + shifted[b] - back[b], 0.0) for b in BEARERS}
        released = np.where(struck, stock, 0.0)                       # the stock that a disaster empties onto communities
        new_stock = np.where(struck, 0.0, stock + x["later_years"])

        # Earnings per employee: up by what is shifted, down by what returns.
        gain = sum(shifted.values()) * wage
        loss_people = (back["employees"] + back["communities"]) * wage
        loss = loss_people + back["later_years"] * wage
        # The module sets its own income component: the burdens off the books times the wage. As
        # before, returns cannot take away more than a set part of earnings per employee in one year.
        own = L.components[INCOME]
        income = np.maximum(sum(new_x.values()) * wage, own - self.deepest_cut * e)

        # Parts 5 to 7: risk.
        new_mark = 1.0 + (mark - 1.0) * (1.0 - self.calm)
        new_mark = new_mark * (1.0 + self.return_risk * np.minimum(loss_people / e, self.deepest_cut))
        new_mark = np.where(struck, new_mark * self.strike_risk, new_mark)

        changes = [SetComponent(INCOME, income, self.name),
                   Scale("risk", new_mark / mark, self.name),
                   Scale(MARK, new_mark / mark, self.name),
                   Scale(STOCK, (1.0 + new_stock) / (1.0 + stock), self.name)]
        changes += [Scale(ON[b], (1.0 + new_x[b]) / (1.0 + x[b]), self.name) for b in BEARERS]

        # Parts 8 and 9: grievance and readouts, as the account stands after this year's changes.
        employed, heads = n.sum(), L.shared["workforce"]
        on = {b: float((n * new_x[b]).sum()) for b in BEARERS}
        total = sum(on.values())
        per_employee_all = total / employed
        per_employee_top = sum(float((n[top] * new_x[b][top]).sum()) for b in BEARERS) / n[top].sum()
        fell = float((n * released).sum())
        dominant = np.zeros(count, dtype=bool)
        dominant[top] = True
        out = {"externalisation_burden_part": total * wage / float((n * e).sum()),
               "externalisation_on_employees": on["employees"] / employed,
               "externalisation_on_communities": on["communities"] / employed,
               "externalisation_on_later_years": on["later_years"] / employed,
               "externalisation_stock": float((n * new_stock).sum()) / employed,
               "externalisation_differential": per_employee_top / per_employee_all if per_employee_all > 0 else 1.0,
               "externalisation_shifted": float((n * sum(shifted.values())).sum()) / employed,
               "externalisation_returned": float((n * sum(back.values())).sum()) / employed,
               "externalisation_struck": float(struck.sum()),
               "externalisation_struck_dominant": float((struck & dominant).sum()),
               "externalisation_grievance": self.grievance * (on["employees"] + on["communities"] + fell) / heads}
        return changes + [Publish(key, value, self.name) for key, value in out.items()]
