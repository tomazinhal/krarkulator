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
        self.cast_counter: int = 0

    def flip(self):
        result = choice([Coin.HEADS, Coin.TAILS])
        self.history.append(result)
        logger.debug(f"Flipped {result.name}!")
        return result

    def trigger_on_cast(self) -> Result:
        results = Result.empty()
        for card in self.board:
            logger.debug(f"Casting the spell triggered {card}.")
            results += card.trigger_on_cast()
        return results

    def trigger_on_non_creature(self) -> Result:
        results = Result.empty()
        for card in self.board:
            logger.debug(f"Non creature cast from {card} triggered.")
            results += card.trigger_on_non_creature()
        return results

    def trigger_magecraft(self) -> Result:
        results = Result.empty()
        for card in self.board:
            results += card.trigger_magecraft()
        return results

    def cast(self, cast: Card) -> Result:
        """Cast the given card, triggering cards on board that the card
        triggers.

        Calls:
            - `Card.trigger_on_cast`
            - `Card.trigger_on_non_creature`
            - `Card.trigger_magecraft`
        """
        results = Result.empty()
        logger.debug(f"Casting {cast.name}.")
        cast.cast()
        results += self.trigger_on_cast()
        if cast.is_non_creature:
            results += self.trigger_on_non_creature()
        if cast.is_instant_sorcery:
            results += self.trigger_magecraft()
        return results

    @staticmethod
    def pay_spell(spell: Card, pool: Result) -> Result:
        logger.debug(f"Cost of spell: {spell.cost}, pool: {pool}")
        return pool - spell.cost

    def krark_trigger(self, spell: Card, board: list[Card]) -> Result:
        """Resolves a Krark trigger.
        If HEADS, put a copy on the stack and trigger respective cards in board.
        If TAILS, return card to hand.
        """
        coinflip = self.flip()
        result = Result.empty()
        assert spell.is_instant_sorcery
        match coinflip:
            case Coin.HEADS:
                result = self.trigger_magecraft()
                result += spell.copy()
            case Coin.TAILS:
                spell.bounce()
        return result

    def run(
        self, cast: Card, board: list[Card], pool: Optional[Result] = Result.empty()
    ) -> Result:
        self.cast_counter += 1
        pool += self.cast(cast)
        if any(isinstance(card, Krark) for card in board):
            logger.debug("Krark is on board.")
            pool += self.krark_trigger(spell=cast, board=board)
            enhancers = [card for card in board if isinstance(card, Enhancer)]
            for enhancer in enhancers:
                pool += self.krark_trigger(spell=cast, board=board)
        pool += cast.resolve()
        return pool

    def loop(self, spell: Card, board: list[Card], pool: Result) -> Result:
        logger.info(
            f"Casting {spell.name} with {", ".join([card.name for card in board])} in play and {pool.mana} available."
        )
        while spell.in_hand:
            if not Result.can_cast(pool, spell):
                break
            pool = self.pay_spell(spell, pool)
            pool = self.run(spell, board, pool)
        return pool
