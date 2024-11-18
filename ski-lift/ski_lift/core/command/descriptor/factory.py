"""Command descriptor factory."""

from datetime import datetime
from typing import Optional

from ski_lift.core.command.descriptor.object import (
    AbortCommandDescriptor, ChangeStateCommandDescriptor,
    DisplayStatusCommandDescriptor, EmergencyStopCommandDescriptor,
    InsertCardCommandDescriptor, MessageReportCommandDescriptor,
    RemoveCardCommandDescriptor)


class CommandDescriptorFactory:
    """Command descriptor factory.
    
    This is a simple factory that makes it easier to instantiate
    all the various command descriptors.
    """

    @classmethod
    def create_insert_card(
        cls, *, card_to_insert: str, time: Optional[datetime] = None,
    ) -> InsertCardCommandDescriptor:
        return InsertCardCommandDescriptor(
            user_card=None,
            time=time or datetime.now(),
            card_to_insert=card_to_insert,
        )
    
    @classmethod
    def create_remove_card(
        cls, *, user_card: str, time: Optional[datetime] = None
    ):
        return RemoveCardCommandDescriptor(
            user_card=user_card,
            time=time or datetime.now(),
        )
    
    @classmethod
    def create_change_state(
        cls,
        *,
        user_card: str,
        time: Optional[datetime] = None,
        delay: int = 0,
        new_state: ChangeStateCommandDescriptor.Option,
    ) -> ChangeStateCommandDescriptor:
        return ChangeStateCommandDescriptor(
            user_card=user_card,
            time=time or datetime.now(),
            delay=delay,
            new_state=new_state,
        )
    
    @classmethod
    def create_display_status(
        cls,
        *,
        user_card: str,
        time: Optional[datetime] = None,
    ) -> DisplayStatusCommandDescriptor:
        return DisplayStatusCommandDescriptor(
            user_card=user_card,
            time=time or datetime.now(),
        )
    
    @classmethod
    def create_abort_command(
        cls,
        *,
        user_card: str,
        command_to_abort: int,
        time: Optional[datetime] = None,
    ) -> AbortCommandDescriptor:
        return AbortCommandDescriptor(
            user_card=user_card,
            time=time or datetime.now(),
            command_to_abort=command_to_abort,
        )
    
    @classmethod
    def create_emergency_stop(
        cls,
        *,
        user_card: str,
        time: Optional[datetime] = None,
        delay: int = 0,
    ) -> EmergencyStopCommandDescriptor:
        return EmergencyStopCommandDescriptor(
            user_card=user_card,
            time=time or datetime.now(),
            delay=delay,
        )

    @classmethod
    def create_message_report(
        cls,
        *,
        user_card: str,
        time: Optional[datetime] = None,
        delay: int = 0,
        severity: MessageReportCommandDescriptor.Severity,
        message: str,
    ) -> MessageReportCommandDescriptor:
        return MessageReportCommandDescriptor(
            user_card=user_card,
            time=time or datetime.now(),
            delay=delay,
            severity=severity,
            message=message
        )
