"""Module 8: resistance (Capital as Power, chapters 11, 14, 16 and 17).

"Power means the ability to impose order, and imposition presupposes resistance." The book
describes two kinds. The population is "impartial to breadth" and "almost always hostile to
depth", so inflation and unemployment meet popular resistance. Merger meets "roadblocks,
contradictions and counter-forces" of another kind: institutions that cannot adapt quickly.

The module holds one level of each. Popular resistance rises under stagflation and when
unemployment is far from its usual level. It lets wages keep up with prices, lowers the cohesion
of dominant capital, and raises its risk. Roadblocks rise with the volume of mergers. They slow
mergers and hold boundaries closed. Both fade when their causes are absent.

Two numbers for a whole society is the largest simplification in the model. All rates are additions.
"""
import numpy as np
from core import Scale, Publish, top_positions


class Resistance:
    name = "resistance"
    reads = ("unemployment", "concentration")
    supplies = ("resistance", "roadblocks")
    figures = {                   # what the workbench calls each published number: label, unit, note
        "resistance": ("Popular resistance", "index", "Resistance to rising prices, unemployment and the power of the top 100, from 0 to 1."),
        "roadblocks": ("Roadblocks to mergers", "index", "How strongly institutions slow mergers and keep boundaries closed, from 0 to 1."),
    }

    def __init__(self, from_inflation=0.6, from_mergers=3.0, from_unemployment=0.5, from_power=0.02, usual_unemployment=0.05,
                 fade=0.08, risk=0.5, start=0.0, top=100):
        self.from_inflation = from_inflation        # rise per unit of dominant capital's yearly price rise
        self.from_mergers = from_mergers            # rise per unit of merger volume
        self.from_unemployment = from_unemployment  # rise per unit of unemployment above its usual level
        self.usual_unemployment = usual_unemployment
        self.from_power = from_power                # rise per unit of the part of the economy dominant capital holds
        self.fade = fade                            # yearly decay
        self.risk = risk                            # rise in dominant capital's risk per unit rise in resistance
        self.level = start
        self.roadblocks = 0.0
        self.top = top

    def start(self, L):
        return {"resistance": self.level, "roadblocks": self.roadblocks}

    def propose(self, L, rng):
        A = L.accounts
        rise = (self.from_inflation * A.get("inflation_push", 0.0)
                + self.from_unemployment * max(0.0, A["unemployment"] - self.usual_unemployment)
                + self.from_power * A["concentration"]
                + A.get("protection_anger", 0.0)                # anger at bailouts of dominant capital (another module); 0 without it
                + A.get("energy_grievance", 0.0)                # a fall in livelihood energy per head (another module); 0 without it
                + A.get("externalisation_grievance", 0.0))      # burdens shifted off the books onto employees and communities (another module); 0 without it
        repressed = A.get("repression", 0.0) * self.level       # organised force wears resistance down (another module)
        repressed = repressed * (1 - A.get("eruption_stays_force", 0.0))   # an eruption stays the hand of force (another module); 0 without it
        repressed = repressed + A.get("household_debt_placation", 0.0) * self.level   # new borrowing dampens resentment (another module); 0 without it
        new = float(np.clip(self.level + rise - self.fade * self.level - repressed, 0.0, 1.0))
        self.roadblocks = float(np.clip(self.roadblocks + self.from_mergers * A.get("merger_volume", 0.0)
                                        - self.fade * self.roadblocks
                                        # a government organ that owns shares and trails the average wears roadblocks down (another module); 0 without it
                                        - A.get("sovereign_relief", 0.0) * self.roadblocks, 0.0, 1.0))
        changes = [Publish("resistance", new, self.name), Publish("roadblocks", self.roadblocks, self.name)]
        if new > self.level:
            dominant = np.zeros(len(L), dtype=bool)
            dominant[top_positions(L.cap(), np.arange(len(L)), self.top)] = True
            changes.append(Scale("risk", np.where(dominant, 1 + self.risk * (new - self.level), 1.0), self.name))
        self.level = new
        return changes
