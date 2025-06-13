from typing import Optional

from structlog import getLogger

from krarkulator.common import Color, Result

logger = getLogger()


class Card:
    cost: list[Color]
    name: str
    is_non_creature: bool
    is_instant_sorcery: bool
    output: Result
    in_hand = True

    def bounce(self):
        """Set the card to be in hand."""
        if self.in_hand:
            logger.info(f"{self} already in  hand.")
            return
        logger.info(f"Returned {self} to hand.")
        self.in_hand = True

    def cast(self):
        """Casting a spell means removing it from the hand."""
        self.in_hand = False

    def trigger_on_non_creature(self) -> Optional[Result]:
        """Trigger when a non creature spell is cast, Kitten for example."""
        raise NotImplementedError

    def trigger_magecraft(self) -> Optional[Result]:
        """Trigger when an instant or sorcery is cast or copied."""
        raise NotImplementedError

    def trigger_on_cast(self) -> Optional[Result]:
        """Trigger when any spell is cast."""
        logger.info(f"Triggered on-cast trigger from {self.name}")
        raise NotImplementedError

    def resolve(self) -> Optional[Result]:
        if self.in_hand:
            return
        return self.output

    def copy(self) -> Result:
        logger.debug(f"Copied {self.name}")
        return self.output

    def __repr__(self) -> str:
        return self.name


class Sorcery(Card):
    is_non_creature = True
    is_instant_sorcery = True

    def trigger_on_non_creature(self) -> Optional[Result]:
        return None

    def trigger_magecraft(self) -> Optional[Result]:
        return None

    def trigger_on_cast(self) -> Optional[Result]:
        return None


class Creature(Card):
    is_non_creature = False
    is_instant_sorcery = False

    def bounce(self):
        logger.warning("Can't return creature to hand.")

    def trigger_on_non_creature(self) -> Optional[Result]:
        return None

    def trigger_magecraft(self) -> Optional[Result]:
        return None

    def trigger_on_cast(self) -> Optional[Result]:
        return None
