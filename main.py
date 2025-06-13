import structlog

from krarkulator.cards.card import Card
from krarkulator.cards.krark import Krark
from krarkulator.cards.rite import RiteOfFlame
from krarkulator.common import Mana, Result
from krarkulator.engine import Coin, Engine

structlog.stdlib.recreate_defaults()

logger = structlog.getLogger("krarkulator")

if __name__ == "__main__":
    board: list[Card] = []  # , HarmonicProdigy()]
    cast = RiteOfFlame()
    starting_pool = Result(mana=Mana(red=1))
    engine = Engine(board=board)
    # results = engine.run(cast=cast)
    result = engine.loop(spell=cast, board=board, pool=starting_pool)
    logger.info(f"Copied {cast.name} {engine.history.count(Coin.HEADS)} times")
    logger.info(result)
