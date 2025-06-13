from structlog import getLogger

from krarkulator.cards.card import Sorcery
from krarkulator.common import Color, Result

logger = getLogger()


class RiteOfFlame(Sorcery):
    cost = Result.from_colors([Color.RED])
    name = "Rite of Flame"
    is_instant_sorcery = True
    is_non_creature = True
    output = Result.from_colors([Color.RED, Color.RED])
