"""Base view."""

from abc import abstractmethod
from typing import Optional

from ski_lift.core.command.command_panel import CommandPanel
from ski_lift.core.controller import Controller
from ski_lift.core.monitor.result.result_monitor import CommandResultMonitor
from ski_lift.core.remote.suggestion.suggestion import Suggestion


class BaseView(CommandPanel, CommandResultMonitor):
    """Base view.
    
    Abstract base class for views.
    
    A view is responsible for reading user inputs, executing corresponding
    commands on the controller, and displaying the controller's results.

    To achieve this functionality, views inherit from the CommandPanel class,
    which enables the creation and execution of commands on a controller.
    Additionally, they inherit from the CommandResultMonitor class, allowing
    them to receive results and provide appropriate feedback to the user.
    """ 

    def __init__(self, controller: Controller, *args, **kwargs) -> None:
        controller.register_result_monitor(self)
        super().__init__(controller=controller, *args, **kwargs)

    @property
    def inserted_card(self) -> Optional[str]:
        return self._controller.inserted_card
    
    @property
    def lift_id(self) -> str:
        return self._controller.lift_id

    @abstractmethod
    def start_handling_user_inputs(self) -> None:
        """Start handling user inputs.

        This function is responsible for starting the process of handling user
        inputs. It typically blocks the main thread.
        """

    @abstractmethod
    def display_suggestion(self, suggestion: Suggestion) -> None:
        """Display suggestion.
        
        This function is responsible for displaying a suggestion on the user
        interface.
        """