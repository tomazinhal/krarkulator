import logging

import structlog

from krarkulator.cards.card import Card
from krarkulator.cards.enhancers import HarmonicProdigy
from krarkulator.cards.krark import Krark
from krarkulator.cards.rite import RiteOfFlame
from krarkulator.cards.ska import SKA
from krarkulator.common import Mana, Result
from krarkulator.engine import Coin, Engine

LEVEL = logging.INFO

structlog.stdlib.recreate_defaults()

structlog.configure(wrapper_class=structlog.make_filtering_bound_logger(LEVEL))


logger = structlog.getLogger("krarkulator")

if __name__ == "__main__":
    board: list[Card] = [
        Krark(),
        HarmonicProdigy(),
        # HarmonicProdigy(),
        # HarmonicProdigy(),
        SKA(),
    ]
    card = RiteOfFlame()
    starting_pool = Result(mana=Mana(red=1))
    engine = Engine(board=board)
    result = engine.loop(spell=card, board=board, pool=starting_pool)
    logger.info(f"Cast {card.name} {engine.cast_counter} times")
    logger.info(f"Copied {card.name} {engine.history.count(Coin.HEADS)} times")
    logger.info(result)
