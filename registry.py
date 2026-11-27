"""Optional modules, switched off unless asked for.

Each entry maps a short name to the file and the class that hold the module:

    OPTIONAL["coalitions"] = ("modules.coalitions", "Coalitions")

Switch modules on from the command line:

    python full.py 100000 60 --with coalitions,force
"""
import importlib

OPTIONAL = {}
OPTIONAL["sales"] = ("modules.sales", "Sales")
OPTIONAL["leaders"] = ("modules.leaders", "Leaders")
OPTIONAL["boundary_contest"] = ("modules.boundary_contest", "BoundaryContest")
OPTIONAL["compasses"] = ("modules.compasses", "ConsensusCompass")   # three compasses in one file; this is the fullest
OPTIONAL["compass_targets"] = ("modules.compasses", "TargetsCompass")
OPTIONAL["compass_ahead"] = ("modules.compasses", "AheadCompass")
OPTIONAL["compass_consensus"] = ("modules.compasses", "ConsensusCompass")
OPTIONAL["coalitions"] = ("modules.coalitions", "Coalitions")
OPTIONAL["force"] = ("modules.force", "Force")
OPTIONAL["owners"] = ("modules.owners", "Owners")
OPTIONAL["hype"] = ("modules.hype", "Hype")
OPTIONAL["risk_shaping"] = ("modules.risk_shaping", "RiskShaping")
OPTIONAL["public_debt"] = ("modules.public_debt", "PublicDebt")
OPTIONAL["policy_rate"] = ("modules.policy_rate", "PolicyRate")
OPTIONAL["protections"] = ("modules.protections", "Protections")
OPTIONAL["privatisation"] = ("modules.privatisation", "Privatisation")
OPTIONAL["barriers"] = ("modules.barriers", "Barriers")
OPTIONAL["proletarianization"] = ("modules.proletarianization", "Proletarianization")
OPTIONAL["labour"] = ("modules.labour", "Labour")
OPTIONAL["household_debt"] = ("modules.household_debt", "HouseholdDebt")
OPTIONAL["hierarchy"] = ("modules.hierarchy", "Hierarchy")
OPTIONAL["wants"] = ("modules.wants", "Wants")
OPTIONAL["eruptions"] = ("modules.eruptions", "Eruptions")
OPTIONAL["energy"] = ("modules.energy", "Energy")
OPTIONAL["externalisation"] = ("modules.externalisation", "Externalisation")
OPTIONAL["nature"] = ("modules.nature", "Nature")
OPTIONAL["second_country"] = ("modules.second_country", "SecondCountry")   # runs in place of the merger module
OPTIONAL["cross_border"] = ("modules.cross_border", "CrossBorder")   # meant to run with second_country; alone it draws the same border
OPTIONAL["currencies"] = ("modules.currencies", "Currencies")   # needs owners crossing the border: run with cross_border, or with second_country once its border opens
OPTIONAL["sovereign_funds"] = ("modules.sovereign_funds", "SovereignFunds")   # the resistance module reads the number it publishes
OPTIONAL["synchronisation"] = ("modules.synchronisation", "Synchronisation")   # a readout; it changes no term of any firm
OPTIONAL["fear"] = ("modules.fear", "Fear")   # a readout; with the hype module on it also weakens upward pushes on hype
OPTIONAL["plant"] = ("modules.plant", "Plant")   # a readout; it changes nothing and no module reads it
OPTIONAL["concentration_measures"] = ("modules.concentration_measures", "ConcentrationMeasures")   # a readout; it changes nothing and no module reads it


def make(names):
    """Build the named optional modules with their default settings."""
    out = []
    for name in names:
        path, cls = OPTIONAL[name]
        out.append(getattr(importlib.import_module(path), cls)())
    return out
