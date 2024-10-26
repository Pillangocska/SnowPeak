"""Command panel."""

from ski_lift.core.command.descriptor.factory import CommandDescriptorFactory
from ski_lift.core.command.descriptor.object import ChangeStateCommandDescriptor
from ski_lift.core.controller import Controller


class CommandPanel:
    """Command panel.
    
    This class is designed to represent the core functionality of a control
    panel that a lift operator would access in real life.

    The class offers a number of functions which represent the real life
    buttons on a panel. These functions create the appropriate commands
    and execute them on the controller itself.

    This class is meant to be used via view objects for example a CLI view or
    a GUI based one.
    """

    def __init__(self, controller: Controller):
        self._controller = controller

    @property
    def inserted_card(self) -> str:
        return self._controller.inserted_card

    def insert_card(self, card_to_insert: str) -> None:
        self._controller.execute(
            CommandDescriptorFactory.create_insert_card(
                card_to_insert=card_to_insert
            )
        )

    def remove_card(self) -> None:
        self._controller.execute(
            CommandDescriptorFactory.create_remove_card(
                user_card=self.inserted_card
            )
        )

    def change_state(self, new_state: ChangeStateCommandDescriptor.Option) -> None:
        self._controller.execute(
            CommandDescriptorFactory.create_change_state(
                user_card=self.inserted_card,
                new_state=new_state,
            )
        )

    def display_status(self) -> None:
        self._controller.execute(
            CommandDescriptorFactory.create_display_status(
                user_card=self.inserted_card
            )
        )

    def abort_command(self, command_id: int) -> None:
        self._controller.execute(
            CommandDescriptorFactory.create_abort_command(
                user_card=self.inserted_card,
                command_to_abort=command_id,
            )
        )

    def emergency_stop(self) -> None:
        self._controller.execute(
            CommandDescriptorFactory.create_emergency_stop(
                user_card=self.inserted_card
            )
        )
