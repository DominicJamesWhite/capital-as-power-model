r"""Optional module: other measures of concentration. A readout. It changes nothing.

Each year the module measures the same ledger in four ways: the share of the hundred largest
claims in the total, the differential measure, the Gini index and the Herfindahl-Hirschman
index. It publishes all four, for capitalization and for earnings, so that the reader can see
them move apart. No module reads what it publishes, and it adds no attribute to the claims, so
a run with this module gives exactly the figures of the run without it.

To print the table of measures, run from the project root:
    .venv\Scripts\python.exe experiments\casp\model\modules\concentration_measures.py [claims] [years] [seed]

SOURCE

Capital as Power (2009), chapter 14, the sections "Dominant capital", "Aggregate concentration"
and "Differential measures", with Equation (1), Table 14.1 and Figures 14.1 and 14.2. Chapter 15,
"Green-field", for the remark that new firms are smaller than the average, and "Breaking the
envelope" for the limit of merger. The papers in data/bn_archives/papers were searched for
"Gini", "Herfindahl" and "aggregate concentration". The two 2001 papers on regimes repeat the
argument of chapter 14 in one sentence each. The other papers use the Gini index only for the
incomes of persons. The online archive was not searched.

WHAT THE LITERATURE SAYS

  - The integral indices. "The most elegant solution is to not delineate it all, and instead use
    an integral index such as Gini or Herfindahl-Hirschman (HH). The advantage of these indices
    is that they take into account the entire distributional pattern of companies, so there is no
    need to set an arbitrary cut-off point. But integral indices also have two important
    deficiencies: they require detailed data that often do not exist, and they are difficult to
    reconcile intuitively with the binary notion of differential accumulation." The book then
    sets them aside and uses "a fixed number of firms - for example, the top 50 or 100".
  - Aggregate concentration. "Each index measures the per cent share of the top 100 firms ranked
    by market capitalization in the relevant corporate universe." "In the early 1950s, the top
    100 firms accounted for 40 per cent of all market capitalization. By the early 2000s their
    share was 60 per cent." For net profit the share rose from 23 to 53 per cent.
  - Equation (1). With s the average size of a dominant firm, n their fixed number, S the
    average size of all firms and N the number of all firms,
        aggregate concentration = (s x n) / (S x N) = (s / S) x (n / N).
    "Over time these two ratios tend to trend in opposite directions. Whereas (s/S) tends to
    increase as large firms grow bigger while small firms do not, (n/N) tends to fall since the
    number of dominant-capital firms remains fixed while the overall number of firms keeps
    rising. In many instances, the rise in N is so fast that the aggregate concentration ratio
    ends up moving sideways or even down."
  - Why the two differ in meaning. "An increase in the number of small firms causes aggregate
    concentration to decline - yet that very increase fractures the sector even further, causing
    the relative power of dominant capital to rise." "The relevant measure of power, therefore,
    is not aggregate but disaggregate. What we need to compare are not the totals, but the
    'typical' units that make up those totals - i.e. the relevant (s/S) in Equation (1)."
  - The figures. Differential capitalization against listed firms rose from "nearly 7" to
    "around 35". Differential profit against all firms rose from 1,667 to 31,325. The number of
    corporations rose "from around 600,000 in the early 1950s to over 5.5 million".
  - The opposite case. Chapter 15: "newborn firms, by their very nature, tend to be smaller than
    the average". And when only large firms are left to buy each other, "the impact on the
    group's differential accumulation relative to the average is negligible: by this stage,
    dominant capital has grown so big it is the average".
  The literature gives the share of the top hundred and the differential measure exactly. It
  names the Gini and Herfindahl-Hirschman indices and gives no formula, no figure and no chart
  for either. It describes the case in which the share falls while the differential measure
  rises. It does not describe the case the model produced, in which the share rises while the
  differential measure falls.

RULE

  1. The group. The dominant group is the hundred claims with the largest capitalization, ranked
     afresh each year, as in the book. The same group is used for every measure.
  2. The share. The share of the top hundred is the group's total divided by the total of all
     claims. It is computed for capitalization, for earnings and for employees.
  3. The differential measure. It is the average of the group divided by the average of all
     claims. It is computed for capitalization and for earnings.
  4. The number ratio. It is one hundred divided by the number of all claims. By Equation (1)
     the share equals the differential measure times the number ratio. The module publishes the
     change over the last year in the logarithm of each of the three, so the first change is
     always the sum of the other two.
  5. The Gini index. All claims are ranked by size. The index is 0 when every claim has the same
     size and approaches 1 when one claim holds everything. It is computed for capitalization
     and for earnings.
  6. The Herfindahl-Hirschman index. It is the sum, over all claims, of the square of each
     claim's share of the total. It is 1 divided by the number of claims when all are equal and
     1 when one claim holds everything. It is computed for capitalization and for earnings. The
     module also publishes 1 divided by the index, which is the number of equal claims that
     would give the same index.
  7. The counts of years apart. The module counts the years so far in which the share of the
     top hundred in capitalization fell while differential capitalization rose, which is the
     case the book describes. It counts the years in which that share rose while differential
     capitalization fell. It also counts the years in which the top hundred's share of employees
     and differential capitalization moved in opposite directions.

Every reading describes the start of the year, because a module sees only the start-of-step
ledger. The module uses no random numbers.

WHAT IS ADDED

The share of the top hundred, the differential measure, the ranking by capitalization and
Equation (1) are the book's. Everything else is an addition:
  - the formulas of the Gini and Herfindahl-Hirschman indices. They are the usual ones. The book
    names the indices and does not write them out;
  - applying the two integral indices to the whole ledger, across all industries. The
    Herfindahl-Hirschman index is commonly used inside one market. The book speaks of "the entire
    distributional pattern of companies", so the whole ledger is used here;
  - the number of equal claims that would give the same index;
  - the share of employees, which the book does not chart;
  - the three counts of years in which measures moved in opposite directions.
The module has no settings except the size of the dominant group, which is the book's hundred.

WHAT IS MISSING

The book says the integral indices are hard to reconcile with differential accumulation and
does not say how. The module can show how they move in the model. It cannot say which of them
the theory would prefer beyond what the book says of the differential measure.
"""
import os
import sys
import numpy as np
if __name__ == "__main__":     # run as a script: make the model folder importable before reading core
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core import Publish, top_positions

NOTHING = float("nan")     # published while a reading cannot yet be computed

KEYS = ("conc_claims", "conc_number_ratio",
        "conc_share_cap", "conc_share_earnings", "conc_share_employees",
        "conc_diff_cap", "conc_diff_earnings",
        "conc_gini_cap", "conc_gini_earnings",
        "conc_hh_cap", "conc_hh_earnings", "conc_hh_equal_claims",
        "conc_change_share", "conc_change_diff", "conc_change_number",
        "conc_years_share_down_diff_up", "conc_years_share_up_diff_down", "conc_years_apart_employees")


def gini(x):
    """The Gini index of the sizes in x: 0 when all are equal, near 1 when one holds everything."""
    x = np.sort(np.asarray(x, dtype=float))
    total = x.sum()
    if x.size < 2 or total <= 0 or x[0] < 0:
        return NOTHING
    rank = np.arange(1, x.size + 1)
    return float(2.0 * (rank * x).sum() / (x.size * total) - (x.size + 1.0) / x.size)


def herfindahl(x):
    """The sum of squared shares: 1/N when all are equal, 1 when one holds everything."""
    x = np.asarray(x, dtype=float)
    total = x.sum()
    if total <= 0:
        return NOTHING
    return float(((x / total) ** 2).sum())


class ConcentrationMeasures:
    name = "concentration_measures"
    reads = ()
    supplies = KEYS

    def __init__(self, top=100):
        self.top = top            # number of claims in the dominant group: the book's "top 100"
        self.before = None        # last year's logarithms of the share, the differential measure and the number ratio
        self.down_up = 0          # years so far in which the share fell while the differential measure rose
        self.up_down = 0          # years so far in which the share rose while the differential measure fell
        self.apart_employees = 0  # years so far in which the share of employees and the differential measure moved in opposite directions
        self.rows = []            # one dictionary of readings for each year, for printing

    def start(self, L):
        return {k: NOTHING for k in KEYS}

    def propose(self, L, rng):
        K, E, n = L.cap(), L.earnings(), L.n
        count = len(L)
        g = top_positions(K, np.arange(count), self.top)          # part 1: ranked by capitalization
        k = g.size
        out = {key: NOTHING for key in KEYS}
        out.update(
            conc_claims=float(count),
            conc_number_ratio=k / count,                          # part 4: n / N
            conc_share_cap=float(K[g].sum() / K.sum()),           # part 2
            conc_share_earnings=float(E[g].sum() / E.sum()),
            conc_share_employees=float(n[g].sum() / n.sum()),
            conc_diff_cap=float(K[g].mean() / K.mean()),          # part 3: s / S
            conc_diff_earnings=float(E[g].mean() / E.mean()),
            conc_gini_cap=gini(K), conc_gini_earnings=gini(E),    # part 5
            conc_hh_cap=herfindahl(K), conc_hh_earnings=herfindahl(E))   # part 6
        if out["conc_hh_cap"] > 0:
            out["conc_hh_equal_claims"] = 1.0 / out["conc_hh_cap"]

        # parts 4 and 7: the yearly changes of Equation (1), and whether the two measures parted
        now = {"share": np.log(out["conc_share_cap"]), "diff": np.log(out["conc_diff_cap"]),
               "number": np.log(out["conc_number_ratio"]), "employees": np.log(out["conc_share_employees"])}
        if self.before is not None:
            d = {key: float(now[key] - self.before[key]) for key in now}
            out.update(conc_change_share=d["share"], conc_change_diff=d["diff"],
                       conc_change_number=d["number"])
            self.down_up += d["share"] < 0 < d["diff"]
            self.up_down += d["diff"] < 0 < d["share"]
            self.apart_employees += d["employees"] * d["diff"] < 0
        self.before = now
        out.update(conc_years_share_down_diff_up=float(self.down_up),
                   conc_years_share_up_diff_down=float(self.up_down),
                   conc_years_apart_employees=float(self.apart_employees))
        self.rows.append(out)
        return [Publish(key, value, self.name) for key, value in out.items()]


if __name__ == "__main__":
    # Prints the measures every five years for a run of the nine modules with this readout added.
    import full
    argv = [int(a) for a in sys.argv[1:]]
    count, years, seed = (argv + [60_000, 60, 0][len(argv):])[:3]
    readout = ConcentrationMeasures()
    full.run(count, years, seed, modules=full.all_modules() + [readout], quiet=True)
    every = 5
    print("Each line describes the ledger at the start of the year. The last three columns are the change")
    print("over the five years before in the logarithm of the share, the differential measure and the")
    print("number ratio (capitalization). The first always equals the sum of the other two.")
    print("year   claims  share_K share_E share_n   diff_K   diff_E gini_K gini_E     hh_K equal_claims "
          "  d_share   d_diff d_number  moved    d_share_n")
    rows = readout.rows
    for i in range(0, len(rows), every):
        r = rows[i]
        if i:
            p = rows[i - every]
            ds = np.log(r["conc_share_cap"] / p["conc_share_cap"])
            dd = np.log(r["conc_diff_cap"] / p["conc_diff_cap"])
            dn = np.log(r["conc_number_ratio"] / p["conc_number_ratio"])
            tail = f"{ds:>+8.2f} {dd:>+8.2f} {dn:>+8.2f}  {'apart' if ds * dd < 0 else 'together':<8} {np.log(r['conc_share_employees'] / p['conc_share_employees']):>+8.2f}"
        else:
            tail = ""
        print(f"{full.START + i} {int(r['conc_claims']):>8} {r['conc_share_cap']:>8.2%} {r['conc_share_earnings']:>7.2%} "
              f"{r['conc_share_employees']:>7.2%} {r['conc_diff_cap']:>8.0f} {r['conc_diff_earnings']:>8.0f} "
              f"{r['conc_gini_cap']:>6.3f} {r['conc_gini_earnings']:>6.3f} {r['conc_hh_cap']:>8.5f} "
              f"{r['conc_hh_equal_claims']:>12.0f} {tail}")
    last, n = rows[-1], len(rows) - 1
    print(f"Years in which the share of capitalization fell while the differential measure rose: "
          f"{int(last['conc_years_share_down_diff_up'])} of {n}")
    print(f"Years in which the share of capitalization rose while the differential measure fell: "
          f"{int(last['conc_years_share_up_diff_down'])} of {n}")
    print(f"Years in which the share of employees and the differential measure moved in opposite directions: "
          f"{int(last['conc_years_apart_employees'])} of {n}")
