"""Base implementation for authorizer."""

from abc import ABC, abstractmethod
from functools import wraps
from typing import Callable

from ski_lift.core.auth.authenticator.base_authenticator import \
    BaseAuthenticator
from ski_lift.core.command.descriptor.executor.base import CommandExecutor
from ski_lift.core.command.descriptor.object import CommandDescriptor
from ski_lift.core.command.result.object import CommandResult


class BaseAuthorizer(CommandExecutor):
    """Base authorizer.
    
    This is a special `CommandExecutor` which can be used to authorize given
    commands.

    The idea is that the incoming commands can be handled specifically in
    their own process functions where if the given command is permitted or not
    can be decided individually. If the authorization process fails an error
    should be raised. The super class will generate the appropriate failed
    result with the given exception.

    The `authorize` function only exists to make a more fitting name for the
    context. The base `execute` function could have been used as
    well.
    """


    def __init__(self, authenticator: BaseAuthenticator, *args, **kwargs):
        self._authenticator = authenticator
        super().__init__(*args, **kwargs)

    @property
    def inserted_card(self) -> str:
        return self._authenticator.inserted_card

    def authorize(self, command: CommandDescriptor) -> CommandResult:
        return self.execute(command)

    def authenticate_delayed(self, command: CommandDescriptor) -> None:
        """Authenticate delayed.

        Delayed functions use the one-time only secret key based authentication
        provided by the `BaseAuthenticator` class.

        Args:
            command (CommandDescriptor): Command with the one-time only secret.
        """
        command.secret = self._authenticator.generate_secret()

class CommandAuthorizable(ABC):
    """Command authorizable.
    
    Inheriting from this marks to given class as a command authorizable which
    means that it's process functions can be authorized before execution.

    To trigger the authorization process for a given command you can use the
    `send_through_auth` function manually, however you need to evaluate
    yourself whether the result was successful or not
    (`result.is_successful`) and only allow the command execution accordingly.

    A much simpler way is to use the `send_trough_auth` decorator which does
    all the above automatically.
    """

    def __init__(self, authorizer: BaseAuthorizer, *args, **kwargs):
        self._authorizer: BaseAuthorizer = authorizer
        super().__init__(*args, **kwargs)

    def authenticate_delayed(self, command: CommandDescriptor) -> None:
        self._authorizer.authenticate_delayed(command)

    def send_through_auth(self, command: CommandDescriptor) -> CommandResult:
        return self._authorizer.authorize(command)
        

def send_through_auth(func: Callable[[CommandAuthorizable, CommandDescriptor], CommandResult]):
    """Send trough auth decorator.
    
    Place this decorator onto functions where you want to authorize the
    commands before execution. First the command will be sent to the authorizer
    class to check whether its alright to execute the function or not. If the
    result received is successful then command is executed normally otherwise
    the failed result from the authorizer is returned.

    Decorated functions are marked with a `_send_through_auth` attribute
    which makes them filterable for example in test cases via the inspect
    module.

    !WARNING!: Only use it on functions which follow the argument types
    defined in the type hint below otherwise the code could break.
    """
    func._send_through_auth = True
    @wraps(func)
    def wrapper(self: CommandAuthorizable, command: CommandDescriptor) -> CommandResult:
        result: CommandResult = self.send_through_auth(command)
        if result.is_successful:
            return func(self, command)
        return result
    return wrapper