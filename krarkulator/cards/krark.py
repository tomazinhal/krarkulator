import structlog

from krarkulator.cards.card import Creature
from krarkulator.common import Color

logger = structlog.getLogger()


class Krark(Creature):
    # the greedy goblin
    cost = [Color.RED]
    name = "Krark, the Thumbless"

    def trigger_on_cast(self):
        """Trigger when any spell is cast."""
        return
