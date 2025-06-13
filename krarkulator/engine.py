from enum import Flag
from random import choice
from typing import Optional

from structlog import getLogger

from krarkulator.cards.card import Card
from krarkulator.cards.enhancers import Enhancer
from krarkulator.cards.krark import Krark
from krarkulator.common import Result

logger = getLogger()


class Coin(Flag):
    HEADS = True
    TAILS = False


class Engine:
    def __init__(self, board):
        self.board: list[Card] = board
        self.history: list[Coin] = []
        self.result: Result = Result.empty()

    def flip(self):
        result = choice([Coin.HEADS, Coin.TAILS])
        self.history.append(result)
        logger.info(f"Flipped {result.name}!")
        return result

    def trigger_on_non_creature(self) -> Result:
        results = Result.empty()
        for card in self.board:
            results += card.trigger_on_non_creature()
        return results

    def trigger_magecraft(self) -> Result:
        results = Result.empty()
        for card in self.board:
            logger.info(f"Magecraft from {card} triggered.")
            results += card.trigger_magecraft()
        return results

    def cast(self, cast: Card) -> Result:
        """Cast the given card,, triggering cards on board that the card
        triggers.

        Calls:
            - `Card.trigger_on_cast`
            - `Card.trigger_on_non_creature`
            - `Card.trigger_magecraft`
        """
        results = Result.empty()
        logger.info(f"Casting {cast.name}.")
        cast.cast()
        for card in self.board:
            logger.debug(f"Checking {card.name}")
            results += card.trigger_on_cast()
            if cast.is_non_creature:
                results += self.trigger_on_non_creature()
            if cast.is_instant_sorcery:
                results += self.trigger_magecraft()
        return results

    @staticmethod
    def pay_spell(cast: Card, pool: Result) -> Result:
        logger.debug(f"Cost of spell: {cast.cost}, pool: {pool}")
        return pool - Result.from_colors(cast.cost)

    def run(
        self, cast: Card, board: list[Card], pool: Optional[Result] = Result.empty()
    ) -> Result:
        pool += self.cast(cast)
        # logger.debug("Running")
        if any(isinstance(card, Krark) for card in board):
            logger.info("Krark is on board.")
            for _ in range(len([isinstance(card, Enhancer) for card in board])):
                if self.flip():
                    pool += self.trigger_magecraft()
                    pool += cast.copy()
                else:
                    cast.bounce()
        pool += cast.resolve()
        return pool

    def loop(self, spell: Card, board: list[Card], pool: Result) -> Result:
        logger.debug(
            f"Casting {spell.name} with {" and ".join([card.name for card in board])} in play and {pool.mana} available."
        )
        while spell.in_hand:
            if not Result.can_cast(pool, spell):
                break
            pool = self.pay_spell(spell, pool)
            logger.debug(f"Pool status: {pool}")
            pool += self.run(spell, board, pool)
        return pool
