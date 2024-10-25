"""Concrete descriptor implementation for testing purposes."""


from ski_lift.core.command import CommandDescriptor
from ski_lift.core.command.processor.base import CommandProcessor


class ConcreteCommandDescriptor(CommandDescriptor):

    def accept(self, processor: CommandProcessor):
        pass
