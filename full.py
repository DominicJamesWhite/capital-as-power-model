r"""The main modules together, from the starting position of 1890.

Nothing is entered by hand after the start. The model has to produce its own merger waves,
its own periods of stagflation and its own openings of boundaries.

Run from the folder that holds this file:
    python full.py [firms] [years] [seed]
        [--with name,name]   optional modules, by their names in registry.py
        [--without name,name] main modules to leave out, by the names they give themselves (for example failure)
        [--overlap part]     the part of a smaller premium's excess that counts in the overlap group
                             "hold on buyers": 0 (the default) means only the largest premium counts,
                             1 means the premiums multiply
        [--discounts-overlap] for comparisons only: the discounts of that group overlap as its premiums do
                             (left out, every discount counts in full)
For example:
    python full.py 30000 60 --with labour
"""
import sys
import numpy as np
from core import Model, LedgerError, HOLD_ON_BUYERS
from stage2 import starting_ledger
from modules.sabotage import Sabotage
from modules.greenfield import Greenfield
from modules.mergers import Mergers
from modules.compass import Compass
from modules.stagflation import Stagflation
from modules.resistance import Resistance
from modules.envelope import Envelope
from modules.debt import Debt
from modules.costcutting import CostCutting
from modules.failure import Failure

START = 1890


def all_modules():
    return [Sabotage(), Debt(), Greenfield(), Mergers(), CostCutting(), Stagflation(),
            Compass(), Resistance(), Envelope(), Failure()]


def run(count=300_000, years=119, seed=0, modules=None, every=5, quiet=False, overlap=None, discounts_overlap=()):
    m = Model(starting_ledger(seed, count), modules or all_modules(), seed=seed, overlap=overlap,
              discounts_overlap=discounts_overlap)
    head = ("year    firms unemp share       dk  breadth depth d_risk top_emp infl  merg/hire "
            "stagfl resist roadbl sector nation interest markup other  gain by source over the period")
    if not quiet:
        print(head)
    window, last_price = {}, m.L.accounts and 1.0
    last_price = None
    for step in range(1, years + 1):
        try:
            r = m.step()
        except LedgerError as stop:      # the core's guard found an impossible value, or a module broke a rule
            print(f"The run ended in the year labelled {START + step}. {stop}")
            break
        r["year"] = START + step
        r["perm_sector"], r["perm_nation"] = m.L.shared["perm_sector"], m.L.shared["perm_nation"]
        r["wage"] = m.L.shared["wage"]
        for s, v in r["attribution"].items():
            window[s] = window.get(s, 0.0) + v
        if step % every == 0 and not quiet:
            p, A = r["published"], m.L.accounts
            hires = p.get("new_hires", 0.0)
            ratio = p.get("merger_volume", 0.0) * r["employment"] / hires if hires > 0 else float("nan")
            prev = m.history[-1 - every]["price_level"] if len(m.history) > every else None
            infl = (r["price_level"] / prev) ** (1 / every) - 1 if prev else 0.0
            parts = ", ".join(f"{s} {v:+.2f}" for s, v in sorted(window.items()) if abs(v) >= 0.005)
            print(f"{r['year']} {r['firms']:>8} {r['unemployment']:>5.1%} {r['capital_share']:>5.1%} "
                  f"{r['dk']:>8.0f} {r['breadth']:>8.0f} {r['depth']:>5.2f} {r['d_risk']:>6.2f} "
                  f"{r['top_share_employees']:>7.1%} {infl:>5.1%} {ratio:>9.2f} "
                  f"{A.get('stagflation_intensity', 0):>6.2f} {A.get('resistance', 0):>6.2f} {A.get('roadblocks', 0):>6.2f} "
                  f"{r['perm_sector']:>6.2f} {r['perm_nation']:>6.2f} {A.get('interest_share', 0):>8.1%} {r['markup']:>6.3f} {r['other_income_part']:>5.1%}  {parts}")
            window = {}
    if not quiet and m.history and m.history[-1]["transfers"]:
        last = m.history[-1]
        income = last["employment"] * last["wage"] / (1 - last["capital_share"])
        print(f"Transfers in the year labelled {last['year']}, each as a part of all income:")
        for t in last["transfers"]:
            print(f"  {t['label']}: from {t['payer']} to {t['receiver']}, asked {t['asked'] / income:.3%}, "
                  f"paid {t['paid'] / income:.3%}")
        for name, p in last["parties"].items():
            holds = "" if p["holds"] is None else f", holds {p['holds'] / income:.3%}"
            print(f"  {name}: received {p['received'] / income:.3%}, paid {p['paid'] / income:.3%}{holds}")
    return m


if __name__ == "__main__":
    import registry
    argv = sys.argv[1:]
    extra = []
    if "--with" in argv:                       # optional modules, by their names in registry.py
        i = argv.index("--with")
        extra = registry.make([n for n in argv[i + 1].split(",") if n])
        argv = argv[:i] + argv[i + 2:]
    without = set()
    if "--without" in argv:                    # main modules to leave out
        i = argv.index("--without")
        without = {n for n in argv[i + 1].split(",") if n}
        argv = argv[:i] + argv[i + 2:]
        unknown = without - {m.name for m in all_modules()}
        if unknown:
            sys.exit(f"No main module is called {', '.join(sorted(unknown))}.")
    overlap = None
    if "--overlap" in argv:                    # see the top of this file
        i = argv.index("--overlap")
        overlap = {HOLD_ON_BUYERS: float(argv[i + 1])}
        argv = argv[:i] + argv[i + 2:]
    discounts_overlap = ()
    if "--discounts-overlap" in argv:          # see the top of this file
        argv.remove("--discounts-overlap")
        discounts_overlap = (HOLD_ON_BUYERS,)
    count, years, seed = ([int(a) for a in argv] + [300_000, 119, 0][len(argv):])[:3]
    # An optional module may name modules it takes the place of, as in replaces = ("envelope",).
    replaced = {name for m in extra for name in getattr(m, "replaces", ())} | without
    run(count, years, seed, modules=[m for m in all_modules() if m.name not in replaced] + extra, overlap=overlap,
        discounts_overlap=discounts_overlap)
