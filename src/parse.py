from dataclasses import dataclass
import discord
from random import randint

@dataclass
class GrowthClass:
    _id: str
    _hp: int
    _str: int
    _mag: int
    _dex: int
    _spd: int
    _lck: int
    _def: int
    _res: int

    def __post_init__(self):
        self._id = self._id.split("-", 1)[1]
    
    def __str__(self):
        return self._id
    
    @property
    def embed(self):
        return discord.Embed.from_dict({
            "title": self._id,
            "type": "rich",
            "fields": [
                {"inline": True, "name": name, "value": f"`{value}`"}  for name,value in 
                    (("HP", self._hp), ("STR", self._str), ("MAG", self._mag), ("DEX", self._dex), ("SPD", self._spd), ("LCK", self._lck), ("DEF", self._def), ("RES", self._res))
            ]
        })

@dataclass
class GrowthUnit:
    _id: str
    _class: str
    _hp: int
    _str: int
    _mag: int
    _dex: int
    _spd: int
    _lck: int
    _def: int
    _res: int
    
    def __post_init__(self):
        self._id = self._id.split("-", 1)[1]
        self._level = 1
    
    def __str__(self):
        return self._id
    
    def level_up(self, cl):
        self._level+=1
        for stat in ("_hp", "_str", "_mag", "_dex", "_spd", "_lck", "_def", "_res"):
            current = getattr(self, stat, 0)
            rate = getattr(cl, stat, 0)
            if randint(1, 100) <= rate:
                setattr(self, stat, current+1)
        

    @property
    def embed(self):
        return discord.Embed.from_dict({
            "title": f"{self._id}: Lv. {self._level} {self._class}",
            "type": "rich",
            "fields": [
                {"inline": True, "name": name, "value": f"`{value}`"}  for name,value in 
                    (("HP", self._hp), ("STR", self._str), ("MAG", self._mag), ("DEX", self._dex), ("SPD", self._spd), ("LCK", self._lck), ("DEF", self._def), ("RES", self._res))
            ]
        })