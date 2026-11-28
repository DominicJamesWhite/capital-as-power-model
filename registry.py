"""Every module of the model, and the modules that can take the place of one of them.

The model is all of its modules running together. Each module is kept in its own file so that it
can be replaced by a better version, not so that it can be left out.

Each entry maps a short name to the file and the class that hold the module:

    MODULES["sales"] = ("modules.sales", "Sales")

MODULES lists every module that runs by default, in the order in which they run.

REPLACEMENTS lists modules that can run in place of one of them. A module names the modules whose
place it can take in its `replaces`, by the names the modules give themselves.

BASIC is a small set of ten modules that runs by itself. The tests in checks.py use it. It has no
government, no account of what can be sold and no household debt, so its results are not the
model's results.

From the command line:

    python full.py 30000 60                       every module
    python full.py 30000 60 0 --with envelope     the envelope module in place of the boundary contest
    python full.py 30000 60 0 --without failure   every module but one, for a test
    python full.py 30000 60 0 --basic             the basic set
"""
import importlib

MODULES = {}
MODULES["sabotage"] = ("modules.sabotage", "Sabotage")
MODULES["debt"] = ("modules.debt", "Debt")
MODULES["greenfield"] = ("modules.greenfield", "Greenfield")
MODULES["cost_cutting"] = ("modules.costcutting", "CostCutting")
MODULES["stagflation"] = ("modules.stagflation", "Stagflation")
MODULES["resistance"] = ("modules.resistance", "Resistance")
MODULES["failure"] = ("modules.failure", "Failure")
MODULES["sales"] = ("modules.sales", "Sales")
MODULES["leaders"] = ("modules.leaders", "Leaders")
MODULES["boundary_contest"] = ("modules.boundary_contest", "BoundaryContest")
MODULES["compass_consensus"] = ("modules.compasses", "ConsensusCompass")
MODULES["coalitions"] = ("modules.coalitions", "Coalitions")
MODULES["force"] = ("modules.force", "Force")
MODULES["owners"] = ("modules.owners", "Owners")
MODULES["hype"] = ("modules.hype", "Hype")
MODULES["risk_shaping"] = ("modules.risk_shaping", "RiskShaping")
MODULES["public_debt"] = ("modules.public_debt", "PublicDebt")
MODULES["policy_rate"] = ("modules.policy_rate", "PolicyRate")
MODULES["protections"] = ("modules.protections", "Protections")
MODULES["privatisation"] = ("modules.privatisation", "Privatisation")
MODULES["barriers"] = ("modules.barriers", "Barriers")
MODULES["proletarianization"] = ("modules.proletarianization", "Proletarianization")
MODULES["labour"] = ("modules.labour", "Labour")
MODULES["household_debt"] = ("modules.household_debt", "HouseholdDebt")
MODULES["hierarchy"] = ("modules.hierarchy", "Hierarchy")
MODULES["wants"] = ("modules.wants", "Wants")
MODULES["eruptions"] = ("modules.eruptions", "Eruptions")
MODULES["energy"] = ("modules.energy", "Energy")
MODULES["externalisation"] = ("modules.externalisation", "Externalisation")
MODULES["nature"] = ("modules.nature", "Nature")
MODULES["second_country"] = ("modules.second_country", "SecondCountry")   # applies the merger rule to each country
MODULES["cross_border"] = ("modules.cross_border", "CrossBorder")
MODULES["currencies"] = ("modules.currencies", "Currencies")   # acts once owners cross the border
MODULES["sovereign_funds"] = ("modules.sovereign_funds", "SovereignFunds")
MODULES["synchronisation"] = ("modules.synchronisation", "Synchronisation")   # a readout; it changes no term of any firm
MODULES["fear"] = ("modules.fear", "Fear")   # a readout; it also weakens upward pushes on hype
MODULES["plant"] = ("modules.plant", "Plant")   # a readout; it changes nothing and no module reads it
MODULES["concentration_measures"] = ("modules.concentration_measures", "ConcentrationMeasures")   # a readout
MODULES["capacity"] = ("modules.capacity", "Capacity")   # the sales module reads its plant

REPLACEMENTS = {}
REPLACEMENTS["mergers"] = ("modules.mergers", "Mergers")   # one country only, in place of second_country
REPLACEMENTS["compass"] = ("modules.compass", "Compass")   # compares recent mergers with earlier ones
REPLACEMENTS["compass_targets"] = ("modules.compasses", "TargetsCompass")
REPLACEMENTS["compass_ahead"] = ("modules.compasses", "AheadCompass")
REPLACEMENTS["envelope"] = ("modules.envelope", "Envelope")   # in place of boundary_contest

# Older names that still work on the command line.
ALIASES = {"compasses": "compass_consensus"}

BASIC = ("sabotage", "debt", "greenfield", "mergers", "cost_cutting", "stagflation", "compass", "resistance",
         "envelope", "failure")


def where(name):
    """The file and class of a module, by its short name."""
    name = ALIASES.get(name, name)
    if name in MODULES:
        return MODULES[name]
    if name in REPLACEMENTS:
        return REPLACEMENTS[name]
    raise KeyError(f"No module is called '{name}'. The names are in registry.py.")


def load(name):
    """The class of a module, by its short name."""
    path, cls = where(name)
    return getattr(importlib.import_module(path), cls)


def make(names):
    """Build the named modules with their default settings."""
    return [load(name)() for name in names]


def basic():
    """The basic set, built with its default settings."""
    return make(BASIC)


def plan(swap=(), without=(), start=None):
    """The short names of the modules of one run, in running order.

    It starts from every module, or from the names in `start`. Each module in `swap` goes in the place
    of the module it replaces, or at the end if it replaces none in the run. The modules in `without`
    are left out. A name in `without` may be a short name or the name the module gives itself."""
    keys = [ALIASES.get(k, k) for k in (MODULES if start is None else start)]
    own = {k: load(k).name for k in keys}
    swapped = set()
    for k in (ALIASES.get(s, s) for s in swap):
        if k in keys:
            raise ValueError(f"The module '{k}' is already in the run.")
        cls = load(k)
        own[k] = cls.name
        places = [i for i, x in enumerate(keys) if own[x] in getattr(cls, "replaces", ())]
        for x in (keys[i] for i in places):
            if x in swapped:
                raise ValueError(f"The modules '{x}' and '{k}' do the same job, so they cannot run together.")
        swapped.add(k)
        if places:
            keys[places[0]] = k
            keys = [x for i, x in enumerate(keys) if i not in places[1:]]
        else:
            keys.append(k)
    unknown = {n for n in without if n not in keys and n not in own.values()
               and ALIASES.get(n, n) not in keys}
    if unknown:
        raise ValueError(f"No module in the run is called {', '.join(sorted(unknown))}.")
    gone = {ALIASES.get(n, n) for n in without}
    return [k for k in keys if k not in gone and own[k] not in gone]
