from typing import Iterable

from ski_lift.core.auth.authenticator.base_authenticator import \
    BaseAuthenticator


class InMemoryAuthenticator(BaseAuthenticator):
    """Memory based authentication.
    
    This is an example implementation of the authentication object which stores
    the eligible cards in set.

    This version of authentication should be used for testing and 
    developing purposes only.
    """

    def __init__(self):
        super().__init__()
        self._allowed_cards = set()

    def check_card_eligibility(self, card_number: str) -> bool:
        return card_number in self._allowed_cards
        
    def add(self, card_number: str):
        self._allowed_cards.add(card_number)

    def remove(self, card_number: str):
        self._allowed_cards.discard(card_number)

    def load(self, card_numbers: Iterable[str]):
        self._allowed_cards = self._allowed_cards.union(set(card_numbers))

    def clear(self):
        self._allowed_cards.clear()
