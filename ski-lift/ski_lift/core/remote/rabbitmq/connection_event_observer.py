"""Connection event observer."""


from abc import ABC, abstractmethod


class ConnectionEventObserver(ABC):
    """Connection event observer.
    
    Observer that can listen to different kinds of connection events related
    to remote services.
    """

    @abstractmethod
    def on_connected(self, exchange: str):
        """Invoked when the connection is successfully made."""

    
    @abstractmethod
    def on_connected_error(self, exchange: str):
        """Invoked when connection cannot be established"""

    @abstractmethod
    def on_closed(self, exchange: str):
        """Invoked when the connection was closed."""
            