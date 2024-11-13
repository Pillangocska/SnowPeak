"""Command line interface view"""

from typing import Any
from ski_lift.core.command.descriptor.object import ChangeStateCommandDescriptor
from ski_lift.core.command.result.object import AbortCommandResult, ChangeStateCommandResult, CommandResult, DisplayStatusCommandResult, EmergencyStopCommandResult, InsertCardCommandResult, RemoveCardCommandResult
from ski_lift.core.view.base_view import BaseView
from ski_lift.core.remote.suggestion.suggestion import Suggestion
from tests.entity import command
from string import Template
from ski_lift import __version__


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

    class UnsupportedCommand(Exception):
        pass

    class UnsupportedChangeStateOption(Exception):
        pass

    @property
    def welcome_text(self) -> str:
        return Template(WELCOME_TEXT_TEMPLATE).substitute(
            version=__version__.__version__,
            lift_id=self._lift_id,
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
                    case 'insert_card': self.insert_card(*args)
                    case 'remove_card': self.remove_card()
                    case 'change_state': self.change_state(self.parse_to_engine_option(*args))
                    case 'display_status': self.display_status()
                    case 'emergency_stop': self.emergency_stop()
                    case 'abort': self.abort_command(*args)
                    case 'help': print(DEFAULT_HELP_TEXT)
                    case 'exit': break
                    case _: raise self.UnsupportedCommand()
            except self.UnsupportedCommand:
                print(
                    f'Did not recognize "{command_name}" command. Type "help" to display the available commands.'
                )
            except Exception as exc:
                print(str(exc))

    def parse_to_engine_option(self, option_str: str) -> ChangeStateCommandDescriptor.Option:
        match(option_str):
            case 'max_steam': return ChangeStateCommandDescriptor.Option.MAX_STEAM
            case 'full_steam': return ChangeStateCommandDescriptor.Option.FULL_STEAM
            case 'half_steam': return ChangeStateCommandDescriptor.Option.HALF_STEAM
            case 'stopped': return ChangeStateCommandDescriptor.Option.STOP
            case _: raise self.UnsupportedChangeStateOption()

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

    def handle_result(self, result: CommandResult, message_on_success: str):
        if result.outcome == CommandResult.OutCome.DELAYED:
            print(f'Type "abort {result.command.id}" to abort it.\n\n>', end='')
        elif result.is_successful:
            print(message_on_success)
        else:
            print(str(result.exception))

    def display_suggestion(self, suggestion: Suggestion, reset_input=True) -> None:
        formatted_time = suggestion.time.strftime("%Y-%m-%d %H:%M:%S")
        print(f'\n[{formatted_time}] [{suggestion.category.name}]  {suggestion.message}{'\n\n>' if reset_input else '\n'}', end='')
