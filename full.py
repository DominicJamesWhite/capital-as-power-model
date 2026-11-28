r"""Every module of the model together, from one of three starts.

Nothing is entered by hand after the start. The model has to produce its own merger waves,
its own periods of stagflation and its own openings of boundaries.

Run from the folder that holds this file:
    python full.py [firms] [years] [seed]
        [--with name,name]    modules to run in place of others, by their names in registry.py
                              (for example envelope, in place of the boundary contest)
        [--without name,name] modules to leave out, for a test (for example failure)
        [--start name]        the conditions of the first year (see starts.py): stated (the default),
                              1950 or present. A historical start takes only its first year from the data
        [--draws]             with the stated start: each seed takes the conditions of one year of the US data,
                              picked at random from 1950 to 2025, so that results can be shown for several draws
        [--basic]             start from the basic set of ten modules in registry.py, not from every module;
                              --with then adds modules to it
        [--overlap part]     the part of a smaller premium's excess that counts in the overlap group
                             "hold on buyers": 0 (the default) means only the largest premium counts,
                             1 means the premiums multiply
        [--discounts-overlap] for comparisons only: the discounts of that group overlap as its premiums do
                             (left out, every discount counts in full)
For example:
    python full.py 30000 60 0 --with envelope
"""
import sys
import numpy as np
from core import Model, LedgerError, HOLD_ON_BUYERS, readouts, top_positions
import registry
import scorecard
import starts

START = 0      # the label of the first year of the stated start: years are counted from 0


def all_modules():
    """Every module, with its default settings, in the order in which they run."""
    return registry.make(registry.plan())


def describe(c):
    """One line that says what a start is."""
    if c["name"] == "stated" and c["drawn_from"] is None:
        return "Stated start. Years are counted from 0."
    first = (f"Stated start with the conditions of the US in {c['drawn_from']}. Years are counted from 0."
             if c["name"] == "stated" else
             f"Start from the US data of {'1950' if c['name'] == '1950' else 'the last five years'}. "
             "Only the first year is historical; every later year is made by the modules.")
    return (f"{first} Unemployment {c['unemployment']:.1%}, growth of the working population {c['growth']:.1%}, "
            f"organised employees {c['organised']:.1%}, firm sizes "
            f"{'stated' if c['sizes'] == 'stated' else 'of US employer firms in ' + str(c['sizes'])}.")


def run(count=300_000, years=119, seed=0, modules=None, every=5, quiet=False, overlap=None, discounts_overlap=(),
        start="stated", draws=False):
    c = starts.conditions(start, seed, draws)
    modules = modules or all_modules()
    starts.apply(c, modules)
    m = Model(starts.starting_ledger(seed, count, start=c), modules, seed=seed, overlap=overlap,
              discounts_overlap=discounts_overlap)
    m.start = c
    if not quiet and (c["name"] != "stated" or draws):
        print(describe(c))
        if c["name"] != "stated":
            r0 = readouts(m.L, m.top)
            E = m.L.earnings()
            top = top_positions(m.L.cap(), np.arange(len(m.L)), m.top)
            model = {"capitalist share of income": r0["capital_share"], "corporations": len(m.L),
                     "net profit of the 100 largest against the average corporation": E[top].mean() / E.mean(),
                     "part of all profit earned by the 100 largest": E[top].sum() / E.sum()}
            print("The first year against the data (results, not fed in; a run with fewer firms than the data")
            print("puts more of the whole in its 100 largest):")
            for k, v in starts.compare(c).items():
                key = "part of all profit earned by the 100 largest" if k.startswith("part of all") else k
                show = (lambda x: f"{x:.1%}") if "share" in k or "part" in k else (lambda x: f"{x:,.0f}")
                print(f"  {k}: model {show(model[key])}, data {show(v)}")
    head = ("year    firms unemp share       dk  breadth depth d_risk top_emp infl  merg/hire "
            "stagfl resist roadbl sector nation interest markup other  gain by source over the period")
    if not quiet:
        print(head)
    window, last_price = {}, m.L.accounts and 1.0
    last_price = None
    m.card = scorecard.Card()
    for step in range(1, years + 1):
        try:
            r = m.step()
        except LedgerError as stop:      # the core's guard found an impossible value, or a module broke a rule
            print(f"The run ended in year {c['year'] + step}. {stop}")
            break
        r["year"] = c["year"] + step
        r["perm_sector"], r["perm_nation"] = m.L.shared["perm_sector"], m.L.shared["perm_nation"]
        r["wage"] = m.L.shared["wage"]
        m.card.add(r)
        for s, v in r["attribution"].items():
            window[s] = window.get(s, 0.0) + v
        if step % every == 0 and not quiet:
            p, A = r["published"], m.L.accounts
            hires = p.get("new_hires", 0.0)
            ratio = p.get("merger_volume", 0.0) * r["employment"] / hires if hires > 0 else float("nan")
            prev = m.history[-1 - every]["price_level"] if len(m.history) > every else None
            infl = (r["price_level"] / prev) ** (1 / every) - 1 if prev else 0.0
            parts = ", ".join(f"{s} {v:+.2f}" for s, v in sorted(window.items()) if abs(v) >= 0.005)
            print(f"{r['year']:>4} {r['firms']:>8} {r['unemployment']:>5.1%} {r['capital_share']:>5.1%} "
                  f"{r['dk']:>8.0f} {r['breadth']:>8.0f} {r['depth']:>5.2f} {r['d_risk']:>6.2f} "
                  f"{r['top_share_employees']:>7.1%} {infl:>5.1%} {ratio:>9.2f} "
                  f"{A.get('stagflation_intensity', 0):>6.2f} {A.get('resistance', 0):>6.2f} {A.get('roadblocks', 0):>6.2f} "
                  f"{r['perm_sector']:>6.2f} {r['perm_nation']:>6.2f} {A.get('interest_share', 0):>8.1%} {r['markup']:>6.3f} {r['other_income_part']:>5.1%}  {parts}")
            window = {}
    if not quiet and m.history and m.history[-1]["transfers"]:
        last = m.history[-1]
        income = last["employment"] * last["wage"] / (1 - last["capital_share"])
        print(f"Transfers in year {last['year']}, each as a part of all income:")
        for t in last["transfers"]:
            print(f"  {t['label']}: from {t['payer']} to {t['receiver']}, asked {t['asked'] / income:.3%}, "
                  f"paid {t['paid'] / income:.3%}")
        for name, p in last["parties"].items():
            holds = "" if p["holds"] is None else f", holds {p['holds'] / income:.3%}"
            print(f"  {name}: received {p['received'] / income:.3%}, paid {p['paid'] / income:.3%}{holds}")
    if not quiet and m.card.years:
        print(f"Against US data, over the last {min(len(m.card.years), scorecard.WINDOW)} years (scorecard.py):")
        for t, got in zip(m.card.tests, m.card.results()):
            run = "not measured" if got["value"] is None else f"{got['value']:.1%}"
            us = "" if t["us"] is None else f"typical {t['us']:.1%}, "
            print(f"  {t['label']}: run {run}; US {us}{t['low']:.1%} to {t['high']:.1%} "
                  f"({t.get('range', 'the middle half of the years')}, {t['span']})")
    return m


if __name__ == "__main__":
    argv = sys.argv[1:]

    def option(flag):
        global argv
        if flag not in argv:
            return []
        i = argv.index(flag)
        names = [n for n in argv[i + 1].split(",") if n]
        argv = argv[:i] + argv[i + 2:]
        return names

    swap, without, begin = option("--with"), option("--without"), option("--start")
    draws = "--draws" in argv
    if draws:
        argv.remove("--draws")
    start = None
    if "--basic" in argv:                      # the basic set of ten modules
        argv.remove("--basic")
        start = registry.BASIC
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
    try:
        names = registry.plan(swap, without, start)
    except (KeyError, ValueError) as e:
        sys.exit(str(e).strip("'\""))
    try:
        starts.conditions(begin[0] if begin else "stated")
    except ValueError as e:
        sys.exit(str(e))
    run(count, years, seed, modules=registry.make(names), overlap=overlap, discounts_overlap=discounts_overlap,
        start=begin[0] if begin else "stated", draws=draws)
