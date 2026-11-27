"""Module 7: the differential compass (Capital as Power, chapters 14, 16 and 17).

Dominant capital aims to beat the average. Merger is its usual route. The book says that
"temporary declines in mergers and acquisitions typically were 'compensated' for by sharp
increases in stagflation", and that stagflation "promptly abated" when amalgamation resumed.
So when the volume of mergers falls below the volume of recent decades, dominant capital turns
toward raising prices, as far as it is able to act in concert. When mergers resume, it lets
prices rest. The book names the decline of mergers as the trigger, so the rule compares volumes
of mergers and does not compare differential accumulation with its own past.

The module supplies two numbers: cohesion (how far dominant capital can act in concert) and the
intensity of stagflation. It never switches merger off.

This whole rule is an addition to the book, which describes conduct and gives no rule.
"""
import numpy as np
from core import Publish, readouts


class Compass:
    name = "compass"
    reads = ("concentration", "merger_volume", "unemployment")
    supplies = ("cohesion", "stagflation_intensity")

    def __init__(self, short=5, long=20, rise=0.15, fall=0.10, slack=20.0, usual_unemployment=0.05, top=100):
        self.short = short     # years over which the recent volume of mergers is judged
        self.long = long       # years that set the volume dominant capital has become used to
        self.slack = slack     # rise in cohesion per unit of unemployment above its usual level
        self.usual_unemployment = usual_unemployment
        self.rise = rise       # yearly rise in intensity when recent gains fall short
        self.fall = fall       # yearly fall in intensity when they do not
        self.top = top
        self.lndk = []
        self.intensity = 0.0

    def cohesion(self, L):
        # Concentration "makes it easier for firms to collude" (chapter 15). Crisis lets "a consensus
        # emerge within dominant capital", and growth undermines "the ability to coordinate" (chapter 16),
        # so cohesion rises with slack. That resistance lowers cohesion is an addition.
        A = L.accounts
        slack = 1 + self.slack * (A["unemployment"] - self.usual_unemployment)
        loosened = A.get("breadth_cohesion", 1.0)   # proletarianization loosens cohesion while it lasts (optional module); 1 without it
        return float(np.clip(A["concentration"] * max(slack, 0.0), 0, 1) * (1 - min(1.0, A.get("resistance", 0.0))) * loosened)

    def start(self, L):
        return {"cohesion": self.cohesion(L), "stagflation_intensity": 0.0}

    def propose(self, L, rng):
        self.lndk.append(L.accounts["merger_volume"])
        c = self.cohesion(L)
        h = self.lndk
        if len(h) > self.long:
            recent, used_to = np.mean(h[-self.short:]), np.mean(h[-self.long:])
            self.intensity += self.rise if recent < used_to else -self.fall
        self.intensity = float(np.clip(self.intensity, 0.0, min(1.0, 4 * c)))   # no concert, no inflation
        return [Publish("cohesion", c, self.name),
                Publish("stagflation_intensity", self.intensity, self.name)]
