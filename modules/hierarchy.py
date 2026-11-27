"""Optional module: hierarchy inside the firm (a readout; it changes nothing in the ledger).

THE RULE IN PLAIN WORDS

The ledger says how many employees each firm has and what one wage is paid. It says nothing
about who inside a firm commands whom, or about who is paid what. This module lays Blair Fix's
hierarchy model over the ledger. From the number of employees of each firm it works out the
ranks of a chain of command, the number of people in each rank, and the average pay of each
rank. It then reports how pay is distributed, and in particular the pay of the top rank. The
module proposes no change to any firm. Every other figure of a run is exactly the same with
the module on or off.

  1. Ranks. Rank 1 is the bottom of a firm. Each higher rank holds fewer people than the rank
     below it. The number of people in one rank divided by the number in the rank above is
     the span of control. The span of control between rank h-1 and rank h is a * exp(b * h)
     (Fix's equation 13), so it widens toward the top. The number of people in rank h is the
     number in rank 1 divided by all the spans up to h, rounded down to a whole number (Fix's
     equation 16). The top rank is the last rank that still holds at least one person (Fix's
     equation 19). The same a and b apply to every firm, as in Fix's model.
  2. From total employees to the bottom rank. The ledger gives the total employees of a firm
     and not the size of its bottom rank. The module does what Fix does (his section E.3): it
     works out the total for a long list of bottom ranks and reads the bottom rank back from
     the total. The bottom rank then takes whatever is left after the higher ranks are
     counted, so the ranks add up to the firm's employees exactly. A firm with fewer than
     one employee has one rank.
  3. Pay by rank. The average pay of rank h is the average pay of rank h-1 times r to the
     power h (Fix's equations 21 and 22), so the step in pay also widens toward the top. The
     number r is Fix's pay-scaling parameter.
  4. The level of pay. The model has one wage. The module reads that wage as the average pay
     of every firm (Fix's equation 24 turned round) and sets the pay of the bottom rank so
     that the pay of all ranks adds up to the firm's wage bill. Pay in the top rank is
     therefore taken out of the same wage bill, and people in the bottom rank of a large
     firm are paid less than the wage.
  5. The pay of the top rank. The pay of the top rank divided by the average pay of the firm
     is the ratio Fix calls the CEO pay ratio (his equation 25). The module reports it as a
     multiple of the wage.
  6. Hierarchical power. Fix defines a person's hierarchical power as the number of
     subordinates plus one, taken as an average for the rank (his equations 28 to 30). For
     the top rank this is the employees of the firm divided by the people in the top rank.
  7. Readouts, published every year and measured at the start of the year:
       hierarchy_ranks_average       ranks in the firm of the average employee
       hierarchy_ranks_dominant      average number of ranks in the hundred largest firms
       hierarchy_ranks_most          ranks in the firm with the most ranks
       hierarchy_top_pay_median      top-rank pay of the median firm, as a multiple of the wage
       hierarchy_top_pay_99          top-rank pay of the firm at the 99th percentile of firms
       hierarchy_top_pay_dominant    average top-rank pay in the hundred largest firms
       hierarchy_top_pay_highest     the highest top-rank pay of any firm
       hierarchy_power_dominant      average hierarchical power of the top rank in the hundred largest firms
       hierarchy_top_percent_share   part of all pay that goes to the best paid one per cent of employees
       hierarchy_top_percent_held    part of the best paid one per cent who work in the hundred largest firms
       hierarchy_gini                Gini index of pay among all employees (0 is equal pay)
       hierarchy_tail_exponent       exponent of a power law fitted to the pay of the best paid one
                                     per cent, with Fix's estimator (his equation 5); a smaller
                                     exponent means a fatter tail

No existing module reads these numbers. Pay inside the firm has no effect on conduct, on
earnings or on capitalization here.

WHAT IT RESTS ON

  - Blair Fix, "A Hierarchy Model of Income Distribution" (Working Papers on Capital as Power,
    2018), record 540 of the authors' archive. The companion paper "Hierarchy and the
    Power-Law Income Distribution Tail" (record 546) prints the same equations.
    Appendix D states the three assumptions the rule uses: "Firms are hierarchically
    structured, with a span of control that increases exponentially with hierarchical
    level." "The ratio of mean pay between adjacent hierarchical levels increases
    exponentially with hierarchical level." The third, lognormal dispersion of pay inside a
    rank, is left out here. Parts 1 to 6 are his equations 13, 16, 19, 21 to 25 and 28 to 30.
  - The same paper, on what the model is: "The hierarchy model is not built on micro
    principles. It is not dynamic, and it is not agent based." "It is essentially an
    extrapolation." That is why the module is a readout laid over the ledger each year.
  - The same paper, on what it finds: "the tail of the distribution is almost completely
    determined by hierarchy". "The model suggests that without large, hierarchically
    organized firms, there would be no power law distribution of top incomes." "Top earning
    US executives, as well as the wealthiest Americans, work for (or own) firms that are much
    larger than those of the general population."
  - The same paper, on the tie to capital as power: "Building on Nitzan and Bichler's capital
    as power hypothesis, I propose that capitalist income is derived from power -
    hierarchical power. By owning firms, capitalists earn the legal right to helm firm
    hierarchies. From this position of power, capitalists can partition firm income streams
    as they see fit." And: "I propose that one's power within a social hierarchy is
    proportional to the number of subordinates under one's control."
  - Capital as Power (2009), chapter 14, on why the ledger counts employees: "Ever since they
    first emerged in the power civilizations of the ancient river deltas, hierarchical
    organizations have been measured by 'head', or capita. They have been counted in slaves,
    soldiers, serfs, religious followers, factory workers and now, more generically, in
    employees. The number of 'heads' under one's immediate command - relative to the number
    of heads commanded by others - is indicative of one's immediate power." Fix's measure of
    hierarchical power counts the same heads rank by rank.

WHAT IS ADDED

The form of parts 1, 3, 5 and 6 is Fix's. The numbers are not. Both papers print the equations
and draw the fitted values in charts, and neither prints them as figures. The two numbers for
the span of control are read from the axes of Fix's Figure 29, which draws a between 0.8 and
1.6 and b between 0.075 and 0.175; the settings are the middle of each range. Fix gives every
firm its own pay-scaling parameter, drawn from a distribution fitted to the pay of chief
executives in a commercial database, and his charts draw it between 1.0 and 1.3. The module
uses one value for every firm, 1.1, which is an addition. Fix also gives every firm its own
average pay; the module gives every firm the one wage of the model (part 4). In part 2 the
bottom rank takes the remainder so that the ranks add up to employees that are not whole
numbers; Fix's firms have whole numbers of employees. Using the hundred largest firms for the
readouts on dominant capital follows the model and not Fix, who uses the 350 largest firms.

WHAT IS MISSING

Pay does not differ inside a rank, so the tail of the distribution is a set of steps and the
fitted exponent is rougher than Fix's. Pay does not differ between firms except through their
size. The pay-scaling parameter is fixed, so the module cannot show what Fix calls
hierarchical redistribution, in which that parameter rose in the United States after 1980
together with the capitalist share of income. Tying the parameter to the markup or to the
capitalist share would be a rule that Fix does not give. Fix's proposal that the part of a
person's income that comes from ownership rises with hierarchical power is not built: the
earnings of a firm are not handed to its top ranks. Government organs and unincorporated
businesses are not in the ledger, so their hierarchies are not counted. Nothing in the model
reads the readouts, so resistance does not respond to the pay of the top rank.
"""
import numpy as np
from core import Publish, top_positions


class Hierarchy:
    name = "hierarchy"
    reads = ()
    supplies = ("hierarchy_ranks_average", "hierarchy_ranks_dominant", "hierarchy_ranks_most",
                "hierarchy_top_pay_median", "hierarchy_top_pay_99", "hierarchy_top_pay_dominant",
                "hierarchy_top_pay_highest", "hierarchy_power_dominant", "hierarchy_top_percent_share",
                "hierarchy_top_percent_held", "hierarchy_gini", "hierarchy_tail_exponent")
    figures = {                   # what the workbench calls each published number: label, unit, note
        "hierarchy_ranks_average": ("Ranks for the average employee", "number", "Ranks in the firm of the average employee."),
        "hierarchy_ranks_dominant": ("Ranks in the top 100", "number", "Average number of ranks in the top 100 firms."),
        "hierarchy_ranks_most": ("Most ranks in one firm", "number", ""),
        "hierarchy_top_pay_median": ("Top pay in the median firm", "times", "Top-rank pay of the median firm, as a multiple of the wage."),
        "hierarchy_top_pay_99": ("Top pay at the 99th percentile", "times", "Top-rank pay of the firm at the 99th percentile, as a multiple of the wage."),
        "hierarchy_top_pay_dominant": ("Top pay in the top 100", "times", "Average top-rank pay in the top 100, as a multiple of the wage."),
        "hierarchy_top_pay_highest": ("Highest top pay", "times", "Highest top-rank pay of any firm, as a multiple of the wage."),
        "hierarchy_power_dominant": ("Hierarchical power in the top 100", "number", "Average hierarchical power of the top rank in the top 100."),
        "hierarchy_top_percent_share": ("Pay to the best paid 1%", "share", "Part of all pay that goes to the best paid 1% of employees."),
        "hierarchy_top_percent_held": ("Best paid 1% in the top 100", "share", "Part of the best paid 1% who work in the top 100."),
        "hierarchy_gini": ("Gini index of pay", "index", "0 is equal pay."),
        "hierarchy_tail_exponent": ("Tail exponent of pay", "number", "Power-law exponent for the best paid 1%. A smaller exponent means a fatter tail."),
    }

    def __init__(self, span_a=1.2, span_b=0.125, pay_scaling=1.1, tail=0.01, largest_firm=1e10,
                 grid=4000, top=100):
        self.span_a = span_a            # the span of control between rank h-1 and rank h is span_a * exp(span_b * h) (Fix, equation 13); the value is an addition: Fix prints no value, and 1.2 is the middle of the range on the axis of his Figure 29, which is a reading of a chart
        self.span_b = span_b            # how fast the span of control widens toward the top; the value is an addition: Fix prints no value, and 0.125 is the middle of the range on the axis of his Figure 29, which is a reading of a chart
        self.pay_scaling = pay_scaling  # average pay of rank h is that of rank h-1 times this number to the power h (Fix, equation 21); the value is an addition: Fix prints no value and gives every firm its own, and 1.1 is picked from the range that his charts draw, between 1.0 and 1.3
        self.tail = tail                # the part of employees counted as the top of the distribution; Fix uses the best paid one per cent
        self.largest_firm = largest_firm  # the largest number of employees the table of part 2 covers (a limit of the arithmetic, not of the rule)
        self.grid = grid                # number of entries in that table (a limit of the arithmetic, not of the rule)
        self.top = top                  # the number of largest firms that stands for dominant capital
        if span_a * np.exp(2 * span_b) <= 1.0 or span_b < 0:
            raise ValueError("each rank must hold fewer people than the rank below it")
        # the part of the bottom rank that each rank holds, before rounding down (Fix, equation 16)
        part = [1.0]
        while part[-1] * largest_firm >= 1.0:
            part.append(part[-1] / (span_a * np.exp(span_b * (len(part) + 1))))
        self.part = np.array(part[:-1])
        h = np.arange(1, self.part.size + 1)
        self.pay = pay_scaling ** (h * (h + 1) / 2.0 - 1.0)      # pay of rank h as a multiple of the pay of rank 1 (Fix, equation 23)
        # part 2: total employees for a long list of bottom ranks (Fix, section E.3)
        self.base_list = np.geomspace(1.0, largest_firm, grid)
        self.total_list = self.base_list + np.floor(self.base_list[:, None] * self.part[None, 1:]).sum(axis=1)

    # ------------------------------------------------------------------ pieces of the rule

    def structure(self, employees):
        """Ranks of every firm. Returns the number of ranks of each firm, and one entry for
        every rank of every firm: the firm, the people in the rank, and the pay of the rank
        as a multiple of the pay of the firm's bottom rank."""
        T = np.asarray(employees, dtype=float)
        base = np.where(T >= 1.0, np.interp(T, self.total_list, self.base_list), T)     # part 2
        ranks = np.ones(T.size, dtype=int)
        above = np.zeros(T.size)
        firms, people, pay = [], [], []
        for h in range(1, self.part.size):                  # h is the position in self.part, so the rank is h + 1
            idx = np.flatnonzero(base * self.part[h] >= 1.0)
            if idx.size == 0:
                break
            count = np.floor(base[idx] * self.part[h])      # part 1
            ranks[idx] = h + 1
            above[idx] += count
            firms.append(idx); people.append(count); pay.append(np.full(idx.size, self.pay[h]))
        bottom = np.maximum(T - above, 1e-12)               # the bottom rank takes the remainder
        firms.append(np.arange(T.size)); people.append(bottom); pay.append(np.ones(T.size))
        return ranks, np.concatenate(firms), np.concatenate(people), np.concatenate(pay)

    def measure(self, L):
        """The readouts, from the ledger as it stands. Pay is in multiples of the wage."""
        n = L.n
        count = len(L)
        ranks, firm, people, pay = self.structure(n)
        # part 4: the pay of each firm adds up to its wage bill
        mean_multiple = np.bincount(firm, people * pay, count) / np.bincount(firm, people, count)
        pay = pay / mean_multiple[firm]                    # pay of each rank as a multiple of the wage
        top_pay = self.pay[ranks - 1] / mean_multiple       # part 5 (Fix, equation 25)
        top_people = np.where(ranks > 1, np.floor(np.interp(n, self.total_list, self.base_list) * self.part[ranks - 1]), n)
        power = n / np.maximum(top_people, 1e-12)           # part 6, for the top rank
        dominant = top_positions(L.cap(), np.arange(count), self.top)

        # the distribution of pay among all employees, best paid first
        order = np.argsort(-pay, kind="stable")
        x, w, c = pay[order], people[order], firm[order]
        everyone, all_pay = w.sum(), (w * x).sum()
        cutoff = self.tail * everyone
        before = np.cumsum(w) - w
        inside = np.clip(cutoff - before, 0.0, w)           # people of each entry who are among the best paid
        last = min(int(np.searchsorted(np.cumsum(w), cutoff)), x.size - 1)
        logs = (inside * np.log(x / x[last])).sum()
        is_dominant = np.zeros(count, dtype=bool)
        is_dominant[dominant] = True
        # Gini index from the entries in rising order of pay
        xa, wa = x[::-1], w[::-1]
        s = np.cumsum(wa * xa)
        gini = 1.0 - (wa * (2 * s - wa * xa)).sum() / (everyone * all_pay)

        return {"hierarchy_ranks_average": float((ranks * n).sum() / n.sum()),
                "hierarchy_ranks_dominant": float(ranks[dominant].mean()),
                "hierarchy_ranks_most": float(ranks.max()),
                "hierarchy_top_pay_median": float(np.median(top_pay)),
                "hierarchy_top_pay_99": float(np.quantile(top_pay, 0.99)),
                "hierarchy_top_pay_dominant": float(top_pay[dominant].mean()),
                "hierarchy_top_pay_highest": float(top_pay.max()),
                "hierarchy_power_dominant": float(power[dominant].mean()),
                "hierarchy_top_percent_share": float((inside * x).sum() / all_pay),
                "hierarchy_top_percent_held": float(inside[is_dominant[c]].sum() / inside.sum()),
                "hierarchy_gini": float(gini),
                "hierarchy_tail_exponent": float(1.0 + inside.sum() / logs) if logs > 0 else float("nan")}   # Fix, equation 5

    # ------------------------------------------------------------------ start and yearly step

    def start(self, L):
        return self.measure(L)

    def propose(self, L, rng):
        return [Publish(key, value, self.name) for key, value in self.measure(L).items()]
