"""Command line interface view"""

from string import Template
from typing import Any

from ski_lift import __version__
from ski_lift.core.command.result.object import (AbortCommandResult,
                                                 ChangeStateCommandResult,
                                                 CommandResult,
                                                 DisplayStatusCommandResult,
                                                 EmergencyStopCommandResult,
                                                 InsertCardCommandResult,
                                                 RemoveCardCommandResult)
from ski_lift.core.remote.suggestion.suggestion import Suggestion
from ski_lift.core.view.base_view import BaseView

from ..command.result.object import MessageReportCommandResult
from ..controller import Controller

DEFAULT_HELP_TEXT: str = """
Available commands:

    insert_card <card_id>
        - Inserts a card into the system, using the specified <card_id>.

    remove_card
        - Removes the currently inserted card from the system.

    change_state <state>
        - Changes the engine state to the specified <state>.
          Valid states include MAX_STEAM, FULL_STEAM, HALF_STEAM, and STOPPED.

    display_status
        - Displays the current status of the lift system.

    emergency_stop
        - Stop the ski lift in a case of an emergency.

    abort <command_id>
        - Aborts a delayed command with the specified <command_id>.

    report <severity> <message>
        - Send a report to the central room.
        - Possible severities are INFO, WARNING and DANGER.

    suggestion_level <SEVERITY>
        - Suggestions with severities equal to or greater than the selected level will be displayed.
        - Order is INFO < WARNING < DANGER.
        - If you set it to NONE, no suggestions will be displayed.

    help
        - Displays this help message listing all available commands.
"""

WELCOME_TEXT_TEMPLATE: str = """
 __                      ___           _
/ _\\_ __   _____      __/ _ \\___  __ _| | __
\\ \\| '_ \\ / _ \\ \\ /\\ / / /_)/ _ \\/ _` | |/ /
_\\ \\ | | | (_) \\ V  V / ___/  __/ (_| |   <
\\__/_| |_|\\___/ \\_/\\_/\\/    \\___|\\__,_|_|\\_\\

version: $version
lift id: $lift_id$current_user
"""

class CommandLineInterfaceView(BaseView):

    def __init__(self, controller: Controller, *args, **kwargs) -> None:
        self._suggestion_level: str = ['INFO', 'WARNING', 'DANGER']
        super().__init__(controller, *args, **kwargs)

    class UnsupportedCommand(Exception):
        pass

    class UnsupportedChangeStateOption(Exception):
        pass

    @property
    def welcome_text(self) -> str:
        return Template(WELCOME_TEXT_TEMPLATE).substitute(
            version=__version__.__version__,
            lift_id=self.lift_id,
            current_user=f'\nuser: {self.inserted_card}' if self.inserted_card else '',
        )


    def start_handling_user_inputs(self) -> None:
        try:
            self.start_handling_cli_input()
        except KeyboardInterrupt:
            print('Exiting...')

    def start_handling_cli_input(self) -> None:
        print(self.welcome_text)
        while True:
            user_input = input('\n> ').lower().split()
            command_name = user_input[0]
            args = user_input[1:]

            try:
                match(command_name):
                    case 'suggestion_level': self.set_suggestion_level(*args)
                    case 'insert_card': self.insert_card(*args)
                    case 'remove_card': self.remove_card()
                    case 'change_state': self.change_state(*args)
                    case 'display_status': self.display_status()
                    case 'emergency_stop': self.emergency_stop()
                    case 'report': self.message_report(*args)
                    case 'abort': self.abort_command(*args)
                    case 'help': print(DEFAULT_HELP_TEXT)
                    case 'exit': break
                    case _: raise self.UnsupportedCommand()
            except self.UnsupportedCommand:
                print(
                    f'Did not recognize "{command_name}" command. Type "help" to display the available commands.'
                )
            except TypeError as type_exc:
                print(f'Incorrect arguments for command "{command_name}". Type "help" to display correct usage.')
    def set_suggestion_level(self, level: str):
        match(level.upper()):
            case 'INFO': self._suggestion_level = ['INFO', 'WARNING', 'DANGER']
            case 'WARNING': self._suggestion_level = ['WARNING', 'DANGER']
            case 'DANGER': self._suggestion_level = ['DANGER']
            case 'NONE': self._suggestion_level = []
            case _: print(f'Did not recognize level "{level}".')
                
    def process_insert_card_result(self, result: InsertCardCommandResult) -> Any:
        self.handle_result(result, 'CARD ACCEPTED')

    def process_remove_card_result(self, result: RemoveCardCommandResult) -> Any:
        self.handle_result(result, 'CARD REMOVED')

    def process_change_state_result(self, result: ChangeStateCommandResult) -> Any:
        self.handle_result(result, 'STATE CHANGED')

    def process_display_status_result(self, result: DisplayStatusCommandResult) -> Any:
        self.handle_result(result, result.result)

    def process_abort_command_result(self, result: AbortCommandResult) -> Any:
        self.handle_result(result, f'COMMAND {result.command.command_to_abort} ABORTED')

    def process_emergency_stop_result(self, result: EmergencyStopCommandResult) -> Any:
        self.handle_result(result, 'ENGINE STOPPED')

    def process_message_report_result(self, result: MessageReportCommandResult) -> Any:
        self.handle_result(result, 'REPORT SENT')

    def handle_result(self, result: CommandResult, message_on_success: str):
        if result.outcome == CommandResult.OutCome.DELAYED:
            print(f'Type "abort {result.command.id}" to abort it.\n', end='')
        elif result.is_successful:
            print(message_on_success)
        else:
            print(str(result.exception))

    def display_suggestion(self, suggestion: Suggestion, reset_input=True) -> None:
        if suggestion.category.name in self._suggestion_level:
            formatted_time = suggestion.time.strftime("%Y-%m-%d %H:%M:%S")
            print(f'\n[{formatted_time}] [{suggestion.category.name}]  {suggestion.message}{'\n\n>' if reset_input else '\n'}', end='')
