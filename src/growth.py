from dataclasses import dataclass
from typing import Dict, List
from random import randint

# [rate, initial]
StatDict = Dict[str, List[int]]

@dataclass
class Unit:
    name: str
    _stats: StatDict
    level: int = 1

    @property
    def stats(self):
        return f"{self.name} (Level {self.level}): " + ", ".join(f"{key}: {stat[1]}" for key, stat in self._stats.items())

    def level_up(self, times: int = 1):
        for i in range(times):
            for stat, pair in self._stats.items():
                rate = pair[0]
                roll = randint(1, 100)
                if roll <= rate:
                    self._stats[stat][1] += 1
            self.level += 1


Hari = Unit(
    "Hari", {
        "HP": [100, 20]
    }
)

print(Hari.stats)
Hari.level_up(10)
print(Hari.stats)