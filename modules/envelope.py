"""Module 9: breaking the envelope (Capital as Power, chapters 14 and 15).

It can run in place of the contest over a boundary (module 14), which runs by default.

Dominant capital opens its own boundaries: "to take advantage of this broader pool, dominant
capital has to break through its original 'envelope'". The model is not told when.

Pressure on a boundary is high when dominant capital already holds most of what it can reach.
Resistance pushes back. A boundary opens while pressure exceeds resistance by a margin, and
closes again when resistance exceeds pressure by a wide margin. The sector boundary gives way
before the national one.

This whole rule is an addition to the book, which says who opens the envelopes and why, and
gives no rule for when. The model cannot say what form an opening takes.
"""
import numpy as np
from core import Set, Publish


class Envelope:
    name = "envelope"
    replaces = ("boundary contest",)   # both move the same two boundaries, so only one of them runs
    reads = ("pool_open",)
    supplies = ("pressure",)
    figures = {                   # what the workbench calls each published number: label, unit, note
        "pressure": ("Pressure on boundaries", "share", "Part of its reach that the top 100 already hold."),
    }

    def __init__(self, threshold=0.5, speed=0.2, close_margin=0.3):
        self.threshold = threshold        # how much of its reach dominant capital must hold before a boundary gives
        self.speed = speed                # yearly movement of a boundary per unit of net pressure
        self.close_margin = close_margin  # how far resistance must exceed pressure to close a boundary

    def start(self, L):
        return {"pressure": 0.0}

    def propose(self, L, rng):
        pressure = 1.0 - L.accounts["pool_open"]         # the part of its reach that dominant capital already holds
        resistance = L.accounts.get("roadblocks", 0.0)
        net = pressure - self.threshold - resistance
        sector, nation = L.shared.get("perm_sector", 0.0), L.shared.get("perm_nation", 0.0)
        changes = [Publish("pressure", pressure, self.name)]
        if net > 0:                                       # the nearest closed boundary gives way first
            if sector < 1.0:
                changes.append(Set("perm_sector", min(1.0, sector + self.speed * net), self.name))
            elif nation < 1.0:
                changes.append(Set("perm_nation", min(1.0, nation + self.speed * net), self.name))
        elif resistance - pressure > self.close_margin:   # resistance wins: the widest open boundary closes first
            back = self.speed * (resistance - pressure - self.close_margin)
            if nation > 0.0:
                changes.append(Set("perm_nation", max(0.0, nation - back), self.name))
            elif sector > 0.0:
                changes.append(Set("perm_sector", max(0.0, sector - back), self.name))
        return changes
