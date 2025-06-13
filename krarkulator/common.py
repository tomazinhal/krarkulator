from dataclasses import dataclass
from enum import Enum
from typing import Optional, Self

import structlog

logger = structlog.getLogger()


class Color(Enum):
    WHITE = "white"
    BLUE = "blue"
    BLACK = "black"
    RED = "red"
    GREEN = "green"
    COLORLESS = "colorless"
    RAINBOW = "rainbow"


class Object(Enum):
    TREASURE = "treasure"


class Action(Enum):
    UNTAP = "untap"
    DRAW = "draw"
    FLICKER = "flicker"


@dataclass
class Mana:
    white: int = 0
    blue: int = 0
    black: int = 0
    red: int = 0
    green: int = 0
    colorless: int = 0

    def __repr__(self) -> str:
        self.white
        self.blue
        self.black
        self.red
        self.green
        self.colorless
        return str(
            [{color: value} for color, value in self.__dict__.items() if value != 0]
        )


@dataclass
class Result:
    mana: Mana
    treasures: int = 0
    untaps: int = 0
    prowess: int = 0

    @classmethod
    def empty(cls) -> Self:
        return cls(mana=Mana())

    @classmethod
    def from_colors(cls, input: list[Color]) -> Self:
        mana = Mana()
        for item in input:
            match item:
                case Color.WHITE:
                    mana.white += 1
                case Color.BLUE:
                    mana.blue += 1
                case Color.BLACK:
                    mana.black += 1
                case Color.RED:
                    mana.red += 1
                case Color.GREEN:
                    mana.green += 1
                case Color.COLORLESS:
                    mana.colorless += 1
        return cls(mana=mana)

    def trigger_prowess(self, times: int = 1) -> None:
        """Triggers prowess `times` times."""
        self.prowess += times

    def can_cast(self, spell) -> bool:
        """Check if a spell can be cost. Done by comparing the cost of a spell
        with the available pool."""
        for color, available_mana in self.mana.__dict__.items():
            color_mana_cost = getattr(spell.cost.mana, color)
            if available_mana < color_mana_cost:
                logger.info(f"{spell.name} can NOT be cast.")
                return False
        logger.debug(f"{spell.name} can be cast.")
        return True

    def __add__(self, other: Optional[Self]) -> Self:
        """Overloaded left add for Result."""
        if other is None:
            return self
        self.mana.white += other.mana.white
        self.mana.blue += other.mana.blue
        self.mana.black += other.mana.black
        self.mana.red += other.mana.red
        self.mana.green += other.mana.green
        self.mana.colorless += other.mana.colorless
        self.untaps += other.untaps
        self.treasures += other.treasures
        self.prowess += other.prowess
        return self

    def __radd__(self, other: Optional[Self]) -> Self:
        """Overloaded right add for Result."""
        return self.__add__(other)

    def __sub__(self, other: Optional[Self]) -> Self:
        """Overloaded left subtract for Result."""
        if other is None:
            return self
        self.mana.white -= other.mana.white
        self.mana.blue -= other.mana.blue
        self.mana.black -= other.mana.black
        self.mana.red -= other.mana.red
        self.mana.green -= other.mana.green
        self.mana.colorless -= other.mana.colorless
        self.untaps -= other.untaps
        self.treasures -= other.treasures
        self.prowess -= other.prowess
        return self

    def __rsub__(self, other: Optional[Self]) -> Self:
        """Overloaded right subtract for Result."""
        return self.__sub__(other)
