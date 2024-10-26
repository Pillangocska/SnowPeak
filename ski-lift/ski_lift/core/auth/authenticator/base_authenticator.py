"""Base implementation for authentication."""

import secrets
from abc import ABC, abstractmethod
from typing import List, Optional


class BaseAuthenticator(ABC):
    """Base class for authentication.
    
    Users will authenticate themselves with magnetic cards which are
    represented via the `card_number: str` parameter.

    Generally speaking authentication can be requested with the `authenticate`
    function which relies on the `check_card_eligibility` abstract function.
    Subclasses should override this function and nothing else for their
    custom eligibility logic. Checkout the `InMemoryAuthenticator` example
    implementation.

    The class also supports secrets, which are one-time keys for
    authentication.These keys solve the problem of authenticating remote
    requests or delayed commands. If the local user (the ski lift operator)
    logs out before a delayed command is executed or when a remote request
    arrives without a logged-in user, the command can still be authenticated
    using the secret.
    """

    class NotAuthenticatedError(Exception):
        """Not authenticated error.
        
        Should be raised when the user tries the execute a command which
        requires authentication without being authenticated.
        """

    class InvalidCardNumberError(Exception):
        """Invalid card number error.
        
        Should be raised when a provided `user_card` fails the authentication
        process. More specifically the `check_card_eligibility` function
        returned `False`.
        """

    class InvalidSecretError(Exception):
        """Invalid secret error.
        
        Should be raised when a one-time secret that is being used does not
        exist.
        """

    class TimeOutError(Exception):
        """Time out error.
        
        Should be raised when the authentication process takes more time then
        a predefined timeout constant.
        """

    def __init__(self):
        self._card_number: Optional[str] = None
        self._secrets: List[str] = []

    @property
    def inserted_card(self) -> Optional[str]:
        """Currently authenticated local user's card or None."""
        return self._card_number
    
    @property
    def is_authenticated(self) -> bool:
        """Check whether a local user is authenticated or not."""
        return self._card_number is not None

    def authenticate(self, card_number: str):
        """Authenticate the given card number.

        Card eligibility will be determined via the `check_card_eligibility`
        function.

        Do not modify this function. If you need custom eligibility logic
        then override the `check_card_eligibility` function.

        Raises:
            InvalidCardNumberError: Raised when the card is not eligible.

        Args:
            card_number (str): Represents the magnetic card of the operators.
        """
        if self.check_card_eligibility(card_number):
            self._card_number = card_number
        else:
            self.raise_invalid_card_error(card_number)

    @abstractmethod
    def check_card_eligibility(self, card_number: str) -> bool:
        """Check card eligibility logic.

        Custom eligibility logic for the given user card.
        Override this function for custom logic in subclasses.

        Args:
            card_number (str): Represents the magnetic card of the operators.

        Returns:
            bool: True if the `user_card` is eligible.
        """
        pass

    def de_authenticate(self):
        """Simply de authenticated the user by setting it to `None`"""
        self._card_number = None
    
    def generate_secret(self) -> str:
        """Generate secret.

        Generate a one-time only secret that can be used for authentication
        which is stored in a list.

        Returns:
            str: Generated secret.
        """
        secret: str = secrets.token_hex(16)
        self._secrets.append(secret)
        return secret
    
    def use_secret(self, secret: str):
        """Use secret.

        Use the one-time secret and remove it from the list of secrets.

        Raises:
            InvalidSecretError: Raised when the secret does not exist.

        Args:
            secret (str): Secrete being used.
        """
        if secret in self._secrets:
            self._secrets.remove(secret)
        else:
            self.raise_invalid_secret_error(secret)
    
    @classmethod
    def raise_not_authenticated_error(cls):
        raise cls.NotAuthenticatedError('Error: Card Not Detected or Rejected')

    @classmethod
    def raise_invalid_card_error(cls, card_number: str):
        raise cls.InvalidCardNumberError(f'Error: Card with number "{card_number}" was rejected!')
    
    @classmethod
    def raise_invalid_secret_error(cls, secret: str):
        raise cls.InvalidSecretError(f'Error: Secret "{secret} was rejected!"')

    @classmethod
    def raise_time_out_error(cls):
        raise cls.TimeOutError(f'Error: Authentication timeout reached. The host might be down.')
