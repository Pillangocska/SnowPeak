"""RabbitMQ based authentication."""

from ski_lift.core.auth.authenticator.base_authenticator import \
    BaseAuthenticator


class RabbitMQAuth(BaseAuthenticator):
    """RabbitMQ based authentication.
    
    This authentication method transmits a message to the central backend
    containing the `card_number`, and based on the response received, the
    authentication status can be established.
    """


    def check_card_eligibility(self, card_number: str) -> bool:
        # TODO: send message to central backend and wait for the response
        # maybe use a timeout
        raise NotImplementedError()