from ski_lift.app.entity.ski_lift_authorizer import SkiLiftAuthorizer
from ski_lift.app.entity.ski_lift_controller import SkiLiftController
from ski_lift.core.auth.authenticator.in_memory_authenticator import InMemoryAuthenticator
from ski_lift.core.engine import Engine
from ski_lift.core.monitor.command_file_monitor import CommandFileMonitor
from ski_lift.core.remote.suggestion.test_remote_emergency_stopper import TestEmergencyStopper
from ski_lift.core.remote.suggestion.test_suggestion_forwarder import TestSuggestionForwarder
from ski_lift.core.view.cli_view import CommandLineInterfaceView
import sys


def main() -> int:
    # create an example authenticator and register a card number
    authenticator = InMemoryAuthenticator()
    authenticator.add('secret')

    # create a controller which needs an engine and an authorizer
    controller = SkiLiftController(engine=Engine(), authorizer=SkiLiftAuthorizer(authenticator=authenticator))

    # create a logger and register it as a descriptor (command request)
    # and result monitor
    command_logger = CommandFileMonitor()
    controller.register_descriptor_monitor(command_logger)
    controller.register_result_monitor(command_logger)

    # create a cli view with the controller and start accepting user input
    cli = CommandLineInterfaceView(controller=controller)

    # test suggestion forwarder
    suggestion_handler = TestSuggestionForwarder(view=cli)
    remote_emergency_stopper = TestEmergencyStopper(view=cli)

    # start thread that handles delayed commands
    controller.start()
    # start thread that sends dummy suggestions
    #suggestion_handler.start()
    # start thread that sends emergency stops every minute
    #remote_emergency_stopper.start()
    cli.start_handling_user_inputs()

    suggestion_handler.stop()
    remote_emergency_stopper.stop()
    controller.stop()
    return 0


if __name__ == '__main__':
    sys.exit(main())
