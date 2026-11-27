"""Fourteen checks of the model's bookkeeping. They test arithmetic, not the theory.

Checks 1 to 4 test the ledger and its measures. Checks 5 to 9 test the named components of
earnings per employee. Check 10 tests the bookkeeping of the green-field module when it founds
firms. Check 11 tests that every stacking component holds a level that means something in a
long run with many modules. Check 12 tests that the price of every firm is worked out from the
wage, the markup and the named costs. Check 13 tests the record of transfers: every transfer has
a payer and a receiver, and no payer pays more than it has. Check 14 tests the sales module's
account of who buys: what is offered equals what each buyer bought plus what is unsold, and no
buyer spends money that the record does not show it had.
Check 6 also tests that the figures a module declares for the workbench are figures it supplies.

Run from the folder that holds this file:
    python checks.py
"""
import numpy as np
from core import (Ledger, Model, Scale, SetComponent, ScaleComponent, Merge, Found, Set, Publish, Transfer, LedgerError,
                  readouts, top_positions, group_value, HOLD_ON_BUYERS, BASE, WAGE_EARNERS, GOVERNMENT)


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
    """Every optional module that takes the place of no other, with the nine modules, for 60 years.

    The check is a test and not a limit: nothing in the model holds a component inside the range
    tested here. The run is made twice, with the core's netting of the record on and off."""
    import registry
    from stage2 import starting_ledger
    from full import all_modules
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
            m.step()
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
    # 4. The test can fail: the gross record, without the netting, does not pass it.
    assert off["furthest"] > width and off["beside"] > 1.0
    print(f"11. Levels: with the nine modules and {len(names)} optional modules on for 60 steps, the stacking part of "
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
          f"received 50 pays five ninths of each payment. Wage earners asked for more than the wage bill pay the "
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
    # Offered 1,180. Wage earners buy 1,000. Owners lay out last year's 150 and 5 x 4 = 20 for the new jobs. 10 is unsold.
    assert np.isclose(a["offered"], 1180.0) and np.isclose(a["bought_by_wage_earners"], 1000.0)
    assert np.isclose(a["bought_by_owners"], 170.0) and np.isclose(a["unsold"], 10.0)
    assert np.isclose(r2["published"]["unsold"], 10 / 1180) and np.isclose(r2["published"]["sold_part"], 170 / 180)
    assert np.isclose(r2["published"]["sales_cut"], 10 / 1180)
    lost = 10 / 180
    # The larger firm keeps its price and books the whole loss. The smaller takes half out of its price and books half.
    # (The core has set the price cut against the standing rise of the same firm, so the markup is tested.)
    assert np.allclose(L.markup_without(SHORTFALL), [0.18, 0.18 * (1 - 0.5 * lost)])
    assert np.allclose(L.components[PRICE_CUT] * L.components["push"], [1.2, 1.2 * (1 - 0.5 * lost)])
    assert np.allclose(L.components[SHORTFALL], [1 - lost, (1 - lost) / (1 - 0.5 * lost)])
    assert np.allclose(L.e, [0.18 * (1 - lost), 0.18 * (1 - lost)])
    assert np.isclose(L.p[0], 1.18) and np.isclose(L.p[1], 1 + 0.18 * (1 - 0.5 * lost))
    assert np.isclose(r2["capital_share"], 170.0 / 1170.0)          # unsold goods are income to nobody
    with np.errstate(divide="ignore"):
        r3 = m.step()                                               # owners now lay out the 170 they received
    assert np.isclose(r3["published"]["sales_account"]["owners_outlay"], 170.0)

    # 2. Long runs, with the modules that move money, in opposite listing orders.
    import registry
    from stage2 import starting_ledger
    from full import all_modules
    mixes = [["sales"],
             ["sales", "public_debt", "household_debt", "privatisation", "risk_shaping", "labour", "force",
              "externalisation", "proletarianization"]]
    years_unsold = years = 0
    largest = 0.0
    for names in mixes:
        histories = []
        for order in names, names[::-1]:
            m = Model(starting_ledger(0, 5000), all_modules() + registry.make(order), seed=0)
            kept = 0.0
            for step in range(60):
                r = m.step()
                a = r["published"]["sales_account"]
                tol = 1e-9 * a["offered"]
                bought = a["bought_by_wage_earners"] + a["bought_by_government"] + a["bought_by_owners"]
                assert abs(a["offered"] - bought - a["unsold"]) <= tol
                assert min(a["bought_by_wage_earners"], a["bought_by_government"], a["bought_by_owners"], a["unsold"]) >= 0
                assert np.isclose(a["offered"], a["wages"] + a["priced_earnings"], rtol=1e-12)
                if step:      # the account is of the year before: set it against that year's record of transfers
                    last = m.history[-2]
                    parties, pub = last["parties"], last["published"]
                    net = {p: row["received"] - row["paid"] for p, row in parties.items()}
                    to_firms = sum(t["paid"] * ((t["receiver"] == "firms") - (t["payer"] == "firms"))
                                   for t in last["transfers"])
                    holders = sum(row["received"] for p, row in parties.items() if p not in (WAGE_EARNERS, GOVERNMENT))
                    lent, repaid = pub.get("household_debt_lent", 0.0), pub.get("household_debt_repaid", 0.0)
                    assert a["bought_by_wage_earners"] <= a["wages"] + net.get(WAGE_EARNERS, 0.0) + lent - repaid + kept + tol
                    assert a["bought_by_government"] <= max(net.get(GOVERNMENT, 0.0), 0.0) + kept + tol
                    assert a["bought_by_owners"] <= (a["priced_earnings"] - a["unsold"] + to_firms + holders
                                                     + repaid - lent + tol)
                kept = a["kept_for_next_year"]
                years += 1
                years_unsold += a["unsold"] > 0
                largest = max(largest, a["unsold"] / a["offered"])
                assert np.isclose(sum(r["attribution"].values()), r["da"], atol=1e-10)
            histories.append(m.history)
        for x, y in zip(*histories):
            assert x["dk"] == y["dk"] and x["capital_share"] == y["capital_share"] and x["unemployment"] == y["unemployment"]
            assert x["published"]["unsold"] == y["published"]["unsold"]
    print(f"14. Sales account: with wages of 1,000, priced earnings of 180, owners who received 150 the year before "
          f"and 5 new jobs at 4 years' wages each, owners buy 170 and 10 is unsold. The firm of dominant capital "
          f"keeps its price and books the whole loss; the other firm takes half of it out of its price. The capitalist "
          f"share is 170 in 1,170. In {years} years of runs with the modules that move money, what was offered equalled "
          f"what wage earners, the government and owners bought plus what was unsold, and no buyer spent more than the "
          f"record of transfers shows it had. Goods were unsold in {years_unsold} of those years, at most {largest:.1%} of "
          f"what was offered. Opposite listing orders gave identical figures.")


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
    print("All fourteen checks passed.")
