"""Command line interface view"""

from string import Template
from typing import Any

from rich import print

from ski_lift import __version__
from ski_lift.core.command.result.object import (AbortCommandResult,
                                                 ChangeStateCommandResult,
                                                 CommandResult,
                                                 DisplayStatusCommandResult,
                                                 EmergencyStopCommandResult,
                                                 InsertCardCommandResult,
                                                 RemoveCardCommandResult,
                                                 MessageReportCommandResult)
from ski_lift.core.remote.suggestion.suggestion import Suggestion, SuggestionCategory
from ski_lift.core.view.base_view import BaseView

from ski_lift.core.controller import Controller
from datetime import datetime

DEFAULT_HELP_TEXT: str = """
[yellow]Available commands:

    insert_card [blue]<card_id>[/blue]
        - [cyan]Inserts a card into the system, using the specified [blue]<card_id>[/blue].[/cyan]

    remove_card
        - Removes the currently inserted card from the system.

    change_state [blue]<state>[/blue]
        - [cyan]Changes the engine state to the specified [blue]<state>[/blue].[/cyan]
        - [cyan]Valid states include [orange3]MAX_STEAM[/orange3], [orange3]FULL_STEAM[/orange3], [orange3]HALF_STEAM[/orange3], and [orange3]STOPPED[/orange3].[/cyan]

    display_status
        - [cyan]Displays the current status of the lift system.[/cyan]

    emergency_stop
        - [cyan]Stop the ski lift in a case of an emergency.[/cyan]

    abort [blue]<command_id>[/blue]
        - [cyan]Aborts a delayed command with the specified [blue]<command_id>[/blue].[/cyan]

    report [blue]<severity> <message>[/blue]
        - [cyan]Send a report to the central room.[/cyan]
        - [cyan]Possible severities are [orange3]INFO[/orange3], [orange3]WARNING[/orange3] and [orange3]DANGER[/orange3].[/cyan]

    suggestion_level [blue]<severity>[/blue]
        - [cyan]Suggestions with severities equal to or greater than the selected level will be displayed.[/cyan]
        - [cyan]Order is [orange3]INFO[/orange3] < [orange3]WARNING[/orange3] < [orange3]DANGER[/orange3].[/cyan]
        - [cyan]If you set it to NONE, no suggestions will be displayed.[/cyan]

    help
        - [cyan]Displays this help message listing all available commands.[/yellow][/cyan]
"""

WELCOME_TEXT_TEMPLATE: str = """
 __                      ___           _
/ _\\_ __   _____      __/ _ \\___  __ _| | __
\\ \\| '_ \\ / _ \\ \\ /\\ / / /_)/ _ \\/ _` | |/ /
_\\ \\ | | | (_) \\ V  V / ___/  __/ (_| |   <
\\__/_| |_|\\___/ \\_/\\_/\\/    \\___|\\__,_|_|\\_\\

version: [orange3]$version[/orange3]
lift id: [orange3]$lift_id$current_user[/orange3]
"""

class CommandLineInterfaceView(BaseView):

    def __init__(self, controller: Controller, *args, **kwargs) -> None:
        self._stopped = False
        self._connection_error_count = 0
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
            self._stopped = True
            print('Exiting...')
            print('Closing connections ...')

    def start_handling_cli_input(self) -> None:
        print(self.welcome_text)
        while True:
            user_input = input('\n> ').lower().split()
            if not user_input:
                continue
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
                    case 'report': self.message_report(args[0], ' '.join(args[1:]))
                    case 'abort': self.abort_command(*args)
                    case 'help': print(DEFAULT_HELP_TEXT)
                    case 'exit': break
                    case _: raise self.UnsupportedCommand()
            except self.UnsupportedCommand:
                print(
                    f'Did not recognize "{command_name}" command. Type "help" to display the available commands.'
                )
            except Exception as exc:
                print(f'Incorrect arguments for command "{command_name}". Type "help" to display correct usage.')
        self._stopped = True

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
        self.handle_result(result, 'REPORT SENT' if self._connection_error_count == 0 else 'REPORT PENDING')

    def handle_result(self, result: CommandResult, message_on_success: str):
        if result.outcome == CommandResult.OutCome.DELAYED:
            print(f'Type "abort {result.command.id}" to abort it.')
        elif result.is_successful:
            print(f'[green]{message_on_success}[/green]')
        else:
            print(f'[red]{str(result.exception)}[/red]')

        if result.command.delay != 0:
            print('\n> ', end='')

    def on_connected(self, exchange: str):
        self._connection_error_count = 0
        self.display_suggestion(
            Suggestion(
                sender_card_number='system',
                time=datetime.now(),
                category=SuggestionCategory.INFO,
                message=f'Connected to "{exchange}" channel.',
            ),
        )

    def on_closed(self, exchange: str):
        self.display_suggestion(
            Suggestion(
                sender_card_number='system',
                time=datetime.now(),
                category=SuggestionCategory.WARNING,
                message=f'Connection to "{exchange}" was closed.',
            ),
        )

    def on_connected_error(self, exchange: str):
        if self._connection_error_count < 2:
            self.display_suggestion(
                Suggestion(
                    sender_card_number='system',
                    time=datetime.now(),
                    category=SuggestionCategory.WARNING,
                    message=f'Could not connect "{exchange}" channel.',
                ),
            )
        self._connection_error_count += 1


    def display_suggestion(self, suggestion: Suggestion, reset_input: bool = True) -> None:
        if self._should_display_suggestion(suggestion):
            print()
            print(suggestion.as_rich_text)
            if reset_input:
                print('\n> ', end='')

    def _should_display_suggestion(self, suggestion: Suggestion):
        severity_is_allowed: bool = suggestion.category.name in self._suggestion_level
        return severity_is_allowed and not self._stopped