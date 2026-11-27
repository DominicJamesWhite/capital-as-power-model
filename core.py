"""The core of the model: a ledger of firms, each with its capitalization.

The core holds the firms, applies the changes that modules propose, and reports
differential measures. It has no behaviour of its own. With no modules, nothing changes.

Capitalization of a firm (Capital as Power, chapter 11, equation 8):

    K = employees * earnings_per_employee * hype / (risk * normal_rate_of_return)

Earnings per employee are not changed directly by any module. They are worked out from named
components, and each component belongs to one module:

    earnings_per_employee = wage * markup + other income per employee
    markup                = the combination of the markup components
    other income          = the sum of the income components

The price of a firm is not changed directly by any module either. The core works it out, for
the output of one employee in a year, from the same parts (Capital as Power, chapter 16,
equation 1: earnings are unit price less unit cost; chapter 12, "The markup and the target
rate of return": a price is a cost with a markup "tacked onto" it):

    cost per employee     = wage * (1 + the sum of the cost components)
    price                 = cost per employee + wage * markup

A cost component is a named cost other than the wage, counted in wages for each employee, and
it belongs to one module. Other income (interest, for example) is not a receipt from sales and
is no part of the price.

How the markup components combine is declared when a component is registered. A component
either "stacks" (it multiplies with everything else) or belongs to a named "overlap group".
Inside an overlap group only the largest premium counts in full. Each of the other premiums
counts for a declared part of its excess over 1; the part is a setting and is 0 unless changed.
A value below 1 is a discount and not a hold, and a discount always counts in full.
(A switch for comparisons, `discounts_overlap`, lets the discounts of a group overlap as its premiums do.)

What a stacking component holds. The base markup is a level: the markup the firm would have
if no gain or loss stood on top of it. Every other stacking component holds the part of its
owner's movements of the markup that still stands. At the end of each year the core cancels,
inside each firm, movements in opposite directions against each other (see Model._net). No
firm's markup changes when this is done, and no gain is credited to anybody for it.

Transfers. A transfer is money that passes in a year from a payer to a receiver without being
the price of anything: a tax, or interest. A module proposes a transfer with both sides named,
and the core settles it (see Model._settle). The payer and the receiver are each either firms
of the ledger or a named party: wage earners, the government, or a party that a module
registers. No payer pays more than it has in that year. A firm has its earnings of the year
before any transfer. Wage earners have the wage bill. The government has what it holds: what
it received earlier and has not paid out, and what it receives in the same year. What a payer
cannot pay, the receiver does not get. The net amount that each firm receives or pays under a
module's transfers is entered by the core in an income component of that module.

ADDITION TO THE LITERATURE. Nitzan and Bichler give no rule for how several sources of power
over the same buyers combine. The division of the markup into named components, the choice of
which components stack and which overlap, the rule for an overlap group, the convention
that divides a gain among the members of a group, and the cancelling of opposite movements
among the stacking components are all additions made for this model. The record of transfers
is bookkeeping, and the rule that a payer who cannot pay in full pays every one of its
transfers in the same proportion is an addition.

Run the scripts from the folder that holds this file, for example:
    python checks.py
"""
import zlib
from dataclasses import dataclass
from itertools import combinations
from math import factorial
import numpy as np

# The terms of the formula that a module may scale directly, and whether each raises (+1) or
# lowers (-1) capitalization. Earnings per employee are changed through components only.
TERMS = {"employees": 1, "hype": 1, "risk": -1}
ATTR = {"employees": "n", "hype": "h", "risk": "d"}

WAGE_EARNERS = "wage earners"      # a party to transfers: it has the wage bill of the year
GOVERNMENT = "government"          # a party to transfers: it has what it holds and what it receives in the year

# A firm that pays out all it has keeps this part of its earnings. It is an allowance for rounding and
# not a rule: without it a rounding error could leave earnings a hair below zero, and earnings of exactly
# zero have no logarithm, which the division of the year's gain among its sources needs.
ROUNDING = 1e-12

BASE = "base"                      # the industry-level markup; always present; stacks
HOLD_ON_BUYERS = "hold on buyers"  # the overlap group for premiums that rest on a hold on the same buyers (an addition)


class LedgerError(RuntimeError):
    """The ledger holds an impossible value, or a module broke a rule of the core."""


# ---------------------------------------------------------------- changes a module may propose

@dataclass
class Scale:
    """Multiply one term of some or all firms by a factor. Not for earnings per employee and not
    for the price: the core works both out from the wage and the components."""
    term: str            # "employees", "hype" or "risk", or the name of an added attribute
    factor: object       # one number for all firms, or an array with one number per firm
    source: str


@dataclass
class SetComponent:
    """Replace the values of a component. Only the module that owns the component may do this."""
    name: str
    values: object       # one number for all firms, or an array with one number per firm
    source: str


@dataclass
class ScaleComponent:
    """Multiply a component by a factor. Only the module that owns the component may do this."""
    name: str
    factor: object       # one number for all firms, or an array with one number per firm
    source: str


@dataclass
class Merge:
    """Buyers absorb targets. Employees and earnings add. Capitalization is preserved,
    then the buyer's risk is multiplied by risk_factor."""
    buyers: np.ndarray   # positions in the ledger
    targets: np.ndarray  # positions in the ledger, each target at most once
    source: str
    risk_factor: float = 1.0


@dataclass
class Found:
    """Add new firms.

    With `epe` left out, a new firm takes the average base markup of its industry and the
    default of every other component. With `epe` given, the base markup is set so that the new
    firm has exactly those earnings per employee. `components` may give values for named
    components; the others take their default. The price of a new firm is not given: the core
    works it out from the wage and the new firm's components, as for every firm."""
    employees: np.ndarray
    epe: np.ndarray      # earnings per employee at founding, or None
    hype: np.ndarray
    risk: np.ndarray
    industry: np.ndarray
    source: str
    extra: dict = None        # optional values for added per-firm attributes; others take their default
    components: dict = None   # optional values for named components; others take their default


@dataclass
class Dissolve:
    """Remove firms."""
    positions: np.ndarray
    source: str


@dataclass
class Set:
    """Change a shared number of the envelope, such as the wage or the working population."""
    key: str
    value: float
    source: str


@dataclass
class Publish:
    """Make a number available for other modules to read in the next step."""
    key: str
    value: float
    source: str


@dataclass
class Transfer:
    """Move money, in this year, from a payer to a receiver. Both sides are always named.

    payer     the name of a party (WAGE_EARNERS, GOVERNMENT, or a party registered with
              Ledger.add_party), or an array with the money that each firm is asked to pay.
    receiver  the name of a party, or an array with each firm's part of what is received
              (the parts are divided by their sum).
    amount    the money asked from a payer that is a party. Left out when firms pay: the amount
              asked is then the sum of the array.
    The core pays out no more than the payer has (see Model._settle). The proposing module must
    have registered an income component with transfers=True if firms pay or receive: the core
    enters there, for each firm, what it received less what it paid, for each employee."""
    label: str           # what the transfer is, in words; the record of the year lists it under this label
    payer: object
    receiver: object
    source: str
    amount: float = None


# ---------------------------------------------------------------- components

@dataclass
class Component:
    kind: str                       # "markup", "income" or "cost"
    owner: str                      # the name of the one module that may change it (None: nobody yet)
    neutral: float                  # 1 for a markup component, 0 for an income or a cost component
    default: float                  # the value a newly founded firm takes
    group: str = None               # None: the component stacks. Otherwise the name of its overlap group.
    paid_from_wages: bool = False   # income component only: the income is taken out of the wage bill,
                                    # so it is already counted in total income (used by the capitalist share)
    settled: bool = False           # income component only: the core sets it each year from the owner's transfers.
                                    # Every such income has a payer inside the model, so it adds nothing to total income.


def group_value(values, part, discounts_overlap=False):
    """The combined premium of one overlap group (an addition to the literature).

    The largest premium counts in full. Each other premium counts for `part` of its excess
    over 1. A value below 1 is a discount, and discounts multiply in full. With part = 1 the
    result is the plain product of all values; with one member it is that member's value.

    discounts_overlap is a switch for comparisons. With it on, the
    discounts of the group are treated as its premiums are: the deepest discount counts in
    full, and each other discount counts for `part` of the amount by which it stands below 1."""
    if len(values) == 1:
        return values[0]
    P = np.stack(values)
    up, down = np.maximum(P, 1.0), np.minimum(P, 1.0)
    largest = up.max(axis=0)
    counted = 1.0 + part * (up - 1.0)
    if not discounts_overlap:
        return down.prod(axis=0) * largest * counted.prod(axis=0) / (1.0 + part * (largest - 1.0))
    deepest = down.min(axis=0)
    counted_down = 1.0 - part * (1.0 - down)
    discounts = deepest * counted_down.prod(axis=0) / (1.0 - part * (1.0 - deepest))
    return discounts * largest * counted.prod(axis=0) / (1.0 + part * (largest - 1.0))


# ---------------------------------------------------------------- the ledger

class Ledger:
    def __init__(self, employees, epe, industry, sector_of_industry,
                 hype=1.0, risk=1.0, shared=None):
        self.n = np.array(employees, dtype=float)
        size = self.n.size
        self.h = np.broadcast_to(np.asarray(hype, dtype=float), size).copy()
        self.d = np.broadcast_to(np.asarray(risk, dtype=float), size).copy()
        self.ind = np.array(industry, dtype=int)
        self.sector_of = np.array(sector_of_industry, dtype=int)
        self.shared = {"nrr": 0.05, "wage": 1.0, "workforce": float(self.n.sum()),
                       "workforce_growth": 0.0}
        if shared:
            self.shared.update(shared)
        self.accounts = {}
        self.extra = {}          # added per-firm attributes, by name
        self.extra_default = {}
        # Components of earnings per employee. At the start the whole markup is the base markup.
        base = np.broadcast_to(np.asarray(epe, dtype=float), size) / self.shared["wage"]
        self.components = {BASE: base.copy()}
        self.info = {BASE: Component("markup", None, 1.0, 1.0)}
        # Parties to transfers other than firms. `holds` lists the parties that keep what they receive
        # until they pay it out, with the money each holds. A party in `parties` and not in `holds`
        # only receives: the ledger does not follow what it does with the money.
        self.parties = {WAGE_EARNERS, GOVERNMENT}
        self.holds = {GOVERNMENT: 0.0}
        self.overlap = {}        # for each overlap group, the part of a smaller premium's excess that counts
        self.discounts_overlap = set()   # the overlap groups whose discounts overlap as their premiums do (a switch for
                                         # comparisons; empty unless a run asks for it: every discount then counts in full)
        self.e = None            # earnings per employee: stored, and always equal to wage * markup + other income
        self.p = None            # price of one employee's output: stored, and always equal to wage * (1 + markup + costs)
        self.refresh()

    # ---- added attributes

    def add_attribute(self, name, values, default):
        """Give every firm an extra attribute, such as a coalition label. A module calls this
        in its start(). In a merger the buyer keeps its own value. A new firm takes `default`
        unless the Found change supplies a value."""
        self.extra[name] = np.broadcast_to(np.asarray(values), self.n.size).copy()
        self.extra_default[name] = default

    def add_party(self, name, holds=False):
        """Name a party to transfers that is not a firm, such as a group of households. A module
        calls this in its start(). With holds=False the party only receives. With holds=True it
        keeps what it receives and can pay it out later, as the government does."""
        self.parties.add(name)
        if holds:
            self.holds.setdefault(name, 0.0)

    # ---- components

    def add_component(self, name, owner, kind="markup", group=None, default=None, values=None,
                      paid_from_wages=False, transfers=False):
        """Register a component of earnings per employee. A module calls this in its start().

        kind    "markup" (neutral value 1), "income" (neutral value 0, in money per employee) or
                "cost" (neutral value 0; a cost other than the wage, counted in wages per employee:
                0.03 is a cost of three per cent of the wage for each employee). A cost component
                enters the price and never the earnings. A module that moves a markup without
                moving the price says so by moving a cost component by the opposite amount.
        group   None if the component stacks; the name of an overlap group otherwise.
        default the value a newly founded firm takes (the neutral value unless given).
        transfers  income component only, and at most one for each module: the core sets it each
                year to what each firm received less what it paid under the owner's Transfer
                changes, for each employee. The owner cannot set it directly.
        The base markup exists from the start; registering it gives it its owner."""
        if kind not in ("markup", "income", "cost"):
            raise LedgerError(f"component '{name}': kind must be 'markup', 'income' or 'cost'")
        if name in self.info:
            if name == BASE and self.info[BASE].owner in (None, owner):
                self.info[BASE].owner = owner
                return
            raise LedgerError(f"module '{owner}' cannot register component '{name}': "
                              f"it already belongs to '{self.info[name].owner}'")
        neutral = 1.0 if kind == "markup" else 0.0
        if transfers and kind != "income":
            raise LedgerError(f"component '{name}': only an income component can record transfers")
        if transfers and self.transfer_component(owner) is not None:
            raise LedgerError(f"module '{owner}' already has a component that records its transfers")
        if kind != "markup" and group is not None:
            raise LedgerError(f"component '{name}': only a markup component can be in an overlap group")
        self.info[name] = Component(kind, owner, neutral, neutral if default is None else float(default),
                                    group, bool(paid_from_wages), bool(transfers))
        start = neutral if values is None else values
        self.components[name] = np.broadcast_to(np.asarray(start, dtype=float), self.n.size).copy()
        if group is not None:
            self.overlap.setdefault(group, 0.0)     # only the largest premium counts, unless set otherwise
        self.refresh()

    def transfer_component(self, owner):
        """The name of the income component that records a module's transfers, or None."""
        for name, c in self.info.items():
            if c.settled and c.owner == owner:
                return name
        return None

    def markup_from(self, components):
        """The markup that a set of component arrays gives. Names are taken in alphabetical order,
        so the result does not depend on the order in which modules registered them."""
        out, groups = 1.0, {}
        for name in sorted(components):
            c = self.info[name]
            if c.kind != "markup":
                continue
            if c.group is None:
                out = out * components[name]
            else:
                groups.setdefault(c.group, []).append(components[name])
        for g in sorted(groups):
            out = out * group_value(groups[g], self.overlap[g], g in self.discounts_overlap)
        return np.broadcast_to(np.asarray(out, dtype=float), self.n.size)

    def markup(self):
        """Each firm's markup: the combination of its markup components."""
        return self.markup_from(self.components)

    def markup_with(self, name, values):
        """Each firm's markup if one component had the given values and nothing else changed."""
        comps = dict(self.components)
        comps[name] = np.broadcast_to(np.asarray(values, dtype=float), self.n.size)
        return self.markup_from(comps)

    def markup_without(self, name):
        """Each firm's markup with one component at its neutral value."""
        return self.markup_with(name, self.info[name].neutral)

    def stacking_markup(self):
        """The product of the markup components that stack (everything outside overlap groups)."""
        out = 1.0
        for name in sorted(self.components):
            c = self.info[name]
            if c.kind == "markup" and c.group is None:
                out = out * self.components[name]
        return np.broadcast_to(np.asarray(out, dtype=float), self.n.size)

    def other_income(self, only_outside_wages=False):
        """Other income per employee: the sum of the income components. With only_outside_wages,
        leave out the components that are paid out of the wage bill and the components that record
        transfers, because every transfer is paid by somebody whose income is already counted."""
        out = np.zeros(self.n.size)
        for name in sorted(self.components):
            c = self.info[name]
            if c.kind == "income" and not (only_outside_wages and (c.paid_from_wages or c.settled)):
                out = out + self.components[name]
        return out

    def has_income(self):
        return any(c.kind == "income" for c in self.info.values())

    def costs(self):
        """Costs other than the wage, for each employee, counted in wages: the sum of the cost components."""
        out = np.zeros(self.n.size)
        for name in sorted(self.components):
            if self.info[name].kind == "cost":
                out = out + self.components[name]
        return out

    def has_costs(self):
        return any(c.kind == "cost" for c in self.info.values())

    def unit_cost(self):
        """The cost of one employee's output: the wage and the named costs."""
        return self.shared["wage"] * (1.0 + self.costs()) if self.has_costs() else np.full(self.n.size, self.shared["wage"])

    def components_of(self, positions):
        """A copy of every component's values for the given firms, to hand to a Found change."""
        return {name: values[positions].copy() for name, values in self.components.items()}

    def refresh(self):
        """Work out earnings per employee and the price from the wage and the components."""
        e = self.shared["wage"] * self.markup()
        self.p = self.unit_cost() + e          # price = cost + earnings from the markup (chapter 16, equation 1)
        self.e = e + self.other_income() if self.has_income() else e.copy()

    def __len__(self):
        return self.n.size

    @property
    def sector(self):
        return self.sector_of[self.ind]

    def earnings(self):
        return self.n * self.e

    def markup_earnings(self):
        """The part of each firm's earnings that comes from its markup."""
        return self.n * (self.shared["wage"] * self.markup()) if self.has_income() else self.n * self.e

    def cap(self):
        return self.n * self.e * self.h / (self.d * self.shared["nrr"])


def top_positions(K, members, top):
    """Positions of the `top` largest firms by capitalization among `members`."""
    k = min(top, members.size)
    part = np.argpartition(K[members], -k)[-k:]
    return members[part]


# What the workbench calls each number the core reports every year: label, unit, note. The units
# are the same as in a module's `figures`: "share" (a part of a whole, from 0 to 1), "rate" (a
# change in a year), "times" (a multiple), "index" (a scale from 0 to 1) and "number".
# Most keys are readouts (below). The rest are numbers the core keeps in L.shared or L.accounts,
# or that the workbench works out from the readouts (inflation, mergers against hiring).
CORE_FIGURES = {
    "firms": ("Number of firms", "number", ""),
    "dk": ("Differential capitalization", "times", "Average capitalization of a top 100 firm divided by that of the average firm."),
    "breadth": ("Breadth", "times", "Employees of the average top 100 firm divided by those of the average firm."),
    "depth": ("Depth", "times", "Earnings per employee of the top 100 divided by those of the average firm."),
    "d_earnings": ("Differential earnings", "times", "Average earnings of a top 100 firm divided by those of the average firm."),
    "d_hype": ("Differential hype", "times", "Hype of the top 100 divided by the hype of all firms."),
    "d_risk": ("Differential risk", "times", "Risk of the top 100 divided by the risk of all firms."),
    "top_share_employees": ("Top 100 share of employees", "share", ""),
    "top_share_cap": ("Top 100 share of capitalization", "share", ""),
    "capital_share": ("Capitalist share of income", "share", "Part of all income that goes to owners, each income counted once."),
    "unemployment": ("Unemployment", "share", "Part of the working population without paid work."),
    "price_level": ("Price level", "number", "Average price, weighted by employees. The wage at the start is 1."),
    "other_costs": ("Costs other than the wage", "number", "Average, counted in wages."),
    "power_index": ("Power index", "times", "Average capitalization of a top 100 firm, divided by the wage."),
    "employment": ("Employment", "number", "Number of people employed."),
    "markup": ("Average markup", "share", "Weighted by employees."),
    "markup_top": ("Average markup of the top 100", "share", "Weighted by employees."),
    "other_income_part": ("Other income", "share", "Other income as a part of capitalist income."),
    "other_income_part_top": ("Other income of the top 100", "share", "Other income as a part of the top 100's capitalist income."),
    "inflation": ("Inflation", "rate", "Change in the price level from the year before."),
    "mergers_against_hiring": ("Mergers against new hiring", "times", "Employees bought by the top 100 for each new hire."),
    "da": ("Differential accumulation", "rate", "Change in differential capitalization in the year, on a log scale."),
    "concentration": ("Top 100 share of employees, as modules read it", "share", ""),
    "wage_earners_net": ("Net transfers to wage earners", "number", "What wage earners received less what they paid, as a part of the wage bill."),
    "wage": ("Wage", "number", "The wage at the start is 1."),
    "workforce": ("Working population", "number", ""),
    "workforce_growth": ("Growth of the working population", "rate", ""),
    "nrr": ("Normal rate of return", "rate", ""),
    "perm_sector": ("Opening of the sector boundary", "index", "How freely the top 100 can buy outside their industry but inside their sector."),
    "perm_nation": ("Opening of the national boundary", "index", "How freely the top 100 can buy anywhere in the country."),
}
# Numbers in CORE_FIGURES that are not readouts: where each comes from.
CORE_FIGURES_ELSEWHERE = {"inflation": "workbench", "mergers_against_hiring": "workbench", "da": "accounts",
                          "concentration": "accounts", "wage_earners_net": "accounts", "wage": "shared",
                          "workforce": "shared", "workforce_growth": "shared", "nrr": "shared",
                          "perm_sector": "shared", "perm_nation": "shared"}
FIGURE_UNITS = ("share", "rate", "times", "index", "number")


def readouts(L, top=100, mask=None, group=None):
    """Differential measures for an envelope.

    mask selects the firms that make up the envelope (default: all firms).
    group fixes the top group by position (default: the `top` largest in the envelope).
    """
    K = L.cap()
    members = np.arange(len(L)) if mask is None else np.flatnonzero(mask)
    g = top_positions(K, members, top) if group is None else np.asarray(group)
    E, n, h, d = L.earnings(), L.n, L.h, L.d

    def parts(idx):
        e_sum, n_sum = E[idx].sum(), n[idx].sum()
        expected = (E[idx] * h[idx]).sum()
        return {"count": idx.size, "employees": n_sum / idx.size, "epe": e_sum / n_sum,
                "earnings": e_sum / idx.size, "hype": expected / e_sum,
                "risk": expected / (E[idx] * h[idx] / d[idx]).sum(), "cap": K[idx].mean()}

    D, A = parts(g), parts(members)
    emp = n[members].sum()
    wage = L.shared["wage"]
    markup = L.markup()
    if L.has_income():
        other = n * L.other_income()                              # other income, in money
        from_markup = E[members].sum() - other[members].sum()
        # Total income counts each income once: an income paid out of wages is already in the wage bill.
        total_income = from_markup + wage * emp + (n * L.other_income(only_outside_wages=True))[members].sum()
        other_part, other_part_top = other[members].sum() / E[members].sum(), other[g].sum() / E[g].sum()
    else:
        total_income = E[members].sum() + wage * emp
        other_part = other_part_top = 0.0
    return {
        "firms": members.size,
        "dk": D["cap"] / A["cap"],                       # differential capitalization
        "breadth": D["employees"] / A["employees"],      # differential employees
        "depth": D["epe"] / A["epe"],                    # differential earnings per employee
        "d_earnings": D["earnings"] / A["earnings"],
        "d_hype": D["hype"] / A["hype"],
        "d_risk": D["risk"] / A["risk"],
        "top_share_employees": n[g].sum() / emp,
        "top_share_cap": K[g].sum() / K[members].sum(),
        "capital_share": E[members].sum() / total_income,   # capitalist income as a part of all income, each income counted once
        "unemployment": 1.0 - emp / L.shared["workforce"],
        "price_level": (L.p[members] * n[members]).sum() / emp,   # average price, weighted by employees
        "other_costs": (L.costs()[members] * n[members]).sum() / emp,   # average cost other than the wage, counted in wages
        "power_index": D["cap"] / wage,
        "employment": emp,
        "markup": (n[members] * markup[members]).sum() / emp,        # average markup, weighted by employees
        "markup_top": (n[g] * markup[g]).sum() / n[g].sum(),         # the same for the top group
        "other_income_part": other_part,                 # other income as a part of capitalist income
        "other_income_part_top": other_part_top,         # the same for the top group
    }


def _logmean(a, b):
    out = np.where(np.isclose(a, b), a, (a - b) / (np.log(a) - np.log(b) + (a == b)))
    return out


# ---------------------------------------------------------------- the model

class Model:
    """A ledger plus a list of modules. Each step:

    1. every module reads the same start-of-step ledger and proposes changes;
    2. all scalings and all changes to components are applied together, the wage is updated,
       and earnings per employee and the price are worked out again from the components;
    3. mergers, foundings and dissolutions are applied in a fixed order;
    4. shared numbers and published accounts are updated;
    5. the change in differential capitalization is divided among its sources.

    After step 2, and again after step 3, the record kept in the stacking components is netted
    (see _net). This changes no firm's markup and is credited to no source.

    The order in which modules are listed makes no difference to the result: changes are
    applied in the alphabetical order of their sources, and components are combined in the
    alphabetical order of their names.
    """
    CORE_SUPPLIES = ("unemployment", "capital_share", "concentration", "transfers", "wage_earners_net")

    def __init__(self, ledger, modules=(), top=100, seed=0, overlap=None, netting=True, discounts_overlap=()):
        self.L = ledger
        self.modules = list(modules)
        self.top = top
        self.netting = netting      # False keeps the gross record of every module's movements; for comparisons only
        self.streams = {m.name: np.random.default_rng([seed, zlib.crc32(m.name.encode())])
                        for m in self.modules}
        self.history = []
        self.settlement = {"transfers": [], "parties": {}}     # the record of the last year's transfers
        supplied = set(self.CORE_SUPPLIES)
        for m in self.modules:
            supplied.update(getattr(m, "supplies", ()))
        for m in self.modules:
            missing = [r for r in getattr(m, "reads", ()) if r not in supplied]
            if missing:
                raise ValueError(f"module '{m.name}' reads {missing}, which no active module supplies")
        self._core_accounts()
        # A component that opens at a value other than its neutral one changes the opening ledger
        # (an opening cost is in the opening price). A module registers such a component in
        # register(), which the core calls for every module, in the alphabetical order of their
        # names, before any start(). Every start() therefore reads the same opening ledger, and
        # the listing order cannot matter.
        for m in sorted(self.modules, key=lambda m: m.name):
            if hasattr(m, "register"):
                m.register(self.L)
        for m in self.modules:
            self.L.accounts.update(m.start(self.L) if hasattr(m, "start") else {})
        # overlap: for a named overlap group, the part of each smaller premium's excess over 1 that
        # counts (0: only the largest counts; 1: plain stacking). A setting, and an addition.
        for g, part in (overlap or {}).items():
            self.L.overlap[g] = float(part)
        # discounts_overlap: the names of overlap groups in which discounts overlap as premiums do. A switch
        # for comparisons, and an addition. Left empty, every discount counts in full.
        self.L.discounts_overlap = set(discounts_overlap)
        self.L.refresh()

    def _core_accounts(self):
        r = readouts(self.L, self.top)
        # "transfers": for each label, the money asked and the money paid in the last year. A module
        # reads it the next year, like every account, to learn whether its transfers were paid in full.
        paid = {}
        for t in self.settlement["transfers"]:
            row = paid.setdefault(t["label"], {"asked": 0.0, "paid": 0.0})
            row["asked"] += t["asked"]
            row["paid"] += t["paid"]
        # "wage_earners_net": what wage earners received in transfers less what they paid, as a part of the wage bill.
        w = self.settlement["parties"].get(WAGE_EARNERS)
        net = (w["received"] - w["paid"]) / w["wage_bill"] if w and w["wage_bill"] > 0 else 0.0
        self.L.accounts.update(unemployment=r["unemployment"], capital_share=r["capital_share"],
                               concentration=r["top_share_employees"], transfers=paid, wage_earners_net=net)

    def _lndk(self, group=None):
        K = self.L.cap()
        g = top_positions(K, np.arange(len(K)), self.top) if group is None else group
        return float(np.log(K[g].mean() / K.mean()))

    # ---- the guard

    def _guard(self, touched, stage):
        """Stop the run if the ledger holds an impossible value, and name the sources that
        changed the offending firms in this step."""
        L = self.L
        tests = [("employees that are negative or not finite", ~np.isfinite(L.n) | (L.n < 0)),
                 ("earnings per employee that are negative or not finite", ~np.isfinite(L.e) | (L.e < 0)),
                 ("hype that is not finite or not positive", ~np.isfinite(L.h) | (L.h <= 0)),
                 ("risk that is not finite or not positive", ~np.isfinite(L.d) | (L.d <= 0))]
        if L.has_costs():
            unit = L.unit_cost()
            tests.append(("a cost for each employee that is not finite or not above zero", ~np.isfinite(unit) | (unit <= 0)))
        for name, values in L.components.items():
            c = L.info[name]
            bad = ~np.isfinite(values) | ((values <= 0) if c.kind == "markup" else False)
            tests.append((f"a value of the component '{name}' (owned by '{c.owner}') that is not finite"
                          + (" or not positive" if c.kind == "markup" else ""), bad))
        for what, bad in tests:
            if np.any(bad):
                sources = sorted(s for s, mask in touched.items() if mask[bad].any())
                named = ", ".join(sources) if sources else "none (no change of this step touched them)"
                raise LedgerError(
                    f"The run was stopped in step {len(self.history) + 1}, {stage}. "
                    f"{int(np.sum(bad))} of {len(L)} firms have {what}. "
                    f"Sources that changed these firms in this step: {named}.")

    # ---- the record kept in the stacking components

    def _net(self, base_move=None):
        """Cancel opposite movements among the stacking markup components of each firm.

        THE CONVENTION (an addition). Several rules move the markup of a firm, and each records
        its movements in its own component. A rule that pushes up every year and a rule that
        pushes down every year would each pile up a record without limit, although the markup
        itself stays ordinary. The core therefore keeps, in every stacking component other than
        the base, only the part of its owner's movements that still stands:

          - a gain stands until a later fall of the markup takes it away;
          - a loss stands until a later rise of the markup restores it;
          - the base holds the rest: the markup the firm would have if no gain or loss stood.

        Each year, in each firm, what pushes up is set against what pushes down. The things set
        against each other are the standing gains (components above 1), the standing losses
        (components below 1), and this year's movement of the base by its owner (`base_move`, the
        change in its logarithm). The smaller side is cancelled in full. The larger side keeps
        the difference, and each of its members keeps the same proportion of what it had. The
        reckoning is in logarithms, so the product of the components, and with it the markup of
        the firm, is the same before and after. Nothing is credited to any source for it.

        Components of an overlap group are levels that their owners set, and income components
        are amounts of money. Neither takes part."""
        L = self.L
        names = sorted(n for n, c in L.info.items() if c.kind == "markup" and c.group is None and n != BASE)
        if not self.netting or not names:
            return
        X = np.log(np.stack([L.components[n] for n in names]))
        y = np.zeros(len(L)) if base_move is None else base_move
        up = np.maximum(X, 0.0).sum(axis=0) + np.maximum(y, 0.0)
        down = -(np.minimum(X, 0.0).sum(axis=0) + np.minimum(y, 0.0))
        cancelled = np.minimum(up, down)
        act = np.flatnonzero(cancelled > 0)
        if act.size == 0:
            return
        keep_up = 1.0 - cancelled[act] / up[act]          # the proportion that each gain keeps
        keep_down = 1.0 - cancelled[act] / down[act]      # the proportion that each loss keeps
        for name, x in zip(names, X):
            x = x[act]
            L.components[name][act] = np.exp(x * np.where(x > 0, keep_up, keep_down))
        ya = y[act]
        L.components[BASE][act] *= np.exp(ya * np.where(ya > 0, keep_up, keep_down) - ya)
        L.refresh()

    # ---- one step

    def step(self):
        L = self.L
        changes = []
        for m in self.modules:          # each module has its own random stream, so listing order cannot matter
            for c in m.propose(L, self.streams[m.name]):
                if isinstance(c, (SetComponent, ScaleComponent)):
                    if c.name not in L.info:
                        raise LedgerError(f"module '{m.name}' tried to change the component '{c.name}', "
                                          f"which no module has registered")
                    if L.info[c.name].owner != m.name:
                        raise LedgerError(f"module '{m.name}' tried to change the component '{c.name}', "
                                          f"which belongs to '{L.info[c.name].owner}'. A module may change "
                                          f"only the components it owns.")
                    if L.info[c.name].settled:
                        raise LedgerError(f"module '{m.name}' tried to set the component '{c.name}' directly. It "
                                          f"records transfers, and the core sets it from the module's Transfer changes.")
                elif isinstance(c, Transfer):
                    if c.source != m.name:
                        raise LedgerError(f"module '{m.name}' proposed a transfer under the name '{c.source}'")
                elif isinstance(c, Scale) and c.term == "price":
                    raise LedgerError(f"module '{m.name}' proposed Scale('price', ...). The price is worked out from "
                                      f"the wage, the markup and the cost components and cannot be scaled directly. "
                                      f"A change of the markup moves the price by itself. To move a markup without "
                                      f"moving the price, register a cost component in start() with "
                                      f"L.add_component(name, owner, kind='cost') and move it by the opposite amount.")
                elif isinstance(c, Scale) and (c.term == "epe" or c.term in L.info):
                    raise LedgerError(f"module '{m.name}' proposed Scale('{c.term}', ...). Earnings per employee "
                                      f"are worked out from components and cannot be scaled directly. Register a "
                                      f"component in start() with L.add_component and change it with "
                                      f"SetComponent or ScaleComponent.")
                changes.append(c)
        changes.sort(key=lambda c: c.source)     # a stable sort: listing order cannot matter, a module's own order is kept
        attribution = {}

        def credit(source, amount):
            attribution[source] = attribution.get(source, 0.0) + float(amount)

        ln0 = self._lndk()
        K0 = L.cap()
        count = len(L)
        group = top_positions(K0, np.arange(count), self.top)
        touched = {}                    # for the guard: which firms each source changed in this step

        def touch(source, mask):
            touched[source] = touched.get(source, np.zeros(len(L), dtype=bool)) | mask

        # --- all scalings together
        logf = {}

        def add_log(source, values):
            logf[source] = logf.get(source, 0.0) + values

        for c in changes:
            if isinstance(c, Scale):
                f = np.broadcast_to(np.asarray(c.factor, dtype=float), count)
                arr = getattr(L, ATTR[c.term]) if c.term in ATTR else L.extra[c.term]   # an added attribute holding numbers
                arr *= f
                if c.term in ATTR:
                    touch(c.source, f != 1.0)
                if c.term in TERMS:
                    with np.errstate(divide="ignore", invalid="ignore"):
                        add_log(c.source, TERMS[c.term] * np.log(f))

        # --- components and the wage, then earnings per employee
        comp_changes = [c for c in changes if isinstance(c, (SetComponent, ScaleComponent))]
        wage_sets = [c for c in changes if isinstance(c, Set) and c.key == "wage"]
        transfers = [c for c in changes if isinstance(c, Transfer)]
        recording = sorted(name for name, c in L.info.items() if c.settled)    # the components that record transfers
        self.settlement = {"transfers": [], "parties": {}}
        if comp_changes or wage_sets or recording or transfers:
            w0, e0, m0 = L.shared["wage"], L.e.copy(), L.markup().copy()
            old = {name: L.components[name].copy() for name in {c.name for c in comp_changes} | set(recording)}
            for c in comp_changes:
                v = np.broadcast_to(np.asarray(c.values if isinstance(c, SetComponent) else c.factor,
                                               dtype=float), count)
                if isinstance(c, SetComponent):
                    L.components[c.name] = v.copy()
                else:
                    L.components[c.name] = L.components[c.name] * v
            for c in wage_sets:
                L.shared["wage"] = c.value
            w1 = L.shared["wage"]
            L.refresh()
            if recording or transfers:      # after the year's scalings, markups and wage: what each payer has is now known
                self.settlement = self._settle(transfers, group)
            for name in old:
                touch(L.info[name].owner, L.components[name] != old[name])
            # Divide the change in the logarithm of earnings per employee among the sources, exactly.
            # e = M + O, with M = wage * markup and O = other income. The change in ln e is the change
            # in M plus the change in O, each divided by the logarithmic mean of e before and after.
            # The change in ln M is the change in ln wage, plus that of each stacking component, plus
            # that of each overlap group.
            with np.errstate(divide="ignore", invalid="ignore"):
                if L.has_income():
                    lm_e = _logmean(L.e, e0)
                    weight = _logmean(w1 * L.markup(), w0 * m0) / lm_e
                else:
                    lm_e, weight = None, 1.0
                if w1 != w0:
                    sources = sorted({c.source for c in wage_sets})
                    for s in sources:
                        touch(s, np.ones(count, dtype=bool))
                        add_log(s, weight * np.full(count, np.log(w1 / w0)) / len(sources))
                groups = {}
                for name in sorted(old):
                    c = L.info[name]
                    if c.kind == "cost":          # a cost enters the price and not the earnings: nothing to divide
                        continue
                    if c.kind == "income":
                        add_log(c.owner, (L.components[name] - old[name]) / lm_e)
                    elif c.group is None:
                        add_log(c.owner, weight * np.log(L.components[name] / old[name]))
                    else:
                        groups.setdefault(c.group, []).append(name)
                for g in sorted(groups):
                    for owner, share in self._group_shares(g, groups[g], old).items():
                        add_log(owner, weight * share)

        if (L.d < 1.0).any():          # risk is 1 when owners are fully confident; it cannot go lower
            floor = np.maximum(L.d, 1.0)
            logf["risk floor"] = -np.log(floor / L.d)
            L.d[:] = floor
        self._guard(touched, "after the year's scalings")
        if logf:
            K1 = L.cap()
            lm = _logmean(K1, K0)
            w_top = np.zeros(len(L))
            w_top[group] = lm[group] / _logmean(K1[group].sum(), K0[group].sum())
            w_all = lm / _logmean(K1.sum(), K0.sum())
            for source in sorted(logf):
                credit(source, ((w_top - w_all) * logf[source]).sum())
        # The year's gain has been divided among its sources. Now net the record of the stacking components.
        base_move = None
        if comp_changes and BASE in old:
            base_move = np.log(L.components[BASE] / old[BASE])
        self._net(base_move)
        ln_fixed = self._lndk(group=group)
        ln_now = self._lndk()
        if abs(ln_now - ln_fixed) > 0:
            credit("turnover", ln_now - ln_fixed)

        # --- structural changes, in a fixed order that does not depend on module order
        structural = [c for c in changes if isinstance(c, (Merge, Found, Dissolve))]
        rank = {Merge: 0, Dissolve: 1, Found: 2}
        structural.sort(key=lambda c: (rank[type(c)], c.source))
        remove = np.zeros(len(L), dtype=bool)
        for c in structural:
            if isinstance(c, Merge):
                self._merge(c, remove)
                touch(c.source, np.isin(np.arange(len(L)), c.buyers))
            elif isinstance(c, Dissolve):
                remove[c.positions] = True
        if remove.any():
            sources = sorted({c.source for c in structural if isinstance(c, (Merge, Dissolve))})
            keep = ~remove
            for name in "n", "e", "h", "d", "p", "ind":
                setattr(L, name, getattr(L, name)[keep])
            for name in L.extra:
                L.extra[name] = L.extra[name][keep]
            for name in L.components:
                L.components[name] = L.components[name][keep]
            touched = {s: mask[keep] for s, mask in touched.items()}
            ln_after = self._lndk()
            for s in sources:          # one source in practice; shared equally if several
                credit(s, (ln_after - ln_now) / len(sources))
            ln_now = ln_after
        for c in structural:
            if isinstance(c, Found) and len(c.employees):
                k = len(c.employees)
                self._found(c)
                touched = {s: np.concatenate([mask, np.zeros(k, dtype=bool)]) for s, mask in touched.items()}
                touch(c.source, np.arange(len(L)) >= len(L) - k)
                ln_after = self._lndk()
                credit(c.source, ln_after - ln_now)
                ln_now = ln_after
        if structural:                  # a merger averages components, which can leave a gain beside a loss
            self._net()

        # --- shared numbers and published accounts
        for c in changes:
            if isinstance(c, Set) and c.key != "wage":      # the wage was updated with the scalings
                L.shared[c.key] = c.value
        published = {c.key: c.value for c in changes if isinstance(c, Publish)}
        L.accounts.update(published)
        self._guard(touched, "after the year's mergers, dissolutions and foundings")
        self._core_accounts()

        r = readouts(L, self.top)
        r["da"] = ln_now - ln0                      # differential accumulation in this step (log change)
        r["attribution"] = attribution
        r["published"] = published
        r["transfers"] = self.settlement["transfers"]      # every transfer of the year: label, payer, receiver, asked, paid
        r["parties"] = self.settlement["parties"]          # for each party that is not a firm: received, paid, and what it holds
        self.history.append(r)
        return r

    # ---- transfers

    def _settle(self, transfers, group):
        """Settle the year's transfers and enter the firms' side in the components that record them.

        THE RULE. Every transfer has a payer and a receiver, and no payer pays more than it has.

          - A firm has its earnings of the year before any transfer: its employees times the wage
            times its markup, plus its other income that is not a transfer. These are the figures
            after the year's scalings, markups and wage, and before the year's mergers. (A firm
            that pays all it has keeps one part in a million million, as an allowance for rounding.)
          - Wage earners have the wage bill of the year.
          - The government, and any other party registered as holding money, has what it held at the
            start of the year and what it receives in transfers during the year.
          - A party registered as receiving only cannot pay.

        A payer that is asked for more than it has pays every one of its transfers in the same
        proportion (a convention, and an addition). What a payer does not pay, the receiver does
        not get. What a firm receives in the year does not add to what it can pay in the same
        year, so the result does not depend on any order among the transfers. Parties that hold
        money are settled after the firms and the wage earners, and a party that is paid by
        another such party is settled after it.

        The firms' side is entered as money for each employee, reckoned on the employees the firm
        has after the year's scalings. The whole amount settled is therefore the amount that
        changes the firms' earnings, to the last unit.

        Returns the record of the year: one row for each transfer, and one for each party."""
        L = self.L
        count = len(L)
        recording = [name for name, c in L.info.items() if c.settled]
        for name in recording:                     # last year's amounts are replaced and never added to
            L.components[name] = np.zeros(count)
        L.refresh()
        wage_bill = L.shared["wage"] * L.n.sum()
        means = np.maximum(L.n * L.e, 0.0) * (1.0 - ROUNDING)    # what each firm has: its earnings before any transfer

        rows = []
        for t in transfers:
            by_firms = not isinstance(t.payer, str)
            to_firms = not isinstance(t.receiver, str)
            for side in ([] if by_firms else [t.payer]) + ([] if to_firms else [t.receiver]):
                if side not in L.parties:
                    raise LedgerError(f"module '{t.source}' named '{side}' in the transfer '{t.label}', and no "
                                      f"such party exists. Register it in start() with L.add_party.")
            if (by_firms or to_firms) and L.transfer_component(t.source) is None:
                raise LedgerError(f"module '{t.source}' proposed the transfer '{t.label}', which firms pay or "
                                  f"receive, and has no component to record it. Register one in start() with "
                                  f"L.add_component(name, owner, kind='income', transfers=True).")
            if by_firms:
                ask = np.broadcast_to(np.asarray(t.payer, dtype=float), count)
                asked = float(ask.sum())
            else:
                if t.amount is None:
                    raise LedgerError(f"the transfer '{t.label}' of module '{t.source}' has a party as payer and no amount")
                if not to_firms and t.payer == t.receiver:
                    raise LedgerError(f"the transfer '{t.label}' of module '{t.source}' has '{t.payer}' on both sides")
                if t.payer != WAGE_EARNERS and t.payer not in L.holds:
                    raise LedgerError(f"module '{t.source}' asked '{t.payer}' to pay the transfer '{t.label}'. That "
                                      f"party only receives: the ledger knows of nothing that it has.")
                ask, asked = None, float(t.amount)
            parts = None
            if to_firms:
                parts = np.broadcast_to(np.asarray(t.receiver, dtype=float), count)
                if not np.all(np.isfinite(parts)) or (parts < 0).any() or (asked > 0 and parts.sum() <= 0):
                    raise LedgerError(f"the transfer '{t.label}' of module '{t.source}' divides what is received "
                                      f"among firms in parts that are negative, missing or all zero")
            if not np.isfinite(asked) or asked < 0 or (ask is not None and (ask < 0).any()):
                raise LedgerError(f"the transfer '{t.label}' of module '{t.source}' asks for an amount that is "
                                  f"negative or not a number. A transfer in the other direction names the other payer.")
            rows.append({"t": t, "ask": ask, "asked": asked, "parts": parts, "paid": None})

        received = {p: 0.0 for p in L.parties}
        paid_out = {p: 0.0 for p in L.parties}
        net = {}                                    # for each module, what each firm received less what it paid

        def give(row, total, paid_by_firms=None):
            t = row["t"]
            row["paid"] = float(total)
            if paid_by_firms is not None:
                net[t.source] = net.get(t.source, 0.0) - paid_by_firms
                row["paid_top"] = float(paid_by_firms[group].sum())
            else:
                paid_out[t.payer] += float(total)
            if row["parts"] is not None:
                share = row["parts"] * (total / row["parts"].sum()) if total > 0 else np.zeros(count)
                net[t.source] = net.get(t.source, 0.0) + share
                row["received_top"] = float(share[group].sum())
            else:
                received[t.receiver] += float(total)

        # 1. firms pay out of their earnings
        asked_of_firms = np.zeros(count)
        for row in rows:
            if row["ask"] is not None:
                asked_of_firms = asked_of_firms + row["ask"]
        able = np.where(asked_of_firms > means, means / np.maximum(asked_of_firms, 1e-300), 1.0)
        for row in rows:
            if row["ask"] is not None:
                paid = row["ask"] * able
                give(row, paid.sum(), paid)
        # 2. wage earners pay out of the wage bill
        asked_of_wages = sum(row["asked"] for row in rows if row["ask"] is None and row["t"].payer == WAGE_EARNERS)
        able_wages = min(1.0, wage_bill / asked_of_wages) if asked_of_wages > 0 else 1.0
        for row in rows:
            if row["ask"] is None and row["t"].payer == WAGE_EARNERS:
                give(row, row["asked"] * able_wages)
        # 3. parties that hold money pay out of what they hold and what they have received this year
        waiting = [row for row in rows if row["paid"] is None]
        while waiting:
            payers = sorted({row["t"].payer for row in waiting})
            still_to_receive = {row["t"].receiver for row in waiting if row["parts"] is None}
            ready = [p for p in payers if p not in still_to_receive]
            if not ready:
                raise LedgerError(f"the transfers among {', '.join(payers)} go round in a circle, so none of "
                                  f"them can be settled first")
            for p in ready:
                mine = [row for row in waiting if row["t"].payer == p]
                has = L.holds[p] + received[p]
                asked = sum(row["asked"] for row in mine)
                able_p = min(1.0, has / asked) if asked > 0 else 1.0
                for row in mine:
                    give(row, row["asked"] * able_p)
            waiting = [row for row in waiting if row["paid"] is None]

        for p in L.holds:
            L.holds[p] = L.holds[p] + received[p] - paid_out[p]
        for source, amounts in net.items():
            name = L.transfer_component(source)
            L.components[name] = np.where(L.n > 0, amounts / np.maximum(L.n, 1e-300), 0.0)
        L.refresh()
        parties = {p: {"received": received[p], "paid": paid_out[p], "holds": L.holds.get(p)}
                   for p in sorted(L.parties)}
        parties[WAGE_EARNERS]["wage_bill"] = wage_bill
        record = []
        for row in rows:
            t = row["t"]
            record.append({"label": t.label, "source": t.source,
                           "payer": t.payer if row["ask"] is None else "firms",
                           "receiver": t.receiver if row["parts"] is None else "firms",
                           "asked": row["asked"], "paid": row["paid"],
                           "paid_by_top": row.get("paid_top", 0.0),            # the part the hundred largest firms paid
                           "received_by_top": row.get("received_top", 0.0)})   # the part they received
        return {"transfers": record, "parties": parties}

    def _group_shares(self, g, changed, old):
        """Divide the change in the logarithm of an overlap group's combined premium among the
        owners of the members that changed.

        THE CONVENTION (an addition): each owner is credited with the average of what its own
        change adds, taken over every order in which the year's changes to the group could be
        applied (the Shapley value). The shares add up to the whole change exactly, and they do
        not depend on the order in which modules are listed."""
        L = self.L
        members = sorted(name for name in L.components if L.info[name].group == g)
        part = L.overlap[g]

        def value(new_names):
            return np.log(group_value([L.components[m] if (m in new_names or m not in old) else old[m]
                                       for m in members], part, g in L.discounts_overlap))

        changed = sorted(changed)
        k = len(changed)
        cache = {}

        def v(subset):
            key = frozenset(subset)
            if key not in cache:
                cache[key] = value(key)
            return cache[key]

        shares = {}
        for name in changed:
            rest = [m for m in changed if m != name]
            total = 0.0
            for size in range(k):
                w = factorial(size) * factorial(k - size - 1) / factorial(k)
                for subset in combinations(rest, size):
                    total = total + w * (v(subset + (name,)) - v(subset))
            owner = L.info[name].owner
            shares[owner] = shares.get(owner, 0.0) + total
        return shares

    def _merge(self, c, remove):
        """Buyers absorb targets. Employees, earnings and expected earnings add, so totals are kept.
        Each income component adds, and so does each cost component, so the value of what the two
        firms sell is kept as well. Each markup component other than the base becomes the average
        of the two firms' values, weighted by their earnings from the markup. The base markup is
        then set so that the buyer's markup earnings are exactly the sum of the two."""
        L = self.L
        b, t = np.asarray(c.buyers), np.asarray(c.targets)
        if t.size == 0:
            return
        assert np.unique(t).size == t.size, "a target was acquired twice"
        assert not np.isin(t, b).any(), "a firm was both buyer and target"
        assert not remove[t].any() and not remove[b].any()
        nrr, wage = L.shared["nrr"], L.shared["wage"]
        K, E = L.cap(), L.earnings()
        EH = E * L.h
        ME = L.markup_earnings()
        ub = np.unique(b)

        def summed(part):
            total = part.copy()
            np.add.at(total, b, part[t])
            return total

        K_sum, E_sum, EH_sum, n_sum, ME_sum = (summed(x) for x in (K, E, EH, L.n, ME))
        for name in sorted(L.components):
            info = L.info[name]
            if name == BASE:
                continue
            weight, total = (ME, ME_sum) if info.kind == "markup" else (L.n, n_sum)
            L.components[name][ub] = summed(weight * L.components[name])[ub] / total[ub]
        L.n[ub] = n_sum[ub]
        L.components[BASE][ub] = 1.0
        rest = L.markup()[ub]                               # the buyer's markup apart from its base
        L.components[BASE][ub] = ME_sum[ub] / (wage * n_sum[ub]) / rest
        if L.has_income():
            L.e[ub] = (wage * L.markup() + L.other_income())[ub]
        else:
            L.e[ub] = wage * L.markup()[ub]
        L.p[ub] = (L.unit_cost() + wage * L.markup())[ub]
        L.h[ub] = EH_sum[ub] / E_sum[ub]
        L.d[ub] = np.maximum(EH_sum[ub] / (nrr * K_sum[ub]) * c.risk_factor, 1.0)
        remove[t] = True

    def _found(self, c):
        """Add new firms. Each component takes the value the Found change gives, or its default.
        The base markup takes the average of the industry entered, weighted by employees, unless
        the change gives earnings per employee; it is then set to produce exactly those earnings."""
        L = self.L
        k = len(c.employees)
        given = c.components or {}
        ind = np.asarray(c.industry, dtype=int)
        new = {}
        for name, info in L.info.items():
            if name in given:
                new[name] = np.broadcast_to(np.asarray(given[name], dtype=float), k).copy()
            elif name != BASE:
                new[name] = np.full(k, info.default)
        if BASE not in new:
            if c.epe is None:
                n_j = np.bincount(L.ind, L.n, L.sector_of.size)
                b_j = np.bincount(L.ind, L.n * L.components[BASE], L.sector_of.size)
                overall = (L.n * L.components[BASE]).sum() / L.n.sum()
                new[BASE] = np.where(n_j[ind] > 0, b_j[ind] / np.maximum(n_j[ind], 1e-300), overall)
            else:
                new[BASE] = np.ones(k)
        old_size = len(L)
        L.n = np.concatenate([L.n, c.employees])
        L.h = np.concatenate([L.h, c.hype]); L.d = np.concatenate([L.d, c.risk])
        L.ind = np.concatenate([L.ind, ind])
        for name in L.components:
            L.components[name] = np.concatenate([L.components[name], new[name]])
        for name in L.extra:
            g = (c.extra or {}).get(name)
            add = np.full(k, L.extra_default[name]) if g is None else np.asarray(g)
            L.extra[name] = np.concatenate([L.extra[name], add])
        fresh = np.arange(old_size, old_size + k)
        if c.epe is not None and BASE not in given:
            other = L.other_income()[fresh] if L.has_income() else 0.0
            rest = L.markup()[fresh]                        # with the base at 1
            L.components[BASE][fresh] = (np.asarray(c.epe, dtype=float) - other) / (L.shared["wage"] * rest)
        L.refresh()

    def run(self, steps):
        for _ in range(steps):
            self.step()
        return self.history
