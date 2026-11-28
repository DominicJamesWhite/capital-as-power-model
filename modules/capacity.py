"""Optional module: plant that stands idle.

THE RULE IN PLAIN WORDS

Each firm holds plant for a number of jobs: the people it can employ at the use of its plant that
business takes as standard. At the start of a run every firm holds plant for the people it employs.

  1. A firm that employs more people than its plant holds has built the difference. A firm that
     employs fewer has plant standing idle beyond the standard.
  2. Idle plant wears out and is not replaced (`wear`). Plant in use is kept up.
  3. When a firm buys another, it takes over the other's plant, idle or not. When a firm closes,
     its plant leaves with it, as the sabotage module counts the capacity of a closed firm as
     capacity that left its industry. A new firm builds all of its plant. Public employees whom
     the top 100 take over (privatisation module) arrive with their plant.
  4. The sales module, when this module is on, counts as building only the jobs that plant did
     not already hold. A firm that takes people back on into idle plant buys no equipment.

The module publishes the part of all plant that stands idle beyond the standard, and the jobs
built in the year as a part of employees. It changes no term of any firm other than its own
record of plant.

WHAT IT RESTS ON

  - Chapter 12, "The pace of industry": "business can tolerate neither full-capacity
    utilization nor maximum growth". "In sum": owners limit industry "by pricing products
    toward earning a target rate of return at some standard capacity utilization". An endnote
    of the chapter: conventional measures "usually estimate normal utilization to be in the
    70–90 per cent range". The plant of this module is counted at that standard, so idle plant
    here is plant idle beyond it.
  - Chapter 12, "Immaterial assets": "the widespread practice of post-merger 'downsizing' to
    shed excess capacity".
  - Chapter 14: in a merger "no new capacity is created", and, Proposition 3, "Mergers and
    acquisitions alleviate the problem whereas greenfield aggravates it."

FIGURES

  - `wear`, 0.08. The depreciation of private nonresidential fixed assets at current cost,
    divided by the net stock at the end of the year before (Bureau of Economic Analysis, fixed
    assets, 1951 to 2019): median 0.081, all years between 0.064 and 0.092, 0.072 before 1980 and
    0.086 after it. That idle plant wears at the rate of all plant is our own reading.
  - The cost of equipping a job that plant did not hold stays the sales module's `job_cost`, 3
    years of the wage: the plant behind a job in the record.

WHAT IS ADDED

That plant is counted in jobs; that a run starts with no idle plant; that idle plant is not
replaced; that the plant of a closed firm is lost and not sold to the firms that take on its
buyers; that people hired by any module other than the privatisation module need plant like
any others.
"""
import numpy as np
from core import Publish, SetAttribute, top_positions

PLANT = "plant in place"     # each firm's plant, in the jobs it holds at the standard use


class Capacity:
    name = "capacity"
    reads = ()                    # it also reads privatisation_jobs when the privatisation module is on
    supplies = ("idle_part", "places_built")
    figures = {                   # what the workbench calls each published number: label, unit, note
        "idle_part": ("Idle plant", "share", "Part of all plant that stands idle beyond the standard use."),
        "places_built": ("Jobs built", "rate", "Jobs that plant did not hold, equipped in the year just ended, as a part of employees."),
    }

    def __init__(self, wear=0.08, top=100):
        self.wear = wear          # part of idle plant that wears out in a year (fixed assets of the United States)
        self.top = top            # the firms that take over public services, as in the privatisation module

    def start(self, L):
        L.add_attribute(PLANT, L.n.copy(), 0.0, adds=True, owner=self.name)
        return {"idle_part": 0.0, "places_built": 0.0}

    def propose(self, L, rng):
        held, n = L.extra[PLANT], L.n
        built = np.maximum(n - held, 0.0)            # jobs equipped last year beyond the plant held
        idle = np.maximum(held - n, 0.0)
        plant = n + idle * (1.0 - self.wear)
        # Public employees whom the top 100 take over this year (privatisation module) arrive with their plant:
        # a takeover creates no new capacity. The module adds them to the top 100 in proportion to employees.
        arriving = float(L.accounts.get("privatisation_jobs", 0.0))
        if arriving > 0:
            top = top_positions(L.cap(), np.arange(len(L)), self.top)
            plant[top] += arriving * n[top] / max(float(n[top].sum()), 1e-300)
        whole = float(np.maximum(held, n).sum())
        return [SetAttribute(PLANT, plant, self.name),
                Publish("idle_part", float(idle.sum() / whole) if whole > 0 else 0.0, self.name),
                Publish("places_built", float(built.sum() / max(n.sum(), 1e-300)), self.name)]
