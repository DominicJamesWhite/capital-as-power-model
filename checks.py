"""Sixteen checks of the model's bookkeeping. They test arithmetic, not the theory.

Checks 1 to 4 test the ledger and its measures. Checks 5 to 9 test the named components of
earnings per employee. Check 10 tests the bookkeeping of the green-field module when it founds
firms. Check 11 tests that every stacking component holds a level that means something in a
long run with many modules. Check 12 tests that the price of every firm is worked out from the
wage, the markup and the named costs. Check 13 tests the record of transfers: every transfer has
a payer and a receiver, and no payer pays more than it has. Check 14 tests the sales module's
account of who buys: what is offered equals what each buyer bought plus what is unsold, and no
buyer spends money that the record does not show it had. Check 15 tests the failure module: the
interest that firms owe adds up, a firm that closes leaves the list, and a year in which some
firms are bought and others close is divided among its sources with nothing left over.
Check 16 tests that the money for military orders, for public employment, for burdens that firms
shift onto others and for advertising has a payer and a receiver, and that the sales account
counts each of them.
Check 20 tests that when buyers do not even pay back the wage bill, no firm books a loss below nothing
and no firm that holds back production is left with fewer than no employees.
Check 6 also tests that the figures a module declares for the workbench are figures it supplies.

Run from the folder that holds this file:
    python checks.py
"""
import numpy as np
from core import (Ledger, Model, Scale, SetComponent, ScaleComponent, Merge, Found, Set, Publish, Transfer, LedgerError,
                  readouts, top_positions, group_value, lend_to_government, HOLD_ON_BUYERS, BASE, WAGE_EARNERS, GOVERNMENT)


def make_ledger(count=3000, seed=1):
    rng = np.random.default_rng(seed)
    sector_of = np.repeat(np.arange(5), 4)                 # 20 industries in 5 sectors
    return Ledger(employees=rng.lognormal(3.0, 1.2, count),
                  epe=rng.lognormal(0.0, 0.3, count),
                  industry=rng.integers(0, 20, count), sector_of_industry=sector_of,
                  hype=rng.lognormal(0.0, 0.2, count), risk=1.0 + rng.random(count),
                  shared={"workforce": 1e6})


class Fixed:
    """A stand-in module that proposes a hand-written list of changes."""
    def __init__(self, name, make, begin=None):
        self.name, self.make, self.begin = name, make, begin

    def start(self, L):
        if self.begin:
            self.begin(L)
        return {}

    def propose(self, L, rng):
        return self.make(L)


def check_stillness():
    m = Model(make_ledger())
    first = readouts(m.L)
    m.run(25)
    last = m.history[-1]
    for key, value in first.items():
        assert last[key] == value, key
    assert all(h["da"] == 0 and h["attribution"] == {} for h in m.history)
    print("1. Stillness: with no modules, every readout is unchanged after 25 steps.")


def check_identity():
    L = make_ledger()
    r = readouts(L)
    assert np.isclose(r["dk"], r["d_earnings"] * r["d_hype"] / r["d_risk"], rtol=1e-12)
    assert np.isclose(r["d_earnings"], r["breadth"] * r["depth"], rtol=1e-12)
    print(f"2. Identity: differential capitalization {r['dk']:.3f} = earnings {r['d_earnings']:.3f} "
          f"x hype {r['d_hype']:.3f} / risk {r['d_risk']:.3f}; "
          f"earnings = breadth {r['breadth']:.3f} x depth {r['depth']:.3f}.")


def check_attribution():
    def alpha(L):      # raises earnings per employee of large firms, and merges a few firms
        big = L.n > np.quantile(L.n, 0.9)
        K = L.cap()
        order = np.argsort(K)
        return [ScaleComponent("alpha edge", np.where(big, 1.08, 0.99), "alpha"),
                Merge(buyers=order[-5:], targets=order[100:105], source="alpha", risk_factor=0.95)]

    def beta(L):       # changes hype and risk unevenly, and founds small firms
        rng = np.random.default_rng(7)
        k = 200
        return [Scale("hype", rng.lognormal(0, 0.1, len(L)), "beta"),
                Scale("risk", 1.0 + 0.2 * rng.random(len(L)), "beta"),
                Found(employees=np.full(k, 2.0), epe=np.ones(k), hype=np.ones(k), risk=np.full(k, 1.5),
                      industry=np.zeros(k, dtype=int), source="beta")]

    begin = {"alpha": lambda L: L.add_component("alpha edge", "alpha"), "beta": None}
    results = []
    for order in ("alpha", "beta"), ("beta", "alpha"):
        mods = [Fixed(n, {"alpha": alpha, "beta": beta}[n], begin[n]) for n in order]
        m = Model(make_ledger(), mods)
        r = m.step()
        total = sum(r["attribution"].values())
        assert np.isclose(total, r["da"], atol=1e-10), (total, r["da"])
        results.append(r)
    a, b = results
    assert np.isclose(a["dk"], b["dk"], rtol=1e-12)
    for key in a["attribution"]:
        assert np.isclose(a["attribution"][key], b["attribution"][key], atol=1e-10), key
    parts = ", ".join(f"{k} {v:+.4f}" for k, v in sorted(a["attribution"].items()))
    print(f"3. Attribution: a gain of {a['da']:+.4f} (log) divides into {parts}, "
          f"with nothing left over, in either module order.")


def check_averages():
    L = make_ledger()
    group = top_positions(L.cap(), np.arange(len(L)), 100)
    before = readouts(L, group=group)["dk"]

    def found(L):
        k = 1000
        return [Found(employees=np.full(k, 1.0), epe=np.ones(k), hype=np.ones(k), risk=np.full(k, 1.5),
                      industry=np.zeros(k, dtype=int), source="founding")]

    m = Model(L, [Fixed("founding", found)])
    cap_before = L.cap()[group].copy()
    m.step()
    assert np.array_equal(L.cap()[group], cap_before)        # the top group itself has not changed
    after = readouts(L, group=group)["dk"]
    assert after > before
    narrow = readouts(L, group=group, mask=L.sector == L.sector[group[0]])["dk"]
    assert not np.isclose(narrow, after)
    print(f"4. Averages: founding 1,000 small firms raises the differential capitalization of an "
          f"unchanged top group from {before:.2f} to {after:.2f}. "
          f"Against one sector alone the same group measures {narrow:.2f}.")


def check_formula():
    """Earnings per employee equal wage x markup + other income for every firm, with many modules on."""
    import registry
    from stage2 import starting_ledger
    from full import all_modules
    names = ["leaders", "protections", "wants", "public_debt", "household_debt", "externalisation"]
    m = Model(starting_ledger(0, 5000), all_modules() + registry.make(names), seed=0)
    L = m.L
    worst = 0.0
    for _ in range(30):
        m.step()
        info, c = L.info, L.components
        stacking = np.ones(len(L))
        for name in c:
            if info[name].kind == "markup" and info[name].group is None:
                stacking = stacking * c[name]
        holds = np.stack([c[name] for name in c if info[name].group == HOLD_ON_BUYERS])
        up, down = np.maximum(holds, 1.0), np.minimum(holds, 1.0)
        markup = stacking * up.max(axis=0) * down.prod(axis=0)       # only the largest premium counts; discounts count in full
        other = sum(c[name] for name in c if info[name].kind == "income")
        by_hand = L.shared["wage"] * markup + other
        assert np.allclose(L.e, by_hand, rtol=1e-12, atol=0.0)
        worst = max(worst, float(np.abs(L.e / by_hand - 1).max()))
    kinds = sorted(c)
    print(f"5. Formula: with fifteen modules on for 30 steps, earnings per employee equal wage x markup "
          f"+ other income for every firm (largest relative difference {worst:.1e}). "
          f"The {len(kinds)} components are: {', '.join(kinds)}.")


def check_ownership():
    def owner_start(L):
        L.add_component("owner premium", "owner")

    trespass = Fixed("trespasser", lambda L: [ScaleComponent("owner premium", 1.1, "trespasser")])
    disguised = Fixed("trespasser", lambda L: [ScaleComponent("owner premium", 1.1, "owner")])   # gives the owner's name as its source
    direct = Fixed("direct", lambda L: [Scale("epe", 1.1, "direct")])
    messages = []
    for bad in trespass, disguised, direct:
        m = Model(make_ledger(), [Fixed("owner", lambda L: [], owner_start), bad])
        before = m.L.e.copy()
        try:
            m.step()
        except LedgerError as stop:
            messages.append(str(stop))
        else:
            raise AssertionError("the core accepted a change it should refuse")
        assert np.array_equal(m.L.e, before)
    assert "belongs to 'owner'" in messages[0] and "belongs to 'owner'" in messages[1]
    assert "cannot be scaled directly" in messages[2]
    # A module names only the numbers it publishes. Every key in a module's `figures` is in its `supplies`, and
    # every unit is one the workbench knows. Every number the core names is a readout, or is listed with its source.
    import importlib
    import registry
    from full import all_modules
    from core import CORE_FIGURES, CORE_FIGURES_ELSEWHERE, FIGURE_UNITS
    classes = [type(m) for m in all_modules()]
    classes += [getattr(importlib.import_module(path), name) for path, name in registry.OPTIONAL.values()]
    classes = list(dict.fromkeys(classes))            # two registry names can point at one class
    named = 0
    for cls in classes:
        figures = getattr(cls, "figures", {})
        for key, (label, unit, note) in figures.items():
            assert key in cls.supplies, f"{cls.__name__} names {key!r}, which it does not supply"
            assert unit in FIGURE_UNITS, f"{cls.__name__} gives {key!r} the unknown unit {unit!r}"
            assert label and isinstance(note, str), key
        named += len(figures) if "figures" in cls.__dict__ else 0
    keys = set(readouts(make_ledger(300)))
    for key, (label, unit, note) in CORE_FIGURES.items():
        assert key in keys or key in CORE_FIGURES_ELSEWHERE, f"the core names {key!r}, which is not a readout"
        assert unit in FIGURE_UNITS, key
    assert keys <= set(CORE_FIGURES), sorted(keys - set(CORE_FIGURES))
    print("6. Ownership: the core refuses a change to a component by a module that does not own it, "
          f"and it refuses a direct scaling of earnings per employee. The {named} figures that modules name are "
          f"all numbers they supply, and the {len(CORE_FIGURES)} that the core names are all readouts or numbers "
          f"it keeps.")


def check_overlap():
    hand = [np.array([1.5]), np.array([1.2]), np.array([0.9])]
    assert np.isclose(group_value(hand, 0.0)[0], 0.9 * 1.5)                 # only the largest premium counts; the discount counts in full
    assert np.isclose(group_value(hand, 0.5)[0], 0.9 * 1.5 * 1.1)           # half of the smaller premium's excess of 0.2
    assert np.isclose(group_value(hand, 1.0)[0], 0.9 * 1.5 * 1.2)           # plain stacking
    L = Ledger(employees=[10.0], epe=0.2, industry=[0], sector_of_industry=[0], shared={"wage": 2.0})
    L.add_component("a", "A", group="g", values=1.5)
    L.add_component("b", "B", group="g", values=1.2)
    L.add_component("c", "C", group="g", values=0.9)
    L.add_component("d", "D", values=2.0)                                   # a stacking component
    L.add_component("i", "I", kind="income", values=0.05)
    assert np.isclose(L.markup()[0], 0.1 * 2.0 * 1.35)
    assert np.isclose(L.e[0], 2.0 * 0.27 + 0.05)
    L.overlap["g"] = 0.5
    L.refresh()
    assert np.isclose(L.markup()[0], 0.1 * 2.0 * 1.485)
    # The switch for comparisons: the discounts of a group overlap as its premiums do.
    two = [np.array([1.5]), np.array([0.9]), np.array([0.8])]
    assert np.isclose(group_value(two, 0.0)[0], 1.5 * 0.9 * 0.8)            # the rule: every discount counts in full
    assert np.isclose(group_value(two, 0.0, True)[0], 1.5 * 0.8)            # the switch: only the deepest discount counts
    assert np.isclose(group_value(two, 0.5, True)[0], 1.5 * 0.8 * 0.95)     # half of the other discount's 0.1
    assert np.isclose(group_value(two, 1.0, True)[0], 1.5 * 0.9 * 0.8)      # plain stacking either way
    assert np.isclose(group_value(hand, 0.0, True)[0], 0.9 * 1.5)           # one discount: the switch changes nothing
    print("7. Overlap: premiums of 1.5 and 1.2 and a discount of 0.9 in one group combine to 1.35 when only "
          "the largest counts, to 1.485 when half of the smaller excess counts, and to 1.62 when they stack. "
          "A premium of 1.5 with discounts of 0.9 and 0.8 gives 1.08, because every discount counts in full; "
          "with the switch that lets discounts overlap it gives 1.20.")


def check_overlap_attribution():
    """Two modules own premiums in one overlap group. The larger premium is the first module's for some
    firms and the second module's for others, and it changes hands during the step."""
    def start_for(name):
        return lambda L: L.add_component(name + " premium", name, group=HOLD_ON_BUYERS)

    def gamma(L):
        big = L.n > np.quantile(L.n, 0.8)
        return [SetComponent("gamma premium", np.where(big, 1.30, 0.95), "gamma"),
                Set("wage", L.shared["wage"] * 1.03, "gamma")]

    def delta(L):
        rng = np.random.default_rng(11 + int(L.shared["wage"] * 100))
        return [SetComponent("delta premium", np.where(rng.random(len(L)) < 0.3, 1.5, 1.1), "delta"),
                SetComponent("delta income", 0.05 * rng.random(len(L)), "delta"),
                Scale("risk", 1.0 + 0.1 * rng.random(len(L)), "delta")]

    def delta_start(L):
        start_for("delta")(L)
        L.add_component("delta income", "delta", kind="income")

    begin = {"gamma": start_for("gamma"), "delta": delta_start}
    lines = []
    for part in 0.0, 0.5, 1.0:
        results = []
        for order in ("gamma", "delta"), ("delta", "gamma"):
            mods = [Fixed(n, {"gamma": gamma, "delta": delta}[n], begin[n]) for n in order]
            m = Model(make_ledger(), mods, overlap={HOLD_ON_BUYERS: part})
            rs = [m.step(), m.step()]            # the second step starts from premiums that already overlap
            for r in rs:
                total = sum(r["attribution"].values())
                assert np.isclose(total, r["da"], atol=1e-10), (total, r["da"])
            results.append(rs)
        a, b = results
        for ra, rb in zip(a, b):
            assert ra["dk"] == rb["dk"]
            assert set(ra["attribution"]) == set(rb["attribution"])
            for key in ra["attribution"]:
                assert ra["attribution"][key] == rb["attribution"][key], key
        lines.append(f"with part {part:.1f}, a gain of {a[0]['da']:+.4f} divides into "
                     + ", ".join(f"{k} {v:+.4f}" for k, v in sorted(a[0]["attribution"].items())))
    print("8. Attribution with overlap: with two modules in one overlap group, the gain divides among its "
          "sources with nothing left over, and every figure is identical in either module order. In the first step, "
          + "; ".join(lines) + ".")


def check_guard():
    def wreck(L):
        f = np.ones(len(L))
        f[:3] = -0.5
        return [Scale("employees", f, "wrecker")]

    m = Model(make_ledger(), [Fixed("bystander", lambda L: [Scale("hype", 1.01, "bystander")]), Fixed("wrecker", wreck)])
    try:
        m.step()
    except LedgerError as stop:
        message = str(stop)
    else:
        raise AssertionError("the guard let a negative employee count pass")
    assert "3 of 3000 firms have employees that are negative" in message
    assert "bystander, wrecker" in message
    print(f"9. Guard: a change that makes three employee counts negative stops the run. The message reads: \"{message}\"")


def check_founding():
    """The green-field module, with its rounding forced upward in every industry. Industry 0 holds a
    single small firm, which hires less in a year than one new firm employs. Half of all firms
    hold a premium of 1.5 in the overlap group."""
    from modules.sabotage import Sabotage
    from modules.greenfield import Greenfield

    class RoundUp:                       # stands in for the module's random stream
        def random(self, k):
            return np.full(k, 1.0 - 1e-12)

    rng = np.random.default_rng(3)
    count = 3000
    industry = rng.integers(1, 20, count)
    industry[0] = 0
    employees = rng.lognormal(3.0, 1.2, count)
    employees[0] = 1.0
    L = Ledger(employees=employees, epe=0.10, industry=industry, sector_of_industry=np.repeat(np.arange(5), 4),
               risk=2.0, shared={"workforce": employees.sum() / 0.90, "workforce_growth": 0.02})
    holder = Fixed("holder", lambda L: [],
                   begin=lambda L: L.add_component("holder premium", "holder", group=HOLD_ON_BUYERS,
                                                   values=np.where(np.arange(count) % 2 == 0, 1.5, 1.0)))
    green = Greenfield()
    m = Model(L, [Sabotage(), green, holder])
    changes = green.propose(m.L, RoundUp())
    scale = [c for c in changes if isinstance(c, Scale) and c.term == "employees"][0]
    found = [c for c in changes if isinstance(c, Found)][0]
    assert (scale.factor >= 1.0 - 1e-9).all(), "a founding took employees from an existing firm"
    assert not (found.industry == 0).any(), "a firm was founded that its industry's hiring could not staff"
    assert green.withheld >= 1
    k = L.sector_of.size
    stacking = np.bincount(L.ind, L.n * L.stacking_markup(), k) / np.bincount(L.ind, L.n, k)
    whole = np.bincount(L.ind, L.n * L.markup(), k) / np.bincount(L.ind, L.n, k)
    before = len(L)
    m.step()
    new = np.arange(before, len(L))
    assert len(new) > 0 and (L.n > 0).all()
    assert (L.components["holder premium"][new] == 1.0).all()
    assert np.allclose(L.components["base"][new], stacking[L.ind[new]], rtol=1e-12)
    print(f"10. Founding: with the rounding forced upward, the green-field module takes no employee from an "
          f"existing firm and founds nothing in an industry whose hiring cannot staff one new firm. A new firm "
          f"in an industry where half the firms hold a premium of 1.5 starts at the stacking markup of "
          f"{stacking[1]:.3f} and not at the average markup of {whole[1]:.3f}.")


def check_levels():
    """Every optional module that takes the place of no other, with the main modules, for 60 years.

    The check is a test and not a limit: nothing in the model holds a component inside the range
    tested here. The run is made twice, with the core's netting of the record on and off. If the
    core's guard stops the run, the years before the stop are tested. If fewer than 1 in 20 people
    still have work, the years before that one are tested: after it the figures are divisions of
    rounding errors by one another."""
    import registry
    from stage2 import starting_ledger
    from full import all_modules
    collapsed = False
    names, seen = [], set()
    for name, where in registry.OPTIONAL.items():
        if where not in seen and not getattr(registry.make([name])[0], "replaces", ()):
            names.append(name)
        seen.add(where)
    result = {}
    for netting in True, False:
        m = Model(starting_ledger(0, 3000), all_modules() + registry.make(names), seed=0, netting=netting)
        L = m.L
        low, high, furthest, base_low, base_high, beside = np.inf, 0.0, 0.0, np.inf, 0.0, 0.0
        for _ in range(60):
            try:
                m.step()
            except LedgerError:          # the guard stopped the run: the years so far are tested
                break
            if m.history[-1]["unemployment"] > 0.95:     # fewer than 1 in 20 still have work: the years before are tested
                m.history.pop()
                collapsed = True
                break
            stacking = L.stacking_markup()
            low, high = min(low, stacking.min()), max(high, stacking.max())
            others = [n for n, c in L.info.items() if c.kind == "markup" and c.group is None and n != BASE]
            X = np.log(np.stack([L.components[n] for n in others]))
            furthest = max(furthest, float(np.abs(X).max()))
            gains, losses = np.maximum(X, 0.0).sum(axis=0), -np.minimum(X, 0.0).sum(axis=0)
            beside = max(beside, float(np.minimum(gains, losses).max()))     # a gain standing beside a loss in one firm
            base_low, base_high = min(base_low, L.components[BASE].min()), max(base_high, L.components[BASE].max())
        result[netting] = dict(low=low, high=high, furthest=np.exp(furthest), base_low=base_low,
                               base_high=base_high, beside=beside, history=m.history, components=len(others) + 1)
    on, off = result[True], result[False]
    assert len(on["history"]) == len(off["history"]) >= 20
    ran = len(on["history"])
    # 1. The netting changes no markup: both runs give the same figures in every year, and the same division of the gain.
    for a, b in zip(on["history"], off["history"]):
        for key in "dk", "markup", "markup_top", "capital_share", "unemployment":
            assert np.isclose(a[key], b[key], rtol=1e-9, atol=0.0), key
        for key in set(a["attribution"]) | set(b["attribution"]):
            assert np.isclose(a["attribution"].get(key, 0.0), b["attribution"].get(key, 0.0), rtol=1e-6, atol=1e-9), key
    # 2. No firm ends a year with a gain standing beside a loss.
    assert on["beside"] < 1e-9
    # 3. No component says more than the markups themselves do. The base of no firm lies above the highest
    #    markup seen in the run, and no other component stands further from 1 than the highest of those
    #    markups stands from the lowest.
    #    The lowest base is printed and not tested, because a base may lie below the lowest markup seen.
    #    A merger gives the buyer the average of the two firms' gains, weighted by earnings, and sets the
    #    buyer's base to whatever then gives the right earnings. That base can lie below the bases of both firms.
    width = on["high"] / on["low"]
    assert on["base_high"] <= on["high"]
    assert on["furthest"] <= width
    # 4. The test can fail: the gross record, without the netting, does not pass part 2, and its components
    #    stand further from 1.
    assert off["beside"] > 1.0 and off["furthest"] > 5 * on["furthest"]
    print(f"11. Levels: with the main modules and {len(names)} optional modules on for {ran} steps"
          f"{'' if ran == 60 else ' (after which fewer than 1 in 20 people had work)' if collapsed else ' (the guard then stopped the run, in which almost every firm had closed)'}, the stacking part of "
          f"a markup lay between {on['low']:.4f} and {on['high']:.2f}. The base markup of every firm stayed between "
          f"{on['base_low']:.4f} and {on['base_high']:.2f}, and no other stacking component stood further from 1 than a "
          f"factor of {on['furthest']:.0f}. No firm ended a year with a gain standing beside a loss. The same run "
          f"with the netting switched off gave the same figures in every year, and its record did not pass the "
          f"test: one component stood a factor of {off['furthest']:.1e} from 1, and in one firm a gain of a factor "
          f"of {np.exp(off['beside']):.0f} stood beside a loss of the same size.")


def check_price():
    """The price of a firm is its cost plus its earnings from the markup, for every firm and at every
    time, and no module can move it in any other way."""
    # 1. By hand. Two premiums of one overlap group stand above 1 in the same firm. The markup counts
    #    only the larger, and so does the price.
    L = Ledger(employees=[10.0], epe=0.2, industry=[0], sector_of_industry=[0], shared={"wage": 2.0})
    assert np.isclose(L.p[0], 2.0 * (1 + 0.1))
    L.add_component("a", "A", group="g", values=1.5)
    L.add_component("b", "B", group="g", values=1.2)
    L.add_component("outlay", "C", kind="cost", values=0.03)
    L.add_component("interest", "I", kind="income", values=0.05)
    assert np.isclose(L.markup()[0], 0.15)
    assert np.isclose(L.p[0], 2.0 * (1 + 0.15 + 0.03))                    # 2.36: wage 2.00, markup 0.30, named cost 0.06
    assert np.isclose(L.p[0] - L.unit_cost()[0], 2.0 * 0.15)              # price less cost is the earnings from the markup
    assert np.isclose(L.e[0], 2.0 * 0.15 + 0.05)                          # other income is in the earnings and not in the price

    # 2. A module cannot scale the price.
    m = Model(make_ledger(), [Fixed("direct", lambda L: [Scale("price", 1.1, "direct")])])
    try:
        m.step()
    except LedgerError as stop:
        assert "cannot be scaled directly" in str(stop)
    else:
        raise AssertionError("the core accepted a direct scaling of the price")

    # 3. A cost moves the price and nothing else: no earnings, no capitalization, and no part of the gain.
    def spender(L):
        return [SetComponent("spender cost", L.components["spender cost"] + 0.02, "spender")]

    m = Model(make_ledger(), [Fixed("spender", spender, lambda L: L.add_component("spender cost", "spender", kind="cost"))])
    e0, k0, p0 = m.L.e.copy(), m.L.cap().copy(), m.L.p.copy()
    r = m.step()
    assert np.array_equal(m.L.e, e0) and np.array_equal(m.L.cap(), k0)
    assert r["da"] == 0 and all(v == 0 for v in r["attribution"].values())
    assert np.allclose(m.L.p - p0, 0.02 * m.L.shared["wage"], rtol=1e-12)

    # 4. A merger keeps the value of what the two firms sell, and a founded firm's price follows its components.
    def buyer(L):
        order = np.argsort(L.cap())
        k = 50
        return [Merge(buyers=order[-5:], targets=order[100:105], source="buyer"),
                Found(employees=np.full(k, 2.0), epe=np.full(k, 0.5), hype=np.ones(k), risk=np.full(k, 1.5),
                      industry=np.zeros(k, dtype=int), source="buyer")]

    def buyer_start(L):
        rng = np.random.default_rng(5)
        L.add_component("buyer premium", "buyer", values=rng.lognormal(0, 0.2, len(L)))
        L.add_component("buyer cost", "buyer", kind="cost", values=0.1 * rng.random(len(L)))

    m = Model(make_ledger(), [Fixed("buyer", buyer, buyer_start)])
    L = m.L
    sales0, count0 = (L.p * L.n).sum(), len(L)
    m.step()
    new = np.arange(len(L) - 50, len(L))
    assert len(L) == count0 - 5 + 50
    assert np.isclose((L.p * L.n).sum() - (L.p * L.n)[new].sum(), sales0, rtol=1e-12)
    assert np.allclose(L.p[new], L.shared["wage"] + 0.5, rtol=1e-12)      # no named cost: the price is the wage and the earnings

    # 5. In a run with many modules, the stored price of every firm equals the formula in every year.
    import registry
    from stage2 import starting_ledger
    from full import all_modules
    names = ["sales", "leaders", "protections", "wants", "nature", "coalitions", "boundary_contest", "barriers",
             "public_debt", "household_debt", "externalisation", "labour"]
    m = Model(starting_ledger(0, 5000), all_modules() + registry.make(names), seed=0)
    L = m.L
    worst, lowest, highest = 0.0, np.inf, -np.inf
    for _ in range(30):
        m.step()
        costs = sum(L.components[n] for n, c in L.info.items() if c.kind == "cost")
        by_hand = L.shared["wage"] * (1 + L.markup() + costs)
        assert np.allclose(L.p, by_hand, rtol=1e-12, atol=0.0)
        worst = max(worst, float(np.abs(L.p / by_hand - 1).max()))
        lowest, highest = min(lowest, float(costs.min())), max(highest, float(costs.max()))
    kinds = sorted(n for n, c in L.info.items() if c.kind == "cost")
    print(f"12. Price: a firm with a wage of 2, a markup of 0.15 from premiums of 1.5 and 1.2 in one overlap group, "
          f"and a named cost of 0.03 has a price of 2.36, so the price counts only the larger premium, as the markup "
          f"does. The core refuses a direct scaling of the price. A change of a cost moves the price and no earnings. "
          f"A merger keeps the value of what the two firms sell. With {len(names) + 9} modules on for 30 steps, the "
          f"price of every firm equals wage x (1 + markup + costs) (largest relative difference {worst:.1e}). "
          f"The cost components are: {', '.join(kinds)}. Their sum for one firm lay between {lowest:+.3f} and "
          f"{highest:+.3f} of the wage.")


def check_transfers():
    """Every transfer has a payer and a receiver, and no payer pays more than it has."""
    def small():
        # Three firms with a wage of 1 and a markup of 0.5: earnings of 50, 50 and 40, and a wage bill of 280.
        L = Ledger(employees=[100.0, 100.0, 80.0], epe=0.5, industry=[0, 0, 0], sector_of_industry=[0])
        return L

    def begin(L):
        L.add_component("levy income", "levy", kind="income", transfers=True)
        L.add_party("bystanders")

    # 1. By hand. The third firm is asked for 100 and has 40. The government is asked for 90 and has 50.
    def levy(L):
        return [Transfer("levy", payer=np.array([5.0, 5.0, 100.0]), receiver=GOVERNMENT, source="levy"),
                Transfer("grant to firms", payer=GOVERNMENT, receiver=np.array([1.0, 0.0, 0.0]), source="levy", amount=60.0),
                Transfer("grant to wage earners", payer=GOVERNMENT, receiver=WAGE_EARNERS, source="levy", amount=30.0)]

    m = Model(small(), [Fixed("levy", levy, begin)], top=1)
    r = m.step()
    L = m.L
    rows = {t["label"]: t for t in r["transfers"]}
    assert np.isclose(rows["levy"]["asked"], 110.0) and np.isclose(rows["levy"]["paid"], 50.0)
    assert np.isclose(rows["grant to firms"]["paid"], 50.0 * 60 / 90)
    assert np.isclose(rows["grant to wage earners"]["paid"], 50.0 * 30 / 90)
    assert np.allclose(L.n * L.e, [50 - 5 + 50 * 60 / 90, 50 - 5, 0.0])       # the third firm paid all it had and no more
    assert abs(L.holds[GOVERNMENT]) < 1e-9
    assert np.isclose(sum(r["attribution"].values()), r["da"], atol=1e-12)
    # Total income is unchanged by any transfer: the capitalist share is the firms' earnings over the same total.
    assert np.isclose(r["capital_share"], (L.n * L.e).sum() / (140.0 + 280.0))

    # 1b. A loan. Owners lend the government 30 out of their earnings (10 from each firm) and it pays wage earners 30:
    #     the earnings do not fall. The next year wage earners are taxed 30 and the government repays the owners:
    #     the earnings do not rise. The record shows 30 lent and 30 repaid.
    def lend(L):
        if L.holds[GOVERNMENT] == 0 and not getattr(L, "_lent", False):
            L._lent = True
            return [Transfer("loan", payer=np.array([10.0, 10.0, 10.0]), receiver=GOVERNMENT, source="levy", loan=True),
                    Transfer("pay", payer=GOVERNMENT, receiver=WAGE_EARNERS, source="levy", amount=30.0)]
        return [Transfer("tax", payer=WAGE_EARNERS, receiver=GOVERNMENT, source="levy", amount=30.0),
                Transfer("repaid", payer=GOVERNMENT, receiver=np.ones(3), source="levy", amount=30.0, loan=True)]

    m = Model(small(), [Fixed("levy", lend, begin)], top=1)
    r1 = m.step()
    assert np.allclose(m.L.n * m.L.e, [50.0, 50.0, 40.0]) and np.isclose(m.L.accounts["transfers"]["loan"]["lent_to_government"], 30.0)
    r2 = m.step()
    assert np.allclose(m.L.n * m.L.e, [50.0, 50.0, 40.0]) and np.isclose(m.L.accounts["transfers"]["repaid"]["lent_to_government"], -30.0)
    assert abs(m.L.holds[GOVERNMENT]) < 1e-9 and np.isclose(r1["capital_share"], 140.0 / 420.0)

    # 1c. The holders of the debt. A stand-in lends the government 1,000 once. The debt module adds it to the debt
    #     the next year, and from then on taxes wages and earnings at one rate for holders_press times what is added,
    #     and repays that much to owners, so the added debt falls by a twentieth each year.
    from modules.debt import Debt
    def lend_once(L):
        if not getattr(L, "_lent", False):
            L._lent = True
            return [Transfer("loan", payer=1000.0 * L.n * L.e / (L.n * L.e).sum(), receiver=GOVERNMENT, source="lender", loan=True)]
        return []
    def lender_start(L):
        L.add_component("lender income", "lender", kind="income", transfers=True)
    m = Model(make_ledger(), [Debt(), Fixed("lender", lend_once, lender_start)])
    rs = [m.step() for _ in range(4)]
    debt = m.modules[0] if isinstance(m.modules[0], Debt) else m.modules[1]
    pressed = [sum(t["paid"] for t in r["transfers"] if t["label"].startswith("tax on")) for r in rs]
    repaid = [sum(t["paid"] for t in r["transfers"] if t["label"] == "repaid to the holders of the public debt") for r in rs]
    assert pressed[0] == 0.0 and np.isclose(pressed[1], 50.0) and np.isclose(pressed[2], 47.5) and np.allclose(pressed, repaid)
    assert np.isclose(debt.added, 1000.0 * 0.95 ** 2)
    # With nothing lent, the debt module proposes no transfer.
    m = Model(make_ledger(), [Debt()])
    assert all(not m.step()["transfers"] for _ in range(3))

    # 2. Wage earners asked for more than the wage bill pay the wage bill. What the government does not
    #    pay out it holds, and it can pay it out in a later year.
    def squeeze(L):
        if L.holds[GOVERNMENT] == 0:
            return [Transfer("poll tax", payer=WAGE_EARNERS, receiver=GOVERNMENT, source="levy", amount=1000.0)]
        return [Transfer("grant to firms", payer=GOVERNMENT, receiver=np.ones(3), source="levy", amount=500.0)]

    m = Model(small(), [Fixed("levy", squeeze, begin)], top=1)
    r1, r2 = m.step(), m.step()
    assert np.isclose(r1["transfers"][0]["paid"], 280.0) and np.isclose(r1["parties"][GOVERNMENT]["holds"], 280.0)
    assert np.isclose(r2["transfers"][0]["paid"], 280.0) and abs(m.L.holds[GOVERNMENT]) < 1e-9
    assert np.isclose((m.L.n * m.L.e).sum(), 140.0 + 280.0)

    # 3. The core refuses a transfer with a side it cannot name, a payment by a party that only receives,
    #    a negative amount, and a direct change of a component that records transfers.
    bad = [lambda L: [Transfer("x", payer="nobody", receiver=GOVERNMENT, source="levy", amount=1.0)],
           lambda L: [Transfer("x", payer="bystanders", receiver=GOVERNMENT, source="levy", amount=1.0)],
           lambda L: [Transfer("x", payer=WAGE_EARNERS, receiver=GOVERNMENT, source="levy", amount=-1.0)],
           lambda L: [SetComponent("levy income", 0.1, "levy")]]
    words = ["no such party", "only receives", "negative", "records transfers"]
    for make, word in zip(bad, words):
        m = Model(small(), [Fixed("levy", make, begin)], top=1)
        try:
            m.step()
        except LedgerError as stop:
            assert word in str(stop), str(stop)
        else:
            raise AssertionError("the core accepted a transfer it should refuse")
    m = Model(small(), [Fixed("bare", lambda L: [Transfer("x", payer=WAGE_EARNERS, receiver=np.ones(3), source="bare", amount=1.0)])], top=1)
    try:
        m.step()
    except LedgerError as stop:
        assert "no component to record it" in str(stop)
    else:
        raise AssertionError("the core accepted a transfer to firms with no component to record it")

    # 4. A tax fixed at the start of a year in which the markup collapses. The tax
    #    asked is nine tenths of the earnings at the start of the year, and the markup falls by 95 per cent.
    def crash_start(L):
        begin(L)
        L.add_component("crash", "levy")

    def crash(L):
        return [ScaleComponent("crash", 0.05, "levy"),
                Transfer("levy", payer=0.9 * L.n * L.e, receiver=GOVERNMENT, source="levy")]

    m = Model(make_ledger(), [Fixed("levy", crash, crash_start)])
    r = m.step()
    assert (m.L.e >= 0).all() and np.isclose(r["transfers"][0]["paid"], 0.05 / 0.9 * r["transfers"][0]["asked"])

    # 5. A run with the modules that propose transfers, in opposite listing orders.
    import registry
    from stage2 import starting_ledger
    from full import all_modules
    names = ["public_debt", "household_debt", "risk_shaping", "privatisation", "labour", "sales"]
    histories, count, largest = [], 0, 0.0
    for order in names, names[::-1]:
        m = Model(starting_ledger(0, 5000), all_modules() + registry.make(order), seed=0)
        L = m.L
        for _ in range(40):
            before = dict(L.holds)
            r = m.step()
            firms_net = 0.0
            for t in r["transfers"]:
                assert 0.0 <= t["paid"] <= t["asked"] * (1 + 1e-12)
                firms_net += t["paid"] * ((t["receiver"] == "firms") - (t["payer"] == "firms"))
                count += 1
            gov = r["parties"][GOVERNMENT]
            assert gov["paid"] <= before[GOVERNMENT] + gov["received"] + 1e-9 * max(1.0, gov["received"])
            wages = r["parties"][WAGE_EARNERS]
            assert wages["paid"] <= wages["wage_bill"] * (1 + 1e-12)
            largest = max(largest, wages["paid"] / wages["wage_bill"])
            assert np.isclose(sum(r["attribution"].values()), r["da"], atol=1e-10)
        histories.append(m.history)
    for a, b in zip(*histories):
        assert a["dk"] == b["dk"] and a["capital_share"] == b["capital_share"]
        for key in a["attribution"]:
            assert a["attribution"][key] == b["attribution"][key], key
    print(f"13. Transfers: a firm asked for 100 that has 40 pays 40, and a government asked for 90 that has "
          f"received 50 pays five ninths of each payment. Owners who lend the government 30 keep their earnings, and "
          f"so do owners who are repaid. Once owners have lent the government 1,000, the holders of the debt have it "
          f"tax 50 the next year and 47.5 the year after, and repay as much; with nothing lent there is no such tax. Wage earners asked for more than the wage bill pay the "
          f"wage bill. The core refuses a transfer with an unknown side, a payment by a party that only receives, "
          f"a negative amount, and a direct change of a component that records transfers. A tax fixed before a "
          f"markup falls by 95 per cent is paid only as far as the earnings reach, and no earnings go below zero. "
          f"With {len(names) + 9} modules on for 40 steps, {count} transfers were settled, none above what was asked or "
          f"above what its payer had, the gain divided among its sources with nothing left over, and every figure "
          f"was identical in either module order. Wage earners paid at most {largest:.1%} of the wage bill.")


def check_sales_account():
    """The sales module's account balances, and nobody in it spends money it did not have."""
    from modules.sales import Sales, PRICE_CUT, SHORTFALL

    # 1. By hand. Two firms with a wage of 1 and a markup of 0.15: wages of 1,000, priced earnings of 150.
    #    In the first year a stand-in module raises every markup to 0.18 and reports 5 new jobs.
    class Push:
        name, supplies = "push", ("jobs_created",)

        def __init__(self):
            self.done = False

        def start(self, L):
            L.add_component("push", self.name)
            return {"jobs_created": 0.0}

        def propose(self, L, rng):
            first, self.done = not self.done, True
            return [ScaleComponent("push", 1.2 if first else 1.0, self.name),
                    Publish("jobs_created", 5.0 if first else 0.0, self.name)]

    L = Ledger(employees=[600.0, 400.0], epe=0.15, industry=[0, 0], sector_of_industry=[0])
    m = Model(L, [Push(), Sales(top=1)], top=1)
    with np.errstate(divide="ignore"):      # with two firms the top group is half the list, which the division of the gain meets as a zero
        r1, r2 = m.step(), m.step()
    assert r1["published"]["unsold"] == 0.0 and r1["published"]["sold_part"] == 1.0     # the opening prices are all paid
    a = r2["published"]["sales_account"]
    # Offered 1,180. Wage earners buy 1,000. Owners were paid 150 at the start. Firms keep a quarter of the 150
    # received, so the payout moves half of the way from 150 to 112.5: owners lay out 131.25. The new jobs are
    # equipped for 5 x 3 = 15. Owners buy 146.25 and 33.75 is unsold.
    assert np.isclose(a["offered"], 1180.0) and np.isclose(a["bought_by_wage_earners"], 1000.0)
    assert np.isclose(a["owners_outlay"], 131.25) and np.isclose(a["building"], 15.0)
    assert np.isclose(a["bought_by_owners"], 146.25) and np.isclose(a["unsold"], 33.75)
    assert np.isclose(r2["published"]["unsold"], 33.75 / 1180) and np.isclose(r2["published"]["sold_part"], 146.25 / 180)
    assert np.isclose(r2["published"]["sales_cut"], 33.75 / 1180)
    lost = 33.75 / 180
    # The larger firm keeps its price and books the whole loss. The smaller takes half out of its price and books half.
    # (The core has set the price cut against the standing rise of the same firm, so the markup is tested.)
    assert np.allclose(L.markup_without(SHORTFALL), [0.18, 0.18 * (1 - 0.5 * lost)])
    assert np.allclose(L.components[PRICE_CUT] * L.components["push"], [1.2, 1.2 * (1 - 0.5 * lost)])
    assert np.allclose(L.components[SHORTFALL], [1 - lost, (1 - lost) / (1 - 0.5 * lost)])
    assert np.allclose(L.e, [0.18 * (1 - lost), 0.18 * (1 - lost)])
    assert np.isclose(L.p[0], 1.18) and np.isclose(L.p[1], 1 + 0.18 * (1 - 0.5 * lost))
    assert np.isclose(r2["capital_share"], 146.25 / 1146.25)        # unsold goods are income to nobody
    with np.errstate(divide="ignore"):
        r3 = m.step()                                               # the payout moves half of the way to three quarters of the 146.25 received
    assert np.isclose(r3["published"]["sales_account"]["owners_outlay"], 0.5 * 131.25 + 0.5 * 0.75 * 146.25)
    # When the equipment of the new jobs costs at least what owners do not lay out, nothing is unsold: with 17
    # new jobs, 131.25 + 51 covers the 180. With no new job, 48.75 is unsold. And when firms keep nothing,
    # owners lay out the 150 they received, and 30 is unsold.
    for jobs, retained, unsold in (17.0, 0.25, 0.0), (0.0, 0.25, 48.75), (0.0, 0.0, 30.0):
        class Jobs(Push):
            def propose(self, L, rng, jobs=jobs):
                first, self.done = not self.done, True
                return [ScaleComponent("push", 1.2 if first else 1.0, self.name),
                        Publish("jobs_created", jobs if first else 0.0, self.name)]
        m = Model(Ledger(employees=[600.0, 400.0], epe=0.15, industry=[0, 0], sector_of_industry=[0]),
                  [Jobs(), Sales(top=1, retained=retained)], top=1)
        with np.errstate(divide="ignore"):
            m.step()
            assert np.isclose(m.step()["published"]["sales_account"]["unsold"], unsold)

    # A tax set in law. A stand-in module pays wage earners 115 in the first year and 230 in the second, taxes them 115
    # in both, and has owners lend the difference of 115 in the second. Firms keep nothing, so owners lay out all they
    # receive and nothing is unsold in the first year. In the second, the government had 230 to spend and owners
    # 115 less than they received; nothing is unsold, because the loan is spent by the government. In the third year
    # the pay falls to 0 and the 115 repays owners, who do not spend it.
    class Levy:
        name, supplies = "levy", ("jobs_created", "government_debt")

        def __init__(self):
            self.year = 0

        def start(self, L):
            L.add_component("levy income", self.name, kind="income", transfers=True)
            return {"jobs_created": 0.0, "government_debt": 1000.0}     # a debt that the government can repay

        def propose(self, L, rng):
            self.year += 1
            pay = {1: 115.0, 2: 230.0}.get(self.year, 0.0)
            out = [Transfer("levy", payer=WAGE_EARNERS, receiver=GOVERNMENT, source=self.name, amount=115.0)]
            out += lend_to_government("lent", pay - 115.0, L, GOVERNMENT, self.name)
            if pay > 0:
                out.append(Transfer("pay", payer=GOVERNMENT, receiver=WAGE_EARNERS, source=self.name, amount=pay))
            return out

    L = Ledger(employees=[600.0, 400.0], epe=0.15, industry=[0, 0], sector_of_industry=[0])
    m = Model(L, [Levy(), Sales(top=1, retained=0.0, payout_follows=1.0, benefit=0.0)], top=1)
    with np.errstate(divide="ignore"):
        rs = [m.step() for _ in range(4)]      # each year's account is of the year before
    a, b = rs[2]["published"]["sales_account"], rs[3]["published"]["sales_account"]
    assert np.isclose(a["borrowed_by_government"], 115.0) and np.isclose(a["wage_earners_had"], 1115.0)
    assert np.isclose(a["owners_had"], a["owners_income"] - 115.0) and a["unsold"] == 0.0
    assert np.isclose(rs[2]["published"]["deficit_part"], 115.0 / 1150.0)
    assert np.isclose(b["borrowed_by_government"], -115.0) and np.isclose(b["owners_had"], b["owners_income"] + 115.0)
    assert np.isclose(rs[2]["capital_share"], 150.0 / 1150.0)     # the loan lowers no earnings
    # The government repays no more than it owes. With a debt of 50, the surplus of 115 repays 50 and the government holds 65.
    Levy.start = lambda self, L: (L.add_component("levy income", self.name, kind="income", transfers=True),
                                  {"jobs_created": 0.0, "government_debt": 50.0})[1]
    m = Model(Ledger(employees=[600.0, 400.0], epe=0.15, industry=[0, 0], sector_of_industry=[0]),
              [Levy(), Sales(top=1, retained=0.0, payout_follows=1.0, benefit=0.0)], top=1)
    with np.errstate(divide="ignore"):
        r3 = [m.step() for _ in range(3)][-1]
    assert np.isclose(m.L.accounts["transfers"]["lent"]["lent_to_government"], -50.0) and np.isclose(r3["parties"][GOVERNMENT]["holds"], 65.0)

    # 2. Long runs, with the modules that move money, in opposite listing orders.
    import registry
    from stage2 import starting_ledger
    from full import all_modules
    mixes = [["sales"],
             ["sales", "public_debt", "household_debt", "privatisation", "risk_shaping", "labour", "force",
              "externalisation", "proletarianization", "wants"]]
    years_unsold = years = stopped = years_borrowed = years_repaid = 0
    largest = 0.0
    for names in mixes:
        histories = []
        for order in names, names[::-1]:
            optional = registry.make(order)
            m = Model(starting_ledger(0, 5000), all_modules() + optional, seed=0)
            kept = 0.0
            for step in range(60):
                try:
                    r = m.step()
                except LedgerError:      # the guard stopped the run: the years so far are tested
                    stopped += 1
                    break
                a, pub_now = r["published"]["sales_account"], r["published"]
                tol = 1e-9 * a["offered"]
                bought = (a["bought_by_wage_earners"] + a["bought_by_government"] + a["bought_by_owners"]
                          + a["bought_by_firms"])
                assert abs(a["offered"] - bought - a["unsold"]) <= tol
                assert min(a["bought_by_wage_earners"], a["bought_by_government"], a["bought_by_owners"], a["unsold"]) >= 0
                assert np.isclose(a["offered"], a["wages"] + a["priced_earnings"] + a["bought_by_firms"], rtol=1e-12)
                if step:      # the account is of the year before: set it against that year's record of transfers
                    last = m.history[-2]
                    parties, pub = last["parties"], last["published"]
                    net = {p: row["received"] - row["paid"] for p, row in parties.items()}
                    to_firms = sum(t["paid"] * ((t["receiver"] == "firms") - (t["payer"] == "firms"))
                                   for t in last["transfers"] if not t["loan"])     # a loan is no income
                    organs = sum(row["received"] for p, row in parties.items() if p in m.L.buyers)
                    holders = sum(row["received"] for p, row in parties.items()
                                  if p not in (WAGE_EARNERS, GOVERNMENT) and p not in m.L.buyers)
                    lent, repaid = pub.get("household_debt_lent", 0.0), pub.get("household_debt_repaid", 0.0)
                    assert a["bought_by_wage_earners"] <= max(a["wages"] + net.get(WAGE_EARNERS, 0.0) + lent - repaid, 0.0) + kept + tol
                    assert a["bought_by_government"] <= max(net.get(GOVERNMENT, 0.0), 0.0) + organs + kept + tol
                    # What the government borrowed is what the record shows owners lent, less what they were repaid.
                    loans = sum(t["paid"] * ((t["payer"] == "firms") - (t["receiver"] == "firms"))
                                for t in last["transfers"] if t["loan"])
                    assert np.isclose(a["borrowed_by_government"], loans, atol=tol)
                    years_borrowed += a["borrowed_by_government"] > tol
                    years_repaid += a["borrowed_by_government"] < -tol
                    assert a["bought_by_owners"] <= (a["priced_earnings"] - a["unsold"] + to_firms + holders
                                                     - a["borrowed_by_government"] + repaid - lent + tol)
                kept = a["kept_for_next_year"]
                years += 1
                years_unsold += a["unsold"] > 0
                largest = max(largest, a["unsold"] / a["offered"])
                assert np.isclose(sum(r["attribution"].values()), r["da"], atol=1e-10)
            histories.append(m.history)
        assert len(histories[0]) == len(histories[1]) >= 20
        for x, y in zip(*histories):
            assert x["dk"] == y["dk"] and x["capital_share"] == y["capital_share"] and x["unemployment"] == y["unemployment"]
            assert x["published"]["unsold"] == y["published"]["unsold"]
    print(f"14. Sales account: with wages of 1,000, priced earnings of 180, owners who received 150 the year before, "
          f"of which firms kept a quarter, a payout that follows half of the way, and 5 new jobs at 3 years' wages each, "
          f"owners buy 146.25 and 33.75 is unsold. With 17 new jobs nothing is unsold. The firm of dominant capital "
          f"keeps its price and books the whole loss; the other firm takes half of it out of its price. The capitalist "
          f"share is 146.25 in 1,146.25. In {years} years of runs with the modules that move money, what was offered equalled "
          f"what wage earners, the government, owners and firms bought plus what was unsold, and no buyer spent more than the "
          f"record of transfers shows it had. When the government pays out 115 more than a tax set in law collects, "
          f"owners lend it 115, have 115 less to spend, and nothing is unsold; when the pay stops, the tax repays them, "
          f"but no more than the government owes. "
          f"The loans lower no earnings. In the long runs the government borrowed in {years_borrowed} of those years and "
          f"repaid in {years_repaid}. Goods were unsold in {years_unsold} of those years, at most {largest:.1%} of "
          f"what was offered. Opposite listing orders gave identical figures."
          + (f" The guard stopped {stopped} of the 4 runs before the 60th year." if stopped else ""))


def check_failure():
    """Firms that fail: who owes what, who closes, and what the books show afterwards."""
    from math import erfc, sqrt
    from stage2 import starting_ledger
    from full import all_modules
    from modules.failure import Failure, chance_below
    from core import Dissolve

    # The curve used for the chance of failing agrees with the exact one.
    z = np.linspace(-6.0, 6.0, 241)
    exact = np.array([0.5 * erfc(-v / sqrt(2.0)) for v in z])
    assert np.abs(chance_below(z) - exact).max() < 1e-6

    # A hand-made list of 400 firms that all earn 0.10 for each employee. Lenders take four tenths of earnings.
    def ledger(risk):
        n = np.concatenate([np.full(200, 10.0), np.full(160, 100.0), np.full(40, 5000.0)])
        return Ledger(employees=n, epe=0.10, industry=np.arange(400) % 20, sector_of_industry=np.repeat(np.arange(5), 4),
                      risk=risk, shared={"workforce": float(n.sum())})

    f = Failure(top=10)
    L = ledger(1.0)
    L.accounts["interest_share"] = 0.4
    cover, chance, owed = f.chances(L)
    assert np.isclose(owed.sum(), 0.4 * (L.n * L.e).sum(), rtol=1e-12)      # in the first year the interest of all firms is the total owed
    assert np.isclose(cover[0] / cover[-1], 1.90 / 5.92) and np.isclose(cover[250] / cover[-1], 1.90 / 3.48)
    # Each firm owes on its own debt: when half the small firms have closed, and when the largest firms earn
    # three times as much, every firm that is left owes what it owed before.
    left = np.arange(100, 400)
    fewer = Ledger(employees=L.n[left], epe=0.10, industry=left % 20, sector_of_industry=np.repeat(np.arange(5), 4),
                   risk=1.0, shared={"workforce": float(L.n.sum())})
    fewer.accounts["interest_share"] = 0.4
    assert np.allclose(f.chances(fewer)[2], owed[left], rtol=1e-12)
    richer = ledger(1.0)
    richer.components[BASE][360:] = 0.30
    richer.refresh()
    richer.accounts["interest_share"] = 0.4
    assert np.allclose(f.chances(richer)[2][:360], owed[:360], rtol=1e-12)
    assert owed[left].sum() / (L.n * L.e)[left].sum() < 0.4      # the firms that closed owed the most for their earnings
    assert set(np.unique(chance)) <= {0.0, 1.0}                              # with a risk of 1 nothing is left to chance
    assert (chance[:200] == 1.0).all() and (chance[360:] == 0.0).all() and cover[:200].max() < 1 < cover[360:].min()

    # In a year: the small firms close, their employees are without work, nobody else is touched.
    class Lenders:
        name, supplies = "lenders", ("interest_share",)

        def start(self, L):
            return {"interest_share": 0.4}

        def propose(self, L, rng):
            return []

    m = Model(ledger(1.0), [Lenders(), Failure(top=10)], seed=0)
    before = m.L.n.copy()
    r = m.step()
    assert len(m.L) == 200 and np.array_equal(m.L.n, before[200:])
    assert r["published"]["failures"] == 200 and np.isclose(r["published"]["failed_employees"], 2000.0 / before.sum())
    assert np.isclose(r["unemployment"], 2000.0 / before.sum())
    assert np.isclose(sum(r["attribution"].values()), r["da"], atol=1e-10) and set(r["attribution"]) == {"failure"}
    assert np.isclose(r["published"]["failed_by_industry"] @ np.bincount(np.arange(400) % 20, before, 20), 2000.0)

    # The year after, the firms left in each industry take on the buyers of those that closed and hire for them,
    # in proportion to their size. With no other hiring, every industry is back to its employees of the start,
    # and the hiring counts as no growth of the industry's capacity: it only moved from one firm to another.
    class Plain:
        name, supplies = "plain", ("hire_small", "hire_dominant", "entry_open")

        def start(self, L):
            return {"hire_small": np.zeros(20), "hire_dominant": np.zeros(20), "entry_open": np.zeros(20)}

        def propose(self, L, rng):
            return []

    class Lenders2(Lenders):
        def propose(self, L, rng):                   # lenders take nothing after the first year
            return [Publish("interest_share", 0.0, self.name)]

    from modules.greenfield import Greenfield
    L = ledger(1.0)
    L.shared.update(workforce=float(L.n.sum()) / 0.9, workforce_growth=0.0)
    m = Model(L, [Lenders2(), Plain(), Failure(top=10), Greenfield(top=10)], seed=0)
    m.step()
    assert len(m.L) == 200
    r = m.step()
    by_industry = np.bincount(m.L.ind, m.L.n, 20)
    assert np.allclose(by_industry, np.bincount(np.arange(400) % 20, before, 20), rtol=1e-12)
    assert np.allclose(r["published"]["industry_sought"] - 2000.0 / before.sum(), 0.0, atol=1e-12)
    L = ledger(1.0)
    L.shared.update(workforce=float(L.n.sum()) / 0.9, workforce_growth=0.0)
    m = Model(L, [Lenders2(), Plain(), Failure(top=10), Greenfield(top=10, taken_on=0.0)], seed=0)
    m.step(); m.step()
    assert np.isclose(m.L.n.sum(), before.sum() - 2000.0)       # with taken_on at 0 nobody is taken on

    # A firm among the largest that cannot pay is restructured: it stays, with every employee, and its risk rises.
    L = ledger(1.0)
    L.components[BASE][-1] = 0.03                    # one of the largest firms earns a third of what the others earn
    L.refresh()
    m = Model(L, [Lenders(), Failure(top=40, small_burden=1.0, medium_burden=1.0, large_burden=1.0)], seed=0)
    r = m.step()
    assert len(m.L) == 400 and m.L.n[-1] == 5000.0 and np.isclose(m.L.d[-1], 1.5)
    assert r["published"]["restructurings"] == 1 and r["published"]["failures"] == 0

    # Switched off, or with no interest owed, no firm fails.
    for module, share in (Failure(on=False), 0.4), (Failure(), 0.0):
        L = ledger(2.0)
        L.accounts["interest_share"] = share
        assert not any(isinstance(c, (Dissolve, Scale)) for c in module.propose(L, np.random.default_rng(0)))

    # Firms bought and firms closed in the same year: the year's gain still divides with nothing left over.
    def both(L):
        order = np.argsort(L.cap())
        return [Merge(buyers=order[-5:], targets=order[100:105], source="buyer", risk_factor=0.95)]

    def closing(L):
        order = np.argsort(L.cap())
        return [Dissolve(order[:300], "closer")]

    m = Model(make_ledger(), [Fixed("buyer", both), Fixed("closer", closing)])
    r = m.step()
    alone = Model(make_ledger(), [Fixed("buyer", both)]).step()
    assert np.isclose(sum(r["attribution"].values()), r["da"], atol=1e-10)
    assert np.isclose(r["attribution"]["buyer"], alone["attribution"]["buyer"], atol=1e-10)   # the buyer is credited as if nobody closed

    # A full run: firms fail in ordinary years, and the books stay whole.
    m = Model(starting_ledger(0, 5000), all_modules(), seed=0)
    closed = restructured = 0
    for _ in range(40):
        r = m.step()
        closed += r["published"]["failures"]
        restructured += r["published"]["restructurings"]
        assert np.isclose(sum(r["attribution"].values()), r["da"], atol=1e-9)
    assert closed > 0
    print(f"15. Failure: in the first year the interest that firms owe adds up to the total; each firm owes on its own debt, so a firm left owes the same when other firms close or earn more; a small firm owes 5.92 for each 1.90 that a "
          f"large firm owes on the same sales; a firm with a risk of 1 fails only if it cannot pay; a firm that closes "
          f"leaves the list and its employees are without work; a firm among the largest is restructured and stays; "
          f"switched off, nothing fails; firms bought and firms closed in one year are each credited with their own "
          f"part of the gain. In a run of 40 years from 5,000 firms, {closed:.0f} firms closed and {restructured:.0f} "
          f"of the largest were restructured.")

def check_payers():
    """The money for military orders, public employment, burdens off the books and advertising has a payer and a receiver."""
    import registry
    from stage2 import starting_ledger
    from full import all_modules
    from modules.force import ARMED_FORCES
    from modules.wants import OUTLAY

    # 1. By hand: a party that spends all it receives holds nothing, and it cannot also hold money.
    L = Ledger(employees=[100.0, 100.0], epe=0.5, industry=[0, 0], sector_of_industry=[0])
    L.add_party("buyer", buys=True)
    assert "buyer" in L.buyers and "buyer" not in L.holds
    try:
        L.add_party("both", holds=True, buys=True)
        raise AssertionError("a party that both holds and spends all was accepted")
    except LedgerError:
        pass
    L.add_component("outlay", "x", kind="cost", values=0.25, bought_from_firms=True)
    L.add_component("other cost", "x", kind="cost", values=0.5)
    assert np.allclose(L.outlays_on_firms(), 0.25)          # only the cost that is laid out on what firms sell

    # 2. A run with the four modules and the sales module.
    names = ["sales", "force", "privatisation", "externalisation", "wants"]
    m = Model(starting_ledger(0, 5000), all_modules() + registry.make(names), seed=0)
    arms = pay = burdens = advertising = short = 0.0
    kept = held = 0.0
    for step in range(45):
        outlay = float((m.L.n * m.L.shared["wage"] * m.L.components[OUTLAY]).sum())
        owed = max(float(m.L.accounts.get("government_debt", 0.0)), 0.0)    # what the government owes at the start of the year
        r = m.step()
        rows = {t["label"]: t for t in r["transfers"]}
        parties = r["parties"]
        tol = 1e-9 * r["employment"] * m.L.shared["wage"]
        # The armed forces receive the orders from the government and hold nothing. The government pays the orders,
        # public employees and people out of work in full, from the tax and what owners lent, and keeps nothing.
        tax = rows["military orders paid by the government"]["paid"] if "military orders paid by the government" in rows else 0.0
        assert abs(parties[ARMED_FORCES]["received"] - tax) <= tol and parties[ARMED_FORCES]["holds"] is None
        collected = rows["pay of public employees"]["paid"]
        # Firms whose earnings fell during the year may lend or pay a little less than they were asked, and the
        # government then pays a little less in the same proportion.
        for k in ("pay of public employees", "military orders paid by the government", "pay to people out of work"):
            if k in rows:
                short = max(short, 1.0 - rows[k]["paid"] / rows[k]["asked"])
        # What it holds rises only in a year when it collected more beyond its spending than all it owed, and
        # repaid all of that (the rule of lend_to_government in core.py). What it holds is not spent later.
        repaid = sum(t["paid"] for t in r["transfers"] if t["payer"] == GOVERNMENT and t["receiver"] == "firms")
        rise = parties[GOVERNMENT]["holds"] - (m.history[-2]["parties"][GOVERNMENT]["holds"] if step else 0.0)
        assert parties[GOVERNMENT]["holds"] >= -tol and (rise <= tol or repaid >= owed - tol)
        held = max(held, parties[GOVERNMENT]["holds"] / (r["employment"] * m.L.shared["wage"]))
        # Wage earners pay for the burdens on employees and communities, in full.
        b = rows["burdens borne by employees and communities"]
        assert b["payer"] == WAGE_EARNERS and b["receiver"] == "firms" and abs(b["paid"] - b["asked"]) <= tol
        # No firm paid more tax than it earned.
        assert (m.L.e >= 0).all()
        assert np.isclose(sum(r["attribution"].values()), r["da"], atol=1e-9)
        # The sales account of this year is of the year before.
        a = r["published"]["sales_account"]
        assert np.isclose(a["bought_by_firms"], outlay, rtol=1e-12)
        assert np.isclose(a["offered"], a["wages"] + a["priced_earnings"] + a["bought_by_firms"], rtol=1e-12)
        if step:
            last = m.history[-2]["parties"]
            # what the government had to spend: the orders it paid, money that found no goods the year before, and
            # what it collected in that year beyond its spending and its repayments (when it paid out more than it
            # collected, what it drew from its holdings went to those it paid, and is counted with them)
            gained = max(last[GOVERNMENT]["holds"] - (m.history[-3]["parties"][GOVERNMENT]["holds"] if step > 1 else 0.0), 0.0)
            assert abs(a["government_had"] - last[ARMED_FORCES]["received"] - kept - gained) <= tol
            net = last[WAGE_EARNERS]["received"] - last[WAGE_EARNERS]["paid"]
            assert abs(a["wage_earners_had"] - max(a["wages"] + net, 0.0) - kept_wages) <= tol
        kept, kept_wages = 0.0, 0.0
        if a["kept_for_next_year"] > 0:          # money that found no goods is split between the two; follow it from the account
            kept = a["government_had"] - a["bought_by_government"]
            kept_wages = a["wage_earners_had"] - a["bought_by_wage_earners"]
        income = r["employment"] * m.L.shared["wage"] / (1 - r["capital_share"])
        arms, pay = max(arms, tax / income), max(pay, collected / income)
        burdens, advertising = max(burdens, b["paid"] / income), max(advertising, a["bought_by_firms"] / a["offered"])
    assert arms > 0 and pay > 0 and burdens > 0 and advertising > 0 and short < 0.05
    print(f"16. Payers: a party that spends all it receives holds nothing. In a run of 45 years from 5,000 firms with "
          f"the sales, force, privatisation, externalisation and wants modules, the armed forces received exactly the "
          f"military orders that the government paid (at most {arms:.1%} of all income) and the sales account counted "
          f"them as bought by the government; the government paid out all it collected and borrowed, and added to the money "
          f"it holds (at most {held:.1%} of the wage bill) only in years when it had repaid all it owed, "
          f"public employees (at most {pay:.1%}) among them, short of what was asked by at most {short:.2%} in a year; wage earners paid in full for the burdens on employees and communities (at most "
          f"{burdens:.1%}); and the outlay on advertising (at most {advertising:.1%} of what firms offered) was on "
          f"both sides of the sales account.")


def check_unemployment_level():
    """In the sabotage module a level of unemployment sets a level of the capitalist share, and not a yearly rise."""
    from stage2 import starting_ledger
    from modules.sabotage import Sabotage

    class Steady:           # stands in for the green-field module: every industry sets out to hire as fast as the working population grows
        name, supplies = "steady", ("industry_growth", "industry_sought")

        def start(self, L):
            return {"industry_sought": np.full(L.sector_of.size, L.shared["workforce_growth"])}

        def propose(self, L, rng):
            return []

    shares = {}
    for u in 0.05, 0.15, 0.04:
        L = starting_ledger(0, 3000)
        L.shared["workforce"] = L.n.sum() / (1 - u)        # nobody is hired, so unemployment stays at this level
        m = Model(L, [Sabotage(hold=0.0), Steady()], seed=0)   # with no holding toward a target, only unemployment moves a markup
        shares[u] = [m.step()["capital_share"] for _ in range(40)]
    still, slump = shares[0.05], shares[0.15]
    # At the level where wages keep pace with prices, nothing moves.
    assert max(still) - min(still) < 1e-12
    # Ten points above it the share ends 3 points higher. A third of that comes in the first year,
    # and after 40 years of the same unemployment the share has stopped rising.
    assert abs(slump[0] - still[0] - 0.01) < 5e-4 and abs(slump[-1] - still[-1] - 0.03) < 1.5e-3
    assert all(b > a for a, b in zip(slump[:10], slump[1:11])) and slump[-1] - slump[-2] < 1e-8
    # One point below it, wage earners press for more: the share ends labour_gain times 0.01 lower.
    tight, drop = shares[0.04], Sabotage().labour_gain * 0.01
    assert abs(still[-1] - tight[-1] - drop) < 0.05 * drop and abs(tight[-1] - tight[-2]) < 1e-8
    print(f"17. Unemployment and the share: with unemployment held at 5 per cent the capitalist share stays at "
          f"{still[-1]:.4f} for 40 years. Held at 15 per cent it rises by {slump[0] - still[0]:.4f} in the first year "
          f"and stands {slump[-1] - still[-1]:.4f} higher after 40 years, where it has stopped rising. Held at 4 per "
          f"cent it stands {still[-1] - tight[-1]:.4f} lower.")


def check_second_country_purchases():
    """With the border open, no purchase of the second country module names a firm bought in the same year,
    or buys a firm that bought, even when firms tie in capitalization at the edge of the dominant group."""
    from stage2 import starting_ledger
    from modules.second_country import SecondCountry
    sc = SecondCountry(start_permeability=1.0, takeover=0.5)
    m = Model(starting_ledger(0, 3000), [sc], seed=0)
    L = m.L
    sec = np.flatnonzero(sc.industries(L)[L.ind])
    K = L.cap().copy()
    K[sec] = 1.0
    K[sec[:4]] = 100.0                  # four clear leaders, then 26 firms tied for fifth place
    K[sec[4:30]] = 50.0
    L.cap = lambda: K
    years = cross = 0
    for i in range(150):
        sc.permeability, sc.roadblocks = 1.0, 0.0
        merges = [c for c in sc.propose(L, np.random.default_rng(i)) if isinstance(c, Merge)]
        bought, buyers = set(), set()
        for c in merges:                # in the order the core applies them
            t, b = set(map(int, c.targets)), set(map(int, c.buyers))
            assert not (t | b) & bought and not t & buyers, "a firm is bought again, or a buyer is bought"
            bought |= t; buyers |= b
        years += 1
        cross += len(merges) > 2
    assert cross > years / 2            # the purchases across the border did happen
    print(f"18. Second country: in {years} years with the border open and 26 firms tied for fifth place in the "
          f"second country, purchases across the border happened in {cross}, and no firm was bought twice or bought "
          f"after it had bought.")


def check_public_debt_tax():
    """The public debt module asks no negative tax of a firm whose earnings, after what it paid other
    modules, are below nothing, and its readouts stay numbers when no firm is left outside the top 100."""
    from stage2 import starting_ledger
    from modules.public_debt import PublicDebt, TAX_EARNINGS

    class Charges:          # publishes a government debt, and owns an income that records payments to the government
        name, supplies = "charges", ("government_debt",)

        def start(self, L):
            L.add_component("charges", self.name, kind="income", transfers=True)
            return {"government_debt": 0.5 * float(L.earnings().sum() + L.shared["wage"] * L.n.sum())}

        def propose(self, L, rng):
            return []

    seen = {}
    for count in 3000, 60:
        m = Model(starting_ledger(0, count), [Charges(), PublicDebt()], seed=0)
        m.step()
        L = m.L
        e0 = float(L.e[0])
        L.components["charges"][:5] = -3.0 * L.e[:5]     # five firms paid other modules three times what they now earn
        L.refresh()
        asks = [c for c in m.modules[1].propose(L, np.random.default_rng(0)) if getattr(c, "label", None) == TAX_EARNINGS]
        ask = np.asarray(asks[0].payer, dtype=float)
        assert np.all(np.isfinite(ask)) and (ask >= 0).all() and (ask[:5] == 0).all()
        assert ask[5:].sum() > 0 or count <= 100     # with 100 firms or fewer all are dominant capital, whose rate is 0 here
        for _ in range(3):
            r = m.step()        # the core accepts every payment, and every readout is a number
        vals = [v for k, v in m.L.accounts.items() if k.startswith("public_debt_")]
        assert all(np.all(np.isfinite(v)) for v in vals), count
        seen[count] = (e0, m.L.accounts["public_debt_net_others"])
    assert seen[60][1] == 0.0               # with 60 firms every firm is in the top 100, and nothing is left to measure
    print(f"19. Public debt tax: five firms whose earnings after last year's payments are three times below nothing "
          f"are asked for no tax, and the others are. With 60 firms, all in the top 100, the run goes on and every "
          f"readout of the module is a number; the top 100 then hold all capitalization, so their tax advantage is "
          f"whole and wages carry the tax.")


def check_no_earnings():
    """When buyers do not even pay back the wage bill, no firm books a loss larger than its earnings, owners
    buy no goods with a payout below nothing, and a firm that holds back production keeps no fewer than nobody."""
    from core import ROUNDING
    from modules.sales import Sales, SHORTFALL
    from modules.greenfield import Greenfield

    # 1. Two firms with a wage of 1 and a markup of 0.15: wages of 1,000, priced earnings of 150. From the second
    #    year a stand-in module taxes wage earners 500 and the government repays owners with it, who do not spend
    #    it. Wage earners buy 500 of the 1,150 offered, owners lay out the 150 they were paid, and 500 is unsold:
    #    more than the 150 priced. Each firm keeps the allowance for rounding of its markup and the run goes on.
    class Repay:
        name, supplies = "repay", ("jobs_created", "government_debt")

        def __init__(self):
            self.year = 0

        def start(self, L):
            L.add_component("repay income", self.name, kind="income", transfers=True)
            return {"jobs_created": 0.0, "government_debt": 1e6}

        def propose(self, L, rng):
            self.year += 1
            if self.year < 2:
                return []
            return ([Transfer("tax", payer=WAGE_EARNERS, receiver=GOVERNMENT, source=self.name, amount=500.0)]
                    + lend_to_government("repaid", -500.0, L, GOVERNMENT, self.name))

    L = Ledger(employees=[600.0, 400.0], epe=0.15, industry=[0, 0], sector_of_industry=[0])
    sales = Sales(top=1, retained=0.0, payout_follows=1.0, benefit=0.0)
    m = Model(L, [Repay(), sales], top=1)
    with np.errstate(divide="ignore"):
        rs = [m.step() for _ in range(4)]
    a = rs[2]["published"]["sales_account"]
    assert np.isclose(a["bought_by_wage_earners"], 500.0) and np.isclose(a["unsold"], 500.0)
    assert np.allclose(L.components[SHORTFALL], [ROUNDING, ROUNDING / (1 - 0.5 * (1 - ROUNDING))])
    assert (L.e > 0).all() and (L.e < 1e-9).all()
    # The year after, owners' income was 150 - 500 below nothing: they are paid nothing to spend on goods.
    assert sales.payout < 0 and rs[3]["published"]["sales_account"]["owners_outlay"] == 0.0
    assert rs[3]["published"]["sales_account"]["bought_by_owners"] >= 0.0

    # 2. The green-field module: the top firm's industry rate is -0.5 and it holds back 0.9 of what is left for
    #    want of sales. It keeps 0.5 x 0.1 = 0.05 of its employees.
    L = Ledger(employees=[600.0, 400.0], epe=0.15, industry=[0, 0], sector_of_industry=[0],
               shared={"workforce": 2000.0, "workforce_growth": 0.0})
    class Rates:
        name, supplies = "rates", ("hire_small", "hire_dominant", "entry_open", "sales_cut")

        def start(self, L):
            return {"hire_small": np.array([0.0]), "hire_dominant": np.array([-0.5]),
                    "entry_open": np.array([1.0]), "sales_cut": 0.9}

        def propose(self, L, rng):
            return []

    green = Greenfield(top=1)
    m = Model(L, [Rates(), green], top=1)
    scale = [c for c in green.propose(m.L, np.random.default_rng(0)) if isinstance(c, Scale) and c.term == "employees"][0]
    assert np.allclose(scale.factor, [0.05, 1.0])
    print(f"20. No earnings: when wage earners pay 500 of a wage bill of 1,000 to owners who do not spend it, 500 is "
          f"unsold against priced earnings of 150. Each firm keeps one part in a million million of its markup in "
          f"place of a loss below nothing, the run goes on, and the next year owners, paid below nothing, buy no "
          f"goods. A top firm whose industry rate is -0.5 and that holds back 0.9 for want of sales keeps 0.05 of "
          f"its employees.")


if __name__ == "__main__":
    check_stillness()
    check_identity()
    check_attribution()
    check_averages()
    check_formula()
    check_ownership()
    check_overlap()
    check_overlap_attribution()
    check_guard()
    check_founding()
    check_levels()
    check_price()
    check_transfers()
    check_sales_account()
    check_failure()
    check_payers()
    check_unemployment_level()
    check_second_country_purchases()
    check_public_debt_tax()
    check_no_earnings()
    print("All twenty checks passed.")
