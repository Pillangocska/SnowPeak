"""Base implementation for authentication."""


from ski_lift.core.auth.authenticator.base_authenticator import \
    BaseAuthenticator
from ski_lift.core.auth.authorizer.base_authorizer import BaseAuthorizer
from ski_lift.core.command.descriptor.object import (
    CommandDescriptor, InsertCardCommandDescriptor,
    RemoveCardCommandDescriptor)
from ski_lift.core.command.descriptor_result_factory import DescriptorResultFactory
from ski_lift.core.command.result.object import (CommandResult,
                                                 InsertCardCommandResult)


class SkiLiftAuthorizer(BaseAuthorizer):
    """Ski lift authorizer.
    
    This is a concrete implementation of the authorizer base class.

    Inserting and removing cards does not require any authentication or
    authorization.

    All the other commands are handled in the universal process function which
    only require card or secret based authentication.
    """

    def __init__(self, authenticator: BaseAuthenticator, *args, **kwargs):
        super().__init__(authenticator=authenticator ,*args, **kwargs)

    def process_insert_card_descriptor(self, command: InsertCardCommandDescriptor) -> InsertCardCommandResult:
        self._authenticator.authenticate(command.card_to_insert)
        return DescriptorResultFactory().build(command=command, outcome=CommandResult.OutCome.SUCCESSFUL)

    def process_remove_card_descriptor(self, command: RemoveCardCommandDescriptor) -> RemoveCardCommandDescriptor:
        self._authenticator.de_authenticate()
        return DescriptorResultFactory().build(command=command, outcome=CommandResult.OutCome.SUCCESSFUL)

    def process_descriptor_universally(self, command: CommandDescriptor) -> CommandResult:
        """Process descriptors universally.

        If a secret is present use secret based authentication. If the secret
        is incorrect an error will be raised.
        Otherwise check whether a local user is authenticated or not.

        If an error was raised the super class will create an appropriate
        failed result with the raised exception.
        """
        if command.secret is not None:
            self._authenticator.use_secret(command.secret)
        elif not self._authenticator.is_authenticated:
            BaseAuthenticator.raise_not_authenticated_error()
        return super().process_descriptor_universally(command)
