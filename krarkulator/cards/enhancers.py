import structlog

from krarkulator.cards.card import Card, Creature
from krarkulator.common import Color, Result

logger = structlog.getLogger()


class Enhancer(Card): ...


class HarmonicProdigy(Enhancer, Creature):
    name = "Harmonic Prodigy"
    cost = [Color.COLORLESS, Color.RED]

    def trigger_on_non_creature(self) -> Result:
        """Trigger when any spell is cast."""
        result = Result.empty()
        result.trigger_prowess()
        return result
