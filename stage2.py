"""Three modules alone: sabotage, green-field growth and mergers.

Four runs from the same starting position, to see what each module adds.
Each run of 80 years takes about two minutes at 300,000 starting firms.
  A. green-field growth and sabotage only;
  B. the same with mergers, every boundary beyond the industry closed;
  C. as B, with the sector boundary opened by hand in year 40 (a what-if run);
  E. as B, with the modules listed in the opposite order.

Run from the folder that holds this file:
    python stage2.py [firms]
"""
import numpy as np
from core import Ledger, Model, LedgerError
from modules.sabotage import Sabotage
from modules.greenfield import Greenfield
from modules.mergers import Mergers

YEARS = 80
COLUMNS = [("firms", "firms", "{:>7.0f}"), ("unemployment", "unemp", "{:>6.1%}"),
           ("capital_share", "share", "{:>6.1%}"), ("dk", "dk", "{:>7.1f}"),
           ("breadth", "breadth", "{:>7.1f}"), ("depth", "depth", "{:>6.2f}"),
           ("d_risk", "d_risk", "{:>6.2f}"), ("top_share_employees", "top_emp", "{:>7.1%}"),
           ("price_level", "prices", "{:>6.3f}")]


COUNT = 300_000      # about the number of United States corporations in the 1910s


def starting_ledger(seed=0, count=None, industries=400, sectors=20):
    """Many small firms of similar size: the book's 'golden age of free competition'."""
    count = count or COUNT
    rng = np.random.default_rng(seed)
    employees = rng.lognormal(np.log(100), 0.8, count)
    sab = Sabotage()
    u0 = sab.labour_holds_at     # start where wages keep pace with prices
    return Ledger(employees=employees, epe=sab.normal_markup, risk=2.0,
                  industry=rng.integers(0, industries, count),
                  sector_of_industry=np.arange(industries) % sectors,
                  shared={"workforce": employees.sum() / (1 - u0), "workforce_growth": 0.017,
                          "perm_sector": 0.0, "perm_nation": 0.0})


def run(label, modules, events=None, seed=0):
    m = Model(starting_ledger(seed), modules, seed=seed)
    print(f"\n{label}")
    print("year " + " ".join(f"{h:>7}" if "7" in f else f"{h:>6}" for _, h, f in COLUMNS)
          + "  mergers/hires  gain by source over the last ten years")
    window = {}
    for year in range(1, YEARS + 1):
        for key, value in (events or {}).get(year, {}).items():
            m.L.shared[key] = value
        try:
            r = m.step()
        except LedgerError as stop:      # the core's guard found an impossible value; report it and end this run
            print(f"  The run ended in year {year}. {stop}")
            break
        for s, v in r["attribution"].items():
            window[s] = window.get(s, 0.0) + v
        if year % 10 == 0:
            pub = r["published"]
            hires = pub.get("new_hires", 0.0)
            ratio = pub.get("merger_volume", 0.0) * r["employment"] / hires if hires > 0 else float("nan")
            parts = ", ".join(f"{s} {v:+.2f}" for s, v in sorted(window.items()) if abs(v) >= 0.005)
            print(f"{year:>4} " + " ".join(f.format(r[k]) for k, _, f in COLUMNS)
                  + f"  {ratio:>12.2f}   {parts}")
            window = {}
    return m


def mods(order=(0, 1, 2), **merger_settings):
    made = [Sabotage(), Greenfield(), Mergers(**merger_settings)]
    return [made[i] for i in order]


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        COUNT = int(sys.argv[1])
    run("A. Green-field growth and sabotage", mods()[:2])
    b = run("B. With mergers, closed at the industry", mods())
    run("C. As B, sector boundary opened by hand in year 40 (what-if)", mods(),
        events={40: {"perm_sector": 1.0}})
    if COUNT <= 50_000:        # the order check is run at a small count, where it is quick
        e = run("E. As B, modules listed in the opposite order", mods(order=(2, 1, 0)))
        same = all(x["dk"] == y["dk"] for x, y in zip(b.history, e.history))
        print()
        print(f"B and E give identical differential capitalization in every year: {same}")
